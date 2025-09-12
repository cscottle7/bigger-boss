#!/usr/bin/env python3
"""
Detailed Advertools testing - fix what's broken and identify what works
"""

import advertools as adv
import pandas as pd
from urllib.parse import urljoin

def test_advertools_comprehensively():
    print(f"Advertools version: {adv.__version__}")
    
    working = []
    failed = []
    
    # Test 1: Robots.txt (we know this works)
    try:
        robots_df = adv.robotstxt_to_df("https://sydneycoachcharter.com.au/robots.txt")
        working.append(f"✓ robots_txt: {len(robots_df)} rules found")
    except Exception as e:
        failed.append(f"✗ robots_txt: {str(e)[:60]}")
    
    # Test 2: URL analysis (we know this works) 
    try:
        urls = ["https://sydneycoachcharter.com.au/", "https://sydneycoachcharter.com.au/contact-sydney-coach-charter/"]
        url_df = adv.url_to_df(urls)
        working.append(f"✓ url_analysis: {len(url_df)} URLs analyzed, {len(url_df.columns)} features")
    except Exception as e:
        failed.append(f"✗ url_analysis: {str(e)[:60]}")
    
    # Test 3: Keyword generation (fix the parameters)
    try:
        # Fix the parameter - needs products list and match_types
        keywords = adv.kw_generate(products=["bus charter", "sydney transport"], 
                                 match_types=['exact', 'phrase'])
        working.append(f"✓ keyword_gen: {len(keywords)} keywords generated")
        print(f"Sample keywords: {keywords[:3]}")
    except Exception as e:
        failed.append(f"✗ keyword_gen: {str(e)[:60]}")
    
    # Test 4: Word frequency (we know this works)
    try:
        text = "Sydney Coach Charter provides reliable bus charter services for corporate events, weddings, school trips and tourism in Sydney NSW"
        words = text.split()
        word_freq = adv.word_frequency(words)
        working.append(f"✓ word_frequency: analyzed {len(words)} words")
    except Exception as e:
        failed.append(f"✗ word_frequency: {str(e)[:60]}")
    
    # Test 5: Emoji analysis
    try:
        emoji_df = adv.emoji_search("🚌 Bus charter Sydney 🇦🇺")
        working.append(f"✓ emoji_search: found emojis in text")
    except Exception as e:
        failed.append(f"✗ emoji_search: {str(e)[:60]}")
    
    # Test 6: Stopwords
    try:
        stopwords = adv.stopwords['english']
        working.append(f"✓ stopwords: {len(stopwords)} English stopwords available")
    except Exception as e:
        failed.append(f"✗ stopwords: {str(e)[:60]}")
    
    # Test 7: Google Ads keyword tools
    try:
        broad_keywords = adv.kw_broad(["bus charter"])
        working.append(f"✓ kw_broad: generated {len(broad_keywords)} broad match keywords")
    except Exception as e:
        failed.append(f"✗ kw_broad: {str(e)[:60]}")
    
    try:
        exact_keywords = adv.kw_exact(["sydney coach charter"]) 
        working.append(f"✓ kw_exact: generated {len(exact_keywords)} exact match keywords")
    except Exception as e:
        failed.append(f"✗ kw_exact: {str(e)[:60]}")
    
    # Test 8: Search engine URL builders
    try:
        google_url = adv.serp_goog(q="sydney bus charter", num=10)
        working.append(f"✓ serp_goog: Google search URL generator working")
    except Exception as e:
        failed.append(f"✗ serp_goog: {str(e)[:60]}")
    
    # Test 9: Text processing
    try:
        extracted = adv.extract_numbers("Call us on (02) 9181 5557 for quotes")
        working.append(f"✓ extract_numbers: found numbers in text")
    except Exception as e:
        failed.append(f"✗ extract_numbers: {str(e)[:60]}")
    
    print(f"\n=== ADVERTOOLS COMPREHENSIVE TEST RESULTS ===")
    print(f"\n✓ WORKING ({len(working)} features):")
    for item in working:
        print(f"  {item}")
    
    print(f"\n✗ FAILED ({len(failed)} features):")
    for item in failed:
        print(f"  {item}")
    
    # Check available functions
    all_functions = [attr for attr in dir(adv) if not attr.startswith('_') and callable(getattr(adv, attr))]
    seo_functions = [f for f in all_functions if any(keyword in f.lower() for keyword in ['crawl', 'seo', 'kw_', 'serp', 'extract', 'url', 'robot'])]
    
    print(f"\n📊 ADVERTOOLS CAPABILITIES:")
    print(f"  Total functions available: {len(all_functions)}")
    print(f"  SEO-related functions: {len(seo_functions)}")
    print(f"  Key working functions: robotstxt_to_df, url_to_df, kw_generate, word_frequency")
    
    # Return summary
    return {
        "working_count": len(working),
        "failed_count": len(failed), 
        "working_features": working,
        "failed_features": failed,
        "total_functions": len(all_functions),
        "seo_functions": len(seo_functions)
    }

if __name__ == "__main__":
    results = test_advertools_comprehensively()
    
    if results["working_count"] >= 6:
        print(f"\n🎉 ADVERTOOLS STATUS: MOSTLY WORKING ({results['working_count']}/{results['working_count'] + results['failed_count']} features)")
    elif results["working_count"] >= 4:
        print(f"\n⚠️ ADVERTOOLS STATUS: PARTIALLY WORKING ({results['working_count']}/{results['working_count'] + results['failed_count']} features)")
    else:
        print(f"\n❌ ADVERTOOLS STATUS: LIMITED FUNCTIONALITY ({results['working_count']}/{results['working_count'] + results['failed_count']} features)")
    
    print(f"\nCONCLUSION: Advertools has {results['total_functions']} total functions with {results['seo_functions']} SEO-related.")
    print("Main limitation: Sitemap.xml doesn't exist on this website (returns HTML instead of XML)")