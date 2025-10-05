"""
Bigger Boss Agent System - Scrapy Pipelines
Data processing and export pipelines.
"""

import csv
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set

import pandas as pd
import scrapy
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


logger = logging.getLogger(__name__)


class ValidationPipeline:
    """Pipeline for validating scraped items."""

    def __init__(self):
        self.required_fields = {
            'SEODataItem': ['url', 'title'],
            'ContentItem': ['url', 'title', 'content'],
            'CompetitorAnalysisItem': ['url', 'domain'],
            'LocalBusinessItem': ['url', 'business_name'],
            'TechnicalSEOItem': ['url', 'status_code'],
        }

    def process_item(self, item, spider):
        """Validate item fields."""
        adapter = ItemAdapter(item)
        item_type = type(item).__name__

        # Check required fields
        if item_type in self.required_fields:
            for field in self.required_fields[item_type]:
                if not adapter.get(field):
                    raise DropItem(f"Missing required field '{field}' in {item_type}")

        # Validate URL format
        url = adapter.get('url')
        if url and not (url.startswith('http://') or url.startswith('https://')):
            raise DropItem(f"Invalid URL format: {url}")

        # Add timestamp if not present
        if not adapter.get('scraped_at'):
            adapter['scraped_at'] = datetime.now().isoformat()

        spider.logger.debug(f"Validated {item_type} for {url}")
        return item


class DuplicationPipeline:
    """Pipeline for handling duplicate items."""

    def __init__(self):
        self.seen_urls: Set[str] = set()
        self.duplicate_count = 0

    def process_item(self, item, spider):
        """Filter out duplicate URLs."""
        adapter = ItemAdapter(item)
        url = adapter.get('url')

        if url in self.seen_urls:
            self.duplicate_count += 1
            spider.logger.warning(f"Duplicate item found: {url}")
            raise DropItem(f"Duplicate item: {url}")
        else:
            self.seen_urls.add(url)
            return item

    def close_spider(self, spider):
        """Log statistics when spider closes."""
        spider.logger.info(f"Filtered {self.duplicate_count} duplicate items")


class CleaningPipeline:
    """Pipeline for cleaning and normalising data."""

    def process_item(self, item, spider):
        """Clean and normalise item data."""
        adapter = ItemAdapter(item)

        # Clean text fields
        text_fields = ['title', 'meta_description', 'content', 'description']
        for field in text_fields:
            value = adapter.get(field)
            if value and isinstance(value, str):
                # Remove extra whitespace and normalise
                cleaned_value = ' '.join(value.split())
                # Remove common artifacts
                cleaned_value = self._remove_artifacts(cleaned_value)
                adapter[field] = cleaned_value

        # Normalise lists
        list_fields = ['h2_tags', 'h3_tags', 'services', 'categories']
        for field in list_fields:
            value = adapter.get(field)
            if value and isinstance(value, list):
                # Remove empty strings and strip whitespace
                cleaned_list = [item.strip() for item in value if item and item.strip()]
                adapter[field] = cleaned_list

        # Convert numeric strings to numbers
        numeric_fields = ['word_count', 'internal_links_count', 'external_links_count',
                         'images_count', 'rating', 'reviews_count']
        for field in numeric_fields:
            value = adapter.get(field)
            if value and isinstance(value, str) and value.isdigit():
                adapter[field] = int(value)

        return item

    def _remove_artifacts(self, text: str) -> str:
        """Remove common text artifacts from scraped content."""
        # Remove common cookie notices and privacy texts
        artifacts = [
            'This site uses cookies',
            'We use cookies',
            'Accept cookies',
            'Privacy policy',
            'Terms and conditions',
            'GDPR compliance',
        ]

        cleaned_text = text
        for artifact in artifacts:
            cleaned_text = cleaned_text.replace(artifact, '')

        return cleaned_text.strip()


