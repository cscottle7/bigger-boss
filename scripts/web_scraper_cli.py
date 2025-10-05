#!/usr/bin/env python3
"""
Bigger Boss Agent System - Web Scraper CLI
Command-line interface for running web scraping operations.
"""

import argparse
import json
import logging
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from decouple import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WebScraperCLI:
    """Command-line interface for web scraping operations."""

    def __init__(self):
        self.scrapy_project_dir = Path(__file__).parent / 'web_scraper'
        self.output_dir = Path('output')
        self.output_dir.mkdir(exist_ok=True)

    def run_seo_spider(self, urls: List[str], mode: str = 'basic', output_format: str = 'json') -> bool:
        """
        Run SEO spider on specified URLs.

        Args:
            urls: List of URLs to scrape
            mode: Scraping mode ('basic', 'technical', 'comprehensive')
            output_format: Output format ('json', 'csv', 'excel')

        Returns:
            True if successful, False otherwise
        """
        try:
            urls_str = ','.join(urls)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            cmd = [
                'scrapy', 'crawl', 'seo_spider',
                '-a', f'urls={urls_str}',
                '-a', f'mode={mode}',
                '-s', f'FEEDS={{output/seo_data_{timestamp}.{output_format}: {{"format": "{output_format}"}}}}',
                '-L', 'INFO'
            ]

            logger.info(f"Running SEO spider with command: {' '.join(cmd)}")

            result = subprocess.run(
                cmd,
                cwd=self.scrapy_project_dir,
                capture_output=True,
                text=True,
                check=False
            )

            if result.returncode == 0:
                logger.info("SEO spider completed successfully")
                print(f"✅ SEO analysis completed. Output saved to output/seo_data_{timestamp}.{output_format}")
                return True
            else:
                logger.error(f"SEO spider failed: {result.stderr}")
                print(f"❌ SEO spider failed: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"Error running SEO spider: {e}")
            print(f"❌ Error: {str(e)}")
            return False

    def run_competitor_spider(self, urls: List[str], analysis_depth: str = 'standard', output_format: str = 'json') -> bool:
        """
        Run competitor analysis spider.

        Args:
            urls: List of competitor URLs to analyse
            analysis_depth: Analysis depth ('basic', 'standard', 'comprehensive')
            output_format: Output format ('json', 'csv', 'excel')

        Returns:
            True if successful, False otherwise
        """
        try:
            urls_str = ','.join(urls)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            cmd = [
                'scrapy', 'crawl', 'competitor_spider',
                '-a', f'urls={urls_str}',
                '-a', f'analysis_depth={analysis_depth}',
                '-s', f'FEEDS={{output/competitor_analysis_{timestamp}.{output_format}: {{"format": "{output_format}"}}}}',
                '-L', 'INFO'
            ]

            logger.info(f"Running competitor spider with command: {' '.join(cmd)}")

            result = subprocess.run(
                cmd,
                cwd=self.scrapy_project_dir,
                capture_output=True,
                text=True,
                check=False
            )

            if result.returncode == 0:
                logger.info("Competitor spider completed successfully")
                print(f"✅ Competitor analysis completed. Output saved to output/competitor_analysis_{timestamp}.{output_format}")
                return True
            else:
                logger.error(f"Competitor spider failed: {result.stderr}")
                print(f"❌ Competitor spider failed: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"Error running competitor spider: {e}")
            print(f"❌ Error: {str(e)}")
            return False

    def bulk_seo_analysis(self, urls_file: str, mode: str = 'basic') -> bool:
        """
        Run bulk SEO analysis from a file containing URLs.

        Args:
            urls_file: Path to file containing URLs (one per line)
            mode: Scraping mode ('basic', 'technical', 'comprehensive')

        Returns:
            True if successful, False otherwise
        """
        try:
            urls_path = Path(urls_file)
            if not urls_path.exists():
                logger.error(f"URLs file not found: {urls_file}")
                return False

            with open(urls_path, 'r') as f:
                urls = [line.strip() for line in f if line.strip()]

            if not urls:
                logger.error("No URLs found in file")
                return False

            logger.info(f"Starting bulk SEO analysis for {len(urls)} URLs")
            return self.run_seo_spider(urls, mode, 'json')

        except Exception as e:
            logger.error(f"Error in bulk SEO analysis: {e}")
            return False

    def generate_seo_report(self, data_file: str, output_file: Optional[str] = None) -> bool:
        """
        Generate SEO analysis report from scraped data.

        Args:
            data_file: Path to scraped data JSON file
            output_file: Output file path (optional)

        Returns:
            True if successful, False otherwise
        """
        try:
            import pandas as pd

            with open(data_file, 'r') as f:
                data = json.load(f)

            if not data:
                logger.error("No data found in file")
                return False

            # Convert to DataFrame
            df = pd.DataFrame(data)

            # Generate summary statistics
            report = {
                'summary': {
                    'total_pages': len(df),
                    'average_title_length': df['title_length'].mean() if 'title_length' in df else 0,
                    'pages_without_meta_description': len(df[df.get('meta_description', '') == '']),
                    'pages_with_multiple_h1': len(df[df.get('h1_count', 0) > 1]),
                },
                'issues': [],
                'recommendations': [],
            }

            # Identify common issues
            if 'title' in df.columns:
                long_titles = df[df['title'].str.len() > 60]
                if not long_titles.empty:
                    report['issues'].append({
                        'type': 'Long titles',
                        'count': len(long_titles),
                        'urls': long_titles['url'].tolist()[:5]  # First 5 examples
                    })

            if 'meta_description' in df.columns:
                missing_meta = df[df['meta_description'].str.len() == 0]
                if not missing_meta.empty:
                    report['issues'].append({
                        'type': 'Missing meta descriptions',
                        'count': len(missing_meta),
                        'urls': missing_meta['url'].tolist()[:5]
                    })

            # Generate recommendations
            if report['issues']:
                report['recommendations'] = [
                    "Optimize title tags to be under 60 characters",
                    "Add meta descriptions to all pages",
                    "Ensure each page has exactly one H1 tag",
                    "Optimize images with alt text",
                ]

            # Save report
            if not output_file:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = f"seo_report_{timestamp}.json"

            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)

            logger.info(f"SEO report generated: {output_file}")
            print(f"✅ SEO report generated: {output_file}")
            return True

        except Exception as e:
            logger.error(f"Error generating SEO report: {e}")
            print(f"❌ Error generating report: {str(e)}")
            return False

    def setup_scrapy_project(self) -> bool:
        """Set up Scrapy project structure if not exists."""
        try:
            if self.scrapy_project_dir.exists():
                logger.info("Scrapy project already exists")
                return True

            # Create scrapy project
            result = subprocess.run(
                ['scrapy', 'startproject', 'web_scraper'],
                cwd=self.scrapy_project_dir.parent,
                capture_output=True,
                text=True,
                check=False
            )

            if result.returncode == 0:
                logger.info("Scrapy project created successfully")
                return True
            else:
                logger.error(f"Failed to create Scrapy project: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"Error setting up Scrapy project: {e}")
            return False

    def list_available_spiders(self) -> List[str]:
        """List all available spiders."""
        try:
            result = subprocess.run(
                ['scrapy', 'list'],
                cwd=self.scrapy_project_dir,
                capture_output=True,
                text=True,
                check=False
            )

            if result.returncode == 0:
                spiders = result.stdout.strip().split('\n')
                return [spider.strip() for spider in spiders if spider.strip()]
            else:
                logger.error(f"Failed to list spiders: {result.stderr}")
                return []

        except Exception as e:
            logger.error(f"Error listing spiders: {e}")
            return []

    def validate_urls(self, urls: List[str]) -> List[str]:
        """Validate and clean URLs."""
        import re
        from urllib.parse import urlparse

        valid_urls = []
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        for url in urls:
            url = url.strip()
            if not url:
                continue

            # Add http:// if missing
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url

            # Validate URL format
            if url_pattern.match(url):
                parsed = urlparse(url)
                if parsed.netloc:
                    valid_urls.append(url)
                else:
                    logger.warning(f"Invalid URL format: {url}")
            else:
                logger.warning(f"Invalid URL format: {url}")

        return valid_urls


def main():
    """Main function for command-line interface."""
    parser = argparse.ArgumentParser(
        description='Bigger Boss Web Scraper - Professional web scraping for SEO and competitor analysis'
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # SEO analysis command
    seo_parser = subparsers.add_parser('seo', help='Run SEO analysis')
    seo_parser.add_argument('urls', nargs='+', help='URLs to analyse')
    seo_parser.add_argument(
        '--mode',
        choices=['basic', 'technical', 'comprehensive'],
        default='basic',
        help='Analysis mode (default: basic)'
    )
    seo_parser.add_argument(
        '--format',
        choices=['json', 'csv', 'excel'],
        default='json',
        help='Output format (default: json)'
    )

    # Competitor analysis command
    competitor_parser = subparsers.add_parser('competitor', help='Run competitor analysis')
    competitor_parser.add_argument('urls', nargs='+', help='Competitor URLs to analyse')
    competitor_parser.add_argument(
        '--depth',
        choices=['basic', 'standard', 'comprehensive'],
        default='standard',
        help='Analysis depth (default: standard)'
    )
    competitor_parser.add_argument(
        '--format',
        choices=['json', 'csv', 'excel'],
        default='json',
        help='Output format (default: json)'
    )

    # Bulk analysis command
    bulk_parser = subparsers.add_parser('bulk', help='Run bulk SEO analysis from file')
    bulk_parser.add_argument('urls_file', help='File containing URLs (one per line)')
    bulk_parser.add_argument(
        '--mode',
        choices=['basic', 'technical', 'comprehensive'],
        default='basic',
        help='Analysis mode (default: basic)'
    )

    # Report generation command
    report_parser = subparsers.add_parser('report', help='Generate SEO report from scraped data')
    report_parser.add_argument('data_file', help='Path to scraped data JSON file')
    report_parser.add_argument('--output', help='Output file path')

    # Setup command
    setup_parser = subparsers.add_parser('setup', help='Set up Scrapy project')

    # List command
    list_parser = subparsers.add_parser('list', help='List available spiders')

    # Global options
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging')

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if not args.command:
        parser.print_help()
        return

    cli = WebScraperCLI()

    try:
        if args.command == 'seo':
            valid_urls = cli.validate_urls(args.urls)
            if not valid_urls:
                print("❌ No valid URLs provided")
                sys.exit(1)

            print(f"🔍 Analysing {len(valid_urls)} URLs with {args.mode} mode...")
            success = cli.run_seo_spider(valid_urls, args.mode, args.format)
            sys.exit(0 if success else 1)

        elif args.command == 'competitor':
            valid_urls = cli.validate_urls(args.urls)
            if not valid_urls:
                print("❌ No valid URLs provided")
                sys.exit(1)

            print(f"🕵️ Analysing {len(valid_urls)} competitor websites with {args.depth} depth...")
            success = cli.run_competitor_spider(valid_urls, args.depth, args.format)
            sys.exit(0 if success else 1)

        elif args.command == 'bulk':
            print(f"📊 Running bulk SEO analysis from {args.urls_file}...")
            success = cli.bulk_seo_analysis(args.urls_file, args.mode)
            sys.exit(0 if success else 1)

        elif args.command == 'report':
            print(f"📋 Generating SEO report from {args.data_file}...")
            success = cli.generate_seo_report(args.data_file, args.output)
            sys.exit(0 if success else 1)

        elif args.command == 'setup':
            print("⚙️ Setting up Scrapy project...")
            success = cli.setup_scrapy_project()
            sys.exit(0 if success else 1)

        elif args.command == 'list':
            spiders = cli.list_available_spiders()
            if spiders:
                print("Available spiders:")
                for spider in spiders:
                    print(f"  • {spider}")
            else:
                print("No spiders found")

    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()