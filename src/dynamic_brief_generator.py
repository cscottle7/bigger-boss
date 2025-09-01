"""
Dynamic Brief Generation System
Automatically creates campaign_brief.md and task_deps.md files based on user natural language requests
"""

import re
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class UserRequest:
    """Structured representation of user natural language request"""
    raw_text: str
    intent: str
    primary_goal: str
    urls: List[str]
    topics: List[str]
    keywords: List[str]
    competitors: List[str]
    content_types: List[str]
    urgency: str
    scope: str


@dataclass
class SquadActivation:
    """Squad activation configuration"""
    sitespect: bool = False
    contentforge: bool = False
    strategynexus: bool = False
    sitespect_focus: List[str] = None
    contentforge_focus: List[str] = None
    strategynexus_focus: List[str] = None


class NaturalLanguageProcessor:
    """Process natural language requests and extract structured intent"""
    
    def __init__(self):
        self.url_pattern = re.compile(r'https?://(?:[-\w.])+(?:\:[0-9]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:\#(?:[\w.])*)?)?')
        self.intent_patterns = {
            'website_audit': [
                r'audit.*website', r'check.*site', r'analyze.*site', r'website.*analysis',
                r'site.*performance', r'technical.*seo', r'accessibility.*check'
            ],
            'content_strategy': [
                r'content.*strategy', r'create.*content', r'content.*brief', r'content.*plan',
                r'marketing.*content', r'blog.*strategy', r'content.*calendar'
            ],
            'competitive_analysis': [
                r'competitor.*analysis', r'competitive.*research', r'compare.*competitors',
                r'market.*analysis', r'competitor.*study'
            ],
            'strategic_planning': [
                r'marketing.*strategy', r'business.*strategy', r'strategic.*planning',
                r'market.*positioning', r'strategic.*analysis'
            ],
            'combined_analysis': [
                r'complete.*analysis', r'full.*audit', r'comprehensive.*review',
                r'audit.*and.*content', r'strategy.*and.*audit'
            ]
        }
        
        self.urgency_indicators = {
            'critical': ['urgent', 'asap', 'immediately', 'critical', 'emergency'],
            'high': ['soon', 'quickly', 'fast', 'priority', 'important'],
            'normal': ['when possible', 'regular', 'standard', 'normal']
        }
        
        self.content_type_indicators = {
            'blog_posts': ['blog', 'article', 'post'],
            'landing_pages': ['landing', 'page', 'conversion'],
            'social_media': ['social', 'twitter', 'facebook', 'linkedin', 'instagram'],
            'email': ['email', 'newsletter', 'campaign'],
            'website_copy': ['website', 'copy', 'homepage', 'about'],
            'product_descriptions': ['product', 'description', 'catalog'],
            'whitepapers': ['whitepaper', 'guide', 'ebook', 'report']
        }
    
    def parse_request(self, request_text: str) -> UserRequest:
        """Parse natural language request into structured format"""
        logger.info(f"Parsing user request: {request_text[:100]}...")
        
        # Extract URLs
        urls = self.url_pattern.findall(request_text)
        
        # Determine primary intent
        intent = self._classify_intent(request_text)
        
        # Extract topics and keywords
        topics = self._extract_topics(request_text)
        keywords = self._extract_keywords(request_text)
        
        # Extract competitor information
        competitors = self._extract_competitors(request_text, urls)
        
        # Determine content types
        content_types = self._extract_content_types(request_text)
        
        # Assess urgency
        urgency = self._assess_urgency(request_text)
        
        # Determine scope
        scope = self._determine_scope(intent, len(urls), len(competitors))
        
        # Generate primary goal
        primary_goal = self._generate_primary_goal(intent, topics, urgency)
        
        return UserRequest(
            raw_text=request_text,
            intent=intent,
            primary_goal=primary_goal,
            urls=urls,
            topics=topics,
            keywords=keywords,
            competitors=competitors,
            content_types=content_types,
            urgency=urgency,
            scope=scope
        )
    
    def _classify_intent(self, text: str) -> str:
        """Classify the primary intent of the user request"""
        text_lower = text.lower()
        intent_scores = {}
        
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    score += 1
            intent_scores[intent] = score
        
        # Return intent with highest score, default to combined_analysis if tie
        max_score = max(intent_scores.values()) if intent_scores.values() else 0
        if max_score == 0:
            return 'strategic_planning'  # Default intent
        
        # If multiple intents have max score, prioritize combined analysis
        top_intents = [intent for intent, score in intent_scores.items() if score == max_score]
        if len(top_intents) > 1 and 'combined_analysis' in top_intents:
            return 'combined_analysis'
        
        return top_intents[0]
    
    def _extract_topics(self, text: str) -> List[str]:
        """Extract main topics from the request"""
        # Common topic extraction patterns
        topic_patterns = [
            r'for ([^,\n.]+(?:campaign|strategy|marketing|sales))',
            r'about ([^,\n.]+)',
            r'regarding ([^,\n.]+)',
            r'content.*for ([^,\n.]+)',
            r'([^,\n.]+(?:industry|market|sector))',
        ]
        
        topics = []
        text_lower = text.lower()
        
        for pattern in topic_patterns:
            matches = re.findall(pattern, text_lower)
            topics.extend([match.strip() for match in matches if len(match.strip()) > 2])
        
        # Clean and deduplicate
        return list(set([topic for topic in topics if len(topic) <= 50]))[:5]  # Limit to 5 topics
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract potential keywords from the request"""
        # Remove common words and extract meaningful terms
        stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        
        keywords = [word for word in words if word not in stop_words and len(word) > 3]
        
        # Return top 10 most relevant keywords
        return list(set(keywords))[:10]
    
    def _extract_competitors(self, text: str, urls: List[str]) -> List[str]:
        """Extract competitor URLs and names"""
        competitors = []
        
        # Extract explicitly mentioned competitors
        competitor_patterns = [
            r'competitor[s]?:?\s*([^,\n.]+)',
            r'compared? to ([^,\n.]+)',
            r'against ([^,\n.]+)',
            r'vs\.?\s+([^,\n.]+)'
        ]
        
        text_lower = text.lower()
        for pattern in competitor_patterns:
            matches = re.findall(pattern, text_lower)
            competitors.extend([match.strip() for match in matches])
        
        # Add URLs that might be competitors (not the main site being audited)
        if len(urls) > 1:
            competitors.extend(urls[1:])  # Assume first URL is primary site
        
        return list(set(competitors))[:5]  # Limit to 5 competitors
    
    def _extract_content_types(self, text: str) -> List[str]:
        """Extract mentioned content types"""
        text_lower = text.lower()
        content_types = []
        
        for content_type, indicators in self.content_type_indicators.items():
            if any(indicator in text_lower for indicator in indicators):
                content_types.append(content_type)
        
        return content_types or ['blog_posts']  # Default to blog posts
    
    def _assess_urgency(self, text: str) -> str:
        """Assess urgency level from the request"""
        text_lower = text.lower()
        
        for urgency, indicators in self.urgency_indicators.items():
            if any(indicator in text_lower for indicator in indicators):
                return urgency
        
        return 'normal'
    
    def _determine_scope(self, intent: str, url_count: int, competitor_count: int) -> str:
        """Determine analysis scope based on request characteristics"""
        if intent == 'combined_analysis' or url_count > 1 or competitor_count > 2:
            return 'comprehensive'
        elif intent in ['competitive_analysis', 'strategic_planning']:
            return 'strategic'
        elif intent in ['website_audit', 'content_strategy']:
            return 'focused'
        else:
            return 'standard'
    
    def _generate_primary_goal(self, intent: str, topics: List[str], urgency: str) -> str:
        """Generate a clear primary goal statement"""
        goal_templates = {
            'website_audit': "Conduct comprehensive website audit and provide actionable recommendations",
            'content_strategy': "Develop data-driven content strategy and implementation plan",
            'competitive_analysis': "Analyze competitive landscape and identify strategic opportunities",
            'strategic_planning': "Create strategic marketing plan with competitive intelligence",
            'combined_analysis': "Deliver comprehensive marketing analysis combining technical audit, content strategy, and competitive intelligence"
        }
        
        base_goal = goal_templates.get(intent, "Provide comprehensive marketing analysis and recommendations")
        
        if topics:
            topic_context = f" for {', '.join(topics[:2])}"  # Include up to 2 topics
            base_goal += topic_context
        
        if urgency == 'critical':
            base_goal += " (URGENT PRIORITY)"
        elif urgency == 'high':
            base_goal += " (HIGH PRIORITY)"
        
        return base_goal


class SquadRouter:
    """Determine which squads should be activated based on user request"""
    
    def determine_squad_activation(self, request: UserRequest) -> SquadActivation:
        """Determine which squads to activate and their focus areas"""
        
        activation = SquadActivation()
        
        # SiteSpect activation logic
        if (request.intent in ['website_audit', 'combined_analysis'] or 
            request.urls or 
            any(term in request.raw_text.lower() for term in ['site', 'website', 'performance', 'seo', 'accessibility'])):
            
            activation.sitespect = True
            activation.sitespect_focus = self._determine_sitespect_focus(request)
        
        # ContentForge activation logic
        if (request.intent in ['content_strategy', 'combined_analysis'] or
            request.content_types or
            any(term in request.raw_text.lower() for term in ['content', 'blog', 'article', 'marketing'])):
            
            activation.contentforge = True
            activation.contentforge_focus = self._determine_contentforge_focus(request)
        
        # StrategyNexus activation logic
        if (request.intent in ['competitive_analysis', 'strategic_planning', 'combined_analysis'] or
            request.competitors or
            any(term in request.raw_text.lower() for term in ['strategy', 'competitor', 'market', 'positioning'])):
            
            activation.strategynexus = True
            activation.strategynexus_focus = self._determine_strategynexus_focus(request)
        
        return activation
    
    def _determine_sitespect_focus(self, request: UserRequest) -> List[str]:
        """Determine specific focus areas for SiteSpect squad"""
        focus_areas = []
        text_lower = request.raw_text.lower()
        
        focus_mapping = {
            'technical_seo': ['seo', 'technical', 'crawl', 'index', 'meta'],
            'performance': ['speed', 'performance', 'load', 'fast', 'slow'],
            'accessibility': ['accessibility', 'wcag', 'compliance', 'disabled'],
            'ux_analysis': ['ux', 'user experience', 'usability', 'navigation', 'flow']
        }
        
        for focus, keywords in focus_mapping.items():
            if any(keyword in text_lower for keyword in keywords):
                focus_areas.append(focus)
        
        return focus_areas or ['comprehensive_audit']
    
    def _determine_contentforge_focus(self, request: UserRequest) -> List[str]:
        """Determine specific focus areas for ContentForge squad"""
        focus_areas = []
        
        if request.topics:
            focus_areas.append('topic_research')
        if request.keywords:
            focus_areas.append('keyword_optimization')
        if request.competitors:
            focus_areas.append('competitive_content_analysis')
        if 'brand' in request.raw_text.lower():
            focus_areas.append('brand_voice_analysis')
        
        return focus_areas or ['comprehensive_content_strategy']
    
    def _determine_strategynexus_focus(self, request: UserRequest) -> List[str]:
        """Determine specific focus areas for StrategyNexus squad"""
        focus_areas = []
        text_lower = request.raw_text.lower()
        
        focus_mapping = {
            'competitive_analysis': ['competitor', 'competitive', 'compare', 'vs'],
            'brand_positioning': ['brand', 'positioning', 'identity', 'voice'],
            'market_analysis': ['market', 'industry', 'sector', 'landscape'],
            'seo_strategy': ['seo', 'search', 'organic', 'ranking'],
            'user_journey': ['journey', 'experience', 'funnel', 'conversion']
        }
        
        for focus, keywords in focus_mapping.items():
            if any(keyword in text_lower for keyword in keywords):
                focus_areas.append(focus)
        
        return focus_areas or ['strategic_analysis']


class BriefGenerator:
    """Generate campaign briefs and task dependencies"""
    
    def __init__(self):
        self.nlp = NaturalLanguageProcessor()
        self.router = SquadRouter()
    
    def generate_briefs(self, user_request: str) -> Tuple[str, str]:
        """Generate both campaign brief and task dependencies"""
        
        # Parse user request
        parsed_request = self.nlp.parse_request(user_request)
        
        # Determine squad activation
        squad_activation = self.router.determine_squad_activation(parsed_request)
        
        # Generate campaign brief
        campaign_brief = self._generate_campaign_brief(parsed_request, squad_activation)
        
        # Generate task dependencies
        task_deps = self._generate_task_deps(parsed_request, squad_activation)
        
        return campaign_brief, task_deps
    
    def _generate_campaign_brief(self, request: UserRequest, activation: SquadActivation) -> str:
        """Generate campaign brief markdown"""
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        brief = f"""# Campaign Brief: {self._generate_project_title(request)}

