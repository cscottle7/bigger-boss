#!/usr/bin/env python3
"""
Bigger Boss Agent System - British English Validator
Validates and corrects British English spelling and terminology compliance.
"""

import argparse
import json
import logging
import re
import sys
from datetime import datetime
from typing import Dict, List, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BritishEnglishValidator:
    """Validator for British English spelling and terminology compliance."""

    def __init__(self):
        # American to British spelling corrections
        self.spelling_corrections = {
            # -ize/-ise endings
            r'\borganization\b': 'organisation',
            r'\borganizations\b': 'organisations',
            r'\borganizational\b': 'organisational',
            r'\borganize\b': 'organise',
            r'\borganizes\b': 'organises',
            r'\borganized\b': 'organised',
            r'\borganizing\b': 'organising',
            r'\borganizer\b': 'organiser',
            r'\borganizers\b': 'organisers',

            r'\brealize\b': 'realise',
            r'\brealizes\b': 'realises',
            r'\brealized\b': 'realised',
            r'\brealizing\b': 'realising',
            r'\brealization\b': 'realisation',

            r'\boptimize\b': 'optimise',
            r'\boptimizes\b': 'optimises',
            r'\boptimized\b': 'optimised',
            r'\boptimizing\b': 'optimising',
            r'\boptimization\b': 'optimisation',

            r'\banalyze\b': 'analyse',
            r'\banalyzes\b': 'analyses',
            r'\banalyzed\b': 'analysed',
            r'\banalyzing\b': 'analysing',
            r'\banalysis\b': 'analysis',  # Same in both

            r'\brecognize\b': 'recognise',
            r'\brecognizes\b': 'recognises',
            r'\brecognized\b': 'recognised',
            r'\brecognizing\b': 'recognising',
            r'\brecognition\b': 'recognition',  # Same in both

            r'\bspecialize\b': 'specialise',
            r'\bspecializes\b': 'specialises',
            r'\bspecialized\b': 'specialised',
            r'\bspecializing\b': 'specialising',
            r'\bspecialization\b': 'specialisation',

            # -or/-our endings
            r'\bcolor\b': 'colour',
            r'\bcolors\b': 'colours',
            r'\bcolored\b': 'coloured',
            r'\bcoloring\b': 'colouring',

            r'\bhonor\b': 'honour',
            r'\bhonors\b': 'honours',
            r'\bhonored\b': 'honoured',
            r'\bhonoring\b': 'honouring',
            r'\bhonorable\b': 'honourable',

            r'\bfavor\b': 'favour',
            r'\bfavors\b': 'favours',
            r'\bfavored\b': 'favoured',
            r'\bfavoring\b': 'favouring',
            r'\bfavorite\b': 'favourite',
            r'\bfavorites\b': 'favourites',

            r'\bbehavior\b': 'behaviour',
            r'\bbehaviors\b': 'behaviours',
            r'\bbehavioral\b': 'behavioural',

            r'\blabor\b': 'labour',
            r'\blabors\b': 'labours',
            r'\blabored\b': 'laboured',
            r'\blaboring\b': 'labouring',

            r'\bneighbor\b': 'neighbour',
            r'\bneighbors\b': 'neighbours',
            r'\bneighborhood\b': 'neighbourhood',
            r'\bneighboring\b': 'neighbouring',

            # -er/-re endings
            r'\bcenter\b': 'centre',
            r'\bcenters\b': 'centres',
            r'\bcentered\b': 'centred',
            r'\bcentering\b': 'centring',

            r'\btheater\b': 'theatre',
            r'\btheaters\b': 'theatres',

            r'\bmeter\b': 'metre',
            r'\bmeters\b': 'metres',

            r'\bliter\b': 'litre',
            r'\bliters\b': 'litres',

            # -se/-ce endings
            r'\bdefense\b': 'defence',
            r'\bdefenses\b': 'defences',
            r'\bdefensive\b': 'defensive',  # Same in both

            r'\boffense\b': 'offence',
            r'\boffenses\b': 'offences',
            r'\boffensive\b': 'offensive',  # Same in both

            r'\blicense\b': 'licence',  # Noun form
            # Note: 'license' is correct as verb in British English

            r'\bpractice\b': 'practise',  # Verb form
            # Note: 'practice' is correct as noun in British English

            # Double consonants
            r'\btraveled\b': 'travelled',
            r'\btraveling\b': 'travelling',
            r'\btraveler\b': 'traveller',
            r'\btravelers\b': 'travellers',

            r'\bcanceled\b': 'cancelled',
            r'\bcanceling\b': 'cancelling',

            r'\bmodeled\b': 'modelled',
            r'\bmodeling\b': 'modelling',

            r'\blabeled\b': 'labelled',
            r'\blabeling\b': 'labelling',

            r'\bfueled\b': 'fuelled',
            r'\bfueling\b': 'fuelling',

            # Miscellaneous
            r'\bcheck\b(?=\s+(?:mark|box|list))': 'tick',  # Check mark -> Tick mark
            r'\bgray\b': 'grey',
            r'\bskeptical\b': 'sceptical',
            r'\bskepticism\b': 'scepticism',

            # Program vs Programme (context dependent)
            r'\bprogram\b(?=\s+(?:of|for|in))': 'programme',  # Programme for events
            # Note: 'program' is correct for computer programs
        }

        # American terminology to British terminology
        self.terminology_corrections = {
            # Technology and business terms
            r'\bcell\s+phone\b': 'mobile phone',
            r'\bcellphone\b': 'mobile',
            r'\bmobile\s+phone\b': 'mobile phone',  # Already correct

            r'\belevator\b': 'lift',
            r'\bapartment\b': 'flat',
            r'\bgas\s+station\b': 'petrol station',
            r'\btrash\b(?!\s+(?:talk|can))': 'rubbish',
            r'\bgarbage\b(?!\s+(?:collection|disposal))': 'rubbish',

            # Business and professional terms
            r'\bresume\b': 'CV',
            r'\bzip\s+code\b': 'postcode',
            r'\bmail\b(?=\s+(?:address|box))': 'post',
            r'\bmailbox\b': 'postbox',

            # Transportation
            r'\btruck\b(?!\s+(?:driver|stop))': 'lorry',
            r'\bfreeway\b': 'motorway',
            r'\bhighway\b': 'motorway',
            r'\bparking\s+lot\b': 'car park',

            # Time and scheduling
            r'\bvacation\b': 'holiday',
            r'\bfall\b(?=\s+(?:season|semester))': 'autumn',

            # Food and dining
            r'\bcookies\b(?!\s+(?:policy|consent))': 'biscuits',
            r'\bcandy\b': 'sweets',
            r'\bsoda\b': 'soft drink',

            # Retail and shopping
            r'\bstore\b(?=\s+(?:hours|location))': 'shop',
            r'\bmall\b': 'shopping centre',
            r'\bshopping\s+mall\b': 'shopping centre',

            # Education
            r'\bgrade\b(?=\s+(?:\d|school))': 'year',
            r'\bcollege\b(?!\s+(?:university|degree))': 'university',
        }

        # Context-aware corrections (more sophisticated)
        self.contextual_corrections = {
            # License/Licence - depends on noun vs verb usage
            r'\b(drivers?)\s+license\b': r'\1 licence',
            r'\b(business)\s+license\b': r'\1 licence',
            r'\bto\s+license\b': 'to license',  # Verb form is correct

            # Practice/Practise - depends on noun vs verb usage
            r'\b(medical|legal|dental)\s+practice\b': r'\1 practice',  # Noun
            r'\bto\s+practice\b': 'to practise',  # Verb
            r'\bpractice\s+(medicine|law)\b': 'practise \\1',  # Verb

            # Programme/Program - context dependent
            r'\b(television|TV|radio)\s+program\b': r'\1 programme',
            r'\b(training|education|development)\s+program\b': r'\1 programme',
            r'\b(computer|software)\s+program\b': r'\1 program',  # Correct as is
        }

        # Australian-specific terms and spellings
        self.australian_specific = {
            # Currency
            r'\$(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:USD|dollars?)': r'$\1 AUD',
            r'\bdollars?\b(?!\s+AUD)': 'dollars AUD',

            # Geographic terms
            r'\bstates?\b(?=\s+(?:and|&)\s+territories)': 'states',  # Already correct
            r'\bfederal\s+government\b': 'federal government',  # Already correct

            # Business terms
            r'\bcompany\s+registration\b': 'company registration',
            r'\bbusiness\s+license\b': 'business licence',
            r'\bGST\b': 'GST',  # Already correct - Goods and Services Tax
            r'\bABN\b': 'ABN',  # Already correct - Australian Business Number
            r'\bACN\b': 'ACN',  # Already correct - Australian Company Number
        }

        # Measurement conversions (informational only)
        self.measurement_patterns = {
            r'\bfeet\b': 'metres',
            r'\binches\b': 'centimetres',
            r'\bmiles\b': 'kilometres',
            r'\bfahrenheit\b': 'celsius',
            r'\bgallons\b': 'litres',
            r'\bpounds\b(?!\s+(?:sterling|GBP))': 'kilograms',
        }

    def validate_text(self, text: str, auto_correct: bool = False) -> Dict:
        """
        Validate text for British English compliance.

        Args:
            text: Text to validate
            auto_correct: Whether to return corrected text

        Returns:
            Validation result dictionary
        """
        issues = []
        corrections = {}
        corrected_text = text

        # Check spelling corrections
        spelling_issues, spelling_corrections, corrected_text = self._check_spelling(
            corrected_text, auto_correct
        )
        issues.extend(spelling_issues)
        corrections.update(spelling_corrections)

        # Check terminology corrections
        term_issues, term_corrections, corrected_text = self._check_terminology(
            corrected_text, auto_correct
        )
        issues.extend(term_issues)
        corrections.update(term_corrections)

        # Check contextual corrections
        context_issues, context_corrections, corrected_text = self._check_contextual(
            corrected_text, auto_correct
        )
        issues.extend(context_issues)
        corrections.update(context_corrections)

        # Check Australian-specific terms
        aus_issues, aus_corrections, corrected_text = self._check_australian_specific(
            corrected_text, auto_correct
        )
        issues.extend(aus_issues)
        corrections.update(aus_corrections)

        # Calculate compliance score
        total_words = len(text.split())
        total_issues = len(issues)
        compliance_score = max(0, 100 - (total_issues / max(total_words / 100, 1) * 5))

        return {
            'status': 'success',
            'compliant': len(issues) == 0,
            'compliance_score': round(compliance_score, 1),
            'total_issues': total_issues,
            'total_words': total_words,
            'issues': issues,
            'corrections': corrections,
            'corrected_text': corrected_text if auto_correct else None,
            'categories': {
                'spelling': len(spelling_issues),
                'terminology': len(term_issues),
                'contextual': len(context_issues),
                'australian_specific': len(aus_issues)
            },
            'validated_at': datetime.now().isoformat()
        }

    def _check_spelling(self, text: str, auto_correct: bool) -> Tuple[List, Dict, str]:
        """Check for American spelling issues."""
        issues = []
        corrections = {}
        corrected_text = text

        for american_pattern, british_spelling in self.spelling_corrections.items():
            matches = list(re.finditer(american_pattern, text, re.IGNORECASE))

            for match in matches:
                american_word = match.group()
                start_pos = match.start()
                end_pos = match.end()

                # Get context for the issue
                context_start = max(0, start_pos - 30)
                context_end = min(len(text), end_pos + 30)
                context = text[context_start:context_end].strip()

                # Preserve original case
                if american_word.isupper():
                    british_word = british_spelling.upper()
                elif american_word.istitle():
                    british_word = british_spelling.capitalize()
                else:
                    british_word = british_spelling

                issues.append({
                    'type': 'spelling',
                    'severity': 'medium',
                    'american_word': american_word,
                    'british_word': british_word,
                    'position': start_pos,
                    'context': context,
                    'rule': f'{american_pattern} -> {british_spelling}'
                })

                corrections[american_word] = british_word

                if auto_correct:
                    # Use word boundaries to avoid partial matches
                    corrected_text = re.sub(
                        american_pattern,
                        british_spelling,
                        corrected_text,
                        flags=re.IGNORECASE
                    )

        return issues, corrections, corrected_text

    def _check_terminology(self, text: str, auto_correct: bool) -> Tuple[List, Dict, str]:
        """Check for American terminology issues."""
        issues = []
        corrections = {}
        corrected_text = text

        for american_term, british_term in self.terminology_corrections.items():
            matches = list(re.finditer(american_term, text, re.IGNORECASE))

            for match in matches:
                american_phrase = match.group()
                start_pos = match.start()
                end_pos = match.end()

                # Get context
                context_start = max(0, start_pos - 30)
                context_end = min(len(text), end_pos + 30)
                context = text[context_start:context_end].strip()

                issues.append({
                    'type': 'terminology',
                    'severity': 'high',
                    'american_term': american_phrase,
                    'british_term': british_term,
                    'position': start_pos,
                    'context': context,
                    'rule': f'{american_term} -> {british_term}'
                })

                corrections[american_phrase] = british_term

                if auto_correct:
                    corrected_text = re.sub(
                        american_term,
                        british_term,
                        corrected_text,
                        flags=re.IGNORECASE
                    )

        return issues, corrections, corrected_text

    def _check_contextual(self, text: str, auto_correct: bool) -> Tuple[List, Dict, str]:
        """Check for contextual spelling issues."""
        issues = []
        corrections = {}
        corrected_text = text

        for pattern, replacement in self.contextual_corrections.items():
            matches = list(re.finditer(pattern, text, re.IGNORECASE))

            for match in matches:
                matched_text = match.group()
                start_pos = match.start()

                # Get context
                context_start = max(0, start_pos - 40)
                context_end = min(len(text), start_pos + len(matched_text) + 40)
                context = text[context_start:context_end].strip()

                issues.append({
                    'type': 'contextual',
                    'severity': 'medium',
                    'matched_text': matched_text,
                    'suggested_replacement': replacement,
                    'position': start_pos,
                    'context': context,
                    'rule': f'{pattern} -> {replacement}'
                })

                corrections[matched_text] = replacement

                if auto_correct:
                    corrected_text = re.sub(
                        pattern,
                        replacement,
                        corrected_text,
                        flags=re.IGNORECASE
                    )

        return issues, corrections, corrected_text

    def _check_australian_specific(self, text: str, auto_correct: bool) -> Tuple[List, Dict, str]:
        """Check for Australian-specific terminology and conventions."""
        issues = []
        corrections = {}
        corrected_text = text

        for pattern, replacement in self.australian_specific.items():
            matches = list(re.finditer(pattern, text, re.IGNORECASE))

            for match in matches:
                matched_text = match.group()
                start_pos = match.start()

                # Get context
                context_start = max(0, start_pos - 30)
                context_end = min(len(text), start_pos + len(matched_text) + 30)
                context = text[context_start:context_end].strip()

                issues.append({
                    'type': 'australian_specific',
                    'severity': 'low',
                    'matched_text': matched_text,
                    'suggested_replacement': replacement,
                    'position': start_pos,
                    'context': context,
                    'rule': f'{pattern} -> {replacement}'
                })

                corrections[matched_text] = replacement

                if auto_correct:
                    corrected_text = re.sub(
                        pattern,
                        replacement,
                        corrected_text,
                        flags=re.IGNORECASE
                    )

        return issues, corrections, corrected_text

    def validate_file(self, file_path: str, auto_correct: bool = False) -> Dict:
        """
        Validate a file for British English compliance.

        Args:
            file_path: Path to file to validate
            auto_correct: Whether to save corrected version

        Returns:
            Validation result dictionary
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            result = self.validate_text(content, auto_correct)
            result['file_path'] = file_path

            if auto_correct and result['corrected_text']:
                # Create backup
                backup_path = file_path + '.backup'
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                # Save corrected version
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(result['corrected_text'])

                result['backup_created'] = backup_path
                result['file_updated'] = True

            return result

        except Exception as e:
            return {
                'status': 'error',
                'file_path': file_path,
                'message': str(e),
                'compliant': False
            }

    def generate_style_guide(self) -> str:
        """Generate British English style guide for reference."""
        guide_sections = []

        guide_sections.append("# British English Style Guide")
        guide_sections.append("## Bigger Boss Agent System - Language Standards")
        guide_sections.append("")
        guide_sections.append(f"Generated: {datetime.now().strftime('%d %B %Y')}")
        guide_sections.append("")

        # Spelling section
        guide_sections.append("## Spelling Conventions")
        guide_sections.append("")
        guide_sections.append("### -ise vs -ize endings")
        guide_sections.append("Use British -ise endings:")
        ise_examples = [
            ('organize', 'organise'),
            ('realize', 'realise'),
            ('optimize', 'optimise'),
            ('analyze', 'analyse'),
            ('recognize', 'recognise'),
            ('specialize', 'specialise')
        ]
        for american, british in ise_examples:
            guide_sections.append(f"- {american} → **{british}**")

        guide_sections.append("")
        guide_sections.append("### -our vs -or endings")
        guide_sections.append("Use British -our endings:")
        our_examples = [
            ('color', 'colour'),
            ('honor', 'honour'),
            ('favor', 'favour'),
            ('behavior', 'behaviour'),
            ('neighbor', 'neighbour')
        ]
        for american, british in our_examples:
            guide_sections.append(f"- {american} → **{british}**")

        guide_sections.append("")
        guide_sections.append("### -re vs -er endings")
        guide_sections.append("Use British -re endings:")
        re_examples = [
            ('center', 'centre'),
            ('theater', 'theatre'),
            ('meter', 'metre'),
            ('liter', 'litre')
        ]
        for american, british in re_examples:
            guide_sections.append(f"- {american} → **{british}**")

        # Terminology section
        guide_sections.append("")
        guide_sections.append("## Terminology Preferences")
        guide_sections.append("")
        guide_sections.append("### Technology Terms")
        tech_terms = [
            ('cell phone', 'mobile phone'),
            ('resume', 'CV'),
            ('zip code', 'postcode')
        ]
        for american, british in tech_terms:
            guide_sections.append(f"- {american} → **{british}**")

        guide_sections.append("")
        guide_sections.append("### Business Terms")
        business_terms = [
            ('elevator', 'lift'),
            ('apartment', 'flat'),
            ('vacation', 'holiday'),
            ('trash', 'rubbish')
        ]
        for american, british in business_terms:
            guide_sections.append(f"- {american} → **{british}**")

        # Australian specific section
        guide_sections.append("")
        guide_sections.append("## Australian Specifications")
        guide_sections.append("")
        guide_sections.append("### Currency")
        guide_sections.append("- Always specify AUD for dollar amounts")
        guide_sections.append("- Example: $1,500 AUD (not just $1,500)")
        guide_sections.append("")
        guide_sections.append("### Business Terms")
        guide_sections.append("- GST (Goods and Services Tax)")
        guide_sections.append("- ABN (Australian Business Number)")
        guide_sections.append("- ACN (Australian Company Number)")

        # Context-sensitive rules
        guide_sections.append("")
        guide_sections.append("## Context-Sensitive Rules")
        guide_sections.append("")
        guide_sections.append("### License vs Licence")
        guide_sections.append("- **Noun:** licence (driver's licence, business licence)")
        guide_sections.append("- **Verb:** license (to license software)")
        guide_sections.append("")
        guide_sections.append("### Practice vs Practise")
        guide_sections.append("- **Noun:** practice (medical practice)")
        guide_sections.append("- **Verb:** practise (to practise medicine)")

        return "\n".join(guide_sections)

    def batch_validate_files(self, directory: str, file_pattern: str = "*.md", auto_correct: bool = False) -> Dict:
        """
        Validate multiple files in a directory.

        Args:
            directory: Directory to scan
            file_pattern: File pattern to match
            auto_correct: Whether to correct files

        Returns:
            Batch validation results
        """
        from pathlib import Path
        import glob

        directory_path = Path(directory)
        if not directory_path.exists():
            return {
                'status': 'error',
                'message': f'Directory does not exist: {directory}',
                'results': []
            }

        # Find matching files
        pattern_path = directory_path / file_pattern
        matching_files = glob.glob(str(pattern_path), recursive=True)

        if not matching_files:
            return {
                'status': 'success',
                'message': f'No files found matching pattern: {file_pattern}',
                'results': [],
                'summary': {
                    'total_files': 0,
                    'compliant_files': 0,
                    'total_issues': 0,
                    'files_corrected': 0
                }
            }

        results = []
        total_issues = 0
        compliant_files = 0
        files_corrected = 0

        for file_path in matching_files:
            result = self.validate_file(file_path, auto_correct)
            results.append(result)

            if result.get('compliant', False):
                compliant_files += 1

            total_issues += result.get('total_issues', 0)

            if result.get('file_updated', False):
                files_corrected += 1

        compliance_rate = (compliant_files / len(results)) * 100 if results else 0

        return {
            'status': 'success',
            'validation_date': datetime.now().isoformat(),
            'directory': directory,
            'file_pattern': file_pattern,
            'auto_correct_enabled': auto_correct,
            'results': results,
            'summary': {
                'total_files': len(results),
                'compliant_files': compliant_files,
                'compliance_rate': round(compliance_rate, 1),
                'total_issues': total_issues,
                'files_corrected': files_corrected,
                'average_issues_per_file': round(total_issues / len(results), 1) if results else 0
            }
        }


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description='Validate and correct British English compliance'
    )

    parser.add_argument(
        'input',
        help='Text content, file path, or directory to validate'
    )
    parser.add_argument(
        '--content',
        help='Validate text content directly'
    )
    parser.add_argument(
        '--auto-correct',
        action='store_true',
        help='Automatically correct issues (creates backup for files)'
    )
    parser.add_argument(
        '--batch',
        action='store_true',
        help='Batch validate files in directory'
    )
    parser.add_argument(
        '--pattern',
        default='*.md',
        help='File pattern for batch validation (default: *.md)'
    )
    parser.add_argument(
        '--generate-guide',
        action='store_true',
        help='Generate British English style guide'
    )
    parser.add_argument(
        '--report',
        help='Save detailed report to file'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    validator = BritishEnglishValidator()

    try:
        if args.generate_guide:
            guide = validator.generate_style_guide()
            print(guide)

            if args.report:
                with open(args.report, 'w', encoding='utf-8') as f:
                    f.write(guide)
                print(f"\n📄 Style guide saved to: {args.report}")

            return

        if args.content:
            # Validate provided content
            results = validator.validate_text(args.content, args.auto_correct)
        elif args.batch:
            # Batch validate directory
            results = validator.batch_validate_files(args.input, args.pattern, args.auto_correct)
        else:
            # Validate single file
            results = validator.validate_file(args.input, args.auto_correct)

        # Display results
        if args.batch:
            # Batch results
            summary = results.get('summary', {})
            print(f"📊 British English Validation Results")
            print(f"📁 Directory: {results.get('directory')}")
            print(f"📄 Files Processed: {summary.get('total_files', 0)}")
            print(f"✅ Compliant Files: {summary.get('compliant_files', 0)}")
            print(f"📈 Compliance Rate: {summary.get('compliance_rate', 0)}%")
            print(f"⚠️  Total Issues: {summary.get('total_issues', 0)}")

            if args.auto_correct:
                print(f"🔧 Files Corrected: {summary.get('files_corrected', 0)}")

            # Show detailed issues for non-compliant files
            non_compliant = [r for r in results.get('results', []) if not r.get('compliant', True)]
            if non_compliant and not args.auto_correct:
                print(f"\n⚠️  Issues found in {len(non_compliant)} files:")
                for result in non_compliant[:5]:  # Show first 5
                    file_name = Path(result.get('file_path', '')).name
                    issues = result.get('total_issues', 0)
                    print(f"  • {file_name}: {issues} issues")

        else:
            # Single file/content results
            if results.get('status') == 'error':
                print(f"❌ Error: {results.get('message')}")
                sys.exit(1)

            compliant = results.get('compliant', False)
            score = results.get('compliance_score', 0)
            issues = results.get('total_issues', 0)

            status_icon = "✅" if compliant else "⚠️"
            print(f"{status_icon} British English Compliance: {score}%")

            if issues > 0:
                print(f"📋 Issues Found: {issues}")

                # Show issue breakdown
                categories = results.get('categories', {})
                for category, count in categories.items():
                    if count > 0:
                        print(f"  • {category.title()}: {count} issues")

                # Show some example issues
                issue_list = results.get('issues', [])
                if issue_list and not args.auto_correct:
                    print(f"\nExample issues:")
                    for issue in issue_list[:3]:  # Show first 3
                        american = issue.get('american_word') or issue.get('american_term') or issue.get('matched_text')
                        british = issue.get('british_word') or issue.get('british_term') or issue.get('suggested_replacement')
                        print(f"  • {american} → {british}")

                if not args.auto_correct:
                    print(f"\n💡 Use --auto-correct to fix these issues automatically")

            if args.auto_correct and results.get('file_updated'):
                backup = results.get('backup_created')
                print(f"✅ File corrected successfully")
                if backup:
                    print(f"🔄 Backup created: {backup}")

        # Save detailed report if requested
        if args.report and not args.generate_guide:
            with open(args.report, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False, default=str)
            print(f"\n📄 Detailed report saved to: {args.report}")

        # Exit with appropriate code
        if args.batch:
            success = results.get('summary', {}).get('total_issues', 1) == 0
        else:
            success = results.get('compliant', False)

        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()