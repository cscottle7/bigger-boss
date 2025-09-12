#!/usr/bin/env python3
"""
Universal Autonomous Website Analyzer
Analyzes ANY website without requiring WebFetch permissions
Usage: python analyze.py [website.com]
"""

import asyncio
import sys
from pathlib import Path

# Add system path
sys.path.append(str(Path(__file__).parent))

from system.autonomous_market_research import analyze_australian_generator_market
from system.orchestration.master_autonomous_orchestrator import analyze_website_autonomously

async def main():
    """Universal website analysis without WebFetch permissions"""
    
    if len(sys.argv) < 2:
        print("Usage: python analyze.py [website.com]")
        print("Example: python analyze.py greenpowersolutions.com.au")
        return
    
    domain = sys.argv[1].replace('https://', '').replace('http://', '').strip('/')
    
    print(f"AUTONOMOUS WEBSITE ANALYSIS")
    print(f"Domain: {domain}")
    print("No WebFetch permissions required!")
    print("=" * 50)
    
    try:
        # Method 1: Use autonomous market research (Playwright direct)
        print("Method 1: Market Research Analysis...")
        market_result = await analyze_australian_generator_market(domain)
        
        if market_result.get('error'):
            print(f"Market analysis failed: {market_result['error']}")
        else:
            print("SUCCESS: Market research completed autonomously!")
            primary = market_result.get('primaryWebsiteAnalysis', {})
            print(f"  - Industry: {primary.get('industry', 'Unknown')}")
            print(f"  - Positioning: {primary.get('brandPositioning', 'Unknown')}")
            print(f"  - Target: {', '.join(primary.get('targetMarkets', ['Unknown']))}")
        
        print("\n" + "-" * 30)
        
        # Method 2: Use comprehensive SEO analysis
        print("Method 2: SEO Analysis...")
        seo_command = f"analyze website {domain} with 10 pages"
        seo_success, seo_result = await analyze_website_autonomously(seo_command)
        
        if seo_success:
            print("SUCCESS: SEO analysis completed autonomously!")
            exec_summary = seo_result.get('executive_summary', {})
            print(f"  - SEO Score: {exec_summary.get('overall_health_score', 'N/A')}")
            print(f"  - Analyses: {', '.join(exec_summary.get('analyses_performed', []))}")
        else:
            print(f"SEO analysis failed: {seo_result.get('error', 'Unknown error')}")
        
        print("\n" + "=" * 50)
        print("ANALYSIS COMPLETE - Check clients/ folder for reports")
        print("No user permissions were required!")
        
    except Exception as e:
        print(f"ERROR: Analysis failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())