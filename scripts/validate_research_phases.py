#!/usr/bin/env python3
"""
Bigger Boss Agent System - Research Phase Validator
Validates completion of mandatory research phases before content creation.
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ResearchPhaseValidator:
    """Validator for research phase completion."""

    def __init__(self):
        self.phase_requirements = {
            1: {
                'name': 'Foundation Research & Strategic Analysis',
                'description': 'Market research, audience analysis, and strategic positioning',
                'required_files': [
                    'audience_personas.md',
                    'market_research.md',
                    'competitive_analysis.md'
                ],
                'optional_files': [
                    'brand_swot_analysis.md',
                    'usp_analysis.md',
                    'market_positioning.md'
                ],
                'minimum_file_size': 500,  # bytes
                'key_content_indicators': [
                    'demographics',
                    'psychographics',
                    'target audience',
                    'competitor analysis',
                    'market research'
                ]
            },
            2: {
                'name': 'Competitive Intelligence & Search Landscape',
                'description': 'Competitor analysis, trending topics, and search landscape mapping',
                'required_files': [
                    'trending_topics_research.md',
                    'content_gap_analysis.md',
                    'search_landscape_analysis.md'
                ],
                'optional_files': [
                    'competitor_content_audit.md',
                    'brand_positioning_analysis.md',
                    'seasonal_trends.md'
                ],
                'minimum_file_size': 400,
                'key_content_indicators': [
                    'trending topics',
                    'content gaps',
                    'search volume',
                    'competition analysis',
                    'market trends'
                ]
            },
            3: {
                'name': 'Advanced SEO & Keyword Strategy',
                'description': 'Comprehensive keyword research and search intent mapping',
                'required_files': [
                    'keyword_research.md',
                    'search_intent_analysis.md',
                    'keyword_gap_analysis.md'
                ],
                'optional_files': [
                    'funnel_stage_keywords.md',
                    'untapped_keywords.md',
                    'emerging_trends_keywords.md'
                ],
                'minimum_file_size': 600,
                'key_content_indicators': [
                    'keyword research',
                    'search intent',
                    'search volume',
                    'keyword difficulty',
                    'long-tail keywords'
                ]
            },
            4: {
                'name': 'Content Planning, Briefs & AI Optimization',
                'description': 'Detailed content briefs and AI-ready content structure',
                'required_files': [
                    'content_briefs.md',
                    'ai_optimization_guide.md',
                    'content_calendar.md'
                ],
                'optional_files': [
                    'content_structure_specs.md',
                    'future_content_calendar.md',
                    'content_cluster_mapping.md'
                ],
                'minimum_file_size': 800,
                'key_content_indicators': [
                    'content brief',
                    'content calendar',
                    'ai optimization',
                    'content structure',
                    'publishing schedule'
                ]
            }
        }

    def validate_research_phase(self, client_domain: str, phase: int) -> Dict:
        """
        Validate a specific research phase for completion.

        Args:
            client_domain: Client domain name
            phase: Phase number (1-4)

        Returns:
            Validation result dictionary
        """
        if phase not in self.phase_requirements:
            return {
                'status': 'error',
                'message': f'Invalid phase number: {phase}. Must be 1-4.',
                'phase_complete': False
            }

        client_path = Path(f'clients/{client_domain}')
        research_path = client_path / 'research'

        if not research_path.exists():
            return {
                'status': 'error',
                'message': f'Research folder does not exist: {research_path}',
                'phase_complete': False,
                'client_domain': client_domain,
                'phase': phase
            }

        phase_info = self.phase_requirements[phase]
        results = {
            'status': 'success',
            'client_domain': client_domain,
            'phase': phase,
            'phase_name': phase_info['name'],
            'phase_description': phase_info['description'],
            'phase_complete': False,
            'completion_score': 0,
            'file_checks': [],
            'content_analysis': {},
            'recommendations': [],
            'validated_at': datetime.now().isoformat()
        }

        # Check required files
        required_files_found = 0
        total_required = len(phase_info['required_files'])

        for filename in phase_info['required_files']:
            file_path = research_path / filename
            file_check = self._check_file_quality(file_path, phase_info, filename, required=True)
            results['file_checks'].append(file_check)

            if file_check['exists'] and file_check['meets_requirements']:
                required_files_found += 1

        # Check optional files (bonus points)
        optional_files_found = 0
        total_optional = len(phase_info['optional_files'])

        for filename in phase_info['optional_files']:
            file_path = research_path / filename
            file_check = self._check_file_quality(file_path, phase_info, filename, required=False)
            results['file_checks'].append(file_check)

            if file_check['exists'] and file_check['meets_requirements']:
                optional_files_found += 1

        # Calculate completion score
        required_score = (required_files_found / total_required) * 80  # 80% for required files
        optional_score = (optional_files_found / total_optional) * 20  # 20% for optional files
        results['completion_score'] = round(required_score + optional_score, 1)

        # Phase is complete if at least 70% of required files are present and meet quality standards
        results['phase_complete'] = required_files_found >= max(1, int(total_required * 0.7))

        # Content analysis
        results['content_analysis'] = self._analyze_phase_content(research_path, phase_info)

        # Generate recommendations
        results['recommendations'] = self._generate_phase_recommendations(results)

        return results

    def _check_file_quality(self, file_path: Path, phase_info: Dict, filename: str, required: bool) -> Dict:
        """Check individual file for existence and quality."""
        file_check = {
            'filename': filename,
            'required': required,
            'exists': False,
            'file_size': 0,
            'meets_size_requirement': False,
            'has_key_content': False,
            'content_indicators_found': [],
            'meets_requirements': False,
            'issues': []
        }

        if not file_path.exists():
            file_check['issues'].append('File does not exist')
            return file_check

        file_check['exists'] = True

        try:
            # Check file size
            file_size = file_path.stat().st_size
            file_check['file_size'] = file_size
            file_check['meets_size_requirement'] = file_size >= phase_info['minimum_file_size']

            if not file_check['meets_size_requirement']:
                file_check['issues'].append(f'File too small ({file_size} bytes, minimum {phase_info["minimum_file_size"]})')

            # Check content quality
            content = file_path.read_text(encoding='utf-8').lower()

            # Check for key content indicators
            indicators_found = []
            for indicator in phase_info['key_content_indicators']:
                if indicator.lower() in content:
                    indicators_found.append(indicator)

            file_check['content_indicators_found'] = indicators_found
            file_check['has_key_content'] = len(indicators_found) >= 2  # At least 2 key indicators

            if not file_check['has_key_content']:
                file_check['issues'].append(f'Missing key content indicators (found {len(indicators_found)}/2 minimum)')

            # Overall requirement check
            file_check['meets_requirements'] = (
                file_check['meets_size_requirement'] and
                file_check['has_key_content']
            )

            if not file_check['issues']:
                file_check['issues'] = []  # Clear issues if all checks pass

        except Exception as e:
            file_check['issues'].append(f'Error reading file: {str(e)}')

        return file_check

    def _analyze_phase_content(self, research_path: Path, phase_info: Dict) -> Dict:
        """Analyze overall content quality for the phase."""
        analysis = {
            'total_words': 0,
            'total_files_analyzed': 0,
            'key_topics_covered': [],
            'content_depth_score': 0,
            'research_quality_indicators': []
        }

        all_files = phase_info['required_files'] + phase_info['optional_files']

        for filename in all_files:
            file_path = research_path / filename
            if file_path.exists():
                try:
                    content = file_path.read_text(encoding='utf-8')
                    analysis['total_words'] += len(content.split())
                    analysis['total_files_analyzed'] += 1

                    # Check for research quality indicators
                    quality_indicators = [
                        ('data sources', 'references to data sources or research'),
                        ('statistics', 'numerical data and statistics'),
                        ('citations', 'source citations and references'),
                        ('methodology', 'research methodology mentioned'),
                        ('analysis', 'analytical insights and conclusions')
                    ]

                    for indicator, description in quality_indicators:
                        if indicator in content.lower():
                            if indicator not in analysis['research_quality_indicators']:
                                analysis['research_quality_indicators'].append(indicator)

                except Exception as e:
                    logger.warning(f'Error analyzing {filename}: {e}')

        # Calculate content depth score
        if analysis['total_files_analyzed'] > 0:
            avg_words_per_file = analysis['total_words'] / analysis['total_files_analyzed']
            # Score based on average words per file (0-10 scale)
            analysis['content_depth_score'] = min(10, avg_words_per_file / 100)

        return analysis

    def _generate_phase_recommendations(self, results: Dict) -> List[str]:
        """Generate specific recommendations based on validation results."""
        recommendations = []

        # File-specific recommendations
        for file_check in results['file_checks']:
            if not file_check['exists'] and file_check['required']:
                recommendations.append(f"Create required file: {file_check['filename']}")
            elif file_check['exists'] and file_check['issues']:
                recommendations.append(f"Improve {file_check['filename']}: {', '.join(file_check['issues'])}")

        # Content quality recommendations
        content_analysis = results.get('content_analysis', {})

        if content_analysis.get('total_words', 0) < 1000:
            recommendations.append("Expand research content - current total word count is below recommended minimum")

        if len(content_analysis.get('research_quality_indicators', [])) < 3:
            recommendations.append("Include more research quality indicators (data sources, statistics, citations)")

        # Phase-specific recommendations
        phase = results.get('phase')
        if phase == 1 and results['completion_score'] < 80:
            recommendations.append("Phase 1: Focus on detailed audience personas and competitive positioning")
        elif phase == 2 and results['completion_score'] < 80:
            recommendations.append("Phase 2: Conduct thorough trending topics research and content gap analysis")
        elif phase == 3 and results['completion_score'] < 80:
            recommendations.append("Phase 3: Complete comprehensive keyword research with search intent mapping")
        elif phase == 4 and results['completion_score'] < 80:
            recommendations.append("Phase 4: Develop detailed content briefs and AI optimization guidelines")

        # General recommendations
        if results['completion_score'] < 70:
            recommendations.append("Phase not yet ready for content creation - complete outstanding research requirements")

        return recommendations

    def validate_all_phases(self, client_domain: str, required_phases: List[int] = None) -> Dict:
        """
        Validate all research phases for a client.

        Args:
            client_domain: Client domain name
            required_phases: List of phase numbers to validate (default: all phases)

        Returns:
            Comprehensive validation results
        """
        if required_phases is None:
            required_phases = [1, 2, 3, 4]

        overall_results = {
            'status': 'success',
            'client_domain': client_domain,
            'validation_date': datetime.now().isoformat(),
            'required_phases': required_phases,
            'all_phases_complete': False,
            'overall_completion_score': 0,
            'phase_results': {},
            'content_creation_ready': False,
            'next_steps': [],
            'summary': {}
        }

        total_score = 0
        completed_phases = 0

        # Validate each required phase
        for phase in required_phases:
            phase_result = self.validate_research_phase(client_domain, phase)
            overall_results['phase_results'][phase] = phase_result

            total_score += phase_result.get('completion_score', 0)
            if phase_result.get('phase_complete', False):
                completed_phases += 1

        # Calculate overall metrics
        overall_results['overall_completion_score'] = round(total_score / len(required_phases), 1)
        overall_results['all_phases_complete'] = completed_phases == len(required_phases)
        overall_results['content_creation_ready'] = overall_results['overall_completion_score'] >= 75

        # Generate summary
        overall_results['summary'] = {
            'completed_phases': completed_phases,
            'total_required_phases': len(required_phases),
            'completion_percentage': round((completed_phases / len(required_phases)) * 100, 1),
            'ready_for_content_creation': overall_results['content_creation_ready']
        }

        # Generate next steps
        if not overall_results['all_phases_complete']:
            incomplete_phases = [phase for phase in required_phases
                               if not overall_results['phase_results'][phase].get('phase_complete', False)]

            for phase in incomplete_phases:
                phase_name = self.phase_requirements[phase]['name']
                overall_results['next_steps'].append(f"Complete Phase {phase}: {phase_name}")

            if not overall_results['content_creation_ready']:
                overall_results['next_steps'].append("Research phases must be completed before content creation can begin")

        else:
            overall_results['next_steps'].append("All research phases complete - ready to begin content creation")

        return overall_results

    def create_research_phase_templates(self, client_domain: str, phases: List[int] = None) -> Dict:
        """
        Create template files for research phases.

        Args:
            client_domain: Client domain name
            phases: List of phase numbers to create templates for

        Returns:
            Results of template creation
        """
        if phases is None:
            phases = [1, 2, 3, 4]

        client_path = Path(f'clients/{client_domain}')
        research_path = client_path / 'research'

        # Ensure research directory exists
        research_path.mkdir(parents=True, exist_ok=True)

        results = {
            'status': 'success',
            'client_domain': client_domain,
            'templates_created': [],
            'templates_skipped': [],  # Already exist
            'errors': []
        }

        for phase in phases:
            if phase not in self.phase_requirements:
                results['errors'].append(f'Invalid phase number: {phase}')
                continue

            phase_info = self.phase_requirements[phase]

            for filename in phase_info['required_files']:
                file_path = research_path / filename

                if file_path.exists():
                    results['templates_skipped'].append(filename)
                    continue

                try:
                    template_content = self._generate_research_template(filename, client_domain, phase)
                    file_path.write_text(template_content, encoding='utf-8')
                    results['templates_created'].append(filename)

                except Exception as e:
                    results['errors'].append(f'Error creating {filename}: {str(e)}')

        return results

    def _generate_research_template(self, filename: str, client_domain: str, phase: int) -> str:
        """Generate research template content based on filename and phase."""

        templates = {
            'audience_personas.md': f"""# Audience Personas - {client_domain.replace('_', ' ').title()}

