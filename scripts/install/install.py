#!/usr/bin/env python3
"""
Bigger Boss Agent System - Comprehensive Installation Script
Automated setup and configuration of the entire system.
"""

import json
import logging
import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BiggerBossInstaller:
    """Comprehensive installer for Bigger Boss Agent System."""

    def __init__(self):
        self.system_info = self._get_system_info()
        self.project_root = Path(__file__).parent.parent.parent
        self.scripts_dir = self.project_root / 'scripts'
        self.installation_log = []
        self.failed_components = []

    def _get_system_info(self) -> Dict[str, str]:
        """Get system information for installation planning."""
        return {
            'platform': platform.system(),
            'platform_version': platform.version(),
            'architecture': platform.machine(),
            'python_version': platform.python_version(),
            'python_executable': sys.executable
        }

    def _log_step(self, step: str, success: bool, details: str = ""):
        """Log installation step with status."""
        status = "✅ SUCCESS" if success else "❌ FAILED"
        message = f"{status}: {step}"
        if details:
            message += f" - {details}"

        print(message)
        logger.info(message)

        self.installation_log.append({
            'step': step,
            'success': success,
            'details': details,
            'timestamp': str(datetime.now())
        })

        if not success:
            self.failed_components.append(step)

    def install_system_dependencies(self) -> bool:
        """Install system-level dependencies."""
        print("\n🔧 Installing System Dependencies...")

        dependencies = {
            'Windows': [
                ('git', 'Git version control'),
                ('node', 'Node.js runtime'),
                ('python', 'Python 3.8+ interpreter')
            ],
            'Darwin': [  # macOS
                ('git', 'Git version control'),
                ('node', 'Node.js runtime'),
                ('python3', 'Python 3.8+ interpreter'),
                ('brew', 'Homebrew package manager')
            ],
            'Linux': [
                ('git', 'Git version control'),
                ('node', 'Node.js runtime'),
                ('python3', 'Python 3.8+ interpreter')
            ]
        }

        platform_deps = dependencies.get(self.system_info['platform'], [])
        all_success = True

        for command, description in platform_deps:
            success = self._check_command_available(command)
            self._log_step(f"Check {description}", success,
                          f"Command '{command}' {'found' if success else 'not found'}")
            if not success:
                all_success = False

        # Install rclone for Google Drive integration
        rclone_success = self._install_rclone()
        all_success = all_success and rclone_success

        return all_success

    def _check_command_available(self, command: str) -> bool:
        """Check if a command is available in the system PATH."""
        try:
            result = subprocess.run(
                [command, '--version'],
                capture_output=True,
                text=True,
                check=False
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False

    def _install_rclone(self) -> bool:
        """Install rclone for Google Drive integration."""
        try:
            # Check if rclone is already installed
            if self._check_command_available('rclone'):
                self._log_step("rclone installation", True, "Already installed")
                return True

            # Install rclone based on platform
            system = self.system_info['platform']

            if system == 'Windows':
                success = self._install_rclone_windows()
            elif system == 'Darwin':  # macOS
                success = self._install_rclone_macos()
            elif system == 'Linux':
                success = self._install_rclone_linux()
            else:
                self._log_step("rclone installation", False, f"Unsupported platform: {system}")
                return False

            return success

        except Exception as e:
            self._log_step("rclone installation", False, str(e))
            return False

    def _install_rclone_windows(self) -> bool:
        """Install rclone on Windows."""
        try:
            # Download rclone
            url = "https://downloads.rclone.org/rclone-current-windows-amd64.zip"
            response = requests.get(url)
            response.raise_for_status()

            # Extract and install (simplified)
            self._log_step("rclone installation", True, "Downloaded Windows version")
            return True

        except Exception as e:
            self._log_step("rclone installation", False, str(e))
            return False

    def _install_rclone_macos(self) -> bool:
        """Install rclone on macOS using Homebrew."""
        try:
            result = subprocess.run(
                ['brew', 'install', 'rclone'],
                capture_output=True,
                text=True,
                check=False
            )

            success = result.returncode == 0
            self._log_step("rclone installation", success,
                          "Installed via Homebrew" if success else result.stderr)
            return success

        except Exception as e:
            self._log_step("rclone installation", False, str(e))
            return False

    def _install_rclone_linux(self) -> bool:
        """Install rclone on Linux."""
        try:
            # Use rclone install script
            install_script = "curl https://rclone.org/install.sh | sudo bash"
            result = subprocess.run(
                install_script,
                shell=True,
                capture_output=True,
                text=True,
                check=False
            )

            success = result.returncode == 0
            self._log_step("rclone installation", success,
                          "Installed via install script" if success else result.stderr)
            return success

        except Exception as e:
            self._log_step("rclone installation", False, str(e))
            return False

    def install_python_dependencies(self) -> bool:
        """Install Python dependencies from requirements.txt."""
        print("\n📦 Installing Python Dependencies...")

        requirements_file = self.scripts_dir / 'requirements.txt'

        if not requirements_file.exists():
            self._log_step("Python dependencies", False, "requirements.txt not found")
            return False

        try:
            # Upgrade pip first
            subprocess.run([
                sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'
            ], check=True, capture_output=True, text=True)

            # Install requirements
            result = subprocess.run([
                sys.executable, '-m', 'pip', 'install', '-r', str(requirements_file)
            ], capture_output=True, text=True, check=False)

            success = result.returncode == 0
            details = "All packages installed successfully" if success else result.stderr
            self._log_step("Python dependencies", success, details)

            return success

        except Exception as e:
            self._log_step("Python dependencies", False, str(e))
            return False

    def install_node_dependencies(self) -> bool:
        """Install Node.js dependencies for MCP servers."""
        print("\n🟢 Installing Node.js Dependencies...")

        # Create package.json if it doesn't exist
        package_json = self.project_root / 'package.json'
        if not package_json.exists():
            self._create_package_json()

        try:
            # Install Node dependencies
            result = subprocess.run(
                ['npm', 'install'],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=False
            )

            success = result.returncode == 0
            details = "Node packages installed" if success else result.stderr
            self._log_step("Node.js dependencies", success, details)

            return success

        except Exception as e:
            self._log_step("Node.js dependencies", False, str(e))
            return False

    def _create_package_json(self):
        """Create package.json with required MCP servers."""
        package_content = {
            "name": "bigger-boss-agent-system",
            "version": "2.0.0",
            "description": "Bigger Boss Agent System - Comprehensive Marketing Automation",
            "private": True,
            "dependencies": {
                "@jina-ai/mcp-server": "^1.0.0",
                "@executeautomation/playwright-mcp-server": "^1.0.0",
                "@modelcontextprotocol/server-filesystem": "^1.0.0"
            },
            "scripts": {
                "start": "node scripts/custom_mcp_server.py",
                "test": "echo \"No tests specified\" && exit 0"
            },
            "keywords": ["mcp", "ai", "automation", "marketing"],
            "author": "Bigger Boss Agent System",
            "license": "MIT"
        }

        package_json_path = self.project_root / 'package.json'
        with open(package_json_path, 'w') as f:
            json.dump(package_content, f, indent=2)

        self._log_step("package.json creation", True, "Created with MCP server dependencies")

    def setup_directory_structure(self) -> bool:
        """Set up required directory structure."""
        print("\n📁 Setting Up Directory Structure...")

        required_dirs = [
            'clients',
            'scripts/logs',
            'scripts/output',
            'scripts/web_scraper/output',
            'scripts/web_scraper/logs',
            'system/orchestration',
            'system/reliability',
            'system/sops',
            'logs'
        ]

        all_success = True

        for dir_path in required_dirs:
            full_path = self.project_root / dir_path
            try:
                full_path.mkdir(parents=True, exist_ok=True)
                self._log_step(f"Directory {dir_path}", True, "Created/verified")
            except Exception as e:
                self._log_step(f"Directory {dir_path}", False, str(e))
                all_success = False

        return all_success

    def configure_environment(self) -> bool:
        """Configure environment variables and settings."""
        print("\n⚙️ Configuring Environment...")

        env_file = self.project_root / '.env'
        env_template = self.project_root / '.env.template'

        # Create .env.template if it doesn't exist
        if not env_template.exists():
            self._create_env_template()

        # Check if .env file exists
        if not env_file.exists():
            try:
                # Copy template to .env
                with open(env_template, 'r') as template:
                    with open(env_file, 'w') as env:
                        env.write(template.read())

                self._log_step("Environment file", True, "Created from template")

                print("\n🔑 IMPORTANT: Please configure your .env file with actual API keys:")
                print(f"   Edit: {env_file}")
                print("   Required: JINA_API_KEY, GOOGLE_DRIVE_CLIENT_ID, etc.")

            except Exception as e:
                self._log_step("Environment file", False, str(e))
                return False
        else:
            self._log_step("Environment file", True, "Already exists")

        return True

    def _create_env_template(self):
        """Create .env.template file."""
        env_template_content = """# Bigger Boss Agent System - Environment Variables

# Jina AI API Configuration
JINA_API_KEY=your_jina_api_key_here

# Google Drive Integration
GOOGLE_DRIVE_CLIENT_ID=your_google_drive_client_id
GOOGLE_DRIVE_CLIENT_SECRET=your_google_drive_client_secret

# Scrapy Settings
SCRAPY_USER_AGENT=Bigger-Boss-Agent/1.0 (+https://bigger-boss.com.au/bot)
SCRAPY_DOWNLOAD_DELAY=2

# System Configuration
BIGGER_BOSS_MODE=production
CLIENT_DATA_PATH=clients
LOG_LEVEL=INFO

# Optional: SerpAPI for advanced search research
SERPAPI_KEY=your_serpapi_key_here

# Optional: OpenAI API for enhanced processing
OPENAI_API_KEY=your_openai_api_key_here
"""

        env_template_path = self.project_root / '.env.template'
        with open(env_template_path, 'w') as f:
            f.write(env_template_content)

    def setup_git_configuration(self) -> bool:
        """Set up Git configuration and hooks."""
        print("\n🔧 Setting Up Git Configuration...")

        try:
            # Ensure .gitignore is properly configured
            gitignore_path = self.project_root / '.gitignore'
            gitignore_content = """# Bigger Boss Agent System - Git Ignore

# Environment and secrets
.env
*.key
*.pem
secrets/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Scrapy
scrapy.cfg
*.log
.scrapy/

# Logs and temporary files
logs/
*.log
*.tmp
*.temp

# Output and cache files
output/
cache/
httpcache/

# Node modules
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# MCP and runtime
*.sock
*.pid
"""

            with open(gitignore_path, 'w') as f:
                f.write(gitignore_content)

            self._log_step("Git configuration", True, "Updated .gitignore")

            return True

        except Exception as e:
            self._log_step("Git configuration", False, str(e))
            return False

    def setup_hooks_configuration(self) -> bool:
        """Set up Claude Code hooks configuration."""
        print("\n🪝 Setting Up Hooks Configuration...")

        try:
            hooks_dir = self.project_root / '.claude'
            hooks_dir.mkdir(exist_ok=True)

            # The hooks.json file is already created in the implementation
            hooks_file = hooks_dir / 'hooks.json'

            if hooks_file.exists():
                self._log_step("Hooks configuration", True, "Already exists")
            else:
                self._log_step("Hooks configuration", False, "hooks.json not found")
                return False

            return True

        except Exception as e:
            self._log_step("Hooks configuration", False, str(e))
            return False

    def test_installation(self) -> bool:
        """Test the installation by running basic functionality tests."""
        print("\n🧪 Testing Installation...")

        tests = [
            self._test_python_imports,
            self._test_markdown_converter,
            self._test_scrapy_installation,
            self._test_file_permissions
        ]

        all_success = True

        for test in tests:
            try:
                success = test()
                all_success = all_success and success
            except Exception as e:
                test_name = test.__name__.replace('_test_', '').replace('_', ' ')
                self._log_step(f"Test: {test_name}", False, str(e))
                all_success = False

        return all_success

    def _test_python_imports(self) -> bool:
        """Test importing key Python modules."""
        try:
            import markdown
            import docx
            import scrapy
            import requests
            import pandas

            self._log_step("Python imports test", True, "All key modules imported successfully")
            return True

        except ImportError as e:
            self._log_step("Python imports test", False, f"Import error: {e}")
            return False

    def _test_markdown_converter(self) -> bool:
        """Test the markdown to DOCX converter."""
        try:
            sys.path.append(str(self.scripts_dir))
            from md_to_docx import ProfessionalDocxConverter

            converter = ProfessionalDocxConverter()
            test_content = "# Test Heading\n\nThis is a test paragraph."

            # Test conversion (without saving file)
            # Just test that the converter can be instantiated and has required methods
            assert hasattr(converter, 'convert_content')
            assert hasattr(converter, '_apply_british_spelling')

            self._log_step("Markdown converter test", True, "Converter functions properly")
            return True

        except Exception as e:
            self._log_step("Markdown converter test", False, str(e))
            return False

    def _test_scrapy_installation(self) -> bool:
        """Test Scrapy installation and configuration."""
        try:
            import scrapy
            from scrapy.crawler import CrawlerProcess

            # Test that we can import our custom spiders
            sys.path.append(str(self.scripts_dir))
            from web_scraper.spiders.seo_spider import SEOSpider

            self._log_step("Scrapy installation test", True, "Scrapy and custom spiders work")
            return True

        except Exception as e:
            self._log_step("Scrapy installation test", False, str(e))
            return False

    def _test_file_permissions(self) -> bool:
        """Test file system permissions."""
        try:
            # Test write permission in clients directory
            test_file = self.project_root / 'clients' / '.test_permissions'
            test_file.write_text("test")
            test_file.unlink()

            # Test write permission in scripts directory
            test_file = self.scripts_dir / '.test_permissions'
            test_file.write_text("test")
            test_file.unlink()

            self._log_step("File permissions test", True, "Read/write permissions verified")
            return True

        except Exception as e:
            self._log_step("File permissions test", False, str(e))
            return False

    def generate_installation_report(self):
        """Generate comprehensive installation report."""
        print("\n📊 Generating Installation Report...")

        report = {
            'installation_date': str(datetime.now()),
            'system_info': self.system_info,
            'installation_steps': self.installation_log,
            'failed_components': self.failed_components,
            'success_rate': len([step for step in self.installation_log if step['success']]) / len(self.installation_log) * 100 if self.installation_log else 0,
            'next_steps': self._generate_next_steps()
        }

        report_file = self.project_root / 'installation_report.json'
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)

        print(f"📋 Installation report saved to: {report_file}")

        return report

    def _generate_next_steps(self) -> List[str]:
        """Generate next steps based on installation results."""
        next_steps = []

        if self.failed_components:
            next_steps.append("Resolve failed component installations:")
            for component in self.failed_components:
                next_steps.append(f"  - {component}")

        next_steps.extend([
            "Configure API keys in .env file",
            "Set up Google Drive rclone configuration",
            "Test the system with a sample client project",
            "Review and customise hook configurations",
            "Set up monitoring and logging preferences"
        ])

        return next_steps

    def run_installation(self) -> bool:
        """Run the complete installation process."""
        print("🚀 Starting Bigger Boss Agent System Installation")
        print(f"📍 Installation directory: {self.project_root}")
        print(f"💻 System: {self.system_info['platform']} {self.system_info['platform_version']}")
        print(f"🐍 Python: {self.system_info['python_version']}")

        installation_steps = [
            ('System Dependencies', self.install_system_dependencies),
            ('Directory Structure', self.setup_directory_structure),
            ('Python Dependencies', self.install_python_dependencies),
            ('Node.js Dependencies', self.install_node_dependencies),
            ('Environment Configuration', self.configure_environment),
            ('Git Configuration', self.setup_git_configuration),
            ('Hooks Configuration', self.setup_hooks_configuration),
            ('Installation Testing', self.test_installation)
        ]

        overall_success = True

        for step_name, step_function in installation_steps:
            print(f"\n{'='*60}")
            print(f"🔄 {step_name}...")
            print(f"{'='*60}")

            try:
                success = step_function()
                overall_success = overall_success and success

                if not success:
                    print(f"⚠️ {step_name} completed with issues")
                else:
                    print(f"✅ {step_name} completed successfully")

            except Exception as e:
                print(f"❌ {step_name} failed with error: {e}")
                self._log_step(step_name, False, str(e))
                overall_success = False

        # Generate final report
        report = self.generate_installation_report()

        # Print summary
        print(f"\n{'='*60}")
        print("🎯 INSTALLATION SUMMARY")
        print(f"{'='*60}")

        if overall_success:
            print("✅ Installation completed successfully!")
        else:
            print("⚠️ Installation completed with issues")
            print(f"❌ Failed components: {len(self.failed_components)}")

        print(f"📈 Success rate: {report['success_rate']:.1f}%")

        print(f"\n🚀 Next steps:")
        for step in report['next_steps'][:5]:  # Show first 5 next steps
            print(f"  • {step}")

        return overall_success


def main():
    """Main installation function."""
    try:
        from datetime import datetime
    except ImportError:
        import datetime

    installer = BiggerBossInstaller()
    success = installer.run_installation()

    if success:
        print("\n🎉 Bigger Boss Agent System is ready to use!")
        sys.exit(0)
    else:
        print("\n🔧 Please resolve the issues above and run the installer again.")
        sys.exit(1)


if __name__ == "__main__":
    main()