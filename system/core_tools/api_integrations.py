"""
Automatic API Integrations for Performance Testing and Competitive Analysis
Handles GTmetrix, SerpAPI, and Google APIs with autonomous rate limiting
"""

import asyncio
import aiohttp
import requests
from requests_ratelimiter import LimiterSession
import time
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path

from system.config.api_credentials import credentials
from system.orchestration.autonomous_operation_manager import autonomous_manager

class APIIntegrationManager:
    """Manages all API integrations with rate limiting and error handling"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.rate_limiters = self._setup_rate_limiters()
        
    def _setup_rate_limiters(self) -> Dict:
        """Setup rate-limited sessions for each API service"""
        return {
            'gtmetrix': LimiterSession(per_minute=10),
            'serpapi': LimiterSession(per_minute=60),
            'google': LimiterSession(per_minute=100)
        }

class GTMetrixIntegration:
    """GTmetrix API integration for performance testing"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.GTMetrix")
        self.base_url = "https://gtmetrix.com/api/2.0"
        self.session = LimiterSession(per_minute=10)  # GTmetrix rate limit
        
    async def test_website_performance(self, url: str, client_domain: str) -> Dict:
        """Test website performance using GTmetrix API"""
        
        # Check if we have credentials
        api_key = credentials.get_credential('gtmetrix', 'api_key')
        username = credentials.get_credential('gtmetrix', 'username')
        
        if not api_key or not username:
            return {
                'status': 'error',
                'error': 'GTmetrix API credentials not configured',
                'suggestion': 'Set GTMETRIX_API_KEY and GTMETRIX_USERNAME environment variables'
            }
        
        # Check autonomous operation permissions
        can_api, message = autonomous_manager.can_perform_operation('api_calls', service='gtmetrix')
        if not can_api:
            return {
                'status': 'error',
                'error': f"API call not allowed: {message}"
            }
        
        try:
            # Track API usage
            autonomous_manager.session_tracker.track_api_usage('gtmetrix')
            
            # Submit test request
            test_data = {
                'url': url,
                'location': 2,  # Sydney, Australia
                'browser': 3,   # Chrome
                'connection': 'broadband'
            }
            
            response = self.session.post(
                f"{self.base_url}/tests",
                auth=(username, api_key),
                data=test_data,
                timeout=30
            )
            
            if response.status_code != 200:
                return {
                    'status': 'error',
                    'error': f"GTmetrix API error: {response.status_code}",
                    'details': response.text
                }
            
            test_result = response.json()
            test_id = test_result.get('test_id')
            
            if not test_id:
                return {
                    'status': 'error',
                    'error': 'No test ID returned from GTmetrix'
                }
            
            # Poll for results (with timeout)
            result = await self._poll_for_results(test_id, username, api_key)
            
            # Save results to client folder
            if result.get('status') == 'success':
                await self._save_performance_report(result, client_domain)
            
            return result
            
        except Exception as e:
            self.logger.error(f"GTmetrix integration error: {e}")
            return {
                'status': 'error',
                'error': f"GTmetrix integration failed: {str(e)}"
            }
    
    async def _poll_for_results(self, test_id: str, username: str, api_key: str, max_wait: int = 300) -> Dict:
        """Poll GTmetrix for test completion"""
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            try:
                response = self.session.get(
                    f"{self.base_url}/tests/{test_id}",
                    auth=(username, api_key),
                    timeout=30
                )
                
                if response.status_code != 200:
                    await asyncio.sleep(10)
                    continue
                
                result = response.json()
                state = result.get('state')
                
                if state == 'completed':
                    return {
                        'status': 'success',
                        'test_id': test_id,
                        'results': result,
                        'performance_scores': {
                            'pagespeed_score': result.get('pagespeed_score'),
                            'yslow_score': result.get('yslow_score'),
                            'fully_loaded_time': result.get('fully_loaded_time'),
                            'page_load_time': result.get('page_load_time'),
                            'page_size': result.get('page_bytes'),
                            'requests': result.get('page_requests')
                        }
                    }
                elif state == 'error':
                    return {
                        'status': 'error',
                        'error': f"GTmetrix test failed: {result.get('error', 'Unknown error')}"
                    }
                
                # Still running, wait before next check
                await asyncio.sleep(15)
                
            except Exception as e:
                self.logger.warning(f"Error polling GTmetrix: {e}")
                await asyncio.sleep(10)
        
        return {
            'status': 'timeout',
            'error': f"GTmetrix test timed out after {max_wait} seconds"
        }
    
    async def _save_performance_report(self, result: Dict, client_domain: str) -> None:
        """Save performance report to client folder"""
        try:
            client_folder = Path(f"clients/{client_domain}/technical")
            client_folder.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_file = client_folder / f"gtmetrix_performance_report_{timestamp}.json"
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            # Track file operation
            autonomous_manager.session_tracker.increment('file_writes', 1)
            
            self.logger.info(f"Performance report saved: {report_file}")
            
        except Exception as e:
            self.logger.error(f"Failed to save performance report: {e}")

