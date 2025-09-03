#!/usr/bin/env python3
"""
Natural Language Document Converter Demo
Demonstrates the conversational interface with real examples
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

from natural_language_converter import NaturalLanguageConverter

def demonstrate_converter():
    """Demonstrate the natural language converter with realistic scenarios"""
    
    print("🎭 NATURAL LANGUAGE CONVERTER DEMONSTRATION")
    print("==========================================")
    print("Showing how users can convert documents using plain English")
    print()
    
    converter = NaturalLanguageConverter()
    
    # Realistic user scenarios
    scenarios = [
        {
            'context': "User wants to convert a specific SOP",
            'request': "Convert the token optimisation SOP to Word format",
            'explanation': "User references a specific SOP by its key terms"
        },
        {
            'context': "User wants to batch convert all SOPs", 
            'request': "Turn all my SOPs into Word documents",
            'explanation': "User wants bulk conversion of all Standard Operating Procedures"
        },
        {
            'context': "User searches for a file and converts it",
            'request': "Find the Universal Orchestrator checklist and convert it to docx",
            'explanation': "User combines search and conversion in one natural request"
        },
        {
            'context': "User references a file casually",
            'request': "Export that content refinement guide as a Word document", 
            'explanation': "User uses casual reference 'that guide' expecting system to understand"
        },
        {
            'context': "User wants to convert reports",
            'request': "Convert my analysis reports to Word format",
            'explanation': "User wants to convert analytical documents for sharing"
        },
        {
            'context': "Unclear request needing clarification",
            'request': "Convert my stuff to Word",
            'explanation': "Vague request that requires clarification from system"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{'='*60}")
        print(f"SCENARIO {i}: {scenario['context']}")
        print(f"{'='*60}")
        print(f"User Request: \"{scenario['request']}\"")
        print(f"Context: {scenario['explanation']}")
        print()
        print("🤖 System Response:")
        print("-" * 20)
        
        # Process the request
        result = converter.process_natural_request(scenario['request'])
        
        # Display formatted response
        display_scenario_result(result)
        
        print()
        input("Press Enter to continue to next scenario...")
    
    # Show final session summary
    print(f"\n{'='*60}")
    print("SESSION COMPLETE")
    print(f"{'='*60}")
    
    summary = converter.get_conversation_summary()
    print(f"📊 Demonstration Summary:")
    print(f"   • Total Scenarios: {len(scenarios)}")
    print(f"   • System Requests: {summary['total_requests']}")
    print(f"   • Successful Operations: {summary['successful_operations']}")
    print(f"   • Files Converted: {summary['total_files_converted']}")
    print(f"   • Session Duration: {summary['session_duration_minutes']:.1f} minutes")
    
    print(f"\n✅ Natural Language Converter demonstration complete!")
    print("The system successfully interpreted user requests and provided appropriate responses.")

def display_scenario_result(result):
    """Display scenario result in a clean format"""
    
    status = result.get('status', 'unknown')
    message = result.get('message', 'No response')
    
    # Status mapping
    status_display = {
        'success': '✅ SUCCESS',
        'batch_success': '🎉 BATCH SUCCESS',
        'batch_partial': '⚠️ PARTIAL SUCCESS', 
        'needs_clarification': '❓ NEEDS CLARIFICATION',
        'file_not_found': '🔍 FILE NOT FOUND',
        'multiple_matches': '📁 MULTIPLE FILES FOUND',
        'multiple_found_batch_option': '📂 MULTIPLE FILES - BATCH OPTION',
        'conversion_error': '❌ CONVERSION ERROR',
        'system_error': '⚠️ SYSTEM ERROR',
        'search_no_results': '🔍 NO SEARCH RESULTS'
    }
    
    print(f"Status: {status_display.get(status, f'📋 {status.upper()}')}")
    print(f"Response: {message}")
    
    # Show key information based on response type
    if 'details' in result:
        print(f"\n📋 Conversion Details:")
        details = result['details']
        if 'source_file' in details:
            print(f"   Source: {details['source_file']}")
        if 'output_file' in details:
            print(f"   Output: {details['output_file']}")
        if 'file_size' in details:
            print(f"   Size: {details['file_size']}")
        if 'drive_status' in details:
            print(f"   Drive: {details['drive_status']}")
    
    if 'summary' in result:
        summary = result['summary']
        print(f"\n📊 Operation Summary:")
        if 'total_processed' in summary:
            print(f"   Files Processed: {summary['total_processed']}")
        if 'successful' in summary:
            print(f"   Successfully Converted: {summary['successful']}")
        if 'failed' in summary:
            print(f"   Failed: {summary['failed']}")
    
    if 'files' in result and len(result['files']) > 0:
        file_count = len(result['files'])
        print(f"\n📄 Files Found: {file_count}")
        if file_count <= 3:
            for file_info in result['files']:
                if isinstance(file_info, dict):
                    print(f"   • {file_info.get('name', 'Unknown')}")
                else:
                    print(f"   • {file_info}")
        else:
            print(f"   (showing first 3 of {file_count})")
            for file_info in result['files'][:3]:
                if isinstance(file_info, dict):
                    print(f"   • {file_info.get('name', 'Unknown')}")
                else:
                    print(f"   • {file_info}")
    
    if 'suggestions' in result:
        print(f"\n💡 System Suggestions:")
        for suggestion in result['suggestions'][:3]:  # Show max 3
            print(f"   • {suggestion}")
    
    if 'next_actions' in result:
        print(f"\n🎯 Next Actions:")
        for action in result['next_actions'][:3]:  # Show max 3
            print(f"   → {action}")
    
    if 'examples' in result:
        print(f"\n📝 Usage Examples:")
        for example in result['examples'][:2]:  # Show max 2
            print(f"   • {example}")

def quick_demo():
    """Quick demonstration of key features"""
    
    print("QUICK DEMO: Natural Language Document Converter")
    print("=" * 50)
    
    converter = NaturalLanguageConverter()
    
    # Test key features
    test_requests = [
        "Convert my SEO report to Word",
        "Turn all SOPs into docx files", 
        "Find the orchestrator checklist and export it as Word"
    ]
    
    for i, request in enumerate(test_requests, 1):
        print(f"\n{i}. User: \"{request}\"")
        result = converter.process_natural_request(request)
        print(f"   System: {result['message'][:100]}...")
        if result['status'] in ['success', 'batch_success']:
            print(f"   [OK] Would convert files successfully")
        elif result['status'] in ['file_not_found', 'search_no_results']:
            print(f"   [SEARCH] Would help user find the right files")
        else:
            print(f"   [GUIDE] Would provide helpful guidance")
    
    summary = converter.get_conversation_summary()
    print(f"\nDemo Complete - {summary['total_requests']} requests processed")

def check_system_readiness():
    """Check if the system components are ready"""
    
    print("[SYSTEM READINESS CHECK]")
    print("=" * 25)
    
    checks = []
    
    # Check DocumentConverter
    try:
        from document_conversion_system import DocumentConverter
        converter = DocumentConverter()
        checks.append(("Document Converter", "[OK] Ready"))
    except Exception as e:
        checks.append(("Document Converter", f"[ERROR] {e}"))
    
    # Check GoogleDriveAutomation
    try:
        from google_drive_automation import GoogleDriveAutomation
        drive_auto = GoogleDriveAutomation()
        checks.append(("Google Drive Automation", "[OK] Ready"))
    except Exception as e:
        checks.append(("Google Drive Automation", f"[ERROR] {e}"))
    
    # Check NaturalLanguageConverter
    try:
        converter = NaturalLanguageConverter()
        checks.append(("Natural Language Interface", "[OK] Ready"))
    except Exception as e:
        checks.append(("Natural Language Interface", f"[ERROR] {e}"))
    
    # Check directories
    directories = [
        "system/sops",
        "system/orchestration", 
        "system/reports",
        "system/reports/docx_exports"
    ]
    
    for directory in directories:
        if os.path.exists(directory):
            md_count = len(list(Path(directory).glob("*.md")))
            checks.append((f"Directory: {directory}", f"[OK] Exists ({md_count} .md files)"))
        else:
            checks.append((f"Directory: {directory}", "[WARN] Not found"))
    
    # Display results
    for component, status in checks:
        print(f"{component:.<40} {status}")
    
    # Overall status
    all_ready = all("[OK]" in check[1] for check in checks[:3])  # Core components only
    print(f"\nSystem Status: {'[OK] READY' if all_ready else '[WARN] NEEDS ATTENTION'}")
    
    return all_ready

def main():
    """Main demo entry point"""
    
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        
        if mode in ['check', 'status']:
            check_system_readiness()
        elif mode in ['quick', 'fast']:
            quick_demo()
        elif mode in ['full', 'complete']:
            if check_system_readiness():
                print("\n" + "="*60)
                demonstrate_converter()
            else:
                print("\n❌ System not ready. Please address the issues above.")
        else:
            print("Usage: python demo_converter.py [check|quick|full]")
    else:
        # Default to system check then quick demo
        print("NATURAL LANGUAGE CONVERTER DEMO")
        print("=" * 35)
        
        if check_system_readiness():
            print("\n" + "="*35)
            quick_demo()
            
            print(f"\nFor full demonstration: python demo_converter.py full")
            print(f"For system check only: python demo_converter.py check")
        else:
            print("\nPlease resolve system issues before running demo.")

if __name__ == "__main__":
    main()