import scrapy
import json
import re
from urllib.parse import urljoin, urlparse

class SydneyCoachCharterSpider(scrapy.Spider):
    name = 'sydney_coach_charter'
    allowed_domains = ['sydneycoachcharter.com.au']
    start_urls = ['https://sydneycoachcharter.com.au/']
    
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'DWS-Agent/1.0 (+https://discoverwebsolutions.com.au)',
    }
    
    def __init__(self):
        self.crawled_pages = []
        self.all_internal_links = set()
        self.all_external_links = set()
        
    def parse(self, response):
        # Extract page data
        page_data = self.extract_page_data(response)
        self.crawled_pages.append(page_data)
        
        # Follow all internal links
        internal_links = response.css('a[href]::attr(href)').getall()
        for link in internal_links:
            if link and not link.startswith(('tel:', 'mailto:', 'javascript:', '#')):
                absolute_url = urljoin(response.url, link)
                parsed_url = urlparse(absolute_url)
                
                # Check if it's an internal HTTP/HTTPS link
                if parsed_url.scheme in ['http', 'https'] and parsed_url.netloc in ['sydneycoachcharter.com.au', 'www.sydneycoachcharter.com.au', '']:
                    self.all_internal_links.add(absolute_url)
                    # Follow the link if we haven't crawled it yet
                    if absolute_url not in [page['url'] for page in self.crawled_pages]:
                        yield response.follow(link, self.parse)
                elif parsed_url.scheme in ['http', 'https']:
                    self.all_external_links.add(absolute_url)
    
    def extract_page_data(self, response):
        """Extract comprehensive SEO data from a page"""
        
        # Basic page info
        page_data = {
            'url': response.url,
            'status_code': response.status,
            'page_title': response.css('title::text').get(),
            'meta_description': response.css('meta[name="description"]::attr(content)').get(),
            'meta_keywords': response.css('meta[name="keywords"]::attr(content)').get(),
            'canonical_url': response.css('link[rel="canonical"]::attr(href)').get(),
            'word_count': len(response.css('body *::text').re(r'\w+')),
        }
        
        # Meta data analysis
        if page_data['page_title']:
            page_data['title_length'] = len(page_data['page_title'])
        if page_data['meta_description']:
            page_data['meta_description_length'] = len(page_data['meta_description'])
            
        # Extract headings
        headings = {
            'h1': response.css('h1::text').getall(),
            'h2': response.css('h2::text').getall(),
            'h3': response.css('h3::text').getall(),
            'h4': response.css('h4::text').getall(),
            'h5': response.css('h5::text').getall(),
            'h6': response.css('h6::text').getall(),
        }
        page_data['headings'] = headings
        
        # Image analysis
        images = response.css('img')
        image_data = []
        for img in images:
            img_info = {
                'src': img.css('::attr(src)').get(),
                'alt': img.css('::attr(alt)').get(),
                'title': img.css('::attr(title)').get(),
                'width': img.css('::attr(width)').get(),
                'height': img.css('::attr(height)').get(),
            }
            image_data.append(img_info)
        page_data['images'] = image_data
        
        # Schema markup extraction
        schema_scripts = response.css('script[type="application/ld+json"]::text').getall()
        schemas = []
        for script in schema_scripts:
            try:
                schema_json = json.loads(script)
                schemas.append(schema_json)
            except json.JSONDecodeError:
                pass
        page_data['schema_markup'] = schemas
        
        # Links analysis
        internal_links = []
        external_links = []
        
        all_links = response.css('a[href]')
        for link in all_links:
            href = link.css('::attr(href)').get()
            anchor_text = link.css('::text').get()
            
            if href:
                absolute_url = urljoin(response.url, href)
                parsed_url = urlparse(absolute_url)
                
                link_data = {
                    'url': absolute_url,
                    'anchor_text': anchor_text,
                    'title': link.css('::attr(title)').get(),
                }
                
                if parsed_url.netloc in ['sydneycoachcharter.com.au', 'www.sydneycoachcharter.com.au', '']:
                    internal_links.append(link_data)
                else:
                    external_links.append(link_data)
        
        page_data['internal_links'] = internal_links
        page_data['external_links'] = external_links
        
        return page_data
    
    def closed(self, reason):
        """Generate comprehensive SEO report when crawl is complete"""
        
        # Create comprehensive report
        report = {
            'crawl_summary': {
                'total_pages_crawled': len(self.crawled_pages),
                'total_internal_links_found': len(self.all_internal_links),
                'total_external_links_found': len(self.all_external_links),
                'crawl_status': 'completed',
            },
            'pages': self.crawled_pages,
            'site_analysis': self.generate_site_analysis(),
            'seo_issues': self.identify_seo_issues(),
        }
        
        # Save detailed report
        with open('sydney_coach_charter_crawl_report.json', 'w') as f:
            json.dump(report, f, indent=2)
            
        # Generate markdown report
        self.generate_markdown_report(report)
        
    def generate_site_analysis(self):
        """Generate comprehensive site analysis"""
        
        analysis = {
            'url_structure': {},
            'meta_tag_analysis': {},
            'heading_structure': {},
            'image_optimization': {},
            'schema_markup': {},
        }
        
        # URL structure analysis
        urls = [page['url'] for page in self.crawled_pages]
        analysis['url_structure'] = {
            'total_pages': len(urls),
            'average_url_length': sum(len(url) for url in urls) / len(urls) if urls else 0,
            'ssl_enabled': all(url.startswith('https://') for url in urls),
        }
        
        # Meta tag analysis
        titles_with_length = [(page['page_title'], page.get('title_length', 0)) for page in self.crawled_pages if page.get('page_title')]
        descriptions_with_length = [(page['meta_description'], page.get('meta_description_length', 0)) for page in self.crawled_pages if page.get('meta_description')]
        
        analysis['meta_tag_analysis'] = {
            'pages_with_titles': len(titles_with_length),
            'pages_missing_titles': len(self.crawled_pages) - len(titles_with_length),
            'average_title_length': sum(length for _, length in titles_with_length) / len(titles_with_length) if titles_with_length else 0,
            'pages_with_descriptions': len(descriptions_with_length),
            'pages_missing_descriptions': len(self.crawled_pages) - len(descriptions_with_length),
            'average_description_length': sum(length for _, length in descriptions_with_length) / len(descriptions_with_length) if descriptions_with_length else 0,
        }
        
        # Image analysis
        total_images = sum(len(page['images']) for page in self.crawled_pages)
        images_with_alt = sum(len([img for img in page['images'] if img.get('alt')]) for page in self.crawled_pages)
        
        analysis['image_optimization'] = {
            'total_images': total_images,
            'images_with_alt_text': images_with_alt,
            'images_missing_alt_text': total_images - images_with_alt,
            'alt_text_coverage': (images_with_alt / total_images * 100) if total_images > 0 else 0,
        }
        
        # Schema markup analysis
        pages_with_schema = len([page for page in self.crawled_pages if page.get('schema_markup')])
        analysis['schema_markup'] = {
            'pages_with_schema': pages_with_schema,
            'pages_without_schema': len(self.crawled_pages) - pages_with_schema,
            'schema_coverage': (pages_with_schema / len(self.crawled_pages) * 100) if self.crawled_pages else 0,
        }
        
        return analysis
    
    def identify_seo_issues(self):
        """Identify SEO issues from crawl data"""
        
        issues = {
            'critical': [],
            'important': [],
            'minor': [],
        }
        
        # Check for critical issues
        for page in self.crawled_pages:
            url = page['url']
            
            # Missing title tags
            if not page.get('page_title'):
                issues['critical'].append(f"Missing title tag: {url}")
            
            # Missing meta descriptions
            if not page.get('meta_description'):
                issues['important'].append(f"Missing meta description: {url}")
            
            # Title too long
            if page.get('title_length', 0) > 60:
                issues['minor'].append(f"Title tag too long ({page['title_length']} chars): {url}")
            
            # Description too long
            if page.get('meta_description_length', 0) > 160:
                issues['minor'].append(f"Meta description too long ({page['meta_description_length']} chars): {url}")
            
            # Missing H1 tags
            if not page.get('headings', {}).get('h1'):
                issues['important'].append(f"Missing H1 tag: {url}")
            
            # Multiple H1 tags
            if len(page.get('headings', {}).get('h1', [])) > 1:
                issues['minor'].append(f"Multiple H1 tags found: {url}")
                
            # Images without alt text
            images_without_alt = [img for img in page.get('images', []) if not img.get('alt')]
            if images_without_alt:
                issues['important'].append(f"{len(images_without_alt)} images missing alt text: {url}")
        
        return issues
    
    def generate_markdown_report(self, report):
        """Generate a comprehensive markdown report"""
        
        markdown_content = f"""# Sydney Coach Charter - Comprehensive SEO Crawl Report

**Website**: https://sydneycoachcharter.com.au/  
**Crawl Date**: {self.crawler.stats.start_time.strftime('%d/%m/%Y')}  
**Pages Crawled**: {report['crawl_summary']['total_pages_crawled']}

## Executive Summary

### Site Structure
- **Total Pages**: {report['crawl_summary']['total_pages_crawled']}
- **Internal Links**: {report['crawl_summary']['total_internal_links_found']}
- **External Links**: {report['crawl_summary']['total_external_links_found']}

### SEO Health Overview
- **Critical Issues**: {len(report['seo_issues']['critical'])}
- **Important Issues**: {len(report['seo_issues']['important'])}
- **Minor Issues**: {len(report['seo_issues']['minor'])}

## Page-by-Page Analysis

"""
        
        for page in report['pages']:
            markdown_content += f"""### {page['url']}

**Status**: {page['status_code']}  
**Title**: {page.get('page_title', 'MISSING')} ({page.get('title_length', 0)} chars)  
**Meta Description**: {page.get('meta_description', 'MISSING')} ({page.get('meta_description_length', 0)} chars)  
**Word Count**: {page.get('word_count', 0)}

#### Headings Structure
"""
            
            for heading_level, headings in page.get('headings', {}).items():
                if headings:
                    markdown_content += f"- **{heading_level.upper()}**: {len(headings)} found\n"
                    for heading in headings[:3]:  # Show first 3
                        markdown_content += f"  - {heading}\n"
            
            markdown_content += f"""
#### Images Analysis
- **Total Images**: {len(page.get('images', []))}
- **Images with Alt Text**: {len([img for img in page.get('images', []) if img.get('alt')])}
- **Missing Alt Text**: {len([img for img in page.get('images', []) if not img.get('alt')])}

#### Schema Markup
- **Schema Types Found**: {len(page.get('schema_markup', []))}

---

"""

        # Add SEO issues section
        markdown_content += """## SEO Issues Identified

### Critical Issues
"""
        for issue in report['seo_issues']['critical']:
            markdown_content += f"- ❌ {issue}\n"
            
        markdown_content += """
### Important Issues
"""
        for issue in report['seo_issues']['important']:
            markdown_content += f"- ⚠️ {issue}\n"
            
        markdown_content += """
### Minor Issues
"""
        for issue in report['seo_issues']['minor']:
            markdown_content += f"- ℹ️ {issue}\n"
        
        # Save markdown report
        with open('sydney_coach_charter_seo_report.md', 'w', encoding='utf-8') as f:
            f.write(markdown_content)