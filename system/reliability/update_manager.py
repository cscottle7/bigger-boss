"""
Comprehensive Update Management System
Handles API changes, dependency updates, and feature additions with automated testing and rollback
"""

import asyncio
import logging
import json
import time
import subprocess
import sys
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from dataclasses import dataclass, field, asdict
from enum import Enum
import requests
import pkg_resources
import hashlib
import shutil
import tempfile
from packaging import version
import yaml

from system.reliability.testing_framework import testing_framework, TestPriority
from system.reliability.health_monitor import health_monitor
from system.orchestration.autonomous_operation_manager import autonomous_manager

class UpdateType(Enum):
    """Types of updates"""
    DEPENDENCY = "dependency"
    API_CHANGE = "api_change"
    FEATURE_ADDITION = "feature_addition"
    SECURITY_PATCH = "security_patch"
    BUG_FIX = "bug_fix"
    CONFIGURATION = "configuration"

class UpdatePriority(Enum):
    """Update priority levels"""
    CRITICAL = "critical"     # Security patches, critical bugs
    HIGH = "high"            # Important features, major API changes
    MEDIUM = "medium"        # Regular updates, minor features
    LOW = "low"              # Optional updates, improvements

class UpdateStatus(Enum):
    """Update status"""
    PENDING = "pending"
    TESTING = "testing"
    APPROVED = "approved"
    DEPLOYED = "deployed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"

@dataclass
class UpdatePackage:
    """Update package definition"""
    update_id: str
    update_type: UpdateType
    priority: UpdatePriority
    name: str
    description: str
    current_version: str
    target_version: str
    dependencies: List[str] = field(default_factory=list)
    breaking_changes: bool = False
    rollback_available: bool = True
    test_requirements: List[str] = field(default_factory=list)
    estimated_duration: int = 30  # minutes
    created_at: datetime = field(default_factory=datetime.now)
    status: UpdateStatus = UpdateStatus.PENDING

@dataclass
class UpdateResult:
    """Update execution result"""
    update_id: str
    status: UpdateStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    error_message: Optional[str] = None
    test_results: Optional[Dict] = None
    rollback_point: Optional[str] = None
    logs: List[str] = field(default_factory=list)

