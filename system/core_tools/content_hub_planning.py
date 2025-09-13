"""
Content Hub and Pillar Page Planning System for Bigger Boss Agent System
Implements comprehensive content hub strategies with pillar page architecture.
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class PillarPage:
    """Structure for pillar pages in content hub"""
    id: str
    title: str
    topic: str
    target_keywords: List[str]
    search_intent: str
    word_count_target: int
    authority_score: float
    internal_links_target: int
    cluster_themes: List[str]
    content_depth: str  # comprehensive, detailed, overview
    business_objective: str
    conversion_funnel_stage: str  # awareness, consideration, decision
    priority_level: str  # high, medium, low
    estimated_traffic_potential: int


@dataclass
class SupportingContent:
    """Structure for supporting content pieces"""
    id: str
    title: str
    content_type: str  # blog_post, guide, case_study, faq, infographic
    pillar_page_id: str
    target_keywords: List[str]
    word_count_target: int
    internal_links_to_pillar: int
    external_links_target: int
    content_angle: str
    audience_segment: str
    publication_timeline: str
    content_format: str  # text, video, infographic, interactive


@dataclass
class ContentHub:
    """Complete content hub structure"""
    id: str
    name: str
    primary_topic: str
    business_objectives: List[str]
    target_audience: Dict[str, Any]
    pillar_pages: List[PillarPage]
    supporting_content: List[SupportingContent]
    internal_linking_strategy: Dict[str, Any]
    content_calendar: Dict[str, Any]
    performance_metrics: Dict[str, Any]
    seo_strategy: Dict[str, Any]


class ContentHubPlanner:
    """Advanced content hub and pillar page planning system"""
    
    def __init__(self):
        self.hubs_storage_path = Path("C:/Apps/Agents/Bigger Boss/bigger-boss/system/content_hubs")
        self.hubs_storage_path.mkdir(exist_ok=True)
        self.templates_path = Path("C:/Apps/Agents/Bigger Boss/bigger-boss/system/templates/content_hubs")
        self.templates_path.mkdir(parents=True, exist_ok=True)
    
    def create_content_hub_strategy(self, client_domain: str, primary_topic: str, 
                                  business_objectives: List[str], 
                                  target_audience: Dict[str, Any]) -> ContentHub:
        """Create comprehensive content hub strategy"""
        logger.info(f"Creating content hub strategy for {client_domain}: {primary_topic}")
        
        hub_id = str(uuid.uuid4())[:8]
        hub_name = f"{primary_topic.title()} Content Hub"
        
        # Generate pillar pages based on topic analysis
        pillar_pages = self._generate_pillar_pages(primary_topic, business_objectives, target_audience)
        
        # Generate supporting content for each pillar
        supporting_content = []
        for pillar in pillar_pages:
            pillar_support = self._generate_supporting_content(pillar, target_audience)
            supporting_content.extend(pillar_support)
        
        # Create internal linking strategy
        internal_linking = self._design_internal_linking_strategy(pillar_pages, supporting_content)
        
        # Generate content calendar
        content_calendar = self._create_content_calendar(pillar_pages, supporting_content)
        
        # Define performance metrics
        performance_metrics = self._define_performance_metrics(business_objectives)
        
        # Create SEO strategy
        seo_strategy = self._create_hub_seo_strategy(primary_topic, pillar_pages)
        
        content_hub = ContentHub(
            id=hub_id,
            name=hub_name,
            primary_topic=primary_topic,
            business_objectives=business_objectives,
            target_audience=target_audience,
            pillar_pages=pillar_pages,
            supporting_content=supporting_content,
            internal_linking_strategy=internal_linking,
            content_calendar=content_calendar,
            performance_metrics=performance_metrics,
            seo_strategy=seo_strategy
        )
        
        # Save content hub strategy
        self._save_content_hub(client_domain, content_hub)
        
        return content_hub
    
    def _generate_pillar_pages(self, primary_topic: str, business_objectives: List[str], 
                              target_audience: Dict[str, Any]) -> List[PillarPage]:
        """Generate pillar pages for content hub"""
        logger.info(f"Generating pillar pages for topic: {primary_topic}")
        
        # Define pillar page themes based on common business patterns
        pillar_themes = self._identify_pillar_themes(primary_topic, business_objectives)
        
        pillar_pages = []
        
        for i, theme in enumerate(pillar_themes):
            pillar_id = str(uuid.uuid4())[:8]
            
            # Determine search intent based on theme
            search_intent = self._determine_search_intent(theme)
            
            # Generate target keywords
            target_keywords = self._generate_pillar_keywords(primary_topic, theme)
            
            # Determine conversion funnel stage
            funnel_stage = self._determine_funnel_stage(theme, search_intent)
            
            # Calculate authority score potential
            authority_score = self._calculate_authority_potential(theme, primary_topic)
            
            pillar_page = PillarPage(
                id=pillar_id,
                title=f"Complete Guide to {theme.title()} in {primary_topic.title()}",
                topic=theme,
                target_keywords=target_keywords,
                search_intent=search_intent,
                word_count_target=self._determine_word_count_target(search_intent, theme),
                authority_score=authority_score,
                internal_links_target=self._calculate_internal_links_target(i + 1, len(pillar_themes)),
                cluster_themes=self._identify_cluster_themes(theme, primary_topic),
                content_depth="comprehensive",
                business_objective=self._map_business_objective(theme, business_objectives),
                conversion_funnel_stage=funnel_stage,
                priority_level=self._determine_priority_level(i, authority_score, funnel_stage),
                estimated_traffic_potential=self._estimate_traffic_potential(target_keywords, search_intent)
            )
            
            pillar_pages.append(pillar_page)
        
        return pillar_pages
    
    def _identify_pillar_themes(self, primary_topic: str, business_objectives: List[str]) -> List[str]:
        """Identify key pillar themes based on topic and objectives"""
        
        # Common business pillar patterns
        theme_patterns = {
            "digital marketing": [
                "strategy and planning",
                "implementation and execution", 
                "measurement and optimization",
                "tools and technologies",
                "industry trends and insights"
            ],
            "seo": [
                "technical seo fundamentals",
                "content optimization strategies",
                "link building and authority",
                "local seo techniques",
                "seo tools and analytics"
            ],
            "content marketing": [
                "content strategy development",
                "content creation and production",
                "content distribution and promotion",
                "content performance measurement",
                "content team and workflow"
            ],
            "social media marketing": [
                "platform strategy and selection",
                "content creation and curation",
                "community management and engagement",
                "social media advertising",
                "social media analytics and roi"
            ]
        }
        
        # Find matching pattern or create generic themes
        topic_lower = primary_topic.lower()
        
        for pattern_key in theme_patterns:
            if pattern_key in topic_lower:
                return theme_patterns[pattern_key]
        
        # Generic business themes if no specific pattern found
        return [
            f"{primary_topic} fundamentals and basics",
            f"advanced {primary_topic} strategies", 
            f"{primary_topic} tools and resources",
            f"{primary_topic} case studies and examples",
            f"future of {primary_topic} and trends"
        ]
    
    def _determine_search_intent(self, theme: str) -> str:
        """Determine search intent based on theme"""
        intent_keywords = {
            "informational": ["guide", "what", "how", "fundamentals", "basics", "insights", "trends"],
            "navigational": ["tools", "resources", "platforms", "software"],
            "commercial": ["best", "comparison", "review", "vs", "alternatives"],
            "transactional": ["services", "solutions", "hire", "buy", "get"]
        }
        
        theme_lower = theme.lower()
        
        for intent, keywords in intent_keywords.items():
            if any(keyword in theme_lower for keyword in keywords):
                return intent
        
        return "informational"  # Default
    
    def _generate_pillar_keywords(self, primary_topic: str, theme: str) -> List[str]:
        """Generate target keywords for pillar page"""
        base_keywords = [
            f"{primary_topic}",
            f"{primary_topic} {theme}",
            f"{theme} for {primary_topic}",
            f"best {primary_topic} {theme}",
            f"{primary_topic} {theme} guide"
        ]
        
        # Add long-tail variations
        long_tail = [
            f"how to use {theme} for {primary_topic}",
            f"{primary_topic} {theme} strategies",
            f"{primary_topic} {theme} tips",
            f"{theme} in {primary_topic} industry"
        ]
        
        return base_keywords + long_tail
    
    def _determine_funnel_stage(self, theme: str, search_intent: str) -> str:
        """Determine conversion funnel stage"""
        if search_intent == "transactional":
            return "decision"
        elif search_intent == "commercial":
            return "consideration" 
        elif "advanced" in theme.lower() or "strategy" in theme.lower():
            return "consideration"
        else:
            return "awareness"
    
    def _calculate_authority_potential(self, theme: str, primary_topic: str) -> float:
        """Calculate potential authority score for pillar page"""
        # Base score
        authority = 0.6
        
        # Boost for comprehensive themes
        if any(word in theme.lower() for word in ["fundamentals", "complete", "comprehensive"]):
            authority += 0.2
            
        # Boost for advanced themes
        if any(word in theme.lower() for word in ["advanced", "expert", "professional"]):
            authority += 0.15
            
        # Boost for trending themes
        if any(word in theme.lower() for word in ["trends", "future", "latest"]):
            authority += 0.1
        
        return min(authority, 1.0)
    
    def _determine_word_count_target(self, search_intent: str, theme: str) -> int:
        """Determine target word count for pillar page"""
        base_counts = {
            "informational": 3500,
            "navigational": 2800,
            "commercial": 3200,
            "transactional": 2500
        }
        
        base_count = base_counts.get(search_intent, 3000)
        
        # Adjust for theme complexity
        if any(word in theme.lower() for word in ["complete", "comprehensive", "ultimate"]):
            base_count += 1500
        elif any(word in theme.lower() for word in ["advanced", "expert"]):
            base_count += 1000
        elif any(word in theme.lower() for word in ["basics", "introduction"]):
            base_count -= 500
        
        return max(base_count, 2000)  # Minimum 2000 words for pillar pages
    
    def _calculate_internal_links_target(self, position: int, total_pillars: int) -> int:
        """Calculate internal links target for pillar page"""
        # Primary pillars get more internal links
        if position <= 2:
            return 25 + (total_pillars * 3)
        elif position <= 4:
            return 20 + (total_pillars * 2)
        else:
            return 15 + total_pillars
    
    def _identify_cluster_themes(self, theme: str, primary_topic: str) -> List[str]:
        """Identify supporting cluster themes"""
        cluster_patterns = {
            "fundamentals": ["basics", "getting started", "introduction", "overview"],
            "strategy": ["planning", "tactics", "approaches", "methods"],
            "tools": ["software", "platforms", "resources", "applications"],
            "measurement": ["analytics", "tracking", "metrics", "reporting"],
            "trends": ["future", "emerging", "innovations", "developments"]
        }
        
        theme_lower = theme.lower()
        
        for pattern_key, clusters in cluster_patterns.items():
            if pattern_key in theme_lower:
                return [f"{cluster} for {primary_topic}" for cluster in clusters]
        
        # Generic clusters
        return [
            f"{theme} examples",
            f"{theme} best practices", 
            f"{theme} case studies",
            f"{theme} mistakes to avoid"
        ]
    
    def _map_business_objective(self, theme: str, business_objectives: List[str]) -> str:
        """Map theme to relevant business objective"""
        theme_lower = theme.lower()
        
        objective_mapping = {
            "lead generation": ["fundamentals", "basics", "getting started"],
            "brand awareness": ["trends", "insights", "industry"],
            "customer education": ["guide", "how-to", "tutorial", "advanced"],
            "thought leadership": ["expert", "professional", "strategy"],
            "conversion optimization": ["tools", "resources", "comparison"]
        }
        
        for objective in business_objectives:
            objective_lower = objective.lower()
            if any(keyword in objective_lower for keyword in ["lead", "generation"]):
                return "lead generation"
            elif any(keyword in objective_lower for keyword in ["brand", "awareness"]):
                return "brand awareness"
            elif any(keyword in objective_lower for keyword in ["education", "inform"]):
                return "customer education"
        
        # Default mapping based on theme
        for objective, keywords in objective_mapping.items():
            if any(keyword in theme_lower for keyword in keywords):
                return objective
        
        return business_objectives[0] if business_objectives else "brand awareness"
    
    def _determine_priority_level(self, position: int, authority_score: float, 
                                funnel_stage: str) -> str:
        """Determine priority level for pillar page"""
        score = 0
        
        # Position bonus (earlier = higher priority)
        if position == 0:
            score += 3
        elif position <= 2:
            score += 2
        elif position <= 4:
            score += 1
        
        # Authority score bonus
        if authority_score >= 0.8:
            score += 2
        elif authority_score >= 0.7:
            score += 1
        
        # Funnel stage bonus
        if funnel_stage == "decision":
            score += 2
        elif funnel_stage == "consideration":
            score += 1
        
        if score >= 5:
            return "high"
        elif score >= 3:
            return "medium"
        else:
            return "low"
    
    def _estimate_traffic_potential(self, keywords: List[str], search_intent: str) -> int:
        """Estimate traffic potential for pillar page"""
        base_traffic = {
            "informational": 2500,
            "navigational": 1800,
            "commercial": 2200,
            "transactional": 1500
        }
        
        base = base_traffic.get(search_intent, 2000)
        
        # Adjust for keyword count
        keyword_multiplier = len(keywords) * 0.15
        
        # Random variation for realism
        import random
        variation = random.uniform(0.8, 1.3)
        
        return int(base * (1 + keyword_multiplier) * variation)
    
    def _generate_supporting_content(self, pillar_page: PillarPage, 
                                   target_audience: Dict[str, Any]) -> List[SupportingContent]:
        """Generate supporting content for pillar page"""
        logger.info(f"Generating supporting content for pillar: {pillar_page.title}")
        
        supporting_content = []
        
        # Generate different types of supporting content
        content_types = [
            ("blog_post", "in-depth article"),
            ("guide", "step-by-step guide"), 
            ("case_study", "real-world example"),
            ("faq", "frequently asked questions"),
            ("infographic", "visual summary")
        ]
        
        for i, (content_type, angle) in enumerate(content_types):
            if i >= 6:  # Limit to 6 pieces per pillar
                break
                
            content_id = str(uuid.uuid4())[:8]
            
            supporting_piece = SupportingContent(
                id=content_id,
                title=f"{pillar_page.topic.title()}: {angle.title()}",
                content_type=content_type,
                pillar_page_id=pillar_page.id,
                target_keywords=self._generate_supporting_keywords(pillar_page, angle),
                word_count_target=self._determine_supporting_word_count(content_type),
                internal_links_to_pillar=1,
                external_links_target=self._determine_external_links_target(content_type),
                content_angle=angle,
                audience_segment=self._determine_audience_segment(content_type, target_audience),
                publication_timeline=self._calculate_publication_timeline(i, content_type),
                content_format=self._determine_content_format(content_type)
            )
            
            supporting_content.append(supporting_piece)
        
        return supporting_content
    
    def _generate_supporting_keywords(self, pillar_page: PillarPage, angle: str) -> List[str]:
        """Generate keywords for supporting content"""
        base_keyword = pillar_page.topic
        
        keywords = [
            f"{base_keyword} {angle}",
            f"how to {base_keyword}",
            f"{base_keyword} examples",
            f"{base_keyword} tips"
        ]
        
        # Add angle-specific keywords
        if "guide" in angle:
            keywords.extend([f"{base_keyword} tutorial", f"{base_keyword} walkthrough"])
        elif "case study" in angle:
            keywords.extend([f"{base_keyword} success story", f"{base_keyword} results"])
        elif "faq" in angle:
            keywords.extend([f"{base_keyword} questions", f"{base_keyword} answers"])
        
        return keywords
    
    def _determine_supporting_word_count(self, content_type: str) -> int:
        """Determine word count for supporting content"""
        word_counts = {
            "blog_post": 1800,
            "guide": 2500, 
            "case_study": 2000,
            "faq": 1200,
            "infographic": 500  # Accompanying text
        }
        
        return word_counts.get(content_type, 1500)
    
    def _determine_external_links_target(self, content_type: str) -> int:
        """Determine external links target"""
        link_counts = {
            "blog_post": 4,
            "guide": 6,
            "case_study": 3,
            "faq": 2,
            "infographic": 2
        }
        
        return link_counts.get(content_type, 3)
    
    def _determine_audience_segment(self, content_type: str, 
                                  target_audience: Dict[str, Any]) -> str:
        """Determine audience segment for content"""
        if "segments" in target_audience:
            segments = target_audience["segments"]
            if content_type == "guide":
                return segments.get("beginners", "general audience")
            elif content_type == "case_study":
                return segments.get("decision_makers", "business owners")
            elif content_type == "faq":
                return segments.get("prospects", "potential customers")
        
        return target_audience.get("primary_segment", "general audience")
    
    def _calculate_publication_timeline(self, position: int, content_type: str) -> str:
        """Calculate publication timeline"""
        base_weeks = 2 + position
        
        if content_type in ["guide", "case_study"]:
            base_weeks += 1
        
        return f"Week {base_weeks}"
    
    def _determine_content_format(self, content_type: str) -> str:
        """Determine content format"""
        format_mapping = {
            "blog_post": "text",
            "guide": "text + images",
            "case_study": "text + data visualisation",
            "faq": "text + expandable sections",
            "infographic": "visual + minimal text"
        }
        
        return format_mapping.get(content_type, "text")
    
    def _design_internal_linking_strategy(self, pillar_pages: List[PillarPage], 
                                        supporting_content: List[SupportingContent]) -> Dict[str, Any]:
        """Design internal linking strategy for content hub"""
        
        strategy = {
            "hub_architecture": "pillar_and_cluster",
            "linking_principles": [
                "All supporting content links to relevant pillar pages",
                "Pillar pages link to each other where contextually relevant",
                "Supporting content cross-links within same topic cluster",
                "Hub pages link to external authority sources"
            ],
            "link_distribution": {
                "pillar_to_pillar": f"2-3 links per pillar page",
                "supporting_to_pillar": "1-2 links per supporting piece",
                "pillar_to_supporting": f"5-8 links per pillar to cluster content",
                "supporting_cross_links": "1-2 relevant cross-links"
            },
            "anchor_text_strategy": {
                "primary_keywords": "30% exact match",
                "partial_keywords": "40% partial match", 
                "branded_terms": "20% brand terms",
                "natural_language": "10% natural phrases"
            },
            "link_monitoring": {
                "internal_link_equity": "Track PageRank flow through hub",
                "click_through_rates": "Monitor internal CTR performance",
                "user_journey_analysis": "Analyse navigation patterns"
            }
        }
        
        return strategy
    
    def _create_content_calendar(self, pillar_pages: List[PillarPage], 
                               supporting_content: List[SupportingContent]) -> Dict[str, Any]:
        """Create content calendar for hub"""
        
        calendar = {
            "publication_strategy": "pillar-first_approach",
            "timeline_overview": "12-week implementation plan",
            "phase_1_pillars": [
                {
                    "pillar_id": pillar.id,
                    "title": pillar.title,
                    "publication_week": f"Week {i+2}",
                    "priority": pillar.priority_level
                }
                for i, pillar in enumerate(pillar_pages[:3])  # First 3 pillars
            ],
            "phase_2_pillars": [
                {
                    "pillar_id": pillar.id,
                    "title": pillar.title,
                    "publication_week": f"Week {i+6}",
                    "priority": pillar.priority_level
                }
                for i, pillar in enumerate(pillar_pages[3:])  # Remaining pillars
            ],
            "supporting_content_schedule": [
                {
                    "content_id": content.id,
                    "title": content.title,
                    "content_type": content.content_type,
                    "publication_timeline": content.publication_timeline,
                    "pillar_connection": content.pillar_page_id
                }
                for content in supporting_content
            ],
            "maintenance_schedule": {
                "content_updates": "Monthly review and refresh",
                "link_validation": "Quarterly internal link audit",
                "performance_review": "Monthly traffic and ranking analysis",
                "content_expansion": "Quarterly new supporting content addition"
            }
        }
        
        return calendar
    
    def _define_performance_metrics(self, business_objectives: List[str]) -> Dict[str, Any]:
        """Define performance metrics for content hub"""
        
        base_metrics = {
            "seo_metrics": {
                "organic_traffic_growth": "Target: 40% increase within 6 months",
                "keyword_ranking_improvements": "Target: Top 10 for 60% of target keywords",
                "featured_snippet_captures": "Target: 3-5 featured snippets",
                "backlink_acquisition": "Target: 25 high-quality backlinks"
            },
            "engagement_metrics": {
                "average_session_duration": "Target: 4+ minutes per session",
                "pages_per_session": "Target: 2.5+ pages per session",
                "bounce_rate": "Target: <45% bounce rate",
                "internal_click_through_rate": "Target: 8%+ internal CTR"
            },
            "conversion_metrics": {
                "lead_generation": "Target: 15% increase in qualified leads",
                "email_subscriptions": "Target: 200 new subscribers per month",
                "content_downloads": "Target: 50 downloads per pillar page",
                "consultation_requests": "Target: 25% increase in enquiries"
            }
        }
        
        # Customise metrics based on business objectives
        if any("brand awareness" in obj.lower() for obj in business_objectives):
            base_metrics["brand_metrics"] = {
                "brand_mention_increase": "Target: 30% increase in brand mentions",
                "social_media_shares": "Target: 500 shares per pillar page",
                "direct_traffic_growth": "Target: 20% increase in direct traffic"
            }
        
        if any("lead generation" in obj.lower() for obj in business_objectives):
            base_metrics["lead_metrics"] = {
                "cost_per_lead_reduction": "Target: 25% reduction in CPL",
                "lead_quality_score": "Target: 8.5/10 average lead quality",
                "conversion_rate": "Target: 3.5% content-to-lead conversion"
            }
        
        return base_metrics
    
    def _create_hub_seo_strategy(self, primary_topic: str, 
                               pillar_pages: List[PillarPage]) -> Dict[str, Any]:
        """Create SEO strategy for content hub"""
        
        seo_strategy = {
            "keyword_strategy": {
                "primary_focus": primary_topic,
                "semantic_keywords": self._generate_semantic_keywords(primary_topic),
                "long_tail_opportunities": self._identify_long_tail_opportunities(pillar_pages),
                "competitor_gap_keywords": f"Research competitor content gaps for {primary_topic}"
            },
            "technical_seo": {
                "url_structure": f"/{primary_topic.lower().replace(' ', '-')}/pillar-topic/",
                "internal_linking": "Hub and spoke model with pillar pages as hubs",
                "schema_markup": "Article, HowTo, and FAQ schema implementation",
                "site_speed": "Target: <3 second load times for all hub pages"
            },
            "content_optimisation": {
                "title_tag_format": "Primary Keyword | Secondary Keyword | Brand",
                "meta_description_approach": "Compelling 150-character summaries with CTA",
                "header_structure": "H1 (main topic) → H2 (pillar themes) → H3 (subtopics)",
                "image_optimisation": "Alt text, file naming, and compression for all images"
            },
            "authority_building": {
                "expert_content": "Include expert quotes and industry insights",
                "original_research": "Conduct surveys or studies for unique data",
                "thought_leadership": "Position content as industry-leading resource",
                "citation_strategy": "Reference and cite authoritative sources"
            }
        }
        
        return seo_strategy
    
    def _generate_semantic_keywords(self, primary_topic: str) -> List[str]:
        """Generate semantic keywords for topic"""
        semantic_patterns = [
            f"{primary_topic} strategies",
            f"{primary_topic} techniques",
            f"{primary_topic} methods",
            f"{primary_topic} best practices",
            f"{primary_topic} solutions",
            f"how to improve {primary_topic}",
            f"{primary_topic} tips and tricks",
            f"{primary_topic} for beginners"
        ]
        
        return semantic_patterns
    
    def _identify_long_tail_opportunities(self, pillar_pages: List[PillarPage]) -> List[str]:
        """Identify long-tail keyword opportunities"""
        long_tail_keywords = []
        
        for pillar in pillar_pages:
            topic = pillar.topic
            long_tail_keywords.extend([
                f"how to implement {topic}",
                f"best {topic} strategies for small business",
                f"{topic} mistakes to avoid",
                f"{topic} vs alternatives comparison",
                f"why {topic} is important for business"
            ])
        
        return long_tail_keywords[:20]  # Return top 20
    
    def _save_content_hub(self, client_domain: str, content_hub: ContentHub):
        """Save content hub strategy to file"""
        try:
            filename = f"content_hub_{client_domain}_{content_hub.id}.json"
            filepath = self.hubs_storage_path / filename
            
            # Convert dataclass to dict for JSON serialisation
            hub_dict = asdict(content_hub)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(hub_dict, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Content hub strategy saved: {filepath}")
            
        except Exception as e:
            logger.error(f"Failed to save content hub: {str(e)}")
    
    def generate_content_hub_briefs(self, content_hub: ContentHub, 
                                   client_domain: str) -> Dict[str, str]:
        """Generate detailed content briefs for all hub content"""
        logger.info(f"Generating content briefs for {content_hub.name}")
        
        briefs = {}
        
        # Generate pillar page briefs
        for pillar in content_hub.pillar_pages:
            brief = self._generate_pillar_page_brief(pillar, content_hub)
            briefs[f"pillar_{pillar.id}"] = brief
        
        # Generate supporting content briefs
        for supporting in content_hub.supporting_content:
            brief = self._generate_supporting_content_brief(supporting, content_hub)
            briefs[f"supporting_{supporting.id}"] = brief
        
        # Save briefs to files
        self._save_content_briefs(client_domain, content_hub.id, briefs)
        
        return briefs
    
    def _generate_pillar_page_brief(self, pillar: PillarPage, 
                                   content_hub: ContentHub) -> str:
        """Generate detailed brief for pillar page"""
        brief = f"""
