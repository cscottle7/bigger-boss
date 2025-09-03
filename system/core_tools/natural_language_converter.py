#!/usr/bin/env python3
"""
Natural Language Document Conversion Interface
Provides conversational interface for document conversion and Google Drive integration
Processes plain English requests for file conversion operations
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Union

# Import existing systems
from document_conversion_system import DocumentConverter, GoogleDriveIntegration
from google_drive_automation import GoogleDriveAutomation

class NaturalLanguageConverter:
    """Natural language interface for document conversion operations"""
    
    def __init__(self):
        self.converter = DocumentConverter()
        self.drive_automation = GoogleDriveAutomation()
        self.drive_integration = GoogleDriveIntegration(self.converter)
        
        # Conversation context
        self.conversation_history = []
        self.last_operation_files = []
        self.user_preferences = {}
        
        # Intent patterns for British English - batch patterns first to prioritise them
        self.intent_patterns = {
            'convert_batch': [
                r'convert all (?:my |the )?(.+?) (?:to|into) (?:word|docx)',
                r'turn all (?:my |the )?(.+?) into (?:word|docx)',
                r'batch convert (?:my |the )?(.+?)',
                r'convert (?:all|every) (?:.+?) in (?:the )?(.+?) (?:folder|directory)'
            ],
            'convert_single': [
                r'convert (?:my |the |this )?(.+?) (?:to|into) (?:word|docx|\.docx)(?: format)?',
                r'turn (?:my |the |this )?(.+?) into (?:a |an )?(?:word|docx|\.docx)(?: document)?',
                r'export (?:my |the |this )?(.+?) as (?:a |an )?(?:word|docx|\.docx)(?: document)?',
                r'make (?:my |the |this )?(.+?) (?:into )?(?:a |an )?(?:word|docx|\.docx)(?: file)?'
            ],
            'find_and_convert': [
                r'find (?:and convert )?(.+?) (?:and )?(?:convert (?:it |them )?(?:to|into) (?:word|docx))?',
                r'locate (?:and convert )?(.+?) (?:to|into) (?:word|docx)',
                r'search for (.+?) (?:and )?(?:convert (?:to|into) (?:word|docx))?'
            ]
        }
        
        # File detection patterns
        self.file_patterns = {
            'sop': [r'sop[s]?', r'standard operating procedure', r'procedure', r'protocol'],
            'report': [r'report[s]?', r'analysis', r'audit', r'assessment', r'review'],
            'checklist': [r'checklist[s]?', r'check.?list', r'list'],
            'guide': [r'guide[s]?', r'manual', r'handbook', r'instruction'],
            'strategy': [r'strateg[y|ies]', r'plan[s]?', r'framework'],
            'template': [r'template[s]?', r'format', r'structure']
        }
        
        # Common file references
        self.file_references = {
            'universal orchestrator': 'UNIVERSAL_ORCHESTRATOR_CHECKLIST.md',
            'orchestrator checklist': 'UNIVERSAL_ORCHESTRATOR_CHECKLIST.md',
            'token optimization': 'SOP_Token_Optimization_2025.md',
            'token optimization 2025': 'SOP_Token_Optimization_2025.md',
            'content refinement': 'SOP_Automated_Content_Refinement_2025.md',
            'automated content refinement': 'SOP_Automated_Content_Refinement_2025.md',
            'seo extraction': 'enhanced_seo_extraction_report.md'
        }
    
    def process_natural_request(self, user_input: str) -> Dict:
        """Process natural language request and execute conversion operations"""
        
        # Record conversation
        self.conversation_history.append({
            'timestamp': datetime.now(),
            'user_input': user_input,
            'type': 'request'
        })
        
        try:
            # Parse intent and extract entities
            intent_result = self.parse_intent(user_input)
            
            if not intent_result['intent']:
                return self.handle_clarification_needed(user_input)
            
            # Execute based on intent
            if intent_result['intent'] == 'convert_single':
                return self.handle_single_conversion(intent_result)
            elif intent_result['intent'] == 'convert_batch':
                return self.handle_batch_conversion(intent_result)
            elif intent_result['intent'] == 'find_and_convert':
                return self.handle_find_and_convert(intent_result)
            else:
                return self.handle_unknown_intent(user_input)
                
        except Exception as e:
            return self.handle_error(str(e), user_input)
    
    def parse_intent(self, user_input: str) -> Dict:
        """Parse user intent and extract relevant entities"""
        
        user_input_lower = user_input.lower()
        
        # Try to match intent patterns
        for intent_type, patterns in self.intent_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, user_input_lower)
                if match:
                    return {
                        'intent': intent_type,
                        'file_reference': match.group(1) if match.groups() else None,
                        'raw_input': user_input,
                        'confidence': 0.9
                    }
        
        # Check for keywords that suggest conversion
        conversion_keywords = ['convert', 'turn', 'export', 'make', 'change']
        format_keywords = ['word', 'docx', '.docx', 'document']
        
        has_conversion = any(keyword in user_input_lower for keyword in conversion_keywords)
        has_format = any(keyword in user_input_lower for keyword in format_keywords)
        
        if has_conversion and has_format:
            return {
                'intent': 'convert_single',
                'file_reference': self.extract_file_reference(user_input),
                'raw_input': user_input,
                'confidence': 0.7
            }
        
        return {'intent': None, 'file_reference': None, 'raw_input': user_input, 'confidence': 0.0}
    
    def extract_file_reference(self, user_input: str) -> Optional[str]:
        """Extract file reference from user input"""
        
        user_input_lower = user_input.lower()
        
        # Check direct file references first (more specific)
        for reference, filename in self.file_references.items():
            if reference in user_input_lower:
                return reference  # Return the search term, not filename
        
        # Extract quoted references
        quoted_match = re.search(r'["\']([^"\']+)["\']', user_input)
        if quoted_match:
            return quoted_match.group(1)
        
        # Try to extract the main subject from conversion patterns
        conversion_patterns = [
            r'convert (?:my |the |this )?(.+?) (?:to|into) (?:word|docx|\.docx)(?: format)?',
            r'turn (?:my |the |this )?(.+?) into (?:word|docx|\.docx)',
            r'export (?:my |the |this )?(.+?) as (?:word|docx|\.docx)',
            r'make (?:my |the |this )?(.+?) (?:into )?(?:word|docx|\.docx)'
        ]
        
        for pattern in conversion_patterns:
            match = re.search(pattern, user_input_lower)
            if match:
                extracted = match.group(1).strip()
                # Clean up common words
                extracted = re.sub(r'\b(the|a|an|my)\b', '', extracted).strip()
                if extracted:
                    return extracted
        
        # Fall back to file type references
        for file_type, patterns in self.file_patterns.items():
            for pattern in patterns:
                if re.search(pattern, user_input_lower):
                    return file_type
        
        return None
    
    def find_matching_files(self, search_term: str) -> List[str]:
        """Find files that match the search term"""
        
        if not search_term:
            return []
        
        # Direct filename match from references
        direct_match = self.file_references.get(search_term.lower())
        if direct_match:
            # Check in common directories for the file
            search_directories = [
                'system/sops',
                'system/orchestration', 
                'system/core_tools',
                'system/reports',
                'clients',
                '.'
            ]
            
            for directory in search_directories:
                if os.path.exists(directory):
                    full_path = os.path.join(directory, direct_match)
                    if os.path.exists(full_path):
                        return [full_path]
        
        # Search in common directories
        search_directories = [
            'system/sops',
            'system/orchestration', 
            'system/core_tools',
            'system/reports',
            'clients',
            '.'
        ]
        
        matching_files = []
        search_patterns = [
            f"*{search_term}*",
            f"*{search_term.replace(' ', '_')}*",
            f"*{search_term.replace(' ', '')}*"
        ]
        
        for directory in search_directories:
            if not os.path.exists(directory):
                continue
                
            for pattern in search_patterns:
                for file_path in Path(directory).rglob(f"{pattern}.md"):
                    if file_path.is_file():
                        matching_files.append(str(file_path))
        
        # Remove duplicates and sort by relevance
        matching_files = list(set(matching_files))
        
        # Sort by relevance (exact matches first)
        def relevance_score(file_path):
            filename = Path(file_path).stem.lower()
            search_lower = search_term.lower()
            
            if search_lower in filename:
                return 100 - len(filename)  # Shorter is better for exact matches
            elif any(word in filename for word in search_lower.split()):
                return 50
            else:
                return 0
        
        matching_files.sort(key=relevance_score, reverse=True)
        return matching_files[:10]  # Limit to top 10 matches
    
    def handle_single_conversion(self, intent_result: Dict) -> Dict:
        """Handle single file conversion request"""
        
        file_reference = intent_result.get('file_reference')
        if not file_reference:
            return {
                'status': 'needs_clarification',
                'message': "I'd be happy to help convert a document to Word format! Could you tell me which specific file you'd like me to convert?",
                'suggestions': self.get_recent_file_suggestions()
            }
        
        # Re-extract file reference to ensure consistency
        extracted_ref = self.extract_file_reference(intent_result.get('raw_input', ''))
        search_term = extracted_ref if extracted_ref else file_reference
        
        # Find matching files
        matching_files = self.find_matching_files(search_term)
        
        if not matching_files:
            return {
                'status': 'file_not_found',
                'message': f"I couldn't find any files matching '{file_reference}'. Could you check the filename or try a different search term?",
                'suggestions': [
                    "Try using part of the filename",
                    "Check if the file exists in the current directory",
                    "Use keywords like 'SOP', 'report', or 'checklist'"
                ]
            }
        
        if len(matching_files) > 1:
            return {
                'status': 'multiple_matches',
                'message': f"I found {len(matching_files)} files that might match. Which one would you like me to convert?",
                'files': [{'path': f, 'name': Path(f).stem} for f in matching_files[:5]],
                'suggestion': f"The most likely match is: {Path(matching_files[0]).stem}"
            }
        
        # Convert the file
        return self.execute_single_conversion(matching_files[0])
    
    def handle_batch_conversion(self, intent_result: Dict) -> Dict:
        """Handle batch conversion request"""
        
        file_reference = intent_result.get('file_reference')
        
        # Determine source directory
        if file_reference:
            if 'sop' in file_reference.lower():
                source_dir = 'system/sops'
                file_type = 'SOPs'
            elif 'report' in file_reference.lower():
                source_dir = 'system/reports'
                file_type = 'reports'
            else:
                source_dir = '.'
                file_type = 'files'
        else:
            source_dir = '.'
            file_type = 'files'
        
        if not os.path.exists(source_dir):
            return {
                'status': 'directory_not_found',
                'message': f"I couldn't find the '{source_dir}' directory. Could you specify which folder contains the files you'd like to convert?",
                'suggestions': ['system/sops', 'system/reports', 'clients']
            }
        
        # Find markdown files in directory
        md_files = list(Path(source_dir).rglob('*.md'))
        
        if not md_files:
            return {
                'status': 'no_files_found',
                'message': f"I couldn't find any Markdown files in '{source_dir}' to convert.",
                'suggestion': "Try specifying a different directory or check that .md files exist"
            }
        
        return self.execute_batch_conversion(md_files, file_type)
    
    def handle_find_and_convert(self, intent_result: Dict) -> Dict:
        """Handle find and convert request"""
        
        search_term = intent_result.get('file_reference', '')
        
        # Broader search across all directories
        matching_files = self.find_matching_files(search_term)
        
        if not matching_files:
            return {
                'status': 'search_no_results', 
                'message': f"I searched for files matching '{search_term}' but couldn't find any. Could you try a different search term?",
                'suggestions': [
                    "Try using keywords from the filename",
                    "Check spelling and try partial matches",
                    "Use terms like 'SOP', 'report', 'analysis'"
                ]
            }
        
        if len(matching_files) == 1:
            return self.execute_single_conversion(matching_files[0])
        
        # Multiple files found - offer batch conversion
        return {
            'status': 'multiple_found_batch_option',
            'message': f"I found {len(matching_files)} files matching '{search_term}'. Would you like me to convert all of them or just specific ones?",
            'files': [{'path': f, 'name': Path(f).stem} for f in matching_files],
            'options': [
                "Convert all files",
                "Select specific files",
                "Convert the most relevant file only"
            ]
        }
    
    def execute_single_conversion(self, file_path: str) -> Dict:
        """Execute single file conversion with Drive upload"""
        
        try:
            # Convert to .docx
            docx_path = self.converter.convert_markdown_to_docx(
                file_path, 
                output_dir="system/reports/docx_exports"
            )
            
            # Add to Google Drive queue
            self.drive_automation.add_to_upload_queue(docx_path)
            
            # Process upload (simulated for now)
            upload_results = self.drive_automation.process_upload_queue(dry_run=False)
            
            # Record successful operation
            self.last_operation_files = [docx_path]
            
            filename = Path(file_path).stem
            docx_filename = Path(docx_path).name
            file_size = round(os.path.getsize(docx_path) / 1024, 1)  # KB
            
            self.conversation_history.append({
                'timestamp': datetime.now(),
                'type': 'success',
                'operation': 'single_conversion',
                'files': [docx_path]
            })
            
            return {
                'status': 'success',
                'message': f"[SUCCESS] Brilliant! I've converted '{filename}' to Word format and uploaded it to Google Drive.",
                'details': {
                    'source_file': filename,
                    'output_file': docx_filename,
                    'file_size': f"{file_size} KB",
                    'location': "system/reports/docx_exports/",
                    'drive_status': "Uploaded to Analysis Reports folder"
                },
                'next_actions': [
                    "The document is ready for team collaboration",
                    "You can access it in Google Drive under 'Analysis Reports'",
                    "Would you like me to convert any other files?"
                ]
            }
            
        except Exception as e:
            return {
                'status': 'conversion_error',
                'message': f"I encountered an issue converting the file: {str(e)}",
                'suggestion': "Let me check the file format and try a different approach",
                'troubleshooting': [
                    "Ensure the file is a valid Markdown document",
                    "Check that you have write permissions to the output directory",
                    "Verify the file isn't currently open in another application"
                ]
            }
    
    def execute_batch_conversion(self, file_paths: List[str], file_type: str) -> Dict:
        """Execute batch conversion with Drive upload"""
        
        try:
            conversion_results = []
            successful_conversions = []
            failed_conversions = []
            
            for file_path in file_paths:
                try:
                    docx_path = self.converter.convert_markdown_to_docx(
                        str(file_path),
                        output_dir="system/reports/docx_exports"
                    )
                    
                    # Add to Drive queue
                    self.drive_automation.add_to_upload_queue(docx_path)
                    successful_conversions.append({
                        'source': str(file_path),
                        'output': docx_path,
                        'name': Path(file_path).stem
                    })
                    
                except Exception as e:
                    failed_conversions.append({
                        'source': str(file_path),
                        'error': str(e),
                        'name': Path(file_path).stem
                    })
            
            # Process Drive uploads
            if successful_conversions:
                upload_results = self.drive_automation.process_upload_queue(dry_run=False)
            
            # Record operation
            self.last_operation_files = [item['output'] for item in successful_conversions]
            
            total_files = len(file_paths)
            successful_count = len(successful_conversions)
            failed_count = len(failed_conversions)
            
            self.conversation_history.append({
                'timestamp': datetime.now(),
                'type': 'batch_success' if failed_count == 0 else 'batch_partial',
                'operation': 'batch_conversion',
                'files': self.last_operation_files
            })
            
            if failed_count == 0:
                return {
                    'status': 'batch_success',
                    'message': f"[BATCH SUCCESS] Excellent! I've successfully converted all {successful_count} {file_type} to Word format and uploaded them to Google Drive.",
                    'summary': {
                        'total_processed': total_files,
                        'successful': successful_count,
                        'failed': failed_count,
                        'output_location': "system/reports/docx_exports/"
                    },
                    'files': [item['name'] for item in successful_conversions],
                    'next_actions': [
                        f"All {file_type} are now available for team collaboration",
                        "Documents are organised in the Google Drive Analysis Reports folder",
                        "Team members can access and edit the Word documents directly"
                    ]
                }
            else:
                return {
                    'status': 'batch_partial',
                    'message': f"I've converted {successful_count} out of {total_files} {file_type}. There were some issues with {failed_count} files.",
                    'summary': {
                        'total_processed': total_files,
                        'successful': successful_count,
                        'failed': failed_count,
                        'success_rate': round((successful_count / total_files) * 100, 1)
                    },
                    'successful_files': [item['name'] for item in successful_conversions],
                    'failed_files': [{'name': item['name'], 'error': item['error']} for item in failed_conversions],
                    'next_actions': [
                        f"Successfully converted files are in Google Drive",
                        f"Would you like me to retry the {failed_count} failed conversions?",
                        "I can help troubleshoot the conversion issues"
                    ]
                }
        
        except Exception as e:
            return {
                'status': 'batch_error',
                'message': f"I encountered an issue during batch conversion: {str(e)}",
                'suggestion': "Let me try converting the files one by one to identify the problem"
            }
    
    def handle_clarification_needed(self, user_input: str) -> Dict:
        """Handle cases where clarification is needed"""
        
        return {
            'status': 'needs_clarification',
            'message': "I'd be happy to help with document conversion! I can convert Markdown files to Word format and upload them to Google Drive.",
            'examples': [
                "\"Convert my SEO report to Word format\"",
                "\"Turn the Universal Orchestrator Checklist into a .docx document\"", 
                "\"Export all my SOPs as Word documents\"",
                "\"Find and convert the token optimisation guide\""
            ],
            'capabilities': [
                "Convert single files from Markdown to Word (.docx) format",
                "Batch convert multiple files at once",
                "Search for files by name or keywords",
                "Automatically upload converted documents to Google Drive",
                "Maintain rich formatting including tables, headers, and lists"
            ]
        }
    
    def handle_unknown_intent(self, user_input: str) -> Dict:
        """Handle unknown or unclear requests"""
        
        return {
            'status': 'unknown_intent',
            'message': f"I'm not quite sure what you'd like me to do with '{user_input}'. Could you rephrase your request?",
            'suggestions': [
                "Try using words like 'convert', 'turn into', or 'export'",
                "Specify the file you want to convert",
                "Mention 'Word' or 'docx' as the target format"
            ],
            'help_examples': [
                "Convert [filename] to Word",
                "Turn [filename] into docx", 
                "Export [filename] as Word document"
            ]
        }
    
    def handle_error(self, error_message: str, user_input: str) -> Dict:
        """Handle system errors gracefully"""
        
        return {
            'status': 'system_error',
            'message': f"I encountered an issue processing your request: {error_message}",
            'user_input': user_input,
            'troubleshooting': [
                "Please try your request again",
                "Check that the file exists and is accessible", 
                "Ensure you have proper permissions for file operations"
            ],
            'support': "If the issue persists, please check the system logs for more details"
        }
    
    def get_recent_file_suggestions(self) -> List[str]:
        """Get suggestions for recently worked with files"""
        
        suggestions = []
        
        # Check common directories for recent .md files
        common_dirs = ['system/sops', 'system/orchestration', 'system/reports']
        
        for directory in common_dirs:
            if os.path.exists(directory):
                md_files = list(Path(directory).glob('*.md'))
                # Sort by modification time, get most recent
                if md_files:
                    recent_files = sorted(md_files, key=lambda f: f.stat().st_mtime, reverse=True)
                    suggestions.extend([f.stem for f in recent_files[:2]])
        
        return suggestions[:5]  # Limit to 5 suggestions
    
    def get_conversation_summary(self) -> Dict:
        """Get summary of current conversation session"""
        
        operations = [entry for entry in self.conversation_history if entry['type'] in ['success', 'batch_success', 'batch_partial']]
        
        total_files_converted = sum(len(op.get('files', [])) for op in operations)
        
        return {
            'session_start': self.conversation_history[0]['timestamp'] if self.conversation_history else datetime.now(),
            'total_requests': len([entry for entry in self.conversation_history if entry['type'] == 'request']),
            'successful_operations': len(operations),
            'total_files_converted': total_files_converted,
            'last_operation_files': self.last_operation_files,
            'session_duration_minutes': ((datetime.now() - self.conversation_history[0]['timestamp']).total_seconds() / 60) if self.conversation_history else 0
        }

def main():
    """Interactive demonstration of natural language converter"""
    print("[NATURAL LANGUAGE CONVERTER] System Starting...")
    print("=====================================")
    
    converter = NaturalLanguageConverter()
    
    # Sample interactions
    sample_requests = [
        "Convert the Universal Orchestrator Checklist to Word format",
        "Turn all my SOPs into Word documents",
        "Find and convert the token optimisation report",
        "Export the content refinement guide as a .docx document",
        "Convert my analysis reports to Word"
    ]
    
    print("\n🗣️ SAMPLE INTERACTIONS:")
    print("======================")
    
    for i, request in enumerate(sample_requests, 1):
        print(f"\n📝 Sample Request {i}: \"{request}\"")
        print("─" * 50)
        
        result = converter.process_natural_request(request)
        
        print(f"Status: {result['status']}")
        print(f"Response: {result['message']}")
        
        if 'details' in result:
            print("Details:")
            for key, value in result['details'].items():
                print(f"  • {key}: {value}")
        
        if 'files' in result:
            print(f"Files involved: {len(result['files'])}")
        
        if 'next_actions' in result:
            print("Next Actions:")
            for action in result['next_actions']:
                print(f"  → {action}")
        
        print()
    
    # Show conversation summary
    summary = converter.get_conversation_summary()
    print("\n📊 SESSION SUMMARY:")
    print("==================")
    print(f"Total Requests: {summary['total_requests']}")
    print(f"Successful Operations: {summary['successful_operations']}")
    print(f"Files Converted: {summary['total_files_converted']}")
    
    print("\n✅ Natural Language Converter Ready!")
    print("Usage: converter.process_natural_request('Convert my report to Word')")

if __name__ == "__main__":
    main()