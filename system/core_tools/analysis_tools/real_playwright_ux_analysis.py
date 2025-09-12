#!/usr/bin/env python3
"""
Real Playwright Browser Automation UX/UI Analysis
Provides actual browser testing with screenshots and measurements
"""

import asyncio
from playwright.async_api import async_playwright
import json
import os
from datetime import datetime

class RealPlaywrightUXAnalyzer:
    def __init__(self, url="https://sydneycoachcharter.com.au"):
        self.url = url
        self.results = {
            "analysis_date": datetime.now().isoformat(),
            "url": url,
            "methodology": "Real Playwright Browser Automation",
            "evidence": {
                "screenshots": [],
                "measurements": {},
                "interactions": [],
                "accessibility": {},
                "performance": {}
            }
        }
        
        # Ensure screenshots directory exists
        self.screenshot_dir = "analysis_tools/screenshots"
        os.makedirs(self.screenshot_dir, exist_ok=True)
    
    async def comprehensive_analysis(self):
        """Run complete UX/UI analysis with real browser automation"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            
            # Test multiple viewports
            viewports = [
                {"name": "desktop", "width": 1920, "height": 1080},
                {"name": "tablet", "width": 768, "height": 1024},
                {"name": "mobile", "width": 375, "height": 667}
            ]
            
            for viewport in viewports:
                await self.analyze_viewport(browser, viewport)
            
            # Test specific UX elements
            await self.test_interactions(browser)
            await self.measure_performance(browser)
            await self.check_accessibility(browser)
            
            await browser.close()
        
        return self.results
    
    async def analyze_viewport(self, browser, viewport):
        """Analyze website at specific viewport size"""
        context = await browser.new_context(
            viewport={"width": viewport["width"], "height": viewport["height"]},
            user_agent="Mozilla/5.0 (compatible; PlaywrightUXAnalyzer/1.0)"
        )
        
        page = await context.new_page()
        await page.goto(self.url, wait_until="networkidle")
        
        # Capture screenshot
        screenshot_path = f"{self.screenshot_dir}/{viewport['name']}_{viewport['width']}x{viewport['height']}.png"
        await page.screenshot(path=screenshot_path, full_page=True)
        
        # Gather measurements
        measurements = await page.evaluate('''() => {
            return {
                viewport_width: window.innerWidth,
                viewport_height: window.innerHeight,
                page_height: document.body.scrollHeight,
                first_h1_visible: !!document.querySelector('h1'),
                navigation_visible: !!document.querySelector('nav'),
                contact_info_visible: !!document.querySelector('a[href*="tel:"]'),
                quote_buttons: document.querySelectorAll('a[href*="quote"], button[type="submit"]').length,
                scroll_to_content: document.querySelector('main') ? document.querySelector('main').offsetTop : 0
            }
        }''')
        
        self.results["evidence"]["screenshots"].append({
            "device": viewport["name"],
            "path": screenshot_path,
            "viewport": f"{viewport['width']}x{viewport['height']}"
        })
        
        self.results["evidence"]["measurements"][viewport["name"]] = measurements
        
        await context.close()
    
    async def test_interactions(self, browser):
        """Test key interactive elements"""
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()
        await page.goto(self.url, wait_until="networkidle")
        
        interactions = []
        
        # Test navigation menu
        try:
            nav_items = await page.query_selector_all('nav a')
            interactions.append({
                "element": "navigation",
                "count": len(nav_items),
                "accessible": len(nav_items) > 0
            })
        except:
            interactions.append({"element": "navigation", "error": "Navigation not found"})
        
        # Test quote/contact forms
        try:
            forms = await page.query_selector_all('form')
            for i, form in enumerate(forms):
                form_info = await form.evaluate('''form => ({
                    action: form.action,
                    method: form.method,
                    fields: form.querySelectorAll('input, textarea, select').length
                })''')
                interactions.append({
                    "element": f"form_{i+1}",
                    "details": form_info
                })
        except:
            interactions.append({"element": "forms", "error": "No forms found"})
        
        # Test phone links
        try:
            phone_links = await page.query_selector_all('a[href^="tel:"]')
            interactions.append({
                "element": "phone_links",
                "count": len(phone_links),
                "functional": len(phone_links) > 0
            })
        except:
            pass
        
        self.results["evidence"]["interactions"] = interactions
        await context.close()
    
    async def measure_performance(self, browser):
        """Measure real performance metrics"""
        context = await browser.new_context()
        page = await context.new_page()
        
        # Start timing
        start_time = datetime.now()
        await page.goto(self.url, wait_until="networkidle")
        load_time = (datetime.now() - start_time).total_seconds()
        
        # Get performance metrics
        performance = await page.evaluate('''() => {
            const navigation = performance.getEntriesByType('navigation')[0];
            return navigation ? {
                dom_content_loaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
                load_complete: navigation.loadEventEnd - navigation.loadEventStart,
                first_contentful_paint: performance.getEntriesByName('first-contentful-paint')[0]?.startTime,
                total_resources: performance.getEntriesByType('resource').length
            } : null;
        }''')
        
        self.results["evidence"]["performance"] = {
            "page_load_time": load_time,
            "browser_metrics": performance
        }
        
        await context.close()
    
    async def check_accessibility(self, browser):
        """Check basic accessibility features"""
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(self.url, wait_until="networkidle")
        
        # Check accessibility features
        accessibility = await page.evaluate('''() => {
            return {
                has_alt_images: Array.from(document.querySelectorAll('img')).some(img => img.alt),
                missing_alt_images: Array.from(document.querySelectorAll('img')).filter(img => !img.alt).length,
                has_headings: !!document.querySelector('h1, h2, h3, h4, h5, h6'),
                heading_structure: Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6')).map(h => h.tagName),
                form_labels: document.querySelectorAll('label').length,
                form_inputs: document.querySelectorAll('input, textarea, select').length,
                skip_links: document.querySelectorAll('a[href^="#"]').length,
                aria_labels: document.querySelectorAll('[aria-label]').length
            }
        }''')
        
        self.results["evidence"]["accessibility"] = accessibility
        await context.close()
    
    def generate_report(self):
        """Generate comprehensive UX/UI analysis report"""
        report = f"""# Real Playwright Browser Automation UX/UI Analysis Report