## Research Methodology
- **Data Sources:** [Survey, interviews, analytics, etc.]
- **Sample Size:** [Number of participants/data points]
- **Research Period:** [Timeframe]
- **Research Tools:** [Tools and platforms used]

## Primary Persona: [Persona Name]

### Demographics
- **Age Range:** [Age range]
- **Location:** [Geographic location]
- **Occupation:** [Job title/industry]
- **Income Level:** [Income range]
- **Education:** [Education level]

### Psychographics
- **Values:** [Core values and beliefs]
- **Goals:** [Primary goals and objectives]
- **Challenges:** [Main pain points and obstacles]
- **Motivations:** [What drives decision-making]

### Behavior Patterns
- **Content Consumption:** [When and how they consume content]
- **Device Preferences:** [Preferred devices and platforms]
- **Information Sources:** [Trusted information sources]
- **Decision-Making Process:** [How they make purchasing decisions]

### Content Preferences
- **Preferred Formats:** [Blog posts, videos, infographics, etc.]
- **Content Topics:** [Subjects of interest]
- **Communication Style:** [Preferred tone and approach]
- **Content Length:** [Preferred content length]

## Secondary Persona: [Persona Name]

[Repeat structure as above]

## User Journey Mapping
- **Awareness Stage:** [Touchpoints and content needs]
- **Consideration Stage:** [Evaluation criteria and information needs]
- **Decision Stage:** [Final decision factors]
- **Post-Purchase:** [Support and retention needs]

---
**Research Completed:** {datetime.now().strftime('%d %B %Y')}
**Next Review:** [Schedule follow-up research]
""",

            'market_research.md': f"""# Market Research - {client_domain.replace('_', ' ').title()}

## Market Overview
- **Industry:** [Industry classification]
- **Market Size:** [Total addressable market]
- **Growth Rate:** [Annual growth percentage]
- **Key Trends:** [Major market trends and drivers]

## Target Market Analysis
- **Market Segments:** [Primary and secondary segments]
- **Geographic Focus:** [Target regions/locations]
- **Market Maturity:** [Stage of market development]
- **Opportunity Size:** [Addressable market opportunity]

## Industry Trends
- **Emerging Trends:** [New developments and innovations]
- **Technology Impact:** [How technology is changing the industry]
- **Regulatory Changes:** [Relevant regulations and compliance]
- **Economic Factors:** [Economic influences on the market]

## Market Challenges and Opportunities
### Challenges
- [Challenge 1 and its impact]
- [Challenge 2 and its impact]
- [Challenge 3 and its impact]

### Opportunities
- [Opportunity 1 and potential]
- [Opportunity 2 and potential]
- [Opportunity 3 and potential]

## Customer Market Behavior
- **Buying Patterns:** [How customers make purchasing decisions]
- **Price Sensitivity:** [Price considerations and budgets]
- **Brand Loyalty:** [Customer retention patterns]
- **Seasonal Factors:** [Seasonal variations in demand]

## Recommendations
- **Market Entry Strategy:** [Recommended approach]
- **Positioning Strategy:** [How to position in market]
- **Priority Opportunities:** [High-value opportunities to pursue]

---
**Research Date:** {datetime.now().strftime('%d %B %Y')}
**Sources:** [Research sources and references]
""",

            'competitive_analysis.md': f"""# Competitive Analysis - {client_domain.replace('_', ' ').title()}

## Analysis Scope
- **Research Period:** {datetime.now().strftime('%B %Y')}
- **Analysis Method:** [Direct observation, tools used, etc.]
- **Competitors Analyzed:** [Number and selection criteria]

## Direct Competitors

### Competitor 1: [Company Name]
- **Website:** [URL]
- **Market Position:** [Market share and positioning]
- **Strengths:** [Key competitive advantages]
- **Weaknesses:** [Areas of vulnerability]
- **Content Strategy:** [Content approach and themes]
- **SEO Performance:** [Organic visibility and rankings]
- **Social Media Presence:** [Platform activity and engagement]
- **Pricing Strategy:** [Pricing model and positioning]

### Competitor 2: [Company Name]
[Repeat structure as above]

### Competitor 3: [Company Name]
[Repeat structure as above]

## Indirect Competitors
- **Alternative Solutions:** [Non-direct competitive options]
- **Substitute Products:** [Alternative approaches customers might take]
- **Market Disruptors:** [Emerging players or technologies]

## Competitive Landscape Analysis
- **Market Leaders:** [Top performers and their advantages]
- **Market Gaps:** [Underserved segments or needs]
- **Competitive Intensity:** [Level of competition assessment]
- **Barriers to Entry:** [Challenges for new market entrants]

## SWOT Analysis Comparison
### Our Strengths vs Competition
- [Unique advantage 1]
- [Unique advantage 2]
- [Unique advantage 3]

### Competitive Threats
- [Threat 1 and mitigation strategy]
- [Threat 2 and mitigation strategy]
- [Threat 3 and mitigation strategy]

## Content and Marketing Analysis
- **Content Themes:** [Common topics and approaches]
- **Content Gaps:** [Missing content opportunities]
- **SEO Opportunities:** [Keywords competitors are missing]
- **Social Media Insights:** [Platform strategies and performance]

## Strategic Recommendations
- **Differentiation Strategy:** [How to stand out from competition]
- **Market Positioning:** [Recommended competitive positioning]
- **Priority Actions:** [Immediate actions to gain advantage]

