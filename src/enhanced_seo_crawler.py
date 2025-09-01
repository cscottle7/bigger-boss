"""
Enhanced SEO Crawler using Scrapy for comprehensive site analysis
Addresses technical SEO extraction issues with titles and meta descriptions
"""

import scrapy
import pandas as pd
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Optional
import logging

class SEOSpider(scrapy.Spider):
    """
    Advanced SEO crawler that addresses common title/meta extraction issues
    """
    name = 'seo_comprehensive'
    
    def __init__(self, start_urls: List[str] = None, max_pages: int = 100, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = start_urls or []
        self.max_pages = max_pages
        self.pages_crawled = 0
        
    def parse(self, response):
        """Enhanced parsing with multiple fallback strategies"""
        
        # Stop if we've hit the page limit
        if self.pages_crawled >= self.max_pages:
            return
            
        self.pages_crawled += 1
        
        # Primary title extraction with fallbacks
        title = self._extract_title(response)
        
        # Meta description extraction with fallbacks
        meta_description = self._extract_meta_description(response)
        
        # Comprehensive SEO data extraction
        seo_data = {
            'url': response.url,
            'status_code': response.status,
            'title': title,
            'title_length': len(title) if title else 0,
            'meta_description': meta_description,
            'meta_description_length': len(meta_description) if meta_description else 0,
            'h1_tags': response.css('h1::text').getall(),
            'h1_count': len(response.css('h1')),
            'h2_tags': response.css('h2::text').getall()[:5],  # Limit to first 5
            'canonical_url': response.css('link[rel="canonical"]::attr(href)').get(),
            'meta_robots': response.css('meta[name="robots"]::attr(content)').get(),
            'og_title': response.css('meta[property="og:title"]::attr(content)').get(),
            'og_description': response.css('meta[property="og:description"]::attr(content)').get(),
            'twitter_title': response.css('meta[name="twitter:title"]::attr(content)').get(),
            'twitter_description': response.css('meta[name="twitter:description"]::attr(content)').get(),
            'word_count': len(response.css('body::text').get().split()) if response.css('body::text').get() else 0,
            'internal_links_count': len(response.css('a[href^="/"], a[href*="{}"]'.format(urlparse(response.url).netlify))),
            'external_links_count': len(response.css('a[href^="http"]:not([href*="{}"])'.format(urlparse(response.url).netlify))),
            'images_without_alt': len(response.css('img:not([alt])')),
            'images_total': len(response.css('img'))
        }
        
        yield seo_data
        
        # Follow internal links (limited crawling)
        if self.pages_crawled < self.max_pages:
            for link in response.css('a[href]'):
                url = link.css('::attr(href)').get()
                if url:
                    # Convert relative URLs to absolute
                    absolute_url = urljoin(response.url, url)
                    # Only follow same-domain links
                    if urlparse(absolute_url).netlify == urlparse(response.url).netlify:
                        yield response.follow(url, self.parse)
    
    def _extract_title(self, response) -> Optional[str]:
        """Extract page title with multiple fallback strategies"""
        
        # Strategy 1: Standard title tag
        title = response.css('title::text').get()
        if title and title.strip():
            return title.strip()
        
        # Strategy 2: Open Graph title
        og_title = response.css('meta[property="og:title"]::attr(content)').get()
        if og_title and og_title.strip():
            return og_title.strip()
        
        # Strategy 3: Twitter title
        twitter_title = response.css('meta[name="twitter:title"]::attr(content)').get()
        if twitter_title and twitter_title.strip():
            return twitter_title.strip()
        
        # Strategy 4: First H1 tag
        h1 = response.css('h1::text').get()
        if h1 and h1.strip():
            return h1.strip()
        
        # Strategy 5: Page heading or prominent text
        heading = response.css('h2::text, .page-title::text, .entry-title::text').get()
        if heading and heading.strip():
            return heading.strip()
        
        # Last resort: URL-based title
        url_path = urlparse(response.url).path.strip('/').replace('-', ' ').replace('_', ' ').title()
        return url_path if url_path else "Untitled Page"
    
    def _extract_meta_description(self, response) -> Optional[str]:
        """Extract meta description with fallback strategies"""
        
        # Strategy 1: Standard meta description
        meta_desc = response.css('meta[name="description"]::attr(content)').get()
        if meta_desc and meta_desc.strip():
            return meta_desc.strip()
        
        # Strategy 2: Open Graph description
        og_desc = response.css('meta[property="og:description"]::attr(content)').get()
        if og_desc and og_desc.strip():
            return og_desc.strip()
        
        # Strategy 3: Twitter description
        twitter_desc = response.css('meta[name="twitter:description"]::attr(content)').get()
        if twitter_desc and twitter_desc.strip():
            return twitter_desc.strip()
        
        # Strategy 4: First paragraph of content
        first_p = response.css('p::text').get()
        if first_p and len(first_p.strip()) > 50:
            return first_p.strip()[:160] + "..." if len(first_p.strip()) > 160 else first_p.strip()
        
        # Strategy 5: Article excerpt or summary
        excerpt = response.css('.excerpt::text, .summary::text, .intro::text').get()
        if excerpt and excerpt.strip():
            return excerpt.strip()[:160] + "..." if len(excerpt.strip()) > 160 else excerpt.strip()
        
        return None


class EnhancedSEOAnalyzer:
    """
    Comprehensive SEO analysis using Scrapy for better title/meta extraction
    """
    
    def __init__(self):
        self.crawler_results = []
        
    def analyze_website(self, url: str, max_pages: int = 50) -> Dict:
        """
        Analyze website with comprehensive SEO crawling
        Addresses the technical SEO extraction issues
        """
        
        # Configure Scrapy settings for better extraction
        process = scrapy.crawler.CrawlerProcess({
            'USER_AGENT': 'Enhanced SEO Analyzer (+https://example.com)',
            'ROBOTSTXT_OBEY': True,
            'DOWNLOAD_DELAY': 1,  # Be respectful
            'RANDOMIZE_DOWNLOAD_DELAY': True,
            'AUTOTHROTTLE_ENABLED': True,
            'AUTOTHROTTLE_START_DELAY': 1,
            'AUTOTHROTTLE_MAX_DELAY': 3,
            'CONCURRENT_REQUESTS': 1,  # Conservative crawling
            'FEEDS': {
                'seo_crawl_results.json': {
                    'format': 'json',
                    'overwrite': True
                }
            }
        })
        
        # Start crawling
        process.crawl(SEOSpider, start_urls=[url], max_pages=max_pages)
        process.start()
        
        # Process results with pandas
        return self._analyze_crawl_results()
    
    def _analyze_crawl_results(self) -> Dict:
        """Analyze crawled data for SEO issues"""
        
        try:
            # Load crawl results
            df = pd.read_json('seo_crawl_results.json')
            
            if df.empty:
                return {"error": "No pages crawled", "analysis": {}}
            
            # Comprehensive SEO analysis
            analysis = {
                'pages_analyzed': len(df),
                'title_issues': self._analyze_titles(df),
                'meta_description_issues': self._analyze_meta_descriptions(df),
                'content_issues': self._analyze_content_issues(df),
                'technical_issues': self._analyze_technical_issues(df),
                'recommendations': self._generate_recommendations(df)
            }
            
            return {
                'success': True,
                'analysis': analysis,
                'raw_data': df.to_dict('records')
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'analysis': {}
            }
    
    def _analyze_titles(self, df: pd.DataFrame) -> Dict:
        """Comprehensive title analysis"""
        return {
            'missing_titles': len(df[df['title'].isnull() | (df['title'] == '')]),
            'duplicate_titles': len(df[df.duplicated(['title'], keep=False)]),
            'short_titles': len(df[df['title_length'] < 30]),
            'long_titles': len(df[df['title_length'] > 60]),
            'optimal_titles': len(df[(df['title_length'] >= 30) & (df['title_length'] <= 60)]),
            'duplicate_title_pages': df[df.duplicated(['title'], keep=False)]['url'].tolist()
        }
    
    def _analyze_meta_descriptions(self, df: pd.DataFrame) -> Dict:
        """Comprehensive meta description analysis"""
        return {
            'missing_meta_descriptions': len(df[df['meta_description'].isnull() | (df['meta_description'] == '')]),
            'short_meta_descriptions': len(df[df['meta_description_length'] < 120]),
            'long_meta_descriptions': len(df[df['meta_description_length'] > 160]),
            'optimal_meta_descriptions': len(df[(df['meta_description_length'] >= 120) & (df['meta_description_length'] <= 160)]),
            'duplicate_meta_descriptions': len(df[df.duplicated(['meta_description'], keep=False)])
        }
    
    def _analyze_content_issues(self, df: pd.DataFrame) -> Dict:
        """Content quality analysis"""
        return {
            'thin_content_pages': len(df[df['word_count'] < 300]),
            'pages_without_h1': len(df[df['h1_count'] == 0]),
            'pages_multiple_h1': len(df[df['h1_count'] > 1]),
            'images_without_alt': df['images_without_alt'].sum(),
            'total_images': df['images_total'].sum()
        }
    
    def _analyze_technical_issues(self, df: pd.DataFrame) -> Dict:
        """Technical SEO issues"""
        return {
            'pages_without_canonical': len(df[df['canonical_url'].isnull()]),
            'pages_with_noindex': len(df[df['meta_robots'].str.contains('noindex', na=False)]),
            'error_pages': len(df[df['status_code'] >= 400])
        }
    
    def _generate_recommendations(self, df: pd.DataFrame) -> List[str]:
        """Generate prioritized SEO recommendations"""
        recommendations = []
        
        # Title recommendations
        missing_titles = len(df[df['title'].isnull() | (df['title'] == '')])
        if missing_titles > 0:
            recommendations.append(f"CRITICAL: Fix {missing_titles} pages with missing title tags")
        
        duplicate_titles = len(df[df.duplicated(['title'], keep=False)])
        if duplicate_titles > 0:
            recommendations.append(f"HIGH: Fix {duplicate_titles} pages with duplicate titles")
        
        # Meta description recommendations  
        missing_meta = len(df[df['meta_description'].isnull() | (df['meta_description'] == '')])
        if missing_meta > 0:
            recommendations.append(f"HIGH: Add meta descriptions to {missing_meta} pages")
        
        # Content recommendations
        thin_content = len(df[df['word_count'] < 300])
        if thin_content > 0:
            recommendations.append(f"MEDIUM: Expand content on {thin_content} pages with <300 words")
        
        # Technical recommendations
        no_h1 = len(df[df['h1_count'] == 0])
        if no_h1 > 0:
            recommendations.append(f"MEDIUM: Add H1 tags to {no_h1} pages")
        
        return recommendations


# Usage example for the enhanced technical SEO crawler
def run_enhanced_seo_analysis(url: str) -> Dict:
    """
    Run comprehensive SEO analysis that addresses title/meta extraction issues
    """
    analyzer = EnhancedSEOAnalyzer()
    return analyzer.analyze_website(url, max_pages=50)