## Project Overview
- **Generated**: {timestamp}
- **Primary Objective**: {request.primary_goal}
- **Urgency Level**: {request.urgency.upper()}
- **Scope**: {request.scope.title()} Analysis
- **Timeline**: {self._estimate_timeline(activation)}

## User Request Analysis
**Original Request**: "{request.raw_text}"

**Interpreted Intent**: {request.intent.replace('_', ' ').title()}

## Target Analysis
"""
        
        if request.urls:
            brief += f"\n**Primary URLs**:\n"
            for url in request.urls:
                brief += f"- {url}\n"
        
        if request.topics:
            brief += f"\n**Focus Topics**:\n"
            for topic in request.topics:
                brief += f"- {topic.title()}\n"
        
        if request.competitors:
            brief += f"\n**Competitors**:\n"
            for comp in request.competitors:
                brief += f"- {comp}\n"
        
        if request.content_types:
            brief += f"\n**Content Types**:\n"
            for content_type in request.content_types:
                brief += f"- {content_type.replace('_', ' ').title()}\n"
        
        brief += f"\n## Execution Strategy\n"
        brief += self._generate_execution_strategy(activation)
        
        brief += f"\n## Squad Activation\n"
        brief += self._generate_squad_activation_summary(activation)
        
        brief += f"\n## Expected Deliverables\n"
        brief += self._generate_deliverables_list(request, activation)
        
        brief += f"\n## Success Criteria\n"
        brief += self._generate_success_criteria(request, activation)
        
        return brief
    
    def _generate_task_deps(self, request: UserRequest, activation: SquadActivation) -> str:
        """Generate task dependencies markdown"""
        
        timestamp = datetime.now().strftime("%Y-%m-%d")
        project_id = f"{request.intent.upper()}_{timestamp.replace('-', '')}"
        
        task_deps = f"""# Task Dependencies: {self._generate_project_title(request)}

