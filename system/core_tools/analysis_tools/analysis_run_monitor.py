#!/usr/bin/env python3
"""
Analysis Run Monitor - Integrates with existing agents to track usage
"""

import json
import os
from datetime import datetime
import time
from tool_usage_tracker import AnalysisRunTracker
from typing import List, Dict, Any

class AnalysisRunMonitor:
    """High-level monitor for complete analysis runs"""
    
    def __init__(self, website_url: str):
        self.website_url = website_url
        self.tracker = AnalysisRunTracker(website_url)
        self.run_log = []
        
    def simulate_comprehensive_analysis(self):
        """Simulate a comprehensive analysis run to demonstrate tracking"""
        
        print(f"Starting comprehensive analysis of {self.website_url}")
        print("=" * 70)
        
        # Phase 1: Foundation Analysis
        print("\nPhase 1: Foundation Analysis")
        
        # WebFetch (always used)
        print("  > Using WebFetch to extract basic content...")
        time.sleep(0.5)  # Simulate execution time
        self.tracker.mark_tool_used("webfetch", 2.3, True, data_points=25, 
                                   output_files=["homepage_content.html"])
        print("  + WebFetch: Success (2.3s, 25 data points)")
        
        # Scrapy crawler
        print("  > Running Scrapy multi-page crawler...")
        time.sleep(1.0)
        self.tracker.mark_tool_used("scrapy", 45.8, True, data_points=280,
                                   output_files=["crawl_data.json", "seo_extraction.csv"])
        print("  + Scrapy: Success (45.8s, 280 data points, 2 files)")
        
        # Multi-page SEO extraction
        print("  > Generating multi-page SEO extraction table...")
        time.sleep(0.8)
        self.tracker.mark_tool_used("multi_page_seo", 12.1, True, data_points=308,
                                   output_files=["multi_page_seo_extraction.csv", "seo_report.md"])
        print("  + Multi-page SEO: Success (12.1s, 308 data points)")
        
        # Invoke technical SEO analyst
        self.tracker.mark_agent_invoked("technical_seo_analyst", 18.5, 
                                       ["webfetch", "scrapy", "multi_page_seo"], 
                                       True, "high")
        
        # Phase 2: Advanced Analysis
        print("\nPhase 2: Advanced Analysis")
        
        # Playwright browser automation
        print("  > Running Playwright browser automation...")
        time.sleep(2.0)
        self.tracker.mark_tool_used("playwright", 23.7, True, data_points=45,
                                   output_files=["desktop_screenshot.png", "tablet_screenshot.png", "mobile_screenshot.png"])
        print("  + Playwright: Success (23.7s, 45 data points, 3 screenshots)")
        
        # Invoke UX/UI analyst
        self.tracker.mark_agent_invoked("ux_ui_analyst", 31.2,
                                       ["playwright", "webfetch"],
                                       True, "high")
        
        # SerpAPI keyword research
        print("  > Conducting keyword research with SerpAPI...")
        time.sleep(1.5)
        self.tracker.mark_tool_used("serpapi", 8.9, True, data_points=50,
                                   output_files=["keyword_research.json"])
        print("  + SerpAPI: Success (8.9s, 50 keyword data points)")
        
        # Invoke keyword researcher agent
        self.tracker.mark_agent_invoked("keyword_researcher", 12.4,
                                       ["serpapi", "advertools"],
                                       True, "medium")
        
        # Advertools SEO analysis
        print("  > Running Advertools SEO analysis...")
        time.sleep(0.7)
        self.tracker.mark_tool_used("advertools", 5.2, True, data_points=15,
                                   output_files=["robots_analysis.json"])
        print("  + Advertools: Success (5.2s, 15 data points)")
        
        # Phase 3: AI & Content Analysis
        print("\nPhase 3: AI & Content Analysis")
        
        # Jina AI content processing
        print("  > Processing content with Jina AI...")
        time.sleep(1.2)
        self.tracker.mark_tool_used("jina_ai", 7.8, True, data_points=32,
                                   output_files=["content_embeddings.json"])
        print("  + Jina AI: Success (7.8s, 32 embeddings)")
        
        # Invoke AI specialist
        self.tracker.mark_agent_invoked("ai_specialist_agent", 25.6,
                                       ["jina_ai", "webfetch"],
                                       True, "high")
        
        # Content strategy
        self.tracker.mark_agent_invoked("content_strategist", 15.3,
                                       ["scrapy", "serpapi", "jina_ai"],
                                       True, "medium")
        
        # Phase 4: Quality Assurance
        print("\nPhase 4: Quality Assurance")
        
        # Brand compliance audit
        self.tracker.mark_agent_invoked("brand_compliance_auditor", 8.7,
                                       ["scrapy", "webfetch"],
                                       True, "high")
        
        # Universal quality gate
        self.tracker.mark_agent_invoked("universal_quality_gate_orchestrator", 6.2,
                                       ["all_previous_outputs"],
                                       True, "high")
        
        # Some tools we didn't use (to show unused tracking)
        # - GTmetrix (API connection issue)
        # - ChromaDB (not needed for this analysis type)
        # - Various other specialist agents
        
        # Update final metrics
        self.tracker.update_metrics(
            total_pages_analyzed=28,
            total_data_points_extracted=755,
            seo_issues_found=12,
            performance_score=7.2,
            accessibility_issues=3,
            api_calls_made=15,
            files_generated=9,
            screenshots_taken=3
        )
        
        # Set coverage information
        self.tracker.add_coverage_info(
            requested=["Complete SEO audit", "UX/UI analysis", "AI optimization", "Keyword research"],
            delivered=["Multi-page SEO extraction", "Real browser testing", "AI content analysis", "SERP keyword data"],
            missing=[],  # Nothing missing in this simulation
            limitations=["GTmetrix API temporarily unavailable"]
        )
        
        print(f"\nAnalysis complete! Total execution time: {sum(tool.execution_time for tool in self.tracker.tools.values() if tool.used):.1f}s")
        
        return self.tracker
    
    def generate_run_comparison(self, previous_runs: List[str] = None):
        """Compare current run with previous runs"""
        if not previous_runs:
            return "No previous runs to compare"
        
        comparison = f"""# Analysis Run Comparison

## Current Run
- Tools Used: {len([t for t in self.tracker.tools.values() if t.used])}/{len(self.tracker.tools)}
- Agents Invoked: {len([a for a in self.tracker.agents.values() if a.invoked])}/{len(self.tracker.agents)}
- Data Points: {self.tracker.metrics.get('total_data_points_extracted', 0)}
- Files Generated: {self.tracker.metrics.get('files_generated', 0)}

## Recommendations
- Consider using unused tools if relevant to analysis goals
- Missing agents may indicate incomplete analysis coverage
- Compare data point extraction with previous runs for consistency
"""
        return comparison