class ExportPipeline:
    """Pipeline for exporting data to various formats."""

    def __init__(self):
        self.items: List[Dict] = []
        self.output_dir = Path('output')
        self.output_dir.mkdir(exist_ok=True)

    def process_item(self, item, spider):
        """Collect items for export."""
        adapter = ItemAdapter(item)
        self.items.append(dict(adapter))
        return item

    def close_spider(self, spider):
        """Export collected items when spider closes."""
        if not self.items:
            spider.logger.info("No items to export")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        spider_name = spider.name

        # Export to JSON
        self._export_json(spider_name, timestamp)

        # Export to CSV
        self._export_csv(spider_name, timestamp)

        # Export to Excel
        self._export_excel(spider_name, timestamp)

        spider.logger.info(f"Exported {len(self.items)} items to multiple formats")

    def _export_json(self, spider_name: str, timestamp: str):
        """Export to JSON format."""
        filename = self.output_dir / f"{spider_name}_{timestamp}.json"

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.items, f, indent=2, ensure_ascii=False, default=str)

        logger.info(f"Exported to JSON: {filename}")

    def _export_csv(self, spider_name: str, timestamp: str):
        """Export to CSV format."""
        filename = self.output_dir / f"{spider_name}_{timestamp}.csv"

        if not self.items:
            return

        # Get all unique field names
        fieldnames = set()
        for item in self.items:
            fieldnames.update(item.keys())

        fieldnames = sorted(list(fieldnames))

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for item in self.items:
                # Handle list/dict fields for CSV
                csv_item = {}
                for key, value in item.items():
                    if isinstance(value, (list, dict)):
                        csv_item[key] = json.dumps(value, ensure_ascii=False)
                    else:
                        csv_item[key] = value
                writer.writerow(csv_item)

        logger.info(f"Exported to CSV: {filename}")

    def _export_excel(self, spider_name: str, timestamp: str):
        """Export to Excel format."""
        filename = self.output_dir / f"{spider_name}_{timestamp}.xlsx"

        try:
            # Convert to DataFrame
            df = pd.DataFrame(self.items)

            # Handle complex data types
            for column in df.columns:
                if df[column].dtype == 'object':
                    df[column] = df[column].astype(str)

            # Export to Excel
            df.to_excel(filename, index=False, engine='openpyxl')
            logger.info(f"Exported to Excel: {filename}")

        except Exception as e:
            logger.error(f"Failed to export Excel: {e}")


class ClientDataPipeline:
    """Pipeline for organising data by client projects."""

    def __init__(self):
        self.client_items: Dict[str, List] = {}

    def process_item(self, item, spider):
        """Organise items by client."""
        adapter = ItemAdapter(item)

        # Try to determine client from URL or spider settings
        client = self._determine_client(adapter, spider)

        if client not in self.client_items:
            self.client_items[client] = []

        self.client_items[client].append(dict(adapter))
        return item

    def close_spider(self, spider):
        """Export client-specific data."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        for client, items in self.client_items.items():
            if not items:
                continue

            # Create client-specific directory
            client_dir = Path(f'clients/{client}/technical')
            client_dir.mkdir(parents=True, exist_ok=True)

            # Export client data
            filename = client_dir / f"scraped_data_{timestamp}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    'client': client,
                    'scraped_at': timestamp,
                    'total_items': len(items),
                    'data': items
                }, f, indent=2, ensure_ascii=False, default=str)

            spider.logger.info(f"Exported {len(items)} items for client {client}")

    def _determine_client(self, adapter: ItemAdapter, spider) -> str:
        """Determine client from item data or spider settings."""
        url = adapter.get('url', '')

        # Extract domain from URL
        if url:
            from urllib.parse import urlparse
            domain = urlparse(url).netloc.lower()

            # Remove www. prefix
            if domain.startswith('www.'):
                domain = domain[4:]

            # Replace dots with underscores for folder names
            return domain.replace('.', '_')

        # Fallback to spider name or default
        return getattr(spider, 'client_name', spider.name)