---
**Analysis Date:** {datetime.now().strftime('%d %B %Y')}
**Next Review:** [Schedule competitive review update]
""",

            'trending_topics_research.md': f"""# Trending Topics Research - {client_domain.replace('_', ' ').title()}

## Research Overview
- **Research Period:** {datetime.now().strftime('%B %Y')}
- **Industry Focus:** [Specific industry or market]
- **Research Tools:** [Google Trends, social listening, etc.]
- **Data Sources:** [Industry publications, social media, news]

## Current Hot Topics

### Topic 1: [Trending Topic Name]
- **Trend Score:** [1-100 trending intensity]
- **Search Volume:** [Monthly search volume]
- **Competition Level:** [Low/Medium/High]
- **Content Opportunities:** [Specific content ideas]
- **Timeline:** [Expected trend duration]

### Topic 2: [Trending Topic Name]
[Repeat structure as above]

### Topic 3: [Trending Topic Name]
[Repeat structure as above]

## Emerging Trends
- **Early Stage Trends:** [Topics gaining momentum]
- **Seasonal Trends:** [Time-sensitive opportunities]
- **Geographic Trends:** [Location-specific trends]
- **Demographic Trends:** [Age/group-specific interests]

## Industry-Specific Trends
- **Technology Trends:** [Tech developments impacting industry]
- **Regulatory Trends:** [Compliance and regulation changes]
- **Economic Trends:** [Market and economic influences]
- **Social Trends:** [Cultural and social shifts]

## Content Opportunity Analysis
### High-Priority Topics
1. [Topic with high opportunity score]
2. [Topic with medium competition]
3. [Topic with growing search volume]

### Content Format Trends
- **Video Content:** [Video topic opportunities]
- **Interactive Content:** [Polls, quizzes, calculators]
- **Long-form Content:** [In-depth guide opportunities]
- **Visual Content:** [Infographic and image opportunities]

## Seasonal Content Calendar
- **Q1 Trends:** [January-March opportunities]
- **Q2 Trends:** [April-June opportunities]
- **Q3 Trends:** [July-September opportunities]
- **Q4 Trends:** [October-December opportunities]

## Recommendations
- **Immediate Actions:** [Content to create now]
- **Medium-term Planning:** [3-6 month content pipeline]
- **Long-term Strategy:** [Annual content themes]

---
**Research Date:** {datetime.now().strftime('%d %B %Y')}
**Next Update:** [Schedule trend research refresh]
""",

            'content_gap_analysis.md': f"""# Content Gap Analysis - {client_domain.replace('_', ' ').title()}

## Analysis Overview
- **Analysis Date:** {datetime.now().strftime('%d %B %Y')}
- **Content Audit Scope:** [Website sections and content types reviewed]
- **Competitor Comparison:** [Competitors analyzed for gap identification]
- **User Journey Coverage:** [Journey stages analyzed]

## Current Content Inventory
### Existing Content Strengths
- [Strong content area 1]
- [Strong content area 2]
- [Strong content area 3]

### Content Performance Analysis
- **High-Performing Content:** [Top content by engagement/traffic]
- **Underperforming Content:** [Content needing improvement]
- **Content Frequency:** [Current publishing schedule analysis]

## Identified Content Gaps

### Topic Gaps
- **Missing Industry Topics:** [Important subjects not covered]
- **Competitor Content Advantages:** [Topics competitors cover better]
- **Trending Topic Gaps:** [Current trends not addressed]
- **Seasonal Content Gaps:** [Time-sensitive content missing]

### Format Gaps
- **Visual Content:** [Infographics, videos, images needed]
- **Interactive Content:** [Tools, calculators, quizzes missing]
- **Long-form Content:** [In-depth guides and resources needed]
- **Quick Reference Content:** [Checklists, templates, summaries]

### Audience Journey Gaps
- **Awareness Stage:** [Educational content missing]
- **Consideration Stage:** [Comparison and evaluation content gaps]
- **Decision Stage:** [Conversion-focused content needs]
- **Post-Purchase:** [Customer success and retention content]

## Keyword Content Gaps
- **High-Volume Keywords:** [Keywords without supporting content]
- **Long-tail Opportunities:** [Specific queries not addressed]
- **Local SEO Gaps:** [Location-based content missing]
- **Voice Search Gaps:** [Question-based content opportunities]

## Competitor Content Advantages
### Competitor 1: [Name]
- [Content advantage 1]
- [Content advantage 2]

### Competitor 2: [Name]
- [Content advantage 1]
- [Content advantage 2]

## Content Prioritization Matrix

### High Priority (Create First)
1. [Content gap with high impact/low effort]
2. [Content gap addressing major keyword opportunity]
3. [Content gap filling competitor advantage]

### Medium Priority
1. [Moderate impact content gaps]
2. [Seasonal content opportunities]
3. [Format diversification needs]

### Low Priority (Future Development)
1. [Nice-to-have content additions]
2. [Advanced topic coverage]
3. [Experimental content formats]

## Recommendations
- **Immediate Actions:** [Content to create within 30 days]
- **Short-term Goals:** [90-day content development plan]
- **Long-term Strategy:** [Annual content gap resolution plan]

---
**Analysis Completed:** {datetime.now().strftime('%d %B %Y')}
**Next Review:** [Schedule follow-up analysis]
""",

            'search_landscape_analysis.md': f"""# Search Landscape Analysis - {client_domain.replace('_', ' ').title()}

## Analysis Overview
- **Analysis Date:** {datetime.now().strftime('%d %B %Y')}
- **Search Market:** [Geographic and industry focus]
- **Analysis Tools:** [SEMrush, Ahrefs, Google Search Console, etc.]
- **Time Period:** [Data collection timeframe]

## Market Size Analysis
- **Total Search Volume:** [Monthly search volume for industry]
- **Seasonal Variations:** [Search volume fluctuations]
- **Geographic Distribution:** [Search volume by location]
- **Device Breakdown:** [Desktop vs mobile search patterns]

## Competition Landscape
### Competition Levels
- **High Competition Keywords:** [Difficult to rank keywords]
- **Medium Competition Keywords:** [Moderate difficulty keywords]
- **Low Competition Keywords:** [Opportunity keywords]
- **Zero Competition Keywords:** [Untapped opportunities]

### SERP Analysis
- **Featured Snippets:** [Opportunities for position zero]
- **Local Pack Opportunities:** [Local SEO potential]
- **Image Search Opportunities:** [Visual search potential]
- **Video Search Opportunities:** [YouTube and video SEO]

## Keyword Categories Analysis

### Informational Keywords
- **How-to Queries:** [Tutorial and guide opportunities]
- **What/Why Questions:** [Educational content needs]
- **Definition Searches:** [Glossary and explanation content]

### Commercial Keywords
- **Service-Related:** [Service page optimization opportunities]
- **Product Comparisons:** [Comparison content needs]
- **Reviews and Ratings:** [Reputation management opportunities]

### Navigational Keywords
- **Brand Searches:** [Brand awareness and protection]
- **Location Searches:** [Local SEO opportunities]
- **Contact Searches:** [Business information optimization]

### Transactional Keywords
- **Purchase Intent:** [High-conversion keyword opportunities]
- **Local Business:** [Near me and local service searches]
- **Emergency/Urgent:** [Immediate need keywords]

## Search Trends Analysis
- **Rising Keywords:** [Growing search terms]
- **Declining Keywords:** [Decreasing interest areas]
- **Stable Keywords:** [Consistent search volume terms]
- **Seasonal Patterns:** [Time-based search variations]

## Technical SEO Landscape
- **Site Speed Benchmarks:** [Industry loading time standards]
- **Mobile-First Requirements:** [Mobile optimization necessities]
- **Core Web Vitals:** [User experience metrics importance]
- **Schema Markup Opportunities:** [Structured data advantages]

## Local SEO Analysis
- **Local Search Volume:** [Location-based search potential]
- **Google My Business Opportunities:** [Local listing optimization]
- **Local Competition:** [Geographic competitor analysis]
- **Review Landscape:** [Reputation management needs]

## Content Format Preferences
- **Text Content:** [Traditional article performance]
- **Video Content:** [YouTube and embedded video potential]
- **Image Content:** [Visual search and Pinterest opportunities]
- **Audio Content:** [Podcast and voice search considerations]

## Recommendations

### Short-term SEO Opportunities
1. [High-impact, low-competition keyword targets]
2. [Technical SEO quick wins]
3. [Local SEO optimization priorities]

### Medium-term Strategy
1. [Content creation priorities based on search data]
2. [Competitive positioning improvements]
3. [Featured snippet targeting]

### Long-term SEO Planning
1. [Authority building through content depth]
2. [Market expansion through keyword growth]
3. [Emerging search technology preparation]

---
**Analysis Date:** {datetime.now().strftime('%d %B %Y')}
**Next Review:** [Schedule landscape analysis update]
""",

            'keyword_research.md': f"""# Keyword Research - {client_domain.replace('_', ' ').title()}

## Research Overview
- **Research Date:** {datetime.now().strftime('%d %B %Y')}
- **Target Market:** [Geographic and demographic focus]
- **Research Tools:** [SEMrush, Ahrefs, Google Keyword Planner, etc.]
- **Analysis Depth:** [Scope and methodology]

## Primary Keywords (High Priority)
| Keyword | Search Volume | Competition | Difficulty | Intent Type | Current Rank |
|---------|---------------|-------------|------------|-------------|--------------|
| [keyword 1] | [monthly volume] | [Low/Med/High] | [1-100] | [Commercial/Info] | [position] |
| [keyword 2] | [monthly volume] | [Low/Med/High] | [1-100] | [Commercial/Info] | [position] |
| [keyword 3] | [monthly volume] | [Low/Med/High] | [1-100] | [Commercial/Info] | [position] |

