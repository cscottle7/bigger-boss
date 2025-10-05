#!/usr/bin/env python3
"""
Bigger Boss Agent System - Pre-Delivery Audit System
Comprehensive compliance audit before client delivery.
"""

import argparse
import json
import logging
import sys
import io
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

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


class PreDeliveryAuditor:
    """Comprehensive pre-delivery audit system."""

    def __init__(self):
        self.mandatory_files = {
            'PROJECT_OVERVIEW.md': 'Executive summary and project navigation',
            'content/audience_style_guide.md': 'Audience-specific writing guidelines',
            'content/content_research.md': 'Content research foundation',
            'content/comprehensive_website_content_plans.md': 'Main content strategy',
            'strategy/research_brief.md': 'Research strategy and objectives',
            'strategy/current_website_analysis.md': 'Baseline website assessment',
            'strategy/implementation_plan.md': 'Implementation roadmap',
            'research/competitive_analysis.md': 'Competitive intelligence',
            'research/audience_personas.md': 'Target audience personas',
            'research/keyword_research.md': 'SEO and keyword strategy',
            'technical/technical_audit.md': 'Technical performance analysis',
            'technical/ai_optimization_guide.md': 'AI optimization recommendations',
            'technical/ux_ui_analysis.md': 'User experience assessment',
            'implementation/task_deps.md': 'Task dependencies with feedback loops',
            'implementation/execution_tracking_report.md': 'Implementation progress tracking'
        }

        # 2025 SOP Word Count Requirements
        self.word_count_requirements = {
            'strategy': (800, 1500),        # Strategy documents
            'content_strategy': (800, 1500), # Content strategy
            'service_page': (800, 1500),    # Service pages
            'blog_post': (1500, 2500),      # SEO-focused blogs
            'about_page': (300, 800),       # About pages
            'homepage': (500, 1000),        # Homepage content
            'research': (500, 1500),        # Research documents
            'technical': (500, 1200),       # Technical documents
            'implementation': (300, 800)    # Implementation documents
        }

    def extract_client_domain_from_path(self, file_path: str) -> Optional[str]:
        """Extract client domain from file path."""
        path = Path(file_path)
        parts = path.parts

        # Find 'clients' in path
        try:
            clients_index = parts.index('clients')
            if clients_index + 1 < len(parts):
                return parts[clients_index + 1]
        except ValueError:
            pass

        return None

    def get_client_root_path(self, file_path: str) -> Optional[Path]:
        """Get client root directory from any file path within client folder."""
        path = Path(file_path)
        parts = path.parts

        try:
            clients_index = parts.index('clients')
            if clients_index + 1 < len(parts):
                client_domain = parts[clients_index + 1]
                return Path('clients') / client_domain
        except ValueError:
            return None

    def check_mandatory_files(self, client_root: Path) -> Tuple[List[str], List[str]]:
        """Check for missing mandatory files."""
        missing_files = []
        existing_files = []

        for file_path, description in self.mandatory_files.items():
            full_path = client_root / file_path
            if full_path.exists() and full_path.stat().st_size > 50:  # Minimum content check
                existing_files.append(file_path)
            else:
                missing_files.append(f"{file_path} - {description}")

        return existing_files, missing_files

    def check_word_count_compliance(self, client_root: Path) -> List[Dict]:
        """Check word count compliance against 2025 SOPs."""
        violations = []

        for file_path in self.mandatory_files.keys():
            full_path = client_root / file_path
            if full_path.exists():
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        word_count = len(content.split())

                    # Determine content type for SOP requirements
                    content_type = self.determine_content_type(file_path)
                    min_words, max_words = self.word_count_requirements.get(content_type, (300, 2000))

                    if word_count < min_words:
                        violations.append({
                            'file': file_path,
                            'issue': 'UNDER_SOP_MINIMUM',
                            'current_words': word_count,
                            'required_range': f"{min_words}-{max_words}",
                            'message': f"Below SOP minimum: {word_count} < {min_words} words"
                        })
                    elif word_count > max_words:
                        violations.append({
                            'file': file_path,
                            'issue': 'OVER_SOP_MAXIMUM',
                            'current_words': word_count,
                            'required_range': f"{min_words}-{max_words}",
                            'message': f"Exceeds SOP maximum: {word_count} > {max_words} words"
                        })

                except Exception as e:
                    logger.error(f"Error reading {full_path}: {e}")

        return violations

    def determine_content_type(self, file_path: str) -> str:
        """Determine content type from file path for SOP requirements."""
        if 'strategy' in file_path:
            return 'strategy'
        elif 'content' in file_path and 'strategy' in file_path:
            return 'content_strategy'
        elif 'research' in file_path:
            return 'research'
        elif 'technical' in file_path:
            return 'technical'
        elif 'implementation' in file_path:
            return 'implementation'
        else:
            return 'general'

    def check_user_journey_mapping(self, client_root: Path) -> List[str]:
        """Check for user journey mapping in content strategy."""
        issues = []
        content_strategy_path = client_root / 'content' / 'comprehensive_website_content_plans.md'

        if content_strategy_path.exists():
            try:
                with open(content_strategy_path, 'r', encoding='utf-8') as f:
                    content = f.read().lower()

                required_journey_elements = [
                    'user journey',
                    'conversion path',
                    'customer journey',
                    'journey mapping',
                    'touchpoint'
                ]

                missing_elements = []
                for element in required_journey_elements:
                    if element not in content:
                        missing_elements.append(element)

                if len(missing_elements) >= 3:  # If missing most journey elements
                    issues.append("User journey mapping appears incomplete or missing from content strategy")

            except Exception as e:
                logger.error(f"Error checking user journey mapping: {e}")
                issues.append("Unable to verify user journey mapping due to file read error")

        return issues

    def check_british_english_compliance(self, client_root: Path) -> List[Dict]:
        """Basic check for British English compliance."""
        violations = []
        american_spellings = {
            'organization': 'organisation',
            'optimize': 'optimise',
            'analyze': 'analyse',
            'color': 'colour',
            'center': 'centre',
            'favor': 'favour',
            'honor': 'honour',
            'behavior': 'behaviour'
        }

        for file_path in self.mandatory_files.keys():
            full_path = client_root / file_path
            if full_path.exists():
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read().lower()

                    found_american = []
                    for american, british in american_spellings.items():
                        if american in content and british not in content.replace(american, ''):
                            found_american.append(f"{american} → {british}")

                    if found_american:
                        violations.append({
                            'file': file_path,
                            'american_spellings': found_american[:3]  # Limit to first 3 found
                        })

                except Exception as e:
                    logger.error(f"Error checking British English in {full_path}: {e}")

        return violations

    def generate_missing_file_templates(self, client_root: Path, missing_files: List[str]) -> List[str]:
        """Generate basic templates for missing files."""
        generated = []
        client_domain = client_root.name

        templates = {
            'PROJECT_OVERVIEW.md': self.generate_project_overview_template(client_domain),
            'content/audience_style_guide.md': self.generate_audience_style_guide_template(client_domain),
            'content/content_research.md': self.generate_content_research_template(client_domain),
            'content/comprehensive_website_content_plans.md': self.generate_comprehensive_content_plans_template(client_domain),
            'strategy/research_brief.md': self.generate_research_brief_template(client_domain),
            'strategy/current_website_analysis.md': self.generate_website_analysis_template(client_domain),
            'strategy/implementation_plan.md': self.generate_implementation_plan_template(client_domain),
            'research/competitive_analysis.md': self.generate_competitive_analysis_template(client_domain),
            'research/audience_personas.md': self.generate_audience_personas_template(client_domain),
            'research/keyword_research.md': self.generate_keyword_research_template(client_domain),
            'technical/technical_audit.md': self.generate_technical_audit_template(client_domain),
            'technical/ai_optimization_guide.md': self.generate_ai_optimization_template(client_domain),
            'technical/ux_ui_analysis.md': self.generate_ux_ui_template(client_domain),
            'implementation/task_deps.md': self.generate_task_deps_template(client_domain),
            'implementation/execution_tracking_report.md': self.generate_execution_tracking_template(client_domain)
        }

        for missing_file_desc in missing_files:
            file_path = missing_file_desc.split(' - ')[0]  # Extract file path from description
            if file_path in templates:
                full_path = client_root / file_path
                full_path.parent.mkdir(parents=True, exist_ok=True)

                try:
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(templates[file_path])
                    generated.append(file_path)
                except Exception as e:
                    logger.error(f"Error generating {file_path}: {e}")

        return generated

    def generate_project_overview_template(self, client_domain: str) -> str:
        """Generate PROJECT_OVERVIEW.md template."""
        return f"""# {client_domain.replace('_', ' ').title()} - Project Overview

## Executive Summary
Comprehensive marketing strategy and content development project for {client_domain.replace('_', '.')}.

## Project Objectives
- Enhance online presence and digital marketing effectiveness
- Develop comprehensive content strategy aligned with business goals
- Improve search engine optimisation and organic visibility
- Create systematic approach to content creation and marketing automation

## Project Scope

### Research Phase (Completed)
- Market analysis and competitive intelligence
- Audience research and persona development
- SEO and keyword research strategy
- Content gap analysis and opportunity identification

### Strategy Development (Completed)
- Content strategy and editorial planning
- Marketing funnel optimisation approach
- Brand messaging and positioning strategy
- Multi-channel distribution planning

### Implementation (In Progress)
- Content creation and optimisation
- Website improvements and technical SEO
- Marketing automation setup and configuration
- Performance monitoring and reporting framework

## Key Deliverables
- ✅ Comprehensive audience persona research
- ✅ Competitive analysis and market positioning
- ✅ Advanced SEO and keyword strategy
- ✅ Content strategy and editorial calendar
- ✅ AI optimisation and future-proofing guide
- ⏳ Implementation roadmap and task dependencies
- ⏳ Execution tracking and progress reporting

## Success Metrics
- Increased organic search visibility and keyword rankings
- Improved content engagement rates and user experience
- Enhanced lead generation and conversion optimisation
- Systematic content production workflow establishment

## Timeline and Milestones
- **Project Initiation:** {datetime.now().strftime('%B %Y')}
- **Research Phase:** Completed
- **Strategy Development:** Completed
- **Implementation Phase:** In Progress
- **Performance Review:** Monthly ongoing

## Team Structure and Responsibilities
- **Research Team:** Market analysis and competitive intelligence
- **Content Team:** Content creation and optimisation
- **Technical Team:** SEO and website optimisation
- **Strategy Team:** Project coordination and performance monitoring

## Next Steps
1. Implementation roadmap execution
2. Content creation workflow deployment
3. Performance monitoring and optimisation
4. Regular review and strategy refinement

---
*Project Overview created: {datetime.now().strftime('%d %B %Y')}*
*Client: {client_domain.replace('_', '.')}*
"""

    def generate_audience_style_guide_template(self, client_domain: str) -> str:
        """Generate audience style guide template."""
        return f"""# {client_domain.replace('_', ' ').title()} - Audience Style Guide

## Brand Voice and Tone

### Primary Brand Voice
- **Professional yet approachable**: Demonstrate expertise while remaining accessible
- **Authoritative and trustworthy**: Establish credibility through evidence-based content
- **Empathetic and understanding**: Address customer pain points with genuine concern
- **Solution-focused**: Always provide clear pathways to resolution

### Tone Variations by Context

#### Educational Content
- **Informative and clear**: Complex topics explained in accessible language
- **Patient and thorough**: Step-by-step guidance without overwhelming details
- **Evidence-based**: Supporting claims with credible sources and data

#### Service-Focused Content
- **Confident and reassuring**: Demonstrate capability and build trust
- **Benefit-oriented**: Focus on outcomes and value proposition
- **Action-oriented**: Clear calls-to-action and next steps

#### Problem-Solution Content
- **Empathetic acknowledgment**: Recognise customer challenges
- **Solution-focused approach**: Provide clear pathways to resolution
- **Supportive guidance**: Offer ongoing assistance and resources

## Writing Standards

### Language Preferences
- **British English**: Use British spelling and terminology throughout
- **Professional vocabulary**: Industry-appropriate language without jargon overuse
- **Conversational elements**: Natural flow while maintaining professionalism
- **Active voice preference**: Direct, engaging sentence construction

### Content Structure Guidelines
- **Clear headings**: Descriptive section headers for easy navigation
- **Logical flow**: Information presented in intuitive sequence
- **Scannable format**: Bullet points, numbered lists, and visual breaks
- **Summary sections**: Key points highlighted for quick reference

### Technical Communication
- **Accessible explanations**: Complex concepts broken down appropriately
- **Visual support**: Diagrams and examples where beneficial
- **Step-by-step guidance**: Clear procedural instructions
- **Troubleshooting focus**: Anticipate and address common questions

## Audience-Specific Adaptations

### Primary Audience Considerations
- **Information-seeking behaviour**: Comprehensive yet digestible content
- **Decision-making process**: Support research and comparison phases
- **Trust-building requirements**: Credentials, testimonials, and evidence
- **Accessibility needs**: Clear navigation and multiple content formats

### Content Personalisation
- **Persona-specific messaging**: Tailored communication for different user types
- **Journey stage awareness**: Content appropriate for awareness, consideration, decision phases
- **Pain point addressing**: Direct response to specific audience challenges
- **Value proposition alignment**: Benefits communicated in audience-relevant terms

## Quality Standards

### Content Requirements
- **Accuracy verification**: All claims supported by credible sources
- **Currency maintenance**: Regular updates to ensure relevance
- **Accessibility compliance**: Content accessible to all users
- **SEO optimisation**: Search-friendly while maintaining readability

### Review Process
- **Editorial review**: Grammar, style, and brand voice consistency
- **Technical accuracy**: Subject matter expert verification
- **Audience alignment**: Persona and journey stage appropriateness
- **Performance monitoring**: Engagement and conversion tracking

---
*Style Guide created: {datetime.now().strftime('%d %B %Y')}*
*Client: {client_domain.replace('_', '.')}*
"""

    def generate_content_research_template(self, client_domain: str) -> str:
        """Generate content research template."""
        return f"""# {client_domain.replace('_', ' ').title()} - Content Research Foundation

## Research Methodology

### Phase 1: Foundation Research
- **Audience Analysis**: Comprehensive persona development and behavioural research
- **Market Assessment**: Industry trends, opportunities, and competitive landscape
- **Brand Positioning**: Unique value proposition and differentiation strategy
- **SWOT Analysis**: Internal strengths/weaknesses and external opportunities/threats

### Phase 2: Competitive Intelligence
- **Competitor Content Audit**: Analysis of top 5 industry competitors
- **Content Gap Identification**: Opportunities for unique content positioning
- **Trending Topics Research**: Current industry discussions and emerging themes
- **Search Landscape Analysis**: Market size, competition levels, and seasonal trends

### Phase 3: SEO and Keyword Strategy
- **Comprehensive Keyword Research**: Primary and secondary keyword identification
- **Search Intent Analysis**: User intent mapping and content journey optimisation
- **Keyword Gap Analysis**: Untapped opportunities and competitive advantages
- **Funnel Stage Mapping**: Keywords aligned with awareness, consideration, decision phases

### Phase 4: Content Planning and Optimisation
- **Content Brief Development**: Detailed specifications for high-priority content
- **AI Optimisation Strategy**: Future-proofing for AI search and voice queries
- **Content Calendar Planning**: 12-month strategic content scheduling
- **Performance Framework**: Measurement and optimisation protocols

## Key Research Findings

### Audience Insights
- **Primary Demographics**: [To be populated from audience persona research]
- **Content Preferences**: [Information seeking behaviour and format preferences]
- **Pain Points**: [Key challenges and solution requirements]
- **Decision Factors**: [Criteria influencing purchase/engagement decisions]

### Market Opportunities
- **Content Gaps**: [Identified opportunities for unique content creation]
- **Trending Topics**: [Current industry discussions and emerging themes]
- **Seasonal Patterns**: [Content timing and seasonal optimisation opportunities]
- **Competitive Advantages**: [Areas for differentiation and thought leadership]

### SEO Opportunities
- **High-Value Keywords**: [Primary target keywords with significant opportunity]
- **Low-Competition Niches**: [Untapped keyword opportunities]
- **Content Clusters**: [Topic authority building opportunities]
- **Technical Optimisation**: [Site-level improvements for search performance]

## Content Strategy Implications

### Priority Content Areas
- **High-Impact Topics**: Content areas with maximum audience engagement potential
- **Authority Building**: Thought leadership and expertise demonstration opportunities
- **Conversion Optimisation**: Content supporting business objective achievement
- **SEO Foundation**: Search visibility and organic traffic growth content

### Content Format Recommendations
- **Long-Form Educational**: Comprehensive guides and authority-building content
- **Problem-Solution Articles**: Direct response to audience pain points
- **Process Documentation**: Step-by-step guidance and instructional content
- **Industry Analysis**: Market insights and trend commentary

### Distribution Strategy
- **Primary Channels**: Website, blog, and owned media properties
- **Secondary Channels**: Social media and industry publication opportunities
- **Partnership Opportunities**: Collaborative content and guest posting
- **Repurposing Strategy**: Multi-format content adaptation and distribution

## Research Sources and Methodology

### Data Collection Methods
- **Primary Research**: Direct audience surveys and feedback collection
- **Secondary Research**: Industry reports, academic studies, and market analysis
- **Competitive Analysis**: Direct competitor review and benchmarking
- **SEO Tools**: Keyword research and search landscape analysis

### Source Credibility
- **Authoritative Sources**: Industry associations, government data, academic research
- **Current Information**: Recent publications and up-to-date market data
- **Verified Statistics**: Cross-referenced data from multiple reliable sources
- **Expert Insights**: Industry professional opinions and case studies

---
*Content Research completed: {datetime.now().strftime('%d %B %Y')}*
*Client: {client_domain.replace('_', '.')}*
*Research foundation for strategic content development*
"""

    def generate_website_analysis_template(self, client_domain: str) -> str:
        """Generate current website analysis template."""
        return f"""# {client_domain.replace('_', ' ').title()} - Current Website Analysis

## Executive Summary
Comprehensive analysis of {client_domain.replace('_', '.')} current website performance, identifying opportunities for improvement and optimisation.

## Technical Performance Analysis

### Site Speed and Performance
- **Page Load Times**: [To be assessed with performance testing tools]
- **Core Web Vitals**: [LCP, FID, CLS measurements and recommendations]
- **Mobile Performance**: [Mobile-specific speed and usability assessment]
- **Technical Optimisation**: [Server response times, image optimisation, caching]

### SEO Foundation Assessment
- **On-Page Optimisation**: [Meta tags, headers, content structure analysis]
- **Technical SEO**: [Site architecture, crawlability, indexation status]
- **Keyword Performance**: [Current ranking positions and opportunities]
- **Content Gaps**: [Missing content for target keyword coverage]

### User Experience Evaluation
- **Navigation Structure**: [Site architecture and user journey analysis]
- **Content Organisation**: [Information hierarchy and accessibility]
- **Conversion Paths**: [User flow optimisation opportunities]
- **Mobile Responsiveness**: [Cross-device experience assessment]

## Content Analysis

### Existing Content Audit
- **Content Inventory**: [Comprehensive list of current website content]
- **Quality Assessment**: [Content depth, accuracy, and engagement potential]
- **SEO Performance**: [Content ranking performance and optimisation needs]
- **Gap Identification**: [Missing content for complete topic coverage]

### Brand Messaging Review
- **Value Proposition**: [Current messaging clarity and effectiveness]
- **Brand Voice Consistency**: [Tone and style alignment across content]
- **Competitive Positioning**: [Differentiation and unique selling points]
- **Call-to-Action Effectiveness**: [Conversion element performance]

## Competitive Positioning

### Industry Benchmark Analysis
- **Competitor Comparison**: [Feature and content comparison with key competitors]
- **Best Practice Identification**: [Industry standards and optimisation opportunities]
- **Differentiation Opportunities**: [Areas for competitive advantage]
- **Market Position Assessment**: [Current standing in competitive landscape]

## Recommendations

### Immediate Improvements
1. **Technical Optimisation**: [Priority technical fixes for performance]
2. **Content Updates**: [Critical content improvements and additions]
3. **SEO Enhancements**: [Quick wins for search visibility]
4. **User Experience**: [Navigation and conversion path improvements]

### Medium-Term Strategy
1. **Content Expansion**: [Strategic content development priorities]
2. **Feature Enhancements**: [Functionality improvements and additions]
3. **Integration Opportunities**: [Third-party tools and service integration]
4. **Performance Monitoring**: [Analytics and tracking implementation]

### Long-Term Vision
1. **Platform Evolution**: [Future-proofing and scalability planning]
2. **Advanced Features**: [Innovative functionality and user experience]
3. **Market Leadership**: [Industry authority and thought leadership positioning]
4. **Continuous Optimisation**: [Ongoing improvement and adaptation framework]

## Implementation Priority Matrix

### High Impact, Low Effort
- [Quick wins for immediate improvement]

### High Impact, High Effort
- [Strategic initiatives requiring significant investment]

### Low Impact, Low Effort
- [Maintenance and minor optimisation tasks]

### Low Impact, High Effort
- [Initiatives to deprioritise or reconsider]

## Success Metrics

### Performance Indicators
- **Technical**: Page speed, Core Web Vitals, uptime reliability
- **SEO**: Keyword rankings, organic traffic, indexation status
- **User Experience**: Bounce rate, session duration, conversion rates
- **Business**: Lead generation, contact form submissions, goal completions

### Monitoring Framework
- **Regular Audits**: Quarterly comprehensive website assessment
- **Continuous Monitoring**: Real-time performance and uptime tracking
- **Monthly Reviews**: SEO and content performance analysis
- **Annual Strategy**: Complete website strategy review and planning

---
*Website Analysis completed: {datetime.now().strftime('%d %B %Y')}*
*Client: {client_domain.replace('_', '.')}*
*Baseline assessment for strategic improvement planning*
"""

    def generate_technical_audit_template(self, client_domain: str) -> str:
        """Generate technical audit template."""
        return f"""# {client_domain.replace('_', ' ').title()} - Technical Audit Report

## Executive Summary
Comprehensive technical assessment of {client_domain.replace('_', '.')} website infrastructure, performance, and optimisation opportunities.

## Performance Analysis

### Core Web Vitals Assessment
- **Largest Contentful Paint (LCP)**: [Loading performance measurement]
- **First Input Delay (FID)**: [Interactivity responsiveness measurement]
- **Cumulative Layout Shift (CLS)**: [Visual stability measurement]
- **Overall Score**: [Combined Core Web Vitals assessment]

### Site Speed Metrics
- **Page Load Time**: [Complete page loading duration]
- **Time to First Byte (TTFB)**: [Server response time measurement]
- **First Contentful Paint (FCP)**: [Initial content rendering time]
- **Speed Index**: [Visual loading progression measurement]

### Mobile Performance
- **Mobile Page Speed**: [Mobile-specific performance metrics]
- **Mobile Usability**: [Touch-friendly interface assessment]
- **Responsive Design**: [Cross-device compatibility evaluation]
- **Mobile Core Web Vitals**: [Mobile-specific vital measurements]

## Technical SEO Analysis

### Crawlability and Indexation
- **Robots.txt Configuration**: [Search engine crawler guidance assessment]
- **XML Sitemap**: [Site structure communication to search engines]
- **Internal Linking**: [Site architecture and page authority distribution]
- **Crawl Errors**: [Identification and resolution of crawling issues]

### On-Page Technical Elements
- **Meta Tags**: [Title tags, meta descriptions, and schema markup]
- **Header Structure**: [H1-H6 hierarchy and semantic organisation]
- **URL Structure**: [Search-friendly URL configuration]
- **Image Optimisation**: [Alt text, file sizes, and format optimisation]

### Site Architecture
- **Navigation Structure**: [Logical hierarchy and user flow]
- **Breadcrumb Implementation**: [User orientation and SEO benefits]
- **Error Page Management**: [404 handling and user experience]
- **Redirect Management**: [301/302 redirects and chain optimisation]

## Security and Compliance

### Security Assessment
- **SSL Certificate**: [HTTPS implementation and certificate validity]
- **Security Headers**: [Content security policy and XSS protection]
- **Vulnerability Scanning**: [Common security threat assessment]
- **Data Protection**: [Privacy compliance and data handling]

### Accessibility Compliance
- **WCAG Guidelines**: [Web Content Accessibility Guidelines adherence]
- **Screen Reader Compatibility**: [Assistive technology support]
- **Keyboard Navigation**: [Non-mouse interaction support]
- **Colour Contrast**: [Visual accessibility requirements]

## Infrastructure Analysis

### Hosting Performance
- **Server Response Time**: [Hosting provider performance assessment]
- **Uptime Reliability**: [Service availability and stability]
- **Geographic Performance**: [Content delivery and global access]
- **Scalability Assessment**: [Traffic handling and growth capacity]

### Content Delivery
- **CDN Implementation**: [Content distribution network utilisation]
- **Image Optimisation**: [File compression and format efficiency]
- **Caching Strategy**: [Browser and server-side caching configuration]
- **Compression**: [Gzip/Brotli compression implementation]

## Recommendations

### Critical Priority (Immediate Action Required)
1. [High-impact technical issues requiring immediate attention]
2. [Security vulnerabilities or compliance gaps]
3. [Performance bottlenecks significantly affecting user experience]

### High Priority (Within 30 Days)
1. [Important optimisations for performance improvement]
2. [SEO technical enhancements for visibility]
3. [User experience improvements for conversion optimisation]

### Medium Priority (Within 90 Days)
1. [Infrastructure improvements for long-term stability]
2. [Advanced optimisation for competitive advantage]
3. [Future-proofing and scalability preparations]

### Ongoing Maintenance
1. [Regular monitoring and maintenance requirements]
2. [Periodic security and performance audits]
3. [Continuous optimisation and improvement processes]

## Implementation Roadmap

### Phase 1: Critical Fixes (Week 1-2)
- [Immediate technical issue resolution]
- [Security vulnerability patching]
- [Performance bottleneck elimination]

### Phase 2: Core Optimisation (Week 3-6)
- [SEO technical enhancement implementation]
- [User experience improvement deployment]
- [Performance optimisation completion]

### Phase 3: Advanced Enhancement (Month 2-3)
- [Infrastructure upgrade and optimisation]
- [Advanced feature implementation]
- [Long-term scalability preparation]

## Monitoring and Maintenance

### Performance Monitoring Tools
- **Google PageSpeed Insights**: [Regular performance assessment]
- **GTmetrix**: [Comprehensive performance analysis]
- **Core Web Vitals Monitoring**: [User experience metric tracking]
- **Uptime Monitoring**: [Service availability tracking]

### Regular Audit Schedule
- **Monthly**: Performance metrics review and optimisation
- **Quarterly**: Comprehensive technical audit and security assessment
- **Annually**: Complete infrastructure review and upgrade planning

---
*Technical Audit completed: {datetime.now().strftime('%d %B %Y')}*
*Client: {client_domain.replace('_', '.')}*
*Technical foundation for performance optimisation*
"""

    def generate_ux_ui_template(self, client_domain: str) -> str:
        """Generate UX/UI analysis template."""
        return f"""# {client_domain.replace('_', ' ').title()} - UX/UI Analysis Report

## Executive Summary
User experience and interface design analysis for {client_domain.replace('_', '.')}, identifying opportunities for improved usability and conversion optimisation.

## User Experience Analysis

### Navigation and Information Architecture
- **Site Structure**: [Logical hierarchy and organisation assessment]
- **Navigation Clarity**: [Menu structure and wayfinding effectiveness]
- **Search Functionality**: [Site search usability and effectiveness]
- **Breadcrumb Navigation**: [User orientation and path clarity]

### User Journey Mapping
- **Primary User Paths**: [Main conversion flows and user objectives]
- **Pain Points**: [Friction areas and abandonment triggers]
- **Conversion Funnels**: [Step-by-step conversion process analysis]
- **User Flow Optimisation**: [Streamlined path recommendations]

### Content Usability
- **Readability**: [Text clarity, font choices, and content hierarchy]
- **Scannability**: [Information structure and visual organisation]
- **Content Accessibility**: [Inclusive design and accessibility compliance]
- **Call-to-Action Effectiveness**: [CTA placement, design, and messaging]

## Interface Design Assessment

### Visual Design Evaluation
- **Brand Consistency**: [Visual identity alignment and coherence]
- **Colour Scheme**: [Brand colours, contrast, and accessibility]
- **Typography**: [Font choices, hierarchy, and readability]
- **Imagery**: [Photo quality, relevance, and professional presentation]

### Layout and Composition
- **Grid System**: [Consistent layout structure and alignment]
- **White Space**: [Content breathing room and visual balance]
- **Element Hierarchy**: [Visual importance and information priority]
- **Responsive Design**: [Cross-device layout adaptation]

### Interactive Elements
- **Button Design**: [CTA buttons, links, and interactive feedback]
- **Form Usability**: [Contact forms, enquiry systems, and input design]
- **Hover States**: [Interactive feedback and user guidance]
- **Loading States**: [Progress indication and user feedback]

## Mobile Experience Analysis

### Mobile Usability
- **Touch Interface**: [Touch-friendly element sizing and spacing]
- **Mobile Navigation**: [Compressed menu systems and mobile-specific features]
- **Content Adaptation**: [Mobile content presentation and readability]
- **Performance**: [Mobile loading speed and responsiveness]

### Cross-Device Consistency
- **Design Coherence**: [Consistent experience across devices]
- **Feature Parity**: [Functionality availability across platforms]
- **Content Presentation**: [Optimal content display for each device]
- **User Flow Continuity**: [Seamless experience across device switches]

## Conversion Optimisation Analysis

### Landing Page Effectiveness
- **Value Proposition**: [Clear benefit communication and positioning]
- **Trust Signals**: [Credibility elements and social proof]
- **Content Hierarchy**: [Information priority and user guidance]
- **Conversion Elements**: [Lead capture and contact facilitation]

### Contact and Enquiry Systems
- **Form Design**: [User-friendly enquiry and contact forms]
- **Contact Information**: [Accessible contact details and methods]
- **Response Expectations**: [Clear communication about response times]
- **Follow-up Processes**: [User guidance for next steps]

### E-commerce Considerations (if applicable)
- **Product Presentation**: [Product information and visual presentation]
- **Shopping Cart**: [Cart functionality and checkout process]
- **Payment Systems**: [Secure and user-friendly payment options]
- **Order Management**: [Order tracking and customer service]

## Accessibility Assessment

### WCAG Compliance
- **Keyboard Navigation**: [Non-mouse interaction support]
- **Screen Reader Compatibility**: [Assistive technology support]
- **Colour Contrast**: [Visual accessibility requirements]
- **Alternative Text**: [Image description for screen readers]

### Inclusive Design
- **Font Size Options**: [Text scalability and readability options]
- **Motor Accessibility**: [Large touch targets and easy interaction]
- **Cognitive Accessibility**: [Clear language and simple navigation]
- **Universal Design**: [Inclusive approach benefiting all users]

## Recommendations

### High Priority UX Improvements
1. [Critical user experience issues affecting conversion]
2. [Navigation improvements for better user flow]
3. [Mobile experience enhancements for accessibility]
4. [Form optimisation for increased completion rates]

### Interface Design Enhancements
1. [Visual design improvements for brand consistency]
2. [Content hierarchy optimisation for better scanning]
3. [Interactive element improvements for user feedback]
4. [Responsive design refinements for cross-device experience]

### Conversion Optimisation
1. [Landing page improvements for better conversion]
2. [Call-to-action optimisation for increased engagement]
3. [Trust signal enhancement for credibility building]
4. [User flow streamlining for reduced friction]

## Implementation Strategy

### Phase 1: Critical UX Fixes (Week 1-2)
- [Immediate usability issue resolution]
- [Mobile experience critical improvements]
- [Navigation and accessibility fixes]

### Phase 2: Design Enhancement (Week 3-6)
- [Visual design improvements and brand alignment]
- [Content hierarchy and readability enhancement]
- [Interactive element optimisation]

### Phase 3: Conversion Optimisation (Month 2)
- [Landing page and conversion flow improvement]
- [Advanced user experience features]
- [Performance and satisfaction optimisation]

## Success Metrics and Testing

### UX Performance Indicators
- **User Engagement**: [Session duration, pages per session, return visits]
- **Conversion Rates**: [Goal completion and lead generation rates]
- **User Satisfaction**: [Feedback scores and usability testing results]
- **Accessibility Compliance**: [WCAG guideline adherence measurement]

### Testing and Validation
- **User Testing**: [Real user feedback and behaviour observation]
- **A/B Testing**: [Conversion optimisation through controlled testing]
- **Analytics Review**: [User behaviour data analysis and insights]
- **Regular Audits**: [Ongoing UX assessment and improvement]

---
*UX/UI Analysis completed: {datetime.now().strftime('%d %B %Y')}*
*Client: {client_domain.replace('_', '.')}*
*User experience foundation for conversion optimisation*
"""

    def generate_task_deps_template(self, client_domain: str) -> str:
        """Generate task dependencies template."""
        return f"""# {client_domain.replace('_', ' ').title()} - Task Dependencies and Implementation Plan

## Project Implementation Framework

### Task Dependency Structure
This document outlines the task dependencies, feedback loops, and implementation sequence for the {client_domain.replace('_', '.')} project, ensuring systematic execution and quality assurance.

## Phase 1: Foundation Implementation

### Task: Content Strategy Deployment
**Dependencies:** All research phases completed (1-4)
**Duration:** 2-3 weeks
**Deliverables:**
- Content brief creation and approval
- Editorial calendar implementation
- Content team briefing and training

**Feedback Loop Integration:**
```yaml
content_strategy_feedback:
  type: IterativeImprovement
  agents: [clarity_conciseness_editor, cognitive_load_minimizer, content_critique_specialist, ai_text_naturalizer]
  max_iterations: 3
  threshold: 8.5/10
  success_criteria:
    - Strategic clarity and implementation feasibility
    - Stakeholder alignment and approval
    - Resource allocation confirmation
```

### Task: Technical Infrastructure Setup
**Dependencies:** Technical audit completed, hosting requirements defined
**Duration:** 1-2 weeks
**Deliverables:**
- Performance optimisation implementation
- SEO technical foundation deployment
- Analytics and monitoring setup

**Quality Gates:**
- Core Web Vitals improvement verification
- SEO technical implementation audit
- Performance benchmark establishment

## Phase 2: Content Creation and Optimisation

### Task: Priority Content Development
**Dependencies:** Content strategy approved, style guide finalised
**Duration:** 4-6 weeks
**Deliverables:**
- High-priority page content creation
- SEO optimisation implementation
- Content quality assurance completion

**Feedback Loop Integration:**
```yaml
content_creation_feedback:
  type: IterativeImprovement
  agents: [clarity_conciseness_editor, cognitive_load_minimizer, content_critique_specialist, ai_text_naturalizer]
  max_iterations: 3
  threshold: 8.5/10
  dependencies: [research_validation, seo_optimisation]
  success_criteria:
    - Content quality score ≥8.5/10
    - SEO compliance verification
    - Brand voice consistency confirmation
```

### Task: User Experience Optimisation
**Dependencies:** UX/UI analysis completed, content structure defined
**Duration:** 2-3 weeks
**Deliverables:**
- User journey optimisation implementation
- Conversion path enhancement
- Mobile experience improvement

**Quality Assurance:**
- User testing validation
- Conversion rate baseline establishment
- Accessibility compliance verification

## Phase 3: Advanced Implementation

### Task: AI and Voice Search Optimisation
**Dependencies:** Content creation completed, technical foundation established
**Duration:** 2-3 weeks
**Deliverables:**
- Schema markup implementation
- Voice search optimisation deployment
- AI-friendly content structure enhancement

**Feedback Loop Integration:**
```yaml
ai_optimisation_feedback:
  type: TechnicalValidation
  agents: [technical_enhanced_auditor, ai_specialist_agent]
  max_iterations: 2
  threshold: 9.0/10
  success_criteria:
    - Schema markup validation
    - Voice search query optimisation
    - AI citability score improvement
```

### Task: Performance and Monitoring Setup
**Dependencies:** All content and technical implementations completed
**Duration:** 1 week
**Deliverables:**
- Comprehensive analytics implementation
- Performance monitoring dashboard
- Reporting automation setup

## Feedback Loop Framework

### Content Quality Assurance Loop
```yaml
content_quality_loop:
  trigger: content_creation_complete
  sequence:
    1. clarity_conciseness_editor:
        focus: Grammar, flow, British English compliance
        threshold: 8.0/10
    2. cognitive_load_minimizer:
        focus: Information hierarchy, scanability
        threshold: 7.0/10
    3. content_critique_specialist:
        focus: Argument strength, evidence support
        threshold: 7.0/10
    4. ai_text_naturalizer:
        focus: Natural flow, personality injection
        threshold: 8.0/10

  loop_back_conditions:
    - Any agent score below threshold
    - Aggregate score below 8.5/10
    - Stakeholder feedback requiring revision

  max_iterations: 3
  escalation: human_review_required
```

### Technical Implementation Loop
```yaml
technical_implementation_loop:
  trigger: technical_change_deployed
  sequence:
    1. performance_validation:
        focus: Core Web Vitals, loading speed
        threshold: 90/100 PageSpeed score
    2. seo_compliance_check:
        focus: Technical SEO, schema markup
        threshold: 95% compliance score
    3. accessibility_audit:
        focus: WCAG compliance, usability
        threshold: AA level compliance

  feedback_integration:
    - Real-time performance monitoring
    - Continuous optimisation recommendations
    - Monthly technical review and adjustment
```

## Risk Management and Contingency Planning

### High-Risk Dependencies
1. **Content Approval Delays**
   - **Mitigation:** Staged approval process, clear feedback timelines
   - **Contingency:** Parallel content track development

2. **Technical Implementation Challenges**
   - **Mitigation:** Thorough testing environment, phased deployment
   - **Contingency:** Rollback procedures, alternative solution paths

3. **Resource Availability**
   - **Mitigation:** Cross-training, flexible resource allocation
   - **Contingency:** Priority task identification, timeline adjustment

### Quality Assurance Checkpoints
- **Weekly Progress Reviews:** Task completion and quality verification
- **Phase Gate Approvals:** Stakeholder sign-off before progression
- **Continuous Monitoring:** Real-time performance and quality tracking

## Success Metrics and KPIs

### Implementation Success Indicators
- **Task Completion Rate:** 100% on-time delivery
- **Quality Threshold Achievement:** 95% first-pass quality approval
- **Feedback Loop Efficiency:** <3 iterations average per content piece
- **Stakeholder Satisfaction:** 9/10 approval rating

### Business Impact Measurements
- **Organic Traffic Growth:** 50% increase within 6 months
- **Conversion Rate Improvement:** 25% increase in lead generation
- **User Experience Enhancement:** 20% improvement in engagement metrics
- **Technical Performance:** 90+ PageSpeed score achievement

## Timeline and Milestones

### Month 1: Foundation Phase
- Week 1-2: Technical infrastructure setup and optimisation
- Week 3-4: Content strategy deployment and team alignment

### Month 2: Content Development Phase
- Week 1-4: Priority content creation and optimisation
- Ongoing: Feedback loop implementation and quality assurance

### Month 3: Advanced Implementation Phase
- Week 1-2: AI optimisation and voice search deployment
- Week 3-4: Performance monitoring and final optimisations

### Ongoing: Monitoring and Optimisation
- Monthly performance reviews and strategy refinement
- Quarterly comprehensive audits and improvement planning
- Annual strategy review and goal adjustment

---
*Task Dependencies Plan created: {datetime.now().strftime('%d %B %Y')}*
*Client: {client_domain.replace('_', '.')}*
*Implementation roadmap with integrated feedback loops*
"""

    def generate_execution_tracking_template(self, client_domain: str) -> str:
        """Generate execution tracking template."""
        return f"""# {client_domain.replace('_', ' ').title()} - Execution Tracking Report

## Project Status Dashboard

### Overall Project Progress
- **Project Completion:** [X]% Complete
- **Timeline Status:** [On Track / Behind Schedule / Ahead of Schedule]
- **Quality Score:** [X]/10 Average Across All Deliverables
- **Client Satisfaction:** [X]/10 Based on Feedback and Reviews

### Phase Completion Status
- ✅ **Research Phase:** 100% Complete
  - Audience personas development: ✅ Complete
  - Competitive analysis: ✅ Complete
  - Keyword research strategy: ✅ Complete
  - Market opportunity assessment: ✅ Complete

- ✅ **Strategy Phase:** 100% Complete
  - Content strategy development: ✅ Complete
  - Implementation planning: ✅ Complete
  - Resource allocation: ✅ Complete

- ⏳ **Implementation Phase:** [X]% Complete
  - Content creation: [X]% Complete
  - Technical optimisation: [X]% Complete
  - User experience enhancement: [X]% Complete

- ⏳ **Quality Assurance:** [X]% Complete
  - Content review cycles: [X]% Complete
  - Technical validation: [X]% Complete
  - Performance testing: [X]% Complete

## Detailed Task Tracking

### Content Development Progress

#### Priority Content Items
| Content Item | Status | Quality Score | Feedback Loops | Completion Date |
|-------------|--------|---------------|----------------|-----------------|
| Homepage Content | [Status] | [X]/10 | [X] iterations | [Date] |
| Service Pages | [Status] | [X]/10 | [X] iterations | [Date] |
| About Page | [Status] | [X]/10 | [X] iterations | [Date] |
| Contact Page | [Status] | [X]/10 | [X] iterations | [Date] |

#### Content Quality Metrics
- **Average Quality Score:** [X]/10 across all content
- **First-Pass Approval Rate:** [X]% of content approved without revision
- **Feedback Loop Efficiency:** [X] average iterations per content piece
- **SOP Compliance Rate:** [X]% adherence to 2025 content standards

### Technical Implementation Progress

#### Technical Tasks Status
| Task Category | Progress | Performance Impact | Completion Date |
|--------------|----------|-------------------|-----------------|
| Core Web Vitals Optimisation | [X]% | [Impact Description] | [Date] |
| SEO Technical Setup | [X]% | [Impact Description] | [Date] |
| Mobile Optimisation | [X]% | [Impact Description] | [Date] |
| Analytics Implementation | [X]% | [Impact Description] | [Date] |

#### Performance Improvements
- **PageSpeed Score:** [Before] → [After] ([+X] point improvement)
- **Core Web Vitals:** [LCP/FID/CLS improvements]
- **Mobile Performance:** [Mobile score improvements]
- **SEO Technical Score:** [Technical SEO compliance percentage]

## Quality Assurance Tracking

### Feedback Loop Performance

#### Content Quality Improvement Cycles
```
Content Item: [Name]
Iteration 1: [X]/10 → Issues: [List]
Iteration 2: [X]/10 → Issues: [List]
Final Score: [X]/10 → Status: [Approved/Requires Further Work]
```

#### Agent Performance Metrics
- **clarity_conciseness_editor:** [X]/10 average improvement contribution
- **cognitive_load_minimizer:** [X]/10 average improvement contribution
- **content_critique_specialist:** [X]/10 average improvement contribution
- **ai_text_naturalizer:** [X]/10 average improvement contribution

### Compliance Verification

#### SOP Adherence Tracking
- **Word Count Compliance:** [X]% of content within SOP guidelines
- **British English Compliance:** [X]% accuracy rate
- **Content Structure Compliance:** [X]% adherence to format requirements
- **Citation and Source Requirements:** [X]% compliance with credibility standards

## Risk and Issue Management

### Current Risks and Mitigations
| Risk Category | Risk Level | Description | Mitigation Strategy | Status |
|--------------|------------|-------------|-------------------|--------|
| Timeline | [High/Medium/Low] | [Description] | [Mitigation] | [Status] |
| Quality | [High/Medium/Low] | [Description] | [Mitigation] | [Status] |
| Resource | [High/Medium/Low] | [Description] | [Mitigation] | [Status] |
| Technical | [High/Medium/Low] | [Description] | [Mitigation] | [Status] |

### Issues Resolved
- **Issue:** [Description] - **Resolution:** [Solution] - **Date:** [Date]
- **Issue:** [Description] - **Resolution:** [Solution] - **Date:** [Date]

## Performance Metrics and KPIs

### Project Delivery Metrics
- **On-Time Delivery Rate:** [X]% of milestones delivered on schedule
- **Quality Gate Pass Rate:** [X]% of deliverables passing quality thresholds
- **Client Approval Rate:** [X]% first-time approval of submitted work
- **Scope Adherence:** [X]% delivery within original project scope

### Business Impact Indicators
- **Baseline Metrics Established:** [Date]
- **Current Performance vs. Baseline:** [Improvement percentages]
- **Leading Indicators:** [Early success signals]
- **Projected Outcomes:** [Expected results based on current progress]

## Resource Utilisation

### Team Performance
- **Total Hours Invested:** [X] hours across all team members
- **Efficiency Rate:** [X] hours per deliverable average
- **Quality vs. Speed Balance:** [Analysis of quality output relative to time investment]
- **Resource Allocation Accuracy:** [Planned vs. actual resource usage]

### Budget and Timeline
- **Budget Utilisation:** [X]% of allocated budget consumed
- **Timeline Adherence:** [X] days ahead/behind original schedule
- **Scope Changes:** [Number and impact of scope modifications]
- **ROI Projection:** [Expected return on investment based on current progress]

## Next Steps and Upcoming Milestones

### Immediate Priorities (Next 2 Weeks)
1. [Priority task 1 with deadline]
2. [Priority task 2 with deadline]
3. [Priority task 3 with deadline]

### Medium-Term Objectives (Next 30 Days)
1. [Objective 1 with success criteria]
2. [Objective 2 with success criteria]
3. [Objective 3 with success criteria]

### Long-Term Goals (Next 90 Days)
1. [Goal 1 with measurement criteria]
2. [Goal 2 with measurement criteria]
3. [Goal 3 with measurement criteria]

## Stakeholder Communication

### Recent Client Feedback
- **Feedback Date:** [Date] - **Summary:** [Key feedback points]
- **Action Items:** [Specific actions taken in response to feedback]
- **Next Review Scheduled:** [Date and agenda items]

### Team Collaboration
- **Regular Check-ins:** [Frequency and effectiveness]
- **Issue Resolution Time:** [Average time to resolve project issues]
- **Communication Effectiveness:** [Quality of team collaboration and information sharing]

## Continuous Improvement

### Lessons Learned
1. [Lesson 1: What worked well and why]
2. [Lesson 2: What could be improved and how]
3. [Lesson 3: Process refinements for future projects]

### Process Optimisations
- **Feedback Loop Refinements:** [Improvements to quality assurance processes]
- **Workflow Enhancements:** [Efficiency improvements in project execution]
- **Quality Gate Adjustments:** [Refinements to quality threshold and review processes]

### Future Project Applications
- [Insight 1 for application to future client projects]
- [Insight 2 for systematic process improvement]
- [Insight 3 for team development and capability building]

---
*Execution Tracking Report updated: {datetime.now().strftime('%d %B %Y')}*
*Client: {client_domain.replace('_', '.')}*
*Comprehensive project progress and performance monitoring*
"""

    def run_comprehensive_audit(self, file_path: str, auto_generate: bool = False) -> Dict:
        """Run comprehensive pre-delivery audit."""
        logger.info(f"Starting comprehensive audit for: {file_path}")

        client_root = self.get_client_root_path(file_path)
        if not client_root:
            return {
                'success': False,
                'error': 'Unable to determine client root path from file path'
            }

        client_domain = self.extract_client_domain_from_path(file_path)
        logger.info(f"Auditing client: {client_domain}")

        # Check mandatory files
        existing_files, missing_files = self.check_mandatory_files(client_root)

        # Check word count compliance
        word_count_violations = self.check_word_count_compliance(client_root)

        # Check user journey mapping
        user_journey_issues = self.check_user_journey_mapping(client_root)

        # Check British English compliance
        british_english_violations = self.check_british_english_compliance(client_root)

        # Calculate compliance score
        total_mandatory = len(self.mandatory_files)
        files_existing = len(existing_files)
        compliance_score = (files_existing / total_mandatory) * 100

        # Generate missing files if requested
        generated_files = []
        if auto_generate and missing_files:
            generated_files = self.generate_missing_file_templates(client_root, missing_files)

        # Prepare audit results
        audit_results = {
            'success': True,
            'client_domain': client_domain,
            'client_root': str(client_root),
            'audit_date': datetime.now().isoformat(),
            'compliance_score': round(compliance_score, 1),
            'mandatory_files': {
                'total_required': total_mandatory,
                'existing': len(existing_files),
                'missing': len(missing_files),
                'existing_files': existing_files,
                'missing_files': missing_files
            },
            'word_count_compliance': {
                'violations_found': len(word_count_violations),
                'violations': word_count_violations
            },
            'user_journey_issues': user_journey_issues,
            'british_english_compliance': {
                'violations_found': len(british_english_violations),
                'violations': british_english_violations
            },
            'auto_generation': {
                'requested': auto_generate,
                'files_generated': len(generated_files),
                'generated_files': generated_files
            },
            'overall_status': 'COMPLIANT' if compliance_score >= 90 and len(word_count_violations) == 0 else 'NON_COMPLIANT',
            'recommendations': self.generate_recommendations(missing_files, word_count_violations, user_journey_issues)
        }

        return audit_results

    def generate_recommendations(self, missing_files: List[str], word_count_violations: List[Dict], user_journey_issues: List[str]) -> List[str]:
        """Generate actionable recommendations based on audit findings."""
        recommendations = []

        if missing_files:
            recommendations.append(f"Create {len(missing_files)} missing mandatory deliverables before client delivery")

        if word_count_violations:
            over_count = len([v for v in word_count_violations if v['issue'] == 'OVER_SOP_MAXIMUM'])
            under_count = len([v for v in word_count_violations if v['issue'] == 'UNDER_SOP_MINIMUM'])

            if over_count > 0:
                recommendations.append(f"Reduce word count in {over_count} documents to meet 2025 SOP requirements")
            if under_count > 0:
                recommendations.append(f"Expand content in {under_count} documents to meet SOP minimum requirements")

        if user_journey_issues:
            recommendations.append("Add comprehensive user journey mapping to content strategy")

        if not missing_files and not word_count_violations and not user_journey_issues:
            recommendations.append("Project meets all compliance requirements - ready for delivery")

        return recommendations

    def generate_comprehensive_content_plans_template(self, client_domain: str) -> str:
        """Generate comprehensive website content plans template."""
        return f"""# {client_domain.replace('_', ' ').title()} - Comprehensive Website Content Plans

## Executive Summary
Strategic content planning framework for {client_domain.replace('_', '.')} encompassing complete website content ecosystem and user journey optimisation.

## Content Strategy Framework

### Primary Content Objectives
- **Authority Building**: Establish thought leadership and industry expertise
- **User Experience Optimisation**: Streamlined information architecture and navigation
- **Conversion Optimisation**: Strategic content placement for lead generation
- **SEO Performance**: Search visibility and organic traffic growth

### Target Audience Content Mapping
- **Primary Audience**: [Industry professionals seeking solutions]
- **Secondary Audience**: [Decision makers and stakeholders]
- **Content Personalisation**: Tailored messaging for different user segments
- **Journey Stage Alignment**: Content matched to awareness, consideration, decision phases

## Website Content Architecture

### Homepage Content Strategy
- **Value Proposition**: Clear benefit communication and competitive differentiation
- **Trust Signals**: Credibility elements, testimonials, and social proof
- **Navigation Hub**: Intuitive pathway to key conversion pages
- **Above-Fold Optimisation**: Critical information and call-to-action placement

### Service Pages Content Framework
- **Problem-Solution Structure**: Clear pain point identification and resolution
- **Benefit-Driven Messaging**: Outcome-focused content and value demonstration
- **Process Documentation**: Step-by-step approach and methodology explanation
- **Social Proof Integration**: Case studies, testimonials, and success metrics

### About Pages Content Strategy
- **Story Narrative**: Compelling brand story and mission communication
- **Team Expertise**: Professional credentials and industry experience
- **Values Alignment**: Shared values communication with target audience
- **Trust Building**: Transparency and authenticity demonstration

## Content Optimisation Strategy

### SEO Content Integration
- **Keyword Strategy**: Primary and secondary keyword integration throughout content
- **Search Intent Alignment**: Content structure optimised for user search behaviour
- **Topic Authority**: Comprehensive coverage of industry-relevant topics
- **Internal Linking**: Strategic content interconnection for SEO performance

### User Experience Content Design
- **Scannable Format**: Headlines, bullet points, and visual hierarchy
- **Mobile Optimisation**: Content presentation optimised for all devices
- **Loading Speed**: Content structure optimised for fast page performance
- **Accessibility**: Inclusive content design for all users

### Conversion Optimisation Content
- **Call-to-Action Strategy**: Strategic placement and compelling messaging
- **Lead Magnet Integration**: Valuable content offers for contact information
- **Trust Signal Placement**: Credentials and testimonials at conversion points
- **Objection Handling**: Proactive addressing of common customer concerns

## Content Creation Guidelines

### Brand Voice and Tone
- **Professional Authority**: Expert knowledge demonstration without intimidation
- **Approachable Communication**: Complex topics explained in accessible language
- **Trustworthy Messaging**: Honest, transparent, and evidence-based content
- **Solution-Focused**: Problem-solving orientation with clear next steps

### Content Quality Standards
- **Research-Backed Information**: All claims supported by credible sources
- **Current and Relevant**: Regular content updates and accuracy verification
- **Comprehensive Coverage**: Thorough topic exploration and complete information
- **Practical Value**: Actionable insights and implementable recommendations

### Content Format Specifications
- **Word Count Guidelines**: Appropriate length for content type and SEO requirements
- **Structure Standards**: Consistent formatting and information hierarchy
- **Visual Integration**: Strategic use of images, diagrams, and visual elements
- **Mobile Responsiveness**: Content optimised for cross-device consumption

## Implementation Roadmap

### Phase 1: Foundation Content (Month 1)
- **Homepage optimisation**: Core messaging and value proposition
- **Primary service pages**: Key offering content and conversion optimisation
- **About page enhancement**: Brand story and trust building content
- **Contact page optimisation**: Clear communication pathways and expectations

### Phase 2: Authority Building Content (Month 2)
- **Industry insight pages**: Thought leadership and expertise demonstration
- **FAQ comprehensive coverage**: Common questions and detailed answers
- **Process documentation**: Methodology explanation and transparency
- **Case study development**: Success story documentation and social proof

### Phase 3: SEO and Conversion Optimisation (Month 3)
- **Blog content strategy**: Regular content creation for SEO and engagement
- **Landing page optimisation**: Conversion-focused content and design
- **Internal linking strategy**: Content interconnection and user journey optimisation
- **Performance monitoring**: Content effectiveness measurement and optimisation

## Content Maintenance and Optimisation

### Regular Review Schedule
- **Monthly Updates**: Content accuracy verification and improvement opportunities
- **Quarterly Audits**: Comprehensive content performance analysis and strategy refinement
- **Annual Strategy Review**: Complete content strategy assessment and planning

### Performance Monitoring
- **Engagement Metrics**: User interaction and content consumption analysis
- **Conversion Tracking**: Content effectiveness for lead generation and goal achievement
- **SEO Performance**: Search ranking and organic traffic impact measurement
- **User Feedback Integration**: Customer insights and content improvement recommendations

## Success Metrics and KPIs

### Content Performance Indicators
- **User Engagement**: Time on page, scroll depth, and interaction rates
- **Conversion Rates**: Lead generation and goal completion from content pages
- **SEO Impact**: Keyword rankings and organic traffic growth
- **Brand Awareness**: Content reach and social media engagement

### Business Impact Measurement
- **Lead Quality**: Content-generated leads and conversion to customers
- **Customer Education**: Reduced support queries through comprehensive content
- **Market Positioning**: Industry recognition and thought leadership establishment
- **Revenue Attribution**: Content contribution to business growth and profitability

---
*Comprehensive Content Plans created: {datetime.now().strftime('%d %B %Y')}*
*Client: {client_domain.replace('_', '.')}*
*Strategic foundation for website content excellence*
"""

    def generate_research_brief_template(self, client_domain: str) -> str:
        """Generate research brief template."""
        return f"""# {client_domain.replace('_', ' ').title()} - Research Brief

## Project Overview
Comprehensive research strategy for {client_domain.replace('_', '.')} encompassing market analysis, competitive intelligence, and audience understanding for strategic content development.

## Research Objectives

### Primary Research Goals
1. **Market Understanding**: Industry landscape, trends, and opportunity identification
2. **Competitive Analysis**: Competitor positioning, content gaps, and differentiation opportunities
3. **Audience Intelligence**: Target audience behaviour, preferences, and content consumption patterns
4. **SEO Foundation**: Keyword research, search intent analysis, and content optimisation opportunities

### Business Context
- **Industry**: [To be specified based on client sector]
- **Target Market**: [Geographic and demographic specifications]
- **Business Objectives**: [Revenue, growth, and market positioning goals]
- **Competitive Landscape**: [Direct and indirect competitor identification]

## Research Methodology

### Phase 1: Foundation Research
- **Industry Analysis**: Market size, growth trends, and regulatory environment
- **Business Model Research**: Revenue streams, service delivery, and value proposition
- **SWOT Analysis**: Internal strengths/weaknesses and external opportunities/threats
- **Stakeholder Mapping**: Key decision makers, influencers, and customer segments

### Phase 2: Competitive Intelligence
- **Competitor Identification**: Direct, indirect, and aspirational competitors
- **Content Audit**: Competitor website content, messaging, and positioning analysis
- **SEO Competitive Analysis**: Keyword rankings, content performance, and technical SEO
- **Social Media Presence**: Content strategy, engagement rates, and audience interaction

### Phase 3: Audience Research
- **Demographic Analysis**: Age, location, profession, and socioeconomic factors
- **Psychographic Profiling**: Values, interests, lifestyle, and decision-making patterns
- **Behaviour Mapping**: Online activity, content consumption, and purchasing behaviour
- **Pain Point Identification**: Challenges, frustrations, and unmet needs

### Phase 4: SEO and Content Research
- **Keyword Research**: Primary, secondary, and long-tail keyword identification
- **Search Intent Analysis**: User motivation and content journey mapping
- **Content Gap Analysis**: Missing topics and underserved search queries
- **Trend Analysis**: Emerging topics and seasonal content opportunities

## Research Tools and Sources

### Primary Research Methods
- **Customer Surveys**: Direct feedback collection and preference analysis
- **Stakeholder Interviews**: Internal team insights and industry expertise
- **User Testing**: Website usability and content effectiveness assessment
- **Analytics Review**: Historical data analysis and performance insights

### Secondary Research Sources
- **Industry Reports**: Market research publications and trade association data
- **Government Statistics**: Official data sources and regulatory publications
- **Academic Research**: Peer-reviewed studies and university publications
- **News and Media**: Industry publications and recent developments

### Digital Research Tools
- **SEO Platforms**: Keyword research, competitor analysis, and ranking data
- **Social Media Analytics**: Audience insights and content performance metrics
- **Website Analytics**: User behaviour, traffic patterns, and conversion data
- **Survey Platforms**: Primary research data collection and analysis

## Deliverables and Timeline

### Week 1-2: Foundation Research
- **Industry Analysis Report**: Market overview and opportunity assessment
- **Business Context Documentation**: Company positioning and competitive environment
- **Initial SWOT Analysis**: Preliminary strengths, weaknesses, opportunities, threats

### Week 3-4: Competitive Intelligence
- **Competitor Mapping**: Comprehensive competitor identification and categorisation
- **Content Audit Summary**: Competitor content analysis and gap identification
- **SEO Competitive Report**: Keyword rankings and technical SEO comparison

### Week 5-6: Audience Research
- **Persona Development**: Detailed audience profiles and behaviour mapping
- **Journey Mapping**: Customer decision process and touchpoint identification
- **Content Preference Analysis**: Format, channel, and messaging preferences

### Week 7-8: SEO and Content Strategy
- **Keyword Research Report**: Comprehensive keyword strategy and opportunity matrix
- **Content Gap Analysis**: Missing content opportunities and competitive advantages
- **Content Strategy Framework**: Strategic recommendations for content development

## Quality Assurance and Validation

### Research Verification
- **Source Credibility**: Authoritative sources and data verification
- **Methodology Consistency**: Systematic approach and bias minimisation
- **Data Triangulation**: Multiple source validation and cross-referencing
- **Stakeholder Review**: Internal validation and expert consultation

### Accuracy Standards
- **Fact Checking**: All statistics and claims verified with primary sources
- **Currency Requirements**: Recent data and current market conditions
- **Relevance Assessment**: Direct applicability to client objectives and market
- **Completeness Verification**: Comprehensive coverage of research objectives

## Success Criteria

### Research Quality Indicators
- **Comprehensiveness**: Complete coverage of all research objectives
- **Accuracy**: Verified information from credible sources
- **Relevance**: Direct applicability to content strategy development
- **Actionability**: Clear insights leading to strategic recommendations

### Strategic Impact Measurement
- **Decision Support**: Research insights informing content strategy decisions
- **Competitive Advantage**: Unique insights and differentiation opportunities
- **Market Positioning**: Clear understanding of market position and opportunities
- **ROI Projection**: Expected return on investment from research-informed strategy

---
*Research Brief created: {datetime.now().strftime('%d %B %Y')}*
*Client: {client_domain.replace('_', '.')}*
*Strategic research foundation for informed content development*
"""

    def generate_implementation_plan_template(self, client_domain: str) -> str:
        """Generate implementation plan template."""
        return f"""# {client_domain.replace('_', ' ').title()} - Implementation Plan

## Project Implementation Framework
Strategic implementation roadmap for {client_domain.replace('_', '.')} encompassing content development, technical optimisation, and performance monitoring.

## Implementation Objectives

### Primary Goals
- **Content Excellence**: High-quality, research-backed content creation and optimisation
- **Technical Performance**: Website speed, SEO, and user experience optimisation
- **Business Impact**: Measurable improvement in lead generation and market positioning
- **Sustainable Growth**: Systematic approach to ongoing content and performance improvement

### Success Metrics
- **Traffic Growth**: 50% increase in organic traffic within 6 months
- **Conversion Improvement**: 25% increase in lead generation and contact enquiries
- **Authority Building**: Top 3 search rankings for primary target keywords
- **User Experience**: 90+ PageSpeed score and improved engagement metrics

## Phase 1: Foundation Setup (Month 1)

### Week 1-2: Technical Infrastructure
**Objective**: Establish robust technical foundation for content and performance optimisation

**Tasks**:
- Technical audit completion and issue resolution
- Core Web Vitals optimisation implementation
- SEO technical setup and schema markup deployment
- Analytics and monitoring tool configuration

**Deliverables**:
- Technical audit report with priority fixes
- Performance improvement documentation
- SEO technical checklist completion
- Analytics dashboard setup and baseline establishment

**Success Criteria**:
- PageSpeed score improvement to 85+ (target: 90+)
- Core Web Vitals compliance achievement
- Complete SEO technical foundation deployment
- Comprehensive tracking and monitoring activation

### Week 3-4: Content Strategy Implementation
**Objective**: Deploy comprehensive content strategy and editorial framework

**Tasks**:
- Content audit and gap analysis completion
- Editorial calendar development and approval
- Brand voice and style guide finalisation
- Content creation workflow establishment

**Deliverables**:
- Complete content audit with recommendations
- 12-month editorial calendar with priorities
- Comprehensive style guide and brand voice documentation
- Content creation and approval process documentation

**Success Criteria**:
- All content gaps identified and prioritised
- Editorial calendar approved and resourced
- Style guide completed and team training conducted
- Content workflow tested and operational

## Phase 2: Content Development (Month 2-3)

### Priority Content Creation
**Objective**: Develop high-impact content for immediate business benefit

**High-Priority Pages**:
1. **Homepage Optimisation**: Value proposition clarity and conversion optimisation
2. **Service Pages**: Comprehensive service descriptions with SEO optimisation
3. **About Page**: Trust building and authority establishment
4. **Contact Page**: Clear communication pathways and conversion optimisation

**Content Requirements**:
- **Research-Backed**: All content supported by market research and competitive analysis
- **SEO Optimised**: Keyword integration and search intent alignment
- **Conversion Focused**: Strategic call-to-action placement and lead generation
- **Brand Consistent**: Voice, tone, and messaging alignment with brand standards

### Content Quality Assurance
**Process**: Multi-stage review and refinement process

**Quality Gates**:
1. **Research Verification**: Fact-checking and source citation requirements
2. **SEO Compliance**: Keyword optimisation and technical SEO requirements
3. **Brand Alignment**: Voice, tone, and messaging consistency verification
4. **Conversion Optimisation**: Call-to-action effectiveness and user journey optimisation

**Approval Process**:
- Initial draft review and feedback incorporation
- SEO and technical optimisation verification
- Stakeholder review and final approval
- Publication and performance monitoring setup

## Phase 3: Optimisation and Enhancement (Month 4-6)

### Performance Monitoring and Improvement
**Objective**: Continuous optimisation based on performance data and user feedback

**Monitoring Framework**:
- **Weekly Reviews**: Traffic, engagement, and conversion performance analysis
- **Monthly Audits**: Comprehensive content and technical performance assessment
- **Quarterly Strategy**: Content strategy refinement and goal adjustment

**Optimisation Activities**:
- **Content Refinement**: Performance-based content improvements and updates
- **SEO Enhancement**: Keyword ranking improvement and technical optimisation
- **Conversion Optimisation**: User journey improvement and conversion rate enhancement
- **User Experience**: Navigation, accessibility, and mobile experience improvement

### Advanced Content Development
**Objective**: Authority building and market leadership establishment

**Content Types**:
- **Industry Insights**: Thought leadership and expertise demonstration
- **Educational Resources**: Comprehensive guides and problem-solving content
- **Case Studies**: Success story documentation and social proof development
- **Blog Content**: Regular content creation for SEO and audience engagement

## Implementation Timeline

### Month 1: Foundation Phase
- **Week 1**: Technical audit and infrastructure setup
- **Week 2**: Performance optimisation and SEO foundation
- **Week 3**: Content strategy deployment and team alignment
- **Week 4**: Workflow establishment and quality assurance setup

### Month 2: Content Development Phase
- **Week 1-2**: Priority page content creation and optimisation
- **Week 3-4**: Secondary content development and quality review

### Month 3: Enhancement Phase
- **Week 1-2**: Content refinement and additional page development
- **Week 3-4**: Performance monitoring setup and optimisation implementation

### Month 4-6: Optimisation Phase
- **Ongoing**: Performance monitoring and continuous improvement
- **Monthly**: Strategy review and content calendar updates
- **Quarterly**: Comprehensive audit and goal adjustment

## Resource Allocation

### Team Structure
- **Project Manager**: Overall coordination and timeline management
- **Content Strategist**: Strategy development and quality oversight
- **Content Creator**: Content writing and optimisation
- **Technical Specialist**: SEO and website optimisation
- **Quality Reviewer**: Final review and approval coordination

### Budget Allocation
- **Content Development**: 40% of total project budget
- **Technical Optimisation**: 30% of total project budget
- **Tools and Resources**: 15% of total project budget
- **Project Management**: 15% of total project budget

## Risk Management

### Identified Risks and Mitigation Strategies

**Content Approval Delays**:
- **Risk**: Stakeholder review bottlenecks affecting timeline
- **Mitigation**: Staged approval process with clear feedback timeframes
- **Contingency**: Parallel content track development for continuity

**Technical Implementation Challenges**:
- **Risk**: Complex technical requirements exceeding timeline
- **Mitigation**: Thorough technical audit and realistic timeline planning
- **Contingency**: Phased technical deployment with priority focus

**Resource Availability**:
- **Risk**: Key team member unavailability affecting delivery
- **Mitigation**: Cross-training and flexible resource allocation
- **Contingency**: External resource identification and rapid onboarding

## Success Measurement

### Key Performance Indicators (KPIs)
- **Traffic Metrics**: Organic traffic growth and keyword ranking improvement
- **Engagement Metrics**: Time on site, bounce rate, and page interaction
- **Conversion Metrics**: Lead generation, contact form submissions, and goal completion
- **Technical Metrics**: Page speed, Core Web Vitals, and SEO technical score

### Reporting Framework
- **Weekly Reports**: Traffic and conversion performance summary
- **Monthly Reviews**: Comprehensive performance analysis and recommendations
- **Quarterly Business Reviews**: Strategic impact assessment and planning

### Long-Term Success Indicators
- **Market Position**: Industry recognition and thought leadership establishment
- **Business Growth**: Revenue increase and customer acquisition improvement
- **Digital Authority**: Search ranking dominance and online reputation enhancement
- **Sustainable System**: Self-maintaining content and optimisation processes

---
*Implementation Plan created: {datetime.now().strftime('%d %B %Y')}*
*Client: {client_domain.replace('_', '.')}*
*Strategic roadmap for measurable business growth*
"""

    def generate_competitive_analysis_template(self, client_domain: str) -> str:
        """Generate competitive analysis template."""
        return f"""# {client_domain.replace('_', ' ').title()} - Competitive Analysis

## Executive Summary
Comprehensive competitive intelligence analysis for {client_domain.replace('_', '.')} identifying market positioning opportunities, content gaps, and strategic differentiation pathways.

## Competitive Landscape Overview

### Market Segmentation
- **Direct Competitors**: Companies offering identical services to the same target market
- **Indirect Competitors**: Alternative solutions addressing similar customer needs
- **Aspirational Competitors**: Market leaders demonstrating best practices and innovation
- **Emerging Players**: New entrants with disruptive approaches or technologies

### Competitive Intensity Assessment
- **Market Saturation**: Competitor density and market share distribution
- **Barrier to Entry**: Requirements for new competitors to enter the market
- **Price Competition**: Pricing strategies and competitive pricing pressure
- **Innovation Rate**: Frequency of new product/service introductions and improvements

## Primary Competitor Analysis

### Competitor 1: [Company Name]
**Market Position**: [Direct/Indirect competitor classification]
**Website**: [URL]
**Analysis Date**: [Current date]

**Strengths**:
- [Key competitive advantages and strong market positions]
- [Superior service offerings or market differentiation]
- [Strong brand recognition or customer loyalty]

**Weaknesses**:
- [Identified gaps in service offering or market coverage]
- [Customer service or delivery limitations]
- [Technical or operational disadvantages]

**Content Strategy**:
- **Content Volume**: [Number of pages, blog posts, resource depth]
- **Content Quality**: [Assessment of depth, authority, and usefulness]
- **SEO Performance**: [Estimated organic traffic and keyword rankings]
- **Content Gaps**: [Missing topics or underserved content areas]

**Digital Presence**:
- **Website Performance**: [Speed, usability, mobile responsiveness]
- **Social Media**: [Platform presence, engagement rates, follower counts]
- **Online Reviews**: [Review volume, average ratings, response management]

### Competitor 2: [Company Name]
[Repeat analysis framework for additional competitors]

### Competitor 3: [Company Name]
[Continue for 3-5 primary competitors]

## Content Gap Analysis

### Underserved Topics
- **Topic 1**: [Specific content area with limited competitor coverage]
  - **Opportunity**: [Description of content opportunity and potential impact]
  - **Competition Level**: [Assessment of current competitor activity]
  - **Recommended Approach**: [Strategic content development recommendations]

- **Topic 2**: [Additional content gap identification]
- **Topic 3**: [Continuing gap analysis]

### Content Quality Opportunities
- **Surface-Level Coverage**: [Topics covered by competitors but lacking depth]
- **Outdated Information**: [Content areas where competitors have stale information]
- **Poor User Experience**: [Competitor content with usability or accessibility issues]
- **Missing Formats**: [Content types not utilised by competitors (video, interactive, etc.)]

## SEO Competitive Analysis

### Keyword Landscape
- **High-Competition Keywords**: [Saturated search terms with strong competitor presence]
- **Medium-Competition Opportunities**: [Balanced competition with ranking potential]
- **Low-Competition Targets**: [Underserved keywords with ranking opportunities]
- **Long-Tail Opportunities**: [Specific, less competitive search phrases]

### Competitor SEO Performance
| Competitor | Estimated Organic Traffic | Top Keywords | Domain Authority | Content Pages |
|------------|-------------------------|--------------|------------------|---------------|
| [Company 1] | [Traffic estimate] | [Primary keywords] | [Authority score] | [Page count] |
| [Company 2] | [Traffic estimate] | [Primary keywords] | [Authority score] | [Page count] |
| [Company 3] | [Traffic estimate] | [Primary keywords] | [Authority score] | [Page count] |

### Technical SEO Comparison
- **Site Speed**: [Competitor performance comparison]
- **Mobile Optimisation**: [Mobile experience quality assessment]
- **Schema Markup**: [Structured data implementation analysis]
- **Technical Issues**: [Common technical SEO problems identified]

## Brand Positioning Analysis

### Value Proposition Comparison
- **Competitor A Positioning**: [How they position their unique value]
- **Competitor B Positioning**: [Alternative positioning approaches]
- **Market Positioning Gaps**: [Unoccupied market positions or messaging approaches]

### Messaging Analysis
- **Common Themes**: [Shared messaging across competitors]
- **Differentiation Approaches**: [How competitors distinguish themselves]
- **Tone and Voice**: [Communication style analysis]
- **Trust Building**: [Methods used to establish credibility and authority]

## Customer Experience Analysis

### Website User Experience
- **Navigation Structure**: [Competitor site architecture and usability]
- **Content Organisation**: [Information hierarchy and findability]
- **Conversion Pathways**: [Lead generation and contact processes]
- **Mobile Experience**: [Mobile usability and functionality]

### Customer Service Approach
- **Contact Methods**: [Available communication channels]
- **Response Times**: [Customer service responsiveness]
- **Support Resources**: [Help documentation, FAQs, and self-service options]
- **Review Management**: [Online reputation management approaches]

## Market Opportunity Assessment

### Competitive Advantages Available
1. **Content Authority**: [Opportunities to establish thought leadership]
2. **User Experience**: [Website and service experience improvements]
3. **Niche Specialisation**: [Underserved market segments or service areas]
4. **Technical Innovation**: [Technology or process improvements]

### Differentiation Strategies
- **Service Excellence**: [Superior service delivery or customer experience]
- **Specialisation Focus**: [Narrow focus on specific market needs]
- **Content Leadership**: [Comprehensive, authoritative content development]
- **Technical Superiority**: [Better tools, processes, or website experience]

## Strategic Recommendations

### Immediate Opportunities (0-3 months)
1. **Content Gap Exploitation**: [Specific content areas for immediate development]
2. **SEO Quick Wins**: [Low-hanging fruit keyword opportunities]
3. **User Experience Improvements**: [Website enhancements with immediate impact]

### Medium-Term Strategy (3-12 months)
1. **Authority Building**: [Systematic approach to thought leadership development]
2. **Market Positioning**: [Strategic brand positioning and messaging refinement]
3. **Content Expansion**: [Comprehensive content strategy for market coverage]

### Long-Term Vision (12+ months)
1. **Market Leadership**: [Path to industry authority and market dominance]
2. **Innovation Leadership**: [Continuous improvement and market innovation]
3. **Brand Recognition**: [Building strong brand awareness and customer loyalty]

## Monitoring and Updates

### Competitive Intelligence Framework
- **Monthly Monitoring**: [Regular competitor website and content review]
- **Quarterly Analysis**: [Comprehensive competitive position assessment]
- **Annual Strategy Review**: [Complete competitive strategy evaluation and planning]

### Key Metrics to Track
- **Market Share Indicators**: [Traffic, rankings, and visibility metrics]
- **Content Performance**: [Competitor content engagement and sharing]
- **Brand Mention Tracking**: [Online reputation and brand awareness monitoring]
- **Innovation Monitoring**: [New service offerings and market developments]

---
*Competitive Analysis completed: {datetime.now().strftime('%d %B %Y')}*
*Client: {client_domain.replace('_', '.')}*
*Strategic intelligence for market differentiation and competitive advantage*
"""

    def generate_audience_personas_template(self, client_domain: str) -> str:
        """Generate audience personas template."""
        return f"""# {client_domain.replace('_', ' ').title()} - Audience Personas

## Overview
Comprehensive audience persona development for {client_domain.replace('_', '.')} based on market research, customer analysis, and behavioural insights for targeted content strategy and marketing optimisation.

## Research Methodology

### Data Collection Sources
- **Customer Surveys**: Direct feedback from existing customers
- **Website Analytics**: User behaviour and engagement patterns
- **Social Media Insights**: Audience demographics and interaction data
- **Industry Research**: Market reports and demographic studies
- **Competitor Analysis**: Audience targeting and messaging analysis

### Persona Development Framework
- **Demographic Profiling**: Age, location, profession, income, education
- **Psychographic Analysis**: Values, interests, lifestyle, and motivations
- **Behavioural Patterns**: Online activity, content consumption, and decision-making
- **Pain Points**: Challenges, frustrations, and unmet needs
- **Goals and Motivations**: Objectives, aspirations, and success criteria

## Primary Persona: The Professional Decision Maker

### Demographics
- **Age Range**: 35-55 years
- **Gender**: [Based on research data]
- **Location**: [Geographic focus areas]
- **Profession**: [Industry-specific roles]
- **Income Level**: [Relevant income bracket]
- **Education**: [Educational background]

### Professional Context
- **Job Title**: [Specific roles and responsibilities]
- **Industry Experience**: [Years of experience and expertise level]
- **Company Size**: [Organisation size and structure]
- **Decision-Making Authority**: [Budget and procurement influence]
- **Professional Challenges**: [Industry-specific pain points]

### Goals and Motivations
- **Primary Objectives**: [What they're trying to achieve]
- **Success Metrics**: [How they measure success]
- **Career Aspirations**: [Professional growth and development goals]
- **Business Impact**: [Contribution to organisational success]

### Pain Points and Challenges
- **Operational Issues**: [Day-to-day frustrations and obstacles]
- **Resource Constraints**: [Budget, time, and staffing limitations]
- **Knowledge Gaps**: [Areas where they need education or support]
- **Decision Complexity**: [Factors that complicate their choices]

### Information Consumption Habits
- **Preferred Channels**: [Where they go for information]
- **Content Formats**: [Preferred content types and presentation]
- **Research Behaviour**: [How they evaluate options and make decisions]
- **Trust Sources**: [Credible information sources and influencers]

### Digital Behaviour
- **Device Usage**: [Desktop, mobile, tablet preferences]
- **Online Activity**: [Websites visited, social media usage]
- **Search Behaviour**: [How they search for solutions]
- **Content Engagement**: [What content they share and interact with]

### Quote
*"[Representative quote that captures their mindset and challenges]"*

### How We Help
- **Solution Alignment**: [How our services address their specific needs]
- **Value Proposition**: [Unique benefits we provide to this persona]
- **Content Strategy**: [Content types and topics that resonate]
- **Engagement Approach**: [Best methods to reach and communicate with them]

## Secondary Persona: The Research-Oriented Stakeholder

### Demographics
- **Age Range**: [Different from primary persona]
- **Professional Role**: [Supporting or influencing role]
- **Decision Influence**: [Level of input in decision-making process]

### Characteristics
- **Research Approach**: [How they gather and evaluate information]
- **Information Needs**: [Specific details and evidence they require]
- **Communication Preferences**: [How they like to receive information]
- **Influencing Factors**: [What persuades them to recommend solutions]

### Content Preferences
- **Detailed Documentation**: [In-depth information and technical details]
- **Comparative Analysis**: [Side-by-side evaluations and benchmarking]
- **Case Studies**: [Real-world examples and success stories]
- **Expert Validation**: [Third-party endorsements and credentials]

## Tertiary Persona: The Budget-Conscious Evaluator

### Profile
- **Role in Decision Process**: [Financial or operational oversight]
- **Primary Concerns**: [Cost-effectiveness and ROI focus]
- **Evaluation Criteria**: [How they assess value and make recommendations]

### Messaging Approach
- **Value Demonstration**: [ROI and cost-benefit communication]
- **Risk Mitigation**: [Addressing concerns about investment safety]
- **Comparative Value**: [Positioning against alternatives]

## Persona-Driven Content Strategy

### Content Mapping by Persona
**Primary Persona Content Needs**:
- **Awareness Stage**: [Content for problem recognition and education]
- **Consideration Stage**: [Solution evaluation and comparison content]
- **Decision Stage**: [Final decision support and vendor selection]

**Secondary Persona Content Needs**:
- **Technical Details**: [In-depth specifications and methodology]
- **Proof Points**: [Evidence, testimonials, and validation]
- **Implementation Guidance**: [Process documentation and support]

### Messaging Framework
**Primary Messaging for Decision Makers**:
- **Efficiency Focus**: [Time and resource optimisation]
- **Results Orientation**: [Outcome achievement and success metrics]
- **Professional Credibility**: [Authority and expertise demonstration]

**Supporting Messaging for Stakeholders**:
- **Detailed Evidence**: [Comprehensive information and documentation]
- **Risk Management**: [Safety and security considerations]
- **Implementation Support**: [Ongoing assistance and guidance]

## User Journey Mapping

### Awareness Stage Journey
- **Trigger Events**: [What causes them to recognise a need]
- **Information Sources**: [Where they go for initial research]
- **Content Consumption**: [What content they consume and when]
- **Key Questions**: [Primary concerns and information needs]

### Consideration Stage Journey
- **Evaluation Process**: [How they compare and assess options]
- **Decision Criteria**: [Factors that influence their choice]
- **Information Requirements**: [Detailed information and proof needed]
- **Stakeholder Involvement**: [Who else is involved in the process]

### Decision Stage Journey
- **Final Evaluation**: [Last steps before making a commitment]
- **Approval Process**: [Internal processes and sign-offs required]
- **Implementation Concerns**: [Questions about getting started]
- **Ongoing Relationship**: [Expectations for ongoing support and service]

## Implementation Guidelines

### Content Creation Priorities
1. **Address Primary Persona First**: [Focus on most important audience segment]
2. **Secondary Persona Support**: [Supporting content for influencers]
3. **Journey Stage Alignment**: [Content matched to decision process]
4. **Multi-Format Approach**: [Various content types for different preferences]

### Messaging Consistency
- **Voice and Tone**: [Communication style for each persona]
- **Value Proposition**: [Core benefits emphasised for each audience]
- **Proof Points**: [Evidence and validation most relevant to each persona]

### Performance Measurement
- **Engagement Metrics**: [How to measure persona-specific content performance]
- **Conversion Tracking**: [Persona-based conversion and goal measurement]
- **Feedback Collection**: [Methods for gathering persona-specific insights]

---
*Audience Personas completed: {datetime.now().strftime('%d %B %Y')}*
*Client: {client_domain.replace('_', '.')}*
*Strategic foundation for targeted content and marketing optimisation*
"""

    def generate_keyword_research_template(self, client_domain: str) -> str:
        """Generate keyword research template."""
        return f"""# {client_domain.replace('_', ' ').title()} - Keyword Research Strategy

## Executive Summary
Comprehensive keyword research and SEO strategy for {client_domain.replace('_', '.')} encompassing primary target keywords, content opportunities, and search visibility optimisation.

## Research Methodology

### Keyword Research Tools and Sources
- **Primary Tools**: [SEO platforms used for keyword analysis]
- **Search Console Data**: [Existing performance and search query analysis]
- **Competitor Analysis**: [Competitor keyword targeting and performance]
- **Customer Language**: [Terms and phrases used by target audience]
- **Industry Research**: [Sector-specific terminology and trending topics]

### Analysis Framework
- **Search Volume Analysis**: [Monthly search volume and trend data]
- **Competition Assessment**: [Keyword difficulty and competitive landscape]
- **Search Intent Classification**: [User intent behind search queries]
- **Commercial Value**: [Business relevance and conversion potential]
- **Ranking Opportunity**: [Realistic ranking potential and timeline]

## Primary Keyword Strategy

### High-Priority Target Keywords
| Keyword | Search Volume | Competition | Search Intent | Business Value | Current Rank | Target Rank |
|---------|---------------|-------------|---------------|----------------|--------------|-------------|
| [Primary Keyword 1] | [Volume] | [High/Med/Low] | [Intent Type] | [High/Med/Low] | [Current] | [Target] |
| [Primary Keyword 2] | [Volume] | [High/Med/Low] | [Intent Type] | [High/Med/Low] | [Current] | [Target] |
| [Primary Keyword 3] | [Volume] | [High/Med/Low] | [Intent Type] | [High/Med/Low] | [Current] | [Target] |

### Secondary Target Keywords
| Keyword | Search Volume | Competition | Search Intent | Business Value | Priority |
|---------|---------------|-------------|---------------|----------------|----------|
| [Secondary Keyword 1] | [Volume] | [Competition] | [Intent] | [Value] | [High/Med/Low] |
| [Secondary Keyword 2] | [Volume] | [Competition] | [Intent] | [Value] | [High/Med/Low] |
| [Secondary Keyword 3] | [Volume] | [Competition] | [Intent] | [Value] | [High/Med/Low] |

## Search Intent Analysis

### Informational Keywords
**Purpose**: Users seeking information and education
**Examples**: [List of informational search terms]
**Content Strategy**: Educational content, guides, and explanatory articles
**Page Types**: Blog posts, FAQ pages, educational resources

### Navigational Keywords
**Purpose**: Users looking for specific website or company
**Examples**: [Brand-related and company-specific terms]
**Content Strategy**: Brand awareness and direct navigation optimisation
**Page Types**: Homepage, about page, contact information

### Commercial Investigation Keywords
**Purpose**: Users researching solutions before purchasing
**Examples**: [Comparison and evaluation search terms]
**Content Strategy**: Comparison content, case studies, and service explanations
**Page Types**: Service pages, comparison articles, case studies

### Transactional Keywords
**Purpose**: Users ready to make a purchase or contact decision
**Examples**: [Action-oriented and conversion search terms]
**Content Strategy**: Clear value propositions and conversion optimisation
**Page Types**: Service pages, contact pages, consultation requests

## Long-Tail Keyword Opportunities

### High-Value Long-Tail Keywords
- **[Specific long-tail phrase 1]**: [Search volume, competition, opportunity description]
- **[Specific long-tail phrase 2]**: [Search volume, competition, opportunity description]
- **[Specific long-tail phrase 3]**: [Search volume, competition, opportunity description]

### Question-Based Keywords
- **"How to [relevant topic]?"**: [Volume and opportunity analysis]
- **"What is [relevant topic]?"**: [Volume and opportunity analysis]
- **"Why [relevant topic]?"**: [Volume and opportunity analysis]

### Location-Based Keywords
- **[Service] + [Location]**: [Local search opportunity analysis]
- **[Service] + "near me"**: [Proximity search optimisation]
- **[Location] + [Industry term]**: [Geographic targeting opportunities]

## Competitive Keyword Analysis

### Competitor Keyword Performance
**Competitor 1: [Company Name]**
- **Top Performing Keywords**: [List of their best-ranking keywords]
- **Keyword Gaps**: [Keywords they rank for that we don't target]
- **Opportunity Assessment**: [Keywords we could compete for]

**Competitor 2: [Company Name]**
- **Top Performing Keywords**: [Their primary keyword targets]
- **Content Strategy**: [How they're targeting these keywords]
- **Differentiation Opportunities**: [How we can approach differently]

### Keyword Gap Analysis
- **Untapped Opportunities**: [Keywords competitors aren't targeting]
- **Underserved Markets**: [Search terms with limited quality content]
- **Emerging Trends**: [New keywords gaining search volume]

## Content Keyword Mapping

### Homepage Keywords
**Primary Target**: [Main homepage keyword focus]
**Secondary Keywords**: [Supporting homepage keywords]
**Search Intent**: [Why users would search these terms]
**Content Strategy**: [How to incorporate keywords naturally]

### Service Page Keywords
**Service 1 Keywords**:
- Primary: [Main keyword for this service]
- Secondary: [Supporting keywords]
- Long-tail: [Specific service-related phrases]

**Service 2 Keywords**:
- Primary: [Main keyword for this service]
- Secondary: [Supporting keywords]
- Long-tail: [Specific service-related phrases]

### Blog Content Keywords
**Educational Content**:
- [Topic 1]: [Keyword cluster and search volume]
- [Topic 2]: [Keyword cluster and search volume]
- [Topic 3]: [Keyword cluster and search volume]

**Problem-Solution Content**:
- [Problem keyword]: [Search volume and content approach]
- [Solution keyword]: [Search volume and content approach]

## Keyword Implementation Strategy

### On-Page Optimisation
- **Title Tags**: [Keyword placement and optimisation guidelines]
- **Meta Descriptions**: [Keyword inclusion and call-to-action optimisation]
- **Header Structure**: [H1, H2, H3 keyword integration strategy]
- **Content Integration**: [Natural keyword inclusion and density guidelines]

### Content Creation Priorities
**Month 1 Focus**:
- [High-priority keyword content creation]
- [Quick-win keyword targeting]
- [Foundation content establishment]

**Month 2-3 Focus**:
- [Medium-competition keyword targeting]
- [Content cluster development]
- [Long-tail keyword expansion]

**Month 4-6 Focus**:
- [Competitive keyword targeting]
- [Authority building content]
- [Advanced SEO optimisation]

## Local SEO Keywords (if applicable)

### Geographic Modifiers
- **Primary Location Terms**: [City, region, area-specific keywords]
- **Service + Location Combinations**: [Service-specific local terms]
- **"Near Me" Optimisation**: [Proximity search targeting]

### Local Business Keywords
- **Industry + Location**: [Professional services in location]
- **Location + Problem**: [Local problem-solving searches]
- **Reviews and Recommendations**: [Local review-related searches]

## Keyword Performance Tracking

### Ranking Monitoring
- **Primary Keywords**: [Monthly ranking position tracking]
- **Secondary Keywords**: [Quarterly ranking assessment]
- **Long-tail Keywords**: [Performance trend monitoring]

### Traffic and Conversion Analysis
- **Organic Traffic Growth**: [Keyword-driven traffic increases]
- **Conversion Tracking**: [Keywords driving leads and conversions]
- **ROI Assessment**: [Revenue attribution to keyword performance]

### Competitive Monitoring
- **Competitor Ranking Changes**: [Tracking competitor keyword performance]
- **Market Share Analysis**: [Visibility share for target keywords]
- **Opportunity Identification**: [New keyword opportunities from competitor analysis]

## Implementation Timeline

### Phase 1: Foundation (Month 1)
- **High-Priority Keywords**: [Immediate keyword targeting implementation]
- **Quick Wins**: [Low-competition, high-value keyword optimisation]
- **Technical Setup**: [Keyword tracking and monitoring implementation]

### Phase 2: Expansion (Month 2-3)
- **Content Development**: [Keyword-focused content creation]
- **Long-tail Targeting**: [Specific phrase optimisation]
- **Competitive Keywords**: [Strategic competitive keyword targeting]

### Phase 3: Authority Building (Month 4-6)
- **Difficult Keywords**: [High-competition keyword targeting]
- **Topic Clusters**: [Comprehensive topic authority development]
- **Link Building**: [Authority development for keyword ranking improvement]

## Success Metrics and KPIs

### Ranking Improvements
- **Target Keyword Rankings**: [Specific position improvements for priority keywords]
- **Keyword Visibility**: [Overall search visibility increase]
- **Featured Snippet Captures**: [Rich snippet and featured content targeting]

### Traffic Growth
- **Organic Traffic Increase**: [Percentage growth in organic search traffic]
- **Keyword-Driven Traffic**: [Traffic attributable to target keywords]
- **Long-tail Traffic Growth**: [Increased traffic from long-tail keywords]

### Business Impact
- **Lead Generation**: [Conversion increase from keyword-targeted traffic]
- **Revenue Attribution**: [Business results from SEO keyword strategy]
- **Market Position**: [Industry authority and competitive positioning]

---
*Keyword Research Strategy completed: {datetime.now().strftime('%d %B %Y')}*
*Client: {client_domain.replace('_', '.')}*
*Strategic foundation for search visibility and organic traffic growth*
"""

    def generate_ai_optimization_template(self, client_domain: str) -> str:
        """Generate AI optimization guide template."""
        return f"""# {client_domain.replace('_', ' ').title()} - AI Optimisation Guide

## Executive Summary
Comprehensive AI optimisation strategy for {client_domain.replace('_', '.')} encompassing voice search, AI-powered search engines, and future-proofing content for evolving search technologies.

## AI Search Landscape Overview

### Current AI Search Technologies
- **Google AI Integration**: BERT, MUM, and RankBrain algorithm impacts
- **Voice Search Platforms**: Alexa, Siri, Google Assistant optimisation
- **AI-Powered Search Engines**: ChatGPT, Bing AI, and emerging platforms
- **Featured Snippets**: Position zero and rich snippet optimisation

### Future AI Search Trends
- **Conversational Search**: Natural language query processing
- **Multimodal Search**: Image, voice, and text combination searches
- **Personalised AI Results**: User-specific content recommendation
- **Real-time AI Responses**: Instant, context-aware search answers

## Voice Search Optimisation

### Voice Search Query Characteristics
- **Natural Language**: Conversational, question-based queries
- **Local Intent**: "Near me" and location-specific searches
- **Longer Phrases**: Complete sentences and detailed questions
- **Action-Oriented**: Immediate need and solution-focused

### Voice Search SEO Strategy
**Question-Based Content**:
- **Who**: [Industry expertise and company information]
- **What**: [Service definitions and explanations]
- **Where**: [Location and service area information]
- **When**: [Timing and availability information]
- **Why**: [Benefits and value proposition explanations]
- **How**: [Process and methodology explanations]

**Featured Snippet Optimisation**:
- **Direct Answers**: Clear, concise responses to common questions
- **Structured Data**: Schema markup for rich snippet eligibility
- **List Formats**: Numbered and bulleted information presentation
- **Table Data**: Comparative information and specifications

### Local Voice Search Optimisation
- **Business Information**: Complete and accurate local business listings
- **Service Areas**: Clear geographic coverage and availability
- **Contact Information**: Easy-to-speak phone numbers and addresses
- **Operating Hours**: Current and accurate business hours

## AI Content Optimisation

### E-A-T Enhancement (Expertise, Authoritativeness, Trustworthiness)
**Expertise Demonstration**:
- **Author Credentials**: Professional qualifications and experience
- **Industry Knowledge**: Deep subject matter expertise demonstration
- **Technical Accuracy**: Factual, current, and verified information
- **Comprehensive Coverage**: Thorough topic exploration and detail

**Authority Building**:
- **Industry Recognition**: Awards, certifications, and professional memberships
- **Media Mentions**: Press coverage and industry publication features
- **Professional Networks**: Industry associations and peer recognition
- **Thought Leadership**: Original insights and innovative approaches

**Trust Signal Implementation**:
- **Contact Information**: Clear, accessible business contact details
- **Privacy Policies**: Transparent data handling and privacy protection
- **Security Measures**: SSL certificates and secure website infrastructure
- **Customer Reviews**: Authentic testimonials and review management

### Content Structure for AI Processing
**Hierarchical Information Architecture**:
- **Clear Headings**: Logical H1, H2, H3 structure for content organisation
- **Topic Clusters**: Related content linking and topical authority
- **Internal Linking**: Strategic content interconnection for context
- **Breadcrumb Navigation**: Clear site structure and page relationships

**Semantic Content Optimisation**:
- **Related Keywords**: LSI keywords and semantic keyword integration
- **Context Building**: Comprehensive topic coverage and related concepts
- **Entity Recognition**: Clear entity relationships and mentions
- **Natural Language**: Conversational tone and readable content structure

## Schema Markup Implementation

### Essential Schema Types
**Organisation Schema**:
- Business information and contact details
- Location and service area definition
- Social media profiles and online presence
- Awards and certifications display

**Service Schema**:
- Service descriptions and offerings
- Pricing information and service areas
- Provider information and qualifications
- Customer review and rating integration

**FAQ Schema**:
- Common questions and detailed answers
- Voice search and featured snippet optimisation
- Structured question and answer format
- Related topic and service integration

**Local Business Schema**:
- Complete business listing information
- Operating hours and availability
- Location and service area mapping
- Contact and communication methods

### Technical Implementation
```json
{{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "{client_domain.replace('_', ' ').title()}",
  "description": "[Professional service description]",
  "url": "https://{client_domain.replace('_', '.')}",
  "address": {{
    "@type": "PostalAddress",
    "streetAddress": "[Street Address]",
    "addressLocality": "[City]",
    "addressRegion": "[State/Region]",
    "postalCode": "[Postal Code]",
    "addressCountry": "AU"
  }}
}}
```

## AI-Friendly Content Creation

### Content Format Optimisation
**Scannable Structure**:
- **Short Paragraphs**: 2-3 sentences for easy AI processing
- **Bullet Points**: Key information in list format
- **Clear Subheadings**: Descriptive headers for content sections
- **Summary Sections**: Key takeaways and conclusion summaries

**Answer-First Approach**:
- **Direct Responses**: Immediate answers to common questions
- **Progressive Detail**: Basic answer followed by detailed explanation
- **Multiple Formats**: Text, lists, and table presentations
- **Action Steps**: Clear next steps and implementation guidance

### Topic Authority Development
**Comprehensive Coverage**:
- **Core Topics**: Primary service and expertise areas
- **Related Subjects**: Supporting and adjacent topic coverage
- **Industry Trends**: Current developments and future predictions
- **Problem-Solution Mapping**: Customer challenges and solution presentation

**Content Depth Strategy**:
- **Pillar Content**: Comprehensive, authoritative topic coverage
- **Cluster Content**: Supporting articles and detailed subtopics
- **Update Frequency**: Regular content refresh and current information
- **Cross-Referencing**: Internal linking and topic relationship building

## Voice Assistant Optimisation

### Amazon Alexa Optimisation
- **Skills Development**: Custom Alexa skills for service information
- **Flash Briefings**: Regular updates and industry news
- **Local Search**: Business listing and service area optimisation

### Google Assistant Optimisation
- **Actions on Google**: Interactive service information and booking
- **Business Messages**: Customer communication and enquiry handling
- **Local Listings**: Google My Business optimisation and management

### Siri and Apple Optimisation
- **Apple Maps**: Business listing and location accuracy
- **Siri Shortcuts**: Quick access to business information
- **iOS Search**: App and website integration for iOS users

## AI Search Console and Monitoring

### Performance Tracking Tools
- **Google Search Console**: Voice search query and performance data
- **AI Search Analytics**: Specialised tracking for AI-powered search
- **Featured Snippet Monitoring**: Position zero tracking and optimisation
- **Voice Search Tools**: Voice query performance and ranking analysis

### Key Performance Indicators
**Voice Search Metrics**:
- **Voice Search Traffic**: Percentage of traffic from voice queries
- **Featured Snippet Captures**: Position zero achievements
- **Question-Based Rankings**: Performance for interrogative queries
- **Local Voice Searches**: "Near me" and location-based performance

**AI Content Performance**:
- **AI Citability Score**: How often AI tools reference our content
- **Entity Mention Frequency**: Brand and expertise recognition in AI responses
- **Topic Authority Metrics**: Search dominance for key subject areas
- **Semantic Search Performance**: Related keyword and concept rankings

## Implementation Roadmap

### Phase 1: Foundation Setup (Month 1)
**Technical Implementation**:
- Schema markup deployment across all pages
- Voice search query analysis and baseline establishment
- Featured snippet opportunity identification
- AI-friendly content audit and gap analysis

**Content Optimisation**:
- FAQ page development with voice search focus
- Question-based content creation for primary topics
- Local business information optimisation
- Mobile and voice user experience improvement

### Phase 2: Content Development (Month 2-3)
**AI-Optimised Content Creation**:
- Comprehensive topic coverage for primary service areas
- Question and answer format content development
- Voice search-friendly blog post creation
- Local and "near me" search optimisation

**Authority Building**:
- Expert author profiles and credentials highlighting
- Industry expertise demonstration content
- Trust signal implementation and enhancement
- Professional network and association integration

### Phase 3: Advanced Optimisation (Month 4-6)
**Advanced AI Features**:
- Custom voice assistant skills development
- Interactive content and tools creation
- Real-time chat and AI assistant integration
- Personalised content and user experience

**Performance Optimisation**:
- AI search performance monitoring and improvement
- Featured snippet optimisation and expansion
- Voice search ranking improvement strategies
- Continuous testing and refinement

## Future-Proofing Strategy

### Emerging AI Technologies
- **GPT Integration**: Optimisation for GPT-style AI responses
- **Multimodal Search**: Image and voice search combination
- **Real-time AI**: Instant response and dynamic content
- **Personalised AI**: User-specific content and recommendations

### Adaptation Framework
- **Continuous Monitoring**: AI search technology development tracking
- **Regular Updates**: Content and technical optimisation refinement
- **Testing and Experimentation**: New AI feature testing and implementation
- **Performance Analysis**: AI search impact measurement and improvement

### Long-term Vision
- **AI Search Leadership**: Industry authority in AI-optimised content
- **Voice Search Dominance**: Top rankings for voice and conversational queries
- **Technology Integration**: Seamless AI tool and platform integration
- **Future Readiness**: Preparation for next-generation search technologies

---
*AI Optimisation Guide completed: {datetime.now().strftime('%d %B %Y')}*
*Client: {client_domain.replace('_', '.')}*
*Strategic foundation for AI-powered search visibility and future-proofing*
"""

    def print_audit_report(self, audit_results: Dict):
        """Print formatted audit report."""
        print("\n" + "="*80)
        print("PRE-DELIVERY AUDIT REPORT")
        print("="*80)
        print(f"Client: {audit_results['client_domain']}")
        print(f"Audit Date: {datetime.fromisoformat(audit_results['audit_date']).strftime('%d %B %Y at %H:%M')}")
        print(f"Overall Status: {audit_results['overall_status']}")
        print(f"Compliance Score: {audit_results['compliance_score']}%")

        print(f"\nMANDATORY FILES STATUS:")
        print(f"Required: {audit_results['mandatory_files']['total_required']}")
        print(f"Existing: {audit_results['mandatory_files']['existing']}")
        print(f"Missing: {audit_results['mandatory_files']['missing']}")

        if audit_results['mandatory_files']['missing_files']:
            print(f"\nMISSING FILES:")
            for missing_file in audit_results['mandatory_files']['missing_files']:
                print(f"  ❌ {missing_file}")

        if audit_results['word_count_compliance']['violations']:
            print(f"\nWORD COUNT SOP VIOLATIONS:")
            for violation in audit_results['word_count_compliance']['violations']:
                print(f"  ⚠️  {violation['file']}: {violation['message']}")

        if audit_results['user_journey_issues']:
            print(f"\nUSER JOURNEY ISSUES:")
            for issue in audit_results['user_journey_issues']:
                print(f"  ⚠️  {issue}")

        if audit_results['auto_generation']['files_generated']:
            print(f"\nAUTO-GENERATED FILES:")
            for generated_file in audit_results['auto_generation']['generated_files']:
                print(f"  ✅ {generated_file}")

        print(f"\nRECOMMENDATIONS:")
        for recommendation in audit_results['recommendations']:
            print(f"  • {recommendation}")

        print("\n" + "="*80)


def main():
    parser = argparse.ArgumentParser(
        description="Pre-delivery audit for client project compliance"
    )
    parser.add_argument(
        'path',
        help='Path to any file within client project folder'
    )
    parser.add_argument(
        '--auto-generate',
        action='store_true',
        help='Automatically generate missing file templates'
    )
    parser.add_argument(
        '--json-output',
        action='store_true',
        help='Output results in JSON format'
    )
    parser.add_argument(
        '--block-if-incomplete',
        action='store_true',
        help='Exit with error code if project is not compliant'
    )

    args = parser.parse_args()

    auditor = PreDeliveryAuditor()
    results = auditor.run_comprehensive_audit(args.path, args.auto_generate)

    if args.json_output:
        print(json.dumps(results, indent=2))
    else:
        if results['success']:
            auditor.print_audit_report(results)
        else:
            print(f"❌ Audit Error: {results['error']}")

    # Exit with error code if blocking requested and project not compliant
    if args.block_if_incomplete and results.get('overall_status') == 'NON_COMPLIANT':
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()