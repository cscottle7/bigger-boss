#!/usr/bin/env python3
"""
Bigger Boss Agent System - Client Folder Structure Validator
Validates and fixes client folder structure compliance.
"""

import argparse
import json
import logging
import sys
import io
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Fix Windows Unicode encoding issues
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ClientStructureValidator:
    """Validator for client folder structure compliance."""

    def __init__(self):
        self.required_structure = {
            'folders': [
                'strategy',
                'research',
                'content',
                'technical',
                'implementation'
            ],
            'files': [
                'README.md',
                'PROJECT_OVERVIEW.md'
            ],
            'strategy_files': [
                'research_brief.md',
                'current_website_analysis.md',
                'implementation_plan.md'
            ],
            'research_files': [
                'competitive_analysis.md',
                'audience_personas.md',
                'keyword_research.md'
            ],
            'content_files': [
                'comprehensive_website_content_plans.md',
                'content_research.md',
                'audience_style_guide.md'
            ],
            'technical_files': [
                'technical_audit.md',
                'ai_optimization_guide.md',
                'ux_ui_analysis.md'
            ],
            'implementation_files': [
                'task_deps.md',
                'execution_tracking_report.md'
            ]
        }

    def validate_client_folder(self, client_path: str, auto_fix: bool = False) -> Dict:
        """
        Validate client folder structure.

        Args:
            client_path: Path to client folder
            auto_fix: Whether to automatically fix issues

        Returns:
            Validation result dictionary
        """
        client_path = Path(client_path)
        client_domain = client_path.name

        if not client_path.exists():
            return {
                'status': 'error',
                'client_domain': client_domain,
                'message': f'Client folder does not exist: {client_path}',
                'compliant': False
            }

        issues = []
        fixes_applied = []

        # Check main folders
        for folder in self.required_structure['folders']:
            folder_path = client_path / folder
            if not folder_path.exists():
                issues.append(f'Missing required folder: {folder}')
                if auto_fix:
                    folder_path.mkdir(parents=True, exist_ok=True)
                    fixes_applied.append(f'Created folder: {folder}')

        # Check main files
        for file in self.required_structure['files']:
            file_path = client_path / file
            if not file_path.exists():
                issues.append(f'Missing required file: {file}')
                if auto_fix:
                    content = self._generate_file_content(file, client_domain)
                    file_path.write_text(content, encoding='utf-8')
                    fixes_applied.append(f'Created file: {file}')

        # Check subfolder files
        subfolder_checks = [
            ('strategy', 'strategy_files'),
            ('research', 'research_files'),
            ('content', 'content_files'),
            ('technical', 'technical_files'),
            ('implementation', 'implementation_files')
        ]

        for folder, files_key in subfolder_checks:
            folder_path = client_path / folder
            if folder_path.exists():
                for file in self.required_structure[files_key]:
                    file_path = folder_path / file
                    if not file_path.exists():
                        issues.append(f'Missing file in {folder}: {file}')
                        if auto_fix:
                            content = self._generate_file_content(file, client_domain, folder)
                            file_path.write_text(content, encoding='utf-8')
                            fixes_applied.append(f'Created file: {folder}/{file}')

        # Check for PROJECT_CHECKLIST.md
        checklist_path = client_path / 'PROJECT_CHECKLIST.md'
        if not checklist_path.exists():
            issues.append('Missing PROJECT_CHECKLIST.md')
            if auto_fix:
                content = self._generate_project_checklist(client_domain)
                checklist_path.write_text(content, encoding='utf-8')
                fixes_applied.append('Created PROJECT_CHECKLIST.md')

        compliant = len(issues) == 0
        compliance_score = max(0, 100 - (len(issues) * 5))

        result = {
            'status': 'success',
            'client_domain': client_domain,
            'client_path': str(client_path),
            'compliant': compliant,
            'compliance_score': compliance_score,
            'total_issues': len(issues),
            'issues': issues,
            'fixes_applied': fixes_applied if auto_fix else [],
            'auto_fix_enabled': auto_fix,
            'validated_at': datetime.now().isoformat()
        }

        return result

    def _generate_file_content(self, filename: str, client_domain: str, folder: str = None) -> str:
        """Generate appropriate content for missing files."""

        if filename == 'README.md':
            return self._generate_readme(client_domain)
        elif filename == 'PROJECT_OVERVIEW.md':
            return self._generate_project_overview(client_domain)
        elif filename == 'research_brief.md':
            return self._generate_research_brief(client_domain)
        elif filename == 'current_website_analysis.md':
            return self._generate_website_analysis(client_domain)
        elif filename == 'implementation_plan.md':
            return self._generate_implementation_plan(client_domain)
        elif filename == 'competitive_analysis.md':
            return self._generate_competitive_analysis(client_domain)
        elif filename == 'audience_personas.md':
            return self._generate_audience_personas(client_domain)
        elif filename == 'keyword_research.md':
            return self._generate_keyword_research(client_domain)
        elif filename == 'comprehensive_website_content_plans.md':
            return self._generate_content_plans(client_domain)
        elif filename == 'content_research.md':
            return self._generate_content_research(client_domain)
        elif filename == 'audience_style_guide.md':
            return self._generate_style_guide(client_domain)
        elif filename == 'technical_audit.md':
            return self._generate_technical_audit(client_domain)
        elif filename == 'ai_optimization_guide.md':
            return self._generate_ai_optimization(client_domain)
        elif filename == 'ux_ui_analysis.md':
            return self._generate_ux_analysis(client_domain)
        elif filename == 'task_deps.md':
            return self._generate_task_deps(client_domain)
        elif filename == 'execution_tracking_report.md':
            return self._generate_execution_tracking(client_domain)
        else:
            return f"""# {filename.replace('.md', '').replace('_', ' ').title()}

## Overview
This document is part of the {client_domain.replace('_', ' ').title()} project.

## Status
- **Created:** {datetime.now().strftime('%d %B %Y')}
- **Status:** Pending content
- **Last Updated:** {datetime.now().strftime('%d %B %Y')}

## Notes
Content to be added based on project requirements.

---
*Generated automatically by Bigger Boss Agent System*
"""

    def _generate_readme(self, client_domain: str) -> str:
        """Generate README.md template."""
        return f"""# {client_domain.replace('_', ' ').title()} - Project Navigation Hub

## Project Overview
Comprehensive marketing strategy and content development project for {client_domain.replace('_', '.')}.

## Folder Structure

### Strategy
Strategic planning and roadmap documents
- Research brief and project scope
- Current website analysis
- Implementation plan and timeline

### Research
Market intelligence and competitive analysis
- Audience personas and demographic research
- Competitive analysis and market positioning
- Keyword research and SEO analysis

### Content
Content strategy and creation guidelines
- Website content plans and briefs
- Content research and gap analysis
- Audience style guide and voice guidelines

### Technical
Technical audits and optimization recommendations
- Technical SEO audit and recommendations
- AI optimization guide for search visibility
- UX/UI analysis and improvement suggestions

### Implementation
Project execution and tracking
- Task dependencies and workflow planning
- Execution tracking and progress reports

## Project Status
- **Created:** {datetime.now().strftime('%d %B %Y')}
- **Status:** In Progress
- **Client:** {client_domain.replace('_', '.')}
- **Last Updated:** {datetime.now().strftime('%d %B %Y')}

## Key Deliverables Checklist
- [ ] Research Brief
- [ ] Audience Personas
- [ ] Competitive Analysis
- [ ] Content Strategy
- [ ] Technical Audit
- [ ] Implementation Plan
- [ ] Execution Tracking

## Quick Links
- [Project Overview](PROJECT_OVERVIEW.md)
- [Project Checklist](PROJECT_CHECKLIST.md)
- [Research Strategy](strategy/research_brief.md)
- [Implementation Plan](strategy/implementation_plan.md)

## Team Access
- **Project Manager:** [Assign team member]
- **Content Strategist:** [Assign team member]
- **SEO Specialist:** [Assign team member]
- **Implementation Lead:** [Assign team member]

---
*Bigger Boss Agent System - Australian Marketing Automation*
"""

    def _generate_project_overview(self, client_domain: str) -> str:
        """Generate PROJECT_OVERVIEW.md template."""
        return f"""# {client_domain.replace('_', ' ').title()} - Project Overview

## Executive Summary
Comprehensive digital marketing strategy and content development project for {client_domain.replace('_', '.')}.

## Project Objectives
- Enhance online presence and search engine visibility
- Develop strategic content marketing approach
- Improve conversion rates and lead generation
- Establish systematic content creation workflow

## Project Scope

### Phase 1: Research & Analysis (Weeks 1-4)
- **Market Research:** Industry analysis and competitive intelligence
- **Audience Research:** Detailed persona development and user journey mapping
- **Technical Audit:** Website performance and SEO analysis
- **Content Audit:** Existing content review and gap analysis

### Phase 2: Strategy Development (Weeks 5-6)
- **Content Strategy:** Editorial calendar and content themes
- **SEO Strategy:** Keyword targeting and optimization plan
- **User Experience:** Website improvement recommendations
- **Brand Messaging:** Voice, tone, and positioning guidelines

### Phase 3: Implementation (Weeks 7-12)
- **Content Creation:** Blog posts, landing pages, and marketing materials
- **SEO Optimization:** On-page and technical SEO improvements
- **Marketing Automation:** Lead nurturing and email campaigns
- **Performance Tracking:** Analytics setup and KPI monitoring

### Phase 4: Review & Optimization (Ongoing)
- **Performance Analysis:** Monthly reporting and insights
- **Strategy Refinement:** Continuous improvement based on data
- **Content Expansion:** Additional content based on performance
- **Scale Optimization:** Growth planning and resource allocation

## Success Metrics

### Primary KPIs
- **Organic Traffic Growth:** Target +25% in 6 months
- **Lead Generation:** Target +30% qualified leads
- **Conversion Rate:** Target +15% improvement
- **Search Visibility:** Target 50+ keyword rankings improvement

### Secondary Metrics
- Content engagement rates and social shares
- Email marketing performance and list growth
- Brand awareness and mention tracking
- Customer acquisition cost reduction

## Project Timeline
- **Project Start:** {datetime.now().strftime('%B %Y')}
- **Research Completion:** {(datetime.now()).strftime('%B %Y')} (Month 1)
- **Strategy Finalization:** {(datetime.now()).strftime('%B %Y')} (Month 1.5)
- **Implementation Launch:** {(datetime.now()).strftime('%B %Y')} (Month 2)
- **First Review:** {(datetime.now()).strftime('%B %Y')} (Month 3)
- **Performance Evaluation:** {(datetime.now()).strftime('%B %Y')} (Month 6)

## Team Structure
- **Strategic Lead:** Market research and competitive analysis
- **Content Team:** Content creation and optimization
- **Technical Team:** SEO and website improvements
- **Analytics Team:** Performance tracking and reporting

## Budget Allocation
- Research & Strategy: 25%
- Content Creation: 35%
- Technical Implementation: 25%
- Tools & Software: 10%
- Contingency: 5%

## Risk Management
- **Timeline Risks:** Buffer periods built into schedule
- **Resource Risks:** Backup team members identified
- **Technical Risks:** Staged implementation approach
- **Market Risks:** Flexible strategy adaptation

---
**Document Status:** Draft
**Last Updated:** {datetime.now().strftime('%d %B %Y')}
**Next Review:** {datetime.now().strftime('%d %B %Y')}
"""

    def _generate_project_checklist(self, client_domain: str) -> str:
        """Generate PROJECT_CHECKLIST.md template."""
        return f"""# {client_domain.replace('_', ' ').title()} - Project Checklist

## Phase 1: Research & Discovery ⏳

### Market Research
- [ ] Industry analysis completed
- [ ] Market size and trends identified
- [ ] Target market segments defined
- [ ] Competitive landscape mapped

### Audience Research
- [ ] Primary personas developed
- [ ] Secondary personas identified
- [ ] User journey mapping completed
- [ ] Pain points and motivations documented

### Competitive Analysis
- [ ] Top 5 competitors identified
- [ ] Competitor SWOT analysis completed
- [ ] Content gap analysis performed
- [ ] Differentiation opportunities identified

### Technical Audit
- [ ] Website performance analysis
- [ ] SEO technical audit completed
- [ ] UX/UI assessment performed
- [ ] Mobile optimization review

## Phase 2: Strategy Development ⏳

### Content Strategy
- [ ] Content pillars defined
- [ ] Editorial calendar created
- [ ] Content themes and topics planned
- [ ] Distribution strategy outlined

### SEO Strategy
- [ ] Keyword research completed
- [ ] Target keywords prioritized
- [ ] On-page optimization plan created
- [ ] Link building strategy developed

### Brand Guidelines
- [ ] Brand voice and tone defined
- [ ] Style guide created
- [ ] Messaging framework established
- [ ] Visual identity guidelines set

## Phase 3: Implementation ⏳

### Content Creation
- [ ] Homepage content optimized
- [ ] Service pages created/updated
- [ ] Blog content calendar executed
- [ ] Landing pages developed

### Technical Implementation
- [ ] On-page SEO optimization
- [ ] Site speed improvements
- [ ] Mobile optimization completed
- [ ] Analytics and tracking setup

### Marketing Automation
- [ ] Email sequences created
- [ ] Lead magnets developed
- [ ] CRM integration completed
- [ ] Social media automation setup

## Phase 4: Launch & Optimization ⏳

### Launch Preparation
- [ ] Quality assurance testing
- [ ] Performance monitoring setup
- [ ] Launch timeline confirmed
- [ ] Team training completed

### Go-Live Activities
- [ ] Website updates deployed
- [ ] Content published
- [ ] Marketing campaigns launched
- [ ] Monitoring systems activated

### Initial Optimization
- [ ] First month performance review
- [ ] Initial adjustments made
- [ ] User feedback incorporated
- [ ] Strategy refinements applied

## Ongoing Activities 📊

### Monthly Reviews
- [ ] Performance metrics analyzed
- [ ] Content performance evaluated
- [ ] SEO rankings tracked
- [ ] Conversion rates monitored

### Quarterly Planning
- [ ] Strategy review and updates
- [ ] New content themes identified
- [ ] Technical improvements planned
- [ ] Resource allocation reviewed

## Key Deliverables Tracking

### Research Deliverables
- [ ] Market Research Report
- [ ] Audience Personas Document
- [ ] Competitive Analysis Report
- [ ] Technical Audit Report

### Strategy Deliverables
- [ ] Content Strategy Document
- [ ] SEO Strategy Plan
- [ ] Brand Guidelines
- [ ] Implementation Roadmap

### Implementation Deliverables
- [ ] Optimized Website Content
- [ ] Blog Content Series
- [ ] Marketing Automation Setup
- [ ] Performance Tracking System

## Success Metrics Dashboard

### Traffic Metrics
- [ ] Organic traffic growth: +25% target
- [ ] Direct traffic increase: +15% target
- [ ] Referral traffic growth: +20% target

### Engagement Metrics
- [ ] Average session duration: +30% target
- [ ] Pages per session: +25% target
- [ ] Bounce rate reduction: -15% target

### Conversion Metrics
- [ ] Lead generation: +30% target
- [ ] Conversion rate: +15% target
- [ ] Customer acquisition cost: -20% target

## Project Status: 🟡 In Progress

**Current Phase:** Research & Discovery
**Progress:** 25% Complete
**Next Milestone:** Strategy Development
**Timeline Status:** On Track

---
**Last Updated:** {datetime.now().strftime('%d %B %Y')}
**Project Manager:** [Assign team member]
**Client Contact:** {client_domain.replace('_', '.')}
"""

    def _generate_research_brief(self, client_domain: str) -> str:
        """Generate research brief template."""
        return f"""# Research Brief - {client_domain.replace('_', ' ').title()}

## Project Overview
This research brief outlines the comprehensive research approach for the {client_domain.replace('_', '.')} marketing project.

## Research Objectives
1. Understand target audience demographics and psychographics
2. Analyze competitive landscape and market positioning
3. Identify content gaps and opportunities
4. Define keyword strategy and SEO opportunities

## Research Methodology

### Primary Research
- Customer surveys and interviews
- Website analytics analysis
- Social media engagement review
- Conversion funnel analysis

### Secondary Research
- Industry reports and market studies
- Competitor website and content analysis
- Keyword research and search volume analysis
- Social media and review site analysis

## Target Audience Research
- Demographics and firmographics
- Pain points and challenges
- Goals and motivations
- Content consumption preferences
- Decision-making process

## Competitive Analysis Scope
- Direct competitors (5-7 identified)
- Indirect competitors (3-5 identified)
- Content strategy comparison
- SEO performance benchmarking
- Social media presence analysis

## Deliverables Timeline
- Week 1: Market and audience research
- Week 2: Competitive analysis
- Week 3: Technical and content audit
- Week 4: Synthesis and strategic recommendations

---
**Status:** {datetime.now().strftime('%d %B %Y')} - Template Created
"""

    def _generate_technical_audit(self, client_domain: str) -> str:
        """Generate technical audit template."""
        return f"""# Technical Audit - {client_domain.replace('_', ' ').title()}

## Audit Overview
Comprehensive technical analysis of {client_domain.replace('_', '.')} website performance, SEO, and user experience.

## Website Performance
- [ ] Page load speed analysis
- [ ] Core Web Vitals assessment
- [ ] Mobile performance review
- [ ] Server response time evaluation

## SEO Technical Analysis
- [ ] Crawlability and indexation
- [ ] URL structure and hierarchy
- [ ] Meta tags and schema markup
- [ ] Internal linking structure

## User Experience Audit
- [ ] Navigation and site structure
- [ ] Mobile responsiveness
- [ ] Accessibility compliance
- [ ] Conversion path optimization

## Security and Compliance
- [ ] SSL certificate verification
- [ ] Privacy policy compliance
- [ ] GDPR/CCPA compliance check
- [ ] Security headers analysis

## Recommendations
*Technical recommendations will be added following audit completion.*

---
**Audit Date:** {datetime.now().strftime('%d %B %Y')}
**Next Review:** [Schedule follow-up]
"""

    def _generate_task_deps(self, client_domain: str) -> str:
        """Generate task dependencies template."""
        return f"""# Task Dependencies - {client_domain.replace('_', ' ').title()}

## Implementation Workflow

### Phase 1: Foundation (Weeks 1-4)
```yaml
research_foundation:
  dependencies: []
  tasks:
    - market_research
    - audience_analysis
    - competitive_audit
  deliverables:
    - research_brief.md
    - audience_personas.md
    - competitive_analysis.md
```

### Phase 2: Strategy Development (Weeks 5-6)
```yaml
strategy_development:
  dependencies: [research_foundation]
  tasks:
    - content_strategy
    - seo_strategy
    - technical_recommendations
  deliverables:
    - content_strategy.md
    - seo_plan.md
    - technical_roadmap.md
```

### Phase 3: Implementation (Weeks 7-12)
```yaml
content_creation:
  dependencies: [strategy_development]
  tasks:
    - homepage_optimization
    - service_page_creation
    - blog_content_development
  deliverables:
    - optimized_website_content
    - blog_articles
    - landing_pages

technical_implementation:
  dependencies: [strategy_development]
  tasks:
    - seo_optimization
    - site_speed_improvements
    - analytics_setup
  deliverables:
    - technical_improvements
    - tracking_implementation
```

### Phase 4: Launch & Optimization (Week 13+)
```yaml
launch_activities:
  dependencies: [content_creation, technical_implementation]
  tasks:
    - quality_assurance
    - soft_launch
    - performance_monitoring
  deliverables:
    - launch_report
    - performance_dashboard
```

## Iterative Feedback Loops
All content creation includes iterative improvement cycles:
- Initial draft creation
- Internal review and feedback
- Client review and approval
- Final optimization and publishing

---
**Created:** {datetime.now().strftime('%d %B %Y')}
**Project:** {client_domain.replace('_', ' ').title()}
"""

    def _generate_competitive_analysis(self, client_domain: str) -> str:
        """Generate competitive analysis template."""
        return f"""# Competitive Analysis - {client_domain.replace('_', ' ').title()}

## Analysis Overview
Comprehensive competitive landscape analysis for {client_domain.replace('_', '.')} market positioning and differentiation strategy.

## Direct Competitors

### Competitor 1: [Name]
- **Website:** [URL]
- **Market Position:** [Description]
- **Strengths:** [Key advantages]
- **Weaknesses:** [Areas for exploitation]
- **Content Strategy:** [Approach analysis]
- **SEO Performance:** [Ranking analysis]

### Competitor 2: [Name]
- **Website:** [URL]
- **Market Position:** [Description]
- **Strengths:** [Key advantages]
- **Weaknesses:** [Areas for exploitation]
- **Content Strategy:** [Approach analysis]
- **SEO Performance:** [Ranking analysis]

## Indirect Competitors
- [Competitor 3]
- [Competitor 4]
- [Competitor 5]

## Market Gap Analysis
- **Underserved Segments:** [Opportunities]
- **Content Gaps:** [Missing topics/formats]
- **Service Gaps:** [Unmet needs]
- **Geographic Gaps:** [Location opportunities]

## Differentiation Opportunities
1. [Unique value proposition 1]
2. [Unique value proposition 2]
3. [Unique value proposition 3]

## Strategic Recommendations
- **Positioning Strategy:** [Recommended approach]
- **Content Focus Areas:** [Priority topics]
- **SEO Opportunities:** [Target keywords]
- **Market Entry Strategy:** [Approach recommendations]

---
**Analysis Date:** {datetime.now().strftime('%d %B %Y')}
**Analyst:** [Team member]
**Next Review:** [Schedule update]
"""

    def _generate_audience_personas(self, client_domain: str) -> str:
        """Generate audience personas template."""
        return f"""# Audience Personas - {client_domain.replace('_', ' ').title()}

## Primary Persona: [Professional Patricia]

### Demographics
- **Age:** 35-55
- **Location:** Major Australian cities
- **Occupation:** Business professional/manager
- **Income:** $75,000-$150,000 AUD
- **Education:** University degree

### Psychographics
- **Values:** Quality, reliability, efficiency
- **Goals:** Career advancement, business success
- **Challenges:** Time constraints, staying current
- **Motivations:** Professional growth, recognition

### Behavior Patterns
- **Content Consumption:** Weekday mornings, lunch breaks
- **Device Preferences:** Desktop at work, mobile commuting
- **Information Sources:** Industry publications, LinkedIn
- **Decision Making:** Research-driven, peer influence

### Content Preferences
- **Formats:** Articles, case studies, whitepapers
- **Topics:** Industry insights, best practices, how-to guides
- **Tone:** Professional, authoritative, practical
- **Length:** 800-1500 words

## Secondary Persona: [Business Owner Bob]

### Demographics
- **Age:** 45-65
- **Location:** Regional centres and major cities
- **Occupation:** Small business owner
- **Income:** $100,000+ AUD
- **Education:** Trade/business experience

### Psychographics
- **Values:** Results, ROI, reliability
- **Goals:** Business growth, profitability
- **Challenges:** Limited time, resource constraints
- **Motivations:** Success, sustainability, legacy

### Behavior Patterns
- **Content Consumption:** Early mornings, evenings
- **Device Preferences:** Mobile, tablet
- **Information Sources:** Industry associations, peers
- **Decision Making:** Practical, cost-focused

### Content Preferences
- **Formats:** Success stories, ROI calculators, quick tips
- **Topics:** Growth strategies, cost reduction, efficiency
- **Tone:** Direct, results-focused, no-nonsense
- **Length:** 500-1000 words

## User Journey Mapping

### Awareness Stage
- **Pain Points:** Problem recognition
- **Content Needs:** Educational, informational
- **Touchpoints:** Search, social media, referrals
- **Goals:** Understanding options

### Consideration Stage
- **Pain Points:** Solution evaluation
- **Content Needs:** Comparison, case studies
- **Touchpoints:** Website, email, consultations
- **Goals:** Narrowing choices

### Decision Stage
- **Pain Points:** Final selection
- **Content Needs:** Testimonials, guarantees
- **Touchpoints:** Sales calls, proposals
- **Goals:** Making confident choice

### Retention Stage
- **Pain Points:** Implementation, results
- **Content Needs:** Support, advanced tips
- **Touchpoints:** Account management, support
- **Goals:** Maximizing value

---
**Research Date:** {datetime.now().strftime('%d %B %Y')}
**Research Method:** [Surveys, interviews, analytics]
**Next Update:** [Schedule review]
"""

    def _generate_keyword_research(self, client_domain: str) -> str:
        """Generate keyword research template."""
        return f"""# Keyword Research - {client_domain.replace('_', ' ').title()}

## Research Overview
Comprehensive keyword analysis for {client_domain.replace('_', '.')} search engine optimization strategy.

## Primary Keywords (High Priority)
| Keyword | Search Volume | Competition | Difficulty | Intent |
|---------|---------------|-------------|------------|--------|
| [keyword 1] | [volume] | [competition] | [difficulty] | [intent] |
| [keyword 2] | [volume] | [competition] | [difficulty] | [intent] |
| [keyword 3] | [volume] | [competition] | [difficulty] | [intent] |

## Secondary Keywords (Medium Priority)
| Keyword | Search Volume | Competition | Difficulty | Intent |
|---------|---------------|-------------|------------|--------|
| [keyword 4] | [volume] | [competition] | [difficulty] | [intent] |
| [keyword 5] | [volume] | [competition] | [difficulty] | [intent] |
| [keyword 6] | [volume] | [competition] | [difficulty] | [intent] |

## Long-tail Keywords (Quick Wins)
- [long-tail keyword 1]
- [long-tail keyword 2]
- [long-tail keyword 3]

## Keyword Mapping Strategy

### Homepage
- **Primary:** [main keyword]
- **Secondary:** [supporting keywords]
- **Intent:** Brand/navigation

### Service Pages
- **Service 1:** [service keywords]
- **Service 2:** [service keywords]
- **Intent:** Commercial/transactional

### Blog Content
- **Topic 1:** [informational keywords]
- **Topic 2:** [informational keywords]
- **Intent:** Informational

## Seasonal Keywords
- **Q1:** [seasonal terms]
- **Q2:** [seasonal terms]
- **Q3:** [seasonal terms]
- **Q4:** [seasonal terms]

## Competitor Keyword Analysis
- **Competitor 1:** [their top keywords]
- **Competitor 2:** [their top keywords]
- **Gap Opportunities:** [keywords they're missing]

## Implementation Priority
1. **Phase 1:** [high-impact, low-competition keywords]
2. **Phase 2:** [medium-difficulty keywords with good volume]
3. **Phase 3:** [competitive keywords requiring content depth]

---
**Research Date:** {datetime.now().strftime('%d %B %Y')}
**Tools Used:** [SEMrush, Ahrefs, Google Keyword Planner]
**Next Review:** [Schedule update]
"""

    # Additional helper methods for remaining templates...
    def _generate_content_plans(self, client_domain: str) -> str:
        """Generate content plans template."""
        return f"""# Website Content Plans - {client_domain.replace('_', ' ').title()}

## Content Strategy Overview
Comprehensive content planning for {client_domain.replace('_', '.')} website optimization and growth.

## Homepage Content Plan
- **Objective:** Clear value proposition and user guidance
- **Key Messages:** [Primary benefits and differentiators]
- **Content Sections:** Hero, services, testimonials, CTA
- **Word Count:** 400-600 words
- **SEO Focus:** [Primary brand keywords]

## Service Pages Content
### Service 1: [Service Name]
- **Content Brief:** [Description and benefits]
- **Target Keywords:** [SEO keywords]
- **Word Count:** 800-1200 words
- **Structure:** Overview, benefits, process, pricing, CTA

### Service 2: [Service Name]
- **Content Brief:** [Description and benefits]
- **Target Keywords:** [SEO keywords]
- **Word Count:** 800-1200 words
- **Structure:** Overview, benefits, process, pricing, CTA

## About Page Content
- **Story Elements:** [Company history and mission]
- **Team Introduction:** [Key personnel highlights]
- **Values and Approach:** [Differentiating factors]
- **Trust Signals:** [Credentials and testimonials]

## Blog Content Strategy
- **Publishing Frequency:** [2-4 posts per month]
- **Content Themes:** [Industry insights, how-to guides, case studies]
- **Word Count Range:** 1000-2000 words
- **SEO Integration:** [Keyword targeting strategy]

---
**Plan Date:** {datetime.now().strftime('%d %B %Y')}
**Content Manager:** [Assign team member]
"""

    def _generate_style_guide(self, client_domain: str) -> str:
        """Generate style guide template."""
        return f"""# Style Guide - {client_domain.replace('_', ' ').title()}

## Brand Voice and Tone

### Brand Personality
- **Professional:** Expert knowledge and reliable service
- **Approachable:** Friendly and accessible communication
- **Trustworthy:** Honest and transparent in all interactions
- **Results-Focused:** Emphasis on outcomes and value

### Tone Attributes
- **Confident:** Assertive without being arrogant
- **Helpful:** Genuinely focused on client success
- **Clear:** Simple, direct communication
- **Australian:** Local terminology and cultural references

## Writing Guidelines

### Language and Style
- **Language:** Australian English (British spelling)
- **Reading Level:** Professional (Year 10-12 equivalent)
- **Sentence Length:** Maximum 25 words for clarity
- **Paragraph Length:** 3-4 sentences maximum
- **Voice:** Active voice preferred

### Formatting Standards
- **Headings:** Clear hierarchy with H1, H2, H3 structure
- **Lists:** Use bullet points for scanability
- **Emphasis:** Bold for key points, italics for emphasis
- **Links:** Descriptive anchor text, not "click here"

### Content Structure
- **Introductions:** Hook + problem + solution preview
- **Body:** Logical flow with subheadings every 200-300 words
- **Conclusions:** Summary + clear call-to-action

## SEO Guidelines
- **Title Tags:** 50-60 characters including primary keyword
- **Meta Descriptions:** 150-160 characters, compelling and informative
- **Headers:** H1 (1 per page), H2 (2-4 per page), H3 (as needed)
- **Keywords:** Natural integration, avoid keyword stuffing
- **Internal Links:** 2-4 relevant internal links per 1000 words

## Terminology Guidelines

### Preferred Terms
- **Clients** (not customers)
- **Solutions** (not products)
- **Investment** (not cost)
- **Partnership** (not vendor relationship)

### Australian Spellings
- Organisation (not organization)
- Optimise (not optimize)
- Colour (not color)
- Centre (not center)

---
**Guide Version:** 1.0
**Created:** {datetime.now().strftime('%d %B %Y')}
**Next Review:** [Schedule update]
"""

    def validate_folder_batch(self, clients_dir: str, auto_fix: bool = False) -> Dict:
        """Validate multiple client folders in batch."""
        clients_path = Path(clients_dir)

        if not clients_path.exists():
            return {
                'status': 'error',
                'message': f'Clients directory does not exist: {clients_dir}',
                'results': []
            }

        results = []
        overall_stats = {
            'total_clients': 0,
            'compliant_clients': 0,
            'total_issues': 0,
            'fixes_applied': 0
        }

        # Find all client folders
        for client_folder in clients_path.iterdir():
            if client_folder.is_dir() and not client_folder.name.startswith('.'):
                result = self.validate_client_folder(str(client_folder), auto_fix)
                results.append(result)

                overall_stats['total_clients'] += 1
                if result.get('compliant', False):
                    overall_stats['compliant_clients'] += 1
                overall_stats['total_issues'] += result.get('total_issues', 0)
                overall_stats['fixes_applied'] += len(result.get('fixes_applied', []))

        compliance_rate = (overall_stats['compliant_clients'] / overall_stats['total_clients'] * 100) if overall_stats['total_clients'] > 0 else 0

        return {
            'status': 'success',
            'validation_date': datetime.now().isoformat(),
            'overall_stats': overall_stats,
            'compliance_rate': compliance_rate,
            'auto_fix_enabled': auto_fix,
            'results': results
        }

    def generate_compliance_report(self, results: Dict) -> str:
        """Generate compliance report text."""
        report = []
        report.append("=" * 60)
        report.append("CLIENT FOLDER STRUCTURE COMPLIANCE REPORT")
        report.append("=" * 60)
        report.append(f"Generated: {datetime.now().strftime('%d %B %Y at %H:%M')}")
        report.append("")

        stats = results.get('overall_stats', {})
        report.append("SUMMARY STATISTICS:")
        report.append(f"• Total Clients Validated: {stats.get('total_clients', 0)}")
        report.append(f"• Compliant Clients: {stats.get('compliant_clients', 0)}")
        report.append(f"• Compliance Rate: {results.get('compliance_rate', 0):.1f}%")
        report.append(f"• Total Issues Found: {stats.get('total_issues', 0)}")
        if results.get('auto_fix_enabled', False):
            report.append(f"• Fixes Applied: {stats.get('fixes_applied', 0)}")
        report.append("")

        # Individual client results
        for result in results.get('results', []):
            client = result.get('client_domain', 'Unknown')
            compliant = result.get('compliant', False)
            issues = result.get('total_issues', 0)
            compliance_score = result.get('compliance_score', 0)

            status_icon = "✅" if compliant else "⚠️"
            report.append(f"{status_icon} {client}")
            report.append(f"   Compliance Score: {compliance_score}%")
            if issues > 0:
                report.append(f"   Issues Found: {issues}")
                for issue in result.get('issues', []):
                    report.append(f"     - {issue}")

            if result.get('fixes_applied'):
                report.append(f"   Fixes Applied: {len(result['fixes_applied'])}")

            report.append("")

        return "\n".join(report)


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description='Validate and fix client folder structure compliance'
    )

    parser.add_argument(
        'path',
        help='Path to client folder or clients directory'
    )
    parser.add_argument(
        '--auto-fix',
        action='store_true',
        help='Automatically fix structural issues'
    )
    parser.add_argument(
        '--batch',
        action='store_true',
        help='Validate all client folders in directory'
    )
    parser.add_argument(
        '--report',
        help='Save compliance report to file'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    validator = ClientStructureValidator()

    try:
        if args.batch:
            results = validator.validate_folder_batch(args.path, args.auto_fix)
        else:
            results = validator.validate_client_folder(args.path, args.auto_fix)
            # Wrap single result for consistent reporting
            results = {
                'status': 'success',
                'validation_date': results.get('validated_at'),
                'auto_fix_enabled': args.auto_fix,
                'results': [results],
                'overall_stats': {
                    'total_clients': 1,
                    'compliant_clients': 1 if results.get('compliant') else 0,
                    'total_issues': results.get('total_issues', 0),
                    'fixes_applied': len(results.get('fixes_applied', []))
                },
                'compliance_rate': 100 if results.get('compliant') else results.get('compliance_score', 0)
            }

        # Generate and display report
        report_text = validator.generate_compliance_report(results)
        print(report_text)

        # Save report if requested
        if args.report:
            with open(args.report, 'w', encoding='utf-8') as f:
                f.write(report_text)
            print(f"\n📄 Report saved to: {args.report}")

        # Exit with appropriate code
        if results.get('overall_stats', {}).get('total_issues', 0) > 0 and not args.auto_fix:
            print("\n⚠️  Issues found. Use --auto-fix to resolve automatically.")
            sys.exit(1)
        else:
            print("\n✅ Validation completed successfully!")
            sys.exit(0)

    except Exception as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()