## Secondary Keywords (Medium Priority)
| Keyword | Search Volume | Competition | Difficulty | Intent Type | Opportunity |
|---------|---------------|-------------|------------|-------------|-------------|
| [keyword 4] | [monthly volume] | [Low/Med/High] | [1-100] | [Informational] | [High/Med/Low] |
| [keyword 5] | [monthly volume] | [Low/Med/High] | [1-100] | [Informational] | [High/Med/Low] |
| [keyword 6] | [monthly volume] | [Low/Med/High] | [1-100] | [Informational] | [High/Med/Low] |

## Long-tail Keywords (Quick Wins)
- [long-tail keyword 1] - [search volume] - [intent]
- [long-tail keyword 2] - [search volume] - [intent]
- [long-tail keyword 3] - [search volume] - [intent]

## Keyword Categories

### Service-Based Keywords
- **Primary Services:** [main service keywords]
- **Service Variations:** [alternative service terms]
- **Service + Location:** [geo-targeted service terms]
- **Service + Modifiers:** [quality, best, top service terms]

### Problem-Solution Keywords
- **Problem Keywords:** [pain point and challenge terms]
- **Solution Keywords:** [how-to and resolution terms]
- **Question Keywords:** [what, why, how questions]
- **Comparison Keywords:** [vs, versus, compare terms]

### Industry-Specific Keywords
- **Technical Terms:** [industry jargon and terminology]
- **Process Keywords:** [methodology and approach terms]
- **Tool Keywords:** [software, equipment, resource terms]
- **Certification Keywords:** [qualification and credential terms]

## Local SEO Keywords
- **[City] + Service:** [location-specific service terms]
- **Near Me Keywords:** [proximity-based search terms]
- **Area-Specific:** [neighborhood and region terms]
- **Local Modifiers:** [local business qualifying terms]

## Seasonal Keywords
- **Q1 Keywords:** [January-March seasonal terms]
- **Q2 Keywords:** [April-June seasonal terms]
- **Q3 Keywords:** [July-September seasonal terms]
- **Q4 Keywords:** [October-December seasonal terms]