## Project Metadata
- **Project ID**: {project_id}
- **Request Type**: {request.intent.replace('_', ' ').title()}
- **Urgency**: {request.urgency.upper()}
- **Scope**: {request.scope.title()}

## Execution Plan

### Phase 1: Research & Analysis (Parallel Execution)
**Timeline**: {self._estimate_phase_duration(activation, 1)}

"""
        
        if activation.sitespect:
            task_deps += f"**SiteSpect Squad Execution**:\n"
            task_deps += f"- **Orchestrator**: @sitespect_orchestrator\n"
            task_deps += f"- **Focus Areas**: {', '.join(activation.sitespect_focus)}\n"
            if request.urls:
                task_deps += f"- **Target URLs**: {', '.join(request.urls)}\n"
            task_deps += f"- **Priority**: {request.urgency.title()}\n\n"
        
        if activation.contentforge:
            task_deps += f"**ContentForge Squad Execution**:\n"
            task_deps += f"- **Orchestrator**: @content_workflow_orchestrator\n"
            task_deps += f"- **Focus Areas**: {', '.join(activation.contentforge_focus)}\n"
            if request.topics:
                task_deps += f"- **Topics**: {', '.join(request.topics)}\n"
            if request.content_types:
                task_deps += f"- **Content Types**: {', '.join(request.content_types)}\n"
            task_deps += f"- **Priority**: {request.urgency.title()}\n\n"
        
        if activation.strategynexus:
            task_deps += f"**StrategyNexus Squad Execution**:\n"
            task_deps += f"- **Orchestrator**: @strategy_orchestrator\n"
            task_deps += f"- **Focus Areas**: {', '.join(activation.strategynexus_focus)}\n"
            if request.competitors:
                task_deps += f"- **Competitors**: {', '.join(request.competitors)}\n"
            task_deps += f"- **Priority**: {request.urgency.title()}\n\n"
        
        task_deps += f"""**Dependencies**: All squads execute in parallel (no interdependencies)