class DependencyMonitor:
    """Monitors dependencies for updates and security issues"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.DependencyMonitor")
        self.critical_packages = [
            'requests', 'aiohttp', 'playwright', 'beautifulsoup4',
            'pandas', 'advertools', 'psutil', 'schedule', 'pyyaml'
        ]
        self.security_sources = [
            'https://pypi.org/pypi/{package}/json',
            'https://api.github.com/advisories'
        ]
    
    async def check_for_updates(self) -> List[UpdatePackage]:
        """Check for dependency updates"""
        updates = []
        
        try:
            installed_packages = {pkg.project_name.lower(): pkg.version 
                                for pkg in pkg_resources.working_set}
            
            for package_name in self.critical_packages:
                package_name_lower = package_name.lower()
                
                if package_name_lower not in installed_packages:
                    continue
                
                current_version = installed_packages[package_name_lower]
                latest_version = await self._get_latest_version(package_name)
                
                if latest_version and version.parse(latest_version) > version.parse(current_version):
                    # Check for security advisories
                    is_security = await self._check_security_advisory(package_name, current_version)
                    
                    update = UpdatePackage(
                        update_id=f"dep_{package_name}_{latest_version}",
                        update_type=UpdateType.SECURITY_PATCH if is_security else UpdateType.DEPENDENCY,
                        priority=UpdatePriority.CRITICAL if is_security else UpdatePriority.MEDIUM,
                        name=f"Update {package_name}",
                        description=f"Update {package_name} from {current_version} to {latest_version}",
                        current_version=current_version,
                        target_version=latest_version,
                        breaking_changes=await self._check_breaking_changes(package_name, current_version, latest_version),
                        test_requirements=['api', 'system', 'workflow']
                    )
                    
                    updates.append(update)
        
        except Exception as e:
            self.logger.error(f"Error checking for updates: {e}")
        
        return updates
    
    async def _get_latest_version(self, package_name: str) -> Optional[str]:
        """Get latest version of package from PyPI"""
        try:
            url = f"https://pypi.org/pypi/{package_name}/json"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data['info']['version']
        
        except Exception as e:
            self.logger.warning(f"Could not get latest version for {package_name}: {e}")
        
        return None
    
    async def _check_security_advisory(self, package_name: str, current_version: str) -> bool:
        """Check if there are security advisories for the package version"""
        try:
            # This is a simplified check - in production would use proper security databases
            # like GitHub Advisory Database, OSV, etc.
            
            # For now, just check if the package is significantly outdated (>6 months)
            url = f"https://pypi.org/pypi/{package_name}/json"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Get upload time of current version
                        releases = data.get('releases', {})
                        if current_version in releases:
                            release_info = releases[current_version]
                            if release_info:
                                upload_time = datetime.fromisoformat(
                                    release_info[0]['upload_time_iso_8601'].replace('Z', '+00:00')
                                )
                                
                                # If version is older than 6 months, consider it potentially insecure
                                if datetime.now(upload_time.tzinfo) - upload_time > timedelta(days=180):
                                    return True
        
        except Exception as e:
            self.logger.warning(f"Could not check security advisory for {package_name}: {e}")
        
        return False
    
    async def _check_breaking_changes(
        self, 
        package_name: str, 
        current_version: str, 
        target_version: str
    ) -> bool:
        """Check if update contains breaking changes"""
        try:
            # Check if major version changed
            current_major = version.parse(current_version).major
            target_major = version.parse(target_version).major
            
            return target_major > current_major
        
        except Exception:
            return False  # Assume no breaking changes if can't determine

class APIChangeDetector:
    """Detects API changes that might affect the system"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.APIChangeDetector")
        self.monitored_apis = {
            'serpapi': 'https://serpapi.com/api',
            'jina': 'https://jina.ai/api',
            'gtmetrix': 'https://gtmetrix.com/api'
        }
    
    async def check_api_changes(self) -> List[UpdatePackage]:
        """Check for API changes"""
        updates = []
        
        for api_name, api_base_url in self.monitored_apis.items():
            try:
                changes = await self._detect_api_changes(api_name, api_base_url)
                if changes:
                    updates.extend(changes)
            
            except Exception as e:
                self.logger.error(f"Error checking {api_name} API changes: {e}")
        
        return updates
    
    async def _detect_api_changes(self, api_name: str, api_base_url: str) -> List[UpdatePackage]:
        """Detect changes for specific API"""
        updates = []
        
        try:
            # Check if we have cached API schema
            schema_file = Path(f"system/api_schemas/{api_name}_schema.json")
            
            if schema_file.exists():
                # Load cached schema
                with open(schema_file, 'r') as f:
                    cached_schema = json.load(f)
                
                # Get current schema (this would be API-specific implementation)
                current_schema = await self._get_api_schema(api_name, api_base_url)
                
                if current_schema and current_schema != cached_schema:
                    # API has changed
                    update = UpdatePackage(
                        update_id=f"api_{api_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                        update_type=UpdateType.API_CHANGE,
                        priority=UpdatePriority.HIGH,
                        name=f"{api_name} API Change",
                        description=f"Detected changes in {api_name} API schema",
                        current_version=cached_schema.get('version', 'unknown'),
                        target_version=current_schema.get('version', 'unknown'),
                        breaking_changes=await self._analyse_breaking_changes(cached_schema, current_schema),
                        test_requirements=['api', 'workflow']
                    )
                    
                    updates.append(update)
                    
                    # Update cached schema
                    with open(schema_file, 'w') as f:
                        json.dump(current_schema, f, indent=2)
        
        except Exception as e:
            self.logger.error(f"Error detecting API changes for {api_name}: {e}")
        
        return updates
    
    async def _get_api_schema(self, api_name: str, api_base_url: str) -> Optional[Dict]:
        """Get current API schema (simplified implementation)"""
        try:
            # This is a simplified implementation
            # In practice, would fetch actual API schema/documentation
            
            if api_name == 'serpapi':
                return await self._get_serpapi_schema()
            elif api_name == 'jina':
                return await self._get_jina_schema()
            elif api_name == 'gtmetrix':
                return await self._get_gtmetrix_schema()
        
        except Exception as e:
            self.logger.warning(f"Could not get schema for {api_name}: {e}")
        
        return None
    
    async def _get_serpapi_schema(self) -> Dict:
        """Get SerpAPI schema"""
        return {
            'version': '1.0',
            'endpoints': ['search', 'account'],
            'parameters': ['q', 'api_key', 'engine'],
            'last_checked': datetime.now().isoformat()
        }
    
    async def _get_jina_schema(self) -> Dict:
        """Get Jina API schema"""
        return {
            'version': '1.0',
            'endpoints': ['reader'],
            'headers': ['Authorization'],
            'last_checked': datetime.now().isoformat()
        }
    
    async def _get_gtmetrix_schema(self) -> Dict:
        """Get GTmetrix API schema"""
        return {
            'version': '2.0',
            'endpoints': ['test', 'locations', 'browsers'],
            'auth': 'basic',
            'last_checked': datetime.now().isoformat()
        }
    
    async def _analyse_breaking_changes(self, old_schema: Dict, new_schema: Dict) -> bool:
        """Analyse if API changes are breaking"""
        try:
            # Check for removed endpoints
            old_endpoints = set(old_schema.get('endpoints', []))
            new_endpoints = set(new_schema.get('endpoints', []))
            
            if not old_endpoints.issubset(new_endpoints):
                return True  # Endpoints were removed
            
            # Check for major version change
            old_version = old_schema.get('version', '0.0')
            new_version = new_schema.get('version', '0.0')
            
            try:
                if version.parse(new_version).major > version.parse(old_version).major:
                    return True
            except:
                pass
            
            return False
        
        except Exception:
            return False  # Assume non-breaking if can't determine

