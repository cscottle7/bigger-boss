#!/usr/bin/env python3
"""
Bigger Boss Agent System - Error Handler
Graceful error handling and recovery for system operations.
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ErrorHandler:
    """Centralized error handling and recovery system."""

    def __init__(self):
        self.log_dir = Path('logs')
        self.log_dir.mkdir(exist_ok=True)
        self.error_log_file = self.log_dir / 'errors.log'

    def handle_error(self, error_message: str, context: str = "", recovery: bool = True) -> Dict:
        """
        Handle system errors with logging and recovery options.

        Args:
            error_message: The error message
            context: Additional context about where the error occurred
            recovery: Whether to attempt recovery

        Returns:
            Error handling result
        """
        error_info = {
            'timestamp': datetime.now().isoformat(),
            'error_message': error_message,
            'context': context,
            'recovery_attempted': recovery,
            'recovery_successful': False,
            'recommendations': []
        }

        # Log the error
        self._log_error(error_info)

        # Attempt recovery if requested
        if recovery:
            recovery_result = self._attempt_recovery(error_message, context)
            error_info.update(recovery_result)

        # Generate recommendations
        error_info['recommendations'] = self._generate_recommendations(error_message, context)

        return error_info

    def _log_error(self, error_info: Dict) -> None:
        """Log error to file and console."""
        log_entry = {
            'timestamp': error_info['timestamp'],
            'level': 'ERROR',
            'message': error_info['error_message'],
            'context': error_info['context']
        }

        # Append to error log file
        with open(self.error_log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')

        # Also log to console
        logger.error(f"{error_info['error_message']} | Context: {error_info['context']}")

    def _attempt_recovery(self, error_message: str, context: str) -> Dict:
        """Attempt automatic recovery based on error type."""
        recovery_info = {
            'recovery_attempted': True,
            'recovery_successful': False,
            'recovery_actions': [],
            'recovery_message': ''
        }

        error_lower = error_message.lower()

        try:
            # File not found errors
            if 'file not found' in error_lower or 'no such file' in error_lower:
                recovery_info = self._recover_missing_file(error_message, context, recovery_info)

            # Permission errors
            elif 'permission denied' in error_lower or 'access denied' in error_lower:
                recovery_info = self._recover_permission_error(error_message, context, recovery_info)

            # Network/connection errors
            elif any(term in error_lower for term in ['connection', 'network', 'timeout', 'unreachable']):
                recovery_info = self._recover_network_error(error_message, context, recovery_info)

            # Import/module errors
            elif 'module not found' in error_lower or 'import error' in error_lower:
                recovery_info = self._recover_import_error(error_message, context, recovery_info)

            # API errors
            elif any(term in error_lower for term in ['api', 'rate limit', 'quota', 'unauthorized']):
                recovery_info = self._recover_api_error(error_message, context, recovery_info)

            # Disk space errors
            elif 'no space' in error_lower or 'disk full' in error_lower:
                recovery_info = self._recover_disk_space_error(error_message, context, recovery_info)

            else:
                recovery_info['recovery_message'] = 'No automatic recovery available for this error type'

        except Exception as e:
            recovery_info['recovery_message'] = f'Recovery attempt failed: {str(e)}'
            logger.error(f"Recovery attempt failed: {e}")

        return recovery_info

    def _recover_missing_file(self, error_message: str, context: str, recovery_info: Dict) -> Dict:
        """Attempt to recover from missing file errors."""
        recovery_info['recovery_actions'].append('Checking for file existence and creating if needed')

        # Try to extract file path from error message
        import re
        path_match = re.search(r'[\'"`]([^\'"`]+)[\'"`]', error_message)
        if path_match:
            file_path = Path(path_match.group(1))

            # Create parent directory if it doesn't exist
            if not file_path.parent.exists():
                try:
                    file_path.parent.mkdir(parents=True, exist_ok=True)
                    recovery_info['recovery_actions'].append(f'Created directory: {file_path.parent}')
                except Exception as e:
                    recovery_info['recovery_actions'].append(f'Failed to create directory: {e}')

            # Create empty file if it's a required file
            required_files = {
                '.env': 'JINA_API_KEY=your_api_key_here\n',
                'requirements.txt': '# Project dependencies\n',
                'README.md': '# Project Documentation\n',
                'package.json': '{"name": "project", "version": "1.0.0"}\n'
            }

            file_name = file_path.name
            if file_name in required_files:
                try:
                    file_path.write_text(required_files[file_name], encoding='utf-8')
                    recovery_info['recovery_actions'].append(f'Created template file: {file_path}')
                    recovery_info['recovery_successful'] = True
                    recovery_info['recovery_message'] = f'Successfully created missing file: {file_path}'
                except Exception as e:
                    recovery_info['recovery_actions'].append(f'Failed to create file: {e}')

        return recovery_info

    def _recover_permission_error(self, error_message: str, context: str, recovery_info: Dict) -> Dict:
        """Attempt to recover from permission errors."""
        recovery_info['recovery_actions'].append('Checking file permissions and ownership')

        # Check if running with sufficient privileges
        import os
        if os.name == 'nt':  # Windows
            recovery_info['recovery_message'] = 'Permission error on Windows. Try running as administrator.'
        else:  # Unix-like systems
            if os.geteuid() != 0:
                recovery_info['recovery_message'] = 'Permission error. Try running with sudo or check file ownership.'
            else:
                recovery_info['recovery_message'] = 'Permission error despite root access. Check file system permissions.'

        recovery_info['recovery_actions'].append('Permission check completed')
        return recovery_info

    def _recover_network_error(self, error_message: str, context: str, recovery_info: Dict) -> Dict:
        """Attempt to recover from network errors."""
        recovery_info['recovery_actions'].append('Attempting network connectivity check')

        try:
            import requests
            # Test basic connectivity
            response = requests.get('https://www.google.com', timeout=5)
            if response.status_code == 200:
                recovery_info['recovery_actions'].append('Basic internet connectivity confirmed')
                recovery_info['recovery_message'] = 'Network error may be service-specific. Try again later.'
            else:
                recovery_info['recovery_actions'].append('Internet connectivity issues detected')
                recovery_info['recovery_message'] = 'Network connectivity issues. Check internet connection.'
        except Exception:
            recovery_info['recovery_actions'].append('Network connectivity test failed')
            recovery_info['recovery_message'] = 'Network connectivity problems detected. Check internet connection.'

        return recovery_info

    def _recover_import_error(self, error_message: str, context: str, recovery_info: Dict) -> Dict:
        """Attempt to recover from import/module errors."""
        recovery_info['recovery_actions'].append('Attempting to install missing module')

        # Extract module name from error message
        import re
        module_match = re.search(r"No module named ['\"]([^'\"]+)['\"]", error_message)
        if module_match:
            module_name = module_match.group(1)
            recovery_info['recovery_actions'].append(f'Identified missing module: {module_name}')

            try:
                import subprocess
                import sys

                # Try to install the module
                result = subprocess.run([
                    sys.executable, '-m', 'pip', 'install', module_name
                ], capture_output=True, text=True, timeout=60)

                if result.returncode == 0:
                    recovery_info['recovery_successful'] = True
                    recovery_info['recovery_message'] = f'Successfully installed missing module: {module_name}'
                    recovery_info['recovery_actions'].append(f'Module {module_name} installed successfully')
                else:
                    recovery_info['recovery_message'] = f'Failed to install module {module_name}: {result.stderr}'
                    recovery_info['recovery_actions'].append(f'Module installation failed: {result.stderr}')

            except Exception as e:
                recovery_info['recovery_message'] = f'Module installation attempt failed: {str(e)}'
                recovery_info['recovery_actions'].append(f'Installation error: {e}')

        return recovery_info

    def _recover_api_error(self, error_message: str, context: str, recovery_info: Dict) -> Dict:
        """Attempt to recover from API errors."""
        recovery_info['recovery_actions'].append('Analyzing API error for recovery options')

        error_lower = error_message.lower()

        if 'rate limit' in error_lower or 'quota' in error_lower:
            recovery_info['recovery_message'] = 'API rate limit exceeded. Implement exponential backoff and retry.'
            recovery_info['recovery_actions'].append('Rate limiting detected - recommend retry with delay')

        elif 'unauthorized' in error_lower or 'authentication' in error_lower:
            recovery_info['recovery_message'] = 'API authentication failed. Check API keys and credentials.'
            recovery_info['recovery_actions'].append('Authentication error detected - check API keys')

        elif 'not found' in error_lower:
            recovery_info['recovery_message'] = 'API endpoint not found. Check API documentation for correct endpoints.'
            recovery_info['recovery_actions'].append('API endpoint error - verify URL and version')

        else:
            recovery_info['recovery_message'] = 'Generic API error. Check API status and documentation.'
            recovery_info['recovery_actions'].append('Generic API error - check service status')

        return recovery_info

    def _recover_disk_space_error(self, error_message: str, context: str, recovery_info: Dict) -> Dict:
        """Attempt to recover from disk space errors."""
        recovery_info['recovery_actions'].append('Checking disk space availability')

        try:
            import shutil
            import os

            # Check available disk space
            total, used, free = shutil.disk_usage(os.getcwd())
            free_gb = free // (1024**3)

            recovery_info['recovery_actions'].append(f'Available disk space: {free_gb} GB')

            if free_gb < 1:
                recovery_info['recovery_message'] = 'Critical: Less than 1GB free space. Clean up files immediately.'
            elif free_gb < 5:
                recovery_info['recovery_message'] = 'Warning: Low disk space. Consider cleaning up temporary files.'
            else:
                recovery_info['recovery_message'] = 'Disk space appears adequate. Error may be temporary or location-specific.'

            recovery_info['recovery_actions'].append('Disk space analysis completed')

        except Exception as e:
            recovery_info['recovery_message'] = f'Could not check disk space: {str(e)}'
            recovery_info['recovery_actions'].append(f'Disk space check failed: {e}')

        return recovery_info

    def _generate_recommendations(self, error_message: str, context: str) -> List[str]:
        """Generate recommendations based on error type."""
        recommendations = []
        error_lower = error_message.lower()

        # File-related recommendations
        if 'file not found' in error_lower:
            recommendations.extend([
                'Verify file path is correct',
                'Check if file has been moved or deleted',
                'Ensure proper file permissions',
                'Create missing directories if needed'
            ])

        # Permission-related recommendations
        elif 'permission denied' in error_lower:
            recommendations.extend([
                'Run with elevated privileges if necessary',
                'Check file ownership and permissions',
                'Ensure directory is writable',
                'Verify user has access to the resource'
            ])

        # Network-related recommendations
        elif any(term in error_lower for term in ['connection', 'network', 'timeout']):
            recommendations.extend([
                'Check internet connectivity',
                'Verify firewall settings',
                'Try again after a short delay',
                'Check if service is available'
            ])

        # Module/import recommendations
        elif 'module not found' in error_lower:
            recommendations.extend([
                'Install missing Python packages',
                'Check virtual environment activation',
                'Verify Python path configuration',
                'Update requirements.txt if needed'
            ])

        # API-related recommendations
        elif any(term in error_lower for term in ['api', 'rate limit', 'unauthorized']):
            recommendations.extend([
                'Check API key configuration',
                'Verify API endpoint URLs',
                'Implement rate limiting',
                'Check API service status'
            ])

        # General recommendations
        recommendations.extend([
            'Check system logs for additional details',
            'Restart the application if error persists',
            'Contact support if issue continues',
            'Document error for future reference'
        ])

        return recommendations

    def get_error_statistics(self, days: int = 7) -> Dict:
        """Get error statistics for the specified period."""
        stats = {
            'period_days': days,
            'total_errors': 0,
            'error_types': {},
            'error_contexts': {},
            'recovery_success_rate': 0,
            'common_errors': []
        }

        if not self.error_log_file.exists():
            return stats

        try:
            from datetime import datetime, timedelta
            cutoff_date = datetime.now() - timedelta(days=days)

            total_errors = 0
            successful_recoveries = 0
            error_messages = []

            with open(self.error_log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        log_entry = json.loads(line.strip())
                        error_date = datetime.fromisoformat(log_entry['timestamp'])

                        if error_date >= cutoff_date:
                            total_errors += 1
                            error_messages.append(log_entry['message'])

                            # Track error types
                            context = log_entry.get('context', 'unknown')
                            stats['error_contexts'][context] = stats['error_contexts'].get(context, 0) + 1

                            # Recovery tracking would need to be enhanced
                            # This is a simplified version

                    except (json.JSONDecodeError, KeyError, ValueError):
                        continue

            stats['total_errors'] = total_errors

            # Find common errors
            from collections import Counter
            error_counter = Counter(error_messages)
            stats['common_errors'] = [
                {'message': msg, 'count': count}
                for msg, count in error_counter.most_common(5)
            ]

        except Exception as e:
            logger.error(f"Error generating statistics: {e}")

        return stats


def main():
    """Main CLI function for error handling."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Handle system errors with recovery and recommendations'
    )

    parser.add_argument('error_message', help='Error message to handle')
    parser.add_argument('--context', help='Additional context about the error')
    parser.add_argument('--recovery', action='store_true', help='Attempt automatic recovery')
    parser.add_argument('--stats', type=int, help='Show error statistics for N days')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging')

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    handler = ErrorHandler()

    try:
        if args.stats:
            # Show error statistics
            stats = handler.get_error_statistics(args.stats)
            print(f"📊 Error Statistics (Last {stats['period_days']} days)")
            print(f"Total Errors: {stats['total_errors']}")

            if stats['error_contexts']:
                print(f"\nErrors by Context:")
                for context, count in sorted(stats['error_contexts'].items(), key=lambda x: x[1], reverse=True):
                    print(f"  • {context}: {count}")

            if stats['common_errors']:
                print(f"\nMost Common Errors:")
                for i, error in enumerate(stats['common_errors'], 1):
                    print(f"  {i}. {error['message']} ({error['count']} times)")

        else:
            # Handle the error
            result = handler.handle_error(
                args.error_message,
                args.context or "",
                args.recovery
            )

            print(f"🔥 Error Handler Results")
            print(f"Error: {result['error_message']}")

            if result['context']:
                print(f"Context: {result['context']}")

            if result['recovery_attempted']:
                recovery_status = "✅ Success" if result['recovery_successful'] else "❌ Failed"
                print(f"Recovery: {recovery_status}")

                if result.get('recovery_message'):
                    print(f"Recovery Message: {result['recovery_message']}")

                if result.get('recovery_actions'):
                    print("Recovery Actions:")
                    for action in result['recovery_actions']:
                        print(f"  • {action}")

            if result['recommendations']:
                print("Recommendations:")
                for rec in result['recommendations'][:5]:  # Show top 5
                    print(f"  • {rec}")

    except Exception as e:
        print(f"❌ Error in error handler: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()