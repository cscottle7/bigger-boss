"""
Bigger Boss Agent System - Scrapy Settings Configuration
Professional web scraping with respectful crawling practices.
"""

BOT_NAME = 'bigger_boss_scraper'

SPIDER_MODULES = ['web_scraper.spiders']
NEWSPIDER_MODULE = 'web_scraper.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure a delay for requests (be respectful)
DOWNLOAD_DELAY = 2
RANDOMIZE_DOWNLOAD_DELAY = 0.5

# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 3
CONCURRENT_REQUESTS_PER_IP = 3

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-AU,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
    'User-Agent': 'Bigger-Boss-Agent/1.0 (+https://bigger-boss.com.au/bot)',
}

# Enable or disable spider middlewares
SPIDER_MIDDLEWARES = {
    'web_scraper.middlewares.BiggerBossSpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    'web_scraper.middlewares.BiggerBossDownloaderMiddleware': 543,
    'scrapy_playwright.middlewares.PlaywrightMiddleware': 585,
}

# Configure item pipelines
ITEM_PIPELINES = {
    'web_scraper.pipelines.ValidationPipeline': 300,
    'web_scraper.pipelines.DuplicationPipeline': 400,
    'web_scraper.pipelines.ExportPipeline': 500,
}

# Configure Playwright
PLAYWRIGHT_BROWSER_TYPE = 'chromium'
PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": True,
    "timeout": 30000,
}

# AutoThrottle settings
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 3.0
AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 3600  # 1 hour
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = [500, 502, 503, 504, 408, 429]

# Retry settings
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]

# Feed settings for output
FEEDS = {
    'output/scraped_data_%(time)s.json': {
        'format': 'json',
        'encoding': 'utf8',
        'store_empty': False,
        'fields': None,
        'indent': 2,
    },
    'output/scraped_data_%(time)s.csv': {
        'format': 'csv',
        'encoding': 'utf8',
        'store_empty': False,
    },
}

# Logging
LOG_LEVEL = 'INFO'
LOG_FILE = 'logs/scrapy.log'

# Request fingerprinting implementation
REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'

# Set settings whose default value is deprecated
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'