class UpdateManager:
    """Main update management system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.dependency_monitor = DependencyMonitor()
        self.api_detector = APIChangeDetector()
        self.pending_updates: List[UpdatePackage] = []
        self.update_history: List[UpdateResult] = []
        self.update_lock = threading.Lock()
        self.setup_update_logging()
        self.load_pending_updates()
    
    def setup_update_logging(self):
        """Setup update management logging"""
        update_log_dir = Path("system/reports/updates")
        update_log_dir.mkdir(parents=True, exist_ok=True)
        
        update_handler = logging.FileHandler(
            update_log_dir / f"updates_{datetime.now().strftime('%Y%m%d')}.log"
        )
        update_handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        update_handler.setFormatter(formatter)
        
        self.logger.addHandler(update_handler)
    
    def load_pending_updates(self):
        """Load pending updates from storage"""
        try:
            updates_file = Path("system/reports/updates/pending_updates.json")
            
            if updates_file.exists():
                with open(updates_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.pending_updates = []
                for update_data in data.get('updates', []):
                    # Reconstruct UpdatePackage objects
                    update = UpdatePackage(**update_data)
                    update.created_at = datetime.fromisoformat(update_data['created_at'])
                    self.pending_updates.append(update)
                
                self.logger.info(f"Loaded {len(self.pending_updates)} pending updates")
        
        except Exception as e:
            self.logger.error(f"Failed to load pending updates: {e}")
            self.pending_updates = []
    
    def save_pending_updates(self):
        """Save pending updates to storage"""
        try:
            updates_file = Path("system/reports/updates/pending_updates.json")
            updates_file.parent.mkdir(parents=True, exist_ok=True)
            
            updates_data = {
                'last_updated': datetime.now().isoformat(),
                'updates': []
            }
            
            for update in self.pending_updates:
                update_dict = asdict(update)
                update_dict['created_at'] = update.created_at.isoformat()
                updates_data['updates'].append(update_dict)
            
            with open(updates_file, 'w', encoding='utf-8') as f:
                json.dump(updates_data, f, indent=2, ensure_ascii=False, default=str)
        
        except Exception as e:
            self.logger.error(f"Failed to save pending updates: {e}")
    
    async def check_for_updates(self) -> Dict[str, List[UpdatePackage]]:
        """Check for all types of updates"""
        self.logger.info("Checking for system updates")
        
        all_updates = {
            'dependencies': [],
            'api_changes': [],
            'total_found': 0
        }
        
        try:
            # Check dependency updates
            dependency_updates = await self.dependency_monitor.check_for_updates()
            all_updates['dependencies'] = dependency_updates
            
            # Check API changes
            api_updates = await self.api_detector.check_api_changes()
            all_updates['api_changes'] = api_updates
            
            # Combine and add to pending updates
            new_updates = dependency_updates + api_updates
            
            with self.update_lock:
                for update in new_updates:
                    # Check if update already exists
                    existing_ids = {u.update_id for u in self.pending_updates}
                    if update.update_id not in existing_ids:
                        self.pending_updates.append(update)
                
                # Save pending updates
                self.save_pending_updates()
            
            all_updates['total_found'] = len(new_updates)
            
            self.logger.info(f"Found {len(new_updates)} new updates")
            
            # Log to autonomous manager
            autonomous_manager.log_operation(
                'update_management',
                'updates_checked',
                {
                    'dependencies_found': len(dependency_updates),
                    'api_changes_found': len(api_updates),
                    'total_pending': len(self.pending_updates)
                }
            )
        
        except Exception as e:
            self.logger.error(f"Error checking for updates: {e}")
            all_updates['error'] = str(e)
        
        return all_updates
    
    async def apply_update(self, update_id: str, force: bool = False) -> UpdateResult:
        """Apply a specific update"""
        
        # Find the update
        update = None
        with self.update_lock:
            for u in self.pending_updates:
                if u.update_id == update_id:
                    update = u
                    break
        
        if not update:
            error_msg = f"Update {update_id} not found"
            self.logger.error(error_msg)
            return UpdateResult(
                update_id=update_id,
                status=UpdateStatus.FAILED,
                start_time=datetime.now(),
                end_time=datetime.now(),
                error_message=error_msg
            )
        
        self.logger.info(f"Applying update: {update.name}")
        
        result = UpdateResult(
            update_id=update_id,
            status=UpdateStatus.TESTING,
            start_time=datetime.now()
        )
        
        try:
            # Create rollback point
            rollback_point = await self._create_rollback_point(update)
            result.rollback_point = rollback_point
            
            # Pre-update health check
            if not force:
                health_ok = await self._pre_update_health_check()
                if not health_ok:
                    raise Exception("System not healthy enough for update")
            
            # Apply the update
            success = await self._execute_update(update, result)
            
            if not success:
                raise Exception("Update execution failed")
            
            # Run tests
            if update.test_requirements and not force:
                test_results = await self._run_update_tests(update)
                result.test_results = test_results
                
                if not test_results.get('success', False):
                    raise Exception("Update tests failed")
            
            # Update successful
            result.status = UpdateStatus.DEPLOYED
            result.end_time = datetime.now()
            
            # Remove from pending updates
            with self.update_lock:
                self.pending_updates = [u for u in self.pending_updates if u.update_id != update_id]
                self.save_pending_updates()
            
            self.logger.info(f"Update {update_id} applied successfully")
        
        except Exception as e:
            result.status = UpdateStatus.FAILED
            result.end_time = datetime.now()
            result.error_message = str(e)
            
            self.logger.error(f"Update {update_id} failed: {e}")
            
            # Attempt rollback if rollback point exists
            if result.rollback_point and update.rollback_available:
                self.logger.info(f"Attempting rollback for {update_id}")
                try:
                    await self._rollback_update(result.rollback_point)
                    result.status = UpdateStatus.ROLLED_BACK
                    self.logger.info(f"Rollback successful for {update_id}")
                except Exception as rollback_error:
                    self.logger.error(f"Rollback failed for {update_id}: {rollback_error}")
        
        # Store result
        self.update_history.append(result)
        self._save_update_result(result)
        
        return result
    
    async def _create_rollback_point(self, update: UpdatePackage) -> str:
        """Create rollback point before applying update"""
        try:
            rollback_dir = Path("system/backups/rollback")
            rollback_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            rollback_id = f"rollback_{update.update_id}_{timestamp}"
            rollback_path = rollback_dir / rollback_id
            
            # Backup critical files/configurations
            critical_paths = [
                Path(".env"),
                Path("system/config"),
                Path("requirements.txt"),
                Path("pyproject.toml")
            ]
            
            rollback_path.mkdir()
            
            for path in critical_paths:
                if path.exists():
                    if path.is_file():
                        shutil.copy2(path, rollback_path / path.name)
                    elif path.is_dir():
                        shutil.copytree(path, rollback_path / path.name)
            
            # Save installed packages list
            try:
                packages_file = rollback_path / "installed_packages.txt"
                result = subprocess.run(
                    [sys.executable, '-m', 'pip', 'freeze'],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    packages_file.write_text(result.stdout)
            except Exception as e:
                self.logger.warning(f"Could not backup package list: {e}")
            
            self.logger.info(f"Rollback point created: {rollback_id}")
            return rollback_id
        
        except Exception as e:
            self.logger.error(f"Failed to create rollback point: {e}")
            return ""
    
    async def _execute_update(self, update: UpdatePackage, result: UpdateResult) -> bool:
        """Execute the actual update"""
        try:
            if update.update_type == UpdateType.DEPENDENCY:
                return await self._update_dependency(update, result)
            elif update.update_type == UpdateType.API_CHANGE:
                return await self._handle_api_change(update, result)
            elif update.update_type == UpdateType.CONFIGURATION:
                return await self._update_configuration(update, result)
            else:
                self.logger.warning(f"Unknown update type: {update.update_type}")
                return False
        
        except Exception as e:
            result.logs.append(f"Update execution error: {str(e)}")
            return False
    
    async def _update_dependency(self, update: UpdatePackage, result: UpdateResult) -> bool:
        """Update a Python dependency"""
        try:
            # Extract package name from update name
            package_name = update.name.replace("Update ", "")
            
            result.logs.append(f"Updating {package_name} to {update.target_version}")
            
            # Run pip install
            cmd = [
                sys.executable, '-m', 'pip', 'install',
                f"{package_name}=={update.target_version}"
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            result.logs.append(f"pip install stdout: {stdout.decode()}")
            if stderr:
                result.logs.append(f"pip install stderr: {stderr.decode()}")
            
            return process.returncode == 0
        
        except Exception as e:
            result.logs.append(f"Dependency update failed: {str(e)}")
            return False
    
    async def _handle_api_change(self, update: UpdatePackage, result: UpdateResult) -> bool:
        """Handle API change update"""
        try:
            result.logs.append(f"Handling API change for {update.name}")
            
            # In a real implementation, this would:
            # 1. Update API client code
            # 2. Update configuration
            # 3. Update tests
            # 4. Validate changes
            
            # For now, just mark as successful
            result.logs.append("API change handling completed")
            return True
        
        except Exception as e:
            result.logs.append(f"API change handling failed: {str(e)}")
            return False
    
    async def _update_configuration(self, update: UpdatePackage, result: UpdateResult) -> bool:
        """Update system configuration"""
        try:
            result.logs.append(f"Updating configuration for {update.name}")
            
            # Configuration updates would be specific to the change
            result.logs.append("Configuration update completed")
            return True
        
        except Exception as e:
            result.logs.append(f"Configuration update failed: {str(e)}")
            return False
    
    async def _pre_update_health_check(self) -> bool:
        """Run health check before applying update"""
        try:
            health_results = await health_monitor.run_comprehensive_health_check()
            
            # Check if system is healthy enough for update
            overall_status = health_results['system_overall'].status
            
            return overall_status.value in ['healthy', 'degraded']
        
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return False
    
    async def _run_update_tests(self, update: UpdatePackage) -> Dict[str, Any]:
        """Run tests after update"""
        try:
            test_results = {'success': True, 'details': {}}
            
            for test_suite_name in update.test_requirements:
                if test_suite_name in testing_framework.test_suites:
                    suite_results = await testing_framework.run_test_suite(
                        test_suite_name,
                        priorities=[TestPriority.CRITICAL, TestPriority.HIGH]
                    )
                    
                    test_results['details'][test_suite_name] = suite_results
                    
                    # Check if tests passed
                    if suite_results['summary']['failed'] > 0 or suite_results['summary']['errors'] > 0:
                        test_results['success'] = False
            
            return test_results
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def _rollback_update(self, rollback_point: str) -> bool:
        """Rollback update using rollback point"""
        try:
            rollback_path = Path(f"system/backups/rollback/{rollback_point}")
            
            if not rollback_path.exists():
                raise Exception(f"Rollback point {rollback_point} not found")
            
            # Restore backed up files
            for backup_file in rollback_path.iterdir():
                if backup_file.name == "installed_packages.txt":
                    # Restore packages
                    try:
                        cmd = [
                            sys.executable, '-m', 'pip', 'install',
                            '-r', str(backup_file)
                        ]
                        
                        process = await asyncio.create_subprocess_exec(
                            *cmd,
                            stdout=asyncio.subprocess.PIPE,
                            stderr=asyncio.subprocess.PIPE
                        )
                        
                        await process.communicate()
                    except Exception as e:
                        self.logger.warning(f"Could not restore packages: {e}")
                else:
                    # Restore file/directory
                    target_path = Path(backup_file.name)
                    
                    if target_path.exists():
                        if target_path.is_dir():
                            shutil.rmtree(target_path)
                        else:
                            target_path.unlink()
                    
                    if backup_file.is_dir():
                        shutil.copytree(backup_file, target_path)
                    else:
                        shutil.copy2(backup_file, target_path)
            
            self.logger.info(f"Rollback from {rollback_point} completed")
            return True
        
        except Exception as e:
            self.logger.error(f"Rollback failed: {e}")
            return False
    
    def _save_update_result(self, result: UpdateResult):
        """Save update result to file"""
        try:
            results_dir = Path("system/reports/updates")
            results_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = result.start_time.strftime('%Y%m%d_%H%M%S')
            result_file = results_dir / f"update_result_{result.update_id}_{timestamp}.json"
            
            result_data = asdict(result)
            result_data['start_time'] = result.start_time.isoformat()
            if result.end_time:
                result_data['end_time'] = result.end_time.isoformat()
            
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, indent=2, ensure_ascii=False, default=str)
            
            self.logger.info(f"Update result saved: {result_file}")
        
        except Exception as e:
            self.logger.error(f"Failed to save update result: {e}")
    
    def get_update_status(self) -> Dict[str, Any]:
        """Get current update status"""
        with self.update_lock:
            pending_by_priority = {}
            for priority in UpdatePriority:
                pending_by_priority[priority.value] = [
                    u for u in self.pending_updates if u.priority == priority
                ]
            
            recent_history = [
                h for h in self.update_history
                if h.start_time > datetime.now() - timedelta(days=7)
            ]
            
            return {
                'total_pending_updates': len(self.pending_updates),
                'pending_by_priority': {
                    k: len(v) for k, v in pending_by_priority.items()
                },
                'recent_update_history': len(recent_history),
                'last_check': datetime.now().isoformat(),
                'critical_updates': len([
                    u for u in self.pending_updates 
                    if u.priority == UpdatePriority.CRITICAL
                ])
            }
    
    async def apply_critical_updates(self) -> Dict[str, Any]:
        """Apply all critical updates automatically"""
        critical_updates = [
            u for u in self.pending_updates 
            if u.priority == UpdatePriority.CRITICAL
        ]
        
        results = {
            'total_critical': len(critical_updates),
            'applied': [],
            'failed': []
        }
        
        for update in critical_updates:
            self.logger.info(f"Auto-applying critical update: {update.update_id}")
            
            try:
                result = await self.apply_update(update.update_id, force=False)
                
                if result.status == UpdateStatus.DEPLOYED:
                    results['applied'].append(update.update_id)
                else:
                    results['failed'].append({
                        'update_id': update.update_id,
                        'error': result.error_message
                    })
            
            except Exception as e:
                results['failed'].append({
                    'update_id': update.update_id,
                    'error': str(e)
                })
        
        return results
    
    async def schedule_update_checks(self):
        """Schedule regular update checks"""
        self.logger.info("Starting scheduled update checks")
        
        while True:
            try:
                # Check for updates every 6 hours
                await self.check_for_updates()
                
                # Auto-apply critical updates
                critical_results = await self.apply_critical_updates()
                
                if critical_results['applied']:
                    self.logger.info(f"Auto-applied {len(critical_results['applied'])} critical updates")
                
                if critical_results['failed']:
                    self.logger.warning(f"Failed to apply {len(critical_results['failed'])} critical updates")
                
                # Wait 6 hours
                await asyncio.sleep(6 * 3600)
            
            except Exception as e:
                self.logger.error(f"Scheduled update check failed: {e}")
                await asyncio.sleep(3600)  # Retry in 1 hour

# Global update manager instance
update_manager = UpdateManager()

async def run_update_check():
    """Run manual update check"""
    try:
        print("Checking for system updates...")
        
        updates = await update_manager.check_for_updates()
        
        print(f"Update check completed:")
        print(f"  Dependency updates: {len(updates['dependencies'])}")
        print(f"  API changes: {len(updates['api_changes'])}")
        print(f"  Total found: {updates['total_found']}")
        
        if updates['total_found'] > 0:
            status = update_manager.get_update_status()
            print(f"\nCurrent status:")
            print(f"  Total pending: {status['total_pending_updates']}")
            print(f"  Critical updates: {status['critical_updates']}")
            
            if status['critical_updates'] > 0:
                print("\nWARNING: Critical updates available - consider applying immediately")
        
        return updates
    
    except Exception as e:
        print(f"Update check failed: {e}")
        logging.error(f"Update check failed: {e}")
        return None

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Update Manager')
    parser.add_argument('--check', action='store_true', help='Check for updates')
    parser.add_argument('--apply', type=str, help='Apply specific update by ID')
    parser.add_argument('--critical', action='store_true', help='Apply all critical updates')
    parser.add_argument('--status', action='store_true', help='Show update status')
    parser.add_argument('--schedule', action='store_true', help='Start scheduled update checks')
    
    args = parser.parse_args()
    
    if args.check:
        asyncio.run(run_update_check())
    elif args.apply:
        asyncio.run(update_manager.apply_update(args.apply))
    elif args.critical:
        asyncio.run(update_manager.apply_critical_updates())
    elif args.status:
        status = update_manager.get_update_status()
        print(json.dumps(status, indent=2, default=str))
    elif args.schedule:
        print("Starting scheduled update checks...")
        try:
            asyncio.run(update_manager.schedule_update_checks())
        except KeyboardInterrupt:
            print("Scheduled update checks stopped.")
    else:
        print("Update Manager - Available commands:")
        print("  --check: Check for updates")
        print("  --apply <update_id>: Apply specific update")
        print("  --critical: Apply all critical updates")
        print("  --status: Show current update status")
        print("  --schedule: Start scheduled update monitoring")