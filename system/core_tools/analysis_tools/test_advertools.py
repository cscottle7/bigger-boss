#!/usr/bin/env python3
"""
Test Advertools functionality and capabilities
"""

import advertools as adv
import pandas as pd
from datetime import datetime

def test_advertools_features():
    """Test what Advertools can actually do"""
    results = {
        "test_date": datetime.now().isoformat(),
        "advertools_version": adv.__version__,
        "available_functions": [],
        "working_features": {},
        "failed_features": {}
    }
    
    print(f"Testing Advertools v{adv.__version__}")
    
    # Test 1: Basic SEO Functions
    try:
        # Test robots.txt parsing
        robots_df = adv.robotstxt_to_df("https://sydneycoachcharter.com.au/robots.txt")
        results["working_features"]["robots_txt"] = {
            "status": "working",
            "sample_data": robots_df.head(3).to_dict() if not robots_df.empty else "empty"
        }
        print("✓ Robots.txt parsing: Working")
    except Exception as e:
        results["failed_features"]["robots_txt"] = str(e)
        print(f"✗ Robots.txt parsing: {e}")
    
    # Test 2: Sitemap Analysis
    try:
        sitemap_df = adv.sitemap_to_df("https://sydneycoachcharter.com.au/sitemap.xml")
        results["working_features"]["sitemap"] = {
            "status": "working", 
            "pages_found": len(sitemap_df),
            "sample_urls": sitemap_df['loc'].head(5).tolist() if 'loc' in sitemap_df.columns else []
        }
        print(f"✓ Sitemap analysis: Working - {len(sitemap_df)} URLs found")
    except Exception as e:
        results["failed_features"]["sitemap"] = str(e)
        print(f"✗ Sitemap analysis: {e}")
    
    # Test 3: Keyword Analysis Functions
    try:
        # Test keyword generation
        keywords = adv.kw_generate(["bus charter", "sydney"], 
                                 match_types=['exact', 'phrase', 'broad'])
        results["working_features"]["keyword_generation"] = {
            "status": "working",
            "sample_keywords": keywords[:10] if keywords else []
        }
        print("✓ Keyword generation: Working")
    except Exception as e:
        results["failed_features"]["keyword_generation"] = str(e)
        print(f"✗ Keyword generation: {e}")
    
    # Test 4: URL Analysis
    try:
        test_urls = ["https://sydneycoachcharter.com.au/", 
                     "https://sydneycoachcharter.com.au/get-a-quote/"]
        url_df = adv.url_to_df(test_urls)
        results["working_features"]["url_analysis"] = {
            "status": "working",
            "features_extracted": list(url_df.columns) if not url_df.empty else []
        }
        print("✓ URL analysis: Working")
    except Exception as e:
        results["failed_features"]["url_analysis"] = str(e)
        print(f"✗ URL analysis: {e}")
    
    # Test 5: Text Analysis
    try:
        text = "Sydney Coach Charter provides bus charter services"
        word_freq = adv.word_frequency(text.split())
        results["working_features"]["text_analysis"] = {
            "status": "working",
            "sample_analysis": dict(word_freq.most_common(5))
        }
        print("✓ Text analysis: Working")
    except Exception as e:
        results["failed_features"]["text_analysis"] = str(e)
        print(f"✗ Text analysis: {e}")
    
    # Test 6: SEO crawler (advanced feature)
    try:
        # Test if we can do basic crawling with advertools
        crawl_result = adv.crawl("https://sydneycoachcharter.com.au/", 
                               output_file="test_crawl.jl", 
                               follow_links=False,
                               custom_settings={'DEPTH_LIMIT': 0})
        results["working_features"]["seo_crawler"] = {
            "status": "working",
            "note": "Basic crawling available"
        }
        print("✓ SEO crawler: Working")
    except Exception as e:
        results["failed_features"]["seo_crawler"] = str(e)
        print(f"✗ SEO crawler: {e}")
    
    # Get list of available functions
    results["available_functions"] = [attr for attr in dir(adv) 
                                     if not attr.startswith('_') and callable(getattr(adv, attr))]
    
    return results

if __name__ == "__main__":
    print("Testing Advertools Capabilities")
    print("=" * 50)
    
    results = test_advertools_features()
    
    print("\n" + "=" * 50)
    print("ADVERTOOLS CAPABILITY SUMMARY")
    print("=" * 50)
    
    print(f"\n✓ WORKING FEATURES ({len(results['working_features'])} total):")
    for feature, details in results["working_features"].items():
        print(f"   - {feature}: {details['status']}")
    
    print(f"\n✗ FAILED FEATURES ({len(results['failed_features'])} total):")
    for feature, error in results["failed_features"].items():
        print(f"   - {feature}: {error}")
    
    print(f"\nTotal functions available: {len(results['available_functions'])}")
    print(f"Key functions: kw_generate, sitemap_to_df, robotstxt_to_df, crawl, word_frequency")
    
    # Save results
    import json
    with open("analysis_tools/advertools_test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: analysis_tools/advertools_test_results.json")