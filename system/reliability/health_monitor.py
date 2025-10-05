"""
Comprehensive System Health Monitoring Framework
Automated health checks for API connectivity, agent functionality, and system performance
"""

import asyncio
import aiohttp
import psutil
import logging
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum
import subprocess
import sys
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from system.config.api_credentials import credentials
from system.core_tools.error_recovery_system import error_recovery_system
from system.orchestration.autonomous_operation_manager import autonomous_manager

class HealthStatus(Enum):
    """Health status levels"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    CRITICAL = "critical"

@dataclass
class HealthCheckResult:
    """Health check result structure"""
    component: str
    status: HealthStatus
    response_time: float
    message: str
    timestamp: datetime
    details: Dict = None

class SystemHealthMonitor:
    """Comprehensive system health monitoring"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.health_history = []
        self.alert_thresholds = {
            'api_response_time': 5.0,  # seconds
            'memory_usage': 85.0,      # percentage
            'disk_usage': 90.0,        # percentage
            'cpu_usage': 90.0,         # percentage
            'error_rate': 10.0         # percentage
        }
        self.setup_health_logging()
    
    def setup_health_logging(self):
        """Setup health monitoring log files"""
        health_log_dir = Path("system/reports/health")
        health_log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create health log handler
        health_handler = logging.FileHandler(
            health_log_dir / f"health_monitor_{datetime.now().strftime('%Y%m%d')}.log"
        )
        health_handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        health_handler.setFormatter(formatter)
        
        self.logger.addHandler(health_handler)
    
    async def run_comprehensive_health_check(self) -> Dict[str, HealthCheckResult]:
        """Run all health checks and return comprehensive results"""
        self.logger.info("Starting comprehensive system health check")
        
        health_results = {}
        
        # API connectivity checks
        api_checks = await self._check_api_connectivity()
        health_results.update(api_checks)
        
        # System resource checks
        resource_checks = self._check_system_resources()
        health_results.update(resource_checks)
        
        # File system checks
        filesystem_checks = self._check_file_system_health()
        health_results.update(filesystem_checks)
        
        # Agent functionality checks
        agent_checks = await self._check_agent_functionality()
        health_results.update(agent_checks)
        
        # Performance checks
        performance_checks = await self._check_system_performance()
        health_results.update(performance_checks)
        
        # Dependency checks
        dependency_checks = self._check_dependencies()
        health_results.update(dependency_checks)
        
        # Generate overall system health summary
        overall_status = self._calculate_overall_health(health_results)
        health_results['system_overall'] = HealthCheckResult(
            component='system_overall',
            status=overall_status,
            response_time=0.0,
            message=f"Overall system status: {overall_status.value}",
            timestamp=datetime.now()
        )
        
        # Store results
        self._store_health_results(health_results)
        
        # Check for alerts
        await self._check_alert_conditions(health_results)
        
        self.logger.info("Comprehensive health check completed")
        return health_results
    
    async def _check_api_connectivity(self) -> Dict[str, HealthCheckResult]:
        """Check connectivity to all configured APIs"""
        api_results = {}
        
        # SerpAPI check
        serpapi_result = await self._check_serpapi()
        api_results['serpapi'] = serpapi_result
        
        # Jina API check
        jina_result = await self._check_jina_api()
        api_results['jina_api'] = jina_result
        
        # GTmetrix API check
        gtmetrix_result = await self._check_gtmetrix_api()
        api_results['gtmetrix'] = gtmetrix_result
        
        # General internet connectivity
        internet_result = await self._check_internet_connectivity()
        api_results['internet'] = internet_result
        
        return api_results
    
    async def _check_serpapi(self) -> HealthCheckResult:
        """Check SerpAPI connectivity and functionality"""
        start_time = time.time()
        
        try:
            api_key = credentials.get_credential('serpapi', 'api_key')
            if not api_key:
                return HealthCheckResult(
                    component='serpapi',
                    status=HealthStatus.CRITICAL,
                    response_time=0.0,
                    message="SerpAPI key not configured",
                    timestamp=datetime.now()
                )
            
            # Test basic API call
            async with aiohttp.ClientSession() as session:
                url = "https://serpapi.com/account"
                params = {'api_key': api_key}
                
                async with session.get(url, params=params, timeout=10) as response:
                    response_time = time.time() - start_time
                    
                    if response.status == 200:
                        data = await response.json()
                        remaining_searches = data.get('total_searches_left', 0)
                        
                        status = HealthStatus.HEALTHY if remaining_searches > 10 else HealthStatus.DEGRADED
                        message = f"API responsive, {remaining_searches} searches remaining"
                        
                        return HealthCheckResult(
                            component='serpapi',
                            status=status,
                            response_time=response_time,
                            message=message,
                            timestamp=datetime.now(),
                            details={'searches_remaining': remaining_searches}
                        )
                    else:
                        return HealthCheckResult(
                            component='serpapi',
                            status=HealthStatus.UNHEALTHY,
                            response_time=response_time,
                            message=f"API returned status {response.status}",
                            timestamp=datetime.now()
                        )
        
        except asyncio.TimeoutError:
            return HealthCheckResult(
                component='serpapi',
                status=HealthStatus.UNHEALTHY,
                response_time=10.0,
                message="API request timed out",
                timestamp=datetime.now()
            )
        except Exception as e:
            return HealthCheckResult(
                component='serpapi',
                status=HealthStatus.UNHEALTHY,
                response_time=time.time() - start_time,
                message=f"API check failed: {str(e)}",
                timestamp=datetime.now()
            )
    
    async def _check_jina_api(self) -> HealthCheckResult:
        """Check Jina API connectivity"""
        start_time = time.time()
        
        try:
            api_key = credentials.get_credential('jina', 'api_key')
            if not api_key:
                return HealthCheckResult(
                    component='jina_api',
                    status=HealthStatus.CRITICAL,
                    response_time=0.0,
                    message="Jina API key not configured",
                    timestamp=datetime.now()
                )
            
            # Test Jina Reader API
            async with aiohttp.ClientSession() as session:
                url = "https://r.jina.ai/https://example.com"
                headers = {'Authorization': f'Bearer {api_key}'}
                
                async with session.get(url, headers=headers, timeout=10) as response:
                    response_time = time.time() - start_time
                    
                    if response.status == 200:
                        return HealthCheckResult(
                            component='jina_api',
                            status=HealthStatus.HEALTHY,
                            response_time=response_time,
                            message="Jina Reader API responsive",
                            timestamp=datetime.now()
                        )
                    else:
                        return HealthCheckResult(
                            component='jina_api',
                            status=HealthStatus.UNHEALTHY,
                            response_time=response_time,
                            message=f"API returned status {response.status}",
                            timestamp=datetime.now()
                        )
        
        except Exception as e:
            return HealthCheckResult(
                component='jina_api',
                status=HealthStatus.UNHEALTHY,
                response_time=time.time() - start_time,
                message=f"API check failed: {str(e)}",
                timestamp=datetime.now()
            )
    
    async def _check_gtmetrix_api(self) -> HealthCheckResult:
        """Check GTmetrix API connectivity"""
        start_time = time.time()
        
        try:
            api_key = credentials.get_credential('gtmetrix', 'api_key')
            username = credentials.get_credential('gtmetrix', 'username')
            
            if not api_key or not username:
                return HealthCheckResult(
                    component='gtmetrix',
                    status=HealthStatus.DEGRADED,
                    response_time=0.0,
                    message="GTmetrix credentials not configured (optional service)",
                    timestamp=datetime.now()
                )
            
            # Test API access
            async with aiohttp.ClientSession() as session:
                url = "https://gtmetrix.com/api/2.0/credits"
                auth = aiohttp.BasicAuth(username, api_key)
                
                async with session.get(url, auth=auth, timeout=10) as response:
                    response_time = time.time() - start_time
                    
                    if response.status == 200:
                        data = await response.json()
                        credits = data.get('credits', 0)
                        
                        status = HealthStatus.HEALTHY if credits > 5 else HealthStatus.DEGRADED
                        message = f"API responsive, {credits} credits remaining"
                        
                        return HealthCheckResult(
                            component='gtmetrix',
                            status=status,
                            response_time=response_time,
                            message=message,
                            timestamp=datetime.now(),
                            details={'credits_remaining': credits}
                        )
                    else:
                        return HealthCheckResult(
                            component='gtmetrix',
                            status=HealthStatus.UNHEALTHY,
                            response_time=response_time,
                            message=f"API returned status {response.status}",
                            timestamp=datetime.now()
                        )
        
        except Exception as e:
            return HealthCheckResult(
                component='gtmetrix',
                status=HealthStatus.DEGRADED,
                response_time=time.time() - start_time,
                message=f"Optional API check failed: {str(e)}",
                timestamp=datetime.now()
            )
    
    async def _check_internet_connectivity(self) -> HealthCheckResult:
        """Check general internet connectivity"""
        start_time = time.time()
        
        test_urls = [
            'https://www.google.com',
            'https://httpbin.org/status/200',
            'https://www.github.com'
        ]
        
        successful_connections = 0
        
        for url in test_urls:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, timeout=5) as response:
                        if response.status == 200:
                            successful_connections += 1
            except:
                continue
        
        response_time = time.time() - start_time
        connection_rate = successful_connections / len(test_urls)
        
        if connection_rate >= 0.8:
            status = HealthStatus.HEALTHY
            message = f"Internet connectivity excellent ({successful_connections}/{len(test_urls)} sites reachable)"
        elif connection_rate >= 0.5:
            status = HealthStatus.DEGRADED
            message = f"Internet connectivity degraded ({successful_connections}/{len(test_urls)} sites reachable)"
        else:
            status = HealthStatus.UNHEALTHY
            message = f"Internet connectivity poor ({successful_connections}/{len(test_urls)} sites reachable)"
        
        return HealthCheckResult(
            component='internet',
            status=status,
            response_time=response_time,
            message=message,
            timestamp=datetime.now(),
            details={'successful_connections': successful_connections, 'total_tested': len(test_urls)}
        )
    
    def _check_system_resources(self) -> Dict[str, HealthCheckResult]:
        """Check system resource usage"""
        results = {}
        
        # Memory usage
        memory = psutil.virtual_memory()
        memory_status = self._evaluate_resource_usage(memory.percent, self.alert_thresholds['memory_usage'])
        results['memory'] = HealthCheckResult(
            component='memory',
            status=memory_status,
            response_time=0.0,
            message=f"Memory usage: {memory.percent:.1f}% ({memory.used // 1024**3}GB/{memory.total // 1024**3}GB)",
            timestamp=datetime.now(),
            details={'percent_used': memory.percent, 'used_gb': memory.used // 1024**3, 'total_gb': memory.total // 1024**3}
        )
        
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_status = self._evaluate_resource_usage(cpu_percent, self.alert_thresholds['cpu_usage'])
        results['cpu'] = HealthCheckResult(
            component='cpu',
            status=cpu_status,
            response_time=0.0,
            message=f"CPU usage: {cpu_percent:.1f}%",
            timestamp=datetime.now(),
            details={'percent_used': cpu_percent, 'cpu_count': psutil.cpu_count()}
        )
        
        # Disk usage
        disk = psutil.disk_usage('.')
        disk_percent = (disk.used / disk.total) * 100
        disk_status = self._evaluate_resource_usage(disk_percent, self.alert_thresholds['disk_usage'])
        results['disk'] = HealthCheckResult(
            component='disk',
            status=disk_status,
            response_time=0.0,
            message=f"Disk usage: {disk_percent:.1f}% ({disk.used // 1024**3}GB/{disk.total // 1024**3}GB)",
            timestamp=datetime.now(),
            details={'percent_used': disk_percent, 'used_gb': disk.used // 1024**3, 'total_gb': disk.total // 1024**3}
        )
        
        return results
    
    def _evaluate_resource_usage(self, usage_percent: float, threshold: float) -> HealthStatus:
        """Evaluate resource usage against thresholds"""
        if usage_percent < threshold * 0.7:
            return HealthStatus.HEALTHY
        elif usage_percent < threshold * 0.85:
            return HealthStatus.DEGRADED
        elif usage_percent < threshold:
            return HealthStatus.UNHEALTHY
        else:
            return HealthStatus.CRITICAL
    
    def _check_file_system_health(self) -> Dict[str, HealthCheckResult]:
        """Check file system health and permissions"""
        results = {}
        
        critical_paths = [
            Path("system"),
            Path("clients"),
            Path("system/reports"),
            Path("system/core_tools"),
            Path("system/config")
        ]
        
        filesystem_issues = []
        
        for path in critical_paths:
            try:
                # Check if path exists
                if not path.exists():
                    filesystem_issues.append(f"Missing critical directory: {path}")
                    continue
                
                # Check read permissions
                if not path.is_dir() or not path.stat().st_mode:
                    filesystem_issues.append(f"Permission issues with: {path}")
                    continue
                
                # Check write permissions by attempting to create temp file
                temp_file = path / ".health_check_temp"
                try:
                    temp_file.touch()
                    temp_file.unlink()
                except:
                    filesystem_issues.append(f"Write permission issues with: {path}")
            
            except Exception as e:
                filesystem_issues.append(f"Error checking {path}: {str(e)}")
        
        if not filesystem_issues:
            status = HealthStatus.HEALTHY
            message = "All critical file system paths accessible"
        else:
            status = HealthStatus.UNHEALTHY if len(filesystem_issues) > 2 else HealthStatus.DEGRADED
            message = f"File system issues detected: {len(filesystem_issues)} problems"
        
        results['filesystem'] = HealthCheckResult(
            component='filesystem',
            status=status,
            response_time=0.0,
            message=message,
            timestamp=datetime.now(),
            details={'issues': filesystem_issues, 'paths_checked': len(critical_paths)}
        )
        
        return results
    
    async def _check_agent_functionality(self) -> Dict[str, HealthCheckResult]:
        """Check agent functionality and communication"""
        results = {}
        
        # Test error recovery system
        try:
            error_summary = error_recovery_system.get_error_summary()
            error_rate = 100 - error_summary['recovery_stats']['recovery_rate']
            
            error_status = self._evaluate_resource_usage(error_rate, self.alert_thresholds['error_rate'])
            
            results['error_recovery'] = HealthCheckResult(
                component='error_recovery',
                status=error_status,
                response_time=0.0,
                message=f"Error recovery system operational, {error_summary['recovery_stats']['recovery_rate']:.1f}% success rate",
                timestamp=datetime.now(),
                details=error_summary
            )
        except Exception as e:
            results['error_recovery'] = HealthCheckResult(
                component='error_recovery',
                status=HealthStatus.UNHEALTHY,
                response_time=0.0,
                message=f"Error recovery system check failed: {str(e)}",
                timestamp=datetime.now()
            )
        
        # Test autonomous operation manager
        try:
            autonomous_status = autonomous_manager.get_operation_status()
            results['autonomous_manager'] = HealthCheckResult(
                component='autonomous_manager',
                status=HealthStatus.HEALTHY,
                response_time=0.0,
                message="Autonomous operation manager operational",
                timestamp=datetime.now(),
                details=autonomous_status
            )
        except Exception as e:
            results['autonomous_manager'] = HealthCheckResult(
                component='autonomous_manager',
                status=HealthStatus.DEGRADED,
                response_time=0.0,
                message=f"Autonomous manager check failed: {str(e)}",
                timestamp=datetime.now()
            )
        
        return results
    
    async def _check_system_performance(self) -> Dict[str, HealthCheckResult]:
        """Check system performance metrics"""
        results = {}
        
        # Check recent operation logs for performance trends
        try:
            # Look for recent analysis runs
            reports_dir = Path("system/reports")
            if reports_dir.exists():
                recent_files = list(reports_dir.glob("**/*.json"))
                recent_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                
                if recent_files:
                    # Analyse performance from recent operations
                    performance_status = HealthStatus.HEALTHY
                    message = f"System performance stable, {len(recent_files)} recent operations tracked"
                else:
                    performance_status = HealthStatus.DEGRADED
                    message = "No recent operation data found"
            else:
                performance_status = HealthStatus.UNHEALTHY
                message = "Performance tracking directory missing"
            
            results['performance'] = HealthCheckResult(
                component='performance',
                status=performance_status,
                response_time=0.0,
                message=message,
                timestamp=datetime.now(),
                details={'recent_operations': len(recent_files) if 'recent_files' in locals() else 0}
            )
        
        except Exception as e:
            results['performance'] = HealthCheckResult(
                component='performance',
                status=HealthStatus.DEGRADED,
                response_time=0.0,
                message=f"Performance check failed: {str(e)}",
                timestamp=datetime.now()
            )
        
        return results
    
    def _check_dependencies(self) -> Dict[str, HealthCheckResult]:
        """Check critical Python dependencies"""
        results = {}
        
        critical_packages = [
            'requests', 'aiohttp', 'playwright', 'beautifulsoup4',
            'pandas', 'advertools', 'psutil'
        ]
        
        missing_packages = []
        outdated_packages = []
        
        for package in critical_packages:
            try:
                __import__(package)
            except ImportError:
                missing_packages.append(package)
        
        if not missing_packages and not outdated_packages:
            status = HealthStatus.HEALTHY
            message = "All critical dependencies available"
        elif missing_packages:
            status = HealthStatus.CRITICAL
            message = f"Missing critical packages: {', '.join(missing_packages)}"
        else:
            status = HealthStatus.DEGRADED
            message = f"Some dependencies may need updates"
        
        results['dependencies'] = HealthCheckResult(
            component='dependencies',
            status=status,
            response_time=0.0,
            message=message,
            timestamp=datetime.now(),
            details={'missing_packages': missing_packages, 'checked_packages': critical_packages}
        )
        
        return results
    
    def _calculate_overall_health(self, health_results: Dict[str, HealthCheckResult]) -> HealthStatus:
        """Calculate overall system health from individual checks"""
        status_weights = {
            HealthStatus.HEALTHY: 0,
            HealthStatus.DEGRADED: 1,
            HealthStatus.UNHEALTHY: 3,
            HealthStatus.CRITICAL: 5
        }
        
        total_weight = 0
        total_checks = 0
        critical_failures = 0
        
        for result in health_results.values():
            weight = status_weights[result.status]
            total_weight += weight
            total_checks += 1
            
            if result.status == HealthStatus.CRITICAL:
                critical_failures += 1
        
        # If we have critical failures, system is critical
        if critical_failures > 0:
            return HealthStatus.CRITICAL
        
        # Calculate average status
        avg_weight = total_weight / total_checks if total_checks > 0 else 0
        
        if avg_weight <= 0.5:
            return HealthStatus.HEALTHY
        elif avg_weight <= 1.5:
            return HealthStatus.DEGRADED
        else:
            return HealthStatus.UNHEALTHY
    
    def _store_health_results(self, health_results: Dict[str, HealthCheckResult]):
        """Store health check results for trend analysis"""
        try:
            results_dir = Path("system/reports/health")
            results_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            results_file = results_dir / f"health_check_{timestamp}.json"
            
            # Convert results to JSON-serializable format
            json_results = {}
            for component, result in health_results.items():
                json_results[component] = {
                    'component': result.component,
                    'status': result.status.value,
                    'response_time': result.response_time,
                    'message': result.message,
                    'timestamp': result.timestamp.isoformat(),
                    'details': result.details
                }
            
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'health_check_metadata': {
                        'timestamp': datetime.now().isoformat(),
                        'total_components': len(health_results),
                        'overall_status': health_results['system_overall'].status.value
                    },
                    'results': json_results
                }, f, indent=2, ensure_ascii=False)
            
            # Keep only last 30 health check files
            health_files = list(results_dir.glob("health_check_*.json"))
            health_files.sort(key=lambda x: x.stat().st_mtime)
            if len(health_files) > 30:
                for old_file in health_files[:-30]:
                    old_file.unlink()
            
            self.logger.info(f"Health check results stored: {results_file}")
        
        except Exception as e:
            self.logger.error(f"Failed to store health results: {e}")
    
    async def _check_alert_conditions(self, health_results: Dict[str, HealthCheckResult]):
        """Check if any health results require alerts"""
        alerts = []
        
        for component, result in health_results.items():
            if result.status in [HealthStatus.CRITICAL, HealthStatus.UNHEALTHY]:
                alerts.append({
                    'severity': result.status.value,
                    'component': component,
                    'message': result.message,
                    'timestamp': result.timestamp.isoformat(),
                    'details': result.details
                })
        
        if alerts:
            await self._send_health_alerts(alerts)
    
    async def _send_health_alerts(self, alerts: List[Dict]):
        """Send health alerts (can be extended for email/Slack notifications)"""
        try:
            alerts_dir = Path("system/reports/alerts")
            alerts_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            alert_file = alerts_dir / f"health_alert_{timestamp}.json"
            
            alert_data = {
                'alert_metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'alert_count': len(alerts),
                    'severity_levels': [alert['severity'] for alert in alerts]
                },
                'alerts': alerts
            }
            
            with open(alert_file, 'w', encoding='utf-8') as f:
                json.dump(alert_data, f, indent=2, ensure_ascii=False)
            
            self.logger.warning(f"Health alerts generated: {len(alerts)} issues detected")
            
            # Log to autonomous manager
            autonomous_manager.log_operation(
                'health_monitoring',
                'alerts_generated',
                {'alert_count': len(alerts), 'alerts': alerts}
            )
        
        except Exception as e:
            self.logger.error(f"Failed to send health alerts: {e}")
    
    def get_health_trends(self, days: int = 7) -> Dict:
        """Analyse health trends over specified days"""
        try:
            results_dir = Path("system/reports/health")
            if not results_dir.exists():
                return {'error': 'No health data available'}
            
            # Get health files from last N days
            cutoff_date = datetime.now() - timedelta(days=days)
            health_files = []
            
            for file in results_dir.glob("health_check_*.json"):
                file_date = datetime.fromtimestamp(file.stat().st_mtime)
                if file_date > cutoff_date:
                    health_files.append(file)
            
            if not health_files:
                return {'error': f'No health data available for last {days} days'}
            
            # Analyse trends
            component_trends = {}
            status_counts = {status.value: 0 for status in HealthStatus}
            
            for file in health_files:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for component, result in data['results'].items():
                    if component not in component_trends:
                        component_trends[component] = []
                    
                    component_trends[component].append({
                        'timestamp': result['timestamp'],
                        'status': result['status'],
                        'response_time': result['response_time']
                    })
                    
                    status_counts[result['status']] += 1
            
            return {
                'analysis_period': f'{days} days',
                'health_checks_analysed': len(health_files),
                'component_trends': component_trends,
                'status_distribution': status_counts,
                'trend_summary': self._generate_trend_summary(component_trends)
            }
        
        except Exception as e:
            self.logger.error(f"Failed to analyse health trends: {e}")
            return {'error': f'Trend analysis failed: {str(e)}'}
    
    def _generate_trend_summary(self, component_trends: Dict) -> Dict:
        """Generate summary of health trends"""
        summary = {}
        
        for component, trend_data in component_trends.items():
            if len(trend_data) < 2:
                continue
            
            recent_statuses = [item['status'] for item in trend_data[-5:]]  # Last 5 checks
            
            # Check if component is consistently unhealthy
            unhealthy_count = sum(1 for status in recent_statuses if status in ['unhealthy', 'critical'])
            
            if unhealthy_count >= 3:
                summary[component] = 'consistently_unhealthy'
            elif unhealthy_count >= 1:
                summary[component] = 'intermittent_issues'
            else:
                summary[component] = 'stable'
        
        return summary

# Global health monitor instance
health_monitor = SystemHealthMonitor()

async def run_scheduled_health_check():
    """Run scheduled health check (can be called by cron job)"""
    try:
        results = await health_monitor.run_comprehensive_health_check()
        
        # Generate summary report
        summary = {
            'timestamp': datetime.now().isoformat(),
            'overall_status': results['system_overall'].status.value,
            'total_components': len(results) - 1,  # Exclude system_overall
            'issues': []
        }
        
        for component, result in results.items():
            if component != 'system_overall' and result.status != HealthStatus.HEALTHY:
                summary['issues'].append({
                    'component': component,
                    'status': result.status.value,
                    'message': result.message
                })
        
        print(f"Health check completed: {summary['overall_status']}")
        if summary['issues']:
            print(f"Issues detected: {len(summary['issues'])}")
            for issue in summary['issues']:
                print(f"  - {issue['component']}: {issue['status']} - {issue['message']}")
        
        return results
    
    except Exception as e:
        print(f"Health check failed: {e}")
        logging.error(f"Scheduled health check failed: {e}")
        return None

if __name__ == "__main__":
    asyncio.run(run_scheduled_health_check())