class SerpAPIIntegration:
    """SerpAPI integration for competitive analysis"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.SerpAPI")
        self.base_url = "https://serpapi.com/search"
        self.session = LimiterSession(per_minute=60)
    
    async def analyze_competitors(self, domain: str, keywords: List[str], client_domain: str) -> Dict:
        """Analyze competitors using SerpAPI"""
        
        api_key = credentials.get_credential('serpapi', 'api_key')
        if not api_key:
            return {
                'status': 'error',
                'error': 'SerpAPI key not configured',
                'suggestion': 'Set SERPAPI_KEY environment variable'
            }
        
        # Check autonomous operation permissions
        can_api, message = autonomous_manager.can_perform_operation('api_calls', service='serpapi')
        if not can_api:
            return {
                'status': 'error',
                'error': f"API call not allowed: {message}"
            }
        
        try:
            competitors_data = []
            
            for keyword in keywords[:5]:  # Limit to 5 keywords to control API usage
                # Track API usage
                if not autonomous_manager.session_tracker.track_api_usage('serpapi'):
                    break
                
                search_params = {
                    'q': keyword,
                    'location': 'Sydney, New South Wales, Australia',
                    'hl': 'en',
                    'gl': 'au',
                    'api_key': api_key
                }
                
                response = self.session.get(self.base_url, params=search_params, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    organic_results = data.get('organic_results', [])
                    
                    competitors_data.append({
                        'keyword': keyword,
                        'results_count': len(organic_results),
                        'top_competitors': [
                            {
                                'title': result.get('title'),
                                'link': result.get('link'),
                                'position': result.get('position'),
                                'snippet': result.get('snippet')
                            }
                            for result in organic_results[:10]
                        ]
                    })
                
                # Rate limiting delay
                await asyncio.sleep(2)
            
            result = {
                'status': 'success',
                'domain': domain,
                'analysis_date': datetime.now().isoformat(),
                'competitors_data': competitors_data
            }
            
            # Save competitive analysis report
            await self._save_competitive_report(result, client_domain)
            
            return result
            
        except Exception as e:
            self.logger.error(f"SerpAPI integration error: {e}")
            return {
                'status': 'error',
                'error': f"Competitive analysis failed: {str(e)}"
            }
    
    async def _save_competitive_report(self, result: Dict, client_domain: str) -> None:
        """Save competitive analysis report to client folder"""
        try:
            client_folder = Path(f"clients/{client_domain}/research")
            client_folder.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_file = client_folder / f"competitive_analysis_{timestamp}.json"
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            # Track file operation
            autonomous_manager.session_tracker.increment('file_writes', 1)
            
            self.logger.info(f"Competitive analysis report saved: {report_file}")
            
        except Exception as e:
            self.logger.error(f"Failed to save competitive report: {e}")

class GoogleAPIIntegration:
    """Google APIs integration for additional insights"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.Google")
        self.session = LimiterSession(per_minute=100)
    
    async def search_insights(self, domain: str, queries: List[str]) -> Dict:
        """Get search insights using Google Custom Search API"""
        
        api_key = credentials.get_credential('google', 'api_key')
        cse_id = credentials.get_credential('google', 'cse_id')
        
        if not api_key or not cse_id:
            return {
                'status': 'error',
                'error': 'Google API credentials not configured',
                'suggestion': 'Set GOOGLE_API_KEY and GOOGLE_CSE_ID environment variables'
            }
        
        # Check autonomous operation permissions
        can_api, message = autonomous_manager.can_perform_operation('api_calls', service='google')
        if not can_api:
            return {
                'status': 'error',
                'error': f"API call not allowed: {message}"
            }
        
        try:
            insights = []
            base_url = "https://www.googleapis.com/customsearch/v1"
            
            for query in queries[:3]:  # Limit queries
                # Track API usage
                if not autonomous_manager.session_tracker.track_api_usage('google'):
                    break
                
                params = {
                    'key': api_key,
                    'cx': cse_id,
                    'q': f"site:{domain} {query}",
                    'num': 10
                }
                
                response = self.session.get(base_url, params=params, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    insights.append({
                        'query': query,
                        'total_results': data.get('searchInformation', {}).get('totalResults', 0),
                        'results': data.get('items', [])[:5]
                    })
                
                await asyncio.sleep(1)  # Rate limiting
            
            return {
                'status': 'success',
                'domain': domain,
                'insights': insights
            }
            
        except Exception as e:
            self.logger.error(f"Google API integration error: {e}")
            return {
                'status': 'error',
                'error': f"Google search insights failed: {str(e)}"
            }

# Global API integration instances
gtmetrix_api = GTMetrixIntegration()
serpapi_integration = SerpAPIIntegration()
google_api = GoogleAPIIntegration()