# Content Brief: {pillar.title}

## Overview
**Content Type:** Pillar Page
**Topic:** {pillar.topic}
**Priority:** {pillar.priority_level.upper()}
**Target Word Count:** {pillar.word_count_target:,} words

## SEO Strategy
**Primary Keywords:** {', '.join(pillar.target_keywords[:3])}
**Secondary Keywords:** {', '.join(pillar.target_keywords[3:6])}
**Search Intent:** {pillar.search_intent.title()}
**Estimated Traffic Potential:** {pillar.estimated_traffic_potential:,} monthly visits

## Content Structure
**Content Depth:** {pillar.content_depth.title()}
**Recommended H2 Sections:** {len(pillar.cluster_themes)} main sections based on cluster themes:
{chr(10).join(f"- {theme.title()}" for theme in pillar.cluster_themes)}

## Internal Linking Strategy
**Target Internal Links:** {pillar.internal_links_target} internal links
**Link Distribution:**
- Links to other pillar pages: 3-4 links
- Links to supporting content: {pillar.internal_links_target - 8} links
- Links to category/hub pages: 2-3 links

## Conversion Strategy
**Business Objective:** {pillar.business_objective.title()}
**Funnel Stage:** {pillar.conversion_funnel_stage.title()}
**Authority Score Target:** {pillar.authority_score:.1f}/1.0