def main():
    """Demonstrate the analysis run monitoring system"""
    
    # Create monitor for a website
    monitor = AnalysisRunMonitor("https://sydneycoachcharter.com.au")
    
    # Run comprehensive analysis simulation
    tracker = monitor.simulate_comprehensive_analysis()
    
    # Generate and save report
    print("\nGenerating comprehensive usage report...")
    report_file = tracker.save_report()
    
    print(f"\n[SUCCESS] Usage report saved to: {report_file}")
    print(f"[DATA] JSON data saved to: {report_file.replace('.md', '.json')}")
    
    # Show summary statistics
    summary = tracker.finalize_run()
    print(f"\n[SUMMARY] STATISTICS:")
    print(f"   - Tool Coverage: {summary['run_summary']['tool_coverage']}")
    print(f"   - Agent Coverage: {summary['run_summary']['agent_coverage']}")
    print(f"   - Total Data Points: {summary['metrics']['total_data_points_extracted']}")
    print(f"   - Files Generated: {summary['metrics']['files_generated']}")
    print(f"   - API Calls Made: {summary['metrics']['api_calls_made']}")
    
    # Show what wasn't used
    unused_tools = len(summary['tools_unused'])
    unused_agents = len(summary['agents_unused'])
    
    if unused_tools > 0:
        print(f"\n[WARNING] UNUSED TOOLS ({unused_tools}):")
        for tool in summary['tools_unused'][:5]:  # Show first 5
            print(f"     - {tool}")
        if unused_tools > 5:
            print(f"     ... and {unused_tools - 5} more")
    
    if unused_agents > 0:
        print(f"\n[WARNING] UNUSED AGENTS ({unused_agents}):")
        for agent in summary['agents_unused'][:5]:  # Show first 5
            print(f"     - {agent}")
        if unused_agents > 5:
            print(f"     ... and {unused_agents - 5} more")
    
    print(f"\n[RECOMMENDATIONS] SYSTEM IMPROVEMENTS:")
    if unused_tools > len(summary['tools_used']):
        print("   - Consider why many tools went unused - may indicate incomplete analysis")
    if unused_agents > len(summary['agents_invoked']):
        print("   - Many agents not invoked - ensure comprehensive coverage")
    
    print("   - Review unused tools/agents to identify analysis gaps")
    print("   - Compare with previous runs to ensure consistency")
    print("   - Use this data to improve agent orchestration")

if __name__ == "__main__":
    main()