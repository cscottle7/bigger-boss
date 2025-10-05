#!/usr/bin/env python3
"""
File System Watcher for Automated Client Delivery Workflow
Provides the missing automation execution layer that monitors client content creation
and triggers the complete automation workflow.

This solves the root cause: absence of automation triggers despite functional tools.

Features:
- Monitors clients/ folder for new .md files
- Triggers complete automation workflow on content creation
- Handles file modifications with debouncing
- Provides robust error handling and recovery
- Integrates with existing functional tools

Usage:
    python scripts/automation/file_system_watcher.py --monitor
    python scripts/automation/file_system_watcher.py --test-client=client_domain
"""

import sys
import os
import time
import threading
import asyncio
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Set, Optional
import argparse
import json
import subprocess

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/file_system_watcher.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    logger.warning("watchdog not available - falling back to polling mode")

class ClientContentWatcher(FileSystemEventHandler):
    """
    File system event handler that monitors client content creation
    and triggers automated delivery workflows.
    """

    def __init__(self, orchestrator_path: Path):
        super().__init__()
        self.orchestrator_path = orchestrator_path
        self.processing_queue: Set[str] = set()
        self.last_processed: Dict[str, datetime] = {}
        self.debounce_seconds = 5

    def should_process_file(self, file_path: str) -> bool:
        """Determine if file should trigger automation workflow."""
        path = Path(file_path)

        # Must be in clients folder
        if 'clients' not in path.parts:
            return False

        # Must be markdown file
        if path.suffix != '.md':
            return False

        # Skip temporary and system files
        if any(part.startswith('.') for part in path.parts):
            return False

        if any(part in ['temp', 'tmp', '__pycache__'] for part in path.parts):
            return False

        # Debouncing - avoid processing same file too frequently
        now = datetime.now()
        last_time = self.last_processed.get(file_path)
        if last_time and (now - last_time).total_seconds() < self.debounce_seconds:
            return False

        return True

    def on_created(self, event):
        """Handle file creation events."""
        if event.is_directory:
            return

        file_path = event.src_path
        if self.should_process_file(file_path):
            logger.info(f"New client content detected: {file_path}")
            self.trigger_automation_workflow(file_path)

    def on_modified(self, event):
        """Handle file modification events with debouncing."""
        if event.is_directory:
            return

        file_path = event.src_path
        if self.should_process_file(file_path):
            logger.info(f"Client content modified: {file_path}")
            # Delay processing to allow for multiple quick modifications
            threading.Timer(self.debounce_seconds, self.trigger_automation_workflow, [file_path]).start()

    def trigger_automation_workflow(self, file_path: str):
        """Trigger the complete automation workflow for the given file."""
        try:
            # Prevent duplicate processing
            if file_path in self.processing_queue:
                logger.debug(f"Already processing {file_path}, skipping")
                return

            self.processing_queue.add(file_path)
            self.last_processed[file_path] = datetime.now()

            logger.info(f"Triggering automation workflow for: {file_path}")

            # Execute automation orchestrator
            cmd = [
                sys.executable,
                str(self.orchestrator_path),
                "--trigger-file", file_path
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )

            if result.returncode == 0:
                logger.info(f"Automation workflow completed successfully for: {file_path}")
                try:
                    workflow_result = json.loads(result.stdout)
                    if workflow_result.get('success'):
                        logger.info(f"Workflow phases completed: {list(workflow_result.get('phases', {}).keys())}")
                    else:
                        logger.error(f"Workflow failed: {workflow_result.get('error', 'Unknown error')}")
                except json.JSONDecodeError:
                    logger.info("Workflow completed but output not in JSON format")
            else:
                logger.error(f"Automation workflow failed for {file_path}: {result.stderr}")

        except Exception as e:
            logger.error(f"Error triggering automation workflow for {file_path}: {e}")
        finally:
            # Remove from processing queue
            self.processing_queue.discard(file_path)

