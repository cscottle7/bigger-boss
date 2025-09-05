#!/usr/bin/env python3
"""
Natural Language Website Crawler Interface
Automatically triggers website crawling when agents request analysis
"""

import asyncio
import re
from pathlib import Path
import json
from datetime import datetime

# Import our comprehensive crawler
from comprehensive_seo_crawler import run_comprehensive_seo_crawl
from ..monitoring.tool_usage_tracker import ToolUsageTracker

class NaturalLanguageCrawler:
    def __init__(self):
        self.crawler_triggers = [
            r'analyze\s+(?:the\s+)?website',
            r'crawl\s+(?:the\s+)?(?:website|site)',
            r'extract\s+seo\s+data',
            r'get\s+page\s+titles?\s+and\s+meta\s+descriptions?',
            r'seo\s+analysis',
            r'website\s+audit',
            r'page.by.page\s+(?:seo|analysis)',
            r'comprehensive\s+(?:seo|website)\s+(?:analysis|audit)',
            r'extract\s+(?:all\s+)?(?:page|seo)\s+data',
            r'full\s+(?:website|seo)\s+(?:crawl|analysis)'
        ]
        self.url_pattern = r'https?://(?:[-\w.])+(?:\.[a-zA-Z]{2,4})+(?:/[^\s]*)?'
        
    def should_trigger_crawling(self, request_text):
        """Detect if natural language request requires website crawling"""
        request_lower = request_text.lower()
        
        # Check for crawling triggers
        for trigger in self.crawler_triggers:
            if re.search(trigger, request_lower):
                return True
        
        # Check for specific SEO-related requests
        seo_keywords = ['seo score', 'meta description', 'page title', 'h1 tag', 'seo audit']
        if any(keyword in request_lower for keyword in seo_keywords):
            return True
            
        return False
    
    def extract_url_from_request(self, request_text):
        """Extract URL from natural language request"""
        urls = re.findall(self.url_pattern, request_text)
        return urls[0] if urls else None
    
    def extract_page_limit(self, request_text):
        """Extract page limit from request (default 25)"""
        # Look for patterns like "first 10 pages", "analyze 50 pages", etc.
        patterns = [
            r'(?:first|analyze|crawl)\s+(\d+)\s+pages?',
            r'(\d+)\s+pages?',
            r'up\s+to\s+(\d+)\s+pages?'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, request_text.lower())
            if match:
                return min(int(match.group(1)), 100)  # Cap at 100 pages
        
        return 25  # Default
    
    async def process_natural_language_request(self, request_text, default_url=None):
        """Process natural language request and trigger crawling if needed"""
        
        if not self.should_trigger_crawling(request_text):
            return {
                "should_crawl": False,
                "reason": "Request does not require website crawling"
            }
        
        # Extract URL
        url = self.extract_url_from_request(request_text) or default_url
        if not url:
            return {
                "should_crawl": False,
                "reason": "No URL found in request and no default provided"
            }
        
        # Extract page limit
        page_limit = self.extract_page_limit(request_text)
        
        # Set up tracking
        tracker = ToolUsageTracker()
        tracker.log_tool_use("natural_language_crawler", "request_processor", 
                           "natural_language_parsing", True, 
                           {"request": request_text[:100], "url": url, "page_limit": page_limit})
        
        print(f"🤖 Natural Language Crawler Activated")
        print(f"📝 Request: {request_text[:100]}...")
        print(f"🎯 Target: {url}")
        print(f"📄 Pages: {page_limit}")
        print("🔄 Starting comprehensive crawl...")
        
        try:
            # Run the comprehensive crawl
            report, report_file = await run_comprehensive_seo_crawl(url, page_limit)
            
            # Track successful crawling
            tracker.log_tool_use("natural_language_crawler", "comprehensive_seo_crawler", 
                               "automated_crawl", True,
                               {"pages_crawled": report["scan_metadata"]["pages_crawled"],
                                "avg_seo_score": report["executive_summary"]["average_seo_score"]})
            
            # Generate user-friendly summary
            summary = self.generate_user_summary(report, request_text)
            
            return {
                "should_crawl": True,
                "crawl_completed": True,
                "url": url,
                "pages_analyzed": report["scan_metadata"]["pages_crawled"],
                "report_file": report_file,
                "summary": summary,
                "full_report": report
            }
            
        except Exception as e:
            # Track failed crawling
            tracker.log_tool_use("natural_language_crawler", "comprehensive_seo_crawler",
                               "automated_crawl", False, {"error": str(e)})
            
            return {
                "should_crawl": True,
                "crawl_completed": False,
                "error": str(e),
                "url": url
            }
    
    def generate_user_summary(self, report, original_request):
        """Generate user-friendly summary based on the original request"""
        pages_analyzed = report["scan_metadata"]["pages_crawled"]
        avg_score = report["executive_summary"]["average_seo_score"]
        critical_issues = report["executive_summary"]["critical_issues"]
        warnings = report["executive_summary"]["warnings"]
        
        # Extract key data for page-by-page requests
        if "page" in original_request.lower() and ("title" in original_request.lower() or "meta" in original_request.lower()):
            page_data = []
            for page in report["page_by_page_analysis"]:
                page_data.append({
                    "url": page["url"],
                    "title": page["page_title"],
                    "meta_description": page["meta_description"],
                    "h1_tags": page["h1_tags"],
                    "seo_score": page["seo_score"]
                })
            
            summary = {
                "type": "page_by_page_data",
                "total_pages": pages_analyzed,
                "page_details": page_data,
                "overview": f"Extracted SEO data from {pages_analyzed} pages with average score {avg_score}/100"
            }
        else:
            # General SEO analysis summary
            summary = {
                "type": "seo_analysis_summary",
                "total_pages": pages_analyzed,
                "average_seo_score": avg_score,
                "critical_issues": critical_issues,
                "warnings": warnings,
                "overview": f"Analyzed {pages_analyzed} pages. Average SEO score: {avg_score}/100. Found {critical_issues} critical issues and {warnings} warnings."
            }
        
        # Add recommendations based on findings
        if critical_issues > 0:
            summary["priority"] = "HIGH - Critical SEO issues found"
        elif warnings > 5:
            summary["priority"] = "MEDIUM - Multiple warnings need attention"  
        else:
            summary["priority"] = "LOW - Minor optimizations available"
            
        return summary

