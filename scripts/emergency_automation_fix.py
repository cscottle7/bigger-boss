#!/usr/bin/env python3
"""
Emergency Automation Fix - Immediate Solution
Addresses the complete absence of automation execution triggers.

This script provides immediate relief by manually triggering the automation workflow
that should have been running automatically.

Usage:
    python scripts/emergency_automation_fix.py --client=australiandentalspecialists_com
    python scripts/emergency_automation_fix.py --test-workflow
    python scripts/emergency_automation_fix.py --enable-monitoring
"""

import sys
import os
import json
import subprocess
import asyncio
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict
import argparse

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class EmergencyAutomationFix:
    """Emergency automation fix to restore automated delivery workflows."""

    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.root_dir = self.script_dir.parent
        self.clients_dir = self.root_dir / "clients"

        # Tool paths
        self.orchestrator = self.script_dir / "automation" / "workflow_orchestrator.py"
        self.watcher = self.script_dir / "automation" / "file_system_watcher.py"
        self.audit_tool = self.script_dir / "pre_delivery_audit.py"

    def check_automation_infrastructure(self) -> Dict:
        """Check if all automation components are available."""
        components = {
            'orchestrator': self.orchestrator.exists(),
            'watcher': self.watcher.exists(),
            'audit_tool': self.audit_tool.exists(),
            'clients_dir': self.clients_dir.exists()
        }

        logger.info("Automation infrastructure check:")
        for component, available in components.items():
            status = "Available" if available else "Missing"
            logger.info(f"  {component}: {status}")

        return components

    async def trigger_workflow_for_client(self, client_domain: str) -> Dict:
        """Manually trigger automation workflow for specific client."""
        try:
            client_path = self.clients_dir / client_domain
            if not client_path.exists():
                return {
                    'success': False,
                    'error': f'Client folder not found: {client_path}'
                }

            # Find a markdown file to trigger with
            md_files = list(client_path.rglob("*.md"))
            if not md_files:
                return {
                    'success': False,
                    'error': f'No markdown files found in {client_path}'
                }

            trigger_file = md_files[0]  # Use first found markdown file
            logger.info(f"Triggering automation workflow for client: {client_domain}")
            logger.info(f"Using trigger file: {trigger_file}")

            # Execute automation orchestrator
            cmd = [
                sys.executable,
                str(self.orchestrator),
                "--trigger-file", str(trigger_file)
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )

            if result.returncode == 0:
                try:
                    workflow_result = json.loads(result.stdout)
                    logger.info("Automation workflow completed successfully")

                    # Log phase results
                    phases = workflow_result.get('phases', {})
                    for phase_name, phase_result in phases.items():
                        status = "Success" if phase_result.get('success') else "Failed"
                        logger.info(f"  {phase_name}: {status}")

                    return {
                        'success': True,
                        'workflow_result': workflow_result,
                        'trigger_file': str(trigger_file)
                    }

                except json.JSONDecodeError:
                    return {
                        'success': True,
                        'output': result.stdout,
                        'trigger_file': str(trigger_file)
                    }
            else:
                return {
                    'success': False,
                    'error': result.stderr,
                    'output': result.stdout
                }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def run_audit_for_client(self, client_domain: str) -> Dict:
        """Run pre-delivery audit for specific client."""
        try:
            client_path = self.clients_dir / client_domain
            if not client_path.exists():
                return {
                    'success': False,
                    'error': f'Client folder not found: {client_path}'
                }

            # Find a file to audit with
            md_files = list(client_path.rglob("*.md"))
            if not md_files:
                return {
                    'success': False,
                    'error': f'No markdown files found in {client_path}'
                }

            trigger_file = md_files[0]
            logger.info(f"Running audit for client: {client_domain}")

            # Execute audit with auto-generation
            cmd = [
                sys.executable,
                str(self.audit_tool),
                str(trigger_file),
                "--auto-generate"
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )

            return {
                'success': result.returncode == 0,
                'output': result.stdout,
                'error': result.stderr if result.returncode != 0 else None
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def enable_continuous_monitoring(self) -> Dict:
        """Enable continuous file system monitoring."""
        try:
            logger.info("Starting continuous file system monitoring...")

            # Check if watchdog is available
            try:
                import watchdog
                use_watchdog = True
                logger.info("Using watchdog for file system monitoring")
            except ImportError:
                use_watchdog = False
                logger.info("Watchdog not available, using polling mode")

            # Start file system watcher
            cmd = [sys.executable, str(self.watcher), "--monitor"]
            if not use_watchdog:
                cmd.append("--polling-only")

            logger.info("File system monitoring started - monitoring clients/ folder")
            logger.info("Press Ctrl+C to stop monitoring")

            # Start monitoring process
            process = subprocess.Popen(cmd)

            try:
                process.wait()
            except KeyboardInterrupt:
                logger.info("Stopping file system monitoring...")
                process.terminate()
                process.wait()

            return {'success': True, 'message': 'Monitoring stopped'}

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def generate_automation_status_report(self) -> Dict:
        """Generate comprehensive status report of automation systems."""
        report = {
            'timestamp': datetime.now().isoformat(),
            'infrastructure': self.check_automation_infrastructure(),
            'clients': []
        }

        # Check each client folder
        for client_dir in self.clients_dir.iterdir():
            if client_dir.is_dir() and not client_dir.name.startswith('.'):
                client_info = {
                    'domain': client_dir.name,
                    'path': str(client_dir),
                    'md_files': len(list(client_dir.rglob("*.md"))),
                    'docx_files': len(list(client_dir.rglob("*.docx"))),
                    'has_project_overview': (client_dir / "PROJECT_OVERVIEW.md").exists(),
                    'has_automation_log': (client_dir / "automation_activity.json").exists()
                }
                report['clients'].append(client_info)

        return report

async def main():
    """Main entry point for emergency automation fix."""
    parser = argparse.ArgumentParser(
        description='Emergency Automation Fix - Restore automated delivery workflows'
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--client',
        type=str,
        help='Trigger automation workflow for specific client'
    )
    group.add_argument(
        '--test-workflow',
        action='store_true',
        help='Test automation workflow with Australian Dental Specialists'
    )
    group.add_argument(
        '--enable-monitoring',
        action='store_true',
        help='Enable continuous file system monitoring'
    )
    group.add_argument(
        '--audit-only',
        type=str,
        help='Run audit only for specific client'
    )
    group.add_argument(
        '--status-report',
        action='store_true',
        help='Generate automation status report'
    )

    args = parser.parse_args()

    # Create emergency fix instance
    fix = EmergencyAutomationFix()

    # Check infrastructure first
    infrastructure = fix.check_automation_infrastructure()
    missing_components = [k for k, v in infrastructure.items() if not v]

    if missing_components:
        logger.error(f"Missing components: {missing_components}")
        print("Cannot proceed - required automation components missing")
        sys.exit(1)

    print("All automation components available")

    if args.client:
        # Trigger workflow for specific client
        result = await fix.trigger_workflow_for_client(args.client)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(0 if result['success'] else 1)

    elif args.test_workflow:
        # Test with Australian Dental Specialists
        result = await fix.trigger_workflow_for_client('australiandentalspecialists_com')
        print("Testing automation workflow with Australian Dental Specialists:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(0 if result['success'] else 1)

    elif args.enable_monitoring:
        # Enable continuous monitoring
        result = fix.enable_continuous_monitoring()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(0 if result['success'] else 1)

    elif args.audit_only:
        # Run audit only
        result = fix.run_audit_for_client(args.audit_only)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(0 if result['success'] else 1)

    elif args.status_report:
        # Generate status report
        report = fix.generate_automation_status_report()
        print("Automation Status Report:")
        print(json.dumps(report, indent=2, ensure_ascii=False))
        sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())