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
        """Analyze competitors using SerpAPI with backup account fallback"""

        # Try primary SerpAPI account first
        api_key = credentials.get_credential('serpapi', 'api_key')
        using_backup = False

        if not api_key:
            # Fallback to backup SerpAPI account
            api_key = credentials.get_credential('serpapi', 'api_key_backup')
            using_backup = True

            if not api_key:
                return {
                    'status': 'error',
                    'error': 'Neither primary nor backup SerpAPI keys configured',
                    'suggestion': 'Set SERPAPI_API_KEY or SERPAPI_API_KEY_BACKUP environment variable'
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

            # Log which account is being used
            if using_backup:
                self.logger.info("Using backup SerpAPI account (primary exhausted/unavailable)")

            # Always use SerpAPI endpoint (same for both accounts)
            base_url = self.base_url
            service_name = 'serpapi'

            for keyword in keywords[:5]:  # Limit to 5 keywords to control API usage
                # Track API usage
                if not autonomous_manager.session_tracker.track_api_usage(service_name):
                    break

                # Build search params (both APIs use similar params)
                search_params = {
                    'q': keyword,
                    'location': 'Sydney, New South Wales, Australia',
                    'hl': 'en',
                    'gl': 'au',
                    'api_key': api_key
                }

                response = self.session.get(base_url, params=search_params, timeout=30)
                
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

class JINAContentAnalyzer:
    """JINA AI integration for content analysis and semantic search"""

    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.JINA")
        self.base_url = "https://api.jina.ai/v1"
        self.session = LimiterSession(per_minute=100)  # Conservative limit

    async def analyze_content_uniqueness(self, content_samples: List[Dict[str, str]], client_domain: str) -> Dict:
        """Analyze content uniqueness using JINA embeddings"""

        api_key = credentials.get_credential('jina', 'api_key')
        if not api_key:
            return {
                'status': 'error',
                'error': 'JINA API key not configured',
                'suggestion': 'Set JINA_API_KEY environment variable'
            }

        # Check autonomous operation permissions
        can_api, message = autonomous_manager.can_perform_operation('api_calls', service='jina')
        if not can_api:
            return {
                'status': 'error',
                'error': f"API call not allowed: {message}"
            }

        try:
            # Track API usage
            autonomous_manager.session_tracker.track_api_usage('jina')

            # Prepare content for embedding (limit to prevent token overuse)
            texts = [sample.get('text', '')[:1000] for sample in content_samples[:50]]

            # Get embeddings using binary encoding for efficiency (96% size reduction)
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }

            payload = {
                'input': texts,
                'model': 'jina-embeddings-v3',
                'encoding_type': 'ubinary',  # Binary encoding for 96% size reduction
                'task': 'text-matching'
            }

            response = self.session.post(
                f"{self.base_url}/embeddings",
                headers=headers,
                json=payload,
                timeout=60
            )

            if response.status_code != 200:
                return {
                    'status': 'error',
                    'error': f"JINA API error: {response.status_code}",
                    'details': response.text
                }

            embeddings_data = response.json()
            embeddings = embeddings_data.get('data', [])

            # Calculate similarity scores
            similarity_analysis = await self._calculate_similarity_matrix(embeddings, content_samples)

            result = {
                'status': 'success',
                'analysis_date': datetime.now().isoformat(),
                'total_samples_analyzed': len(texts),
                'similarity_analysis': similarity_analysis,
                'uniqueness_score': similarity_analysis.get('avg_uniqueness', 0),
                'duplicate_risk_count': similarity_analysis.get('high_similarity_pairs', 0)
            }

            # Save content analysis report
            await self._save_content_analysis_report(result, client_domain)

            return result

        except Exception as e:
            self.logger.error(f"JINA content analysis error: {e}")
            return {
                'status': 'error',
                'error': f"Content analysis failed: {str(e)}"
            }

    async def _calculate_similarity_matrix(self, embeddings: List, content_samples: List[Dict]) -> Dict:
        """Calculate content similarity scores"""
        try:
            import numpy as np

            # Convert embeddings to numpy array
            emb_array = np.array([emb['embedding'] for emb in embeddings])

            # Calculate cosine similarity matrix
            from numpy.linalg import norm
            similarity_matrix = np.dot(emb_array, emb_array.T) / (
                norm(emb_array, axis=1)[:, None] * norm(emb_array, axis=1)[None, :]
            )

            # Analyze uniqueness
            high_similarity_threshold = 0.85
            high_similarity_pairs = 0
            similarity_scores = []

            for i in range(len(similarity_matrix)):
                for j in range(i + 1, len(similarity_matrix)):
                    similarity = similarity_matrix[i][j]
                    similarity_scores.append(similarity)
                    if similarity > high_similarity_threshold:
                        high_similarity_pairs += 1

            avg_similarity = np.mean(similarity_scores) if similarity_scores else 0
            avg_uniqueness = 1 - avg_similarity

            return {
                'avg_uniqueness': float(avg_uniqueness),
                'avg_similarity': float(avg_similarity),
                'high_similarity_pairs': high_similarity_pairs,
                'total_comparisons': len(similarity_scores)
            }

        except Exception as e:
            self.logger.warning(f"Similarity calculation error: {e}")
            return {
                'avg_uniqueness': 0.5,
                'avg_similarity': 0.5,
                'high_similarity_pairs': 0,
                'total_comparisons': 0,
                'error': str(e)
            }

    async def cluster_keywords(self, keywords: List[str], client_domain: str) -> Dict:
        """Cluster keywords using semantic similarity"""

        api_key = credentials.get_credential('jina', 'api_key')
        if not api_key:
            return {
                'status': 'error',
                'error': 'JINA API key not configured'
            }

        try:
            # Track API usage
            if not autonomous_manager.session_tracker.track_api_usage('jina'):
                return {
                    'status': 'error',
                    'error': 'API usage limit reached'
                }

            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }

            payload = {
                'input': keywords[:200],  # Limit to 200 keywords
                'model': 'jina-embeddings-v3',
                'encoding_type': 'ubinary',
                'task': 'clustering'
            }

            response = self.session.post(
                f"{self.base_url}/embeddings",
                headers=headers,
                json=payload,
                timeout=60
            )

            if response.status_code != 200:
                return {
                    'status': 'error',
                    'error': f"JINA API error: {response.status_code}"
                }

            embeddings_data = response.json()

            # Perform clustering
            clusters = await self._perform_clustering(embeddings_data.get('data', []), keywords)

            result = {
                'status': 'success',
                'total_keywords': len(keywords),
                'clusters': clusters
            }

            # Save keyword clustering report
            await self._save_keyword_clustering_report(result, client_domain)

            return result

        except Exception as e:
            self.logger.error(f"JINA keyword clustering error: {e}")
            return {
                'status': 'error',
                'error': f"Keyword clustering failed: {str(e)}"
            }

    async def _perform_clustering(self, embeddings: List, keywords: List[str]) -> List[Dict]:
        """Perform k-means clustering on keyword embeddings"""
        try:
            import numpy as np
            from sklearn.cluster import KMeans

            emb_array = np.array([emb['embedding'] for emb in embeddings])

            # Determine optimal cluster count (between 5 and 20)
            n_clusters = min(max(len(keywords) // 10, 5), 20)

            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            cluster_labels = kmeans.fit_predict(emb_array)

            # Group keywords by cluster
            clusters = []
            for i in range(n_clusters):
                cluster_keywords = [keywords[j] for j in range(len(keywords)) if cluster_labels[j] == i]
                clusters.append({
                    'cluster_id': i,
                    'keywords': cluster_keywords,
                    'size': len(cluster_keywords)
                })

            return clusters

        except Exception as e:
            self.logger.warning(f"Clustering error: {e}")
            return []

    async def _save_content_analysis_report(self, result: Dict, client_domain: str) -> None:
        """Save content analysis report to client folder"""
        try:
            client_folder = Path(f"clients/{client_domain}/content")
            client_folder.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_file = client_folder / f"jina_content_analysis_{timestamp}.json"

            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            autonomous_manager.session_tracker.increment('file_writes', 1)
            self.logger.info(f"Content analysis report saved: {report_file}")

        except Exception as e:
            self.logger.error(f"Failed to save content analysis report: {e}")

    async def _save_keyword_clustering_report(self, result: Dict, client_domain: str) -> None:
        """Save keyword clustering report to client folder"""
        try:
            client_folder = Path(f"clients/{client_domain}/research")
            client_folder.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_file = client_folder / f"jina_keyword_clusters_{timestamp}.json"

            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            autonomous_manager.session_tracker.increment('file_writes', 1)
            self.logger.info(f"Keyword clustering report saved: {report_file}")

        except Exception as e:
            self.logger.error(f"Failed to save keyword clustering report: {e}")

class JINASearchAnalyzer:
    """JINA Search integration for web search and content extraction"""

    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.JINASearch")
        self.search_base = "https://s.jina.ai"
        self.reader_base = "https://r.jina.ai"
        self.session = LimiterSession(per_minute=40)  # Free tier: 40 RPM

    async def search_web(self, query: str, num_results: int = 5, client_domain: str = None) -> Dict:
        """Search web using s.jina.ai and return top results with full content"""

        api_key = credentials.get_credential('jina', 'api_key')
        if not api_key:
            return {
                'status': 'error',
                'error': 'JINA API key not configured',
                'suggestion': 'Set JINA_API_KEY environment variable'
            }

        # Check autonomous operation permissions
        can_api, message = autonomous_manager.can_perform_operation('api_calls', service='jina')
        if not can_api:
            return {
                'status': 'error',
                'error': f"API call not allowed: {message}"
            }

        try:
            # Track API usage
            autonomous_manager.session_tracker.track_api_usage('jina')

            # JINA Search returns top 5 by default
            headers = {
                'Authorization': f'Bearer {api_key}',
                'X-With-Links-Summary': 'true',
                'Accept': 'application/json'
            }

            # Use s.jina.ai for search
            search_url = f"{self.search_base}/{query}"

            response = self.session.get(
                search_url,
                headers=headers,
                timeout=30
            )

            if response.status_code != 200:
                return {
                    'status': 'error',
                    'error': f"JINA Search error: {response.status_code}",
                    'details': response.text
                }

            # Parse response
            search_data = response.json()

            result = {
                'status': 'success',
                'query': query,
                'search_date': datetime.now().isoformat(),
                'results': search_data.get('data', []),
                'total_results': len(search_data.get('data', []))
            }

            # Save search results if client_domain provided
            if client_domain:
                await self._save_search_results(result, client_domain, query)

            return result

        except Exception as e:
            self.logger.error(f"JINA Search error: {e}")
            return {
                'status': 'error',
                'error': f"Web search failed: {str(e)}"
            }

    async def extract_competitor_content(self, urls: List[str], client_domain: str) -> Dict:
        """Extract full content from competitor URLs using r.jina.ai"""

        api_key = credentials.get_credential('jina', 'api_key')
        if not api_key:
            return {
                'status': 'error',
                'error': 'JINA API key not configured'
            }

        try:
            # Track API usage
            if not autonomous_manager.session_tracker.track_api_usage('jina'):
                return {
                    'status': 'error',
                    'error': 'API usage limit reached'
                }

            headers = {
                'Authorization': f'Bearer {api_key}',
                'X-With-Links-Summary': 'true',
                'X-With-Images-Summary': 'true',
                'Accept': 'application/json'
            }

            competitor_content = []

            # Extract content from each URL (limit to 10)
            for url in urls[:10]:
                try:
                    # Use r.jina.ai for content extraction
                    reader_url = f"{self.reader_base}/{url}"

                    response = self.session.get(
                        reader_url,
                        headers=headers,
                        timeout=30
                    )

                    if response.status_code == 200:
                        content_data = response.json()
                        competitor_content.append({
                            'url': url,
                            'title': content_data.get('data', {}).get('title', ''),
                            'content': content_data.get('data', {}).get('content', ''),
                            'word_count': len(content_data.get('data', {}).get('content', '').split()),
                            'links': content_data.get('data', {}).get('links', []),
                            'images': content_data.get('data', {}).get('images', [])
                        })
                    else:
                        self.logger.warning(f"Failed to extract content from {url}: {response.status_code}")

                except Exception as url_error:
                    self.logger.warning(f"Error extracting {url}: {url_error}")
                    continue

            result = {
                'status': 'success',
                'extraction_date': datetime.now().isoformat(),
                'total_urls_processed': len(urls[:10]),
                'successful_extractions': len(competitor_content),
                'competitor_content': competitor_content
            }

            # Save competitor content analysis
            await self._save_competitor_content(result, client_domain)

            return result

        except Exception as e:
            self.logger.error(f"JINA content extraction error: {e}")
            return {
                'status': 'error',
                'error': f"Content extraction failed: {str(e)}"
            }

    async def analyze_search_keywords(self, keywords: List[str], client_domain: str) -> Dict:
        """Search multiple keywords and analyze top-ranking content"""

        all_results = {}

        for keyword in keywords[:10]:  # Limit to 10 keywords to stay within rate limits
            search_result = await self.search_web(
                query=keyword,
                client_domain=client_domain
            )

            if search_result['status'] == 'success':
                all_results[keyword] = {
                    'top_5_urls': [r.get('url', '') for r in search_result.get('results', [])],
                    'top_5_titles': [r.get('title', '') for r in search_result.get('results', [])],
                    'content_previews': [r.get('content', '')[:500] for r in search_result.get('results', [])]
                }

        result = {
            'status': 'success',
            'analysis_date': datetime.now().isoformat(),
            'keywords_analyzed': len(all_results),
            'keyword_results': all_results
        }

        # Save keyword analysis
        await self._save_keyword_analysis(result, client_domain)

        return result

    async def _save_search_results(self, result: Dict, client_domain: str, query: str) -> None:
        """Save search results to client folder"""
        try:
            client_folder = Path(f"clients/{client_domain}/research")
            client_folder.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            safe_query = query.replace(' ', '_').replace('/', '_')[:50]
            result_file = client_folder / f"jina_search_{safe_query}_{timestamp}.json"

            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            autonomous_manager.session_tracker.increment('file_writes', 1)
            self.logger.info(f"Search results saved: {result_file}")

        except Exception as e:
            self.logger.error(f"Failed to save search results: {e}")

    async def _save_competitor_content(self, result: Dict, client_domain: str) -> None:
        """Save competitor content analysis to client folder"""
        try:
            client_folder = Path(f"clients/{client_domain}/research")
            client_folder.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            result_file = client_folder / f"jina_competitor_content_{timestamp}.json"

            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            autonomous_manager.session_tracker.increment('file_writes', 1)
            self.logger.info(f"Competitor content analysis saved: {result_file}")

        except Exception as e:
            self.logger.error(f"Failed to save competitor content: {e}")

    async def _save_keyword_analysis(self, result: Dict, client_domain: str) -> None:
        """Save keyword analysis to client folder"""
        try:
            client_folder = Path(f"clients/{client_domain}/research")
            client_folder.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            result_file = client_folder / f"jina_keyword_search_analysis_{timestamp}.json"

            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            autonomous_manager.session_tracker.increment('file_writes', 1)
            self.logger.info(f"Keyword search analysis saved: {result_file}")

        except Exception as e:
            self.logger.error(f"Failed to save keyword analysis: {e}")

# Global API integration instances
gtmetrix_api = GTMetrixIntegration()
serpapi_integration = SerpAPIIntegration()
google_api = GoogleAPIIntegration()
jina_analyzer = JINAContentAnalyzer()
jina_search = JINASearchAnalyzer()