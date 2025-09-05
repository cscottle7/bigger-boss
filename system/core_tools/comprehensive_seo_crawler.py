#!/usr/bin/env python3
"""
Comprehensive Page-by-Page SEO Crawler for Bigger Boss Agent System
Extracts complete SEO metadata for every page on a website with accuracy tracking
"""

import asyncio
from playwright.async_api import async_playwright
import json
from urllib.parse import urljoin, urlparse
import time
from datetime import datetime
from pathlib import Path
import logging
import sys
import os

# Add system path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from system.orchestration.autonomous_operation_manager import autonomous_manager
from system.config.api_credentials import credentials

class ComprehensiveSEOCrawler:
    def __init__(self, base_url, max_pages=50, client_domain=None, autonomous=True):
        self.base_url = base_url.rstrip('/')
        self.domain = urlparse(base_url).netloc
        self.max_pages = max_pages
        self.client_domain = client_domain or self.domain.replace('.', '_').replace('-', '_')
        self.crawled_pages = {}
        self.failed_pages = []
        self.autonomous = autonomous
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Setup output directories
        self.output_dir = Path(f"clients/{self.client_domain}/technical")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Check autonomous operation permissions
        if self.autonomous:
            can_crawl, message = autonomous_manager.can_perform_operation('web_crawling')
            if not can_crawl:
                raise PermissionError(f"Autonomous crawling not allowed: {message}")
                
            can_write, message = autonomous_manager.can_perform_operation(
                'file_operations', path=str(self.output_dir)
            )
            if not can_write:
                raise PermissionError(f"File operations not allowed: {message}")
        
    async def crawl_all_pages(self):
        """Crawl all pages and extract comprehensive SEO data"""
        self.logger.info(f"Starting comprehensive SEO crawl of {self.base_url}")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # Configure page for better crawling
            await page.set_extra_http_headers({
                "User-Agent": "Bigger-Boss-SEO-Crawler/1.0 (Website Analysis Tool)"
            })
            
            # Start with homepage
            pages_to_crawl = [self.base_url]
            crawled_urls = set()
            
            while pages_to_crawl and len(crawled_urls) < self.max_pages:
                url = pages_to_crawl.pop(0)
                if url in crawled_urls:
                    continue
                
                self.logger.info(f"Crawling page {len(crawled_urls) + 1}: {url}")
                try:
                    seo_data = await self.extract_comprehensive_seo_data(page, url)
                    self.crawled_pages[url] = seo_data
                    
                    # Find more internal links (if we haven't reached max pages)
                    if len(crawled_urls) < self.max_pages:
                        internal_links = await self.find_internal_links(page)
                        for link in internal_links[:10]:  # Limit new links per page
                            if link not in crawled_urls and link not in pages_to_crawl:
                                pages_to_crawl.append(link)
                    
                    crawled_urls.add(url)
                    
                except Exception as e:
                    error_msg = f"Failed to crawl {url}: {str(e)}"
                    self.logger.error(error_msg)
                    self.failed_pages.append({"url": url, "error": str(e), "timestamp": datetime.now().isoformat()})
                
                # Rate limiting to be respectful
                await asyncio.sleep(2)
            
            await browser.close()
        
        self.logger.info(f"Crawl completed: {len(self.crawled_pages)} pages successful, {len(self.failed_pages)} failed")
        return self.generate_comprehensive_seo_report()
    
    async def extract_comprehensive_seo_data(self, page, url):
        """Extract complete SEO data from a single page"""
        await page.goto(url, wait_until="networkidle", timeout=30000)
        
        # Extract all SEO metadata using JavaScript evaluation
        seo_data = await page.evaluate("""
            () => {
                // Helper function to get meta content
                const getMeta = (selector) => {
                    const element = document.querySelector(selector);
                    return element ? element.content || element.getAttribute('content') : null;
                };
                
                // Helper function to get attribute
                const getAttr = (selector, attr) => {
                    const element = document.querySelector(selector);
                    return element ? element.getAttribute(attr) : null;
                };
                
                // Get page title
                const title = document.title || '';
                
                // Get meta description
                const metaDescription = getMeta('meta[name="description"]') || 
                                     getMeta('meta[property="description"]');
                
                // Get canonical URL
                const canonical = document.querySelector('link[rel="canonical"]');
                const canonicalUrl = canonical ? canonical.href : null;
                
                // Get all headings with hierarchy
                const headings = {
                    h1: Array.from(document.querySelectorAll('h1')).map(h => ({
                        text: h.textContent.trim(),
                        position: Array.from(document.querySelectorAll('h1')).indexOf(h) + 1
                    })),
                    h2: Array.from(document.querySelectorAll('h2')).map(h => h.textContent.trim()),
                    h3: Array.from(document.querySelectorAll('h3')).map(h => h.textContent.trim()),
                    h4: Array.from(document.querySelectorAll('h4')).map(h => h.textContent.trim()),
                    h5: Array.from(document.querySelectorAll('h5')).map(h => h.textContent.trim()),
                    h6: Array.from(document.querySelectorAll('h6')).map(h => h.textContent.trim())
                };
                
                // Get meta keywords
                const metaKeywords = getMeta('meta[name="keywords"]');
                
                // Get Open Graph data
                const openGraph = {
                    title: getMeta('meta[property="og:title"]'),
                    description: getMeta('meta[property="og:description"]'),
                    image: getMeta('meta[property="og:image"]'),
                    url: getMeta('meta[property="og:url"]'),
                    type: getMeta('meta[property="og:type"]'),
                    site_name: getMeta('meta[property="og:site_name"]')
                };
                
                // Get Twitter Card data
                const twitterCard = {
                    card: getMeta('meta[name="twitter:card"]'),
                    title: getMeta('meta[name="twitter:title"]'),
                    description: getMeta('meta[name="twitter:description"]'),
                    image: getMeta('meta[name="twitter:image"]'),
                    creator: getMeta('meta[name="twitter:creator"]'),
                    site: getMeta('meta[name="twitter:site"]')
                };
                
                // Get robots meta
                const robots = getMeta('meta[name="robots"]');
                
                // Get viewport
                const viewport = getMeta('meta[name="viewport"]');
                
                // Get language
                const lang = document.documentElement.lang || 
                           getAttr('html', 'lang') ||
                           getMeta('meta[http-equiv="content-language"]');
                
                // Get word count and text analysis
                const bodyText = document.body.innerText || '';
                const wordCount = bodyText.trim().split(/\\s+/).filter(word => word.length > 0).length;
                
                // Get internal and external links
                const links = Array.from(document.querySelectorAll('a[href]'));
                const internalLinks = links.filter(link => 
                    link.href.includes(window.location.hostname) || 
                    link.href.startsWith('/')
                ).length;
                const externalLinks = links.filter(link => 
                    !link.href.includes(window.location.hostname) && 
                    !link.href.startsWith('/') &&
                    !link.href.startsWith('#') &&
                    !link.href.startsWith('mailto:') &&
                    !link.href.startsWith('tel:')
                ).length;
                
                // Get images analysis
                const images = Array.from(document.querySelectorAll('img'));
                const imageAnalysis = {
                    total_images: images.length,
                    images_with_alt: images.filter(img => img.alt && img.alt.trim()).length,
                    images_without_alt: images.filter(img => !img.alt || !img.alt.trim()).length
                };
                
                // Get structured data (JSON-LD)
                const jsonLdScripts = Array.from(document.querySelectorAll('script[type="application/ld+json"]'));
                const structuredData = jsonLdScripts.map(script => {
                    try {
                        return JSON.parse(script.textContent);
                    } catch (e) {
                        return null;
                    }
                }).filter(data => data !== null);
                
                return {
                    url: window.location.href,
                    title: title,
                    title_length: title.length,
                    meta_description: metaDescription,
                    meta_description_length: metaDescription ? metaDescription.length : 0,
                    canonical_url: canonicalUrl,
                    meta_keywords: metaKeywords,
                    robots: robots,
                    viewport: viewport,
                    language: lang,
                    headings: headings,
                    open_graph: openGraph,
                    twitter_card: twitterCard,
                    word_count: wordCount,
                    link_analysis: {
                        internal_links: internalLinks,
                        external_links: externalLinks,
                        total_links: links.length
                    },
                    image_analysis: imageAnalysis,
                    structured_data: structuredData,
                    extraction_timestamp: new Date().toISOString()
                };
            }
        """)
        
        # Add additional analysis
        seo_data['seo_issues'] = self.analyze_seo_issues(seo_data)
        seo_data['seo_score'] = self.calculate_seo_score(seo_data)
        
        return seo_data
    
    def analyze_seo_issues(self, data):
        """Analyze SEO data and identify issues"""
        issues = []
        
        # Title issues
        if not data.get('title') or len(data.get('title', '')) == 0:
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
        image_analysis = data.get('image_analysis', {})
        if image_analysis.get('images_without_alt', 0) > 0:
            issues.append({"type": "warning", "category": "accessibility", 
                          "issue": f"{image_analysis['images_without_alt']} images missing alt text"})
        
        # Canonical issues
        if not data.get('canonical_url'):
            issues.append({"type": "info", "category": "technical", "issue": "Missing canonical URL"})
        
        # Open Graph issues
        og = data.get('open_graph', {})
        if not og.get('title') or not og.get('description'):
            issues.append({"type": "info", "category": "social", "issue": "Incomplete Open Graph metadata"})
        
        return issues
    
    def calculate_seo_score(self, data):
        """Calculate overall SEO score for the page"""
        score = 100
        
        # Title scoring
        title = data.get('title', '')
        if not title:
            score -= 20
        elif len(title) < 30 or len(title) > 60:
            score -= 10
        
        # Meta description scoring
        meta_desc = data.get('meta_description', '')
        if not meta_desc:
            score -= 20
        elif len(meta_desc) < 120 or len(meta_desc) > 160:
            score -= 10
        
        # H1 scoring
        h1_tags = data.get('headings', {}).get('h1', [])
        if len(h1_tags) == 0:
            score -= 15
        elif len(h1_tags) > 1:
            score -= 10
        
        # Image alt text scoring
        image_analysis = data.get('image_analysis', {})
        if image_analysis.get('total_images', 0) > 0:
            alt_ratio = image_analysis.get('images_with_alt', 0) / image_analysis.get('total_images', 1)
            if alt_ratio < 0.8:
                score -= 10
        
        # Content length scoring
        word_count = data.get('word_count', 0)
        if word_count < 300:
            score -= 15
        
        return max(0, score)
    
    async def find_internal_links(self, page):
        """Find internal links on current page"""
        internal_links = await page.evaluate(f"""
            () => {{
                const links = Array.from(document.querySelectorAll('a[href]'));
                const domain = '{self.domain}';
                const baseUrl = '{self.base_url}';
                
                return links
                    .map(link => {{
                        let href = link.href;
                        
                        // Handle relative URLs
                        if (href.startsWith('/')) {{
                            return baseUrl + href;
                        }}
                        
                        // Handle same domain URLs
                        if (href.includes(domain)) {{
                            return href;
                        }}
                        
                        return null;
                    }})
                    .filter(href => href !== null)
                    .filter(href => !href.includes('#'))  // Remove anchors
                    .filter(href => !href.includes('?'))  // Remove query parameters for now
                    .filter((href, index, array) => array.indexOf(href) === index); // Remove duplicates
            }}
        """)
        
        return internal_links[:15]  # Limit to prevent overwhelming
    
    def generate_comprehensive_seo_report(self):
        """Generate comprehensive SEO report with detailed analysis"""
        report = {
            "scan_metadata": {
                "domain": self.domain,
                "base_url": self.base_url,
                "client": self.client_domain,
                "scan_date": datetime.now().isoformat(),
                "pages_crawled": len(self.crawled_pages),
                "pages_failed": len(self.failed_pages),
                "max_pages_setting": self.max_pages,
                "crawler_version": "1.0"
            },
            "executive_summary": {
                "total_pages": len(self.crawled_pages),
                "average_seo_score": 0,
                "critical_issues": 0,
                "warnings": 0,
                "info_items": 0
            },
            "page_by_page_analysis": [],
            "site_wide_issues": [],
            "recommendations": [],
            "failed_pages": self.failed_pages
        }
        
        total_score = 0
        all_issues = []
        
        # Analyze each successfully crawled page
        for url, data in self.crawled_pages.items():
            page_analysis = {
                "url": url,
                "page_title": data.get('title', 'NO TITLE'),
                "meta_description": data.get('meta_description', 'NO META DESCRIPTION'),
                "h1_tags": [h1['text'] if isinstance(h1, dict) else h1 for h1 in data.get('headings', {}).get('h1', [])],
                "seo_score": data.get('seo_score', 0),
                "word_count": data.get('word_count', 0),
                "issues": data.get('seo_issues', []),
                "technical_details": {
                    "canonical_url": data.get('canonical_url'),
                    "robots": data.get('robots'),
                    "language": data.get('language'),
                    "structured_data_found": len(data.get('structured_data', [])) > 0
                }
            }
            
            report["page_by_page_analysis"].append(page_analysis)
            total_score += data.get('seo_score', 0)
            all_issues.extend(data.get('seo_issues', []))
        
        # Calculate summary statistics
        if self.crawled_pages:
            report["executive_summary"]["average_seo_score"] = round(total_score / len(self.crawled_pages), 1)
        
        # Count issue types
        for issue in all_issues:
            issue_type = issue.get('type', 'info')
            if issue_type == 'critical':
                report["executive_summary"]["critical_issues"] += 1
            elif issue_type == 'warning':
                report["executive_summary"]["warnings"] += 1
            else:
                report["executive_summary"]["info_items"] += 1
        
        # Generate site-wide analysis
        report["site_wide_issues"] = self.analyze_site_wide_patterns()
        
        # Generate recommendations
        report["recommendations"] = self.generate_recommendations(all_issues)
        
        # Save comprehensive report
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = self.output_dir / f"comprehensive_seo_analysis_{timestamp}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # Also save a simplified CSV for easy viewing
        self.save_simplified_csv_report(report, timestamp)
        
        self.logger.info(f"Comprehensive SEO report saved: {report_file}")
        return report, str(report_file)
    
    def analyze_site_wide_patterns(self):
        """Analyze patterns across all pages"""
        patterns = []
        
        # Check for consistent title patterns
        titles = [data.get('title', '') for data in self.crawled_pages.values()]
        if len(set(titles)) != len(titles):
            patterns.append("Duplicate titles found across multiple pages")
        
        # Check for consistent meta description patterns
        meta_descs = [data.get('meta_description', '') for data in self.crawled_pages.values()]
        meta_descs = [desc for desc in meta_descs if desc]  # Remove empty ones
        if len(set(meta_descs)) != len(meta_descs):
            patterns.append("Duplicate meta descriptions found across multiple pages")
        
        return patterns
    
    def generate_recommendations(self, all_issues):
        """Generate prioritized recommendations"""
        recommendations = []
        
        # Count issue types
        issue_counts = {}
        for issue in all_issues:
            category = issue.get('category', 'other')
            if category not in issue_counts:
                issue_counts[category] = {'critical': 0, 'warning': 0, 'info': 0}
            issue_counts[category][issue.get('type', 'info')] += 1
        
        # Generate recommendations based on most common issues
        for category, counts in sorted(issue_counts.items(), key=lambda x: x[1]['critical'], reverse=True):
            total_issues = sum(counts.values())
            if total_issues > 0:
                priority = 'HIGH' if counts['critical'] > 0 else 'MEDIUM' if counts['warning'] > 0 else 'LOW'
                recommendations.append({
                    'priority': priority,
                    'category': category.replace('_', ' ').title(),
                    'total_issues': total_issues,
                    'critical': counts['critical'],
                    'warnings': counts['warning'],
                    'recommendation': self.get_recommendation_text(category, counts)
                })
        
        return recommendations
    
    def get_recommendation_text(self, category, counts):
        """Get specific recommendation text for each category"""
        texts = {
            'title': f"Fix {counts['critical']} missing titles and optimize {counts['warning']} title lengths",
            'meta_description': f"Add {counts['critical']} missing meta descriptions and optimize {counts['warning']} lengths",
            'headings': f"Fix {counts['critical']} missing H1 tags and resolve {counts['warning']} multiple H1 issues",
            'accessibility': f"Add alt text to {counts['warning']} images missing descriptions",
            'technical': f"Address {counts['critical'] + counts['warning']} technical SEO issues",
            'social': f"Complete Open Graph and Twitter Card metadata for better social sharing"
        }
        return texts.get(category, f"Address {counts['critical'] + counts['warning']} issues in {category}")
    
    def save_simplified_csv_report(self, report, timestamp):
        """Save a simplified CSV report for easy viewing"""
        csv_content = "URL,Page Title,Meta Description,H1 Tags,SEO Score,Indexable\n"
        
        for page in report["page_by_page_analysis"]:
            # Clean data for CSV
            title = page.get('page_title', '').replace('"', '""')
            meta_desc = page.get('meta_description', '').replace('"', '""')
            h1_tags = '; '.join(page.get('h1_tags', [])).replace('"', '""')
            
            # Determine if page is indexable
            robots = page.get('technical_details', {}).get('robots', '')
            indexable = "Yes"
            if robots and ('noindex' in robots.lower() or 'none' in robots.lower()):
                indexable = "No"
            
            csv_content += f'"{page.get("url", "")}","{title}","{meta_desc}","{h1_tags}",{page.get("seo_score", 0)},{indexable}\n'
        
        csv_file = self.output_dir / f"seo_analysis_summary_{timestamp}.csv"
        with open(csv_file, 'w', encoding='utf-8') as f:
            f.write(csv_content)
        
        self.logger.info(f"CSV summary saved: {csv_file}")

# Main execution function
async def run_comprehensive_seo_crawl(url, max_pages=50, client_domain=None):
    """Main function to run comprehensive SEO crawl"""
    crawler = ComprehensiveSEOCrawler(url, max_pages, client_domain)
    report, report_file = await crawler.crawl_all_pages()
    
    print(f"\\n🎯 COMPREHENSIVE SEO CRAWL COMPLETE!")
    print(f"📊 Report saved: {report_file}")
    print(f"📈 Pages analyzed: {report['scan_metadata']['pages_crawled']}")
    print(f"⚠️  Critical issues: {report['executive_summary']['critical_issues']}")
    print(f"📋 Warnings: {report['executive_summary']['warnings']}")
    print(f"🎯 Average SEO score: {report['executive_summary']['average_seo_score']}/100")
    
    return report, report_file

# Example usage and testing
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
        max_pages = int(sys.argv[2]) if len(sys.argv) > 2 else 25
    else:
        url = "https://sydneycoachcharter.com.au"
        max_pages = 25
    
    print(f"Starting comprehensive SEO crawl of: {url}")
    report, report_file = asyncio.run(run_comprehensive_seo_crawl(url, max_pages))
    
    print(f"\\n📁 Find your complete analysis at: {report_file}")