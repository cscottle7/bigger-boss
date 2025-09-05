"""
Autonomous Operation Configuration
Defines what operations can run without user permission
"""

from typing import Dict, List, Set
import re

class AutonomousOperationConfig:
    """Configuration for autonomous operations"""
    
    def __init__(self):
        # Operations that can run autonomously
        self.autonomous_operations = {
            'web_crawling': {
                'enabled': True,
                'max_pages_per_domain': 100,
                'concurrent_requests': 10,
                'respect_robots_txt': True,
                'timeout_seconds': 30
            },
            'file_operations': {
                'enabled': True,
                'allowed_paths': [
                    r'C:\\Apps\\Agents\\Bigger Boss\\bigger-boss\\clients.*',
                    r'C:\\Apps\\Agents\\Bigger Boss\\bigger-boss\\temp_cleanup.*',
                    r'C:\\Apps\\Agents\\Bigger Boss\\bigger-boss\\system\\reports.*',
                    r'clients.*',  # Relative paths
                    r'temp_cleanup.*',
                    r'system\\reports.*'
                ],
                'max_file_size_mb': 50
            },
            'api_calls': {
                'enabled': True,
                'rate_limits': {
                    'gtmetrix': {'calls_per_hour': 10, 'max_spend': 0},
                    'serpapi': {'calls_per_hour': 100, 'max_spend': 5.00},
                    'google': {'calls_per_hour': 1000, 'max_spend': 0}
                }
            },
            'analysis_tools': {
                'enabled': True,
                'max_execution_time': 900,  # 15 minutes
                'memory_limit_mb': 1024
            }
        }
        
        # Operations that require user permission
        self.permission_required_operations = {
            'software_installation',
            'system_configuration_changes',
            'new_api_service_registration',
            'file_operations_outside_project',
            'network_configuration',
            'scheduled_tasks'
        }
        
        # Safety limits
        self.safety_limits = {
            'max_concurrent_crawls': 3,
            'max_analysis_duration_minutes': 30,
            'max_file_writes_per_session': 100,
            'max_api_calls_per_session': 500
        }
    
    def is_operation_autonomous(self, operation: str) -> bool:
        """Check if an operation can run autonomously"""
        return operation in self.autonomous_operations and \
               self.autonomous_operations[operation].get('enabled', False)
    
    def requires_permission(self, operation: str) -> bool:
        """Check if an operation requires user permission"""
        return operation in self.permission_required_operations
    
    def is_path_allowed(self, path: str) -> bool:
        """Check if file operations are allowed on this path"""
        if not self.is_operation_autonomous('file_operations'):
            return False
        
        allowed_paths = self.autonomous_operations['file_operations']['allowed_paths']
        return any(re.match(pattern, path) for pattern in allowed_paths)
    
    def get_rate_limit(self, service: str) -> Dict:
        """Get rate limits for a service"""
        return self.autonomous_operations.get('api_calls', {}).get(
            'rate_limits', {}
        ).get(service, {})
    
    def is_within_safety_limits(self, metric: str, current_value: int) -> bool:
        """Check if current value is within safety limits"""
        limit = self.safety_limits.get(metric)
        return limit is None or current_value < limit

# Global configuration instance
autonomous_config = AutonomousOperationConfig()