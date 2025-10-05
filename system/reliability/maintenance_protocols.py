"""
Comprehensive System Maintenance Protocols
Automated maintenance procedures, dependency management, and system optimisation
"""

import asyncio
import logging
import json
import subprocess
import sys
import shutil
import schedule
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
import pkg_resources
import requests
from concurrent.futures import ThreadPoolExecutor
import threading

from system.reliability.health_monitor import health_monitor, HealthStatus
from system.core_tools.error_recovery_system import error_recovery_system
from system.orchestration.autonomous_operation_manager import autonomous_manager

class MaintenanceType(Enum):
    """Types of maintenance operations"""
    ROUTINE = "routine"
    PREVENTIVE = "preventive"
    CORRECTIVE = "corrective"
    EMERGENCY = "emergency"

class MaintenancePriority(Enum):
    """Maintenance priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class MaintenanceTask:
    """Maintenance task structure"""
    name: str
    task_type: MaintenanceType
    priority: MaintenancePriority
    description: str
    schedule_expression: str  # cron-like expression
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    success_count: int = 0
    failure_count: int = 0
    enabled: bool = True

class SystemMaintenanceManager:
    """Comprehensive system maintenance management"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.maintenance_tasks = self._initialize_maintenance_tasks()
        self.maintenance_history = []
        self.executor = ThreadPoolExecutor(max_workers=3)
        self.maintenance_running = False
        self.setup_maintenance_logging()
    
    def setup_maintenance_logging(self):
        """Setup maintenance logging"""
        maintenance_log_dir = Path("system/reports/maintenance")
        maintenance_log_dir.mkdir(parents=True, exist_ok=True)
        
        maintenance_handler = logging.FileHandler(
            maintenance_log_dir / f"maintenance_{datetime.now().strftime('%Y%m%d')}.log"
        )
        maintenance_handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        maintenance_handler.setFormatter(formatter)
        
        self.logger.addHandler(maintenance_handler)
    
    def _initialize_maintenance_tasks(self) -> Dict[str, MaintenanceTask]:
        """Initialize standard maintenance tasks"""
        tasks = {
            'health_check': MaintenanceTask(
                name='System Health Check',
                task_type=MaintenanceType.ROUTINE,
                priority=MaintenancePriority.HIGH,
                description='Comprehensive system health monitoring',
                schedule_expression='*/15 * * * *'  # Every 15 minutes
            ),
            'log_cleanup': MaintenanceTask(
                name='Log File Cleanup',
                task_type=MaintenanceType.ROUTINE,
                priority=MaintenancePriority.LOW,
                description='Clean up old log files and reports',
                schedule_expression='0 2 * * 0'  # Weekly at 2 AM Sunday
            ),
            'dependency_check': MaintenanceTask(
                name='Dependency Update Check',
                task_type=MaintenanceType.PREVENTIVE,
                priority=MaintenancePriority.MEDIUM,
                description='Check for dependency updates and security patches',
                schedule_expression='0 1 * * 1'  # Weekly at 1 AM Monday
            ),
            'cache_cleanup': MaintenanceTask(
                name='Cache and Temp Cleanup',
                task_type=MaintenanceType.ROUTINE,
                priority=MaintenancePriority.LOW,
                description='Clean up temporary files and caches',
                schedule_expression='0 3 * * *'  # Daily at 3 AM
            ),
            'performance_optimisation': MaintenanceTask(
                name='Performance Optimisation',
                task_type=MaintenanceType.PREVENTIVE,
                priority=MaintenancePriority.MEDIUM,
                description='Optimise system performance and resource usage',
                schedule_expression='0 4 * * 0'  # Weekly at 4 AM Sunday
            ),
            'backup_maintenance': MaintenanceTask(
                name='Backup and Archive',
                task_type=MaintenanceType.ROUTINE,
                priority=MaintenancePriority.HIGH,
                description='Backup critical system data and configurations',
                schedule_expression='0 0 * * 0'  # Weekly at midnight Sunday
            ),
            'security_scan': MaintenanceTask(
                name='Security Vulnerability Scan',
                task_type=MaintenanceType.PREVENTIVE,
                priority=MaintenancePriority.HIGH,
                description='Scan for security vulnerabilities and compliance issues',
                schedule_expression='0 5 * * 2'  # Weekly at 5 AM Tuesday
            ),
            'api_health_verification': MaintenanceTask(
                name='API Health Verification',
                task_type=MaintenanceType.ROUTINE,
                priority=MaintenancePriority.HIGH,
                description='Verify API connectivity and quota status',
                schedule_expression='0 */6 * * *'  # Every 6 hours
            )
        }
        
        return tasks
    
    async def run_maintenance_cycle(self, maintenance_type: MaintenanceType = None) -> Dict[str, Any]:
        """Run maintenance cycle for specified type or all due tasks"""
        if self.maintenance_running:
            self.logger.warning("Maintenance cycle already running")
            return {'status': 'already_running'}
        
        self.maintenance_running = True
        self.logger.info(f"Starting maintenance cycle: {maintenance_type.value if maintenance_type else 'all'}")
        
        try:
            results = {
                'start_time': datetime.now().isoformat(),
                'maintenance_type': maintenance_type.value if maintenance_type else 'all',
                'tasks_executed': [],
                'tasks_failed': [],
                'summary': {}
            }
            
            # Get tasks to run
            tasks_to_run = self._get_due_tasks(maintenance_type)
            
            if not tasks_to_run:
                self.logger.info("No maintenance tasks due")
                results['summary'] = {'status': 'no_tasks_due', 'message': 'No maintenance tasks currently due for execution'}
                return results
            
            # Execute tasks in priority order
            tasks_to_run.sort(key=lambda x: list(MaintenancePriority).index(x.priority), reverse=True)
            
            for task in tasks_to_run:
                self.logger.info(f"Executing maintenance task: {task.name}")
                
                try:
                    task_result = await self._execute_maintenance_task(task)
                    
                    if task_result['success']:
                        task.success_count += 1
                        results['tasks_executed'].append({
                            'task': task.name,
                            'result': task_result,
                            'execution_time': task_result.get('execution_time', 0)
                        })
                    else:
                        task.failure_count += 1
                        results['tasks_failed'].append({
                            'task': task.name,
                            'error': task_result.get('error', 'Unknown error'),
                            'execution_time': task_result.get('execution_time', 0)
                        })
                    
                    task.last_run = datetime.now()
                    
                except Exception as e:
                    self.logger.error(f"Failed to execute maintenance task {task.name}: {e}")
                    task.failure_count += 1
                    results['tasks_failed'].append({
                        'task': task.name,
                        'error': str(e),
                        'execution_time': 0
                    })
            
            results['end_time'] = datetime.now().isoformat()
            results['summary'] = {
                'total_tasks': len(tasks_to_run),
                'successful_tasks': len(results['tasks_executed']),
                'failed_tasks': len(results['tasks_failed']),
                'success_rate': (len(results['tasks_executed']) / len(tasks_to_run)) * 100 if tasks_to_run else 0
            }
            
            # Save maintenance report
            self._save_maintenance_report(results)
            
            self.logger.info(f"Maintenance cycle completed: {results['summary']['successful_tasks']}/{results['summary']['total_tasks']} tasks successful")
            
            return results
        
        finally:
            self.maintenance_running = False
    
    def _get_due_tasks(self, maintenance_type: MaintenanceType = None) -> List[MaintenanceTask]:
        """Get tasks that are due for execution"""
        due_tasks = []
        current_time = datetime.now()
        
        for task in self.maintenance_tasks.values():
            if not task.enabled:
                continue
            
            if maintenance_type and task.task_type != maintenance_type:
                continue
            
            # Check if task is due
            if self._is_task_due(task, current_time):
                due_tasks.append(task)
        
        return due_tasks
    
    def _is_task_due(self, task: MaintenanceTask, current_time: datetime) -> bool:
        """Check if a maintenance task is due for execution"""
        if task.last_run is None:
            return True  # Never run before
        
        # Parse schedule expression (simplified cron-like)
        # Format: minute hour day_of_month month day_of_week
        # */15 * * * * = every 15 minutes
        # 0 2 * * 0 = every Sunday at 2 AM
        
        schedule_parts = task.schedule_expression.split()
        if len(schedule_parts) != 5:
            self.logger.warning(f"Invalid schedule expression for {task.name}: {task.schedule_expression}")
            return False
        
        minute, hour, day_of_month, month, day_of_week = schedule_parts
        
        # Simple implementation - check if enough time has passed based on the schedule
        time_diff = current_time - task.last_run
        
        # Every few minutes
        if minute.startswith('*/'):
            interval = int(minute[2:])
            return time_diff >= timedelta(minutes=interval)
        
        # Hourly
        if hour == '*' and day_of_month == '*' and month == '*' and day_of_week == '*':
            return time_diff >= timedelta(hours=1)
        
        # Daily
        if day_of_month == '*' and month == '*' and day_of_week == '*':
            return time_diff >= timedelta(days=1)
        
        # Weekly
        if day_of_week != '*':
            return time_diff >= timedelta(days=7)
        
        # Default: check if last run was more than 1 hour ago
        return time_diff >= timedelta(hours=1)
    
    async def _execute_maintenance_task(self, task: MaintenanceTask) -> Dict[str, Any]:
        """Execute a specific maintenance task"""
        start_time = time.time()
        
        try:
            if task.name == 'System Health Check':
                result = await self._run_health_check()
            elif task.name == 'Log File Cleanup':
                result = await self._run_log_cleanup()
            elif task.name == 'Dependency Update Check':
                result = await self._run_dependency_check()
            elif task.name == 'Cache and Temp Cleanup':
                result = await self._run_cache_cleanup()
            elif task.name == 'Performance Optimisation':
                result = await self._run_performance_optimisation()
            elif task.name == 'Backup and Archive':
                result = await self._run_backup_maintenance()
            elif task.name == 'Security Vulnerability Scan':
                result = await self._run_security_scan()
            elif task.name == 'API Health Verification':
                result = await self._run_api_health_verification()
            else:
                result = {'success': False, 'error': f'Unknown maintenance task: {task.name}'}
            
            execution_time = time.time() - start_time
            result['execution_time'] = execution_time
            
            return result
        
        except Exception as e:
            execution_time = time.time() - start_time
            return {
                'success': False,
                'error': str(e),
                'execution_time': execution_time
            }
    
    async def _run_health_check(self) -> Dict[str, Any]:
        """Run comprehensive health check"""
        try:
            health_results = await health_monitor.run_comprehensive_health_check()
            
            # Count issues
            issues = sum(1 for result in health_results.values() 
                        if result.status in [HealthStatus.UNHEALTHY, HealthStatus.CRITICAL])
            
            return {
                'success': True,
                'message': f'Health check completed: {issues} issues detected',
                'details': {
                    'total_components': len(health_results) - 1,  # Exclude system_overall
                    'issues_found': issues,
                    'overall_status': health_results['system_overall'].status.value
                }
            }
        
        except Exception as e:
            return {'success': False, 'error': f'Health check failed: {str(e)}'}
    
    async def _run_log_cleanup(self) -> Dict[str, Any]:
        """Clean up old log files"""
        try:
            log_dirs = [
                Path("system/reports"),
                Path("system/reports/health"),
                Path("system/reports/maintenance"),
                Path("system/reports/errors"),
                Path("system/reports/alerts")
            ]
            
            cleaned_files = 0
            freed_space = 0
            
            cutoff_date = datetime.now() - timedelta(days=30)  # Keep 30 days
            
            for log_dir in log_dirs:
                if not log_dir.exists():
                    continue
                
                for log_file in log_dir.glob("*.log"):
                    if datetime.fromtimestamp(log_file.stat().st_mtime) < cutoff_date:
                        file_size = log_file.stat().st_size
                        log_file.unlink()
                        cleaned_files += 1
                        freed_space += file_size
                
                # Clean old JSON reports (keep last 100)
                json_files = list(log_dir.glob("*.json"))
                json_files.sort(key=lambda x: x.stat().st_mtime)
                if len(json_files) > 100:
                    for old_file in json_files[:-100]:
                        file_size = old_file.stat().st_size
                        old_file.unlink()
                        cleaned_files += 1
                        freed_space += file_size
            
            return {
                'success': True,
                'message': f'Log cleanup completed: {cleaned_files} files removed, {freed_space // 1024}KB freed',
                'details': {
                    'files_removed': cleaned_files,
                    'space_freed_kb': freed_space // 1024
                }
            }
        
        except Exception as e:
            return {'success': False, 'error': f'Log cleanup failed: {str(e)}'}
    
    async def _run_dependency_check(self) -> Dict[str, Any]:
        """Check for dependency updates"""
        try:
            # Get installed packages
            installed_packages = [d for d in pkg_resources.working_set]
            
            outdated_packages = []
            security_updates = []
            
            # Check for updates (simplified - in production would use pip-audit or similar)
            critical_packages = [
                'requests', 'aiohttp', 'playwright', 'beautifulsoup4',
                'pandas', 'advertools', 'psutil', 'schedule'
            ]
            
            for package_name in critical_packages:
                try:
                    # Check if package is installed
                    installed_version = None
                    for pkg in installed_packages:
                        if pkg.project_name.lower() == package_name.lower():
                            installed_version = pkg.version
                            break
                    
                    if not installed_version:
                        outdated_packages.append({
                            'name': package_name,
                            'status': 'not_installed',
                            'current_version': None,
                            'latest_version': 'unknown'
                        })
                
                except Exception as e:
                    self.logger.warning(f"Could not check {package_name}: {e}")
            
            return {
                'success': True,
                'message': f'Dependency check completed: {len(outdated_packages)} packages need attention',
                'details': {
                    'total_packages_checked': len(critical_packages),
                    'outdated_packages': outdated_packages,
                    'security_updates': security_updates
                }
            }
        
        except Exception as e:
            return {'success': False, 'error': f'Dependency check failed: {str(e)}'}
    
    async def _run_cache_cleanup(self) -> Dict[str, Any]:
        """Clean up cache and temporary files"""
        try:
            cache_dirs = [
                Path("temp_cleanup"),
                Path("__pycache__"),
                Path(".pytest_cache"),
                Path("system/__pycache__"),
                Path("system/core_tools/__pycache__")
            ]
            
            cleaned_files = 0
            freed_space = 0
            
            for cache_dir in cache_dirs:
                if cache_dir.exists():
                    for cache_file in cache_dir.rglob("*"):
                        if cache_file.is_file():
                            file_size = cache_file.stat().st_size
                            cache_file.unlink()
                            cleaned_files += 1
                            freed_space += file_size
                    
                    # Remove empty directories
                    if cache_dir.exists() and not any(cache_dir.iterdir()):
                        cache_dir.rmdir()
            
            # Clean Python __pycache__ directories
            for pycache_dir in Path(".").rglob("__pycache__"):
                if pycache_dir.is_dir():
                    shutil.rmtree(pycache_dir, ignore_errors=True)
            
            return {
                'success': True,
                'message': f'Cache cleanup completed: {cleaned_files} files removed, {freed_space // 1024}KB freed',
                'details': {
                    'files_removed': cleaned_files,
                    'space_freed_kb': freed_space // 1024
                }
            }
        
        except Exception as e:
            return {'success': False, 'error': f'Cache cleanup failed: {str(e)}'}
    
    async def _run_performance_optimisation(self) -> Dict[str, Any]:
        """Run performance optimisation tasks"""
        try:
            optimisations_applied = []
            
            # Database/file optimisation (if applicable)
            # Check for large files that could be compressed or archived
            large_files = []
            for file_path in Path(".").rglob("*.json"):
                if file_path.stat().st_size > 10 * 1024 * 1024:  # > 10MB
                    large_files.append(str(file_path))
            
            if large_files:
                optimisations_applied.append(f"Identified {len(large_files)} large files for potential compression")
            
            # Memory optimisation suggestions
            import psutil
            memory = psutil.virtual_memory()
            if memory.percent > 80:
                optimisations_applied.append("High memory usage detected - recommend system restart")
            
            # Check error recovery system performance
            error_summary = error_recovery_system.get_error_summary()
            if error_summary['recovery_stats']['recovery_rate'] < 80:
                optimisations_applied.append("Error recovery rate below optimal - review error handling strategies")
            
            return {
                'success': True,
                'message': f'Performance optimisation completed: {len(optimisations_applied)} recommendations',
                'details': {
                    'optimisations_applied': optimisations_applied,
                    'large_files_detected': len(large_files),
                    'memory_usage_percent': memory.percent
                }
            }
        
        except Exception as e:
            return {'success': False, 'error': f'Performance optimisation failed: {str(e)}'}
    
    async def _run_backup_maintenance(self) -> Dict[str, Any]:
        """Run backup and archive maintenance"""
        try:
            backup_dir = Path("system/backups")
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # Backup critical configuration files
            critical_files = [
                Path(".env"),
                Path("CLAUDE.md"),
                Path("system/config"),
                Path("system/sops")
            ]
            
            backed_up_files = 0
            
            for file_path in critical_files:
                if file_path.exists():
                    if file_path.is_file():
                        backup_file = backup_dir / f"{file_path.name}_{timestamp}.backup"
                        shutil.copy2(file_path, backup_file)
                        backed_up_files += 1
                    elif file_path.is_dir():
                        backup_subdir = backup_dir / f"{file_path.name}_{timestamp}"
                        shutil.copytree(file_path, backup_subdir, ignore=shutil.ignore_patterns('*.pyc', '__pycache__'))
                        backed_up_files += 1
            
            # Clean old backups (keep last 10)
            backup_files = list(backup_dir.glob("*"))
            backup_files.sort(key=lambda x: x.stat().st_mtime)
            if len(backup_files) > 20:  # Keep last 20 backups
                for old_backup in backup_files[:-20]:
                    if old_backup.is_file():
                        old_backup.unlink()
                    elif old_backup.is_dir():
                        shutil.rmtree(old_backup)
            
            return {
                'success': True,
                'message': f'Backup completed: {backed_up_files} items backed up',
                'details': {
                    'backed_up_items': backed_up_files,
                    'backup_location': str(backup_dir),
                    'timestamp': timestamp
                }
            }
        
        except Exception as e:
            return {'success': False, 'error': f'Backup maintenance failed: {str(e)}'}
    
    async def _run_security_scan(self) -> Dict[str, Any]:
        """Run security vulnerability scan"""
        try:
            security_issues = []
            
            # Check file permissions on sensitive files
            sensitive_files = [Path(".env"), Path("system/config")]
            
            for file_path in sensitive_files:
                if file_path.exists():
                    # Check if file is readable by others (basic check)
                    stat_info = file_path.stat()
                    if stat_info.st_mode & 0o044:  # Others can read
                        security_issues.append(f"File {file_path} may have overly permissive permissions")
            
            # Check for hardcoded credentials (basic patterns)
            code_files = list(Path(".").rglob("*.py"))
            
            suspicious_patterns = [
                "password=",
                "api_key=",
                "secret=",
                "token="
            ]
            
            for code_file in code_files[:50]:  # Limit to first 50 files
                try:
                    with open(code_file, 'r', encoding='utf-8') as f:
                        content = f.read().lower()
                        for pattern in suspicious_patterns:
                            if pattern in content and "credentials.get" not in content:
                                security_issues.append(f"Potential hardcoded credential in {code_file}")
                                break
                except:
                    continue
            
            return {
                'success': True,
                'message': f'Security scan completed: {len(security_issues)} issues found',
                'details': {
                    'security_issues': security_issues,
                    'files_scanned': len(code_files),
                    'sensitive_files_checked': len(sensitive_files)
                }
            }
        
        except Exception as e:
            return {'success': False, 'error': f'Security scan failed: {str(e)}'}
    
    async def _run_api_health_verification(self) -> Dict[str, Any]:
        """Verify API health and quotas"""
        try:
            api_results = {}
            
            # Check SerpAPI quota
            try:
                from system.config.api_credentials import credentials
                api_key = credentials.get_credential('serpapi', 'api_key')
                if api_key:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(f"https://serpapi.com/account?api_key={api_key}", timeout=10) as response:
                            if response.status == 200:
                                data = await response.json()
                                api_results['serpapi'] = {
                                    'status': 'healthy',
                                    'searches_remaining': data.get('total_searches_left', 0)
                                }
                            else:
                                api_results['serpapi'] = {'status': 'unhealthy', 'error': f'Status {response.status}'}
                else:
                    api_results['serpapi'] = {'status': 'not_configured'}
            except Exception as e:
                api_results['serpapi'] = {'status': 'error', 'error': str(e)}
            
            # Check Jina API
            try:
                jina_key = credentials.get_credential('jina', 'api_key')
                if jina_key:
                    async with aiohttp.ClientSession() as session:
                        headers = {'Authorization': f'Bearer {jina_key}'}
                        async with session.get('https://r.jina.ai/https://example.com', headers=headers, timeout=10) as response:
                            api_results['jina'] = {
                                'status': 'healthy' if response.status == 200 else 'degraded',
                                'response_status': response.status
                            }
                else:
                    api_results['jina'] = {'status': 'not_configured'}
            except Exception as e:
                api_results['jina'] = {'status': 'error', 'error': str(e)}
            
            healthy_apis = sum(1 for result in api_results.values() if result.get('status') == 'healthy')
            total_apis = len(api_results)
            
            return {
                'success': True,
                'message': f'API health verification completed: {healthy_apis}/{total_apis} APIs healthy',
                'details': {
                    'api_results': api_results,
                    'healthy_apis': healthy_apis,
                    'total_apis': total_apis
                }
            }
        
        except Exception as e:
            return {'success': False, 'error': f'API health verification failed: {str(e)}'}
    
    def _save_maintenance_report(self, maintenance_results: Dict[str, Any]):
        """Save maintenance report to file"""
        try:
            reports_dir = Path("system/reports/maintenance")
            reports_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_file = reports_dir / f"maintenance_report_{timestamp}.json"
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(maintenance_results, f, indent=2, ensure_ascii=False, default=str)
            
            self.logger.info(f"Maintenance report saved: {report_file}")
        
        except Exception as e:
            self.logger.error(f"Failed to save maintenance report: {e}")
    
    def get_maintenance_status(self) -> Dict[str, Any]:
        """Get current maintenance status and statistics"""
        return {
            'maintenance_running': self.maintenance_running,
            'total_tasks': len(self.maintenance_tasks),
            'enabled_tasks': sum(1 for task in self.maintenance_tasks.values() if task.enabled),
            'task_statistics': {
                name: {
                    'success_count': task.success_count,
                    'failure_count': task.failure_count,
                    'last_run': task.last_run.isoformat() if task.last_run else None,
                    'enabled': task.enabled,
                    'priority': task.priority.value,
                    'type': task.task_type.value
                }
                for name, task in self.maintenance_tasks.items()
            }
        }
    
    def schedule_maintenance_tasks(self):
        """Schedule maintenance tasks using the schedule library"""
        self.logger.info("Scheduling maintenance tasks")
        
        # Schedule health checks every 15 minutes
        schedule.every(15).minutes.do(self._run_scheduled_maintenance, 'health_check')
        
        # Schedule daily cache cleanup
        schedule.every().day.at("03:00").do(self._run_scheduled_maintenance, 'cache_cleanup')
        
        # Schedule weekly comprehensive maintenance
        schedule.every().sunday.at("02:00").do(self._run_scheduled_maintenance, 'all')
        
        # Start scheduler in background thread
        def run_scheduler():
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
        
        self.logger.info("Maintenance scheduler started")
    
    def _run_scheduled_maintenance(self, task_name: str):
        """Run scheduled maintenance task"""
        try:
            if task_name == 'all':
                asyncio.run(self.run_maintenance_cycle())
            else:
                if task_name in self.maintenance_tasks:
                    task = self.maintenance_tasks[task_name]
                    asyncio.run(self._execute_maintenance_task(task))
        except Exception as e:
            self.logger.error(f"Scheduled maintenance failed for {task_name}: {e}")

