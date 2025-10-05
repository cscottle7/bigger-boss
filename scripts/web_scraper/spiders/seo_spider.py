"""
Bigger Boss Agent System - SEO Data Spider
Extracts SEO metadata and technical information from websites.
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse

import scrapy
from scrapy import Request
from scrapy.http import HtmlResponse

from ..items import SEODataItem, TechnicalSEOItem


class SEOSpider(scrapy.Spider):
    """Spider for extracting SEO data from websites."""

    name = 'seo_spider'
    allowed_domains = []
    start_urls = []

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 2.0,
    }

    def __init__(self, urls=None, domains=None, mode='basic', *args, **kwargs):
        """
        Initialise SEO spider.

        Args:
            urls: Comma-separated list of URLs to scrape
            domains: Comma-separated list of allowed domains
            mode: Scraping mode ('basic', 'technical', 'comprehensive')
        """
        super().__init__(*args, **kwargs)

        self.mode = mode
        self.scraped_urls = set()

        if urls:
            self.start_urls = [url.strip() for url in urls.split(',')]

        if domains:
            self.allowed_domains = [domain.strip() for domain in domains.split(',')]
        else:
            # Extract domains from start URLs
            for url in self.start_urls:
                domain = urlparse(url).netloc
                if domain and domain not in self.allowed_domains:
                    self.allowed_domains.append(domain)

        self.logger.info(f"Initialised SEO spider with {len(self.start_urls)} URLs")
        self.logger.info(f"Allowed domains: {self.allowed_domains}")
        self.logger.info(f"Scraping mode: {self.mode}")

    def start_requests(self):
        """Generate initial requests."""
        for url in self.start_urls:
            yield Request(
                url=url,
                callback=self.parse,
                meta={'start_time': datetime.now()}
            )

    def parse(self, response: HtmlResponse):
        """Parse response and extract SEO data."""
        start_time = response.meta.get('start_time', datetime.now())
        load_time = (datetime.now() - start_time).total_seconds()

        if self.mode in ['basic', 'comprehensive']:
            # Extract basic SEO data
            yield from self._extract_seo_data(response, load_time)

        if self.mode in ['technical', 'comprehensive']:
            # Extract technical SEO data
            yield from self._extract_technical_data(response, load_time)

        # Follow internal links for comprehensive crawling
        if self.mode == 'comprehensive':
            yield from self._follow_internal_links(response)

    def _extract_seo_data(self, response: HtmlResponse, load_time: float):
        """Extract basic SEO metadata."""
        item = SEODataItem()

        item['url'] = response.url
        item['status_code'] = response.status
        item['load_time'] = load_time
        item['scraped_at'] = datetime.now().isoformat()

        # Title
        title = response.css('title::text').get()
        item['title'] = title.strip() if title else ''

        # Meta description
        meta_desc = response.css('meta[name="description"]::attr(content)').get()
        item['meta_description'] = meta_desc.strip() if meta_desc else ''

        # Meta keywords
        meta_keywords = response.css('meta[name="keywords"]::attr(content)').get()
        item['meta_keywords'] = meta_keywords.strip() if meta_keywords else ''

        # Headings
        h1_tags = response.css('h1::text').getall()
        item['h1'] = h1_tags[0].strip() if h1_tags else ''

        h2_tags = response.css('h2::text').getall()
        item['h2_tags'] = [tag.strip() for tag in h2_tags if tag.strip()]

        h3_tags = response.css('h3::text').getall()
        item['h3_tags'] = [tag.strip() for tag in h3_tags if tag.strip()]

        # Canonical URL
        canonical = response.css('link[rel="canonical"]::attr(href)').get()
        item['canonical_url'] = canonical if canonical else ''

        # Open Graph data
        og_title = response.css('meta[property="og:title"]::attr(content)').get()
        item['og_title'] = og_title.strip() if og_title else ''

        og_desc = response.css('meta[property="og:description"]::attr(content)').get()
        item['og_description'] = og_desc.strip() if og_desc else ''

        og_image = response.css('meta[property="og:image"]::attr(content)').get()
        item['og_image'] = og_image if og_image else ''

        # Robots meta
        robots = response.css('meta[name="robots"]::attr(content)').get()
        item['robots_meta'] = robots if robots else ''

        # Link analysis
        internal_links = self._count_internal_links(response)
        external_links = self._count_external_links(response)
        item['internal_links_count'] = internal_links
        item['external_links_count'] = external_links

        # Image analysis
        images = response.css('img')
        item['images_count'] = len(images)
        images_without_alt = [img for img in images if not img.css('::attr(alt)').get()]
        item['images_without_alt'] = len(images_without_alt)

        # Word count
        text_content = ' '.join(response.css('body *::text').getall())
        words = len(text_content.split())
        item['word_count'] = words

        # Schema markup
        schema_scripts = response.css('script[type="application/ld+json"]::text').getall()
        item['schema_markup'] = self._parse_schema_markup(schema_scripts)

        yield item

    def _extract_technical_data(self, response: HtmlResponse, load_time: float):
        """Extract technical SEO data."""
        item = TechnicalSEOItem()

        item['url'] = response.url
        item['page_load_time'] = load_time
        item['page_size'] = len(response.body)
        item['status_code'] = response.status
        item['scraped_at'] = datetime.now().isoformat()

        # SSL certificate check
        item['ssl_certificate'] = response.url.startswith('https://')

        # Mobile-friendly check
        viewport_meta = response.css('meta[name="viewport"]::attr(content)').get()
        item['viewport_meta'] = viewport_meta if viewport_meta else ''
        item['mobile_friendly'] = bool(viewport_meta and 'width=device-width' in viewport_meta)

        # Canonical URL
        canonical = response.css('link[rel="canonical"]::attr(href)').get()
        item['canonical_url'] = canonical if canonical else ''

        # Structured data
        schema_scripts = response.css('script[type="application/ld+json"]::text').getall()
        item['structured_data'] = self._parse_schema_markup(schema_scripts)

        # Hreflang tags
        hreflang_tags = response.css('link[rel="alternate"][hreflang]')
        hreflang_data = []
        for tag in hreflang_tags:
            hreflang_data.append({
                'hreflang': tag.css('::attr(hreflang)').get(),
                'href': tag.css('::attr(href)').get()
            })
        item['hreflang'] = hreflang_data

        # Security headers (from response headers)
        security_headers = {}
        security_header_names = [
            'strict-transport-security',
            'content-security-policy',
            'x-frame-options',
            'x-content-type-options',
            'referrer-policy'
        ]
        for header_name in security_header_names:
            if header_name in response.headers:
                security_headers[header_name] = response.headers[header_name].decode('utf-8')
        item['security_headers'] = security_headers

        # Performance metrics
        performance_metrics = {
            'response_size': len(response.body),
            'html_size': len(response.text),
            'load_time': load_time,
            'images_count': len(response.css('img')),
            'stylesheets_count': len(response.css('link[rel="stylesheet"]')),
            'scripts_count': len(response.css('script[src]')),
        }
        item['performance_metrics'] = performance_metrics

        # Basic accessibility checks
        accessibility_issues = []

        # Check for images without alt text
        images_no_alt = response.css('img:not([alt])')
        if images_no_alt:
            accessibility_issues.append(f"{len(images_no_alt)} images missing alt text")

        # Check for empty alt text
        images_empty_alt = response.css('img[alt=""]')
        if images_empty_alt:
            accessibility_issues.append(f"{len(images_empty_alt)} images with empty alt text")

        # Check for missing h1 tag
        h1_tags = response.css('h1')
        if not h1_tags:
            accessibility_issues.append("No H1 tag found")
        elif len(h1_tags) > 1:
            accessibility_issues.append(f"Multiple H1 tags found ({len(h1_tags)})")

        item['accessibility_issues'] = accessibility_issues

        yield item

    def _count_internal_links(self, response: HtmlResponse) -> int:
        """Count internal links on the page."""
        domain = urlparse(response.url).netloc
        internal_count = 0

        for link in response.css('a[href]'):
            href = link.css('::attr(href)').get()
            if href:
                # Convert relative URLs to absolute
                absolute_url = urljoin(response.url, href)
                link_domain = urlparse(absolute_url).netloc

                if link_domain == domain:
                    internal_count += 1

        return internal_count

    def _count_external_links(self, response: HtmlResponse) -> int:
        """Count external links on the page."""
        domain = urlparse(response.url).netloc
        external_count = 0

        for link in response.css('a[href]'):
            href = link.css('::attr(href)').get()
            if href:
                # Skip fragment links and email/phone links
                if href.startswith('#') or href.startswith('mailto:') or href.startswith('tel:'):
                    continue

                # Convert relative URLs to absolute
                absolute_url = urljoin(response.url, href)
                link_domain = urlparse(absolute_url).netloc

                if link_domain and link_domain != domain:
                    external_count += 1

        return external_count

    def _parse_schema_markup(self, schema_scripts: List[str]) -> List[Dict]:
        """Parse JSON-LD schema markup."""
        schema_data = []

        for script in schema_scripts:
            try:
                data = json.loads(script.strip())
                schema_data.append(data)
            except json.JSONDecodeError:
                self.logger.warning(f"Invalid JSON-LD schema: {script[:100]}...")
                continue

        return schema_data

    def _follow_internal_links(self, response: HtmlResponse):
        """Follow internal links for comprehensive crawling."""
        domain = urlparse(response.url).netloc

        for link in response.css('a[href]'):
            href = link.css('::attr(href)').get()
            if not href:
                continue

            # Convert to absolute URL
            absolute_url = urljoin(response.url, href)

            # Check if it's an internal link
            link_domain = urlparse(absolute_url).netloc
            if link_domain != domain:
                continue

            # Skip if already scraped
            if absolute_url in self.scraped_urls:
                continue

            # Skip certain file types
            if any(absolute_url.lower().endswith(ext) for ext in ['.pdf', '.doc', '.xls', '.zip']):
                continue

            # Skip fragment links
            if '#' in absolute_url and absolute_url.split('#')[0] in self.scraped_urls:
                continue

            self.scraped_urls.add(absolute_url)

            yield Request(
                url=absolute_url,
                callback=self.parse,
                meta={'start_time': datetime.now()}
            )