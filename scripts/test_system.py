#!/usr/bin/env python3
"""
Bigger Boss Agent System - Comprehensive Testing Suite
Tests all core functionality including hooks, document processing, and integrations.

Usage: python test_system.py [--category=all|hooks|conversion|gdrive|jina]
"""

import argparse
import json
import logging
import os
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SystemTester:
    """Comprehensive system testing for Bigger Boss Agent System."""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.test_results = {}
        self.temp_dir = None

    def setup_test_environment(self) -> bool:
        """Set up test environment with temporary files and folders."""
        try:
            # Create temporary directory for tests
            self.temp_dir = tempfile.mkdtemp(prefix='bigger_boss_test_')
            logger.info(f"Created test environment: {self.temp_dir}")

            # Create test client structure
            test_client_dir = Path(self.temp_dir) / 'clients' / 'test_client_com_au'
            test_client_dir.mkdir(parents=True, exist_ok=True)

            # Create test folders
            folders = ['strategy', 'research', 'content', 'technical', 'implementation']
            for folder in folders:
                (test_client_dir / folder).mkdir(exist_ok=True)

            # Create test markdown file
            test_md_content = """# Test Content for Bigger Boss System

## Introduction
This is a test document to verify the **markdown to DOCX conversion** functionality.

### Key Features to Test
1. **Bold text** formatting
2. *Italic text* emphasis
3. [Links](https://example.com)
4. Code snippets: `print("hello world")`

### List Testing
- Bullet point one
- Bullet point two
- Bullet point three

### Quote Testing
> This is a blockquote to test formatting

### Table Testing
| Feature | Status | Notes |
|---------|--------|-------|
| Conversion | Testing | Markdown to DOCX |
| Upload | Testing | Google Drive integration |
| Quality | Testing | British English compliance |

## Australian English Compliance Test
- This document uses organisation (not organization)
- Content is optimised (not optimized) for quality
- We analyse (not analyze) the behaviour (not behavior)
- The colour (not color) scheme is centred (not centered)
- Price: $100 AUD (converted from USD references)

**Source:** [Test Document - System Validation](https://example.com/test) - September 2025
"""

            test_md_file = test_client_dir / 'content' / 'test_content.md'
            with open(test_md_file, 'w', encoding='utf-8') as f:
                f.write(test_md_content)

            logger.info("✅ Test environment setup complete")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to setup test environment: {e}")
            return False

    def test_hook_system(self) -> Dict[str, bool]:
        """Test hook system functionality."""
        logger.info("🔧 Testing hook system...")
        results = {}

        try:
            # Test 1: Verify hooks.json exists and is valid
            hooks_file = self.project_root / '.claude' / 'hooks.json'
            if hooks_file.exists():
                with open(hooks_file, 'r') as f:
                    hooks_config = json.load(f)
                    results['hooks_config_valid'] = isinstance(hooks_config.get('hooks'), dict)
                    logger.info("✅ Hook configuration file is valid")
            else:
                results['hooks_config_valid'] = False
                logger.error("❌ Hook configuration file not found")

            # Test 2: Verify hook scripts exist
            hook_scripts = [
                'scripts/md_to_docx.py',
                'scripts/gdrive_upload.py',
                'scripts/validate_client_structure.py',
                'scripts/validate_british_english.py'
            ]

            for script in hook_scripts:
                script_path = self.project_root / script
                script_name = script.replace('scripts/', '').replace('.py', '')
                results[f'hook_script_{script_name}'] = script_path.exists()

                if script_path.exists():
                    logger.info(f"✅ Hook script found: {script}")
                else:
                    logger.error(f"❌ Hook script missing: {script}")

            return results

        except Exception as e:
            logger.error(f"❌ Hook system test failed: {e}")
            return {'hook_system_error': False}

    def test_document_conversion(self) -> Dict[str, bool]:
        """Test markdown to DOCX conversion."""
        logger.info("📄 Testing document conversion...")
        results = {}

        try:
            if not self.temp_dir:
                results['conversion_no_test_env'] = False
                return results

            # Test markdown to DOCX conversion
            test_md_file = Path(self.temp_dir) / 'clients' / 'test_client_com_au' / 'content' / 'test_content.md'

            if test_md_file.exists():
                # Run conversion
                conversion_script = self.project_root / 'scripts' / 'md_to_docx.py'

                if conversion_script.exists():
                    cmd = [sys.executable, str(conversion_script), str(test_md_file)]
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

                    results['conversion_script_runs'] = result.returncode == 0

                    if result.returncode == 0:
                        # Check if DOCX file was created
                        docx_file = test_md_file.with_suffix('.docx')
                        results['docx_file_created'] = docx_file.exists()

                        if docx_file.exists():
                            logger.info(f"✅ DOCX file created: {docx_file}")
                            results['docx_file_size_valid'] = docx_file.stat().st_size > 1000  # At least 1KB
                        else:
                            logger.error("❌ DOCX file not created")
                    else:
                        logger.error(f"❌ Conversion failed: {result.stderr}")
                else:
                    results['conversion_script_exists'] = False
                    logger.error("❌ Conversion script not found")
            else:
                results['test_md_file_missing'] = False
                logger.error("❌ Test markdown file not found")

            return results

        except Exception as e:
            logger.error(f"❌ Document conversion test failed: {e}")
            return {'conversion_test_error': False}

    def test_google_drive_integration(self) -> Dict[str, bool]:
        """Test Google Drive integration with rclone."""
        logger.info("☁️ Testing Google Drive integration...")
        results = {}

        try:
            # Test 1: Check if rclone is installed
            try:
                result = subprocess.run(['rclone', 'version'], capture_output=True, text=True, timeout=10)
                results['rclone_installed'] = result.returncode == 0
                if result.returncode == 0:
                    logger.info("✅ rclone is installed")
                else:
                    logger.error("❌ rclone not installed")
            except FileNotFoundError:
                results['rclone_installed'] = False
                logger.error("❌ rclone not found in PATH")

            # Test 2: Check rclone configuration
            if results.get('rclone_installed', False):
                try:
                    result = subprocess.run(['rclone', 'config', 'show', 'googledrive'],
                                          capture_output=True, text=True, timeout=10)
                    results['rclone_configured'] = result.returncode == 0
                    if result.returncode == 0:
                        logger.info("✅ Google Drive remote configured")
                    else:
                        logger.warning("⚠️ Google Drive remote not configured")
                except Exception:
                    results['rclone_configured'] = False

            # Test 3: Test Google Drive script
            gdrive_script = self.project_root / 'scripts' / 'gdrive_upload.py'
            results['gdrive_script_exists'] = gdrive_script.exists()

            if gdrive_script.exists():
                logger.info("✅ Google Drive upload script found")

                # Test script execution (dry run)
                if self.temp_dir:
                    test_file = Path(self.temp_dir) / 'test_upload.txt'
                    with open(test_file, 'w') as f:
                        f.write("Test file for upload validation")

                    # Test with --help to ensure script runs
                    cmd = [sys.executable, str(gdrive_script), '--help']
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                    results['gdrive_script_executable'] = result.returncode == 0
            else:
                logger.error("❌ Google Drive upload script not found")

            return results

        except Exception as e:
            logger.error(f"❌ Google Drive integration test failed: {e}")
            return {'gdrive_test_error': False}

    def test_jina_mcp_integration(self) -> Dict[str, bool]:
        """Test Jina MCP server integration."""
        logger.info("🔍 Testing Jina MCP integration...")
        results = {}

        try:
            # Test 1: Check MCP configuration
            mcp_config_file = self.project_root / '.claude' / 'mcp_settings.json'
            results['mcp_config_exists'] = mcp_config_file.exists()

            if mcp_config_file.exists():
                with open(mcp_config_file, 'r') as f:
                    mcp_config = json.load(f)
                    results['jina_mcp_configured'] = 'jina-mcp-server' in mcp_config.get('mcpServers', {})
                    logger.info("✅ MCP configuration found")
            else:
                logger.error("❌ MCP configuration not found")

            # Test 2: Check for Jina API key
            jina_api_key = os.getenv('JINA_API_KEY')
            results['jina_api_key_set'] = bool(jina_api_key)

            if jina_api_key:
                logger.info("✅ Jina API key is set")
                # Test API key format (should start with 'jina_' typically)
                results['jina_api_key_valid_format'] = len(jina_api_key) > 10
            else:
                logger.error("❌ JINA_API_KEY environment variable not set")

            # Test 3: Test Jina API connectivity (if key available)
            if jina_api_key:
                try:
                    import requests
                    headers = {'Authorization': f'Bearer {jina_api_key}'}
                    response = requests.get('https://api.jina.ai/v1/health',
                                          headers=headers, timeout=10)
                    results['jina_api_accessible'] = response.status_code == 200

                    if response.status_code == 200:
                        logger.info("✅ Jina API is accessible")
                    else:
                        logger.warning(f"⚠️ Jina API returned status {response.status_code}")

                except ImportError:
                    logger.warning("⚠️ requests library not available for API test")
                    results['jina_api_accessible'] = None
                except Exception as e:
                    logger.warning(f"⚠️ Jina API test failed: {e}")
                    results['jina_api_accessible'] = False

            return results

        except Exception as e:
            logger.error(f"❌ Jina MCP integration test failed: {e}")
            return {'jina_test_error': False}

    def test_web_scraping(self) -> Dict[str, bool]:
        """Test web scraping functionality."""
        logger.info("🕷️ Testing web scraping...")
        results = {}

        try:
            # Test web scraper CLI existence
            scraper_script = self.project_root / 'scripts' / 'web_scraper_cli.py'
            results['scraper_script_exists'] = scraper_script.exists()

            if scraper_script.exists():
                logger.info("✅ Web scraper CLI found")

                # Test script execution
                cmd = [sys.executable, str(scraper_script), '--help']
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                results['scraper_script_executable'] = result.returncode == 0

                if result.returncode == 0:
                    logger.info("✅ Web scraper CLI is executable")
                else:
                    logger.error(f"❌ Web scraper CLI execution failed: {result.stderr}")
            else:
                logger.error("❌ Web scraper CLI not found")

            return results

        except Exception as e:
            logger.error(f"❌ Web scraping test failed: {e}")
            return {'scraping_test_error': False}

    def run_comprehensive_test(self, categories: List[str] = None) -> Dict[str, Dict[str, bool]]:
        """Run comprehensive system tests."""
        if categories is None:
            categories = ['hooks', 'conversion', 'gdrive', 'jina', 'scraping']

        logger.info("🚀 Starting comprehensive system tests...")

        # Setup test environment
        if not self.setup_test_environment():
            return {'setup_error': {'environment_setup': False}}

        all_results = {}

        try:
            if 'hooks' in categories:
                all_results['hooks'] = self.test_hook_system()

            if 'conversion' in categories:
                all_results['conversion'] = self.test_document_conversion()

            if 'gdrive' in categories:
                all_results['gdrive'] = self.test_google_drive_integration()

            if 'jina' in categories:
                all_results['jina'] = self.test_jina_mcp_integration()

            if 'scraping' in categories:
                all_results['scraping'] = self.test_web_scraping()

            return all_results

        finally:
            # Cleanup test environment
            if self.temp_dir and Path(self.temp_dir).exists():
                import shutil
                shutil.rmtree(self.temp_dir)
                logger.info(f"🧹 Cleaned up test environment: {self.temp_dir}")

    def generate_test_report(self, results: Dict[str, Dict[str, bool]]) -> str:
        """Generate comprehensive test report."""
        report_lines = [
            "# Bigger Boss Agent System - Test Report",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Test Results Summary",
            ""
        ]

        total_tests = 0
        passed_tests = 0

        for category, category_results in results.items():
            report_lines.append(f"### {category.title()} Tests")
            report_lines.append("")

            for test_name, result in category_results.items():
                total_tests += 1
                status = "✅ PASS" if result else "❌ FAIL"
                if result:
                    passed_tests += 1

                test_display_name = test_name.replace('_', ' ').title()
                report_lines.append(f"- **{test_display_name}**: {status}")

            report_lines.append("")

        # Overall summary
        pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        report_lines.insert(4, f"**Overall Pass Rate:** {passed_tests}/{total_tests} ({pass_rate:.1f}%)")
        report_lines.insert(5, "")

        # Recommendations
        report_lines.extend([
            "## Recommendations",
            "",
            "### Critical Issues (Must Fix Before Production)",
            ""
        ])

        critical_issues = []
        for category, category_results in results.items():
            for test_name, result in category_results.items():
                if not result and 'script_exists' in test_name:
                    critical_issues.append(f"- Missing required script: {test_name}")
                elif not result and 'config' in test_name:
                    critical_issues.append(f"- Configuration issue: {test_name}")

        if critical_issues:
            report_lines.extend(critical_issues)
        else:
            report_lines.append("✅ No critical issues detected")

        report_lines.extend([
            "",
            "### Warnings (Recommended Fixes)",
            ""
        ])

        warnings = []
        for category, category_results in results.items():
            for test_name, result in category_results.items():
                if not result and test_name not in [t.split(': ')[1] for t in critical_issues]:
                    warnings.append(f"- {test_name.replace('_', ' ').title()}")

        if warnings:
            report_lines.extend(warnings)
        else:
            report_lines.append("✅ No warnings")

        return '\n'.join(report_lines)


def main():
    """Main function for test execution."""
    parser = argparse.ArgumentParser(
        description='Bigger Boss Agent System - Comprehensive Testing Suite'
    )

    parser.add_argument(
        '--category',
        choices=['all', 'hooks', 'conversion', 'gdrive', 'jina', 'scraping'],
        default='all',
        help='Test category to run (default: all)'
    )

    parser.add_argument(
        '--output',
        help='Output file for test report (default: print to console)'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Determine test categories
    if args.category == 'all':
        categories = ['hooks', 'conversion', 'gdrive', 'jina', 'scraping']
    else:
        categories = [args.category]

    # Run tests
    tester = SystemTester()
    results = tester.run_comprehensive_test(categories)

    # Generate report
    report = tester.generate_test_report(results)

    # Output report
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"📄 Test report saved to: {args.output}")
    else:
        print(report)

    # Exit with appropriate code
    total_tests = sum(len(category_results) for category_results in results.values())
    passed_tests = sum(sum(1 for result in category_results.values() if result)
                      for category_results in results.values())

    if passed_tests == total_tests:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print(f"\n⚠️ {total_tests - passed_tests} test(s) failed")
        sys.exit(1)


if __name__ == "__main__":
    main()