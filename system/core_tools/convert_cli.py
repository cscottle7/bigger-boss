#!/usr/bin/env python3
"""
Conversational Document Converter CLI
Simple command-line interface for natural language document conversion
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

from natural_language_converter import NaturalLanguageConverter

def print_banner():
    """Print CLI banner"""
    print("🔄 Conversational Document Converter")
    print("====================================")
    print("Transform your documents with natural language!")
    print("Just tell me what you'd like to convert and I'll handle the rest.\n")

def print_help():
    """Print help information"""
    print("💡 How to use:")
    print("─────────────")
    print("• \"Convert my SEO report to Word format\"")
    print("• \"Turn the Universal Orchestrator Checklist into a .docx document\"")
    print("• \"Export all my SOPs as Word documents\"")
    print("• \"Find and convert the token optimisation guide\"")
    print("• \"Turn all files in the reports folder into Word docs\"")
    print()
    print("🎯 What I can do:")
    print("─────────────────")
    print("• Convert Markdown (.md) files to Word (.docx) format")
    print("• Search for files by name or keywords")
    print("• Batch convert multiple files")
    print("• Upload converted documents to Google Drive")
    print("• Maintain rich formatting (tables, headers, lists)")
    print()

def format_response(result):
    """Format and display response"""
    status = result.get('status', 'unknown')
    message = result.get('message', 'No message provided')
    
    # Status indicators
    status_icons = {
        'success': '✅',
        'batch_success': '🎉', 
        'batch_partial': '⚠️',
        'needs_clarification': '❓',
        'file_not_found': '🔍',
        'multiple_matches': '📁',
        'conversion_error': '❌',
        'system_error': '⚠️'
    }
    
    icon = status_icons.get(status, '💬')
    print(f"\n{icon} {message}")
    
    # Show details if available
    if 'details' in result:
        print("\n📋 Details:")
        for key, value in result['details'].items():
            print(f"   • {key.replace('_', ' ').title()}: {value}")
    
    # Show file lists
    if 'files' in result and isinstance(result['files'], list):
        if len(result['files']) <= 5:
            print(f"\n📄 Files ({len(result['files'])}):")
            for file_info in result['files']:
                if isinstance(file_info, dict):
                    print(f"   • {file_info.get('name', 'Unknown')}")
                else:
                    print(f"   • {file_info}")
        else:
            print(f"\n📄 Found {len(result['files'])} files (showing first 5):")
            for file_info in result['files'][:5]:
                if isinstance(file_info, dict):
                    print(f"   • {file_info.get('name', 'Unknown')}")
                else:
                    print(f"   • {file_info}")
    
    # Show successful files
    if 'successful_files' in result:
        print(f"\n✅ Successfully Converted ({len(result['successful_files'])}):")
        for filename in result['successful_files']:
            print(f"   • {filename}")
    
    # Show failed files
    if 'failed_files' in result:
        print(f"\n❌ Failed Conversions ({len(result['failed_files'])}):")
        for failed_file in result['failed_files']:
            if isinstance(failed_file, dict):
                print(f"   • {failed_file.get('name', 'Unknown')}: {failed_file.get('error', 'Unknown error')}")
            else:
                print(f"   • {failed_file}")
    
    # Show summary
    if 'summary' in result:
        summary = result['summary']
        print(f"\n📊 Summary:")
        if 'total_processed' in summary:
            print(f"   • Total Processed: {summary['total_processed']}")
        if 'successful' in summary:
            print(f"   • Successful: {summary['successful']}")
        if 'failed' in summary:
            print(f"   • Failed: {summary['failed']}")
        if 'success_rate' in summary:
            print(f"   • Success Rate: {summary['success_rate']}%")
    
    # Show suggestions
    if 'suggestions' in result:
        print(f"\n💡 Suggestions:")
        for suggestion in result['suggestions']:
            print(f"   • {suggestion}")
    
    # Show examples
    if 'examples' in result:
        print(f"\n📝 Examples:")
        for example in result['examples']:
            print(f"   • {example}")
    
    # Show next actions
    if 'next_actions' in result:
        print(f"\n🎯 Next Actions:")
        for action in result['next_actions']:
            print(f"   → {action}")
    
    # Show options for multiple matches
    if 'options' in result:
        print(f"\n⚙️ Options:")
        for i, option in enumerate(result['options'], 1):
            print(f"   {i}. {option}")

def interactive_mode():
    """Run interactive CLI mode"""
    print_banner()
    print_help()
    
    converter = NaturalLanguageConverter()
    
    print("🚀 Ready! Type your conversion request or 'help' for examples.")
    print("Type 'quit' or 'exit' to finish.\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['quit', 'exit', 'q']:
                # Show session summary
                summary = converter.get_conversation_summary()
                print(f"\n📊 Session Summary:")
                print(f"   • Requests: {summary['total_requests']}")
                print(f"   • Successful Operations: {summary['successful_operations']}")
                print(f"   • Files Converted: {summary['total_files_converted']}")
                print(f"   • Session Duration: {summary['session_duration_minutes']:.1f} minutes")
                print("\n👋 Goodbye! Thanks for using the Conversational Document Converter.")
                break
                
            if user_input.lower() in ['help', 'h', '?']:
                print_help()
                continue
            
            if user_input.lower() in ['status', 'summary']:
                summary = converter.get_conversation_summary()
                print(f"\n📊 Current Session:")
                print(f"   • Requests Made: {summary['total_requests']}")
                print(f"   • Operations Completed: {summary['successful_operations']}")
                print(f"   • Files Converted: {summary['total_files_converted']}")
                if summary['last_operation_files']:
                    print(f"   • Last Converted: {len(summary['last_operation_files'])} files")
                continue
            
            # Process the request
            print("\n🤔 Processing your request...")
            result = converter.process_natural_request(user_input)
            format_response(result)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ System error: {e}")
            print("Please try again or type 'help' for assistance.")

def single_command_mode(command):
    """Process single command and exit"""
    converter = NaturalLanguageConverter()
    
    print("🔄 Conversational Document Converter")
    print("====================================")
    print(f"Processing: \"{command}\"")
    
    result = converter.process_natural_request(command)
    format_response(result)
    
    # Show summary
    summary = converter.get_conversation_summary()
    if summary['total_files_converted'] > 0:
        print(f"\n📊 Operation Complete: {summary['total_files_converted']} files converted")

def main():
    """Main CLI entry point"""
    if len(sys.argv) > 1:
        # Single command mode
        command = ' '.join(sys.argv[1:])
        single_command_mode(command)
    else:
        # Interactive mode
        interactive_mode()

if __name__ == "__main__":
    main()