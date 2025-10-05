"""
Bigger Boss Agent System - Competitor Analysis Spider
Comprehensive competitor website analysis for strategic insights.
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Set
from urllib.parse import urljoin, urlparse

import scrapy
from scrapy import Request
from scrapy.http import HtmlResponse

from ..items import CompetitorAnalysisItem


class CompetitorSpider(scrapy.Spider):
    """Spider for comprehensive competitor analysis."""

    name = 'competitor_spider'
    allowed_domains = []
    start_urls = []

    custom_settings = {
        'DOWNLOAD_DELAY': 3,  # Be more respectful for competitor analysis
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.0,
        'DEPTH_LIMIT': 3,  # Limit crawling depth
    }

    def __init__(self, urls=None, domains=None, analysis_depth='standard', *args, **kwargs):
        """
        Initialise competitor spider.

        Args:
            urls: Comma-separated list of competitor URLs
            domains: Comma-separated list of allowed domains
            analysis_depth: Analysis depth ('basic', 'standard', 'comprehensive')
        """
        super().__init__(*args, **kwargs)

        self.analysis_depth = analysis_depth
        self.scraped_pages: Dict[str, Set[str]] = {}  # domain -> set of scraped URLs
        self.competitor_data: Dict[str, Dict] = {}

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

        # Initialise tracking for each domain
        for domain in self.allowed_domains:
            self.scraped_pages[domain] = set()
            self.competitor_data[domain] = {
                'pages_scraped': 0,
                'services': set(),
                'locations': set(),
                'keywords': set(),
                'content_themes': set(),
            }

        self.logger.info(f"Initialised competitor spider with {len(self.start_urls)} URLs")
        self.logger.info(f"Analysis depth: {self.analysis_depth}")

    def start_requests(self):
        """Generate initial requests."""
        for url in self.start_urls:
            yield Request(
                url=url,
                callback=self.parse,
                meta={
                    'start_time': datetime.now(),
                    'page_type': 'homepage',
                    'depth': 0
                }
            )

    def parse(self, response: HtmlResponse):
        """Parse competitor page and extract business intelligence."""
        domain = urlparse(response.url).netloc
        page_type = response.meta.get('page_type', 'general')
        depth = response.meta.get('depth', 0)

        # Track scraped pages
        self.scraped_pages[domain].add(response.url)
        self.competitor_data[domain]['pages_scraped'] += 1

        # Extract competitor data
        item = CompetitorAnalysisItem()

        item['url'] = response.url
        item['domain'] = domain
        item['scraped_at'] = datetime.now().isoformat()

        # Business identification
        item['business_name'] = self._extract_business_name(response)

        # Services analysis
        services = self._extract_services(response)
        item['services'] = services
        self.competitor_data[domain]['services'].update(services)

        # Location analysis
        locations = self._extract_locations(response)
        item['locations'] = locations
        self.competitor_data[domain]['locations'].update(locations)

        # Contact information
        item['contact_info'] = self._extract_contact_info(response)

        # Social media presence
        item['social_media'] = self._extract_social_media(response)

        # Pricing information
        item['pricing_info'] = self._extract_pricing_info(response)

        # Testimonials and reviews
        item['testimonials'] = self._extract_testimonials(response)

        # Case studies
        item['case_studies'] = self._extract_case_studies(response)

        # Blog posts and content
        item['blog_posts'] = self._extract_blog_posts(response)

        # Technology stack detection
        item['technology_stack'] = self._detect_technology_stack(response)

        # SEO metrics
        item['seo_metrics'] = self._analyse_seo_metrics(response)

        # Content themes analysis
        content_themes = self._analyse_content_themes(response)
        item['content_themes'] = content_themes
        self.competitor_data[domain]['content_themes'].update(content_themes)

        # Unique selling propositions
        item['unique_selling_points'] = self._extract_usps(response)

        # Target keywords analysis
        target_keywords = self._analyse_target_keywords(response)
        item['target_keywords'] = target_keywords
        self.competitor_data[domain]['keywords'].update(target_keywords)

        yield item

        # Follow important internal links based on analysis depth
        if depth < self._get_max_depth():
            yield from self._follow_strategic_links(response, depth)

    def _extract_business_name(self, response: HtmlResponse) -> str:
        """Extract business name from various sources."""
        # Try title tag first
        title = response.css('title::text').get()
        if title:
            # Clean common suffixes
            business_name = title.strip()
            for suffix in [' - Home', ' | Home', ' - Homepage', ' Homepage']:
                business_name = business_name.replace(suffix, '')
            return business_name

        # Try logo alt text
        logo_alt = response.css('img[alt*="logo" i], .logo img::attr(alt)').get()
        if logo_alt:
            return logo_alt.strip()

        # Try header text
        header_text = response.css('h1::text, .company-name::text, .business-name::text').get()
        if header_text:
            return header_text.strip()

        # Fallback to domain
        return urlparse(response.url).netloc

    def _extract_services(self, response: HtmlResponse) -> List[str]:
        """Extract services offered by the competitor."""
        services = set()

        # Common service indicators
        service_selectors = [
            'a[href*="service"]::text',
            'a[href*="solution"]::text',
            '.service-item::text',
            '.services li::text',
            'h2:contains("Service"), h3:contains("Service")',
            'nav a::text',
            '.menu-item a::text',
        ]

        for selector in service_selectors:
            elements = response.css(selector).getall()
            for element in elements:
                text = element.strip()
                if text and len(text) < 100:  # Filter out long descriptions
                    services.add(text)

        # Clean and filter services
        cleaned_services = []
        for service in services:
            # Remove common non-service terms
            if not any(term in service.lower() for term in [
                'home', 'about', 'contact', 'blog', 'news', 'privacy', 'terms'
            ]):
                cleaned_services.append(service)

        return list(cleaned_services)

    def _extract_locations(self, response: HtmlResponse) -> List[str]:
        """Extract business locations and service areas."""
        locations = set()

        # Location indicators
        location_selectors = [
            'address::text',
            '.address::text',
            '.location::text',
            '[itemtype*="PostalAddress"] *::text',
            'a[href*="location"]::text',
            'a[href*="area"]::text',
        ]

        for selector in location_selectors:
            elements = response.css(selector).getall()
            for element in elements:
                text = element.strip()
                # Look for Australian locations
                if any(state in text for state in [
                    'NSW', 'VIC', 'QLD', 'WA', 'SA', 'TAS', 'NT', 'ACT',
                    'Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide'
                ]):
                    locations.add(text)

        return list(locations)

    def _extract_contact_info(self, response: HtmlResponse) -> Dict[str, str]:
        """Extract contact information."""
        contact_info = {}

        # Phone numbers
        phone_pattern = r'(\+?61\s?[0-9\s]{8,12}|0[0-9\s]{8,10})'
        phone_matches = re.findall(phone_pattern, response.text)
        if phone_matches:
            contact_info['phone'] = phone_matches[0]

        # Email addresses
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        email_matches = re.findall(email_pattern, response.text)
        if email_matches:
            # Filter out common spam traps
            valid_emails = [email for email in email_matches
                           if not any(spam in email.lower() for spam in ['example', 'test', 'spam'])]
            if valid_emails:
                contact_info['email'] = valid_emails[0]

        # Address
        address = response.css('address::text, .address::text').get()
        if address:
            contact_info['address'] = address.strip()

        return contact_info

    def _extract_social_media(self, response: HtmlResponse) -> Dict[str, str]:
        """Extract social media links."""
        social_links = {}

        social_platforms = {
            'facebook': ['facebook.com', 'fb.com'],
            'twitter': ['twitter.com', 'x.com'],
            'linkedin': ['linkedin.com'],
            'instagram': ['instagram.com'],
            'youtube': ['youtube.com', 'youtu.be'],
            'tiktok': ['tiktok.com'],
        }

        for link in response.css('a[href]'):
            href = link.css('::attr(href)').get()
            if not href:
                continue

            for platform, domains in social_platforms.items():
                if any(domain in href.lower() for domain in domains):
                    social_links[platform] = href
                    break

        return social_links

    def _extract_pricing_info(self, response: HtmlResponse) -> List[Dict]:
        """Extract pricing information and packages."""
        pricing_info = []

        # Look for price indicators
        price_patterns = [
            r'\$[\d,]+(?:\.\d{2})?',
            r'from \$[\d,]+',
            r'starting at \$[\d,]+',
        ]

        for pattern in price_patterns:
            matches = re.findall(pattern, response.text, re.IGNORECASE)
            for match in matches:
                pricing_info.append({'price': match})

        # Look for pricing packages
        package_selectors = [
            '.pricing-package',
            '.price-table',
            '.plan',
            '.package',
        ]

        for selector in package_selectors:
            packages = response.css(selector)
            for package in packages:
                package_data = {
                    'name': package.css('.package-name::text, .plan-name::text, h3::text').get(),
                    'price': package.css('.price::text, .amount::text').get(),
                    'features': package.css('li::text').getall(),
                }
                if package_data['name'] or package_data['price']:
                    pricing_info.append(package_data)

        return pricing_info

    def _extract_testimonials(self, response: HtmlResponse) -> List[Dict]:
        """Extract customer testimonials."""
        testimonials = []

        testimonial_selectors = [
            '.testimonial',
            '.review',
            '.client-review',
            '.customer-review',
        ]

        for selector in testimonial_selectors:
            items = response.css(selector)
            for item in items:
                testimonial = {
                    'text': item.css('.testimonial-text::text, .review-text::text, p::text').get(),
                    'author': item.css('.author::text, .customer-name::text, .reviewer::text').get(),
                    'company': item.css('.company::text, .business::text').get(),
                    'rating': item.css('.rating::attr(data-rating), .stars::attr(data-rating)').get(),
                }

                if testimonial['text']:
                    testimonials.append(testimonial)

        return testimonials

    def _extract_case_studies(self, response: HtmlResponse) -> List[Dict]:
        """Extract case studies and project examples."""
        case_studies = []

        # Look for case study links and content
        case_study_links = response.css('a[href*="case-study"], a[href*="portfolio"], a[href*="project"]')

        for link in case_study_links:
            case_study = {
                'title': link.css('::text').get(),
                'url': urljoin(response.url, link.css('::attr(href)').get()),
            }
            if case_study['title']:
                case_studies.append(case_study)

        return case_studies

    def _extract_blog_posts(self, response: HtmlResponse) -> List[Dict]:
        """Extract blog posts and content marketing."""
        blog_posts = []

        blog_selectors = [
            '.blog-post',
            '.article',
            '.news-item',
            'article',
        ]

        for selector in blog_selectors:
            posts = response.css(selector)
            for post in posts:
                blog_post = {
                    'title': post.css('h2::text, h3::text, .title::text').get(),
                    'excerpt': post.css('.excerpt::text, .summary::text').get(),
                    'url': post.css('a::attr(href)').get(),
                    'date': post.css('.date::text, .published::text').get(),
                }

                if blog_post['title']:
                    blog_posts.append(blog_post)

        return blog_posts

    def _detect_technology_stack(self, response: HtmlResponse) -> Dict[str, List[str]]:
        """Detect technology stack used by the competitor."""
        tech_stack = {
            'cms': [],
            'analytics': [],
            'frameworks': [],
            'libraries': [],
            'plugins': [],
        }

        # Check for CMS indicators
        cms_indicators = {
            'WordPress': ['wp-content', 'wp-includes', '/wp-json/'],
            'Shopify': ['cdn.shopify.com', 'shopify.com'],
            'Squarespace': ['squarespace.com', 'static1.squarespace.com'],
            'Wix': ['wix.com', 'wixstatic.com'],
            'Drupal': ['drupal', '/sites/default/'],
            'Joomla': ['joomla', '/media/jui/'],
        }

        page_content = response.text.lower()
        for cms, indicators in cms_indicators.items():
            if any(indicator.lower() in page_content for indicator in indicators):
                tech_stack['cms'].append(cms)

        # Check for analytics tools
        analytics_tools = {
            'Google Analytics': ['google-analytics.com', 'gtag(', 'ga('],
            'Google Tag Manager': ['googletagmanager.com', 'gtm.js'],
            'Facebook Pixel': ['facebook.net/tr', 'fbevents.js'],
            'Hotjar': ['hotjar.com'],
            'Mixpanel': ['mixpanel.com'],
        }

        for tool, indicators in analytics_tools.items():
            if any(indicator in page_content for indicator in indicators):
                tech_stack['analytics'].append(tool)

        # Check for JavaScript frameworks/libraries
        js_frameworks = {
            'React': ['react.js', 'react.min.js'],
            'Vue.js': ['vue.js', 'vue.min.js'],
            'Angular': ['angular.js', 'angular.min.js'],
            'jQuery': ['jquery.js', 'jquery.min.js'],
            'Bootstrap': ['bootstrap.css', 'bootstrap.min.css'],
        }

        for framework, indicators in js_frameworks.items():
            if any(indicator in page_content for indicator in indicators):
                tech_stack['frameworks'].append(framework)

        return tech_stack

    def _analyse_seo_metrics(self, response: HtmlResponse) -> Dict[str, any]:
        """Analyse basic SEO metrics."""
        metrics = {}

        # Title tag analysis
        title = response.css('title::text').get()
        metrics['title_length'] = len(title) if title else 0

        # Meta description analysis
        meta_desc = response.css('meta[name="description"]::attr(content)').get()
        metrics['meta_description_length'] = len(meta_desc) if meta_desc else 0

        # Heading structure
        h1_count = len(response.css('h1'))
        h2_count = len(response.css('h2'))
        h3_count = len(response.css('h3'))

        metrics['heading_structure'] = {
            'h1': h1_count,
            'h2': h2_count,
            'h3': h3_count,
        }

        # Internal/external links
        domain = urlparse(response.url).netloc
        internal_links = 0
        external_links = 0

        for link in response.css('a[href]'):
            href = link.css('::attr(href)').get()
            if href:
                absolute_url = urljoin(response.url, href)
                link_domain = urlparse(absolute_url).netloc

                if link_domain == domain:
                    internal_links += 1
                elif link_domain:
                    external_links += 1

        metrics['link_analysis'] = {
            'internal': internal_links,
            'external': external_links,
        }

        # Image optimisation
        images = response.css('img')
        images_with_alt = response.css('img[alt]')
        metrics['image_optimisation'] = {
            'total_images': len(images),
            'images_with_alt': len(images_with_alt),
            'alt_text_usage': len(images_with_alt) / len(images) * 100 if images else 0,
        }

        return metrics

    def _analyse_content_themes(self, response: HtmlResponse) -> List[str]:
        """Analyse content themes and topics."""
        themes = set()

        # Extract text content
        text_content = ' '.join(response.css('p::text, h1::text, h2::text, h3::text').getall())

        # Common business themes (could be expanded with NLP)
        theme_keywords = {
            'digital marketing': ['digital marketing', 'seo', 'social media', 'google ads'],
            'web development': ['web development', 'website design', 'responsive design'],
            'ecommerce': ['ecommerce', 'online store', 'shopping cart', 'payment'],
            'consulting': ['consulting', 'strategy', 'advice', 'expertise'],
            'healthcare': ['health', 'medical', 'doctor', 'clinic', 'patient'],
            'legal': ['legal', 'law', 'lawyer', 'attorney', 'court'],
            'education': ['education', 'training', 'course', 'learning'],
            'finance': ['finance', 'accounting', 'tax', 'financial'],
        }

        text_lower = text_content.lower()
        for theme, keywords in theme_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                themes.add(theme)

        return list(themes)

    def _extract_usps(self, response: HtmlResponse) -> List[str]:
        """Extract unique selling propositions."""
        usps = []

        # Common USP indicators
        usp_selectors = [
            '.usp::text',
            '.unique-selling-point::text',
            '.why-choose-us li::text',
            '.benefits li::text',
            '.advantages li::text',
        ]

        for selector in usp_selectors:
            elements = response.css(selector).getall()
            for element in elements:
                text = element.strip()
                if text and len(text) < 200:  # Filter out long descriptions
                    usps.append(text)

        return usps

    def _analyse_target_keywords(self, response: HtmlResponse) -> List[str]:
        """Analyse target keywords from content."""
        keywords = set()

        # Extract keywords from key areas
        key_content = []

        # Title tag
        title = response.css('title::text').get()
        if title:
            key_content.append(title)

        # Meta description
        meta_desc = response.css('meta[name="description"]::attr(content)').get()
        if meta_desc:
            key_content.append(meta_desc)

        # Headings
        headings = response.css('h1::text, h2::text, h3::text').getall()
        key_content.extend(headings)

        # Extract potential keywords from content
        combined_content = ' '.join(key_content).lower()

        # Simple keyword extraction (could be enhanced with NLP)
        words = re.findall(r'\b\w{3,}\b', combined_content)

        # Filter common stop words
        stop_words = {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had',
            'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his',
            'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy',
        }

        meaningful_words = [word for word in words if word not in stop_words and len(word) > 3]

        # Get most common words as potential keywords
        from collections import Counter
        word_counts = Counter(meaningful_words)
        keywords.update([word for word, count in word_counts.most_common(20) if count > 1])

        return list(keywords)

    def _follow_strategic_links(self, response: HtmlResponse, current_depth: int):
        """Follow strategically important internal links."""
        domain = urlparse(response.url).netloc

        # Priority pages to crawl
        priority_paths = [
            'about', 'services', 'products', 'solutions', 'pricing',
            'contact', 'blog', 'news', 'case-studies', 'portfolio',
            'testimonials', 'reviews'
        ]

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
            if absolute_url in self.scraped_pages[domain]:
                continue

            # Check if it's a priority page
            link_text = link.css('::text').get() or ''
            url_path = urlparse(absolute_url).path.lower()

            is_priority = any(
                priority in url_path or priority in link_text.lower()
                for priority in priority_paths
            )

            if is_priority or current_depth == 0:  # Always follow from homepage
                yield Request(
                    url=absolute_url,
                    callback=self.parse,
                    meta={
                        'start_time': datetime.now(),
                        'page_type': self._classify_page_type(absolute_url, link_text),
                        'depth': current_depth + 1
                    }
                )

    def _classify_page_type(self, url: str, link_text: str) -> str:
        """Classify the type of page based on URL and link text."""
        url_lower = url.lower()
        text_lower = link_text.lower()

        page_types = {
            'about': ['about', 'who-we-are', 'our-story'],
            'services': ['service', 'solution', 'what-we-do'],
            'products': ['product', 'shop', 'store'],
            'pricing': ['pricing', 'price', 'cost', 'fee'],
            'contact': ['contact', 'get-in-touch', 'reach-us'],
            'blog': ['blog', 'news', 'article', 'post'],
            'portfolio': ['portfolio', 'work', 'project', 'case-study'],
        }

        for page_type, keywords in page_types.items():
            if any(keyword in url_lower or keyword in text_lower for keyword in keywords):
                return page_type

        return 'general'

    def _get_max_depth(self) -> int:
        """Get maximum crawling depth based on analysis depth setting."""
        depth_limits = {
            'basic': 1,
            'standard': 2,
            'comprehensive': 3,
        }
        return depth_limits.get(self.analysis_depth, 2)

    def closed(self, reason):
        """Spider closed callback with summary statistics."""
        self.logger.info("Competitor analysis completed")

        for domain, data in self.competitor_data.items():
            self.logger.info(f"Domain: {domain}")
            self.logger.info(f"  Pages scraped: {data['pages_scraped']}")
            self.logger.info(f"  Services found: {len(data['services'])}")
            self.logger.info(f"  Locations found: {len(data['locations'])}")
            self.logger.info(f"  Content themes: {len(data['content_themes'])}")
            self.logger.info(f"  Keywords identified: {len(data['keywords'])}")