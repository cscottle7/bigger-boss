"""
Enhanced Error Recovery System with Advanced Fallback Mechanisms
Extends the base error recovery system with sophisticated fallback strategies and graceful degradation
"""

import asyncio
import logging
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable, Union
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
import functools
import traceback
import requests
import aiohttp
from contextlib import asynccontextmanager
import threading
from concurrent.futures import TimeoutError as FuturesTimeoutError

from system.core_tools.error_recovery_system import (
    error_recovery_system, ErrorSeverity, RecoveryStrategy, 
    ErrorRecoverySystem, with_error_recovery
)
from system.orchestration.autonomous_operation_manager import autonomous_manager

class FallbackMode(Enum):
    """Fallback operation modes"""
    DEGRADED_SERVICE = "degraded_service"
    READ_ONLY_MODE = "read_only_mode"
    CACHE_ONLY = "cache_only"
    OFFLINE_MODE = "offline_mode"
    SAFE_MODE = "safe_mode"

class CircuitBreakerState(Enum):
    """Circuit breaker states"""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing fast
    HALF_OPEN = "half_open"  # Testing recovery

@dataclass
class FallbackConfiguration:
    """Configuration for fallback mechanisms"""
    enable_circuit_breaker: bool = True
    circuit_breaker_threshold: int = 5  # failures before opening
    circuit_breaker_timeout: int = 60   # seconds before half-open
    enable_graceful_degradation: bool = True
    enable_offline_cache: bool = True
    enable_alternative_apis: bool = True
    max_fallback_attempts: int = 3
    fallback_timeout: int = 30

