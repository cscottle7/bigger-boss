"""
Bigger Boss Agent System - Scrapy Middlewares
Custom middleware for enhanced crawling capabilities.
"""

import random
import time
from datetime import datetime
from typing import Dict, List, Optional

import scrapy
from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.http import HtmlResponse, Request
from scrapy.spiders import Spider


class BiggerBossSpiderMiddleware:
    """Spider middleware for request/response processing."""

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        """Process spider input (response)."""
        return None

    def process_spider_output(self, response, result, spider):
        """Process spider output (items and requests)."""
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        """Handle spider exceptions."""
        spider.logger.error(f"Spider exception: {exception} for {response.url}")
        return []

    def process_start_requests(self, start_requests, spider):
        """Process start requests."""
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        """Called when spider is opened."""
        spider.logger.info(f'Spider opened: {spider.name}')


class BiggerBossDownloaderMiddleware:
    """Downloader middleware for request/response processing."""

    def __init__(self):
        self.user_agents = [
            'Bigger-Boss-Agent/1.0 (+https://bigger-boss.com.au/bot)',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        ]

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request: Request, spider: Spider):
        """Process outgoing request."""
        # Rotate User-Agent headers
        request.headers['User-Agent'] = random.choice(self.user_agents)

        # Add Accept-Language header
        request.headers['Accept-Language'] = 'en-AU,en;q=0.9,en-GB;q=0.8,en-US;q=0.7'

        # Add random delay to appear more human-like
        if hasattr(spider, 'custom_delay') and spider.custom_delay:
            delay = random.uniform(1, 3)
            time.sleep(delay)

        return None

    def process_response(self, request: Request, response: HtmlResponse, spider: Spider):
        """Process incoming response."""
        # Log response details
        spider.logger.debug(
            f"Response {response.status} for {request.url} "
            f"(size: {len(response.body)} bytes)"
        )

        # Handle specific status codes
        if response.status in [403, 429]:
            spider.logger.warning(f"Rate limited or blocked: {response.status} for {request.url}")
            # Increase delay for subsequent requests
            spider.crawler.engine.downloader.delay = min(
                spider.crawler.engine.downloader.delay * 2,
                30  # Max 30 seconds
            )

        return response

    def process_exception(self, request: Request, exception: Exception, spider: Spider):
        """Process request exceptions."""
        spider.logger.error(f"Request exception: {exception} for {request.url}")
        return None

    def spider_opened(self, spider):
        """Called when spider is opened."""
        spider.logger.info(f'Downloader middleware enabled for: {spider.name}')


class RateLimitMiddleware:
    """Advanced rate limiting middleware."""

    def __init__(self, delay_range: tuple = (1, 3), respect_retry_after: bool = True):
        self.delay_range = delay_range
        self.respect_retry_after = respect_retry_after
        self.domain_delays: Dict[str, float] = {}
        self.last_request_time: Dict[str, float] = {}

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        delay_range = (
            settings.getfloat('RATE_LIMIT_MIN_DELAY', 1.0),
            settings.getfloat('RATE_LIMIT_MAX_DELAY', 3.0)
        )
        respect_retry_after = settings.getbool('RATE_LIMIT_RESPECT_RETRY_AFTER', True)

        return cls(delay_range, respect_retry_after)

    def process_request(self, request: Request, spider: Spider):
        """Apply rate limiting per domain."""
        domain = self._get_domain(request.url)
        current_time = time.time()

        # Check if we need to wait
        if domain in self.last_request_time:
            time_since_last = current_time - self.last_request_time[domain]
            min_delay = self.domain_delays.get(domain, self.delay_range[0])

            if time_since_last < min_delay:
                sleep_time = min_delay - time_since_last
                spider.logger.debug(f"Rate limiting: sleeping {sleep_time:.2f}s for {domain}")
                time.sleep(sleep_time)

        self.last_request_time[domain] = time.time()
        return None

    def process_response(self, request: Request, response: HtmlResponse, spider: Spider):
        """Adjust rate limiting based on response."""
        domain = self._get_domain(request.url)

        # Handle Retry-After header
        if self.respect_retry_after and 'Retry-After' in response.headers:
            retry_after = int(response.headers['Retry-After'])
            self.domain_delays[domain] = min(retry_after, 60)  # Max 60 seconds
            spider.logger.info(f"Retry-After received: {retry_after}s for {domain}")

        # Adjust delay based on response status
        elif response.status == 429:  # Too Many Requests
            current_delay = self.domain_delays.get(domain, self.delay_range[0])
            new_delay = min(current_delay * 2, 30)  # Max 30 seconds
            self.domain_delays[domain] = new_delay
            spider.logger.warning(f"Rate limit hit, increasing delay to {new_delay}s for {domain}")

        elif response.status == 200:  # Successful request
            # Gradually reduce delay for successful requests
            if domain in self.domain_delays and self.domain_delays[domain] > self.delay_range[1]:
                self.domain_delays[domain] *= 0.9
                spider.logger.debug(f"Reducing delay to {self.domain_delays[domain]:.2f}s for {domain}")

        return response

    def _get_domain(self, url: str) -> str:
        """Extract domain from URL."""
        from urllib.parse import urlparse
        return urlparse(url).netloc


class CacheMiddleware:
    """Custom caching middleware for scraped content."""

    def __init__(self, cache_enabled: bool = True, cache_expire_hours: int = 24):
        self.cache_enabled = cache_enabled
        self.cache_expire_hours = cache_expire_hours
        self.cache: Dict[str, Dict] = {}

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        cache_enabled = settings.getbool('CUSTOM_CACHE_ENABLED', True)
        cache_expire_hours = settings.getint('CUSTOM_CACHE_EXPIRE_HOURS', 24)

        return cls(cache_enabled, cache_expire_hours)

    def process_request(self, request: Request, spider: Spider):
        """Check cache before making request."""
        if not self.cache_enabled:
            return None

        cache_key = self._get_cache_key(request)

        if cache_key in self.cache:
            cached_data = self.cache[cache_key]
            cached_time = cached_data['timestamp']

            # Check if cache is still valid
            age_hours = (datetime.now() - cached_time).total_seconds() / 3600
            if age_hours < self.cache_expire_hours:
                spider.logger.debug(f"Cache hit for {request.url}")
                # Return cached response
                return HtmlResponse(
                    url=request.url,
                    body=cached_data['body'],
                    encoding='utf-8',
                    request=request
                )

        return None

    def process_response(self, request: Request, response: HtmlResponse, spider: Spider):
        """Cache successful responses."""
        if (self.cache_enabled and
                response.status == 200 and
                len(response.body) > 0):

            cache_key = self._get_cache_key(request)
            self.cache[cache_key] = {
                'body': response.body,
                'timestamp': datetime.now(),
                'url': request.url
            }

            spider.logger.debug(f"Cached response for {request.url}")

        return response

    def _get_cache_key(self, request: Request) -> str:
        """Generate cache key for request."""
        import hashlib
        return hashlib.md5(request.url.encode()).hexdigest()