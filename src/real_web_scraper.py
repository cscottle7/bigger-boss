"""
Real Web Scraping Implementation
Replaces mock tools with actual web scraping using multiple approaches
"""

import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
from urllib.robotparser import RobotFileParser
import time
import random
import json
import logging
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
import ssl
import certifi
from datetime import datetime

# Try to import Playwright (optional dependency)
try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("Playwright not available. Install with: pip install playwright")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class WebCrawlResult:
    """Result structure for web crawling operations"""
    url: str
    status_code: int
    title: str
    meta_description: str
    headers: Dict[str, str]
    links: List[str]
    images: List[str]
    content_length: int
    load_time: float
    errors: List[str]
    content_preview: str = ""
    h1_tags: List[str] = None
    h2_tags: List[str] = None
    schema_markup: List[Dict] = None
    performance_metrics: Dict[str, Any] = None


@dataclass
class GTMetrixResult:
    """Result structure for GTMetrix performance testing"""
    test_id: str
    url: str
    lighthouse_score: int
    pagespeed_score: int
    yslow_score: int
    page_load_time: float
    total_page_size: int
    recommendations: List[Dict[str, Any]]


@dataclass
class AccessibilityResult:
    """Result structure for accessibility testing"""
    url: str
    violations: List[Dict[str, Any]]
    passes: List[Dict[str, Any]]
    wcag_level: str
    total_issues: int
    critical_issues: int