class FileSystemWatcherService:
    """
    Service that provides file system monitoring for automated client delivery.
    Implements both watchdog and polling-based monitoring for maximum compatibility.
    """

    def __init__(self):
        self.script_dir = Path(__file__).parent.parent
        self.root_dir = self.script_dir.parent
        self.clients_dir = self.root_dir / "clients"
        self.orchestrator_path = self.script_dir / "automation" / "workflow_orchestrator.py"

        # Ensure required directories exist
        (self.root_dir / "logs").mkdir(exist_ok=True)
        self.clients_dir.mkdir(exist_ok=True)

        self.observer = None
        self.is_monitoring = False

    def start_watchdog_monitoring(self):
        """Start monitoring using watchdog library (preferred method)."""
        if not WATCHDOG_AVAILABLE:
            raise RuntimeError("watchdog library not available")

        try:
            event_handler = ClientContentWatcher(self.orchestrator_path)
            self.observer = Observer()
            self.observer.schedule(event_handler, str(self.clients_dir), recursive=True)
            self.observer.start()
            self.is_monitoring = True

            logger.info(f"Started watchdog monitoring of: {self.clients_dir}")
            return True

        except Exception as e:
            logger.error(f"Failed to start watchdog monitoring: {e}")
            return False

    def start_polling_monitoring(self, check_interval: int = 10):
        """Start monitoring using polling (fallback method)."""
        logger.info(f"Starting polling-based monitoring (interval: {check_interval}s)")

        def polling_loop():
            last_scan_time = datetime.now() - timedelta(seconds=check_interval)

            while self.is_monitoring:
                try:
                    current_time = datetime.now()

                    # Scan for files created/modified since last scan
                    for md_file in self.clients_dir.rglob("*.md"):
                        try:
                            file_mtime = datetime.fromtimestamp(md_file.stat().st_mtime)
                            if file_mtime > last_scan_time:
                                logger.info(f"Detected file change: {md_file}")

                                # Create mock event handler to reuse logic
                                handler = ClientContentWatcher(self.orchestrator_path)
                                if handler.should_process_file(str(md_file)):
                                    handler.trigger_automation_workflow(str(md_file))

                        except Exception as e:
                            logger.error(f"Error checking file {md_file}: {e}")

                    last_scan_time = current_time
                    time.sleep(check_interval)

                except Exception as e:
                    logger.error(f"Error in polling loop: {e}")
                    time.sleep(check_interval)

        # Start polling in background thread
        polling_thread = threading.Thread(target=polling_loop, daemon=True)
        polling_thread.start()
        self.is_monitoring = True

        logger.info("Polling monitoring started successfully")
        return True

    def start_monitoring(self, prefer_watchdog: bool = True):
        """Start file system monitoring using the best available method."""
        if prefer_watchdog and WATCHDOG_AVAILABLE:
            if self.start_watchdog_monitoring():
                return True
            else:
                logger.warning("Watchdog monitoring failed, falling back to polling")

        return self.start_polling_monitoring()

    def stop_monitoring(self):
        """Stop file system monitoring."""
        self.is_monitoring = False

        if self.observer:
            self.observer.stop()
            self.observer.join()
            logger.info("Watchdog monitoring stopped")
        else:
            logger.info("Polling monitoring stopped")

    def test_workflow_with_client(self, client_domain: str) -> bool:
        """Test the automation workflow with a specific client."""
        try:
            client_path = self.clients_dir / client_domain
            if not client_path.exists():
                logger.error(f"Client folder not found: {client_path}")
                return False

            # Find a markdown file to test with
            md_files = list(client_path.rglob("*.md"))
            if not md_files:
                logger.error(f"No markdown files found in client folder: {client_path}")
                return False

            test_file = md_files[0]
            logger.info(f"Testing automation workflow with: {test_file}")

            # Create event handler and trigger workflow
            handler = ClientContentWatcher(self.orchestrator_path)
            handler.trigger_automation_workflow(str(test_file))

            return True

        except Exception as e:
            logger.error(f"Error testing workflow with client {client_domain}: {e}")
            return False

def main():
    """Main entry point for file system watcher service."""
    parser = argparse.ArgumentParser(
        description='File System Watcher for Automated Client Delivery'
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--monitor',
        action='store_true',
        help='Start continuous monitoring of client content'
    )
    group.add_argument(
        '--test-client',
        type=str,
        help='Test automation workflow with specific client'
    )

    parser.add_argument(
        '--polling-only',
        action='store_true',
        help='Use polling mode instead of watchdog (for compatibility)'
    )
    parser.add_argument(
        '--log-level',
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        help='Logging level'
    )

    args = parser.parse_args()

    # Set logging level
    logging.getLogger().setLevel(getattr(logging, args.log_level))

    # Create watcher service
    watcher_service = FileSystemWatcherService()

    if args.test_client:
        # Test mode
        logger.info(f"Testing automation workflow with client: {args.test_client}")
        success = watcher_service.test_workflow_with_client(args.test_client)
        sys.exit(0 if success else 1)

    elif args.monitor:
        # Monitoring mode
        try:
            logger.info("Starting file system watcher service")

            prefer_watchdog = not args.polling_only
            if watcher_service.start_monitoring(prefer_watchdog=prefer_watchdog):
                logger.info("File system monitoring active - Press Ctrl+C to stop")

                try:
                    if WATCHDOG_AVAILABLE and prefer_watchdog:
                        # Keep main thread alive for watchdog
                        while watcher_service.is_monitoring:
                            time.sleep(1)
                    else:
                        # Keep main thread alive for polling
                        while watcher_service.is_monitoring:
                            time.sleep(10)

                except KeyboardInterrupt:
                    logger.info("Received interrupt signal, stopping monitoring")

                watcher_service.stop_monitoring()
                logger.info("File system watcher service stopped")
                sys.exit(0)
            else:
                logger.error("Failed to start file system monitoring")
                sys.exit(1)

        except Exception as e:
            logger.error(f"Critical error in file system watcher: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()