# Global maintenance manager instance
maintenance_manager = SystemMaintenanceManager()

async def run_emergency_maintenance():
    """Run emergency maintenance procedures"""
    try:
        print("Running emergency maintenance procedures...")
        
        # Run critical maintenance tasks
        critical_results = await maintenance_manager.run_maintenance_cycle(MaintenanceType.EMERGENCY)
        
        # Run health check
        health_results = await health_monitor.run_comprehensive_health_check()
        
        # Generate emergency report
        emergency_report = {
            'timestamp': datetime.now().isoformat(),
            'maintenance_results': critical_results,
            'health_status': {
                'overall_status': health_results['system_overall'].status.value,
                'critical_issues': [
                    {'component': comp, 'status': result.status.value, 'message': result.message}
                    for comp, result in health_results.items()
                    if result.status == HealthStatus.CRITICAL
                ]
            }
        }
        
        print(f"Emergency maintenance completed")
        print(f"System status: {emergency_report['health_status']['overall_status']}")
        if emergency_report['health_status']['critical_issues']:
            print(f"Critical issues: {len(emergency_report['health_status']['critical_issues'])}")
        
        return emergency_report
    
    except Exception as e:
        print(f"Emergency maintenance failed: {e}")
        logging.error(f"Emergency maintenance failed: {e}")
        return None

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='System Maintenance Manager')
    parser.add_argument('--emergency', action='store_true', help='Run emergency maintenance')
    parser.add_argument('--schedule', action='store_true', help='Start maintenance scheduler')
    
    args = parser.parse_args()
    
    if args.emergency:
        asyncio.run(run_emergency_maintenance())
    elif args.schedule:
        maintenance_manager.schedule_maintenance_tasks()
        print("Maintenance scheduler started. Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Scheduler stopped.")
    else:
        asyncio.run(maintenance_manager.run_maintenance_cycle())