class RealWebCrawler:
    """Real web crawling functionality using multiple approaches"""
    
    def __init__(self):
        self.session = None
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
        ]
        
    async def web_crawl(self, url: str, depth: int = 1, max_pages: int = 10) -> List[WebCrawlResult]:
        """
        Real web crawling function using aiohttp for fast, real-world analysis
        """
        start_time = time.time()
        results = []
        visited = set()
        to_visit = [(url, 0)]  # (url, current_depth)
        
        logger.info(f"Starting real crawl of {url} with depth {depth}")
        
        # Create SSL context
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE  # For testing - use CERT_REQUIRED in production
        
        connector = aiohttp.TCPConnector(ssl=ssl_context, limit=20, limit_per_host=5)
        timeout = aiohttp.ClientTimeout(total=30, connect=10)
        
        async with aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={'User-Agent': random.choice(self.user_agents)}
        ) as session:
            
            while to_visit and len(results) < max_pages:
                current_url, current_depth = to_visit.pop(0)
                
                if current_url in visited or current_depth > depth:
                    continue
                    
                visited.add(current_url)
                
                try:
                    result = await self._crawl_single_page(session, current_url)
                    results.append(result)
                    
                    # Add links for deeper crawling
                    if current_depth < depth:
                        for link in result.links[:5]:  # Limit links per page
                            if link not in visited:
                                to_visit.append((link, current_depth + 1))
                    
                    # Respectful crawling delay
                    await asyncio.sleep(random.uniform(0.5, 1.5))
                    
                except Exception as e:
                    logger.error(f"Error crawling {current_url}: {str(e)}")
                    # Create error result
                    error_result = WebCrawlResult(
                        url=current_url,
                        status_code=0,
                        title="Error",
                        meta_description="",
                        headers={},
                        links=[],
                        images=[],
                        content_length=0,
                        load_time=0,
                        errors=[str(e)]
                    )
                    results.append(error_result)
        
        total_time = time.time() - start_time
        logger.info(f"Completed real crawl: {len(results)} pages analyzed in {total_time:.2f}s")
        return results
    
    async def _crawl_single_page(self, session: aiohttp.ClientSession, url: str) -> WebCrawlResult:
        """Crawl a single page and extract comprehensive data"""
        start_time = time.time()
        
        try:
            async with session.get(url) as response:
                load_time = time.time() - start_time
                
                # Get response data
                content = await response.text()
                headers = dict(response.headers)
                
                # Parse with BeautifulSoup
                soup = BeautifulSoup(content, 'html.parser')
                
                # Extract page data
                title = self._extract_title(soup)
                meta_description = self._extract_meta_description(soup)
                links = self._extract_links(soup, url)
                images = self._extract_images(soup, url)
                h1_tags = self._extract_heading_tags(soup, 'h1')
                h2_tags = self._extract_heading_tags(soup, 'h2')
                schema_markup = self._extract_schema_markup(soup)
                
                return WebCrawlResult(
                    url=url,
                    status_code=response.status,
                    title=title,
                    meta_description=meta_description,
                    headers=headers,
                    links=links,
                    images=images,
                    content_length=len(content),
                    load_time=load_time,
                    errors=[],
                    content_preview=content[:500] + "..." if len(content) > 500 else content,
                    h1_tags=h1_tags,
                    h2_tags=h2_tags,
                    schema_markup=schema_markup
                )
                
        except Exception as e:
            return WebCrawlResult(
                url=url,
                status_code=0,
                title="Error",
                meta_description="",
                headers={},
                links=[],
                images=[],
                content_length=0,
                load_time=time.time() - start_time,
                errors=[str(e)]
            )
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title"""
        title_tag = soup.find('title')
        return title_tag.get_text().strip() if title_tag else "No title found"
    
    def _extract_meta_description(self, soup: BeautifulSoup) -> str:
        """Extract meta description"""
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        return meta_desc.get('content', '').strip() if meta_desc else "No meta description found"
    
    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract all links from the page"""
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)
            if full_url.startswith(('http://', 'https://')):
                links.append(full_url)
        return list(set(links))  # Remove duplicates
    
    def _extract_images(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract all images from the page"""
        images = []
        for img in soup.find_all('img', src=True):
            src = img['src']
            full_url = urljoin(base_url, src)
            images.append(full_url)
        return list(set(images))  # Remove duplicates
    
    def _extract_heading_tags(self, soup: BeautifulSoup, tag_name: str) -> List[str]:
        """Extract heading tags (h1, h2, etc.)"""
        headings = []
        for heading in soup.find_all(tag_name):
            text = heading.get_text().strip()
            if text:
                headings.append(text)
        return headings
    
    def _extract_schema_markup(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract JSON-LD schema markup"""
        schema_scripts = soup.find_all('script', type='application/ld+json')
        schemas = []
        
        for script in schema_scripts:
            try:
                schema_data = json.loads(script.string)
                schemas.append(schema_data)
            except (json.JSONDecodeError, AttributeError):
                continue
        
        return schemas
    
    def read_robots_txt(self, url: str) -> Dict[str, Any]:
        """Real robots.txt analysis"""
        logger.info(f"Reading robots.txt for {url}")
        
        try:
            # Construct robots.txt URL
            parsed_url = urlparse(url)
            robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
            
            # Use RobotFileParser
            robot_parser = RobotFileParser()
            robot_parser.set_url(robots_url)
            robot_parser.read()
            
            # Extract sitemap URLs
            sitemaps = []
            try:
                response = requests.get(robots_url, timeout=10)
                if response.status_code == 200:
                    content = response.text
                    for line in content.split('\n'):
                        if line.lower().startswith('sitemap:'):
                            sitemap_url = line.split(':', 1)[1].strip()
                            sitemaps.append(sitemap_url)
            except requests.RequestException:
                pass
            
            return {
                "exists": True,
                "allows_crawling": robot_parser.can_fetch('*', url),
                "sitemap_urls": sitemaps,
                "disallowed_paths": self._extract_disallowed_paths(robots_url),
                "crawl_delay": robot_parser.crawl_delay('*'),
                "issues": self._analyze_robots_issues(robot_parser, sitemaps)
            }
            
        except Exception as e:
            logger.warning(f"Could not read robots.txt for {url}: {str(e)}")
            return {
                "exists": False,
                "allows_crawling": True,
                "sitemap_urls": [],
                "disallowed_paths": [],
                "crawl_delay": None,
                "issues": [f"Could not access robots.txt: {str(e)}"]
            }
    
    def _extract_disallowed_paths(self, robots_url: str) -> List[str]:
        """Extract disallowed paths from robots.txt"""
        disallowed = []
        try:
            response = requests.get(robots_url, timeout=10)
            if response.status_code == 200:
                for line in response.text.split('\n'):
                    if line.lower().startswith('disallow:'):
                        path = line.split(':', 1)[1].strip()
                        if path:
                            disallowed.append(path)
        except requests.RequestException:
            pass
        return disallowed
    
    def _analyze_robots_issues(self, robot_parser: RobotFileParser, sitemaps: List[str]) -> List[str]:
        """Analyze common robots.txt issues"""
        issues = []
        
        if not sitemaps:
            issues.append("No sitemap declared in robots.txt")
        
        # Check for overly restrictive rules
        try:
            if not robot_parser.can_fetch('Googlebot', '/'):
                issues.append("Homepage is disallowed for Googlebot")
        except:
            pass
        
        return issues
    
    def fetch_url(self, url: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Real URL fetching with comprehensive response analysis"""
        start_time = time.time()
        
        logger.info(f"Fetching URL: {url}")
        
        # Prepare headers
        request_headers = {
            'User-Agent': random.choice(self.user_agents)
        }
        if headers:
            request_headers.update(headers)
        
        try:
            response = requests.get(
                url, 
                headers=request_headers,
                timeout=15,
                allow_redirects=True,
                verify=False  # For testing - use True in production
            )
            
            response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            # Analyze SSL certificate
            ssl_valid = self._check_ssl_validity(url)
            
            # Count redirects
            redirect_count = len(response.history)
            
            return {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "response_time": response_time,
                "ssl_valid": ssl_valid,
                "redirects": redirect_count,
                "content_preview": response.text[:1000] if response.text else "",
                "content_type": response.headers.get('content-type', ''),
                "server": response.headers.get('server', ''),
                "final_url": response.url,
                "encoding": response.encoding
            }
            
        except requests.exceptions.SSLError as e:
            return {
                "status_code": 0,
                "headers": {},
                "response_time": (time.time() - start_time) * 1000,
                "ssl_valid": False,
                "redirects": 0,
                "content_preview": "",
                "error": f"SSL Error: {str(e)}"
            }
        except requests.exceptions.Timeout as e:
            return {
                "status_code": 0,
                "headers": {},
                "response_time": (time.time() - start_time) * 1000,
                "ssl_valid": False,
                "redirects": 0,
                "content_preview": "",
                "error": f"Timeout: {str(e)}"
            }
        except requests.exceptions.RequestException as e:
            return {
                "status_code": 0,
                "headers": {},
                "response_time": (time.time() - start_time) * 1000,
                "ssl_valid": False,
                "redirects": 0,
                "content_preview": "",
                "error": f"Request Error: {str(e)}"
            }
    
    def _check_ssl_validity(self, url: str) -> bool:
        """Check if SSL certificate is valid"""
        try:
            parsed = urlparse(url)
            if parsed.scheme != 'https':
                return True  # HTTP doesn't use SSL
            
            import socket
            import ssl
            
            context = ssl.create_default_context()
            with socket.create_connection((parsed.hostname, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=parsed.hostname) as ssock:
                    return True
        except:
            return False


class PlaywrightWebCrawler:
    """Advanced web crawling using Playwright for JavaScript-heavy sites"""
    
    def __init__(self):
        self.browser = None
        self.context = None
    
    async def web_crawl_advanced(self, url: str, depth: int = 1, max_pages: int = 10) -> List[WebCrawlResult]:
        """
        Advanced web crawling using Playwright for JavaScript-rendered content
        """
        if not PLAYWRIGHT_AVAILABLE:
            logger.warning("Playwright not available. Falling back to basic crawler.")
            basic_crawler = RealWebCrawler()
            return await basic_crawler.web_crawl(url, depth, max_pages)
        
        results = []
        visited = set()
        to_visit = [(url, 0)]
        
        async with async_playwright() as p:
            # Launch browser
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent=random.choice(RealWebCrawler().user_agents),
                viewport={'width': 1920, 'height': 1080}
            )
            
            try:
                while to_visit and len(results) < max_pages:
                    current_url, current_depth = to_visit.pop(0)
                    
                    if current_url in visited or current_depth > depth:
                        continue
                    
                    visited.add(current_url)
                    
                    try:
                        result = await self._crawl_page_with_playwright(context, current_url)
                        results.append(result)
                        
                        # Add links for deeper crawling
                        if current_depth < depth:
                            for link in result.links[:5]:
                                if link not in visited:
                                    to_visit.append((link, current_depth + 1))
                        
                        # Respectful delay
                        await asyncio.sleep(random.uniform(1.0, 2.0))
                        
                    except Exception as e:
                        logger.error(f"Error crawling {current_url} with Playwright: {str(e)}")
            
            finally:
                await browser.close()
        
        return results
    
    async def _crawl_page_with_playwright(self, context, url: str) -> WebCrawlResult:
        """Crawl single page with Playwright for advanced analysis"""
        start_time = time.time()
        
        page = await context.new_page()
        
        try:
            # Navigate and wait for load
            response = await page.goto(url, wait_until='networkidle', timeout=30000)
            load_time = time.time() - start_time
            
            # Extract page data with JavaScript execution
            title = await page.title()
            
            # Get meta description
            meta_description = await page.get_attribute('meta[name="description"]', 'content') or ""
            
            # Extract links
            links = await page.evaluate('''() => {
                return Array.from(document.querySelectorAll('a[href]'))
                    .map(a => a.href)
                    .filter(href => href.startsWith('http'))
            }''')
            
            # Extract images
            images = await page.evaluate('''() => {
                return Array.from(document.querySelectorAll('img[src]'))
                    .map(img => img.src)
            }''')
            
            # Extract headings
            h1_tags = await page.evaluate('() => Array.from(document.querySelectorAll("h1")).map(h => h.textContent)')
            h2_tags = await page.evaluate('() => Array.from(document.querySelectorAll("h2")).map(h => h.textContent)')
            
            # Get page content
            content = await page.content()
            
            # Get performance metrics
            performance_metrics = await self._get_performance_metrics(page)
            
            return WebCrawlResult(
                url=url,
                status_code=response.status if response else 0,
                title=title,
                meta_description=meta_description,
                headers=dict(response.headers) if response else {},
                links=list(set(links)),
                images=list(set(images)),
                content_length=len(content),
                load_time=load_time,
                errors=[],
                content_preview=content[:500] + "..." if len(content) > 500 else content,
                h1_tags=h1_tags,
                h2_tags=h2_tags,
                performance_metrics=performance_metrics
            )
            
        except Exception as e:
            return WebCrawlResult(
                url=url,
                status_code=0,
                title="Error",
                meta_description="",
                headers={},
                links=[],
                images=[],
                content_length=0,
                load_time=time.time() - start_time,
                errors=[str(e)]
            )
        finally:
            await page.close()
    
    async def _get_performance_metrics(self, page) -> Dict[str, Any]:
        """Extract performance metrics using Playwright"""
        try:
            # Get navigation timing
            timing = await page.evaluate('''() => {
                const nav = performance.getEntriesByType('navigation')[0];
                return nav ? {
                    loadEventEnd: nav.loadEventEnd,
                    domContentLoadedEventEnd: nav.domContentLoadedEventEnd,
                    responseEnd: nav.responseEnd,
                    domInteractive: nav.domInteractive
                } : {};
            }''')
            
            # Get Largest Contentful Paint
            lcp = await page.evaluate('''() => {
                return new Promise((resolve) => {
                    new PerformanceObserver((list) => {
                        const entries = list.getEntries();
                        if (entries.length > 0) {
                            resolve(entries[entries.length - 1].startTime);
                        }
                    }).observe({entryTypes: ['largest-contentful-paint']});
                    
                    setTimeout(() => resolve(null), 5000); // 5 second timeout
                });
            }''')
            
            return {
                'load_time': timing.get('loadEventEnd', 0),
                'dom_ready': timing.get('domContentLoadedEventEnd', 0),
                'response_time': timing.get('responseEnd', 0),
                'dom_interactive': timing.get('domInteractive', 0),
                'largest_contentful_paint': lcp
            }
        except:
            return {}


# Initialize real web crawler
real_crawler = RealWebCrawler()
playwright_crawler = PlaywrightWebCrawler()

# Updated function exports for compatibility
async def web_crawl(url: str, depth: int = 1, max_pages: int = 10, use_playwright: bool = False) -> List[WebCrawlResult]:
    """Main web crawling function with option for Playwright"""
    if use_playwright and PLAYWRIGHT_AVAILABLE:
        return await playwright_crawler.web_crawl_advanced(url, depth, max_pages)
    else:
        return await real_crawler.web_crawl(url, depth, max_pages)

def read_robots_txt(url: str) -> Dict[str, Any]:
    """Read and analyze robots.txt"""
    return real_crawler.read_robots_txt(url)

def fetch_url(url: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """Fetch URL with comprehensive analysis"""
    return real_crawler.fetch_url(url, headers)


# Example usage
if __name__ == "__main__":
    async def test_crawler():
        # Test basic crawling
        results = await web_crawl("https://httpbin.org/html", depth=1, max_pages=3)
        print(f"Crawled {len(results)} pages")
        
        for result in results:
            print(f"URL: {result.url}")
            print(f"Status: {result.status_code}")
            print(f"Title: {result.title}")
            print(f"Load time: {result.load_time:.2f}s")
            print(f"Links found: {len(result.links)}")
            print("---")
    
    # Run test
    asyncio.run(test_crawler())