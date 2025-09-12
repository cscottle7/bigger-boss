#!/usr/bin/env python3
"""
Comprehensive Playwright browser automation analysis for Sydney Coach Charter
Real-time browser rendering and performance analysis
"""

import json
import asyncio
from playwright.async_api import async_playwright
import pandas as pd
from datetime import datetime

class PlaywrightAnalyzer:
    def __init__(self):
        self.results = {}
        
    async def comprehensive_analysis(self):
        """Run comprehensive browser automation analysis"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # Enable performance monitoring
            await page.route("**/*", self.log_requests)
            
            try:
                # Navigate to website
                print("Navigating to Sydney Coach Charter...")
                response = await page.goto('https://sydneycoachcharter.com.au')
                await page.wait_for_load_state('networkidle')
                
                # Comprehensive analysis
                analysis = await self.extract_comprehensive_data(page, response)
                
                await browser.close()
                return analysis
                
            except Exception as e:
                await browser.close()
                return {"error": str(e)}
    
    async def log_requests(self, route):
        """Log network requests for performance analysis"""
        request = route.request
        if not hasattr(self, 'requests'):
            self.requests = []
        
        self.requests.append({
            'url': request.url,
            'method': request.method,
            'resource_type': request.resource_type
        })
        
        await route.continue_()
    
    async def extract_comprehensive_data(self, page, response):
        """Extract comprehensive website data using browser rendering"""
        
        print("Extracting comprehensive browser data...")
        
        # Basic page metrics
        basic_metrics = {
            'url': page.url,
            'title': await page.title(),
            'status_code': response.status,
            'viewport': page.viewport_size,
            'timestamp': datetime.now().isoformat()
        }
        
        # SEO Analysis with browser rendering
        seo_data = await self.extract_seo_data(page)
        
        # Performance metrics
        performance_data = await self.extract_performance_data(page)
        
        # Content analysis with rendered content
        content_data = await self.extract_content_data(page)
        
        # Accessibility analysis
        accessibility_data = await self.extract_accessibility_data(page)
        
        # Forms and CTAs analysis
        forms_data = await self.extract_forms_data(page)
        
        # Mobile responsiveness test
        mobile_data = await self.test_mobile_responsiveness(page)
        
        return {
            'basic_metrics': basic_metrics,
            'seo_analysis': seo_data,
            'performance_metrics': performance_data,
            'content_analysis': content_data,
            'accessibility_analysis': accessibility_data,
            'forms_analysis': forms_data,
            'mobile_analysis': mobile_data,
            'network_requests': getattr(self, 'requests', [])
        }
    
    async def extract_seo_data(self, page):
        """Extract SEO data from rendered page"""
        print("Analyzing SEO elements...")
        
        # Meta tags
        title = await page.title()
        meta_description = await page.get_attribute('meta[name="description"]', 'content') or None
        canonical = await page.get_attribute('link[rel="canonical"]', 'href') or None
        
        # Heading structure
        h1_elements = await page.locator('h1').all()
        h1_texts = [await h1.text_content() for h1 in h1_elements]
        
        h2_elements = await page.locator('h2').all()
        h2_texts = [await h2.text_content() for h2 in h2_elements]
        
        # Images analysis
        images = await page.locator('img').all()
        images_data = []
        for img in images:
            src = await img.get_attribute('src')
            alt = await img.get_attribute('alt')
            images_data.append({'src': src, 'alt': alt, 'has_alt': bool(alt)})
        
        # Links analysis
        internal_links = await page.locator('a[href^="/"], a[href*="sydneycoachcharter.com.au"]').count()
        external_links = await page.locator('a[href^="http"]:not([href*="sydneycoachcharter.com.au"])').count()
        
        return {
            'title': title,
            'title_length': len(title) if title else 0,
            'meta_description': meta_description,
            'meta_description_length': len(meta_description) if meta_description else 0,
            'canonical_url': canonical,
            'h1_count': len(h1_texts),
            'h1_texts': h1_texts,
            'h2_count': len(h2_texts),
            'h2_texts': h2_texts,
            'total_images': len(images_data),
            'images_with_alt': sum(1 for img in images_data if img['has_alt']),
            'images_without_alt': sum(1 for img in images_data if not img['has_alt']),
            'internal_links_count': internal_links,
            'external_links_count': external_links,
            'images_details': images_data[:10]  # First 10 images for detailed analysis
        }
    
    async def extract_performance_data(self, page):
        """Extract performance metrics"""
        print("Analyzing performance metrics...")
        
        # Execute JavaScript to get performance data
        performance_data = await page.evaluate("""
            () => {
                const navigation = performance.getEntriesByType('navigation')[0];
                const resources = performance.getEntriesByType('resource');
                
                return {
                    load_time: navigation ? navigation.loadEventEnd - navigation.loadEventStart : null,
                    dom_content_loaded: navigation ? navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart : null,
                    first_contentful_paint: null, // Would need additional setup for FCP
                    resource_count: resources.length,
                    total_transfer_size: resources.reduce((sum, r) => sum + (r.transferSize || 0), 0),
                    page_size_bytes: document.documentElement.outerHTML.length
                }
            }
        """)
        
        return performance_data
    
    async def extract_content_data(self, page):
        """Extract content analysis from rendered page"""
        print("Analyzing content data...")
        
        # Get all text content
        full_text = await page.text_content('body')
        
        # Service mentions with case-insensitive search
        service_mentions = {
            'wedding': len(await page.locator('text=/wedding/i').all()),
            'corporate': len(await page.locator('text=/corporate/i').all()),
            'school': len(await page.locator('text=/school/i').all()),
            'charter': len(await page.locator('text=/charter/i').all()),
            'tour': len(await page.locator('text=/tour/i').all()),
            'sydney': len(await page.locator('text=/sydney/i').all()),
            'nsw': len(await page.locator('text=/nsw/i').all())
        }
        
        # Contact information detection
        phone_visible = await page.locator('text=/(02) 9181 5557/').count() > 0
        quote_buttons = await page.locator('text=/quote/i').count()
        book_buttons = await page.locator('text=/book/i').count()
        
        return {
            'total_text_length': len(full_text) if full_text else 0,
            'word_count_estimate': len(full_text.split()) if full_text else 0,
            'service_mentions': service_mentions,
            'contact_info': {
                'phone_visible': phone_visible,
                'quote_buttons_count': quote_buttons,
                'book_buttons_count': book_buttons
            }
        }
    
    async def extract_accessibility_data(self, page):
        """Extract accessibility information"""
        print("Analyzing accessibility features...")
        
        # Form accessibility
        inputs_with_labels = await page.locator('input[aria-label], input[aria-labelledby], label input').count()
        inputs_without_labels = await page.locator('input:not([aria-label]):not([aria-labelledby])').count()
        
        # Image accessibility
        images_with_alt = await page.locator('img[alt]').count()
        images_without_alt = await page.locator('img:not([alt])').count()
        
        # Heading structure
        h1_count = await page.locator('h1').count()
        
        return {
            'images_with_alt': images_with_alt,
            'images_without_alt': images_without_alt,
            'inputs_with_labels': inputs_with_labels,
            'inputs_without_labels': inputs_without_labels,
            'proper_h1_structure': h1_count == 1,
            'h1_count': h1_count
        }
    
    async def extract_forms_data(self, page):
        """Extract forms and CTA data"""
        print("Analyzing forms and CTAs...")
        
        forms_count = await page.locator('form').count()
        contact_forms = await page.locator('form:has(input[type="email"]), form:has(input[name*="email"]), form:has(input[name*="contact"])').count()
        
        # CTA analysis
        quote_ctas = await page.locator('text=/get.*quote/i, text=/request.*quote/i').count()
        call_ctas = await page.locator('text=/call/i').count()
        contact_ctas = await page.locator('text=/contact/i').count()
        
        return {
            'total_forms': forms_count,
            'contact_forms': contact_forms,
            'cta_analysis': {
                'quote_ctas': quote_ctas,
                'call_ctas': call_ctas,
                'contact_ctas': contact_ctas
            }
        }
    
    async def test_mobile_responsiveness(self, page):
        """Test mobile responsiveness"""
        print("Testing mobile responsiveness...")
        
        # Test different viewport sizes
        viewports = [
            {'width': 375, 'height': 667, 'name': 'mobile_portrait'},
            {'width': 768, 'height': 1024, 'name': 'tablet_portrait'},
            {'width': 1920, 'height': 1080, 'name': 'desktop'}
        ]
        
        mobile_results = {}
        
        for viewport in viewports:
            await page.set_viewport_size({'width': viewport['width'], 'height': viewport['height']})
            await page.wait_for_timeout(1000)  # Wait for responsive changes
            
            # Check if navigation is accessible
            nav_visible = await page.locator('nav, [role="navigation"]').is_visible()
            
            # Check if key content is visible
            title_visible = await page.locator('h1').first.is_visible() if await page.locator('h1').count() > 0 else False
            
            mobile_results[viewport['name']] = {
                'viewport': {'width': viewport['width'], 'height': viewport['height']},
                'navigation_visible': nav_visible,
                'h1_visible': title_visible,
                'responsive_friendly': nav_visible and title_visible
            }
        
        return mobile_results

def run_playwright_analysis():
    """Run the comprehensive Playwright analysis"""
    analyzer = PlaywrightAnalyzer()
    
    try:
        # Run async analysis
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(analyzer.comprehensive_analysis())
        loop.close()
        
        return results
        
    except Exception as e:
        return {"error": f"Playwright analysis failed: {str(e)}"}

if __name__ == "__main__":
    print("=== PLAYWRIGHT COMPREHENSIVE BROWSER AUTOMATION ANALYSIS ===")
    results = run_playwright_analysis()
    
    # Save results to JSON file
    with open('playwright_analysis_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("Analysis complete! Results saved to playwright_analysis_results.json")
    print(json.dumps(results, indent=2))