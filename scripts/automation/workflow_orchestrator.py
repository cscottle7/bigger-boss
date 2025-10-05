#!/usr/bin/env python3
"""
Emergency Automation Orchestrator
Fixes the complete absence of automation execution triggers in the delivery workflow.

This script provides the missing automation layer that connects all existing functional tools:
- Pre-delivery audit and missing file generation
- Document conversion to .docx format
- Google Drive upload with rclone
- Activity tracking and compliance monitoring

Usage:
    python scripts/automation/workflow_orchestrator.py --trigger-file="path/to/client/file.md"
    python scripts/automation/workflow_orchestrator.py --client="client_domain" --full-audit
"""

import sys
import os
import json
import subprocess
import logging
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import argparse

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/automation_orchestrator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AutomationOrchestrator:
    """
    Emergency automation orchestrator that fixes the missing execution layer.
    Connects all existing functional tools through automated workflow execution.
    """

    def __init__(self):
        self.script_dir = Path(__file__).parent.parent
        self.root_dir = self.script_dir.parent
        self.clients_dir = self.root_dir / "clients"

        # Tool paths
        self.audit_tool = self.script_dir / "pre_delivery_audit.py"
        self.converter = self.script_dir / "convert_my_docs.py"
        self.uploader = self.script_dir / "gdrive_upload.py"
        self.tracker = self.script_dir / "hooks" / "client_activity_tracker.py"

        # Ensure logs directory exists
        (self.root_dir / "logs").mkdir(exist_ok=True)

    def get_client_root_path(self, trigger_file_path: str) -> Optional[Path]:
        """Extract client root directory from any file path within the client folder."""
        try:
            trigger_path = Path(trigger_file_path)
            path_parts = trigger_path.parts

            # Find 'clients' in path
            if 'clients' in path_parts:
                clients_index = path_parts.index('clients')
                if clients_index + 1 < len(path_parts):
                    client_name = path_parts[clients_index + 1]
                    client_root = self.clients_dir / client_name
                    return client_root if client_root.exists() else None

            return None
        except Exception as e:
            logger.error(f"Error extracting client root path: {e}")
            return None

    async def run_pre_delivery_audit(self, trigger_file_path: str) -> Dict:
        """Execute pre-delivery audit with auto-generation of missing files."""
        try:
            logger.info(f"Running pre-delivery audit for: {trigger_file_path}")

            # Run audit with auto-generation
            cmd = [
                sys.executable,
                str(self.audit_tool),
                trigger_file_path,
                "--auto-generate"
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )

            if result.returncode == 0:
                logger.info("Pre-delivery audit completed successfully")
                return {
                    'success': True,
                    'stdout': result.stdout,
                    'stderr': result.stderr
                }
            else:
                logger.error(f"Pre-delivery audit failed: {result.stderr}")
                return {
                    'success': False,
                    'error': result.stderr,
                    'stdout': result.stdout
                }

        except Exception as e:
            logger.error(f"Error running pre-delivery audit: {e}")
            return {'success': False, 'error': str(e)}

    async def convert_client_files_to_docx(self, trigger_file_path: str) -> Dict:
        """Convert all client markdown files to .docx format."""
        try:
            client_root = self.get_client_root_path(trigger_file_path)
            if not client_root:
                return {'success': False, 'error': 'Could not determine client root path'}

            logger.info(f"Converting client files to .docx for: {client_root}")

            # Check if converter exists
            if not self.converter.exists():
                logger.warning(f"Converter not found at {self.converter}, skipping conversion")
                return {'success': True, 'skipped': 'Converter not available'}

            # Run conversion for all .md files in client folder
            md_files = list(client_root.rglob("*.md"))
            conversion_results = []

            for md_file in md_files:
                try:
                    cmd = [sys.executable, str(self.converter), str(md_file)]
                    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')

                    conversion_results.append({
                        'file': str(md_file),
                        'success': result.returncode == 0,
                        'output': result.stdout,
                        'error': result.stderr if result.returncode != 0 else None
                    })

                except Exception as e:
                    conversion_results.append({
                        'file': str(md_file),
                        'success': False,
                        'error': str(e)
                    })

            successful_conversions = [r for r in conversion_results if r['success']]
            failed_conversions = [r for r in conversion_results if not r['success']]

            logger.info(f"Conversion completed: {len(successful_conversions)} success, {len(failed_conversions)} failed")

            return {
                'success': len(failed_conversions) == 0,
                'total_files': len(md_files),
                'successful': len(successful_conversions),
                'failed': len(failed_conversions),
                'results': conversion_results
            }

        except Exception as e:
            logger.error(f"Error converting client files: {e}")
            return {'success': False, 'error': str(e)}

    async def upload_client_files(self, trigger_file_path: str) -> Dict:
        """Upload client files to Google Drive using rclone."""
        try:
            client_root = self.get_client_root_path(trigger_file_path)
            if not client_root:
                return {'success': False, 'error': 'Could not determine client root path'}

            logger.info(f"Uploading client files to Google Drive for: {client_root}")

            # Check if uploader exists
            if not self.uploader.exists():
                logger.warning(f"Uploader not found at {self.uploader}, skipping upload")
                return {'success': True, 'skipped': 'Uploader not available'}

            # Run Google Drive upload with correct command structure
            cmd = [sys.executable, str(self.uploader), 'folder', str(client_root)]
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')

            if result.returncode == 0:
                logger.info("Google Drive upload completed successfully")
                return {
                    'success': True,
                    'stdout': result.stdout,
                    'stderr': result.stderr
                }
            else:
                logger.error(f"Google Drive upload failed: {result.stderr}")
                return {
                    'success': False,
                    'error': result.stderr,
                    'stdout': result.stdout
                }

        except Exception as e:
            logger.error(f"Error uploading client files: {e}")
            return {'success': False, 'error': str(e)}

    async def record_automation_activity(self, trigger_file_path: str, workflow_results: Dict) -> Dict:
        """Record automation activity for tracking and reporting."""
        try:
            client_root = self.get_client_root_path(trigger_file_path)
            if not client_root:
                return {'success': False, 'error': 'Could not determine client root path'}

            # Create automation log entry
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'trigger_file': trigger_file_path,
                'client_root': str(client_root),
                'workflow_results': workflow_results,
                'automation_version': '1.0.0'
            }

            # Save to client activity log
            activity_log_path = client_root / "automation_activity.json"

            # Load existing log or create new
            activity_log = []
            if activity_log_path.exists():
                try:
                    with open(activity_log_path, 'r', encoding='utf-8') as f:
                        activity_log = json.load(f)
                except Exception:
                    activity_log = []

            # Append new entry
            activity_log.append(log_entry)

            # Save updated log
            with open(activity_log_path, 'w', encoding='utf-8') as f:
                json.dump(activity_log, f, indent=2, ensure_ascii=False)

            logger.info(f"Automation activity recorded for: {client_root}")
            return {'success': True, 'log_file': str(activity_log_path)}

        except Exception as e:
            logger.error(f"Error recording automation activity: {e}")
            return {'success': False, 'error': str(e)}

    async def execute_complete_workflow(self, trigger_file_path: str) -> Dict:
        """Execute the complete end-to-end automation workflow."""
        workflow_start_time = datetime.now()
        logger.info(f"Starting complete automation workflow for: {trigger_file_path}")

        try:
            workflow_results = {
                'trigger_file': trigger_file_path,
                'start_time': workflow_start_time.isoformat(),
                'phases': {}
            }

            # Phase 1: Pre-delivery audit and missing file generation
            logger.info("Phase 1: Running pre-delivery audit with auto-generation")
            audit_result = await self.run_pre_delivery_audit(trigger_file_path)
            workflow_results['phases']['audit'] = audit_result

            if not audit_result['success']:
                logger.error("Phase 1 failed - audit unsuccessful")
                workflow_results['success'] = False
                workflow_results['failed_at'] = 'audit'
                return workflow_results

            # Phase 2: Convert all markdown files to .docx
            logger.info("Phase 2: Converting files to .docx format")
            conversion_result = await self.convert_client_files_to_docx(trigger_file_path)
            workflow_results['phases']['conversion'] = conversion_result

            # Phase 3: Upload to Google Drive (even if conversion partially failed)
            logger.info("Phase 3: Uploading files to Google Drive")
            upload_result = await self.upload_client_files(trigger_file_path)
            workflow_results['phases']['upload'] = upload_result

            # Phase 4: Record automation activity
            logger.info("Phase 4: Recording automation activity")
            activity_result = await self.record_automation_activity(trigger_file_path, workflow_results)
            workflow_results['phases']['activity_recording'] = activity_result

            # Determine overall success
            critical_phases_success = (
                audit_result['success'] and
                (upload_result['success'] or upload_result.get('skipped'))
            )

            workflow_results['success'] = critical_phases_success
            workflow_results['end_time'] = datetime.now().isoformat()
            workflow_results['duration_seconds'] = (datetime.now() - workflow_start_time).total_seconds()

            if critical_phases_success:
                logger.info(f"Complete automation workflow succeeded in {workflow_results['duration_seconds']:.2f}s")
            else:
                logger.error(f"Complete automation workflow failed after {workflow_results['duration_seconds']:.2f}s")

            return workflow_results

        except Exception as e:
            logger.error(f"Critical error in automation workflow: {e}")
            return {
                'success': False,
                'error': str(e),
                'trigger_file': trigger_file_path,
                'start_time': workflow_start_time.isoformat(),
                'end_time': datetime.now().isoformat()
            }

async def main():
    """Main entry point for automation orchestrator."""
    parser = argparse.ArgumentParser(
        description='Emergency Automation Orchestrator - Fixes missing execution triggers'
    )
    parser.add_argument(
        '--trigger-file',
        required=True,
        help='Path to the file that triggered the automation workflow'
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

    # Create orchestrator and execute workflow
    orchestrator = AutomationOrchestrator()
    result = await orchestrator.execute_complete_workflow(args.trigger_file)

    # Output results
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # Exit with appropriate code
    sys.exit(0 if result.get('success', False) else 1)

if __name__ == "__main__":
    asyncio.run(main())