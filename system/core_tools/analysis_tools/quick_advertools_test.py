#!/usr/bin/env python3
"""
Quick Advertools test without unicode issues
"""

import advertools as adv
import pandas as pd

def quick_test():
    print(f"Advertools version: {adv.__version__}")
    
    working = []
    failed = []
    
    # Test robots.txt
    try:
        robots_df = adv.robotstxt_to_df("https://sydneycoachcharter.com.au/robots.txt")
        working.append(f"robots_txt: {len(robots_df)} rules found")
    except Exception as e:
        failed.append(f"robots_txt: {str(e)[:50]}")
    
    # Test sitemap
    try:
        sitemap_df = adv.sitemap_to_df("https://sydneycoachcharter.com.au/sitemap.xml")
        working.append(f"sitemap: {len(sitemap_df)} URLs found")
    except Exception as e:
        failed.append(f"sitemap: {str(e)[:50]}")
    
    # Test keyword generation
    try:
        keywords = adv.kw_generate(["bus charter", "sydney"], match_types=['exact'])
        working.append(f"keyword_gen: {len(keywords)} keywords generated")
    except Exception as e:
        failed.append(f"keyword_gen: {str(e)[:50]}")
    
    # Test URL analysis
    try:
        url_df = adv.url_to_df(["https://sydneycoachcharter.com.au/"])
        working.append(f"url_analysis: {len(url_df.columns)} features extracted")
    except Exception as e:
        failed.append(f"url_analysis: {str(e)[:50]}")
    
    print(f"\nWORKING ({len(working)}):")
    for item in working:
        print(f"  + {item}")
    
    print(f"\nFAILED ({len(failed)}):")
    for item in failed:
        print(f"  - {item}")
    
    # List key functions
    key_functions = [f for f in dir(adv) if not f.startswith('_') and 'crawl' in f.lower() or 'kw_' in f or 'sitemap' in f or 'robot' in f]
    print(f"\nKey SEO functions available: {len(key_functions)}")
    for func in key_functions[:10]:  # Show first 10
        print(f"  {func}")

if __name__ == "__main__":
    quick_test()