## Analysis Overview
- **Date**: {self.results['analysis_date']}
- **URL**: {self.results['url']}
- **Method**: {self.results['methodology']}
- **Evidence**: Browser automation with screenshots and measurements

## Multi-Device Analysis Results

"""
        
        for device, measurements in self.results["evidence"]["measurements"].items():
            report += f"""### {device.title()} Device Analysis
- **Viewport**: {measurements.get('viewport_width', 'N/A')}x{measurements.get('viewport_height', 'N/A')}
- **Page Height**: {measurements.get('page_height', 'N/A')}px
- **H1 Visible**: {"✅" if measurements.get('first_h1_visible') else "❌"}
- **Navigation Present**: {"✅" if measurements.get('navigation_visible') else "❌"}
- **Contact Info Visible**: {"✅" if measurements.get('contact_info_visible') else "❌"}
- **Quote Buttons**: {measurements.get('quote_buttons', 0)}

"""
        
        # Add screenshot evidence
        report += "## Visual Evidence (Screenshots)\n\n"
        for screenshot in self.results["evidence"]["screenshots"]:
            report += f"- **{screenshot['device'].title()}** ({screenshot['viewport']}): {screenshot['path']}\n"
        
        # Add interaction analysis
        report += "\n## Interactive Element Analysis\n\n"
        for interaction in self.results["evidence"]["interactions"]:
            report += f"- **{interaction['element']}**: {json.dumps(interaction, indent=2)}\n"
        
        # Add performance analysis
        perf = self.results["evidence"]["performance"]
        report += f"""
## Real Performance Measurements
- **Page Load Time**: {perf.get('page_load_time', 'N/A')} seconds
- **DOM Content Loaded**: {perf.get('browser_metrics', {}).get('dom_content_loaded', 'N/A')}ms
- **Total Resources**: {perf.get('browser_metrics', {}).get('total_resources', 'N/A')}

"""
        
        # Add accessibility findings
        access = self.results["evidence"]["accessibility"]
        report += f"""## Accessibility Assessment
- **Images with Alt Text**: {"✅" if access.get('has_alt_images') else "❌"}
- **Missing Alt Text**: {access.get('missing_alt_images', 'N/A')} images
- **Proper Headings**: {"✅" if access.get('has_headings') else "❌"}
- **Form Labels**: {access.get('form_labels', 0)} labels for {access.get('form_inputs', 0)} inputs
- **ARIA Labels**: {access.get('aria_labels', 0)}

"""
        
        return report

async def main():
    """Run the comprehensive UX/UI analysis"""
    analyzer = RealPlaywrightUXAnalyzer()
    print("Starting Real Playwright Browser Automation UX/UI Analysis...")
    
    results = await analyzer.comprehensive_analysis()
    report = analyzer.generate_report()
    
    # Save results
    with open("analysis_tools/real_ux_analysis_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    with open("analysis_tools/real_ux_analysis_report.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    print("Real UX/UI Analysis Complete!")
    print("Results saved to:")
    print("   - analysis_tools/real_ux_analysis_results.json")
    print("   - analysis_tools/real_ux_analysis_report.md")
    print("Screenshots saved to: analysis_tools/screenshots/")
    
    return report

if __name__ == "__main__":
    report = asyncio.run(main())
    print("\n" + "="*80)
    print("REAL PLAYWRIGHT UX/UI ANALYSIS REPORT")
    print("="*80)
    print(report[:2000] + "..." if len(report) > 2000 else report)