# Global instance for easy import
natural_crawler = NaturalLanguageCrawler()

# Convenience functions for agents
async def auto_crawl_if_needed(request_text, default_url=None):
    """Automatically crawl website if the request requires it"""
    return await natural_crawler.process_natural_language_request(request_text, default_url)

def should_crawl_website(request_text):
    """Quick check if request needs website crawling"""
    return natural_crawler.should_trigger_crawling(request_text)

# Example usage and testing
async def test_natural_language_crawler():
    """Test the natural language crawler with various requests"""
    test_requests = [
        "Please analyze the website https://sydneycoachcharter.com.au for SEO",
        "I need a comprehensive SEO audit of the first 10 pages",
        "Extract all page titles and meta descriptions from the site",
        "Can you crawl https://example.com and give me page-by-page SEO data?",
        "What is the weather like today?",  # Should not trigger crawling
        "Generate a full website analysis including SEO scores"
    ]
    
    print("🧪 Testing Natural Language Crawler")
    print("="*50)
    
    for i, request in enumerate(test_requests, 1):
        print(f"\\nTest {i}: {request}")
        result = await natural_crawler.process_natural_language_request(
            request, "https://sydneycoachcharter.com.au"
        )
        
        if result["should_crawl"]:
            if result.get("crawl_completed"):
                print(f"✅ Crawl completed: {result['pages_analyzed']} pages analyzed")
                print(f"📊 Summary: {result['summary']['overview']}")
            else:
                print(f"❌ Crawl failed: {result.get('error', 'Unknown error')}")
        else:
            print(f"⏭️  No crawling needed: {result['reason']}")

if __name__ == "__main__":
    # Run tests
    asyncio.run(test_natural_language_crawler())