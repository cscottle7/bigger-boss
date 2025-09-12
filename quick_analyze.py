#!/usr/bin/env python3
"""
Quick Autonomous Website Analyzer
Analyzes ANY website without WebFetch permissions using Playwright directly
"""

import asyncio
import sys
from pathlib import Path
from playwright.async_api import async_playwright
import json
from datetime import datetime

async def analyze_website_autonomous(domain: str) -> dict:
    """Quick autonomous website analysis without WebFetch permissions"""
    
    url = f"https://{domain}" if not domain.startswith('http') else domain
    
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # Navigate and extract data
            await page.goto(url, wait_until="networkidle", timeout=30000)
            
            # Extract key website information
            data = await page.evaluate("""
                () => {
                    return {
                        title: document.title || 'No title',
                        description: document.querySelector('meta[name="description"]')?.content || 'No description',
                        h1Tags: Array.from(document.querySelectorAll('h1')).map(h => h.textContent.trim()),
                        h2Tags: Array.from(document.querySelectorAll('h2')).slice(0, 5).map(h => h.textContent.trim()),
                        wordCount: document.body.innerText.trim().split(/\\s+/).length,
                        images: document.querySelectorAll('img').length,
                        links: document.querySelectorAll('a').length,
                        hasContactForm: document.querySelector('form[action*="contact"], form[id*="contact"], form[class*="contact"]') !== null,
                        phoneNumbers: document.body.innerText.match(/\\(\\d{2}\\)\\s\\d{4}\\s\\d{4}|\\d{4}\\s\\d{3}\\s\\d{3}/g) || [],
                        emails: document.body.innerText.match(/[\\w.-]+@[\\w.-]+\\.[\\w]{2,}/gi) || [],
                        australianMentions: document.body.innerText.match(/Australia|Sydney|Melbourne|Brisbane/gi) || []
                    };
                }
            """)
            
            await browser.close()
            
            # Create client folder and save report
            client_domain = domain.replace('.', '_').replace('-', '_').replace('https://', '').replace('http://', '')
            client_folder = Path(f"clients/{client_domain}/technical")
            client_folder.mkdir(parents=True, exist_ok=True)
            
            # Save report
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_file = client_folder / f"quick_analysis_{timestamp}.json"
            
            full_report = {
                'analysisMetadata': {
                    'domain': domain,
                    'url': url,
                    'timestamp': datetime.now().isoformat(),
                    'method': 'Autonomous Playwright Analysis',
                    'webfetch_permissions': 'Not Required'
                },
                'websiteData': data
            }
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(full_report, f, indent=2)
            
            return {
                'success': True,
                'data': data,
                'report_saved': str(report_file)
            }
            
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

async def main():
    if len(sys.argv) < 2:
        print("Usage: python quick_analyze.py [website.com]")
        return
    
    domain = sys.argv[1]
    
    print(f"QUICK AUTONOMOUS ANALYSIS")
    print(f"Domain: {domain}")
    print("No WebFetch permissions required!")
    print("-" * 40)
    
    result = await analyze_website_autonomous(domain)
    
    if result.get('success'):
        data = result['data']
        print("SUCCESS: Website analyzed autonomously!")
        print(f"Title: {data.get('title', 'N/A')}")
        print(f"Word Count: {data.get('wordCount', 0)}")
        print(f"H1 Tags: {len(data.get('h1Tags', []))}")
        print(f"Images: {data.get('images', 0)}")
        print(f"Links: {data.get('links', 0)}")
        print(f"Has Contact Form: {'Yes' if data.get('hasContactForm') else 'No'}")
        
        if data.get('phoneNumbers'):
            print(f"Phone Numbers Found: {len(data['phoneNumbers'])}")
        if data.get('emails'):
            print(f"Email Addresses Found: {len(data['emails'])}")
        
        print(f"\nReport saved: {result.get('report_saved')}")
        
    else:
        print(f"ERROR: {result.get('error')}")

if __name__ == "__main__":
    asyncio.run(main())