## Content Guidelines
1. Comprehensive coverage of {pillar.topic}
2. Expert-level insights and practical advice
3. Include relevant statistics and data (with citations)
4. Add visual elements (infographics, charts, diagrams)
5. Include actionable takeaways and next steps
6. Optimise for featured snippets and voice search
7. Include FAQ section addressing common questions

## Success Metrics
- Rank in top 5 for primary keywords within 6 months
- Generate {pillar.estimated_traffic_potential:,}+ monthly organic visits
- Achieve {pillar.internal_links_target}+ internal links from other content
- Maintain authority score of {pillar.authority_score:.1f}+
"""
        return brief.strip()
    
    def _generate_supporting_content_brief(self, supporting: SupportingContent, 
                                          content_hub: ContentHub) -> str:
        """Generate detailed brief for supporting content"""
        # Find connected pillar page
        pillar = next((p for p in content_hub.pillar_pages if p.id == supporting.pillar_page_id), None)
        pillar_title = pillar.title if pillar else "Related Pillar Page"
        
        brief = f"""
# Content Brief: {supporting.title}

## Overview
**Content Type:** {supporting.content_type.replace('_', ' ').title()}
**Content Format:** {supporting.content_format.title()}
**Content Angle:** {supporting.content_angle.title()}
**Target Word Count:** {supporting.word_count_target:,} words

