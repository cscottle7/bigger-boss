#!/usr/bin/env python3
"""
Autonomous Market Research System
Performs complete market analysis without requiring WebFetch permissions
Uses Playwright directly for autonomous operation
"""

import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime

# Add system path for imports
sys.path.append(str(Path(__file__).parent.parent))

from system.core_tools.autonomous_web_access import autonomous_web
from system.orchestration.autonomous_operation_manager import autonomous_manager

async def analyze_australian_generator_market(domain: str) -> dict:
    """
    Autonomous analysis of Australian generator market
    No WebFetch permissions required - uses Playwright directly
    """
    
    print(f"Starting autonomous market analysis for {domain}")
    
    try:
        # Analyze primary website autonomously
        print("Analyzing primary website...")
        primary_url = f"https://{domain}"
        primary_analysis = await autonomous_web.fetch_website_content(primary_url, analyze_brand=True)
        
        if not primary_analysis.get('success'):
            print(f"Failed to analyze primary website: {primary_analysis.get('error')}")
            return {'error': 'Primary website analysis failed'}
        
        # Extract brand information
        brand_data = primary_analysis['data'].get('brandAnalysis', {})
        detected_industry = brand_data.get('detectedIndustry', 'general')
        
        print(f"Detected industry: {detected_industry}")
        
        # Get competitor URLs for the industry
        competitor_urls = await autonomous_web.get_competitor_urls(domain, detected_industry)
        print(f"Found {len(competitor_urls)} potential competitors")
        
        # Perform market position analysis
        print("Analyzing market position...")
        market_analysis = await autonomous_web.analyze_market_position(primary_url, competitor_urls)
        
        if not market_analysis.get('success'):
            print(f"Market analysis failed: {market_analysis.get('error')}")
            return market_analysis
        
        # Generate comprehensive report
        report = {
            'analysisMetadata': {
                'domain': domain,
                'analysisDate': datetime.now().isoformat(),
                'analysisType': 'Australian Market Position Analysis',
                'autonomous': True
            },
            'primaryWebsiteAnalysis': {
                'url': primary_url,
                'title': primary_analysis['data'].get('title', 'No title'),
                'industry': detected_industry,
                'brandPositioning': brand_data.get('primaryPositioning', 'unknown'),
                'serviceTypes': brand_data.get('serviceTypes', []),
                'targetMarkets': brand_data.get('targetMarkets', []),
                'locations': primary_analysis['data'].get('locations', [])
            },
            'competitiveAnalysis': {
                'competitorsAnalyzed': len(market_analysis.get('competitors', [])),
                'marketComparison': market_analysis.get('marketComparison', {}),
                'competitorData': market_analysis.get('competitors', [])
            },
            'strategicRecommendations': market_analysis.get('marketComparison', {}).get('recommendations', []),
            'marketOpportunities': market_analysis.get('marketComparison', {}).get('marketGaps', [])
        }
        
        # Save report to client folder
        await save_market_research_report(report, domain)
        
        print("Market analysis completed successfully!")
        return report
        
    except Exception as e:
        error_msg = f"Market analysis failed: {str(e)}"
        print(error_msg)
        return {'error': error_msg}

async def save_market_research_report(report: dict, domain: str):
    """Save market research report to client folder"""
    
    try:
        # Check file operation permissions
        client_domain = domain.replace('.', '_').replace('-', '_')
        client_folder = Path(f"clients/{client_domain}/research")
        
        can_write, message = autonomous_manager.can_perform_operation(
            'file_operations', 
            path=str(client_folder)
        )
        
        if not can_write:
            print(f"Cannot save report: {message}")
            return
        
        # Create client folder structure
        client_folder.mkdir(parents=True, exist_ok=True)
        
        # Save detailed JSON report
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = client_folder / f"autonomous_market_research_{timestamp}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # Create markdown summary
        summary_file = client_folder / f"market_research_summary_{timestamp}.md"
        markdown_summary = generate_markdown_summary(report)
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(markdown_summary)
        
        # Track file operations
        autonomous_manager.session_tracker.increment('file_writes', 2)
        
        print(f"Market research report saved: {report_file}")
        print(f"Summary report saved: {summary_file}")
        
    except Exception as e:
        print(f"Failed to save market research report: {e}")

