#!/usr/bin/env python3
"""
Document Conversion - Natural Language Interface
Simple script to convert documents using conversational commands
"""

import sys
import os
from pathlib import Path

# Add system tools to path
sys.path.append(str(Path(__file__).parent / "system" / "core_tools"))

def main():
    """Main entry point for document conversion"""
    
    try:
        from natural_language_converter import NaturalLanguageConverter
        
        print("Natural Language Document Converter")
        print("===================================")
        
        if len(sys.argv) < 2:
            print("Usage Examples:")
            print("  python convert_my_docs.py \"Convert my SEO report to Word format\"")
            print("  python convert_my_docs.py \"Turn all SOPs into docx files\"")
            print("  python convert_my_docs.py \"Find the orchestrator checklist and convert it\"")
            print()
            print("Or run interactively:")
            print("  python system/core_tools/convert_cli.py")
            return
        
        # Get user request
        user_request = ' '.join(sys.argv[1:])
        
        print(f"Request: \"{user_request}\"")
        print("Processing...\n")
        
        # Initialize converter
        converter = NaturalLanguageConverter()
        
        # Process request
        result = converter.process_natural_request(user_request)
        
        # Display result
        status_icons = {
            'success': '[SUCCESS]',
            'batch_success': '[BATCH SUCCESS]',
            'batch_partial': '[PARTIAL SUCCESS]', 
            'needs_clarification': '[CLARIFICATION NEEDED]',
            'file_not_found': '[FILE NOT FOUND]',
            'multiple_matches': '[MULTIPLE FILES FOUND]'
        }
        
        icon = status_icons.get(result.get('status'), '[RESPONSE]')
        print(f"{icon} {result.get('message', 'No response')}")
        
        # Show details
        if 'details' in result:
            print(f"\nDetails:")
            for key, value in result['details'].items():
                print(f"  * {key.replace('_', ' ').title()}: {value}")
        
        # Show summary for batch operations
        if 'summary' in result:
            summary = result['summary']
            print(f"\nSummary:")
            if 'successful' in summary:
                print(f"  * Successfully converted: {summary['successful']} files")
            if 'failed' in summary:
                print(f"  * Failed: {summary['failed']} files")
            if 'output_location' in summary:
                print(f"  * Output location: {summary['output_location']}")
        
        # Show next actions
        if 'next_actions' in result:
            print(f"\nNext Actions:")
            for action in result['next_actions'][:3]:
                print(f"  -> {action}")
        
        # Show suggestions if needed
        if 'suggestions' in result:
            print(f"\nSuggestions:")
            for suggestion in result['suggestions'][:3]:
                print(f"  * {suggestion}")
        
        print(f"\nConversion complete!")
        
    except ImportError as e:
        print(f"[ERROR] System Error: {e}")
        print("Please ensure all required modules are installed:")
        print("  pip install python-docx markdown")
        
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        print("Please try again or check the file paths.")

if __name__ == "__main__":
    main()