#!/usr/bin/env python3
"""
Advanced Scrapy-based SEO Spider for Large-scale Website Crawling
Complements Playwright crawler for deeper, more efficient crawling
"""

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import json
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse
import logging
import re

class SEOSpider(scrapy.Spider):
    name = 'seo_spider'
    
    def __init__(self, start_url=None, max_pages=100, client_domain=None, *args, **kwargs):
        super(SEOSpider, self).__init__(*args, **kwargs)
        
        if not start_url:
            raise ValueError("start_url is required")
            
        self.start_urls = [start_url]
        self.allowed_domains = [urlparse(start_url).netloc]
        self.max_pages = int(max_pages)
        self.pages_crawled = 0
        self.client_domain = client_domain or urlparse(start_url).netloc.replace('.', '_').replace('-', '_')
        
        # Setup output directory
        self.output_dir = Path(f"clients/{self.client_domain}/technical")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Data storage
        self.crawled_data = []
        self.failed_urls = []
        
        # Configure logging
        logging.getLogger('scrapy').setLevel(logging.WARNING)
        
    def parse(self, response):
        """Parse each page and extract SEO data"""
        if self.pages_crawled >= self.max_pages:
            return
            
        # Extract comprehensive SEO data
        seo_data = self.extract_seo_data(response)
        self.crawled_data.append(seo_data)
        self.pages_crawled += 1
        
        self.logger.info(f"Scrapy crawled page {self.pages_crawled}: {response.url}")
        
        # Find and follow internal links
        if self.pages_crawled < self.max_pages:
            links = response.css('a::attr(href)').getall()
            for link in links[:20]:  # Limit links per page
                absolute_url = urljoin(response.url, link)
                
                # Only follow internal links
                if self.is_internal_link(absolute_url, response.url):
                    yield response.follow(absolute_url, callback=self.parse)
    
    def extract_seo_data(self, response):
        """Extract comprehensive SEO data from response"""
        # Get page title
        title = response.css('title::text').get()
        title = title.strip() if title else ''
        
        # Get meta description
        meta_desc = response.css('meta[name="description"]::attr(content)').get()
        if not meta_desc:
            meta_desc = response.css('meta[property="description"]::attr(content)').get()
        
        # Get all headings
        headings = {
            'h1': [h.strip() for h in response.css('h1::text').getall() if h.strip()],
            'h2': [h.strip() for h in response.css('h2::text').getall() if h.strip()],
            'h3': [h.strip() for h in response.css('h3::text').getall() if h.strip()],
            'h4': [h.strip() for h in response.css('h4::text').getall() if h.strip()],
            'h5': [h.strip() for h in response.css('h5::text').getall() if h.strip()],
            'h6': [h.strip() for h in response.css('h6::text').getall() if h.strip()]
        }
        
        # Get canonical URL
        canonical = response.css('link[rel="canonical"]::attr(href)').get()
        
        # Get robots meta
        robots = response.css('meta[name="robots"]::attr(content)').get()
        
        # Get Open Graph data
        og_data = {
            'title': response.css('meta[property="og:title"]::attr(content)').get(),
            'description': response.css('meta[property="og:description"]::attr(content)').get(),
            'image': response.css('meta[property="og:image"]::attr(content)').get(),
            'url': response.css('meta[property="og:url"]::attr(content)').get(),
            'type': response.css('meta[property="og:type"]::attr(content)').get(),
        }
        
        # Get Twitter Card data
        twitter_data = {
            'card': response.css('meta[name="twitter:card"]::attr(content)').get(),
            'title': response.css('meta[name="twitter:title"]::attr(content)').get(),
            'description': response.css('meta[name="twitter:description"]::attr(content)').get(),
            'image': response.css('meta[name="twitter:image"]::attr(content)').get(),
        }
        
        # Analyze text content
        body_text = ' '.join(response.css('body *::text').getall())
        word_count = len([word for word in body_text.split() if len(word) > 0])
        
        # Count links
        all_links = response.css('a[href]::attr(href)').getall()
        internal_links = len([link for link in all_links if self.is_internal_link(urljoin(response.url, link), response.url)])
        external_links = len(all_links) - internal_links
        
        # Count images
        images = response.css('img')
        images_with_alt = len([img for img in images if img.css('::attr(alt)').get()])
        images_without_alt = len(images) - images_with_alt
        
        # Compile SEO data
        seo_data = {
            'url': response.url,
            'title': title,
            'title_length': len(title),
            'meta_description': meta_desc or '',
            'meta_description_length': len(meta_desc) if meta_desc else 0,
            'canonical_url': canonical,
            'robots': robots,
            'headings': headings,
            'open_graph': og_data,
            'twitter_card': twitter_data,
            'word_count': word_count,
            'internal_links': internal_links,
            'external_links': external_links,
            'total_images': len(images),
            'images_with_alt': images_with_alt,
            'images_without_alt': images_without_alt,
            'crawl_timestamp': datetime.now().isoformat(),
            'crawler_type': 'scrapy'
        }
        
        # Analyze SEO issues
        seo_data['seo_issues'] = self.analyze_seo_issues(seo_data)
        seo_data['seo_score'] = self.calculate_seo_score(seo_data)
        
        return seo_data
    
    def is_internal_link(self, url, base_url):
        """Check if URL is internal to the site"""
        try:
            url_domain = urlparse(url).netloc
            base_domain = urlparse(base_url).netloc
            
            # Handle relative URLs and same domain
            if not url_domain or url_domain == base_domain:
                # Exclude common non-page URLs
                exclude_patterns = [
                    r'\.pdf$', r'\.jpg$', r'\.jpeg$', r'\.png$', r'\.gif$',
                    r'\.zip$', r'\.doc$', r'\.docx$', r'\.xls$', r'\.xlsx$',
                    r'mailto:', r'tel:', r'javascript:', r'#'
                ]
                
                for pattern in exclude_patterns:
                    if re.search(pattern, url.lower()):
                        return False
                
                return True
            
            return False
        except:
            return False
    
    def analyze_seo_issues(self, data):
        """Analyze SEO data and identify issues"""
        issues = []
        
        # Title issues
        if not data.get('title'):
            issues.append({"type": "critical", "category": "title", "issue": "Missing title tag"})
        elif len(data.get('title', '')) < 30:
            issues.append({"type": "warning", "category": "title", "issue": "Title too short (< 30 characters)"})
        elif len(data.get('title', '')) > 60:
            issues.append({"type": "warning", "category": "title", "issue": "Title too long (> 60 characters)"})
        
        # Meta description issues
        if not data.get('meta_description'):
            issues.append({"type": "critical", "category": "meta_description", "issue": "Missing meta description"})
        elif len(data.get('meta_description', '')) < 120:
            issues.append({"type": "warning", "category": "meta_description", "issue": "Meta description too short (< 120 characters)"})
        elif len(data.get('meta_description', '')) > 160:
            issues.append({"type": "warning", "category": "meta_description", "issue": "Meta description too long (> 160 characters)"})
        
        # H1 issues
        h1_tags = data.get('headings', {}).get('h1', [])
        if len(h1_tags) == 0:
            issues.append({"type": "critical", "category": "headings", "issue": "Missing H1 tag"})
        elif len(h1_tags) > 1:
            issues.append({"type": "warning", "category": "headings", "issue": f"Multiple H1 tags ({len(h1_tags)} found)"})
        
        # Image alt text issues
        if data.get('images_without_alt', 0) > 0:
            issues.append({"type": "warning", "category": "accessibility", 
                          "issue": f"{data['images_without_alt']} images missing alt text"})
        
        return issues
    
    def calculate_seo_score(self, data):
        """Calculate SEO score for the page"""
        score = 100
        
        # Title scoring
        if not data.get('title'):
            score -= 20
        elif len(data.get('title', '')) < 30 or len(data.get('title', '')) > 60:
            score -= 10
        
        # Meta description scoring
        if not data.get('meta_description'):
            score -= 20
        elif len(data.get('meta_description', '')) < 120 or len(data.get('meta_description', '')) > 160:
            score -= 10
        
        # H1 scoring
        h1_count = len(data.get('headings', {}).get('h1', []))
        if h1_count == 0:
            score -= 15
        elif h1_count > 1:
            score -= 10
        
        # Content length scoring
        if data.get('word_count', 0) < 300:
            score -= 15
        
        # Image alt text scoring
        if data.get('total_images', 0) > 0:
            alt_ratio = data.get('images_with_alt', 0) / data.get('total_images', 1)
            if alt_ratio < 0.8:
                score -= 10
        
        return max(0, score)
    
    def closed(self, reason):
        """Called when spider finishes - save all data"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Generate comprehensive report
        report = {
            'scan_metadata': {
                'start_url': self.start_urls[0],
                'client_domain': self.client_domain,
                'scan_date': datetime.now().isoformat(),
                'pages_crawled': len(self.crawled_data),
                'max_pages_setting': self.max_pages,
                'crawler_type': 'scrapy',
                'spider_name': self.name
            },
            'executive_summary': {
                'total_pages': len(self.crawled_data),
                'average_seo_score': 0,
                'critical_issues': 0,
                'warnings': 0
            },
            'page_by_page_analysis': self.crawled_data,
            'failed_urls': self.failed_urls
        }
        
        # Calculate summary stats
        if self.crawled_data:
            total_score = sum(page.get('seo_score', 0) for page in self.crawled_data)
            report['executive_summary']['average_seo_score'] = round(total_score / len(self.crawled_data), 1)
            
            # Count issues
            for page in self.crawled_data:
                for issue in page.get('seo_issues', []):
                    if issue.get('type') == 'critical':
                        report['executive_summary']['critical_issues'] += 1
                    elif issue.get('type') == 'warning':
                        report['executive_summary']['warnings'] += 1
        
        # Save JSON report
        json_file = self.output_dir / f'scrapy_seo_analysis_{timestamp}.json'
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # Save CSV summary
        csv_content = "URL,Page Title,Meta Description,H1 Tags,SEO Score,Word Count,Critical Issues,Warnings\\n"
        for page in self.crawled_data:
            title = page.get('title', '').replace('"', '""')
            meta_desc = page.get('meta_description', '').replace('"', '""')
            h1_tags = '; '.join(page.get('headings', {}).get('h1', [])).replace('"', '""')
            
            critical = len([i for i in page.get('seo_issues', []) if i.get('type') == 'critical'])
            warnings = len([i for i in page.get('seo_issues', []) if i.get('type') == 'warning'])
            
            csv_content += f'"{page.get("url", "")}","{title}","{meta_desc}","{h1_tags}",{page.get("seo_score", 0)},{page.get("word_count", 0)},{critical},{warnings}\\n'
        
        csv_file = self.output_dir / f'scrapy_seo_summary_{timestamp}.csv'
        with open(csv_file, 'w', encoding='utf-8') as f:
            f.write(csv_content)
        
        print(f"\\n🕷️  SCRAPY CRAWL COMPLETE!")
        print(f"📄 JSON Report: {json_file}")
        print(f"📊 CSV Summary: {csv_file}")
        print(f"📈 Pages crawled: {len(self.crawled_data)}")
        print(f"🎯 Average SEO score: {report['executive_summary']['average_seo_score']}/100")

def run_scrapy_crawl(start_url, max_pages=100, client_domain=None):
    """Run Scrapy SEO crawl"""
    process = CrawlerProcess({
        'USER_AGENT': 'Bigger-Boss-SEO-Scrapy/1.0',
        'ROBOTSTXT_OBEY': True,
        'CONCURRENT_REQUESTS': 2,
        'DOWNLOAD_DELAY': 2,
        'RANDOMIZE_DOWNLOAD_DELAY': 0.5,
        'LOG_LEVEL': 'WARNING'
    })
    
    process.crawl(SEOSpider, start_url=start_url, max_pages=max_pages, client_domain=client_domain)
    process.start()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python seo_spider.py <url> [max_pages]")
        sys.exit(1)
    
    url = sys.argv[1]
    max_pages = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    
    print(f"🕷️  Starting Scrapy SEO crawl: {url}")
    print(f"📄 Max pages: {max_pages}")
    
    run_scrapy_crawl(url, max_pages)