class CircuitBreaker:
    """Circuit breaker pattern implementation"""
    
    def __init__(self, name: str, threshold: int = 5, timeout: int = 60):
        self.name = name
        self.threshold = threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitBreakerState.CLOSED
        self.logger = logging.getLogger(f"{__name__}.CircuitBreaker.{name}")
    
    async def call(self, func: Callable, *args, **kwargs):
        """Execute function through circuit breaker"""
        if self.state == CircuitBreakerState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitBreakerState.HALF_OPEN
                self.logger.info(f"Circuit breaker {self.name} entering half-open state")
            else:
                raise Exception(f"Circuit breaker {self.name} is OPEN - failing fast")
        
        try:
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)
            
            # Success - reset if we were half-open
            if self.state == CircuitBreakerState.HALF_OPEN:
                self.state = CircuitBreakerState.CLOSED
                self.failure_count = 0
                self.logger.info(f"Circuit breaker {self.name} reset to CLOSED state")
            
            return result
        
        except Exception as e:
            self._record_failure()
            raise e
    
    def _should_attempt_reset(self) -> bool:
        """Check if we should attempt to reset the circuit breaker"""
        if self.last_failure_time is None:
            return False
        
        time_since_failure = time.time() - self.last_failure_time
        return time_since_failure >= self.timeout
    
    def _record_failure(self):
        """Record a failure and potentially open the circuit"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.threshold and self.state == CircuitBreakerState.CLOSED:
            self.state = CircuitBreakerState.OPEN
            self.logger.warning(f"Circuit breaker {self.name} OPENED after {self.failure_count} failures")

class EnhancedErrorRecoverySystem(ErrorRecoverySystem):
    """Enhanced error recovery system with advanced fallback mechanisms"""
    
    def __init__(self):
        super().__init__()
        self.fallback_config = FallbackConfiguration()
        self.circuit_breakers = {}
        self.fallback_cache = {}
        self.alternative_services = {}
        self.current_fallback_mode = None
        self.degraded_services = set()
        self.setup_enhanced_logging()
        self.setup_alternative_services()
    
    def setup_enhanced_logging(self):
        """Setup enhanced error recovery logging"""
        recovery_log_dir = Path("system/reports/recovery")
        recovery_log_dir.mkdir(parents=True, exist_ok=True)
        
        recovery_handler = logging.FileHandler(
            recovery_log_dir / f"enhanced_recovery_{datetime.now().strftime('%Y%m%d')}.log"
        )
        recovery_handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        recovery_handler.setFormatter(formatter)
        
        self.logger.addHandler(recovery_handler)
    
    def setup_alternative_services(self):
        """Setup alternative service endpoints"""
        self.alternative_services = {
            'web_scraping': [
                'jina_reader',
                'direct_requests',
                'playwright_fallback'
            ],
            'search_api': [
                'serpapi_primary',
                'google_search_fallback',
                'bing_search_fallback'
            ],
            'performance_testing': [
                'gtmetrix_primary',
                'pagespeed_insights',
                'lighthouse_cli'
            ]
        }
    
    def get_circuit_breaker(self, service_name: str) -> CircuitBreaker:
        """Get or create circuit breaker for service"""
        if service_name not in self.circuit_breakers:
            self.circuit_breakers[service_name] = CircuitBreaker(
                service_name,
                threshold=self.fallback_config.circuit_breaker_threshold,
                timeout=self.fallback_config.circuit_breaker_timeout
            )
        return self.circuit_breakers[service_name]
    
    async def execute_with_enhanced_recovery(
        self,
        func: Callable,
        service_name: str,
        *args,
        enable_circuit_breaker: bool = True,
        enable_fallback: bool = True,
        cache_result: bool = False,
        **kwargs
    ) -> tuple[bool, Any]:
        """Execute function with enhanced recovery mechanisms"""
        
        # Check if service is in degraded mode
        if service_name in self.degraded_services:
            self.logger.info(f"Service {service_name} is in degraded mode, attempting fallback")
            return await self._attempt_service_fallback(service_name, func, *args, **kwargs)
        
        # Use circuit breaker if enabled
        if enable_circuit_breaker and self.fallback_config.enable_circuit_breaker:
            circuit_breaker = self.get_circuit_breaker(service_name)
            
            try:
                result = await circuit_breaker.call(func, *args, **kwargs)
                
                # Cache successful result if requested
                if cache_result:
                    self._cache_result(service_name, func.__name__, args, kwargs, result)
                
                return True, result
            
            except Exception as circuit_error:
                self.logger.warning(f"Circuit breaker failed for {service_name}: {circuit_error}")
                
                # Try fallback if enabled
                if enable_fallback:
                    return await self._attempt_service_fallback(service_name, func, *args, **kwargs)
                else:
                    return False, str(circuit_error)
        
        # Standard execution with enhanced error handling
        return await self.handle_error_with_recovery(
            func, *args, 
            context={'service_name': service_name},
            **kwargs
        )
    
    async def _attempt_service_fallback(
        self, 
        service_name: str, 
        primary_func: Callable, 
        *args, 
        **kwargs
    ) -> tuple[bool, Any]:
        """Attempt fallback service options"""
        
        fallback_attempts = 0
        max_attempts = self.fallback_config.max_fallback_attempts
        
        while fallback_attempts < max_attempts:
            try:
                # Try cached result first
                if self.fallback_config.enable_offline_cache:
                    cached_result = self._get_cached_result(service_name, primary_func.__name__, args, kwargs)
                    if cached_result is not None:
                        self.logger.info(f"Using cached result for {service_name}")
                        return True, cached_result
                
                # Try alternative services
                if self.fallback_config.enable_alternative_apis:
                    alternative_result = await self._try_alternative_service(service_name, primary_func, *args, **kwargs)
                    if alternative_result[0]:
                        return alternative_result
                
                # Try degraded service mode
                if self.fallback_config.enable_graceful_degradation:
                    degraded_result = await self._try_degraded_mode(service_name, primary_func, *args, **kwargs)
                    if degraded_result[0]:
                        return degraded_result
                
                fallback_attempts += 1
                await asyncio.sleep(2 ** fallback_attempts)  # Exponential backoff
            
            except Exception as fallback_error:
                self.logger.error(f"Fallback attempt {fallback_attempts + 1} failed for {service_name}: {fallback_error}")
                fallback_attempts += 1
        
        return False, f"All fallback attempts exhausted for {service_name}"
    
    async def _try_alternative_service(
        self, 
        service_type: str, 
        primary_func: Callable, 
        *args, 
        **kwargs
    ) -> tuple[bool, Any]:
        """Try alternative service implementations"""
        
        if service_type not in self.alternative_services:
            return False, "No alternative services configured"
        
        alternatives = self.alternative_services[service_type]
        
        for alternative in alternatives:
            try:
                self.logger.info(f"Trying alternative service: {alternative} for {service_type}")
                
                # Get alternative implementation
                alt_func = self._get_alternative_implementation(alternative, primary_func)
                if alt_func:
                    if asyncio.iscoroutinefunction(alt_func):
                        result = await alt_func(*args, **kwargs)
                    else:
                        result = alt_func(*args, **kwargs)
                    
                    self.logger.info(f"Alternative service {alternative} succeeded")
                    return True, result
            
            except Exception as alt_error:
                self.logger.warning(f"Alternative service {alternative} failed: {alt_error}")
                continue
        
        return False, "All alternative services failed"
    
    def _get_alternative_implementation(self, alternative_name: str, primary_func: Callable) -> Optional[Callable]:
        """Get alternative implementation for a service"""
        
        # Web scraping alternatives
        if alternative_name == 'jina_reader':
            return self._jina_reader_fallback
        elif alternative_name == 'direct_requests':
            return self._direct_requests_fallback
        elif alternative_name == 'playwright_fallback':
            return self._playwright_fallback
        
        # Search API alternatives
        elif alternative_name == 'google_search_fallback':
            return self._google_search_fallback
        elif alternative_name == 'bing_search_fallback':
            return self._bing_search_fallback
        
        # Performance testing alternatives
        elif alternative_name == 'pagespeed_insights':
            return self._pagespeed_insights_fallback
        elif alternative_name == 'lighthouse_cli':
            return self._lighthouse_cli_fallback
        
        return None
    
    async def _try_degraded_mode(
        self, 
        service_name: str, 
        primary_func: Callable, 
        *args, 
        **kwargs
    ) -> tuple[bool, Any]:
        """Try degraded mode operation"""
        
        self.logger.info(f"Attempting degraded mode for {service_name}")
        
        try:
            # Reduce scope or complexity of operation
            degraded_kwargs = kwargs.copy()
            
            # Common degradation strategies
            if 'max_pages' in degraded_kwargs:
                degraded_kwargs['max_pages'] = min(5, degraded_kwargs.get('max_pages', 10) // 2)
            
            if 'timeout' in degraded_kwargs:
                degraded_kwargs['timeout'] = min(30, degraded_kwargs.get('timeout', 60))
            
            if 'detailed_analysis' in degraded_kwargs:
                degraded_kwargs['detailed_analysis'] = False
            
            self.degraded_services.add(service_name)
            
            if asyncio.iscoroutinefunction(primary_func):
                result = await primary_func(*args, **degraded_kwargs)
            else:
                result = primary_func(*args, **degraded_kwargs)
            
            self.logger.info(f"Degraded mode succeeded for {service_name}")
            return True, result
        
        except Exception as degraded_error:
            self.logger.error(f"Degraded mode failed for {service_name}: {degraded_error}")
            return False, str(degraded_error)
    
    # Alternative service implementations
    async def _jina_reader_fallback(self, url: str, **kwargs) -> Dict:
        """Jina Reader fallback for web scraping"""
        try:
            from system.config.api_credentials import credentials
            api_key = credentials.get_credential('jina', 'api_key')
            
            if not api_key:
                raise Exception("Jina API key not available")
            
            async with aiohttp.ClientSession() as session:
                headers = {'Authorization': f'Bearer {api_key}'}
                async with session.get(f'https://r.jina.ai/{url}', headers=headers, timeout=30) as response:
                    if response.status == 200:
                        content = await response.text()
                        return {'content': content, 'source': 'jina_fallback', 'url': url}
                    else:
                        raise Exception(f"Jina API returned status {response.status}")
        
        except Exception as e:
            raise Exception(f"Jina fallback failed: {str(e)}")
    
    async def _direct_requests_fallback(self, url: str, **kwargs) -> Dict:
        """Direct requests fallback for web scraping"""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                async with session.get(url, headers=headers, timeout=30) as response:
                    if response.status == 200:
                        content = await response.text()
                        return {'content': content, 'source': 'direct_requests_fallback', 'url': url}
                    else:
                        raise Exception(f"Direct request returned status {response.status}")
        
        except Exception as e:
            raise Exception(f"Direct requests fallback failed: {str(e)}")
    
    async def _playwright_fallback(self, url: str, **kwargs) -> Dict:
        """Playwright fallback for web scraping"""
        try:
            from playwright.async_api import async_playwright
            
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                
                await page.goto(url, timeout=30000)
                content = await page.content()
                
                await browser.close()
                
                return {'content': content, 'source': 'playwright_fallback', 'url': url}
        
        except Exception as e:
            raise Exception(f"Playwright fallback failed: {str(e)}")
    
    async def _google_search_fallback(self, query: str, **kwargs) -> Dict:
        """Google Search fallback (limited functionality)"""
        try:
            # This would require Google Custom Search API
            # For now, return a placeholder
            return {
                'results': [{'title': f'Fallback result for: {query}', 'source': 'google_fallback'}],
                'source': 'google_search_fallback'
            }
        except Exception as e:
            raise Exception(f"Google search fallback failed: {str(e)}")
    
    async def _bing_search_fallback(self, query: str, **kwargs) -> Dict:
        """Bing Search fallback"""
        try:
            # This would require Bing Search API
            return {
                'results': [{'title': f'Fallback result for: {query}', 'source': 'bing_fallback'}],
                'source': 'bing_search_fallback'
            }
        except Exception as e:
            raise Exception(f"Bing search fallback failed: {str(e)}")
    
    async def _pagespeed_insights_fallback(self, url: str, **kwargs) -> Dict:
        """PageSpeed Insights fallback"""
        try:
            # Use Google PageSpeed Insights API
            api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy=desktop"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url, timeout=60) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'score': data.get('lighthouseResult', {}).get('categories', {}).get('performance', {}).get('score', 0) * 100,
                            'source': 'pagespeed_insights_fallback'
                        }
                    else:
                        raise Exception(f"PageSpeed Insights returned status {response.status}")
        
        except Exception as e:
            raise Exception(f"PageSpeed Insights fallback failed: {str(e)}")
    
    async def _lighthouse_cli_fallback(self, url: str, **kwargs) -> Dict:
        """Lighthouse CLI fallback"""
        try:
            import subprocess
            import json
            
            # Run Lighthouse CLI (if installed)
            result = subprocess.run([
                'lighthouse', url, '--output=json', '--quiet', '--chrome-flags="--headless"'
            ], capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                lighthouse_data = json.loads(result.stdout)
                return {
                    'score': lighthouse_data.get('categories', {}).get('performance', {}).get('score', 0) * 100,
                    'source': 'lighthouse_cli_fallback'
                }
            else:
                raise Exception(f"Lighthouse CLI failed with return code {result.returncode}")
        
        except Exception as e:
            raise Exception(f"Lighthouse CLI fallback failed: {str(e)}")
    
    def _cache_result(self, service_name: str, func_name: str, args: tuple, kwargs: dict, result: Any):
        """Cache result for fallback use"""
        try:
            cache_key = self._generate_cache_key(service_name, func_name, args, kwargs)
            self.fallback_cache[cache_key] = {
                'result': result,
                'timestamp': datetime.now(),
                'service': service_name,
                'function': func_name
            }
            
            # Limit cache size
            if len(self.fallback_cache) > 1000:
                # Remove oldest entries
                sorted_cache = sorted(
                    self.fallback_cache.items(),
                    key=lambda x: x[1]['timestamp']
                )
                for old_key, _ in sorted_cache[:100]:  # Remove oldest 100
                    del self.fallback_cache[old_key]
        
        except Exception as e:
            self.logger.warning(f"Failed to cache result: {e}")
    
    def _get_cached_result(self, service_name: str, func_name: str, args: tuple, kwargs: dict) -> Optional[Any]:
        """Get cached result if available and not expired"""
        try:
            cache_key = self._generate_cache_key(service_name, func_name, args, kwargs)
            
            if cache_key in self.fallback_cache:
                cache_entry = self.fallback_cache[cache_key]
                
                # Check if cache is still valid (24 hours)
                if datetime.now() - cache_entry['timestamp'] < timedelta(hours=24):
                    return cache_entry['result']
                else:
                    # Remove expired entry
                    del self.fallback_cache[cache_key]
            
            return None
        
        except Exception as e:
            self.logger.warning(f"Failed to get cached result: {e}")
            return None
    
    def _generate_cache_key(self, service_name: str, func_name: str, args: tuple, kwargs: dict) -> str:
        """Generate cache key from function parameters"""
        try:
            # Create a hash of the parameters
            import hashlib
            
            cache_data = {
                'service': service_name,
                'function': func_name,
                'args': str(args),
                'kwargs': {k: v for k, v in kwargs.items() if k not in ['timeout', 'headers']}
            }
            
            cache_string = json.dumps(cache_data, sort_keys=True)
            return hashlib.md5(cache_string.encode()).hexdigest()
        
        except Exception as e:
            # Fallback to simple string concatenation
            return f"{service_name}_{func_name}_{hash(str(args) + str(kwargs))}"
    
    def enter_fallback_mode(self, mode: FallbackMode, reason: str = ""):
        """Enter system-wide fallback mode"""
        self.current_fallback_mode = mode
        self.logger.warning(f"Entering fallback mode: {mode.value} - {reason}")
        
        autonomous_manager.log_operation(
            'error_recovery',
            'fallback_mode_activated',
            {'mode': mode.value, 'reason': reason}
        )
    
    def exit_fallback_mode(self):
        """Exit fallback mode and return to normal operation"""
        if self.current_fallback_mode:
            old_mode = self.current_fallback_mode
            self.current_fallback_mode = None
            self.degraded_services.clear()
            
            self.logger.info(f"Exiting fallback mode: {old_mode.value}")
            
            autonomous_manager.log_operation(
                'error_recovery',
                'fallback_mode_deactivated',
                {'previous_mode': old_mode.value}
            )
    
    def get_recovery_status(self) -> Dict[str, Any]:
        """Get comprehensive recovery system status"""
        circuit_breaker_status = {}
        for name, breaker in self.circuit_breakers.items():
            circuit_breaker_status[name] = {
                'state': breaker.state.value,
                'failure_count': breaker.failure_count,
                'last_failure_time': breaker.last_failure_time
            }
        
        return {
            'current_fallback_mode': self.current_fallback_mode.value if self.current_fallback_mode else None,
            'degraded_services': list(self.degraded_services),
            'circuit_breakers': circuit_breaker_status,
            'cached_results': len(self.fallback_cache),
            'alternative_services': self.alternative_services,
            'fallback_config': {
                'circuit_breaker_enabled': self.fallback_config.enable_circuit_breaker,
                'graceful_degradation_enabled': self.fallback_config.enable_graceful_degradation,
                'offline_cache_enabled': self.fallback_config.enable_offline_cache
            }
        }

# Enhanced decorator for automatic recovery with circuit breaker
def with_enhanced_recovery(
    service_name: str,
    enable_circuit_breaker: bool = True,
    enable_fallback: bool = True,
    cache_result: bool = False
):
    """Decorator for enhanced error recovery with circuit breaker and fallback"""
    def decorator(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            success, result = await enhanced_recovery_system.execute_with_enhanced_recovery(
                func, service_name, *args,
                enable_circuit_breaker=enable_circuit_breaker,
                enable_fallback=enable_fallback,
                cache_result=cache_result,
                **kwargs
            )
            if not success:
                raise Exception(f"Enhanced recovery failed: {result}")
            return result
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(async_wrapper(*args, **kwargs))
            finally:
                loop.close()
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator

# Global enhanced recovery system instance
enhanced_recovery_system = EnhancedErrorRecoverySystem()

# Context manager for graceful degradation
@asynccontextmanager
async def graceful_degradation(service_name: str, fallback_mode: FallbackMode = FallbackMode.DEGRADED_SERVICE):
    """Context manager for graceful degradation"""
    try:
        yield enhanced_recovery_system
    except Exception as e:
        enhanced_recovery_system.logger.warning(f"Entering graceful degradation for {service_name}: {e}")
        enhanced_recovery_system.enter_fallback_mode(fallback_mode, str(e))
        
        # Try to continue with degraded functionality
        try:
            yield enhanced_recovery_system
        finally:
            enhanced_recovery_system.exit_fallback_mode()
    finally:
        if enhanced_recovery_system.current_fallback_mode:
            enhanced_recovery_system.exit_fallback_mode()

if __name__ == "__main__":
    # Test the enhanced recovery system
    async def test_recovery_system():
        print("Testing Enhanced Error Recovery System...")
        
        # Test circuit breaker
        @with_enhanced_recovery('test_service', cache_result=True)
        async def test_function(should_fail: bool = False):
            if should_fail:
                raise Exception("Test failure")
            return "Success!"
        
        # Test normal operation
        try:
            result = await test_function(False)
            print(f"Normal operation: {result}")
        except Exception as e:
            print(f"Error: {e}")
        
        # Test failure and recovery
        for i in range(3):
            try:
                result = await test_function(True)
                print(f"Unexpected success: {result}")
            except Exception as e:
                print(f"Expected failure {i+1}: {e}")
        
        # Check recovery status
        status = enhanced_recovery_system.get_recovery_status()
        print(f"Recovery Status: {json.dumps(status, indent=2, default=str)}")
    
    asyncio.run(test_recovery_system())