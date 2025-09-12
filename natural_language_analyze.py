#!/usr/bin/env python3
"""
Natural Language Website Analysis Interface
Use plain English commands to analyze any website autonomously
"""

import asyncio
import sys
from pathlib import Path

# Add system path
sys.path.append(str(Path(__file__).parent))

from system.orchestration.master_autonomous_orchestrator import analyze_website_autonomously

async def main():
    """Natural language interface for website analysis"""
    
    if len(sys.argv) < 2:
        print("NATURAL LANGUAGE WEBSITE ANALYZER")
        print("=" * 40)
        print("Usage examples:")
        print('  python natural_language_analyze.py "analyze website example.com"')
        print('  python natural_language_analyze.py "seo audit example.com with 25 pages"')
        print('  python natural_language_analyze.py "comprehensive analysis of example.com"')
        print('  python natural_language_analyze.py "crawl website example.com"')
        return
    
    # Get the natural language command
    command = " ".join(sys.argv[1:])
    
    print("NATURAL LANGUAGE ANALYSIS")
    print("=" * 30)
    print(f"Command: {command}")
    print("Processing your request autonomously...")
    print()
    
    try:
        # Use the master orchestrator with natural language processing
        success, result = await analyze_website_autonomously(command)
        
        if success:
            print("SUCCESS: Analysis completed autonomously!")
            print()
            
            # Show executive summary
            exec_summary = result.get('executive_summary', {})
            print("RESULTS SUMMARY:")
            print(f"  Domain: {exec_summary.get('domain', 'N/A')}")
            print(f"  Analyses Performed: {', '.join(exec_summary.get('analyses_performed', ['None']))}")
            print(f"  Overall Health Score: {exec_summary.get('overall_health_score', 'N/A')}")
            
            # Show key findings
            key_findings = exec_summary.get('key_findings', [])
            if key_findings:
                print("  Key Findings:")
                for finding in key_findings[:3]:  # Show first 3
                    print(f"    - {finding}")
            
            # Show session info
            session_status = result.get('session_status', {})
            counters = session_status.get('counters', {})
            print()
            print("AUTONOMOUS OPERATIONS:")
            print(f"  File Reports Generated: {counters.get('file_writes', 0)}")
            print(f"  Analysis Runs: {counters.get('analysis_runs', 0)}")
            print("  No user permissions required!")
            
        else:
            print("ERROR: Analysis failed")
            print(f"Error: {result.get('error', 'Unknown error')}")
            
            # Show what was attempted
            if 'command' in result:
                print(f"Command attempted: {result['command']}")
        
    except Exception as e:
        print(f"FATAL ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(main())