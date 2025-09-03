import scrapy
import json
from urllib.parse import urljoin, urlparse
import re


class SydneycoachSpider(scrapy.Spider):
    name = "sydneycoach"
    allowed_domains = ["sydneycoachcharter.com.au"]
    start_urls = ["https://sydneycoachcharter.com.au"]
    
    custom_settings = {
        'ROBOTSTXT_OBEY': True,
        'DOWNLOAD_DELAY': 1,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'USER_AGENT': 'SydneyCoachCharterAnalyzer/1.0 (+https://sydneycoachcharter.com.au/robots.txt)',
        'FEEDS': {
            'crawl_data.json': {
                'format': 'json',
                'overwrite': True,
            },
            'crawl_data.csv': {
                'format': 'csv',
                'overwrite': True,
            }
        }
    }
    
    def parse(self, response):
        # Extract comprehensive page data
        page_data = self.extract_page_data(response)
        yield page_data
        
        # Follow all internal links (skip tel:, mailto:, and other non-HTTP schemes)
        links = response.css('a::attr(href)').getall()
        for link in links:
            # Skip non-HTTP links
            if link and (link.startswith('tel:') or link.startswith('mailto:') or 
                        link.startswith('#') or link.startswith('javascript:')):
                continue
                
            absolute_url = urljoin(response.url, link)
            if self.is_internal_link(absolute_url) and absolute_url.startswith('http'):
                yield response.follow(absolute_url, callback=self.parse)
    
    def extract_page_data(self, response):
        """Extract comprehensive data from each page"""
        return {
            # URL and Basic Info
            'url': response.url,
            'status_code': response.status,
            'page_type': self.determine_page_type(response),
            
            # SEO Meta Data
            'title': response.css('title::text').get(),
            'meta_description': response.css('meta[name="description"]::attr(content)').get(),
            'meta_keywords': response.css('meta[name="keywords"]::attr(content)').get(),
            'meta_robots': response.css('meta[name="robots"]::attr(content)').get(),
            'canonical_url': response.css('link[rel="canonical"]::attr(href)').get(),
            
            # Open Graph Data
            'og_title': response.css('meta[property="og:title"]::attr(content)').get(),
            'og_description': response.css('meta[property="og:description"]::attr(content)').get(),
            'og_image': response.css('meta[property="og:image"]::attr(content)').get(),
            'og_url': response.css('meta[property="og:url"]::attr(content)').get(),
            
            # Twitter Card Data
            'twitter_card': response.css('meta[name="twitter:card"]::attr(content)').get(),
            'twitter_title': response.css('meta[name="twitter:title"]::attr(content)').get(),
            'twitter_description': response.css('meta[name="twitter:description"]::attr(content)').get(),
            
            # Content Analysis
            'h1_tags': response.css('h1::text').getall(),
            'h2_tags': response.css('h2::text').getall(),
            'h3_tags': response.css('h3::text').getall(),
            'h4_tags': response.css('h4::text').getall(),
            'h5_tags': response.css('h5::text').getall(),
            'h6_tags': response.css('h6::text').getall(),
            
            # Content Metrics
            'word_count': len(response.css('body::text').re(r'\w+')),
            'paragraph_count': len(response.css('p')),
            'text_content': ' '.join(response.css('body *::text').getall()).strip()[:1000],  # First 1000 chars
            
            # Link Analysis
            'internal_links': self.get_internal_links(response),
            'external_links': self.get_external_links(response),
            'total_links': len(response.css('a[href]')),
            
            # Image Analysis
            'images': self.extract_image_data(response),
            'total_images': len(response.css('img')),
            'images_without_alt': len(response.css('img:not([alt])')),
            
            # Technical SEO
            'schema_markup': self.extract_schema_markup(response),
            'structured_data_types': self.get_structured_data_types(response),
            
            # Performance Indicators
            'page_size_estimate': len(response.body),
            'css_files': response.css('link[rel="stylesheet"]::attr(href)').getall(),
            'js_files': response.css('script[src]::attr(src)').getall(),
            
            # Content Quality Indicators
            'has_contact_info': self.has_contact_info(response),
            'has_phone_number': bool(response.css('*::text').re(r'\(?0[2-9]\)?[\s-]?\d{4}[\s-]?\d{4}')),
            'has_email': bool(response.css('*::text').re(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')),
            'has_address': self.has_address_info(response),
            
            # Service-specific Content
            'mentions_wedding': bool(response.css('*::text').re(r'(?i)wedding|bridal|bride')),
            'mentions_corporate': bool(response.css('*::text').re(r'(?i)corporate|business|conference')),
            'mentions_school': bool(response.css('*::text').re(r'(?i)school|education|student')),
            'mentions_tourism': bool(response.css('*::text').re(r'(?i)tour|sightseeing|tourist')),
            'mentions_charter': bool(response.css('*::text').re(r'(?i)charter|hire|rental')),
            
            # Local SEO Indicators
            'mentions_sydney': bool(response.css('*::text').re(r'(?i)sydney')),
            'mentions_nsw': bool(response.css('*::text').re(r'(?i)nsw|new south wales')),
            'mentions_australia': bool(response.css('*::text').re(r'(?i)australia|australian')),
            
            # Forms and CTAs
            'contact_forms': len(response.css('form')),
            'quote_buttons': len(response.css('*::text').re(r'(?i)quote|get quote|request quote')),
            'book_now_buttons': len(response.css('*::text').re(r'(?i)book now|book|reserve')),
            
            # Social Media Links
            'facebook_links': response.css('a[href*="facebook.com"]::attr(href)').getall(),
            'instagram_links': response.css('a[href*="instagram.com"]::attr(href)').getall(),
            'linkedin_links': response.css('a[href*="linkedin.com"]::attr(href)').getall(),
            'twitter_links': response.css('a[href*="twitter.com"]::attr(href)').getall(),
        }
    
    def determine_page_type(self, response):
        """Determine the type of page based on URL and content"""
        url = response.url.lower()
        title = (response.css('title::text').get() or '').lower()
        
        if 'contact' in url or 'contact' in title:
            return 'contact'
        elif 'about' in url or 'about' in title:
            return 'about'
        elif 'service' in url or 'fleet' in url:
            return 'services'
        elif 'blog' in url or 'news' in url:
            return 'blog'
        elif response.url == 'https://sydneycoachcharter.com.au' or response.url == 'https://sydneycoachcharter.com.au/':
            return 'homepage'
        else:
            return 'other'
    
    def is_internal_link(self, url):
        """Check if a URL is internal to the domain"""
        return urlparse(url).netloc in ['sydneycoachcharter.com.au', 'www.sydneycoachcharter.com.au', '']
    
    def get_internal_links(self, response):
        """Extract all internal links"""
        internal_links = []
        for link in response.css('a::attr(href)').getall():
            absolute_url = urljoin(response.url, link)
            if self.is_internal_link(absolute_url):
                internal_links.append(absolute_url)
        return list(set(internal_links))  # Remove duplicates
    
    def get_external_links(self, response):
        """Extract all external links"""
        external_links = []
        for link in response.css('a::attr(href)').getall():
            absolute_url = urljoin(response.url, link)
            if not self.is_internal_link(absolute_url) and absolute_url.startswith('http'):
                external_links.append(absolute_url)
        return list(set(external_links))  # Remove duplicates
    
    def extract_image_data(self, response):
        """Extract comprehensive image data"""
        images = []
        for img in response.css('img'):
            images.append({
                'src': img.css('::attr(src)').get(),
                'alt': img.css('::attr(alt)').get(),
                'title': img.css('::attr(title)').get(),
                'width': img.css('::attr(width)').get(),
                'height': img.css('::attr(height)').get(),
            })
        return images
    
    def extract_schema_markup(self, response):
        """Extract structured data/schema markup"""
        schema_scripts = response.css('script[type="application/ld+json"]::text').getall()
        structured_data = []
        for script in schema_scripts:
            try:
                data = json.loads(script.strip())
                structured_data.append(data)
            except json.JSONDecodeError:
                pass
        return structured_data
    
    def get_structured_data_types(self, response):
        """Get types of structured data present on the page"""
        schema_data = self.extract_schema_markup(response)
        types = set()
        for data in schema_data:
            if isinstance(data, dict) and '@type' in data:
                types.add(data['@type'])
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and '@type' in item:
                        types.add(item['@type'])
        return list(types)
    
    def has_contact_info(self, response):
        """Check if page has contact information"""
        contact_indicators = [
            'contact', 'phone', 'email', 'address', 'location',
            'call us', 'reach us', 'get in touch'
        ]
        page_text = ' '.join(response.css('body *::text').getall()).lower()
        return any(indicator in page_text for indicator in contact_indicators)
    
    def has_address_info(self, response):
        """Check if page has address information"""
        page_text = ' '.join(response.css('body *::text').getall())
        # Look for Australian address patterns
        address_patterns = [
            r'\d+\s+[A-Za-z\s]+(?:Street|St|Road|Rd|Avenue|Ave|Drive|Dr|Lane|Ln|Court|Ct|Place|Pl)',
            r'Sydney.*NSW.*\d{4}',
            r'NSW.*\d{4}',
            r'Australia.*\d{4}'
        ]
        return any(re.search(pattern, page_text) for pattern in address_patterns)