## Connection Strategy
**Connected Pillar Page:** {pillar_title}
**Links to Pillar:** {supporting.internal_links_to_pillar} direct link(s)
**Publication Timeline:** {supporting.publication_timeline}

## SEO Strategy
**Target Keywords:** {', '.join(supporting.target_keywords[:5])}
**External Links Target:** {supporting.external_links_target} authoritative external links

## Audience
**Target Segment:** {supporting.audience_segment.title()}

## Content Requirements
**Format:** {supporting.content_format}
**Angle:** Focus on {supporting.content_angle}

### Content Type Specific Guidelines:
"""
        
        # Add content type specific guidelines
        if supporting.content_type == "blog_post":
            brief += """
- Engaging introduction with hook
- 3-5 main sections with H2 headers
- Practical tips and actionable advice
- Conclusion with clear next steps
- Include relevant images and examples
"""
        elif supporting.content_type == "guide":
            brief += """
- Step-by-step format with numbered sections
- Screenshots or diagrams for each major step
- Prerequisites and requirements section
- Troubleshooting or common mistakes section
- Downloadable checklist or template
"""
        elif supporting.content_type == "case_study":
            brief += """
- Background/challenge section
- Solution approach and implementation
- Results with specific metrics and data
- Key learnings and takeaways
- Call-to-action for similar services
"""
        elif supporting.content_type == "faq":
            brief += """
