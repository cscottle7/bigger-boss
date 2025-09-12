"""
Intelligent Error Handling and Recovery System
Provides autonomous error detection, logging, and recovery mechanisms
"""

import asyncio
import logging
import traceback
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from pathlib import Path
from enum import Enum
import functools
import time

from system.orchestration.autonomous_operation_manager import autonomous_manager

class ErrorSeverity(Enum):
    """Error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class RecoveryStrategy(Enum):
    """Recovery strategy types"""
    RETRY = "retry"
    FALLBACK = "fallback"
    SKIP = "skip"
    ABORT = "abort"

class ErrorRecoverySystem:
    """Intelligent error handling and recovery system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.error_history = []
        self.recovery_stats = {
            'total_errors': 0,
            'successful_recoveries': 0,
            'failed_recoveries': 0,
            'recovery_rate': 0.0
        }
        self.setup_error_logging()
    
    def setup_error_logging(self):
        """Setup comprehensive error logging"""
        error_log_dir = Path("system/reports/errors")
        error_log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create error handler
        error_handler = logging.FileHandler(
            error_log_dir / f"error_recovery_{datetime.now().strftime('%Y%m%d')}.log"
        )
        error_handler.setLevel(logging.ERROR)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        error_handler.setFormatter(formatter)
        
        # Add handler to root logger
        logging.getLogger().addHandler(error_handler)
    
    def classify_error(self, error: Exception, context: Dict = None) -> tuple[ErrorSeverity, RecoveryStrategy]:
        """Classify error and determine recovery strategy"""
        error_type = type(error).__name__
        error_msg = str(error).lower()
        
        # Network/Connection Errors - Usually retry-able
        if any(keyword in error_type.lower() for keyword in ['timeout', 'connection', 'network', 'http']):
            return ErrorSeverity.MEDIUM, RecoveryStrategy.RETRY
        
        # Permission/Authentication Errors - Usually not retry-able
        if any(keyword in error_msg for keyword in ['permission', 'unauthorized', 'forbidden', 'access denied']):
            if 'autonomous operation' in error_msg:
                return ErrorSeverity.HIGH, RecoveryStrategy.ABORT
            return ErrorSeverity.MEDIUM, RecoveryStrategy.SKIP
        
        # API Rate Limiting - Wait and retry
        if any(keyword in error_msg for keyword in ['rate limit', 'quota exceeded', 'too many requests']):
            return ErrorSeverity.LOW, RecoveryStrategy.RETRY
        
        # File System Errors - Usually recoverable
        if any(keyword in error_type.lower() for keyword in ['file', 'directory', 'path']):
            return ErrorSeverity.MEDIUM, RecoveryStrategy.FALLBACK
        
        # Memory/Resource Errors - Try to recover
        if any(keyword in error_type.lower() for keyword in ['memory', 'resource', 'disk']):
            return ErrorSeverity.HIGH, RecoveryStrategy.FALLBACK
        
        # Import/Module Errors - Usually critical
        if any(keyword in error_type.lower() for keyword in ['import', 'module', 'attribute']):
            return ErrorSeverity.CRITICAL, RecoveryStrategy.ABORT
        
        # Generic errors
        return ErrorSeverity.MEDIUM, RecoveryStrategy.RETRY
    
    async def handle_error_with_recovery(
        self, 
        func: Callable,
        *args, 
        max_retries: int = 3,
        backoff_factor: float = 2.0,
        context: Dict = None,
        **kwargs
    ) -> tuple[bool, Any]:
        """
        Execute function with intelligent error handling and recovery
        Returns (success, result)
        """
        last_error = None
        retry_count = 0
        
        for attempt in range(max_retries + 1):
            try:
                # Execute the function
                if asyncio.iscoroutinefunction(func):
                    result = await func(*args, **kwargs)
                else:
                    result = func(*args, **kwargs)
                
                # Success - update stats and return
                if retry_count > 0:
                    self.recovery_stats['successful_recoveries'] += 1
                    self._update_recovery_rate()
                
                return True, result
                
            except Exception as error:
                last_error = error
                retry_count = attempt
                
                # Log the error
                self.logger.error(
                    f"Error in {func.__name__} (attempt {attempt + 1}): {error}",
                    extra={
                        'function': func.__name__,
                        'attempt': attempt + 1,
                        'context': context or {},
                        'traceback': traceback.format_exc()
                    }
                )
                
                # Classify error and determine strategy
                severity, strategy = self.classify_error(error, context)
                
                # Record error
                self._record_error(error, func.__name__, severity, strategy, context)
                
                # Handle based on strategy
                if strategy == RecoveryStrategy.ABORT:
                    self.recovery_stats['failed_recoveries'] += 1
                    self._update_recovery_rate()
                    return False, f"Aborted due to {severity.value} error: {error}"
                
                elif strategy == RecoveryStrategy.SKIP:
                    self.logger.warning(f"Skipping {func.__name__} due to error: {error}")
                    return False, f"Skipped due to error: {error}"
                
                elif strategy == RecoveryStrategy.RETRY:
                    if attempt < max_retries:
                        wait_time = backoff_factor ** attempt
                        self.logger.info(f"Retrying {func.__name__} in {wait_time} seconds...")
                        await asyncio.sleep(wait_time)
                        continue
                
                elif strategy == RecoveryStrategy.FALLBACK:
                    # Try fallback approach if available
                    fallback_result = await self._try_fallback(func, error, *args, **kwargs)
                    if fallback_result[0]:
                        return fallback_result
                    
                    # If fallback failed, continue with retry logic
                    if attempt < max_retries:
                        wait_time = backoff_factor ** attempt
                        await asyncio.sleep(wait_time)
                        continue
        
        # All retries exhausted
        self.recovery_stats['failed_recoveries'] += 1
        self._update_recovery_rate()
        return False, f"Failed after {max_retries + 1} attempts: {last_error}"
    
    async def _try_fallback(self, func: Callable, error: Exception, *args, **kwargs) -> tuple[bool, Any]:
        """Attempt fallback recovery strategies"""
        func_name = func.__name__
        
        # Fallback strategies based on function type
        if 'crawl' in func_name.lower():
            return await self._crawl_fallback(func, error, *args, **kwargs)
        elif 'api' in func_name.lower():
            return await self._api_fallback(func, error, *args, **kwargs)
        elif 'file' in func_name.lower():
            return await self._file_fallback(func, error, *args, **kwargs)
        
        return False, "No fallback strategy available"
    
    async def _crawl_fallback(self, func: Callable, error: Exception, *args, **kwargs) -> tuple[bool, Any]:
        """Fallback strategies for crawling operations"""
        try:
            # Reduce page limit if it's a timeout/memory issue
            if 'max_pages' in kwargs:
                original_pages = kwargs['max_pages']
                kwargs['max_pages'] = min(25, original_pages // 2)
                self.logger.info(f"Fallback: Reduced page limit from {original_pages} to {kwargs['max_pages']}")
                
                if asyncio.iscoroutinefunction(func):
                    result = await func(*args, **kwargs)
                else:
                    result = func(*args, **kwargs)
                
                return True, result
        
        except Exception as fallback_error:
            self.logger.error(f"Crawl fallback failed: {fallback_error}")
        
        return False, "Crawl fallback failed"
    
    async def _api_fallback(self, func: Callable, error: Exception, *args, **kwargs) -> tuple[bool, Any]:
        """Fallback strategies for API operations"""
        try:
            # For rate limiting, wait longer
            if 'rate limit' in str(error).lower():
                self.logger.info("API fallback: Extended wait for rate limiting")
                await asyncio.sleep(60)  # Wait 1 minute
                
                if asyncio.iscoroutinefunction(func):
                    result = await func(*args, **kwargs)
                else:
                    result = func(*args, **kwargs)
                
                return True, result
        
        except Exception as fallback_error:
            self.logger.error(f"API fallback failed: {fallback_error}")
        
        return False, "API fallback failed"
    
    async def _file_fallback(self, func: Callable, error: Exception, *args, **kwargs) -> tuple[bool, Any]:
        """Fallback strategies for file operations"""
        try:
            # Create directories if they don't exist
            if 'file_path' in kwargs:
                file_path = Path(kwargs['file_path'])
                file_path.parent.mkdir(parents=True, exist_ok=True)
                self.logger.info(f"File fallback: Created directory structure for {file_path}")
                
                if asyncio.iscoroutinefunction(func):
                    result = await func(*args, **kwargs)
                else:
                    result = func(*args, **kwargs)
                
                return True, result
        
        except Exception as fallback_error:
            self.logger.error(f"File fallback failed: {fallback_error}")
        
        return False, "File fallback failed"
    
    def _record_error(self, error: Exception, function: str, severity: ErrorSeverity, strategy: RecoveryStrategy, context: Dict = None):
        """Record error for analysis and reporting"""
        error_record = {
            'timestamp': datetime.now().isoformat(),
            'error_type': type(error).__name__,
            'error_message': str(error),
            'function': function,
            'severity': severity.value,
            'recovery_strategy': strategy.value,
            'context': context or {},
            'traceback': traceback.format_exc()
        }
        
        self.error_history.append(error_record)
        self.recovery_stats['total_errors'] += 1
        
        # Log to autonomous manager
        autonomous_manager.log_operation(
            'error_handling',
            'error_recorded',
            error_record
        )
    
    def _update_recovery_rate(self):
        """Update recovery success rate"""
        total_recovery_attempts = self.recovery_stats['successful_recoveries'] + self.recovery_stats['failed_recoveries']
        if total_recovery_attempts > 0:
            self.recovery_stats['recovery_rate'] = (
                self.recovery_stats['successful_recoveries'] / total_recovery_attempts
            ) * 100
    
    def get_error_summary(self) -> Dict:
        """Get summary of errors and recovery performance"""
        recent_errors = [
            error for error in self.error_history
            if datetime.fromisoformat(error['timestamp']) > datetime.now() - timedelta(hours=24)
        ]
        
        error_types = {}
        severity_counts = {}
        
        for error in recent_errors:
            error_type = error['error_type']
            severity = error['severity']
            
            error_types[error_type] = error_types.get(error_type, 0) + 1
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        return {
            'recovery_stats': self.recovery_stats,
            'recent_errors_24h': len(recent_errors),
            'error_types': error_types,
            'severity_distribution': severity_counts,
            'most_common_errors': sorted(error_types.items(), key=lambda x: x[1], reverse=True)[:5]
        }
    
    def save_error_report(self, client_domain: str = None):
        """Save comprehensive error report"""
        try:
            report_dir = Path("system/reports/errors")
            if client_domain:
                report_dir = Path(f"clients/{client_domain}/technical")
            
            report_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_file = report_dir / f"error_recovery_report_{timestamp}.json"
            
            report_data = {
                'report_metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'client_domain': client_domain,
                    'total_errors_recorded': len(self.error_history)
                },
                'error_summary': self.get_error_summary(),
                'recent_errors': self.error_history[-50:],  # Last 50 errors
                'recovery_recommendations': self._generate_recovery_recommendations()
            }
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Error recovery report saved: {report_file}")
            return str(report_file)
            
        except Exception as e:
            self.logger.error(f"Failed to save error report: {e}")
            return None
    
    def _generate_recovery_recommendations(self) -> List[Dict]:
        """Generate recommendations based on error patterns"""
        recommendations = []
        error_summary = self.get_error_summary()
        
        # Check recovery rate
        recovery_rate = error_summary['recovery_stats']['recovery_rate']
        if recovery_rate < 80:
            recommendations.append({
                'priority': 'high',
                'category': 'recovery_performance',
                'issue': f'Low recovery rate: {recovery_rate:.1f}%',
                'recommendation': 'Review and improve error handling strategies for frequently failing operations'
            })
        
        # Check for frequent error types
        for error_type, count in error_summary['most_common_errors']:
            if count > 5:  # More than 5 occurrences
                recommendations.append({
                    'priority': 'medium',
                    'category': 'error_prevention',
                    'issue': f'Frequent {error_type} errors ({count} occurrences)',
                    'recommendation': f'Implement specific prevention measures for {error_type} errors'
                })
        
        # Check for critical errors
        critical_count = error_summary['severity_distribution'].get('critical', 0)
        if critical_count > 0:
            recommendations.append({
                'priority': 'critical',
                'category': 'system_stability',
                'issue': f'{critical_count} critical errors detected',
                'recommendation': 'Immediate investigation required for critical system errors'
            })
        
        return recommendations

# Decorator for automatic error handling
def with_error_recovery(max_retries: int = 3, backoff_factor: float = 2.0):
    """Decorator to add error recovery to functions"""
    def decorator(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            success, result = await error_recovery_system.handle_error_with_recovery(
                func, *args, max_retries=max_retries, backoff_factor=backoff_factor, **kwargs
            )
            if not success:
                raise Exception(f"Function failed after recovery attempts: {result}")
            return result
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            # For sync functions, we need to handle them differently
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(async_wrapper(*args, **kwargs))
            finally:
                loop.close()
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator

# Global error recovery system instance
error_recovery_system = ErrorRecoverySystem()