def generate_markdown_summary(report: dict) -> str:
    """Generate markdown summary of market research"""
    
    metadata = report.get('analysisMetadata', {})
    primary = report.get('primaryWebsiteAnalysis', {})
    competitive = report.get('competitiveAnalysis', {})
    
    markdown = f"""# Market Research Analysis: {primary.get('url', 'Unknown')}

**Analysis Date:** {metadata.get('analysisDate', 'Unknown')}  
**Domain:** {metadata.get('domain', 'Unknown')}  
**Analysis Type:** {metadata.get('analysisType', 'Market Analysis')}  
**Autonomous Analysis:** ✅ Yes

## Primary Website Analysis

- **Industry:** {primary.get('industry', 'Unknown').title()}
- **Brand Positioning:** {primary.get('brandPositioning', 'Unknown').title()}
- **Target Markets:** {', '.join(primary.get('targetMarkets', ['Unknown']))}
- **Service Types:** {', '.join(primary.get('serviceTypes', ['Unknown']))}
- **Geographic Focus:** {', '.join(primary.get('locations', ['Unknown']))}

## Competitive Landscape

- **Competitors Analyzed:** {competitive.get('competitorsAnalyzed', 0)}
- **Market Position:** Analysis completed autonomously

### Competitor Websites
"""
    
    # Add competitor details
    competitors = competitive.get('competitorData', [])
    for i, comp in enumerate(competitors, 1):
        comp_data = comp.get('data', {})
        comp_brand = comp_data.get('brandAnalysis', {})
        markdown += f"""
{i}. **{comp.get('url', 'Unknown')}**
   - Industry: {comp_brand.get('detectedIndustry', 'Unknown').title()}
   - Positioning: {comp_brand.get('primaryPositioning', 'Unknown').title()}
   - Services: {', '.join(comp_brand.get('serviceTypes', ['Unknown']))}
"""
    
    # Add recommendations
    recommendations = report.get('strategicRecommendations', [])
    if recommendations:
        markdown += f"""
## Strategic Recommendations

"""
        for i, rec in enumerate(recommendations, 1):
            markdown += f"{i}. {rec}\n"
    
    # Add market opportunities
    opportunities = report.get('marketOpportunities', [])
    if opportunities:
        markdown += f"""
## Market Opportunities

"""
        for i, opp in enumerate(opportunities, 1):
            markdown += f"{i}. {opp.title()} positioning appears underserved\n"
    
    markdown += f"""

---
*Report generated autonomously by Bigger Boss Agent System*  
*No WebFetch permissions required - Analysis via Playwright*
"""
    
    return markdown

async def main():
    """Main execution function for testing"""
    
    if len(sys.argv) > 1:
        domain = sys.argv[1]
    else:
        domain = "greenpowersolutions.com.au"
    
    print(f"AUTONOMOUS MARKET RESEARCH")
    print(f"Domain: {domain}")
    print("=" * 50)
    
    result = await analyze_australian_generator_market(domain)
    
    if result.get('error'):
        print(f"ERROR: Analysis failed: {result['error']}")
        return False
    
    print("\nSUCCESS: ANALYSIS COMPLETE!")
    print("=" * 30)
    
    primary = result.get('primaryWebsiteAnalysis', {})
    competitive = result.get('competitiveAnalysis', {})
    
    print(f"Industry: {primary.get('industry', 'Unknown').title()}")
    print(f"Brand Positioning: {primary.get('brandPositioning', 'Unknown').title()}")
    print(f"Competitors Analyzed: {competitive.get('competitorsAnalyzed', 0)}")
    
    recommendations = result.get('strategicRecommendations', [])
    if recommendations:
        print(f"Strategic Recommendations: {len(recommendations)}")
        for rec in recommendations[:2]:  # Show first 2
            print(f"  - {rec}")
    
    return True

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)