- 8-12 frequently asked questions
- Expandable format with detailed answers
- Group questions by topic/category
- Include links to related pillar content
- Optimise for voice search queries
"""
        elif supporting.content_type == "infographic":
            brief += """
- Visually appealing design with brand colours
- 5-7 key data points or statistics
- Minimal text with high impact
- Downloadable and shareable format
- Accompanying blog post with full details
"""
        
        brief += f"""

## Success Metrics
- Support pillar page rankings through relevant internal linking
- Generate qualified traffic for {supporting.audience_segment}
- Achieve target word count and external link goals
- Maintain content quality score of 8.5+/10
"""
        
        return brief.strip()
    
    def _save_content_briefs(self, client_domain: str, hub_id: str, 
                           briefs: Dict[str, str]):
        """Save content briefs to individual files"""
        try:
            briefs_dir = self.hubs_storage_path / f"briefs_{client_domain}_{hub_id}"
            briefs_dir.mkdir(exist_ok=True)
            
            for brief_id, brief_content in briefs.items():
                filename = f"{brief_id}_brief.md"
                filepath = briefs_dir / filename
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(brief_content)
            
            logger.info(f"Content briefs saved to: {briefs_dir}")
            
        except Exception as e:
            logger.error(f"Failed to save content briefs: {str(e)}")


# Initialize content hub planner
content_hub_planner = ContentHubPlanner()

# Export main components
__all__ = [
    'ContentHubPlanner',
    'ContentHub',
    'PillarPage', 
    'SupportingContent',
    'content_hub_planner'
]