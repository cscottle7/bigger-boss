"""
Autonomous Operation Manager
Coordinates autonomous analysis operations without requiring user permission for routine tasks
"""

import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json

from system.config.autonomous_config import autonomous_config
from system.config.api_credentials import credentials

class SessionTracker:
    """Tracks operations within a session to enforce safety limits"""
    
    def __init__(self):
        self.session_start = datetime.now()
        self.counters = {
            'concurrent_crawls': 0,
            'file_writes': 0,
            'api_calls': 0,
            'analysis_runs': 0
        }
        self.api_usage = {}
        
    def increment(self, counter: str, amount: int = 1) -> bool:
        """Increment counter and check if within limits"""
        if not autonomous_config.is_within_safety_limits(
            f'max_{counter}_per_session', 
            self.counters.get(counter, 0) + amount
        ):
            return False
        
        self.counters[counter] = self.counters.get(counter, 0) + amount
        return True
    
    def track_api_usage(self, service: str) -> bool:
        """Track API usage and check rate limits"""
        now = datetime.now()
        hour_ago = now - timedelta(hours=1)
        
        if service not in self.api_usage:
            self.api_usage[service] = []
        
        # Clean old entries
        self.api_usage[service] = [
            timestamp for timestamp in self.api_usage[service] 
            if timestamp > hour_ago
        ]
        
        # Check rate limits
        rate_limit = autonomous_config.get_rate_limit(service)
        calls_per_hour = rate_limit.get('calls_per_hour', 100)
        
        if len(self.api_usage[service]) >= calls_per_hour:
            return False
        
        # Add current call
        self.api_usage[service].append(now)
        return True

class AutonomousOperationManager:
    """Manages autonomous operations with safety boundaries"""
    
    def __init__(self):
        self.session_tracker = SessionTracker()
        self.logger = self._setup_logging()
        
    def _setup_logging(self) -> logging.Logger:
        """Set up logging for autonomous operations"""
        logger = logging.getLogger('autonomous_ops')
        logger.setLevel(logging.INFO)
        
        # Create handler if not exists
        if not logger.handlers:
            handler = logging.FileHandler(
                Path(__file__).parent.parent / 'reports' / 'autonomous_operations.log'
            )
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def can_perform_operation(self, operation_type: str, **kwargs) -> tuple[bool, str]:
        """Check if operation can be performed autonomously"""
        
        # Check if operation is autonomous
        if not autonomous_config.is_operation_autonomous(operation_type):
            return False, f"Operation {operation_type} requires user permission"
        
        # Check specific operation types
        if operation_type == 'web_crawling':
            return self._check_crawling_limits(**kwargs)
        elif operation_type == 'file_operations':
            return self._check_file_operations(**kwargs)
        elif operation_type == 'api_calls':
            return self._check_api_limits(**kwargs)
        elif operation_type == 'analysis_tools':
            return self._check_analysis_limits(**kwargs)
        
        return True, "Operation approved"
    
    def _check_crawling_limits(self, **kwargs) -> tuple[bool, str]:
        """Check web crawling limits"""
        current_crawls = self.session_tracker.counters.get('concurrent_crawls', 0)
        max_concurrent = autonomous_config.safety_limits['max_concurrent_crawls']
        
        if current_crawls >= max_concurrent:
            return False, f"Maximum concurrent crawls ({max_concurrent}) reached"
        
        return True, "Crawling approved"
    
    def _check_file_operations(self, path: str = None, **kwargs) -> tuple[bool, str]:
        """Check file operation limits"""
        if path and not autonomous_config.is_path_allowed(path):
            return False, f"File operations not allowed on path: {path}"
        
        if not self.session_tracker.increment('file_writes', 0):  # Check without incrementing
            return False, "Maximum file writes per session exceeded"
        
        return True, "File operations approved"
    
    def _check_api_limits(self, service: str = None, **kwargs) -> tuple[bool, str]:
        """Check API call limits"""
        if service and not self.session_tracker.track_api_usage(service):
            rate_limit = autonomous_config.get_rate_limit(service)
            return False, f"Rate limit exceeded for {service} ({rate_limit.get('calls_per_hour', 'unknown')} calls/hour)"
        
        return True, "API calls approved"
    
    def _check_analysis_limits(self, **kwargs) -> tuple[bool, str]:
        """Check analysis operation limits"""
        duration_minutes = autonomous_config.safety_limits['max_analysis_duration_minutes']
        session_duration = (datetime.now() - self.session_tracker.session_start).total_seconds() / 60
        
        if session_duration > duration_minutes:
            return False, f"Maximum analysis session duration ({duration_minutes} min) exceeded"
        
        return True, "Analysis approved"
    
    def log_operation(self, operation_type: str, status: str, details: Dict = None):
        """Log autonomous operation"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'operation_type': operation_type,
            'status': status,
            'details': details or {}
        }
        
        self.logger.info(json.dumps(log_entry))
    
    def get_session_status(self) -> Dict:
        """Get current session status"""
        return {
            'session_start': self.session_tracker.session_start.isoformat(),
            'counters': self.session_tracker.counters,
            'api_usage': {
                service: len(calls) 
                for service, calls in self.session_tracker.api_usage.items()
            },
            'available_services': credentials.get_available_services(),
            'autonomous_operations': list(autonomous_config.autonomous_operations.keys())
        }

# Global instance for autonomous operation management
autonomous_manager = AutonomousOperationManager()