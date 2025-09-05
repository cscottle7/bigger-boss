#!/usr/bin/env python3
"""
Test Script for Autonomous Analysis Capabilities
Tests the full autonomous analysis system without requiring user permission
"""

import asyncio
import sys
import json
from pathlib import Path

# Add system path for imports
sys.path.append(str(Path(__file__).parent))

from system.orchestration.master_autonomous_orchestrator import master_orchestrator

async def test_autonomous_analysis():
    """Test autonomous analysis with a simple website"""
    
    print("Testing Autonomous Analysis Capabilities")
    print("=" * 50)
    
    # Test command
    test_command = "analyze website sydneycoachcharter.com.au with 10 pages"
    
    print(f"Test Command: {test_command}")
    print("Starting autonomous analysis...")
    
    try:
        # Execute autonomous analysis
        success, result = await master_orchestrator.execute_autonomous_analysis(test_command)
        
        if success:
            print("SUCCESS: Autonomous analysis completed successfully!")
            print("\nExecutive Summary:")
            
            exec_summary = result.get('executive_summary', {})
            print(f"   • Domain: {exec_summary.get('domain')}")
            print(f"   • Analyses Performed: {', '.join(exec_summary.get('analyses_performed', []))}")
            print(f"   • Overall Health Score: {exec_summary.get('overall_health_score', 'N/A')}")
            
            key_findings = exec_summary.get('key_findings', [])
            if key_findings:
                print(f"   • Key Findings: {len(key_findings)} insights generated")
                for finding in key_findings[:3]:  # Show first 3
                    print(f"     - {finding}")
            
            # Show session status
            session_status = result.get('session_status', {})
            print(f"\nSession Statistics:")
            print(f"   • File Writes: {session_status.get('counters', {}).get('file_writes', 0)}")
            print(f"   • API Calls: {session_status.get('counters', {}).get('api_calls', 0)}")
            print(f"   • Analysis Runs: {session_status.get('counters', {}).get('analysis_runs', 0)}")
            
            # Show error recovery stats
            error_summary = result.get('error_summary', {})
            recovery_stats = error_summary.get('recovery_stats', {})
            if recovery_stats.get('total_errors', 0) > 0:
                print(f"\nError Recovery:")
                print(f"   • Total Errors: {recovery_stats.get('total_errors', 0)}")
                print(f"   • Successful Recoveries: {recovery_stats.get('successful_recoveries', 0)}")
                print(f"   • Recovery Rate: {recovery_stats.get('recovery_rate', 0):.1f}%")
            
        else:
            print("ERROR: Autonomous analysis failed!")
            print(f"Error: {result.get('error', 'Unknown error')}")
            
            # Show what was attempted
            if 'command' in result:
                print(f"Command attempted: {result['command']}")
        
        print("\n" + "=" * 50)
        return success
        
    except Exception as e:
        print(f"ERROR: Test failed with exception: {e}")
        return False

async def test_system_capabilities():
    """Test system capabilities and configuration"""
    
    print("Testing System Capabilities")
    print("=" * 30)
    
    try:
        capabilities = master_orchestrator.get_autonomous_capabilities()
        
        print("Autonomous Operations Status:")
        autonomous_ops = capabilities.get('autonomous_operations', {})
        for operation, enabled in autonomous_ops.items():
            status = "ENABLED" if enabled else "DISABLED"
            print(f"   • {operation.replace('_', ' ').title()}: {status}")
        
        print("\nSupported Commands:")
        commands = capabilities.get('supported_commands', [])
        for cmd in commands[:5]:  # Show first 5
            print(f"   • {cmd}")
        
        session_status = capabilities.get('session_status', {})
        available_services = session_status.get('available_services', [])
        if available_services:
            print(f"\nAvailable API Services: {', '.join(available_services)}")
        else:
            print("\nWARNING: No API services configured (analysis will be limited to SEO crawling)")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Capabilities test failed: {e}")
        return False

def print_setup_instructions():
    """Print setup instructions for full functionality"""
    print("\nSETUP INSTRUCTIONS FOR FULL FUNCTIONALITY")
    print("=" * 50)
    print("For complete autonomous analysis, configure these API credentials:")
    print("")
    print("1. GTmetrix Performance Testing:")
    print("   • Set environment variable: GTMETRIX_API_KEY=your_api_key")
    print("   • Set environment variable: GTMETRIX_USERNAME=your_username")
    print("")
    print("2. Competitive Analysis (SerpAPI):")
    print("   • Set environment variable: SERPAPI_KEY=your_api_key")
    print("")
    print("3. Google Search Insights:")
    print("   • Set environment variable: GOOGLE_API_KEY=your_api_key")
    print("   • Set environment variable: GOOGLE_CSE_ID=your_cse_id")
    print("")
    print("Without these, the system will perform SEO analysis only.")
    print("=" * 50)

async def main():
    """Main test execution"""
    print("BIGGER BOSS AGENT - AUTONOMOUS ANALYSIS TEST")
    print("=" * 60)
    
    # Test system capabilities first
    print("Phase 1: System Capabilities Test")
    capabilities_ok = await test_system_capabilities()
    
    if not capabilities_ok:
        print("❌ System capabilities test failed - cannot proceed")
        return False
    
    print("\nPhase 2: Autonomous Analysis Test")
    # Test autonomous analysis
    analysis_ok = await test_autonomous_analysis()
    
    # Print setup instructions
    print_setup_instructions()
    
    # Final summary
    print("\nTEST SUMMARY")
    print("=" * 20)
    if analysis_ok:
        print("SUCCESS: AUTONOMOUS ANALYSIS IS WORKING!")
        print("You can now use commands like:")
        print('   • "analyze website example.com"')
        print('   • "seo audit example.com with 25 pages"')
        print('   • "performance test example.com"')
    else:
        print("ERROR: Autonomous analysis needs configuration")
        print("Review the setup instructions above")
    
    return analysis_ok

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)