## Competitor Keyword Analysis
### Competitor 1: [Name]
- **Top Ranking Keywords:** [their best performing terms]
- **Keyword Gaps:** [terms they rank for that we don't]
- **Opportunity Keywords:** [where we can compete]

### Competitor 2: [Name]
- **Top Ranking Keywords:** [their best performing terms]
- **Keyword Gaps:** [terms they rank for that we don't]
- **Opportunity Keywords:** [where we can compete]

## Keyword Mapping Strategy
### Homepage
- **Primary Keywords:** [main brand and service terms]
- **Supporting Keywords:** [related and LSI keywords]

### Service Pages
- **Service 1 Page:** [specific service keywords]
- **Service 2 Page:** [specific service keywords]
- **Service 3 Page:** [specific service keywords]

### Blog/Content Pages
- **Informational Content:** [educational and how-to keywords]
- **Industry Insights:** [trend and analysis keywords]
- **Problem-Solution Content:** [pain point addressing keywords]

## Implementation Priority
### Phase 1 (Months 1-2)
- [High-impact, low-competition keywords]
- [Branded keywords and variations]
- [Local SEO keywords]

### Phase 2 (Months 3-4)
- [Medium-competition service keywords]
- [Long-tail informational keywords]
- [Industry-specific terms]

### Phase 3 (Months 5-6)
- [Higher competition commercial keywords]
- [Competitive gap keywords]
- [Advanced topic keywords]

## Success Metrics
- **Ranking Improvements:** [Target positions for priority keywords]
- **Traffic Increases:** [Expected organic traffic growth]
- **Conversion Tracking:** [Keyword-to-conversion attribution]
- **SERP Features:** [Featured snippet and local pack targets]

---
**Research Completed:** {datetime.now().strftime('%d %B %Y')}
**Next Review:** [Schedule keyword research update]
""",

            'search_intent_analysis.md': f"""# Search Intent Analysis - {client_domain.replace('_', ' ').title()}

## Analysis Overview
- **Analysis Date:** {datetime.now().strftime('%d %B %Y')}
- **Scope:** [Keywords and search queries analyzed]
- **Methodology:** [SERP analysis, user behavior data, etc.]
- **Intent Categories:** [Informational, Commercial, Transactional, Navigational]

## Search Intent Classification

### Informational Intent Keywords
**User Goal:** Learning and understanding

#### High Volume Informational
| Keyword | Search Volume | Current SERP Type | Content Opportunity |
|---------|---------------|-------------------|-------------------|
| [how to keyword] | [volume] | [Articles/Videos] | [In-depth guide] |
| [what is keyword] | [volume] | [Definition pages] | [Comprehensive explanation] |
| [why keyword] | [volume] | [Educational content] | [Expert analysis] |

#### Content Format Preferences
- **Articles:** [Preferred length and structure]
- **Videos:** [Tutorial and explanation videos]
- **Infographics:** [Visual explanation content]
- **FAQs:** [Question and answer format]

### Commercial Investigation Intent
**User Goal:** Researching before purchase

#### Commercial Keywords
| Keyword | Search Volume | SERP Features | Content Strategy |
|---------|---------------|---------------|------------------|
| [service comparison] | [volume] | [Comparison sites] | [Detailed comparison guide] |
| [best service] | [volume] | [Review sites] | [Authority review content] |
| [service reviews] | [volume] | [Review platforms] | [Testimonial optimization] |

#### Content Approach
- **Comparison Content:** [Feature comparisons and evaluations]
- **Review Content:** [Honest assessments and testimonials]
- **Case Studies:** [Success stories and results]
- **Buying Guides:** [Decision-making support content]

### Transactional Intent Keywords
**User Goal:** Ready to purchase or take action

#### High-Intent Commercial
| Keyword | Search Volume | Conversion Potential | Page Optimization |
|---------|---------------|---------------------|-------------------|
| [service near me] | [volume] | [High] | [Local landing page] |
| [hire service] | [volume] | [High] | [Service booking page] |
| [service cost] | [volume] | [Medium] | [Pricing information] |

#### Conversion Optimization
- **Clear CTAs:** [Action-oriented calls-to-action]
- **Trust Signals:** [Testimonials, certifications, guarantees]
- **Contact Information:** [Easy access to contact details]
- **Urgency Elements:** [Limited time offers, availability]

### Navigational Intent Keywords
**User Goal:** Finding specific brand or website

#### Brand Navigation
| Keyword | Search Volume | Brand Protection | Optimization Strategy |
|---------|---------------|------------------|----------------------|
| [brand name] | [volume] | [High priority] | [Homepage optimization] |
| [brand + service] | [volume] | [Medium priority] | [Service page optimization] |
| [brand + location] | [volume] | [Medium priority] | [Local page optimization] |

## User Journey Mapping

### Awareness Stage (Informational Intent)
- **Typical Queries:** [Problem identification searches]
- **Content Needs:** [Educational and awareness content]
- **User Behavior:** [Research and information gathering]
- **Content Strategy:** [Helpful, non-promotional content]

### Consideration Stage (Commercial Investigation)
- **Typical Queries:** [Solution comparison searches]
- **Content Needs:** [Comparison and evaluation content]
- **User Behavior:** [Vendor research and evaluation]
- **Content Strategy:** [Authority-building and trust content]

### Decision Stage (Transactional Intent)
- **Typical Queries:** [Purchase and action-ready searches]
- **Content Needs:** [Clear action paths and information]
- **User Behavior:** [Ready to convert or contact]
- **Content Strategy:** [Conversion-optimized landing pages]

### Post-Purchase (Customer Success)
- **Typical Queries:** [Support and optimization searches]
- **Content Needs:** [Help documentation and advanced tips]
- **User Behavior:** [Seeking to maximize value]
- **Content Strategy:** [Customer success and retention content]

## SERP Analysis by Intent

### Informational SERP Features
- **Featured Snippets:** [Opportunity for position zero]
- **People Also Ask:** [Related question opportunities]
- **Knowledge Panels:** [Entity optimization opportunities]
- **Video Results:** [YouTube optimization potential]

### Commercial SERP Features
- **Shopping Results:** [E-commerce optimization]
- **Local Pack:** [Local SEO opportunities]
- **Review Stars:** [Schema markup for reviews]
- **Site Links:** [Internal page highlighting]

### Transactional SERP Features
- **Google Ads:** [Paid search competition analysis]
- **Local Services Ads:** [Local advertising opportunities]
- **Maps Integration:** [Location-based optimization]
- **Contact Information:** [Business profile optimization]

## Content Strategy by Intent

### Informational Content Strategy
- **Blog Articles:** [Educational and helpful content]
- **Resource Pages:** [Comprehensive information hubs]
- **Video Content:** [Tutorial and explanation videos]
- **Tools/Calculators:** [Interactive helpful resources]

### Commercial Content Strategy
- **Service Pages:** [Detailed service descriptions]
- **Case Studies:** [Success story documentation]
- **Testimonials:** [Customer experience content]
- **Comparison Pages:** [Competitive positioning content]

### Transactional Content Strategy
- **Landing Pages:** [Conversion-focused page design]
- **Contact Pages:** [Easy contact and conversion paths]
- **Pricing Pages:** [Clear pricing and value proposition]
- **Local Pages:** [Location-specific service information]

## Recommendations

### Content Creation Priorities
1. [High-intent commercial keywords requiring new content]
2. [Informational gaps with high search volume]
3. [Navigational brand protection content]

### Optimization Opportunities
1. [Existing pages not matching search intent]
2. [SERP feature capture opportunities]
3. [User journey gap improvements]

### Technical Implementation
1. [Schema markup for enhanced SERP display]
2. [Page speed optimization for commercial pages]
3. [Mobile optimization for local searches]

---
**Analysis Completed:** {datetime.now().strftime('%d %B %Y')}
**Next Review:** [Schedule intent analysis update]
""",

            'keyword_gap_analysis.md': f"""# Keyword Gap Analysis - {client_domain.replace('_', ' ').title()}

## Analysis Overview
- **Analysis Date:** {datetime.now().strftime('%d %B %Y')}
- **Competitors Analyzed:** [List of competitor websites]
- **Analysis Tools:** [SEMrush, Ahrefs, etc.]
- **Gap Categories:** [Missing opportunities, underperforming keywords]

## Competitive Keyword Gaps

### Competitor 1: [Competitor Name]
**Keywords they rank for that we don't:**

| Keyword | Their Position | Search Volume | Difficulty | Opportunity Score |
|---------|----------------|---------------|------------|-------------------|
| [keyword 1] | [position] | [volume] | [difficulty] | [High/Med/Low] |
| [keyword 2] | [position] | [volume] | [difficulty] | [High/Med/Low] |
| [keyword 3] | [position] | [volume] | [difficulty] | [High/Med/Low] |

### Competitor 2: [Competitor Name]
**Keywords they rank for that we don't:**

| Keyword | Their Position | Search Volume | Difficulty | Opportunity Score |
|---------|----------------|---------------|------------|-------------------|
| [keyword 4] | [position] | [volume] | [difficulty] | [High/Med/Low] |
| [keyword 5] | [position] | [volume] | [difficulty] | [High/Med/Low] |
| [keyword 6] | [position] | [volume] | [difficulty] | [High/Med/Low] |

## Content Gap Analysis

### Missing Topic Categories
- **Industry Topics:** [Subject areas not covered]
- **Service Variations:** [Service-related terms missing]
- **Local Keywords:** [Geographic terms not targeted]
- **Question Keywords:** [FAQ-style queries not addressed]

### Underperforming Keywords
**Keywords we rank poorly for (positions 11-50):**

| Keyword | Current Position | Search Volume | Improvement Potential |
|---------|------------------|---------------|----------------------|
| [keyword] | [position] | [volume] | [estimated traffic gain] |
| [keyword] | [position] | [volume] | [estimated traffic gain] |
| [keyword] | [position] | [volume] | [estimated traffic gain] |

## Seasonal Keyword Gaps
- **Q1 Opportunities:** [Missing seasonal terms]
- **Q2 Opportunities:** [Missing seasonal terms]
- **Q3 Opportunities:** [Missing seasonal terms]
- **Q4 Opportunities:** [Missing seasonal terms]

## Long-tail Keyword Opportunities
### Untapped Long-tail Keywords
- [Long-tail keyword 1] - [search volume] - [competition level]
- [Long-tail keyword 2] - [search volume] - [competition level]
- [Long-tail keyword 3] - [search volume] - [competition level]

### Question-based Keywords
- [Question keyword 1] - [search volume] - [content opportunity]
- [Question keyword 2] - [search volume] - [content opportunity]
- [Question keyword 3] - [search volume] - [content opportunity]

## Local SEO Gaps
### Missing Local Keywords
- **[City] + Service combinations not targeted**
- **Neighborhood-specific keywords missing**
- **Local modifier gaps (near me, local, etc.)**

### Geographic Expansion Opportunities
- **Nearby Cities:** [Expansion location opportunities]
- **Service Areas:** [Geographic coverage gaps]
- **Regional Terms:** [Area-specific terminology]

## SERP Feature Opportunities
### Featured Snippet Gaps
- [Keywords where competitors have featured snippets]
- [Question keywords suitable for featured snippets]
- [Definition keywords with snippet potential]

### Local Pack Opportunities
- [Local keywords where we could appear]
- [Service + location combinations]
- [Google My Business optimization opportunities]

## Intent-based Keyword Gaps

### Informational Intent Gaps
- **How-to Keywords:** [Tutorial opportunities]
- **What/Why Keywords:** [Educational content gaps]
- **Problem Keywords:** [Pain point addressing opportunities]

### Commercial Intent Gaps
- **Comparison Keywords:** [Competitive comparison opportunities]
- **Review Keywords:** [Reputation content gaps]
- **Best/Top Keywords:** [Authority content opportunities]

### Transactional Intent Gaps
- **Service + Action Keywords:** [Conversion keyword opportunities]
- **Pricing Keywords:** [Cost-related search opportunities]
- **Contact Keywords:** [Lead generation keyword gaps]

## Priority Gap Analysis

### High Priority Gaps (Address First)
1. **[Gap Category]:** [Specific opportunities with high impact]
   - Estimated monthly traffic: [traffic potential]
   - Implementation difficulty: [Low/Medium/High]
   - Timeline: [1-3 months]

2. **[Gap Category]:** [Specific opportunities with high impact]
   - Estimated monthly traffic: [traffic potential]
   - Implementation difficulty: [Low/Medium/High]
   - Timeline: [1-3 months]

### Medium Priority Gaps (3-6 months)
1. **[Gap Category]:** [Medium impact opportunities]
2. **[Gap Category]:** [Medium impact opportunities]

### Low Priority Gaps (6+ months)
1. **[Gap Category]:** [Long-term opportunities]
2. **[Gap Category]:** [Long-term opportunities]

## Implementation Strategy

### Content Creation Needs
- **New Pages Required:** [Pages needed to target gap keywords]
- **Existing Page Optimization:** [Pages needing keyword expansion]
- **Content Format Requirements:** [Blog posts, guides, FAQs needed]

### Technical SEO Requirements
- **URL Structure:** [New page URL planning]
- **Internal Linking:** [Link structure to support new keywords]
- **Schema Markup:** [Structured data for SERP features]

### Resource Requirements
- **Content Creation Time:** [Estimated hours/resources needed]
- **SEO Optimization Time:** [Technical implementation time]
- **Expected Timeline:** [Realistic implementation schedule]

## Success Metrics
- **Ranking Improvements:** [Target positions for gap keywords]
- **Traffic Projections:** [Expected organic traffic increase]
- **Competitive Positioning:** [Market share improvement goals]

---
**Analysis Date:** {datetime.now().strftime('%d %B %Y')}
**Next Review:** [Schedule gap analysis update]
""",

            'content_briefs.md': f"""# Content Briefs - {client_domain.replace('_', ' ').title()}

## Content Brief Overview
- **Project:** {client_domain.replace('_', ' ').title()}
- **Brief Creation Date:** {datetime.now().strftime('%d %B %Y')}
- **Content Strategy Phase:** Phase 4 - Content Planning & Briefs
- **Target Audience:** [Primary and secondary personas]

## Homepage Content Brief

### Content Objective
- **Primary Goal:** Clear value proposition and user guidance
- **Secondary Goals:** Brand credibility, service introduction, conversion
- **Target Audience:** [Primary persona + secondary personas]

### Key Messages
1. **Primary Value Proposition:** [Main benefit statement]
2. **Unique Differentiators:** [What sets apart from competitors]
3. **Trust and Credibility:** [Expertise and reliability indicators]
4. **Clear Next Steps:** [Primary call-to-action]

### Content Structure
- **Hero Section:** [Compelling headline + value proposition + CTA]
- **Services Overview:** [Brief service introductions with benefits]
- **Social Proof:** [Testimonials, client logos, statistics]
- **About Preview:** [Brief company introduction and expertise]
- **Contact/CTA Section:** [Clear conversion path]

### SEO Requirements
- **Primary Keywords:** [Main brand and service keywords]
- **Secondary Keywords:** [Supporting and related terms]
- **Meta Title:** [50-60 characters including primary keyword]
- **Meta Description:** [150-160 characters, compelling and informative]

### Technical Specifications
- **Word Count:** 400-600 words
- **Reading Level:** Professional (Year 10-12)
- **Tone:** Professional, confident, approachable
- **Call-to-Actions:** [Primary and secondary CTA placement]

## Service Page Content Briefs

### Service 1: [Service Name]

#### Content Objective
- **Primary Goal:** [Specific service promotion and lead generation]
- **Target Keywords:** [Service-specific keywords]
- **User Intent:** [Commercial/transactional]

#### Content Structure
1. **Service Overview:** [What the service is and who it's for]
2. **Benefits and Outcomes:** [Specific results clients can expect]
3. **Process/Methodology:** [How the service is delivered]
4. **Case Studies/Examples:** [Success stories and proof]
5. **Pricing/Investment:** [Cost information or contact for quote]
6. **Next Steps/CTA:** [Clear path to engagement]

#### Key Messages
- **Problem Solution:** [How this service solves client problems]
- **Unique Approach:** [What makes this service different]
- **Results Focus:** [Outcomes and benefits emphasis]

#### SEO Optimization
- **Primary Keyword:** [Main service keyword]
- **Secondary Keywords:** [Related service terms]
- **Internal Links:** [Links to related services and resources]
- **Schema Markup:** [Service schema implementation]

#### Content Specifications
- **Word Count:** 800-1200 words
- **Headings:** H1, H2, H3 structure for scanability
- **Images:** [Service-related visuals and process diagrams]
- **CTAs:** [Multiple conversion opportunities]

### Service 2: [Service Name]
[Repeat structure as above]

### Service 3: [Service Name]
[Repeat structure as above]

## Blog Content Briefs

### Blog Article 1: [Article Title]

#### Content Objective
- **Primary Goal:** [Educational content for awareness stage]
- **Target Audience:** [Specific persona]
- **User Intent:** Informational
- **Journey Stage:** Awareness

#### Content Outline
1. **Introduction:** [Problem identification and hook]
2. **Main Sections:** [3-4 key points with subheadings]
   - **Section 1:** [Topic and key points]
   - **Section 2:** [Topic and key points]
   - **Section 3:** [Topic and key points]
3. **Conclusion:** [Summary and clear CTA]

#### SEO Strategy
- **Primary Keyword:** [Main informational keyword]
- **Secondary Keywords:** [Related terms and variations]
- **Featured Snippet Opportunity:** [Question format or list structure]
- **Internal Linking:** [Links to related articles and service pages]

#### Content Requirements
- **Word Count:** 1000-1500 words
- **Tone:** Helpful, educational, authoritative
- **Citations:** [2-3 credible sources required]
- **Visuals:** [Relevant images, charts, or infographics]

### Blog Article 2: [Article Title]
[Repeat structure as above]

## Landing Page Content Briefs

### Landing Page 1: [Campaign/Topic]

#### Campaign Objective
- **Traffic Source:** [Paid ads, email, social media]
- **Conversion Goal:** [Lead generation, consultation booking]
- **Target Audience:** [Specific persona segment]

#### Content Strategy
- **Headline:** [Attention-grabbing, benefit-focused]
- **Value Proposition:** [Clear benefit statement]
- **Social Proof:** [Testimonials, reviews, case studies]
- **Conversion Form:** [Lead capture with minimal fields]
- **Risk Reversal:** [Guarantees, free consultation offer]

#### Technical Requirements
- **Page Speed:** [Optimized for fast loading]
- **Mobile Optimization:** [Responsive design priority]
- **A/B Testing Elements:** [Headlines, CTAs, forms]
- **Analytics Tracking:** [Conversion and behavior tracking]

## About Page Content Brief

### Content Objective
- **Primary Goal:** Build trust and credibility
- **Secondary Goals:** Humanize brand, showcase expertise
- **User Intent:** Informational/trust-building

### Content Elements
- **Company Story:** [Founding story and mission]
- **Team Introduction:** [Key personnel and expertise]
- **Values and Approach:** [What makes the company unique]
- **Credentials:** [Certifications, awards, recognition]
- **Client Success:** [Brief testimonials or results]

### Trust Building Elements
- **Professional Photography:** [Team and office photos]
- **Certifications:** [Industry credentials and affiliations]
- **Years in Business:** [Experience and stability indicators]
- **Community Involvement:** [Local engagement and giving back]

## Contact Page Content Brief

### Content Objective
- **Primary Goal:** Make contact as easy as possible
- **Secondary Goals:** Reinforce value proposition, address concerns

### Essential Elements
- **Multiple Contact Methods:** [Phone, email, form, address]
- **Response Time Expectations:** [When clients will hear back]
- **Office Hours:** [Availability and time zone]
- **Location Information:** [Address, directions, parking]
- **Pre-Contact Information:** [What to prepare, what to expect]

### Conversion Optimization
- **Clear Forms:** [Simple, user-friendly contact forms]
- **Trust Signals:** [Security badges, privacy assurance]
- **Value Reinforcement:** [Why choose us reminders]
- **Next Steps:** [What happens after contact]

## Content Quality Standards

### Writing Guidelines
- **Language:** Australian English (British spelling)
- **Tone:** Professional, approachable, helpful
- **Sentence Length:** Maximum 25 words for clarity
- **Paragraph Length:** 3-4 sentences maximum
- **Voice:** Active voice preferred

### SEO Standards
- **Keyword Density:** Natural integration, no stuffing
- **Header Structure:** Proper H1, H2, H3 hierarchy
- **Internal Links:** 2-4 relevant links per 1000 words
- **Meta Data:** Optimized titles and descriptions
- **Schema Markup:** Appropriate structured data

### Content Review Process
1. **Draft Creation:** [Writer creates initial content]
2. **SEO Review:** [SEO specialist optimizes]
3. **Quality Review:** [Editor reviews for quality and compliance]
4. **Client Review:** [Client approval process]
5. **Final Optimization:** [Final tweaks before publishing]

---
**Briefs Created:** {datetime.now().strftime('%d %B %Y')}
**Project Manager:** [Assign team member]
**Content Team:** [List content creators]
""",

            'ai_optimization_guide.md': f"""# AI Optimization Guide - {client_domain.replace('_', ' ').title()}

## AI Optimization Overview
- **Guide Creation Date:** {datetime.now().strftime('%d %B %Y')}
- **AI Systems Targeted:** [Google AI, ChatGPT, Claude, Bing AI, etc.]
- **Optimization Focus:** [Search visibility, voice search, AI recommendations]
- **Content Strategy Integration:** Phase 4 - AI-Ready Content Structure

## AI Search Optimization

### Google AI and SGE (Search Generative Experience)
**Optimization Strategy for AI-powered search results**

#### Content Structure for AI Visibility
- **Clear Headings:** [Descriptive H2 and H3 headings for easy parsing]
- **FAQ Format:** [Question-answer structure for common queries]
- **Definition Clarity:** [Clear explanations of industry terms]
- **Step-by-Step Guides:** [Numbered processes and methodologies]

#### Schema Markup Implementation
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "{client_domain.replace('_', ' ').title()}",
  "description": "[Business description]",
  "url": "https://{client_domain.replace('_', '.')}",
  "sameAs": [
    "[social media profiles]"
  ]
}
```

#### Featured Snippet Optimization
- **Answer Boxes:** [Direct answers to common questions]
- **List Snippets:** [Bulleted processes and benefits]
- **Table Snippets:** [Comparison data and pricing]
- **Paragraph Snippets:** [Concise definitions and explanations]

### Voice Search Optimization
**Preparing content for voice assistants and conversational AI**

#### Natural Language Patterns
- **Conversational Keywords:** [How people actually speak]
- **Question Phrases:** [Who, what, where, when, why, how]
- **Local Voice Queries:** [Near me, closest, local variations]
- **Long-tail Conversational:** [Full sentence queries]

#### Voice Search Content Structure
- **Direct Answers:** [Immediate response to queries]
- **Context Setting:** [Background information for clarity]
- **Follow-up Information:** [Related details and next steps]
- **Action-Oriented:** [Clear instructions and contact information]

### Chatbot and AI Assistant Optimization
**Ensuring content is AI-assistant friendly**

#### Content Formatting for AI Training
- **Consistent Terminology:** [Standardized language throughout]
- **Clear Hierarchies:** [Logical information organization]
- **Comprehensive Coverage:** [Complete information on topics]
- **Factual Accuracy:** [Verified information and statistics]

#### AI-Friendly Content Elements
- **Business Information:** [Consistent NAP (Name, Address, Phone)]
- **Service Descriptions:** [Clear, comprehensive service explanations]
- **FAQ Sections:** [Anticipate common customer questions]
- **Contact Information:** [Multiple ways to reach business]

## Structured Data Implementation

### Essential Schema Types
#### Organization Schema
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "{client_domain.replace('_', ' ').title()}",
  "alternateName": "[Business alternative names]",
  "url": "https://{client_domain.replace('_', '.')}",
  "logo": "[Logo URL]",
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "[Phone number]",
    "contactType": "customer service"
  }
}
```

#### Service Schema
```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "[Service Name]",
  "description": "[Service Description]",
  "provider": {
    "@type": "Organization",
    "name": "{client_domain.replace('_', ' ').title()}"
  },
  "areaServed": "[Geographic area]",
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "[Service category]",
    "itemListElement": [
      {
        "@type": "Offer",
        "itemOffered": {
          "@type": "Service",
          "name": "[Specific service]"
        }
      }
    ]
  }
}
```

#### FAQ Schema
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "[Question text]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[Answer text]"
      }
    }
  ]
}
```

### Local Business Schema
```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "{client_domain.replace('_', ' ').title()}",
  "image": "[Business image URL]",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[Street address]",
    "addressLocality": "[City]",
    "addressRegion": "[State]",
    "postalCode": "[Postcode]",
    "addressCountry": "AU"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "[Latitude]",
    "longitude": "[Longitude]"
  },
  "telephone": "[Phone number]",
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "09:00",
      "closes": "17:00"
    }
  ]
}
```

## Content Optimization for AI Systems

### Content Structure Best Practices
#### Information Architecture
- **Logical Hierarchy:** [Clear content organization]
- **Topic Clustering:** [Related content grouping]
- **Internal Linking:** [Contextual connections between pages]
- **Breadcrumb Navigation:** [Clear site structure indicators]

#### Content Formatting
- **Scannable Content:** [Subheadings, bullet points, short paragraphs]
- **Key Information Highlighting:** [Bold important facts and figures]
- **Summary Sections:** [Key takeaways and conclusions]
- **Table of Contents:** [For long-form content]

### Entity Optimization
**Helping AI systems understand your business entities**

#### Business Entity Signals
- **Consistent Branding:** [Name, description, messaging alignment]
- **Industry Classification:** [Clear category and service definitions]
- **Geographic Signals:** [Location and service area clarity]
- **Authority Indicators:** [Expertise, credentials, testimonials]

#### Topic Entity Development
- **Subject Matter Expertise:** [Deep content on core topics]
- **Comprehensive Coverage:** [Complete information on services]
- **Related Topic Connections:** [Links between related concepts]
- **Authority Building:** [Citations, references, expert quotes]

## Voice Search and Conversational AI

### Query Pattern Optimization
#### Common Voice Search Patterns
- **Question Queries:** [How, what, where, when, why questions]
- **Command Queries:** [Find, get, book, call commands]
- **Comparison Queries:** [Best, versus, compare requests]
- **Local Queries:** [Near me, closest, local variations]

#### Content for Voice Responses
- **Concise Answers:** [Direct responses under 30 words]
- **Context Provision:** [Background information after direct answer]
- **Natural Language:** [Conversational tone and phrasing]
- **Action Orientation:** [Clear next steps for users]

### Local Voice Search Optimization
- **Location Keywords:** [City, neighbourhood, region mentions]
- **Service + Location:** [Service combined with geographic terms]
- **Landmark References:** [Known local landmarks and directions]
- **Hours and Availability:** [When services are available]

## AI Content Quality Factors

### Content Depth and Authority
- **Comprehensive Coverage:** [Complete treatment of topics]
- **Original Research:** [Unique insights and data]
- **Expert Quotes:** [Industry authority contributions]
- **Source Citations:** [Credible reference linking]

### User Experience Signals
- **Page Speed:** [Fast loading for all devices]
- **Mobile Optimization:** [Responsive design and usability]
- **Core Web Vitals:** [Loading, interactivity, visual stability]
- **Accessibility:** [Inclusive design and navigation]

### Content Freshness and Updates
- **Regular Updates:** [Content refresh schedule]
- **Date Indicators:** [Publication and update dates]
- **Trending Topics:** [Current industry developments]
- **Seasonal Relevance:** [Time-appropriate content]

## Implementation Roadmap

### Phase 1: Foundation (Month 1)
- [ ] Implement basic schema markup
- [ ] Optimize existing content for FAQ format
- [ ] Create voice search keyword list
- [ ] Audit current content for AI readiness

### Phase 2: Enhancement (Month 2)
- [ ] Develop comprehensive FAQ pages
- [ ] Implement advanced schema types
- [ ] Optimize for featured snippets
- [ ] Create conversational content formats

### Phase 3: Advanced Optimization (Month 3)
- [ ] Develop entity optimization strategy
- [ ] Create topic cluster content
- [ ] Implement voice search landing pages
- [ ] Develop AI-specific content templates

### Phase 4: Monitoring and Refinement (Month 4+)
- [ ] Track AI search visibility
- [ ] Monitor voice search performance
- [ ] Analyze chatbot interaction data
- [ ] Refine content based on AI feedback

## Success Metrics

### AI Visibility Metrics
- **Featured Snippet Captures:** [Number of position zero rankings]
- **Voice Search Rankings:** [Position for voice queries]
- **AI Mention Frequency:** [Citations in AI responses]
- **Schema Rich Results:** [Enhanced SERP appearances]

### Performance Indicators
- **Organic Traffic Growth:** [AI-driven search traffic]
- **Query Diversity:** [Range of AI-captured searches]
- **Conversion from AI Traffic:** [AI source conversion rates]
- **Brand Entity Recognition:** [AI system brand awareness]

---
**Optimization Guide Created:** {datetime.now().strftime('%d %B %Y')}
**Next Review:** [Schedule AI optimization update]
**Implementation Timeline:** [12-week rollout plan]
""",

            'content_calendar.md': f"""# Content Calendar - {client_domain.replace('_', ' ').title()}

## Calendar Overview
- **Planning Period:** {datetime.now().strftime('%B %Y')} - {(datetime.now().replace(month=datetime.now().month+6) if datetime.now().month <= 6 else datetime.now().replace(year=datetime.now().year+1, month=datetime.now().month-6)).strftime('%B %Y')}
- **Content Strategy:** Phase 4 - Content Planning & Publishing
- **Publishing Frequency:** [Weekly/Bi-weekly schedule]
- **Content Distribution:** 40% Educational, 25% Service-focused, 20% Industry insights, 15% Brand storytelling

## Monthly Content Themes

### Month 1: {datetime.now().strftime('%B %Y')} - Foundation Building
**Theme:** Establishing expertise and trust
**Focus:** Educational content and service introduction

#### Week 1
- **Blog Post:** "Ultimate Guide to [Industry Topic]"
  - **Keywords:** [Primary keyword, secondary keywords]
  - **Intent:** Informational
  - **Word Count:** 1500-2000 words
  - **CTA:** Download comprehensive checklist

- **Social Media:** Blog promotion + industry tips
- **Email Newsletter:** Welcome series part 1

#### Week 2
- **Service Page Update:** [Primary Service] optimization
  - **Keywords:** [Service keywords]
  - **Intent:** Commercial
  - **Updates:** Enhanced descriptions, testimonials, pricing

- **Social Media:** Service highlights + client testimonials
- **Email Newsletter:** Welcome series part 2

#### Week 3
- **Blog Post:** "Common [Industry] Mistakes and How to Avoid Them"
  - **Keywords:** [Problem-solving keywords]
  - **Intent:** Informational
  - **Word Count:** 1200-1500 words
  - **CTA:** Free consultation offer

- **Social Media:** Mistake prevention tips
- **Email Newsletter:** Educational content series

#### Week 4
- **Case Study:** "[Client Success Story]"
  - **Keywords:** [Results keywords]
  - **Intent:** Commercial investigation
  - **Word Count:** 1000-1200 words
  - **CTA:** View more case studies

- **Social Media:** Success story highlights
- **Email Newsletter:** Case study promotion

### Month 2: {(datetime.now().replace(month=datetime.now().month+1) if datetime.now().month < 12 else datetime.now().replace(year=datetime.now().year+1, month=1)).strftime('%B %Y')} - Authority Building
**Theme:** Industry expertise and thought leadership
**Focus:** Advanced topics and industry insights

#### Week 1
- **Blog Post:** "Industry Trends for {datetime.now().year + 1}: What to Expect"
  - **Keywords:** [Trend keywords]
  - **Intent:** Informational
  - **Word Count:** 1800-2200 words
  - **CTA:** Subscribe to trend updates

#### Week 2
- **How-to Guide:** "Step-by-Step: [Complex Process]"
  - **Keywords:** [How-to keywords]
  - **Intent:** Informational
  - **Word Count:** 2000-2500 words
  - **CTA:** Book implementation consultation

#### Week 3
- **Industry Analysis:** "[Industry] Market Analysis {datetime.now().year}"
  - **Keywords:** [Analysis keywords]
  - **Intent:** Informational
  - **Word Count:** 1600-2000 words
  - **CTA:** Download full report

#### Week 4
- **Service Spotlight:** "[Secondary Service] Deep Dive"
  - **Keywords:** [Service keywords]
  - **Intent:** Commercial
  - **Word Count:** 1200-1500 words
  - **CTA:** Service consultation booking

### Month 3: {(datetime.now().replace(month=datetime.now().month+2) if datetime.now().month <= 10 else datetime.now().replace(year=datetime.now().year+1, month=datetime.now().month-10)).strftime('%B %Y')} - Engagement & Conversion
**Theme:** Interactive content and conversion optimization
**Focus:** Tools, calculators, and conversion-focused content

#### Week 1
- **Interactive Tool:** "[Industry] Calculator/Assessment"
  - **Keywords:** [Tool keywords]
  - **Intent:** Commercial investigation
  - **Features:** Results email, consultation offer
  - **CTA:** Book strategy session

#### Week 2
- **Comparison Guide:** "[Service] vs [Alternative]: Complete Comparison"
  - **Keywords:** [Comparison keywords]
  - **Intent:** Commercial investigation
  - **Word Count:** 1500-1800 words
  - **CTA:** Free consultation to discuss options

#### Week 3
- **FAQ Roundup:** "Most Asked Questions About [Industry Topic]"
  - **Keywords:** [Question keywords]
  - **Intent:** Informational/Commercial
  - **Word Count:** 1300-1600 words
  - **CTA:** Ask your question directly

#### Week 4
- **Success Metrics:** "How to Measure [Industry] Success"
  - **Keywords:** [Metrics keywords]
  - **Intent:** Informational
  - **Word Count:** 1400-1700 words
  - **CTA:** Free performance audit

## Content Types Distribution

### Educational Content (40%)
- **How-to Guides:** Step-by-step instructional content
- **Industry Insights:** Trend analysis and market updates
- **Best Practices:** Professional recommendations and standards
- **Problem-Solution:** Addressing common challenges

### Service-Focused Content (25%)
- **Service Pages:** Detailed service descriptions and benefits
- **Case Studies:** Client success stories and results
- **Testimonials:** Customer experience and satisfaction
- **Process Explanations:** How services are delivered

### Industry Insights Content (20%)
- **Market Analysis:** Industry trends and developments
- **Regulatory Updates:** Compliance and legal changes
- **Technology Trends:** Innovation and tool updates
- **Economic Impact:** Market conditions and business effects

### Brand Storytelling Content (15%)
- **Company Updates:** News and announcements
- **Team Spotlights:** Personnel and expertise highlights
- **Behind-the-Scenes:** Company culture and values
- **Community Involvement:** Local engagement and giving back

## Seasonal Content Planning

### Q1 (Jan-Mar): New Year, Fresh Starts
- **January:** Goal setting and planning content
- **February:** Relationship and partnership focus
- **March:** Spring preparation and growth

### Q2 (Apr-Jun): Growth and Expansion
- **April:** Fresh starts and new initiatives
- **May:** Mid-year planning and assessment
- **June:** Summer preparation and optimization

### Q3 (Jul-Sep): Performance and Results
- **July:** Mid-year review and adjustment
- **August:** Performance optimization
- **September:** Preparation for final quarter

### Q4 (Oct-Dec): Review and Planning
- **October:** Year-end preparation
- **November:** Results analysis and reporting
- **December:** Next year planning and reflection

## Content Production Workflow

### Planning Phase (Week before)
1. **Content Research:** Topic research and keyword validation
2. **Outline Creation:** Detailed content structure
3. **Resource Gathering:** Statistics, quotes, references
4. **Visual Planning:** Images, charts, infographics needed

### Creation Phase (Production week)
1. **Draft Creation:** Initial content writing
2. **SEO Optimization:** Keyword integration and meta tags
3. **Visual Creation:** Graphics and multimedia elements
4. **Internal Review:** Quality and accuracy check

### Publishing Phase (Publication week)
1. **Final Review:** Last-minute edits and approvals
2. **Publishing:** Content goes live on schedule
3. **Promotion:** Social media and email distribution
4. **Monitoring:** Performance tracking and engagement

## Content Quality Standards

### Writing Standards
- **Language:** Australian English (British spelling)
- **Tone:** Professional, helpful, authoritative
- **Reading Level:** Professional (Year 10-12)
- **Sentence Length:** Maximum 25 words
- **Paragraph Length:** 3-4 sentences maximum

### SEO Standards
- **Keyword Integration:** Natural, contextual placement
- **Meta Optimization:** Title tags and descriptions optimized
- **Header Structure:** Proper H1, H2, H3 hierarchy
- **Internal Linking:** 2-4 relevant internal links per post
- **Image Optimization:** Alt tags and file compression

### Content Elements
- **Introduction:** Hook + problem + solution preview
- **Body Sections:** Clear subheadings every 200-300 words
- **Visual Elements:** Images, charts, or infographics
- **Conclusion:** Summary + clear call-to-action
- **Citations:** Credible sources for statistics and claims

## Performance Tracking

### Content KPIs
- **Traffic Metrics:** Page views, unique visitors, time on page
- **Engagement Metrics:** Bounce rate, scroll depth, comments
- **Conversion Metrics:** CTA clicks, form submissions, consultations
- **SEO Metrics:** Keyword rankings, organic traffic, backlinks

### Monthly Review Process
1. **Performance Analysis:** Review metrics for all published content
2. **Top Performers:** Identify highest-performing content and themes
3. **Optimization Opportunities:** Content needing improvement
4. **Next Month Planning:** Adjust calendar based on performance data

## Resource Requirements

### Team Structure
- **Content Creator:** Primary writer and researcher
- **SEO Specialist:** Keyword research and optimization
- **Editor:** Quality control and brand consistency
- **Graphic Designer:** Visual content creation (as needed)

### Time Allocation
- **Research and Planning:** 25% of production time
- **Writing and Creation:** 50% of production time
- **Editing and Optimization:** 15% of production time
- **Publishing and Promotion:** 10% of production time

### Tools and Software
- **Content Creation:** [Writing and editing tools]
- **SEO Tools:** [Keyword research and optimization]
- **Analytics:** [Google Analytics, Search Console]
- **Project Management:** [Calendar and workflow tools]

---
**Calendar Created:** {datetime.now().strftime('%d %B %Y')}
**Project Manager:** [Assign team member]
**Content Team:** [List content creators]
**Next Review:** [Schedule monthly calendar review]
"""
        }

        return templates.get(filename, self._generate_generic_template(filename, client_domain))

    def _generate_generic_template(self, filename: str, client_domain: str) -> str:
        """Generate generic template for unknown files."""
        title = filename.replace('.md', '').replace('_', ' ').title()
        return f"""# {title} - {client_domain.replace('_', ' ').title()}

## Document Overview
This document is part of the {client_domain.replace('_', ' ').title()} project research phase.

## Content Status
- **Created:** {datetime.now().strftime('%d %B %Y')}
- **Status:** Template created - content pending
- **Phase:** Research Phase
- **Priority:** [To be determined]

## Research Requirements
Please complete the following sections based on project requirements:

### Section 1: [Primary Topic]
*Content to be added*

### Section 2: [Secondary Topic]
*Content to be added*

### Section 3: [Analysis and Recommendations]
*Content to be added*

## Next Steps
1. Research and gather relevant information
2. Complete content sections based on project scope
3. Review and validate content accuracy
4. Update status and schedule review

---
**Template Generated:** {datetime.now().strftime('%d %B %Y')}
**Research Team:** [Assign researcher]
**Review Date:** [Schedule content review]
"""


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description='Validate research phase completion and create templates'
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Validate phase command
    validate_parser = subparsers.add_parser('validate', help='Validate research phases')
    validate_parser.add_argument('client_domain', help='Client domain name')
    validate_parser.add_argument(
        '--phases',
        nargs='+',
        type=int,
        choices=[1, 2, 3, 4],
        help='Specific phases to validate (default: all phases)'
    )
    validate_parser.add_argument(
        '--require-phases',
        nargs='+',
        type=int,
        choices=[1, 2, 3, 4],
        help='Phases required for content creation approval'
    )

    # Create templates command
    template_parser = subparsers.add_parser('templates', help='Create research phase templates')
    template_parser.add_argument('client_domain', help='Client domain name')
    template_parser.add_argument(
        '--phases',
        nargs='+',
        type=int,
        choices=[1, 2, 3, 4],
        help='Phases to create templates for (default: all phases)'
    )

    # Report command
    report_parser = subparsers.add_parser('report', help='Generate validation report')
    report_parser.add_argument('client_domain', help='Client domain name')
    report_parser.add_argument('--output', help='Save report to file')

    # Global options
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging')

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if not args.command:
        parser.print_help()
        return

    validator = ResearchPhaseValidator()

    try:
        from datetime import datetime

        if args.command == 'validate':
            if args.phases:
                # Validate specific phases
                results = {}
                for phase in args.phases:
                    result = validator.validate_research_phase(args.client_domain, phase)
                    results[phase] = result

                    status = "✅ COMPLETE" if result['phase_complete'] else "⚠️ INCOMPLETE"
                    score = result['completion_score']
                    print(f"Phase {phase}: {status} (Score: {score}%)")

                    if result['recommendations']:
                        print("  Recommendations:")
                        for rec in result['recommendations'][:3]:  # Show top 3
                            print(f"    • {rec}")
                    print()

            else:
                # Validate all phases
                required_phases = args.require_phases or [1, 2, 3, 4]
                results = validator.validate_all_phases(args.client_domain, required_phases)

                print(f"🎯 Research Phase Validation: {args.client_domain}")
                print(f"📊 Overall Score: {results['overall_completion_score']}%")
                print(f"✅ Completed Phases: {results['summary']['completed_phases']}/{results['summary']['total_required_phases']}")
                print(f"🚀 Content Creation Ready: {'Yes' if results['content_creation_ready'] else 'No'}")

                if results['next_steps']:
                    print("\n📋 Next Steps:")
                    for step in results['next_steps']:
                        print(f"  • {step}")

        elif args.command == 'templates':
            phases = args.phases or [1, 2, 3, 4]
            results = validator.create_research_phase_templates(args.client_domain, phases)

            print(f"📝 Creating research templates for {args.client_domain}")

            if results['templates_created']:
                print(f"✅ Created {len(results['templates_created'])} templates:")
                for template in results['templates_created']:
                    print(f"  • {template}")

            if results['templates_skipped']:
                print(f"ℹ️  Skipped {len(results['templates_skipped'])} existing files:")
                for template in results['templates_skipped']:
                    print(f"  • {template}")

            if results['errors']:
                print(f"❌ Errors: {len(results['errors'])}")
                for error in results['errors']:
                    print(f"  • {error}")

        elif args.command == 'report':
            results = validator.validate_all_phases(args.client_domain)

            # Generate detailed report
            report_lines = []
            report_lines.append("=" * 60)
            report_lines.append("RESEARCH PHASE VALIDATION REPORT")
            report_lines.append("=" * 60)
            report_lines.append(f"Client: {args.client_domain}")
            report_lines.append(f"Generated: {datetime.now().strftime('%d %B %Y at %H:%M')}")
            report_lines.append("")

            report_lines.append("SUMMARY:")
            report_lines.append(f"• Overall Completion: {results['overall_completion_score']}%")
            report_lines.append(f"• Phases Complete: {results['summary']['completed_phases']}/{results['summary']['total_required_phases']}")
            report_lines.append(f"• Content Ready: {'Yes' if results['content_creation_ready'] else 'No'}")
            report_lines.append("")

            # Individual phase details
            for phase_num, phase_result in results['phase_results'].items():
                status = "✅" if phase_result['phase_complete'] else "⚠️"
                report_lines.append(f"{status} PHASE {phase_num}: {phase_result['phase_name']}")
                report_lines.append(f"   Score: {phase_result['completion_score']}%")

                if phase_result['recommendations']:
                    report_lines.append("   Recommendations:")
                    for rec in phase_result['recommendations'][:3]:
                        report_lines.append(f"     • {rec}")
                report_lines.append("")

            if results['next_steps']:
                report_lines.append("NEXT STEPS:")
                for step in results['next_steps']:
                    report_lines.append(f"• {step}")

            report_text = "\n".join(report_lines)
            print(report_text)

            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(report_text)
                print(f"\n📄 Report saved to: {args.output}")

    except Exception as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()