**Coordination**: Master Orchestrator monitors progress and handles failures

### Phase 2: Synthesis & Integration (Sequential Execution)
**Timeline**: {self._estimate_phase_duration(activation, 2)}

**Tasks**:
1. **Results Aggregation**: Collect outputs from all activated squads
2. **Cross-Analysis**: Identify connections and synergies between findings
3. **Strategic Synthesis**: Combine insights into unified recommendations
4. **Quality Validation**: Ensure completeness and accuracy of analysis
5. **Report Generation**: Create executive summary and detailed findings

**Dependencies**: Phase 1 completion (all squad outputs available)

### Phase 3: Delivery & Documentation (Sequential Execution)
**Timeline**: {self._estimate_phase_duration(activation, 3)}

**Tasks**:
1. **Executive Summary Creation**: Key findings and recommendations
2. **Detailed Report Compilation**: Comprehensive analysis document
3. **Action Plan Development**: Prioritized implementation roadmap
4. **Document Export**: Convert to user-preferred formats (.docx, PDF)
5. **Results Delivery**: Present findings to user with next steps

**Dependencies**: Phase 2 completion (synthesis and integration complete)

## Quality Gates
- [ ] User intent accurately interpreted and addressed
- [ ] All activated squads completed successfully
- [ ] Cross-squad analysis identifies key insights and opportunities
- [ ] Recommendations are actionable and prioritized
- [ ] Final deliverables meet user expectations and quality standards

