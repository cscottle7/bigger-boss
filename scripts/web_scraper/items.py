"""
Bigger Boss Agent System - Scrapy Items Definition
Data structures for scraped content.
"""

import scrapy
from itemloaders.processors import Compose, MapCompose, TakeFirst
from w3lib.html import remove_tags


class SEODataItem(scrapy.Item):
    """Item for SEO metadata extraction."""

    url = scrapy.Field()
    title = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst()
    )
    meta_description = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst()
    )
    h1 = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst()
    )
    h2_tags = scrapy.Field()
    h3_tags = scrapy.Field()
    meta_keywords = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst()
    )
    canonical_url = scrapy.Field()
    og_title = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst()
    )
    og_description = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst()
    )
    og_image = scrapy.Field()
    schema_markup = scrapy.Field()
    robots_meta = scrapy.Field()
    internal_links_count = scrapy.Field()
    external_links_count = scrapy.Field()
    images_count = scrapy.Field()
    images_without_alt = scrapy.Field()
    word_count = scrapy.Field()
    load_time = scrapy.Field()
    status_code = scrapy.Field()
    scraped_at = scrapy.Field()


class ContentItem(scrapy.Item):
    """Item for full content extraction."""

    url = scrapy.Field()
    title = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst()
    )
    content = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip)
    )
    headings = scrapy.Field()
    paragraphs = scrapy.Field()
    lists = scrapy.Field()
    images = scrapy.Field()
    links = scrapy.Field()
    tables = scrapy.Field()
    forms = scrapy.Field()
    meta_data = scrapy.Field()
    structured_data = scrapy.Field()
    author = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst()
    )
    published_date = scrapy.Field()
    modified_date = scrapy.Field()
    category = scrapy.Field()
    tags = scrapy.Field()
    word_count = scrapy.Field()
    reading_time = scrapy.Field()
    language = scrapy.Field()
    scraped_at = scrapy.Field()


class CompetitorAnalysisItem(scrapy.Item):
    """Item for competitor website analysis."""

    url = scrapy.Field()
    domain = scrapy.Field()
    business_name = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst()
    )
    services = scrapy.Field()
    locations = scrapy.Field()
    contact_info = scrapy.Field()
    social_media = scrapy.Field()
    pricing_info = scrapy.Field()
    testimonials = scrapy.Field()
    case_studies = scrapy.Field()
    blog_posts = scrapy.Field()
    technology_stack = scrapy.Field()
    seo_metrics = scrapy.Field()
    content_themes = scrapy.Field()
    unique_selling_points = scrapy.Field()
    target_keywords = scrapy.Field()
    scraped_at = scrapy.Field()


class LocalBusinessItem(scrapy.Item):
    """Item for local business information extraction."""

    url = scrapy.Field()
    business_name = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst()
    )
    address = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()
    website = scrapy.Field()
    hours = scrapy.Field()
    services = scrapy.Field()
    description = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip)
    )
    reviews_count = scrapy.Field()
    rating = scrapy.Field()
    price_range = scrapy.Field()
    categories = scrapy.Field()
    images = scrapy.Field()
    social_profiles = scrapy.Field()
    schema_org_data = scrapy.Field()
    scraped_at = scrapy.Field()


class TechnicalSEOItem(scrapy.Item):
    """Item for technical SEO analysis."""

    url = scrapy.Field()
    page_load_time = scrapy.Field()
    page_size = scrapy.Field()
    status_code = scrapy.Field()
    redirect_chain = scrapy.Field()
    ssl_certificate = scrapy.Field()
    mobile_friendly = scrapy.Field()
    viewport_meta = scrapy.Field()
    structured_data = scrapy.Field()
    hreflang = scrapy.Field()
    canonical_url = scrapy.Field()
    robots_txt = scrapy.Field()
    sitemap = scrapy.Field()
    core_web_vitals = scrapy.Field()
    lighthouse_score = scrapy.Field()
    security_headers = scrapy.Field()
    performance_metrics = scrapy.Field()
    accessibility_issues = scrapy.Field()
    scraped_at = scrapy.Field()