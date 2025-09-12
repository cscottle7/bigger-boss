#!/usr/bin/env python3
"""
Test script to verify website crawling is working properly
"""
import asyncio
from playwright.async_api import async_playwright

async def test_crawling(url):
    """Test actual website crawling and data extraction"""
    print(f"Testing crawling for: {url}")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        try:
            await page.goto(url, wait_until="networkidle")
            
            # Extract actual SEO data
            data = await page.evaluate("""
                () => {
                    return {
                        title: document.title,
                        meta_description: document.querySelector('meta[name="description"]')?.content || 'NOT FOUND',
                        h1: Array.from(document.querySelectorAll('h1')).map(h => h.textContent.trim()),
                        url: window.location.href,
                        timestamp: new Date().toISOString()
                    };
                }
            """)
            
            print("CRAWLING SUCCESS")
            print(f"Title: {data['title']}")
            print(f"Meta Description: {data['meta_description']}")
            print(f"H1s: {data['h1']}")
            print(f"URL: {data['url']}")
            
            return data
            
        except Exception as e:
            print(f"CRAWLING FAILED: {str(e)}")
            return None
        finally:
            await browser.close()

if __name__ == "__main__":
    url = "https://sydneycoachcharter.com.au"
    result = asyncio.run(test_crawling(url))
    
    if result:
        print("\nSOLUTION: Crawling is working! The issue is in agent tool integration.")
    else:
        print("\nPROBLEM: Basic crawling is failing. Need to fix Playwright setup first.")