## Risk Mitigation
- **Squad Failure**: Graceful degradation with partial analysis delivery
- **Timeline Delays**: Priority-based delivery with core findings first
- **Quality Issues**: Built-in validation and review processes
- **User Satisfaction**: Confirmation of deliverables against original request

## Success Metrics
- **Completion Rate**: Target >95% successful execution
- **Timeline Adherence**: Target <{self._estimate_timeline(activation)} total execution
- **User Satisfaction**: Actionable insights delivered matching request intent
- **Quality Score**: Comprehensive analysis covering all requested areas
"""
        
        return task_deps
    
    def _generate_project_title(self, request: UserRequest) -> str:
        """Generate a descriptive project title"""
        if request.topics:
            topic_part = request.topics[0].title()
        elif request.urls:
            domain = request.urls[0].split('//')[1].split('/')[0]
            topic_part = domain.replace('www.', '').split('.')[0].title()
        else:
            topic_part = "Marketing"
        
        intent_part = request.intent.replace('_', ' ').title()
        return f"{topic_part} {intent_part}"
    
    def _estimate_timeline(self, activation: SquadActivation) -> str:
        """Estimate total execution timeline"""
        squad_count = sum([activation.sitespect, activation.contentforge, activation.strategynexus])
        
        if squad_count == 1:
            return "45-60 seconds"
        elif squad_count == 2:
            return "60-90 seconds"
        else:
            return "90-120 seconds"
    
    def _estimate_phase_duration(self, activation: SquadActivation, phase: int) -> str:
        """Estimate phase-specific durations"""
        squad_count = sum([activation.sitespect, activation.contentforge, activation.strategynexus])
        
        if phase == 1:  # Research & Analysis
            base_time = max(20 if activation.sitespect else 0,
                          35 if activation.contentforge else 0,
                          9 if activation.strategynexus else 0)
            return f"{base_time}-{base_time + 10} seconds"
        elif phase == 2:  # Synthesis
            return f"{squad_count * 5}-{squad_count * 10} seconds"
        else:  # Delivery
            return "5-15 seconds"
    
    def _generate_execution_strategy(self, activation: SquadActivation) -> str:
        """Generate execution strategy description"""
        strategies = []
        
        if activation.sitespect:
            strategies.append("**Technical Analysis**: Complete website audit covering SEO, performance, accessibility, and UX")
        
        if activation.contentforge:
            strategies.append("**Content Strategy**: Research-driven content planning with competitive analysis and keyword optimization")
        
        if activation.strategynexus:
            strategies.append("**Strategic Intelligence**: Competitive analysis and market positioning with advanced analytical tools")
        
        strategy_text = "\n".join(strategies)
        
        if len(strategies) > 1:
            strategy_text += f"\n\n**Integration Approach**: Parallel execution with cross-squad synthesis for comprehensive insights"
        
        return strategy_text
    
    def _generate_squad_activation_summary(self, activation: SquadActivation) -> str:
        """Generate squad activation summary"""
        summary = []
        
        if activation.sitespect:
            summary.append(f"- **SiteSpect**: ✅ Activated - Focus: {', '.join(activation.sitespect_focus)}")
        else:
            summary.append("- **SiteSpect**: ❌ Not Required")
        
        if activation.contentforge:
            summary.append(f"- **ContentForge**: ✅ Activated - Focus: {', '.join(activation.contentforge_focus)}")
        else:
            summary.append("- **ContentForge**: ❌ Not Required")
        
        if activation.strategynexus:
            summary.append(f"- **StrategyNexus**: ✅ Activated - Focus: {', '.join(activation.strategynexus_focus)}")
        else:
            summary.append("- **StrategyNexus**: ❌ Not Required")
        
        return "\n".join(summary)
    
    def _generate_deliverables_list(self, request: UserRequest, activation: SquadActivation) -> str:
        """Generate expected deliverables list"""
        deliverables = []
        
        if activation.sitespect:
            deliverables.append("- **Technical Audit Report**: Comprehensive website analysis with prioritized recommendations")
            deliverables.append("- **Performance Analysis**: Speed optimization and Core Web Vitals assessment")
            deliverables.append("- **SEO Technical Review**: Crawling, indexing, and technical SEO opportunities")
        
        if activation.contentforge:
            deliverables.append("- **Master Content Brief**: Research-driven content strategy and implementation plan")
            deliverables.append("- **Content Calendar**: Structured publication timeline with topic recommendations")
            deliverables.append("- **Keyword Strategy**: SEO-optimized keyword research and content optimization guide")
        
        if activation.strategynexus:
            deliverables.append("- **Strategic Analysis Report**: Competitive intelligence and market positioning insights")
            deliverables.append("- **Website Blueprint**: Strategic implementation roadmap with priorities")
            deliverables.append("- **Competitive Comparison**: Multi-dimensional analysis against key competitors")
        
        # Always include integrated deliverables for multi-squad execution
        if sum([activation.sitespect, activation.contentforge, activation.strategynexus]) > 1:
            deliverables.append("- **Executive Summary**: Integrated findings and strategic recommendations")
            deliverables.append("- **Implementation Roadmap**: Prioritized action plan with timelines and resources")
        
        return "\n".join(deliverables)
    
    def _generate_success_criteria(self, request: UserRequest, activation: SquadActivation) -> str:
        """Generate success criteria"""
        criteria = [
            "- **Request Fulfillment**: All aspects of original request addressed comprehensively",
            "- **Actionable Insights**: Specific, implementable recommendations provided",
            "- **Quality Standards**: Analysis meets professional consulting standards",
            "- **Timely Delivery**: Results delivered within estimated timeline"
        ]
        
        if request.urgency == 'critical':
            criteria.append("- **Urgent Priority**: Critical issues identified and prioritized for immediate action")
        
        if activation.sitespect:
            criteria.append("- **Technical Excellence**: Website audit identifies key optimization opportunities")
        
        if activation.contentforge:
            criteria.append("- **Content Strategy**: Research-backed content plan aligned with business objectives")
        
        if activation.strategynexus:
            criteria.append("- **Strategic Value**: Competitive insights provide clear strategic advantages")
        
        return "\n".join(criteria)


def save_briefs_to_files(campaign_brief: str, task_deps: str, output_dir: str = "generated_briefs") -> Tuple[str, str]:
    """Save generated briefs to markdown files"""
    
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save campaign brief
    campaign_file = output_path / f"campaign_brief_{timestamp}.md"
    with open(campaign_file, 'w', encoding='utf-8') as f:
        f.write(campaign_brief)
    
    # Save task dependencies
    task_deps_file = output_path / f"task_deps_{timestamp}.md"
    with open(task_deps_file, 'w', encoding='utf-8') as f:
        f.write(task_deps)
    
    logger.info(f"Briefs saved to: {campaign_file} and {task_deps_file}")
    
    return str(campaign_file), str(task_deps_file)


# Example usage and testing
if __name__ == "__main__":
    generator = BriefGenerator()
    
    # Test cases
    test_requests = [
        "Audit my website example.com and create content strategy for sustainable fashion",
        "Compare our site to competitors and suggest improvements",
        "Create content briefs for B2B SaaS marketing campaign",
        "Urgent: Complete analysis of e-commerce site performance and competitive landscape"
    ]
    
    for request in test_requests:
        print(f"\n{'='*60}")
        print(f"Processing: {request}")
        print(f"{'='*60}")
        
        campaign_brief, task_deps = generator.generate_briefs(request)
        
        print("\n--- CAMPAIGN BRIEF ---")
        print(campaign_brief[:500] + "..." if len(campaign_brief) > 500 else campaign_brief)
        
        print("\n--- TASK DEPENDENCIES ---") 
        print(task_deps[:500] + "..." if len(task_deps) > 500 else task_deps)