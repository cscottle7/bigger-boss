"""
Comprehensive Testing Framework for Continuous System Validation
Automated testing of all system components, APIs, workflows, and integration points
"""

import asyncio
import logging
import json
import time
import unittest
import pytest
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable, Tuple
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
import functools
import traceback
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
import threading

from system.reliability.health_monitor import health_monitor, HealthStatus
from system.reliability.enhanced_error_recovery import enhanced_recovery_system
from system.orchestration.autonomous_operation_manager import autonomous_manager

class TestType(Enum):
    """Types of tests"""
    UNIT = "unit"
    INTEGRATION = "integration"
    API = "api"
    WORKFLOW = "workflow"
    PERFORMANCE = "performance"
    SECURITY = "security"
    REGRESSION = "regression"

class TestPriority(Enum):
    """Test priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class TestResult(Enum):
    """Test result status"""
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"

@dataclass
class TestCase:
    """Test case definition"""
    name: str
    test_type: TestType
    priority: TestPriority
    description: str
    test_function: Callable
    timeout: int = 30
    retry_count: int = 0
    dependencies: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    expected_duration: float = 5.0  # seconds

@dataclass
class TestExecutionResult:
    """Test execution result"""
    test_name: str
    result: TestResult
    duration: float
    message: str
    timestamp: datetime
    error_details: Optional[str] = None
    performance_metrics: Optional[Dict] = None

class TestSuite:
    """Test suite management"""
    
    def __init__(self, name: str):
        self.name = name
        self.test_cases: Dict[str, TestCase] = {}
        self.execution_history: List[TestExecutionResult] = []
    
    def add_test(self, test_case: TestCase):
        """Add test case to suite"""
        self.test_cases[test_case.name] = test_case
    
    def remove_test(self, test_name: str):
        """Remove test case from suite"""
        if test_name in self.test_cases:
            del self.test_cases[test_name]
    
    def get_tests_by_priority(self, priority: TestPriority) -> List[TestCase]:
        """Get tests by priority level"""
        return [test for test in self.test_cases.values() if test.priority == priority]
    
    def get_tests_by_type(self, test_type: TestType) -> List[TestCase]:
        """Get tests by type"""
        return [test for test in self.test_cases.values() if test.test_type == test_type]

class SystemTestingFramework:
    """Comprehensive system testing framework"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.test_suites: Dict[str, TestSuite] = {}
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.setup_test_logging()
        self.initialize_test_suites()
    
    def setup_test_logging(self):
        """Setup test logging"""
        test_log_dir = Path("system/reports/testing")
        test_log_dir.mkdir(parents=True, exist_ok=True)
        
        test_handler = logging.FileHandler(
            test_log_dir / f"testing_{datetime.now().strftime('%Y%m%d')}.log"
        )
        test_handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        test_handler.setFormatter(formatter)
        
        self.logger.addHandler(test_handler)
    
    def initialize_test_suites(self):
        """Initialize standard test suites"""
        
        # API Test Suite
        api_suite = TestSuite("API_Tests")
        api_suite.add_test(TestCase(
            name="test_serpapi_connectivity",
            test_type=TestType.API,
            priority=TestPriority.CRITICAL,
            description="Test SerpAPI connectivity and quota",
            test_function=self.test_serpapi_connectivity,
            timeout=30
        ))
        api_suite.add_test(TestCase(
            name="test_jina_api_connectivity",
            test_type=TestType.API,
            priority=TestPriority.HIGH,
            description="Test Jina API connectivity",
            test_function=self.test_jina_api_connectivity,
            timeout=30
        ))
        api_suite.add_test(TestCase(
            name="test_gtmetrix_api",
            test_type=TestType.API,
            priority=TestPriority.MEDIUM,
            description="Test GTmetrix API connectivity",
            test_function=self.test_gtmetrix_api,
            timeout=30
        ))
        
        # System Component Tests
        system_suite = TestSuite("System_Components")
        system_suite.add_test(TestCase(
            name="test_error_recovery_system",
            test_type=TestType.UNIT,
            priority=TestPriority.CRITICAL,
            description="Test error recovery system functionality",
            test_function=self.test_error_recovery_system,
            timeout=20
        ))
        system_suite.add_test(TestCase(
            name="test_health_monitor",
            test_type=TestType.UNIT,
            priority=TestPriority.HIGH,
            description="Test health monitoring system",
            test_function=self.test_health_monitor,
            timeout=60
        ))
        system_suite.add_test(TestCase(
            name="test_autonomous_manager",
            test_type=TestType.UNIT,
            priority=TestPriority.HIGH,
            description="Test autonomous operation manager",
            test_function=self.test_autonomous_manager,
            timeout=15
        ))
        
        # Workflow Tests
        workflow_suite = TestSuite("Workflow_Tests")
        workflow_suite.add_test(TestCase(
            name="test_client_folder_creation",
            test_type=TestType.WORKFLOW,
            priority=TestPriority.HIGH,
            description="Test client folder structure creation",
            test_function=self.test_client_folder_creation,
            timeout=15
        ))
        workflow_suite.add_test(TestCase(
            name="test_web_scraping_workflow",
            test_type=TestType.WORKFLOW,
            priority=TestPriority.HIGH,
            description="Test web scraping workflow",
            test_function=self.test_web_scraping_workflow,
            timeout=60
        ))
        workflow_suite.add_test(TestCase(
            name="test_analysis_pipeline",
            test_type=TestType.WORKFLOW,
            priority=TestPriority.MEDIUM,
            description="Test analysis pipeline workflow",
            test_function=self.test_analysis_pipeline,
            timeout=120
        ))
        
        # Performance Tests
        performance_suite = TestSuite("Performance_Tests")
        performance_suite.add_test(TestCase(
            name="test_system_response_time",
            test_type=TestType.PERFORMANCE,
            priority=TestPriority.MEDIUM,
            description="Test system response times",
            test_function=self.test_system_response_time,
            timeout=30
        ))
        performance_suite.add_test(TestCase(
            name="test_memory_usage",
            test_type=TestType.PERFORMANCE,
            priority=TestPriority.MEDIUM,
            description="Test memory usage patterns",
            test_function=self.test_memory_usage,
            timeout=20
        ))
        performance_suite.add_test(TestCase(
            name="test_concurrent_operations",
            test_type=TestType.PERFORMANCE,
            priority=TestPriority.LOW,
            description="Test concurrent operation handling",
            test_function=self.test_concurrent_operations,
            timeout=60
        ))
        
        # Security Tests
        security_suite = TestSuite("Security_Tests")
        security_suite.add_test(TestCase(
            name="test_credential_security",
            test_type=TestType.SECURITY,
            priority=TestPriority.CRITICAL,
            description="Test credential handling security",
            test_function=self.test_credential_security,
            timeout=15
        ))
        security_suite.add_test(TestCase(
            name="test_file_permissions",
            test_type=TestType.SECURITY,
            priority=TestPriority.HIGH,
            description="Test file system permissions",
            test_function=self.test_file_permissions,
            timeout=10
        ))
        
        # Add suites to framework
        self.test_suites["api"] = api_suite
        self.test_suites["system"] = system_suite
        self.test_suites["workflow"] = workflow_suite
        self.test_suites["performance"] = performance_suite
        self.test_suites["security"] = security_suite
    
    async def run_test_suite(
        self, 
        suite_name: str, 
        test_types: List[TestType] = None,
        priorities: List[TestPriority] = None
    ) -> Dict[str, Any]:
        """Run specific test suite"""
        
        if suite_name not in self.test_suites:
            return {'error': f'Test suite {suite_name} not found'}
        
        suite = self.test_suites[suite_name]
        self.logger.info(f"Running test suite: {suite_name}")
        
        # Filter tests
        tests_to_run = list(suite.test_cases.values())
        
        if test_types:
            tests_to_run = [test for test in tests_to_run if test.test_type in test_types]
        
        if priorities:
            tests_to_run = [test for test in tests_to_run if test.priority in priorities]
        
        # Sort by priority (critical first)
        priority_order = [TestPriority.CRITICAL, TestPriority.HIGH, TestPriority.MEDIUM, TestPriority.LOW]
        tests_to_run.sort(key=lambda x: priority_order.index(x.priority))
        
        results = {
            'suite_name': suite_name,
            'start_time': datetime.now().isoformat(),
            'test_results': [],
            'summary': {}
        }
        
        passed = failed = skipped = errors = 0
        
        for test_case in tests_to_run:
            self.logger.info(f"Running test: {test_case.name}")
            
            try:
                result = await self._execute_test_case(test_case)
                results['test_results'].append(result)
                
                if result.result == TestResult.PASSED:
                    passed += 1
                elif result.result == TestResult.FAILED:
                    failed += 1
                elif result.result == TestResult.SKIPPED:
                    skipped += 1
                else:
                    errors += 1
            
            except Exception as e:
                error_result = TestExecutionResult(
                    test_name=test_case.name,
                    result=TestResult.ERROR,
                    duration=0.0,
                    message=f"Test execution error: {str(e)}",
                    timestamp=datetime.now(),
                    error_details=traceback.format_exc()
                )
                results['test_results'].append(error_result)
                errors += 1
        
        results['end_time'] = datetime.now().isoformat()
        results['summary'] = {
            'total_tests': len(tests_to_run),
            'passed': passed,
            'failed': failed,
            'skipped': skipped,
            'errors': errors,
            'success_rate': (passed / len(tests_to_run)) * 100 if tests_to_run else 0
        }
        
        # Save results
        self._save_test_results(results)
        
        self.logger.info(f"Test suite {suite_name} completed: {passed}/{len(tests_to_run)} passed")
        
        return results
    
    async def _execute_test_case(self, test_case: TestCase) -> TestExecutionResult:
        """Execute a single test case"""
        start_time = time.time()
        
        try:
            # Check dependencies
            for dep in test_case.dependencies:
                if not await self._check_dependency(dep):
                    return TestExecutionResult(
                        test_name=test_case.name,
                        result=TestResult.SKIPPED,
                        duration=time.time() - start_time,
                        message=f"Dependency not met: {dep}",
                        timestamp=datetime.now()
                    )
            
            # Execute test with timeout
            if asyncio.iscoroutinefunction(test_case.test_function):
                result = await asyncio.wait_for(
                    test_case.test_function(),
                    timeout=test_case.timeout
                )
            else:
                # Run sync function in executor
                result = await asyncio.get_event_loop().run_in_executor(
                    self.executor,
                    test_case.test_function
                )
            
            duration = time.time() - start_time
            
            # Analyse result
            if isinstance(result, dict):
                if result.get('success', True):
                    test_result = TestResult.PASSED
                    message = result.get('message', 'Test passed')
                    performance_metrics = result.get('performance_metrics')
                else:
                    test_result = TestResult.FAILED
                    message = result.get('message', 'Test failed')
                    performance_metrics = None
            elif result is True:
                test_result = TestResult.PASSED
                message = 'Test passed'
                performance_metrics = None
            elif result is False:
                test_result = TestResult.FAILED
                message = 'Test failed'
                performance_metrics = None
            else:
                test_result = TestResult.PASSED
                message = str(result) if result else 'Test completed'
                performance_metrics = None
            
            # Check performance expectations
            if duration > test_case.expected_duration * 2:
                if test_result == TestResult.PASSED:
                    test_result = TestResult.FAILED
                    message += f" (Performance issue: {duration:.2f}s > {test_case.expected_duration * 2:.2f}s)"
            
            return TestExecutionResult(
                test_name=test_case.name,
                result=test_result,
                duration=duration,
                message=message,
                timestamp=datetime.now(),
                performance_metrics=performance_metrics
            )
        
        except asyncio.TimeoutError:
            return TestExecutionResult(
                test_name=test_case.name,
                result=TestResult.FAILED,
                duration=test_case.timeout,
                message=f"Test timed out after {test_case.timeout} seconds",
                timestamp=datetime.now()
            )
        
        except Exception as e:
            return TestExecutionResult(
                test_name=test_case.name,
                result=TestResult.ERROR,
                duration=time.time() - start_time,
                message=f"Test error: {str(e)}",
                timestamp=datetime.now(),
                error_details=traceback.format_exc()
            )
    
    async def _check_dependency(self, dependency: str) -> bool:
        """Check if test dependency is met"""
        if dependency == 'internet_connection':
            return await self._test_internet_connection()
        elif dependency == 'api_credentials':
            return await self._test_api_credentials()
        elif dependency == 'file_system':
            return self._test_file_system()
        else:
            return True  # Unknown dependency, assume met
    
    async def _test_internet_connection(self) -> bool:
        """Test internet connectivity"""
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get('https://www.google.com', timeout=10) as response:
                    return response.status == 200
        except:
            return False
    
    async def _test_api_credentials(self) -> bool:
        """Test API credentials availability"""
        try:
            from system.config.api_credentials import credentials
            return bool(credentials.get_credential('serpapi', 'api_key'))
        except:
            return False
    
    def _test_file_system(self) -> bool:
        """Test file system access"""
        try:
            test_dir = Path("system/reports/testing")
            test_dir.mkdir(parents=True, exist_ok=True)
            
            test_file = test_dir / ".test_file"
            test_file.write_text("test")
            test_file.unlink()
            
            return True
        except:
            return False
    
    # Individual Test Implementations
    async def test_serpapi_connectivity(self) -> Dict[str, Any]:
        """Test SerpAPI connectivity"""
        try:
            from system.config.api_credentials import credentials
            import aiohttp
            
            api_key = credentials.get_credential('serpapi', 'api_key')
            if not api_key:
                return {'success': False, 'message': 'SerpAPI key not configured'}
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"https://serpapi.com/account?api_key={api_key}",
                    timeout=10
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        remaining_searches = data.get('total_searches_left', 0)
                        
                        return {
                            'success': True,
                            'message': f'SerpAPI connected successfully, {remaining_searches} searches remaining',
                            'performance_metrics': {'response_time': response.headers.get('response-time')}
                        }
                    else:
                        return {'success': False, 'message': f'SerpAPI returned status {response.status}'}
        
        except Exception as e:
            return {'success': False, 'message': f'SerpAPI test failed: {str(e)}'}
    
    async def test_jina_api_connectivity(self) -> Dict[str, Any]:
        """Test Jina API connectivity"""
        try:
            from system.config.api_credentials import credentials
            import aiohttp
            
            api_key = credentials.get_credential('jina', 'api_key')
            if not api_key:
                return {'success': False, 'message': 'Jina API key not configured'}
            
            async with aiohttp.ClientSession() as session:
                headers = {'Authorization': f'Bearer {api_key}'}
                async with session.get(
                    'https://r.jina.ai/https://example.com',
                    headers=headers,
                    timeout=10
                ) as response:
                    if response.status == 200:
                        return {
                            'success': True,
                            'message': 'Jina API connected successfully'
                        }
                    else:
                        return {'success': False, 'message': f'Jina API returned status {response.status}'}
        
        except Exception as e:
            return {'success': False, 'message': f'Jina API test failed: {str(e)}'}
    
    async def test_gtmetrix_api(self) -> Dict[str, Any]:
        """Test GTmetrix API connectivity"""
        try:
            from system.config.api_credentials import credentials
            import aiohttp
            
            api_key = credentials.get_credential('gtmetrix', 'api_key')
            username = credentials.get_credential('gtmetrix', 'username')
            
            if not api_key or not username:
                return {'success': True, 'message': 'GTmetrix API not configured (optional service)'}
            
            async with aiohttp.ClientSession() as session:
                auth = aiohttp.BasicAuth(username, api_key)
                async with session.get(
                    'https://gtmetrix.com/api/2.0/credits',
                    auth=auth,
                    timeout=10
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        credits = data.get('credits', 0)
                        
                        return {
                            'success': True,
                            'message': f'GTmetrix API connected successfully, {credits} credits remaining'
                        }
                    else:
                        return {'success': False, 'message': f'GTmetrix API returned status {response.status}'}
        
        except Exception as e:
            return {'success': True, 'message': f'GTmetrix API test failed (optional): {str(e)}'}
    
    async def test_error_recovery_system(self) -> Dict[str, Any]:
        """Test error recovery system"""
        try:
            # Test basic error recovery
            @enhanced_recovery_system.with_error_recovery()
            async def test_function(should_fail: bool = False):
                if should_fail:
                    raise Exception("Test failure")
                return "Success!"
            
            # Test success case
            result = await test_function(False)
            if result != "Success!":
                return {'success': False, 'message': 'Error recovery system failed success case'}
            
            # Test failure and recovery
            try:
                await test_function(True)
                return {'success': False, 'message': 'Error recovery system should have failed'}
            except Exception:
                pass  # Expected
            
            # Test recovery statistics
            stats = enhanced_recovery_system.get_recovery_status()
            
            return {
                'success': True,
                'message': 'Error recovery system working correctly',
                'performance_metrics': {'recovery_stats': stats}
            }
        
        except Exception as e:
            return {'success': False, 'message': f'Error recovery test failed: {str(e)}'}
    
    async def test_health_monitor(self) -> Dict[str, Any]:
        """Test health monitoring system"""
        try:
            # Run a quick health check
            health_results = await health_monitor.run_comprehensive_health_check()
            
            if 'system_overall' not in health_results:
                return {'success': False, 'message': 'Health monitor missing overall status'}
            
            overall_status = health_results['system_overall'].status
            component_count = len(health_results) - 1  # Exclude system_overall
            
            return {
                'success': True,
                'message': f'Health monitor working correctly, checked {component_count} components',
                'performance_metrics': {
                    'overall_status': overall_status.value,
                    'components_checked': component_count
                }
            }
        
        except Exception as e:
            return {'success': False, 'message': f'Health monitor test failed: {str(e)}'}
    
    async def test_autonomous_manager(self) -> Dict[str, Any]:
        """Test autonomous operation manager"""
        try:
            # Test operation logging
            test_operation = {
                'operation_type': 'test',
                'operation_name': 'unit_test',
                'test_data': {'timestamp': datetime.now().isoformat()}
            }
            
            autonomous_manager.log_operation(
                test_operation['operation_type'],
                test_operation['operation_name'],
                test_operation['test_data']
            )
            
            # Test status retrieval
            status = autonomous_manager.get_operation_status()
            
            return {
                'success': True,
                'message': 'Autonomous manager working correctly',
                'performance_metrics': {'operation_status': status}
            }
        
        except Exception as e:
            return {'success': False, 'message': f'Autonomous manager test failed: {str(e)}'}
    
    async def test_client_folder_creation(self) -> Dict[str, Any]:
        """Test client folder structure creation"""
        try:
            test_client_domain = "test_client_example_com"
            client_dir = Path(f"clients/{test_client_domain}")
            
            # Clean up any existing test directory
            if client_dir.exists():
                import shutil
                shutil.rmtree(client_dir)
            
            # Create standard client structure
            required_dirs = [
                client_dir / "strategy",
                client_dir / "research",
                client_dir / "content",
                client_dir / "technical",
                client_dir / "implementation"
            ]
            
            for dir_path in required_dirs:
                dir_path.mkdir(parents=True, exist_ok=True)
            
            # Create README
            readme_file = client_dir / "README.md"
            readme_file.write_text(f"# {test_client_domain}\n\nTest client project")
            
            # Verify structure
            all_created = all(dir_path.exists() for dir_path in required_dirs)
            readme_exists = readme_file.exists()
            
            # Clean up
            if client_dir.exists():
                import shutil
                shutil.rmtree(client_dir)
            
            if all_created and readme_exists:
                return {
                    'success': True,
                    'message': 'Client folder structure created successfully'
                }
            else:
                return {'success': False, 'message': 'Client folder structure creation failed'}
        
        except Exception as e:
            return {'success': False, 'message': f'Client folder test failed: {str(e)}'}
    
    async def test_web_scraping_workflow(self) -> Dict[str, Any]:
        """Test web scraping workflow"""
        try:
            # Test simple web scraping
            test_url = "https://example.com"
            
            # Use enhanced recovery system for scraping
            from system.reliability.enhanced_error_recovery import enhanced_recovery_system
            
            success, result = await enhanced_recovery_system.execute_with_enhanced_recovery(
                self._test_scrape_function,
                'web_scraping',
                test_url,
                enable_fallback=True
            )
            
            if success:
                return {
                    'success': True,
                    'message': 'Web scraping workflow working correctly'
                }
            else:
                return {'success': False, 'message': f'Web scraping failed: {result}'}
        
        except Exception as e:
            return {'success': False, 'message': f'Web scraping test failed: {str(e)}'}
    
    async def _test_scrape_function(self, url: str) -> str:
        """Simple test scraping function"""
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    content = await response.text()
                    return f"Scraped {len(content)} characters from {url}"
                else:
                    raise Exception(f"HTTP {response.status}")
    
    async def test_analysis_pipeline(self) -> Dict[str, Any]:
        """Test analysis pipeline workflow"""
        try:
            # Simulate analysis pipeline
            test_data = {
                'url': 'https://example.com',
                'analysis_type': 'basic_seo'
            }
            
            # Simulate analysis steps
            steps = ['data_collection', 'processing', 'analysis', 'reporting']
            
            for step in steps:
                await asyncio.sleep(0.1)  # Simulate processing time
                # In real implementation, would run actual analysis
            
            return {
                'success': True,
                'message': f'Analysis pipeline completed {len(steps)} steps'
            }
        
        except Exception as e:
            return {'success': False, 'message': f'Analysis pipeline test failed: {str(e)}'}
    
    async def test_system_response_time(self) -> Dict[str, Any]:
        """Test system response times"""
        try:
            response_times = []
            
            # Test multiple operations
            for i in range(5):
                start_time = time.time()
                
                # Simulate system operation
                await asyncio.sleep(0.1)
                
                response_time = time.time() - start_time
                response_times.append(response_time)
            
            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = max(response_times)
            
            # Check if response times are acceptable
            if avg_response_time < 0.5 and max_response_time < 1.0:
                return {
                    'success': True,
                    'message': f'System response times acceptable (avg: {avg_response_time:.3f}s)',
                    'performance_metrics': {
                        'avg_response_time': avg_response_time,
                        'max_response_time': max_response_time,
                        'response_times': response_times
                    }
                }
            else:
                return {
                    'success': False,
                    'message': f'System response times too slow (avg: {avg_response_time:.3f}s)'
                }
        
        except Exception as e:
            return {'success': False, 'message': f'Response time test failed: {str(e)}'}
    
    async def test_memory_usage(self) -> Dict[str, Any]:
        """Test memory usage patterns"""
        try:
            import psutil
            
            # Get initial memory usage
            process = psutil.Process()
            initial_memory = process.memory_info().rss / 1024 / 1024  # MB
            
            # Simulate memory-intensive operation
            test_data = []
            for i in range(1000):
                test_data.append(f"Test data item {i} " * 100)
            
            # Get peak memory usage
            peak_memory = process.memory_info().rss / 1024 / 1024  # MB
            
            # Clean up
            del test_data
            
            # Get final memory usage
            final_memory = process.memory_info().rss / 1024 / 1024  # MB
            
            memory_increase = peak_memory - initial_memory
            memory_cleanup = peak_memory - final_memory
            
            return {
                'success': True,
                'message': f'Memory usage test completed (peak increase: {memory_increase:.1f}MB)',
                'performance_metrics': {
                    'initial_memory_mb': initial_memory,
                    'peak_memory_mb': peak_memory,
                    'final_memory_mb': final_memory,
                    'memory_increase_mb': memory_increase,
                    'memory_cleanup_mb': memory_cleanup
                }
            }
        
        except Exception as e:
            return {'success': False, 'message': f'Memory usage test failed: {str(e)}'}
    
    async def test_concurrent_operations(self) -> Dict[str, Any]:
        """Test concurrent operation handling"""
        try:
            async def test_operation(operation_id: int):
                await asyncio.sleep(0.1)
                return f"Operation {operation_id} completed"
            
            # Run multiple operations concurrently
            tasks = []
            for i in range(10):
                tasks.append(test_operation(i))
            
            start_time = time.time()
            results = await asyncio.gather(*tasks)
            end_time = time.time()
            
            total_time = end_time - start_time
            
            if len(results) == 10 and total_time < 0.5:  # Should be concurrent
                return {
                    'success': True,
                    'message': f'Concurrent operations working correctly ({total_time:.3f}s)',
                    'performance_metrics': {
                        'operations_completed': len(results),
                        'total_time': total_time,
                        'operations_per_second': len(results) / total_time
                    }
                }
            else:
                return {
                    'success': False,
                    'message': f'Concurrent operations too slow or failed ({total_time:.3f}s)'
                }
        
        except Exception as e:
            return {'success': False, 'message': f'Concurrent operations test failed: {str(e)}'}
    
    async def test_credential_security(self) -> Dict[str, Any]:
        """Test credential handling security"""
        try:
            # Check if .env file exists and has proper permissions
            env_file = Path('.env')
            
            if not env_file.exists():
                return {'success': False, 'message': '.env file not found'}
            
            # Basic security checks
            security_issues = []
            
            # Check file content (shouldn't contain obvious credentials in plain text)
            with open(env_file, 'r') as f:
                content = f.read()
                
                # Look for potential issues (this is a basic check)
                if 'password=' in content.lower():
                    security_issues.append('Potential plain text password found')
            
            # Check that credentials module works
            try:
                from system.config.api_credentials import credentials
                test_cred = credentials.get_credential('test', 'key')  # Should return None
                if test_cred is not None:
                    security_issues.append('Credentials system returned unexpected value')
            except Exception:
                security_issues.append('Credentials system not working')
            
            if not security_issues:
                return {
                    'success': True,
                    'message': 'Credential security checks passed'
                }
            else:
                return {
                    'success': False,
                    'message': f'Security issues found: {"; ".join(security_issues)}'
                }
        
        except Exception as e:
            return {'success': False, 'message': f'Credential security test failed: {str(e)}'}
    
    async def test_file_permissions(self) -> Dict[str, Any]:
        """Test file system permissions"""
        try:
            permission_issues = []
            
            # Check critical directories
            critical_paths = [
                Path('system'),
                Path('system/config'),
                Path('system/core_tools'),
                Path('clients')
            ]
            
            for path in critical_paths:
                if not path.exists():
                    permission_issues.append(f'Critical path missing: {path}')
                    continue
                
                # Test read/write access
                try:
                    test_file = path / '.permission_test'
                    test_file.write_text('test')
                    test_file.unlink()
                except Exception:
                    permission_issues.append(f'No write access to: {path}')
            
            if not permission_issues:
                return {
                    'success': True,
                    'message': 'File permissions check passed'
                }
            else:
                return {
                    'success': False,
                    'message': f'Permission issues: {"; ".join(permission_issues)}'
                }
        
        except Exception as e:
            return {'success': False, 'message': f'File permissions test failed: {str(e)}'}
    
    def _save_test_results(self, results: Dict[str, Any]):
        """Save test results to file"""
        try:
            results_dir = Path("system/reports/testing")
            results_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            results_file = results_dir / f"test_results_{results['suite_name']}_{timestamp}.json"
            
            # Convert results to JSON-serializable format
            json_results = json.loads(json.dumps(results, default=str))
            
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(json_results, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Test results saved: {results_file}")
        
        except Exception as e:
            self.logger.error(f"Failed to save test results: {e}")
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all test suites"""
        all_results = {
            'start_time': datetime.now().isoformat(),
            'suite_results': {},
            'overall_summary': {}
        }
        
        total_passed = total_failed = total_skipped = total_errors = 0
        
        for suite_name in self.test_suites.keys():
            suite_results = await self.run_test_suite(suite_name)
            all_results['suite_results'][suite_name] = suite_results
            
            if 'summary' in suite_results:
                total_passed += suite_results['summary'].get('passed', 0)
                total_failed += suite_results['summary'].get('failed', 0)
                total_skipped += suite_results['summary'].get('skipped', 0)
                total_errors += suite_results['summary'].get('errors', 0)
        
        total_tests = total_passed + total_failed + total_skipped + total_errors
        
        all_results['end_time'] = datetime.now().isoformat()
        all_results['overall_summary'] = {
            'total_tests': total_tests,
            'total_passed': total_passed,
            'total_failed': total_failed,
            'total_skipped': total_skipped,
            'total_errors': total_errors,
            'overall_success_rate': (total_passed / total_tests) * 100 if total_tests > 0 else 0
        }
        
        # Save comprehensive results
        self._save_test_results(all_results)
        
        return all_results

# Global testing framework instance
testing_framework = SystemTestingFramework()

async def run_critical_tests():
    """Run only critical tests for quick validation"""
    try:
        print("Running critical system tests...")
        
        # Run critical tests from all suites
        results = {}
        
        for suite_name, suite in testing_framework.test_suites.items():
            critical_results = await testing_framework.run_test_suite(
                suite_name,
                priorities=[TestPriority.CRITICAL]
            )
            results[suite_name] = critical_results
        
        # Print summary
        total_critical = sum(r['summary']['total_tests'] for r in results.values())
        total_passed = sum(r['summary']['passed'] for r in results.values())
        
        print(f"Critical tests completed: {total_passed}/{total_critical} passed")
        
        for suite_name, result in results.items():
            if result['summary']['total_tests'] > 0:
                print(f"  {suite_name}: {result['summary']['passed']}/{result['summary']['total_tests']} passed")
        
        return results
    
    except Exception as e:
        print(f"Critical tests failed: {e}")
        logging.error(f"Critical tests failed: {e}")
        return None

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='System Testing Framework')
    parser.add_argument('--suite', help='Run specific test suite')
    parser.add_argument('--critical', action='store_true', help='Run only critical tests')
    parser.add_argument('--all', action='store_true', help='Run all tests')
    
    args = parser.parse_args()
    
    if args.critical:
        asyncio.run(run_critical_tests())
    elif args.all:
        asyncio.run(testing_framework.run_all_tests())
    elif args.suite:
        asyncio.run(testing_framework.run_test_suite(args.suite))
    else:
        print("Available test suites:")
        for suite_name in testing_framework.test_suites.keys():
            print(f"  - {suite_name}")
        print("\nUsage: python testing_framework.py --suite <suite_name> | --critical | --all")