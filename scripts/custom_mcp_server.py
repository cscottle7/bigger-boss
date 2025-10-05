#!/usr/bin/env python3
"""
Bigger Boss Agent System - Custom MCP Server
Provides Bigger Boss specific tools and validations through MCP protocol.
"""

import asyncio
import json
import logging
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Load environment variables from .env file
try:
    from decouple import config
    JINA_API_KEY = config('JINA_API_KEY', default=None)
except ImportError:
    JINA_API_KEY = os.getenv('JINA_API_KEY')

# MCP Protocol Implementation (simplified)
class MCPServer:
    """Custom MCP server for Bigger Boss operations."""

    def __init__(self):
        self.tools = {}
        self.logger = self._setup_logging()
        self.client_data_path = Path(os.getenv('CLIENT_DATA_PATH', 'clients'))

        # British spellings dictionary
        self.british_spellings = {
            r'\borganization\b': 'organisation',
            r'\borganizations\b': 'organisations',
            r'\borganizational\b': 'organisational',
            r'\brealize\b': 'realise',
            r'\brealizes\b': 'realises',
            r'\brealized\b': 'realised',
            r'\brealizing\b': 'realising',
            r'\boptimize\b': 'optimise',
            r'\boptimizes\b': 'optimises',
            r'\boptimized\b': 'optimised',
            r'\boptimizing\b': 'optimising',
            r'\banalyze\b': 'analyse',
            r'\banalyzes\b': 'analyses',
            r'\banalyzed\b': 'analysed',
            r'\banalyzing\b': 'analysing',
            r'\bcolor\b': 'colour',
            r'\bcolors\b': 'colours',
            r'\bcenter\b': 'centre',
            r'\bcentered\b': 'centred',
            r'\bcentering\b': 'centring',
            r'\bfavor\b': 'favour',
            r'\bfavors\b': 'favours',
            r'\bfavored\b': 'favoured',
            r'\bfavoring\b': 'favouring',
            r'\bhonor\b': 'honour',
            r'\bhonors\b': 'honours',
            r'\bhonored\b': 'honoured',
            r'\bhonoring\b': 'honouring',
            r'\bbehavior\b': 'behaviour',
            r'\bbehaviors\b': 'behaviours',
            r'\bbehavioral\b': 'behavioural',
            r'\btraveled\b': 'travelled',
            r'\btraveling\b': 'travelling',
            r'\bcanceled\b': 'cancelled',
            r'\bcanceling\b': 'cancelling',
            r'\bdefense\b': 'defence',
            r'\bdefenses\b': 'defences',
        }

        self._register_tools()

    def _setup_logging(self) -> logging.Logger:
        """Set up logging configuration."""
        logger = logging.getLogger('bigger_boss_mcp')
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def _register_tools(self):
        """Register all available MCP tools."""
        self.tools = {
            'client_folder_validation': self._validate_client_folder,
            'research_phase_verification': self._verify_research_phases,
            'british_english_validation': self._validate_british_english,
            'content_quality_scoring': self._score_content_quality,
            'workflow_orchestration': self._orchestrate_workflow,
        }

    async def _validate_client_folder(self, client_domain: str, auto_fix: bool = False) -> Dict[str, Any]:
        """
        Validate client folder structure compliance.

        Args:
            client_domain: Client domain name
            auto_fix: Whether to automatically fix issues

        Returns:
            Validation result with compliance status and issues
        """
        try:
            client_path = self.client_data_path / client_domain

            if not client_path.exists():
                return {
                    'status': 'error',
                    'message': f'Client folder does not exist: {client_path}',
                    'compliant': False
                }

            # Required folder structure
            required_folders = [
                'strategy',
                'research',
                'content',
                'technical',
                'implementation'
            ]

            required_files = [
                'README.md',
                'PROJECT_OVERVIEW.md'
            ]

            issues = []
            compliant = True

            # Check folders
            for folder in required_folders:
                folder_path = client_path / folder
                if not folder_path.exists():
                    issues.append(f'Missing required folder: {folder}')
                    compliant = False

                    if auto_fix:
                        folder_path.mkdir(parents=True, exist_ok=True)
                        self.logger.info(f'Created missing folder: {folder_path}')

            # Check files
            for file in required_files:
                file_path = client_path / file
                if not file_path.exists():
                    issues.append(f'Missing required file: {file}')
                    compliant = False

                    if auto_fix:
                        if file == 'README.md':
                            content = self._generate_readme_template(client_domain)
                        elif file == 'PROJECT_OVERVIEW.md':
                            content = self._generate_project_overview_template(client_domain)
                        else:
                            content = f'# {file.replace(".md", "").replace("_", " ").title()}\n\nContent pending...'

                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        self.logger.info(f'Created missing file: {file_path}')

            return {
                'status': 'success',
                'compliant': compliant,
                'issues': issues,
                'client_domain': client_domain,
                'auto_fixed': auto_fix,
                'checked_at': datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f'Error validating client folder: {e}')
            return {
                'status': 'error',
                'message': str(e),
                'compliant': False
            }

    async def _verify_research_phases(self, client_domain: str, required_phases: List[int]) -> Dict[str, Any]:
        """
        Verify that required research phases are completed.

        Args:
            client_domain: Client domain name
            required_phases: List of phase numbers (1, 2, 3, 4)

        Returns:
            Verification result with completion status
        """
        try:
            client_path = self.client_data_path / client_domain
            research_path = client_path / 'research'

            if not research_path.exists():
                return {
                    'status': 'error',
                    'message': f'Research folder does not exist: {research_path}',
                    'phases_completed': []
                }

            # Phase file mappings
            phase_files = {
                1: ['audience_personas.md', 'competitive_analysis.md', 'market_research.md'],
                2: ['trending_topics_research.md', 'content_gap_analysis.md', 'search_landscape_analysis.md'],
                3: ['keyword_research.md', 'search_intent_analysis.md', 'keyword_gap_analysis.md'],
                4: ['content_briefs.md', 'ai_optimization_guide.md', 'content_calendar.md']
            }

            completed_phases = []
            missing_phases = []

            for phase in required_phases:
                phase_complete = False
                required_files = phase_files.get(phase, [])

                for file_name in required_files:
                    file_path = research_path / file_name
                    if file_path.exists() and file_path.stat().st_size > 100:  # Minimum content check
                        phase_complete = True
                        break

                if phase_complete:
                    completed_phases.append(phase)
                else:
                    missing_phases.append({
                        'phase': phase,
                        'required_files': required_files,
                        'description': self._get_phase_description(phase)
                    })

            all_phases_complete = len(missing_phases) == 0

            return {
                'status': 'success',
                'all_phases_complete': all_phases_complete,
                'completed_phases': completed_phases,
                'missing_phases': missing_phases,
                'client_domain': client_domain,
                'checked_at': datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f'Error verifying research phases: {e}')
            return {
                'status': 'error',
                'message': str(e),
                'phases_completed': []
            }

    async def _validate_british_english(self, content: str, auto_correct: bool = False) -> Dict[str, Any]:
        """
        Validate British English spelling and terminology.

        Args:
            content: Text content to validate
            auto_correct: Whether to return corrected content

        Returns:
            Validation result with issues found and corrections
        """
        try:
            issues = []
            corrections = {}
            corrected_content = content

            # Check for American spellings
            for american_pattern, british_spelling in self.british_spellings.items():
                matches = re.finditer(american_pattern, content, re.IGNORECASE)
                for match in matches:
                    american_word = match.group()
                    issues.append({
                        'type': 'american_spelling',
                        'word': american_word,
                        'position': match.start(),
                        'suggestion': british_spelling,
                        'context': content[max(0, match.start() - 20):match.end() + 20]
                    })
                    corrections[american_word] = british_spelling

                    if auto_correct:
                        corrected_content = re.sub(
                            american_pattern,
                            british_spelling,
                            corrected_content,
                            flags=re.IGNORECASE
                        )

            # Check for American terminology
            american_terms = {
                r'\bcell phone\b': 'mobile phone',
                r'\belevator\b': 'lift',
                r'\bresume\b': 'CV',
                r'\bzip code\b': 'postcode',
                r'\bcolor scheme\b': 'colour scheme',
                r'\bgas station\b': 'petrol station',
                r'\btrash\b': 'rubbish',
                r'\bapartment\b': 'flat',
                r'\bvacation\b': 'holiday',
                r'\btruck\b': 'lorry',
                r'\bcookies\b(?=.*privacy)': 'biscuits',  # Context-aware
            }

            for american_term, british_term in american_terms.items():
                matches = re.finditer(american_term, content, re.IGNORECASE)
                for match in matches:
                    american_phrase = match.group()
                    issues.append({
                        'type': 'american_terminology',
                        'phrase': american_phrase,
                        'position': match.start(),
                        'suggestion': british_term,
                        'context': content[max(0, match.start() - 20):match.end() + 20]
                    })
                    corrections[american_phrase] = british_term

                    if auto_correct:
                        corrected_content = re.sub(
                            american_term,
                            british_term,
                            corrected_content,
                            flags=re.IGNORECASE
                        )

            compliance_score = max(0, 100 - (len(issues) * 5))  # Deduct 5 points per issue

            return {
                'status': 'success',
                'compliant': len(issues) == 0,
                'compliance_score': compliance_score,
                'issues_found': len(issues),
                'issues': issues,
                'corrections': corrections,
                'corrected_content': corrected_content if auto_correct else None,
                'checked_at': datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f'Error validating British English: {e}')
            return {
                'status': 'error',
                'message': str(e),
                'compliant': False
            }

    async def _score_content_quality(self, content: str, criteria: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Score content quality using multiple criteria.

        Args:
            content: Content to score
            criteria: Custom scoring criteria

        Returns:
            Quality score and detailed analysis
        """
        try:
            if criteria is None:
                criteria = {
                    'min_word_count': 300,
                    'max_sentence_length': 25,
                    'readability_target': 60,  # Flesch reading ease
                    'heading_structure': True,
                    'citation_required': True
                }

            scores = {}
            analysis = {}

            # Word count analysis
            words = content.split()
            word_count = len(words)
            scores['word_count'] = min(10, (word_count / criteria['min_word_count']) * 10)
            analysis['word_count'] = {
                'count': word_count,
                'target': criteria['min_word_count'],
                'meets_target': word_count >= criteria['min_word_count']
            }

            # Sentence structure analysis
            sentences = re.split(r'[.!?]+', content)
            sentence_lengths = [len(sentence.split()) for sentence in sentences if sentence.strip()]
            avg_sentence_length = sum(sentence_lengths) / len(sentence_lengths) if sentence_lengths else 0
            long_sentences = [s for s in sentence_lengths if s > criteria['max_sentence_length']]

            scores['sentence_structure'] = max(0, 10 - len(long_sentences))
            analysis['sentence_structure'] = {
                'average_length': round(avg_sentence_length, 1),
                'long_sentences': len(long_sentences),
                'target_max_length': criteria['max_sentence_length']
            }

            # Heading structure analysis
            h1_count = len(re.findall(r'^# ', content, re.MULTILINE))
            h2_count = len(re.findall(r'^## ', content, re.MULTILINE))
            h3_count = len(re.findall(r'^### ', content, re.MULTILINE))

            has_structure = h1_count >= 1 and (h2_count >= 2 or h3_count >= 2)
            scores['heading_structure'] = 10 if has_structure else 5
            analysis['heading_structure'] = {
                'h1_count': h1_count,
                'h2_count': h2_count,
                'h3_count': h3_count,
                'has_proper_structure': has_structure
            }

            # Citation analysis
            citation_patterns = [
                r'\*\*Source:\*\*',
                r'Source:',
                r'\[.*\]\(http',
                r'according to.*\d{4}',
                r'study.*found',
                r'research.*shows'
            ]

            citations_found = sum(len(re.findall(pattern, content, re.IGNORECASE))
                                for pattern in citation_patterns)

            scores['citations'] = min(10, citations_found * 2)
            analysis['citations'] = {
                'citations_found': citations_found,
                'required': criteria['citation_required'],
                'meets_requirement': citations_found > 0 if criteria['citation_required'] else True
            }

            # Readability estimate (simplified Flesch formula)
            total_sentences = len(sentences)
            total_syllables = self._estimate_syllables(content)

            if total_sentences > 0 and word_count > 0:
                flesch_score = (206.835 - 1.015 * (word_count / total_sentences) -
                               84.6 * (total_syllables / word_count))
            else:
                flesch_score = 0

            scores['readability'] = max(0, min(10, flesch_score / 10))
            analysis['readability'] = {
                'flesch_score': round(flesch_score, 1),
                'target_score': criteria['readability_target'],
                'reading_level': self._get_reading_level(flesch_score)
            }

            # Calculate overall score
            overall_score = sum(scores.values()) / len(scores)

            # Quality rating
            if overall_score >= 8.5:
                quality_rating = 'Excellent'
            elif overall_score >= 7.0:
                quality_rating = 'Good'
            elif overall_score >= 5.5:
                quality_rating = 'Fair'
            else:
                quality_rating = 'Needs Improvement'

            return {
                'status': 'success',
                'overall_score': round(overall_score, 2),
                'quality_rating': quality_rating,
                'individual_scores': {k: round(v, 2) for k, v in scores.items()},
                'detailed_analysis': analysis,
                'recommendations': self._generate_recommendations(scores, analysis),
                'scored_at': datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f'Error scoring content quality: {e}')
            return {
                'status': 'error',
                'message': str(e),
                'overall_score': 0
            }

    async def _orchestrate_workflow(self, workflow_type: str, parameters: Dict) -> Dict[str, Any]:
        """
        Orchestrate workflow execution with proper agent coordination.

        Args:
            workflow_type: Type of workflow to execute
            parameters: Workflow parameters

        Returns:
            Workflow execution result
        """
        try:
            workflow_templates = {
                'research_workflow': {
                    'phases': [
                        {
                            'name': 'foundation_research',
                            'agents': ['research_strategist', 'niche_trend_researcher'],
                            'deliverables': ['audience_personas.md', 'market_research.md'],
                            'validation': 'research_phase_verification'
                        },
                        {
                            'name': 'competitive_intelligence',
                            'agents': ['competitive_intelligence_searcher'],
                            'deliverables': ['competitive_analysis.md', 'content_gap_analysis.md'],
                            'validation': 'research_phase_verification'
                        },
                        {
                            'name': 'keyword_research',
                            'agents': ['keyword_researcher'],
                            'deliverables': ['keyword_research.md', 'search_intent_analysis.md'],
                            'validation': 'research_phase_verification'
                        },
                        {
                            'name': 'content_planning',
                            'agents': ['content_strategist'],
                            'deliverables': ['content_briefs.md', 'content_calendar.md'],
                            'validation': 'research_phase_verification'
                        }
                    ]
                },
                'content_creation_workflow': {
                    'phases': [
                        {
                            'name': 'content_creation',
                            'agents': ['content_creator', 'seo_optimiser'],
                            'validation': 'content_quality_scoring'
                        },
                        {
                            'name': 'quality_review',
                            'agents': ['clarity_conciseness_editor', 'ai_text_naturalizer'],
                            'validation': 'content_quality_scoring'
                        }
                    ]
                }
            }

            if workflow_type not in workflow_templates:
                return {
                    'status': 'error',
                    'message': f'Unknown workflow type: {workflow_type}',
                    'available_workflows': list(workflow_templates.keys())
                }

            workflow = workflow_templates[workflow_type]
            client_domain = parameters.get('client_domain')

            execution_plan = {
                'workflow_type': workflow_type,
                'client_domain': client_domain,
                'phases': workflow['phases'],
                'started_at': datetime.now().isoformat(),
                'status': 'planned'
            }

            # Validate prerequisites
            if client_domain:
                validation_result = await self._validate_client_folder(client_domain, auto_fix=True)
                if not validation_result.get('compliant', False):
                    execution_plan['status'] = 'failed'
                    execution_plan['error'] = 'Client folder validation failed'
                    return execution_plan

            execution_plan['status'] = 'ready'
            execution_plan['next_action'] = f"Execute {workflow['phases'][0]['name']} phase"

            return {
                'status': 'success',
                'execution_plan': execution_plan
            }

        except Exception as e:
            self.logger.error(f'Error orchestrating workflow: {e}')
            return {
                'status': 'error',
                'message': str(e)
            }

    def _generate_readme_template(self, client_domain: str) -> str:
        """Generate README.md template for client."""
        return f"""# {client_domain.replace('_', ' ').title()} - Project Navigation Hub

## Project Overview
Marketing strategy and content development project for {client_domain.replace('_', '.')}.

## Folder Structure

### Strategy
- Research brief and strategic planning documents
- Current website analysis
- Implementation roadmap

### Research
- Market intelligence and competitive analysis
- Audience personas and demographic research
- Keyword research and SEO analysis

### Content
- Content strategy and planning documents
- Website content briefs
- Marketing materials and messaging

### Technical
- Technical audits and recommendations
- AI optimisation guides
- UX/UI analysis

### Implementation
- Task dependency planning
- Execution tracking and progress reports
- Quality assurance documentation

## Project Status
- **Created:** {datetime.now().strftime('%d %B %Y')}
- **Status:** In Progress
- **Last Updated:** {datetime.now().strftime('%d %B %Y')}

## Key Deliverables
- [ ] Research Brief
- [ ] Audience Personas
- [ ] Competitive Analysis
- [ ] Content Strategy
- [ ] Implementation Plan

## Quick Links
- [Project Overview](PROJECT_OVERVIEW.md)
- [Research Strategy](strategy/research_brief.md)
- [Implementation Plan](strategy/implementation_plan.md)
"""

    def _generate_project_overview_template(self, client_domain: str) -> str:
        """Generate PROJECT_OVERVIEW.md template for client."""
        return f"""# {client_domain.replace('_', ' ').title()} - Project Overview

## Executive Summary
Comprehensive marketing strategy and content development project for {client_domain.replace('_', '.')}.

## Project Objectives
- Enhance online presence and digital marketing effectiveness
- Develop comprehensive content strategy
- Improve search engine optimisation and visibility
- Create systematic approach to content creation and marketing

## Project Scope

### Research Phase
- Market analysis and competitive intelligence
- Audience research and persona development
- SEO and keyword research
- Content gap analysis

### Strategy Development
- Content strategy and planning
- Marketing funnel optimisation
- Brand messaging and positioning
- Distribution channel strategy

### Implementation
- Content creation and optimisation
- Website improvements and technical SEO
- Marketing automation setup
- Performance monitoring and reporting

## Timeline
- **Project Start:** {datetime.now().strftime('%B %Y')}
- **Research Phase:** 4 weeks
- **Strategy Development:** 2 weeks
- **Implementation:** Ongoing
- **Review and Optimisation:** Monthly

## Success Metrics
- Increased organic search visibility
- Improved content engagement rates
- Enhanced lead generation and conversion
- Systematic content production workflow

## Team Structure
- **Research Team:** Market analysis and competitive intelligence
- **Content Team:** Content creation and optimisation
- **Technical Team:** SEO and website optimisation
- **Strategy Team:** Planning and coordination

---
*Last Updated: {datetime.now().strftime('%d %B %Y')}*
"""

    def _get_phase_description(self, phase: int) -> str:
        """Get description for research phase."""
        descriptions = {
            1: "Foundation Research - Audience analysis, market research, and competitive positioning",
            2: "Competitive Intelligence - Market trends, content gaps, and search landscape analysis",
            3: "SEO & Keyword Strategy - Comprehensive keyword research and search intent mapping",
            4: "Content Planning - Detailed content briefs, AI optimisation, and content calendar"
        }
        return descriptions.get(phase, f"Phase {phase}")

    def _estimate_syllables(self, text: str) -> int:
        """Estimate syllable count for readability calculation."""
        words = re.findall(r'\b\w+\b', text.lower())
        total_syllables = 0

        for word in words:
            # Simple syllable counting heuristic
            syllables = max(1, len(re.findall(r'[aeiou]', word)) -
                           len(re.findall(r'[aeiou]{2}', word)))
            if word.endswith('e'):
                syllables -= 1
            total_syllables += max(1, syllables)

        return total_syllables

    def _get_reading_level(self, flesch_score: float) -> str:
        """Convert Flesch score to reading level."""
        if flesch_score >= 90:
            return "Very Easy"
        elif flesch_score >= 80:
            return "Easy"
        elif flesch_score >= 70:
            return "Fairly Easy"
        elif flesch_score >= 60:
            return "Standard"
        elif flesch_score >= 50:
            return "Fairly Difficult"
        elif flesch_score >= 30:
            return "Difficult"
        else:
            return "Very Difficult"

    def _generate_recommendations(self, scores: Dict, analysis: Dict) -> List[str]:
        """Generate improvement recommendations based on scores."""
        recommendations = []

        if scores.get('word_count', 0) < 7:
            recommendations.append("Increase content length to meet minimum word count requirements")

        if scores.get('sentence_structure', 0) < 7:
            recommendations.append("Break down long sentences for better readability")

        if scores.get('heading_structure', 0) < 8:
            recommendations.append("Improve heading structure with proper H1, H2, and H3 tags")

        if scores.get('citations', 0) < 5:
            recommendations.append("Add credible source citations for statistics and claims")

        if scores.get('readability', 0) < 6:
            recommendations.append("Improve readability by using simpler language and shorter sentences")

        return recommendations

    async def handle_request(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP tool requests."""
        if tool_name not in self.tools:
            return {
                'status': 'error',
                'message': f'Unknown tool: {tool_name}',
                'available_tools': list(self.tools.keys())
            }

        try:
            result = await self.tools[tool_name](**parameters)
            return result
        except Exception as e:
            self.logger.error(f'Error executing tool {tool_name}: {e}')
            return {
                'status': 'error',
                'message': str(e),
                'tool': tool_name,
                'parameters': parameters
            }

    def run_server(self):
        """Run the MCP server."""
        self.logger.info("Starting Bigger Boss Custom MCP Server...")

        # Simple stdin/stdout MCP implementation
        while True:
            try:
                line = sys.stdin.readline()
                if not line:
                    break

                request = json.loads(line.strip())

                if request.get('method') == 'tools/call':
                    params = request.get('params', {})
                    tool_name = params.get('name', '')
                    tool_parameters = params.get('arguments', {})

                    # Run async handler
                    result = asyncio.run(self.handle_request(tool_name, tool_parameters))

                    response = {
                        'jsonrpc': '2.0',
                        'id': request.get('id'),
                        'result': {
                            'content': [
                                {
                                    'type': 'text',
                                    'text': json.dumps(result, indent=2)
                                }
                            ]
                        }
                    }

                    print(json.dumps(response))
                    sys.stdout.flush()

            except KeyboardInterrupt:
                break
            except Exception as e:
                self.logger.error(f'Server error: {e}')
                continue

        self.logger.info("Bigger Boss Custom MCP Server stopped")


if __name__ == "__main__":
    server = MCPServer()
    server.run_server()