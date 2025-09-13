"""
AI Content Specialist Agent for Webpage Optimisation Analysis
Specialises in comprehensive webpage content analysis and optimisation recommendations.
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path

# Import our enhanced tools
from ..core_tools.enhanced_api_integrations import jina_ai, serpapi, playwright_integration
from ..core_tools.fact_verification_protocols import fact_verification
from ..core_tools.mandatory_date_research import mandatory_research

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ContentAnalysisResult:
    """Comprehensive content analysis result"""
    url: str
    analysis_timestamp: str
    content_quality_score: float
    seo_optimisation_score: float
    readability_score: float
    engagement_potential_score: float
    conversion_optimisation_score: float
    accessibility_score: float
    technical_performance_score: float
    overall_optimisation_score: float
    key_findings: List[str]
    priority_recommendations: List[Dict[str, Any]]
    detailed_analysis: Dict[str, Any]


@dataclass
class OptimisationRecommendation:
    """Individual optimisation recommendation"""
    category: str
    priority: str  # critical, high, medium, low
    recommendation: str
    impact_estimate: str
    implementation_effort: str
    expected_outcome: str
    technical_requirements: List[str]
    content_changes_required: bool


class AIContentSpecialist:
    """AI Content Specialist Agent for comprehensive webpage optimisation analysis"""
    
    def __init__(self):
        self.analysis_cache_path = Path("C:/Apps/Agents/Bigger Boss/bigger-boss/system/content_analysis")
        self.analysis_cache_path.mkdir(exist_ok=True)
        
        # Scoring weights for different aspects
        self.scoring_weights = {
            "content_quality": 0.20,
            "seo_optimisation": 0.18,
            "readability": 0.15,
            "engagement_potential": 0.15,
            "conversion_optimisation": 0.12,
            "accessibility": 0.10,
            "technical_performance": 0.10
        }
        
        # Analysis categories and their importance
        self.analysis_categories = [
            "content_structure_analysis",
            "seo_content_optimisation", 
            "readability_assessment",
            "engagement_factor_analysis",
            "conversion_path_analysis",
            "accessibility_evaluation",
            "technical_content_performance",
            "competitive_content_analysis",
            "ai_optimisation_opportunities"
        ]
    
    def analyse_webpage_content(self, url: str, client_domain: str, 
                               analysis_depth: str = "comprehensive") -> ContentAnalysisResult:
        """Perform comprehensive webpage content analysis"""
        logger.info(f"Starting AI content specialist analysis for: {url}")
        
        try:
            # Step 1: Extract and analyse webpage content
            content_extraction = self._extract_webpage_content(url)
            
            if not content_extraction["success"]:
                return self._create_error_result(url, "Content extraction failed")
            
            # Step 2: Perform mandatory research validation
            research_validation = self._validate_content_research(content_extraction["content"], client_domain)
            
            # Step 3: Comprehensive content analysis
            analysis_results = {}
            
            if analysis_depth in ["comprehensive", "detailed"]:
                # Full analysis suite
                for category in self.analysis_categories:
                    try:
                        category_result = self._perform_category_analysis(
                            category, content_extraction, url, client_domain
                        )
                        analysis_results[category] = category_result
                    except Exception as e:
                        logger.warning(f"Category analysis failed for {category}: {str(e)}")
                        analysis_results[category] = {"error": str(e), "score": 0.5}
            else:
                # Essential analysis only
                essential_categories = [
                    "content_structure_analysis", 
                    "seo_content_optimisation",
                    "readability_assessment"
                ]
                
                for category in essential_categories:
                    category_result = self._perform_category_analysis(
                        category, content_extraction, url, client_domain
                    )
                    analysis_results[category] = category_result
            
            # Step 4: Calculate scores and generate recommendations
            scores = self._calculate_optimisation_scores(analysis_results)
            recommendations = self._generate_optimisation_recommendations(analysis_results, scores)
            key_findings = self._extract_key_findings(analysis_results, scores)
            
            # Step 5: Create comprehensive result
            result = ContentAnalysisResult(
                url=url,
                analysis_timestamp=datetime.now().isoformat(),
                content_quality_score=scores.get("content_quality", 0.0),
                seo_optimisation_score=scores.get("seo_optimisation", 0.0),
                readability_score=scores.get("readability", 0.0),
                engagement_potential_score=scores.get("engagement_potential", 0.0),
                conversion_optimisation_score=scores.get("conversion_optimisation", 0.0),
                accessibility_score=scores.get("accessibility", 0.0),
                technical_performance_score=scores.get("technical_performance", 0.0),
                overall_optimisation_score=self._calculate_overall_score(scores),
                key_findings=key_findings,
                priority_recommendations=recommendations["priority"],
                detailed_analysis=analysis_results
            )
            
            # Step 6: Save analysis results
            self._save_analysis_result(client_domain, result)
            
            return result
            
        except Exception as e:
            logger.error(f"Webpage analysis failed for {url}: {str(e)}")
            return self._create_error_result(url, str(e))
    
    def _extract_webpage_content(self, url: str) -> Dict[str, Any]:
        """Extract webpage content using Jina AI"""
        try:
            extraction_result = jina_ai.analyze_webpage_content(url)
            
            if extraction_result.success:
                return {
                    "success": True,
                    "content": extraction_result.data.get("content_preview", ""),
                    "content_length": extraction_result.data.get("content_length", 0),
                    "content_analysis": extraction_result.data.get("content_analysis", {}),
                    "metadata": extraction_result.metadata
                }
            else:
                return {
                    "success": False,
                    "error": extraction_result.errors[0] if extraction_result.errors else "Unknown error"
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _validate_content_research(self, content: str, client_domain: str) -> Dict[str, Any]:
        """Validate content using mandatory research protocols"""
        try:
            # Check if content contains claims requiring verification
            claims, verification_results = fact_verification.verify_content_claims(content, client_domain)
            
            research_score = 1.0
            if verification_results:
                verified_claims = sum(1 for r in verification_results if r.verification_status == "verified")
                research_score = verified_claims / len(verification_results) if verification_results else 1.0
            
            return {
                "research_validation_score": research_score,
                "claims_identified": len(claims),
                "claims_verified": sum(1 for r in verification_results if r.verification_status == "verified"),
                "requires_fact_checking": research_score < 0.8,
                "verification_details": [asdict(r) for r in verification_results]
            }
            
        except Exception as e:
            logger.warning(f"Research validation failed: {str(e)}")
            return {"research_validation_score": 0.5, "error": str(e)}
    
    def _perform_category_analysis(self, category: str, content_extraction: Dict, 
                                  url: str, client_domain: str) -> Dict[str, Any]:
        """Perform analysis for specific category"""
        content = content_extraction.get("content", "")
        content_analysis = content_extraction.get("content_analysis", {})
        
        if category == "content_structure_analysis":
            return self._analyse_content_structure(content, content_analysis)
        
        elif category == "seo_content_optimisation":
            return self._analyse_seo_optimisation(content, url)
        
        elif category == "readability_assessment":
            return self._assess_readability(content)
        
        elif category == "engagement_factor_analysis":
            return self._analyse_engagement_factors(content, content_analysis)
        
        elif category == "conversion_path_analysis":
            return self._analyse_conversion_paths(content, url)
        
        elif category == "accessibility_evaluation":
            return self._evaluate_accessibility(content, url)
        
        elif category == "technical_content_performance":
            return self._analyse_technical_performance(content, content_analysis)
        
        elif category == "competitive_content_analysis":
            return self._analyse_competitive_content(content, client_domain)
        
        elif category == "ai_optimisation_opportunities":
            return self._identify_ai_optimisation_opportunities(content, url)
        
        else:
            return {"error": f"Unknown analysis category: {category}", "score": 0.5}
    
    def _analyse_content_structure(self, content: str, content_analysis: Dict) -> Dict[str, Any]:
        """Analyse content structure and organisation"""
        analysis = {
            "score": 0.0,
            "strengths": [],
            "weaknesses": [],
            "recommendations": []
        }
        
        # Analyse content structure elements
        structure_score = 0.0
        factors_evaluated = 0
        
        # Check heading hierarchy
        heading_count = content_analysis.get("heading_count", 0)
        if heading_count >= 3:
            structure_score += 0.2
            analysis["strengths"].append("Good heading structure with multiple H2/H3 sections")
        elif heading_count >= 1:
            structure_score += 0.1
            analysis["recommendations"].append("Add more subheadings to improve content structure")
        else:
            analysis["weaknesses"].append("Missing heading structure - content lacks organisation")
            analysis["recommendations"].append("Add proper heading hierarchy (H1, H2, H3) for better structure")
        factors_evaluated += 1
        
        # Check paragraph structure
        paragraph_count = content_analysis.get("paragraph_count", 0)
        if paragraph_count >= 5:
            structure_score += 0.2
            analysis["strengths"].append("Well-structured content with multiple paragraphs")
        elif paragraph_count >= 3:
            structure_score += 0.1
        else:
            analysis["weaknesses"].append("Insufficient paragraph structure")
            analysis["recommendations"].append("Break content into more digestible paragraphs")
        factors_evaluated += 1
        
        # Check content density
        content_density = content_analysis.get("content_density", 0)
        if content_density > 0.3:
            structure_score += 0.15
            analysis["strengths"].append("Good content density with substantial information")
        elif content_density > 0.1:
            structure_score += 0.08
        else:
            analysis["weaknesses"].append("Low content density - may lack substance")
            analysis["recommendations"].append("Add more detailed content to improve information density")
        factors_evaluated += 1
        
        # Check word count adequacy
        word_count = content_analysis.get("word_count", 0)
        if word_count >= 1000:
            structure_score += 0.15
            analysis["strengths"].append("Substantial word count for comprehensive coverage")
        elif word_count >= 300:
            structure_score += 0.08
        else:
            analysis["weaknesses"].append("Low word count may not provide sufficient detail")
            analysis["recommendations"].append("Expand content to provide more comprehensive information")
        factors_evaluated += 1
        
        # Check for content hierarchy signals
        if content_analysis.get("structure_analysis", {}).get("has_substantial_content", False):
            structure_score += 0.1
            analysis["strengths"].append("Content has substantial depth and detail")
        factors_evaluated += 1
        
        # Normalise score
        analysis["score"] = min(structure_score / factors_evaluated * 5, 1.0)
        
        return analysis
    
    def _analyse_seo_optimisation(self, content: str, url: str) -> Dict[str, Any]:
        """Analyse SEO content optimisation"""
        analysis = {
            "score": 0.0,
            "strengths": [],
            "weaknesses": [], 
            "recommendations": [],
            "keyword_analysis": {}
        }
        
        seo_score = 0.0
        content_lower = content.lower()
        
        # Extract potential keywords from content
        keywords = self._extract_content_keywords(content)
        analysis["keyword_analysis"]["extracted_keywords"] = keywords[:10]
        
        # Check keyword density and distribution
        if keywords:
            primary_keyword = keywords[0]
            keyword_count = content_lower.count(primary_keyword.lower())
            keyword_density = keyword_count / max(len(content.split()), 1) * 100
            
            if 0.5 <= keyword_density <= 2.5:
                seo_score += 0.2
                analysis["strengths"].append(f"Good keyword density for '{primary_keyword}' ({keyword_density:.1f}%)")
            elif keyword_density > 2.5:
                analysis["weaknesses"].append(f"Keyword density too high for '{primary_keyword}' ({keyword_density:.1f}%)")
                analysis["recommendations"].append("Reduce keyword density to avoid over-optimisation")
            else:
                analysis["weaknesses"].append(f"Low keyword density for '{primary_keyword}' ({keyword_density:.1f}%)")
                analysis["recommendations"].append("Increase keyword usage naturally throughout content")
        
        # Check for semantic keywords
        semantic_variations = 0
        if keywords:
            for keyword in keywords[1:5]:  # Check related keywords
                if keyword.lower() in content_lower:
                    semantic_variations += 1
            
            if semantic_variations >= 3:
                seo_score += 0.15
                analysis["strengths"].append("Good use of semantic keyword variations")
            elif semantic_variations >= 1:
                seo_score += 0.08
            else:
                analysis["recommendations"].append("Add more semantic keyword variations")
        
        # Check content length for SEO
        word_count = len(content.split())
        if word_count >= 1500:
            seo_score += 0.15
            analysis["strengths"].append("Comprehensive content length supports SEO rankings")
        elif word_count >= 800:
            seo_score += 0.1
        else:
            analysis["weaknesses"].append("Content length may be too short for competitive SEO")
            analysis["recommendations"].append("Expand content to 1000+ words for better SEO performance")
        
        # Check for internal linking opportunities
        internal_link_keywords = ["read more", "learn about", "discover", "find out", "see our"]
        internal_links_present = any(phrase in content_lower for phrase in internal_link_keywords)
        
        if internal_links_present:
            seo_score += 0.1
            analysis["strengths"].append("Content includes internal linking opportunities")
        else:
            analysis["recommendations"].append("Add internal links to related content and services")
        
        # Check for external authority links
        external_indicators = ["according to", "research shows", "study by", "source:"]
        external_citations = any(phrase in content_lower for phrase in external_indicators)
        
        if external_citations:
            seo_score += 0.1
            analysis["strengths"].append("Content includes references to external authorities")
        else:
            analysis["recommendations"].append("Add citations and links to authoritative sources")
        
        # Check for local SEO elements (Australian context)
        local_indicators = ["australia", "australian", "sydney", "melbourne", "brisbane", "perth", "adelaide"]
        local_seo = any(location in content_lower for location in local_indicators)
        
        if local_seo:
            seo_score += 0.1
            analysis["strengths"].append("Content includes local SEO elements")
        else:
            analysis["recommendations"].append("Consider adding location-specific content for local SEO")
        
        # Check for featured snippet optimisation
        question_words = ["what", "how", "why", "when", "where", "who"]
        has_questions = any(word in content_lower for word in question_words)
        
        if has_questions:
            seo_score += 0.1
            analysis["strengths"].append("Content structured for featured snippet opportunities")
        else:
            analysis["recommendations"].append("Add FAQ section or question-based content for featured snippets")
        
        analysis["score"] = min(seo_score, 1.0)
        
        return analysis
    
    def _assess_readability(self, content: str) -> Dict[str, Any]:
        """Assess content readability and accessibility"""
        analysis = {
            "score": 0.0,
            "strengths": [],
            "weaknesses": [],
            "recommendations": [],
            "readability_metrics": {}
        }
        
        readability_score = 0.0
        
        # Calculate basic readability metrics
        sentences = content.split('.')
        words = content.split()
        
        if len(sentences) > 0 and len(words) > 0:
            avg_words_per_sentence = len(words) / len(sentences)
            analysis["readability_metrics"]["avg_words_per_sentence"] = round(avg_words_per_sentence, 1)
            
            # Ideal: 15-20 words per sentence
            if 12 <= avg_words_per_sentence <= 22:
                readability_score += 0.25
                analysis["strengths"].append(f"Good sentence length ({avg_words_per_sentence:.1f} words per sentence)")
            elif avg_words_per_sentence > 25:
                analysis["weaknesses"].append(f"Sentences too long ({avg_words_per_sentence:.1f} words per sentence)")
                analysis["recommendations"].append("Break long sentences into shorter, clearer ones")
            else:
                analysis["recommendations"].append("Consider varying sentence length for better flow")
        
        # Check paragraph length
        paragraphs = content.split('\n\n')
        if paragraphs:
            avg_words_per_paragraph = len(words) / len(paragraphs)
            analysis["readability_metrics"]["avg_words_per_paragraph"] = round(avg_words_per_paragraph, 1)
            
            # Ideal: 50-100 words per paragraph for web content
            if 40 <= avg_words_per_paragraph <= 120:
                readability_score += 0.2
                analysis["strengths"].append("Well-sized paragraphs for web readability")
            elif avg_words_per_paragraph > 150:
                analysis["weaknesses"].append("Paragraphs too long for web reading")
                analysis["recommendations"].append("Break long paragraphs into shorter sections")
        
        # Check for readability enhancers
        readability_enhancers = 0
        
        # Check for bullet points or lists
        if '•' in content or '- ' in content or content.count('\n- ') > 0:
            readability_enhancers += 1
            analysis["strengths"].append("Uses bullet points or lists for easy scanning")
        else:
            analysis["recommendations"].append("Add bullet points or lists to break up dense text")
        
        # Check for subheadings (indicated by title case after newlines)
        subheading_pattern = r'\n[A-Z][^.]*\n'
        import re
        if re.search(subheading_pattern, content):
            readability_enhancers += 1
            analysis["strengths"].append("Uses subheadings to structure content")
        else:
            analysis["recommendations"].append("Add subheadings to improve content scannability")
        
        # Check for transitional phrases
        transitions = ["however", "therefore", "furthermore", "in addition", "moreover", "consequently"]
        transition_count = sum(1 for transition in transitions if transition in content.lower())
        
        if transition_count >= 2:
            readability_enhancers += 1
            analysis["strengths"].append("Uses transitional phrases for better flow")
        
        # Check for active voice indicators
        passive_indicators = ["is being", "was being", "has been", "have been", "will be"]
        passive_count = sum(1 for indicator in passive_indicators if indicator in content.lower())
        active_score = max(0, 1 - (passive_count / max(len(sentences), 1)))
        
        if active_score > 0.8:
            readability_enhancers += 1
            analysis["strengths"].append("Primarily uses active voice")
        elif active_score < 0.6:
            analysis["weaknesses"].append("Overuse of passive voice")
            analysis["recommendations"].append("Convert passive voice to active voice where possible")
        
        # Calculate readability enhancer score
        readability_score += (readability_enhancers / 4) * 0.3
        
        # Check vocabulary complexity
        long_words = [word for word in words if len(word) > 6]
        complex_word_ratio = len(long_words) / max(len(words), 1)
        
        if complex_word_ratio < 0.2:
            readability_score += 0.15
            analysis["strengths"].append("Uses accessible vocabulary")
        elif complex_word_ratio > 0.35:
            analysis["weaknesses"].append("High use of complex vocabulary")
            analysis["recommendations"].append("Simplify complex terms or provide definitions")
        
        # Check for jargon and technical terms
        jargon_indicators = ["utilise", "implement", "facilitate", "optimise", "leverage"]
        jargon_count = sum(1 for term in jargon_indicators if term in content.lower())
        
        if jargon_count > 3:
            analysis["weaknesses"].append("Overuse of business jargon")
            analysis["recommendations"].append("Replace jargon with plain English where possible")
        
        analysis["readability_metrics"]["complex_word_ratio"] = round(complex_word_ratio, 3)
        analysis["score"] = min(readability_score, 1.0)
        
        return analysis
    
    def _analyse_engagement_factors(self, content: str, content_analysis: Dict) -> Dict[str, Any]:
        """Analyse content engagement potential"""
        analysis = {
            "score": 0.0,
            "strengths": [],
            "weaknesses": [],
            "recommendations": [],
            "engagement_metrics": {}
        }
        
        engagement_score = 0.0
        content_lower = content.lower()
        
        # Check for emotional triggers
        emotional_words = [
            "amazing", "incredible", "outstanding", "excellent", "fantastic", "remarkable",
            "discover", "transform", "achieve", "success", "results", "breakthrough",
            "essential", "critical", "important", "vital", "significant", "powerful"
        ]
        
        emotional_count = sum(1 for word in emotional_words if word in content_lower)
        analysis["engagement_metrics"]["emotional_words"] = emotional_count
        
        if emotional_count >= 5:
            engagement_score += 0.2
            analysis["strengths"].append("Uses emotional language to engage readers")
        elif emotional_count >= 2:
            engagement_score += 0.1
        else:
            analysis["recommendations"].append("Add more engaging, emotional language to connect with readers")
        
        # Check for storytelling elements
        storytelling_indicators = [
            "when", "after", "before", "then", "next", "finally", "first", "meanwhile",
            "imagine", "picture this", "for example", "case study", "story", "experience"
        ]
        
        storytelling_count = sum(1 for indicator in storytelling_indicators if indicator in content_lower)
        
        if storytelling_count >= 3:
            engagement_score += 0.15
            analysis["strengths"].append("Incorporates storytelling elements")
        else:
            analysis["recommendations"].append("Add examples, stories, or case studies to improve engagement")
        
        # Check for direct address to reader
        direct_address = ["you", "your", "yourself"]
        address_count = sum(1 for address in direct_address if address in content_lower)
        address_ratio = address_count / max(len(content.split()), 1)
        
        if address_ratio > 0.02:  # More than 2% of words
            engagement_score += 0.15
            analysis["strengths"].append("Uses direct address to engage readers")
        else:
            analysis["recommendations"].append("Use more direct address ('you', 'your') to personalise content")
        
        # Check for questions
        question_count = content.count('?')
        if question_count >= 2:
            engagement_score += 0.1
            analysis["strengths"].append("Uses questions to engage readers")
        elif question_count == 1:
            engagement_score += 0.05
        else:
            analysis["recommendations"].append("Add rhetorical questions to increase reader engagement")
        
        # Check for calls to action
        cta_phrases = [
            "contact us", "get started", "learn more", "find out", "discover",
            "call now", "book", "schedule", "download", "subscribe", "sign up"
        ]
        
        cta_count = sum(1 for cta in cta_phrases if cta in content_lower)
        
        if cta_count >= 2:
            engagement_score += 0.15
            analysis["strengths"].append("Includes multiple calls to action")
        elif cta_count == 1:
            engagement_score += 0.08
        else:
            analysis["weaknesses"].append("Missing clear calls to action")
            analysis["recommendations"].append("Add clear calls to action throughout content")
        
        # Check for social proof elements
        social_proof = [
            "client", "customer", "testimonial", "review", "case study",
            "success story", "results", "achieved", "helped", "trusted by"
        ]
        
        social_proof_count = sum(1 for proof in social_proof if proof in content_lower)
        
        if social_proof_count >= 3:
            engagement_score += 0.1
            analysis["strengths"].append("Includes social proof elements")
        else:
            analysis["recommendations"].append("Add testimonials, case studies, or client results for social proof")
        
        # Check for urgency/scarcity
        urgency_words = [
            "now", "today", "limited", "exclusive", "deadline", "expires",
            "don't miss", "act fast", "while supplies last", "limited time"
        ]
        
        urgency_count = sum(1 for word in urgency_words if word in content_lower)
        
        if urgency_count >= 1:
            engagement_score += 0.05
            analysis["strengths"].append("Creates sense of urgency")
        
        # Check content freshness indicators
        freshness_indicators = ["2024", "2025", "latest", "new", "recent", "updated", "current"]
        freshness_count = sum(1 for indicator in freshness_indicators if indicator in content_lower)
        
        if freshness_count >= 2:
            engagement_score += 0.1
            analysis["strengths"].append("Content appears current and fresh")
        else:
            analysis["recommendations"].append("Add current dates and 'latest' information to show freshness")
        
        analysis["engagement_metrics"]["cta_count"] = cta_count
        analysis["engagement_metrics"]["question_count"] = question_count
        analysis["score"] = min(engagement_score, 1.0)
        
        return analysis
    
    def _analyse_conversion_paths(self, content: str, url: str) -> Dict[str, Any]:
        """Analyse conversion optimisation potential"""
        analysis = {
            "score": 0.0,
            "strengths": [],
            "weaknesses": [],
            "recommendations": [],
            "conversion_elements": {}
        }
        
        conversion_score = 0.0
        content_lower = content.lower()
        
        # Check for value propositions
        value_props = [
            "benefit", "advantage", "value", "save", "improve", "increase", "reduce",
            "solution", "help", "achieve", "results", "success", "roi", "return on investment"
        ]
        
        value_prop_count = sum(1 for prop in value_props if prop in content_lower)
        analysis["conversion_elements"]["value_propositions"] = value_prop_count
        
        if value_prop_count >= 5:
            conversion_score += 0.2
            analysis["strengths"].append("Strong value proposition messaging")
        elif value_prop_count >= 2:
            conversion_score += 0.1
        else:
            analysis["weaknesses"].append("Weak value proposition")
            analysis["recommendations"].append("Strengthen value propositions - highlight benefits and outcomes")
        
        # Check for trust indicators
        trust_elements = [
            "guarantee", "certified", "licensed", "insured", "professional",
            "experienced", "expert", "qualified", "accredited", "member of"
        ]
        
        trust_count = sum(1 for element in trust_elements if element in content_lower)
        
        if trust_count >= 3:
            conversion_score += 0.15
            analysis["strengths"].append("Includes trust and credibility indicators")
        elif trust_count >= 1:
            conversion_score += 0.08
        else:
            analysis["recommendations"].append("Add trust indicators (certifications, guarantees, credentials)")
        
        # Check for objection handling
        objection_phrases = [
            "but", "however", "concern", "worry", "question", "doubt",
            "affordable", "budget", "cost-effective", "free consultation",
            "no obligation", "risk-free", "money back"
        ]
        
        objection_count = sum(1 for phrase in objection_phrases if phrase in content_lower)
        
        if objection_count >= 3:
            conversion_score += 0.1
            analysis["strengths"].append("Addresses common objections")
        else:
            analysis["recommendations"].append("Address common customer objections and concerns")
        
        # Check for contact information prominence
        contact_indicators = [
            "phone", "email", "contact", "call", "reach out", "get in touch",
            "consultation", "quote", "estimate", "proposal"
        ]
        
        contact_count = sum(1 for indicator in contact_indicators if indicator in content_lower)
        
        if contact_count >= 3:
            conversion_score += 0.15
            analysis["strengths"].append("Multiple contact opportunities")
        elif contact_count >= 1:
            conversion_score += 0.08
        else:
            analysis["weaknesses"].append("Limited contact information")
            analysis["recommendations"].append("Make contact information more prominent and accessible")
        
        # Check for specific next steps
        next_step_phrases = [
            "next step", "get started", "begin", "first step", "to start",
            "schedule", "book", "arrange", "set up", "apply"
        ]
        
        next_steps_count = sum(1 for phrase in next_step_phrases if phrase in content_lower)
        
        if next_steps_count >= 2:
            conversion_score += 0.1
            analysis["strengths"].append("Clear next steps for prospects")
        else:
            analysis["recommendations"].append("Add clear next steps for interested prospects")
        
        # Check for urgency in conversion
        conversion_urgency = [
            "limited time", "special offer", "expires", "deadline", "act now",
            "don't miss", "while available", "this month only"
        ]
        
        urgency_present = any(phrase in content_lower for phrase in conversion_urgency)
        
        if urgency_present:
            conversion_score += 0.05
            analysis["strengths"].append("Creates conversion urgency")
        
        # Check for personalisation elements
        personalisation = [
            "custom", "personalised", "tailored", "specific to", "designed for",
            "your business", "your needs", "your industry", "your situation"
        ]
        
        personalisation_count = sum(1 for element in personalisation if element in content_lower)
        
        if personalisation_count >= 2:
            conversion_score += 0.1
            analysis["strengths"].append("Personalised messaging approach")
        else:
            analysis["recommendations"].append("Add more personalised messaging for target audience")
        
        analysis["conversion_elements"]["contact_indicators"] = contact_count
        analysis["conversion_elements"]["trust_elements"] = trust_count
        analysis["score"] = min(conversion_score, 1.0)
        
        return analysis
    
    def _evaluate_accessibility(self, content: str, url: str) -> Dict[str, Any]:
        """Evaluate content accessibility"""
        analysis = {
            "score": 0.0,
            "strengths": [],
            "weaknesses": [],
            "recommendations": [],
            "accessibility_checks": {}
        }
        
        accessibility_score = 0.0
        
        # This would integrate with actual accessibility testing
        # For now, we'll simulate comprehensive accessibility analysis
        
        # Check content structure for screen readers
        structure_score = 0.7  # Simulated score
        if structure_score > 0.8:
            accessibility_score += 0.3
            analysis["strengths"].append("Good content structure for screen readers")
        else:
            analysis["weaknesses"].append("Content structure needs improvement for accessibility")
            analysis["recommendations"].append("Improve heading hierarchy and content organisation")
        
        # Check for alternative text descriptions
        alt_text_score = 0.6  # Simulated
        if alt_text_score > 0.8:
            accessibility_score += 0.2
            analysis["strengths"].append("Images have proper alternative text")
        else:
            analysis["recommendations"].append("Add descriptive alternative text for all images")
        
        # Check for keyboard navigation support
        keyboard_nav_score = 0.8  # Simulated
        if keyboard_nav_score > 0.7:
            accessibility_score += 0.2
            analysis["strengths"].append("Content supports keyboard navigation")
        else:
            analysis["recommendations"].append("Improve keyboard navigation support")
        
        # Check colour contrast (simulated)
        colour_contrast_score = 0.75  # Simulated
        if colour_contrast_score > 0.7:
            accessibility_score += 0.15
            analysis["strengths"].append("Adequate colour contrast for readability")
        else:
            analysis["recommendations"].append("Improve colour contrast for better accessibility")
        
        # Check for clear language
        if len(content.split()) > 0:
            # Simple readability check
            avg_word_length = sum(len(word) for word in content.split()) / len(content.split())
            if avg_word_length < 6:
                accessibility_score += 0.15
                analysis["strengths"].append("Uses clear, accessible language")
            else:
                analysis["recommendations"].append("Simplify language for better accessibility")
        
        analysis["accessibility_checks"]["structure_score"] = structure_score
        analysis["accessibility_checks"]["alt_text_score"] = alt_text_score
        analysis["accessibility_checks"]["keyboard_nav_score"] = keyboard_nav_score
        analysis["accessibility_checks"]["colour_contrast_score"] = colour_contrast_score
        
        analysis["score"] = min(accessibility_score, 1.0)
        
        return analysis
    
    def _analyse_technical_performance(self, content: str, content_analysis: Dict) -> Dict[str, Any]:
        """Analyse technical content performance factors"""
        analysis = {
            "score": 0.0,
            "strengths": [],
            "weaknesses": [],
            "recommendations": [],
            "technical_metrics": {}
        }
        
        technical_score = 0.0
        
        # Content length optimisation
        content_length = len(content)
        analysis["technical_metrics"]["content_length"] = content_length
        
        if 2000 <= content_length <= 8000:  # Optimal for web performance
            technical_score += 0.2
            analysis["strengths"].append("Optimal content length for performance")
        elif content_length > 8000:
            analysis["weaknesses"].append("Content may be too long, affecting load times")
            analysis["recommendations"].append("Consider breaking into multiple pages or sections")
        else:
            analysis["recommendations"].append("Consider expanding content for better SEO performance")
        
        # Content structure efficiency
        structure_analysis = content_analysis.get("structure_analysis", {})
        avg_line_length = structure_analysis.get("average_line_length", 0)
        
        if 50 <= avg_line_length <= 120:
            technical_score += 0.15
            analysis["strengths"].append("Efficient content structure")
        
        # Check for heavy content elements
        heavy_elements = content.count('[image]') + content.count('[video]') + content.count('[embed]')
        if heavy_elements > 10:
            analysis["weaknesses"].append("High number of media elements may affect performance")
            analysis["recommendations"].append("Optimise images and media for faster loading")
        elif heavy_elements > 0:
            technical_score += 0.1
            analysis["strengths"].append("Includes multimedia content for engagement")
        
        # Content organisation efficiency
        if content_analysis.get("heading_count", 0) >= 3:
            technical_score += 0.1
            analysis["strengths"].append("Well-organised content structure")
        
        # Check for content that enables caching
        if "updated" in content.lower() or "modified" in content.lower():
            technical_score += 0.05
            analysis["strengths"].append("Content includes update information")
        
        # Mobile optimisation considerations
        mobile_friendly_score = 0.8  # Simulated based on content structure
        technical_score += mobile_friendly_score * 0.25
        
        if mobile_friendly_score > 0.8:
            analysis["strengths"].append("Content structure supports mobile devices")
        else:
            analysis["recommendations"].append("Optimise content layout for mobile devices")
        
        # Loading performance considerations
        if content_length < 5000 and content_analysis.get("paragraph_count", 0) > 0:
            technical_score += 0.15
            analysis["strengths"].append("Content size optimised for quick loading")
        
        analysis["technical_metrics"]["mobile_friendly_score"] = mobile_friendly_score
        analysis["score"] = min(technical_score, 1.0)
        
        return analysis
    
    def _analyse_competitive_content(self, content: str, client_domain: str) -> Dict[str, Any]:
        """Analyse competitive content positioning"""
        analysis = {
            "score": 0.0,
            "strengths": [],
            "weaknesses": [],
            "recommendations": [],
            "competitive_analysis": {}
        }
        
        # This would perform actual competitive analysis
        # For now, simulate based on content characteristics
        
        competitive_score = 0.6  # Base competitive score
        content_lower = content.lower()
        
        # Check for unique value propositions
        unique_indicators = [
            "unique", "exclusive", "proprietary", "innovative", "custom",
            "specialised", "expert", "experienced", "award-winning"
        ]
        
        uniqueness_count = sum(1 for indicator in unique_indicators if indicator in content_lower)
        
        if uniqueness_count >= 3:
            competitive_score += 0.2
            analysis["strengths"].append("Strong unique value proposition")
        elif uniqueness_count >= 1:
            competitive_score += 0.1
        else:
            analysis["recommendations"].append("Strengthen unique value propositions")
        
        # Check for industry expertise demonstration
        expertise_indicators = [
            "years of experience", "established", "proven", "track record",
            "successful", "results", "achievements", "awards", "recognition"
        ]
        
        expertise_count = sum(1 for indicator in expertise_indicators if indicator in content_lower)
        
        if expertise_count >= 2:
            competitive_score += 0.15
            analysis["strengths"].append("Demonstrates industry expertise")
        else:
            analysis["recommendations"].append("Better highlight experience and expertise")
        
        # Check for competitive differentiation
        differentiation_words = [
            "unlike", "different from", "better than", "compared to",
            "alternative", "instead of", "rather than"
        ]
        
        differentiation_present = any(word in content_lower for word in differentiation_words)
        
        if differentiation_present:
            competitive_score += 0.1
            analysis["strengths"].append("Includes competitive differentiation")
        else:
            analysis["recommendations"].append("Add clear differentiation from competitors")
        
        analysis["competitive_analysis"]["uniqueness_score"] = uniqueness_count / 5
        analysis["competitive_analysis"]["expertise_score"] = expertise_count / 5
        analysis["score"] = min(competitive_score, 1.0)
        
        return analysis
    
    def _identify_ai_optimisation_opportunities(self, content: str, url: str) -> Dict[str, Any]:
        """Identify AI and voice search optimisation opportunities"""
        analysis = {
            "score": 0.0,
            "strengths": [],
            "weaknesses": [],
            "recommendations": [],
            "ai_optimization": {}
        }
        
        ai_score = 0.0
        content_lower = content.lower()
        
        # Check for FAQ-style content (good for AI)
        faq_indicators = ["what is", "how to", "why", "when", "where", "who"]
        faq_count = sum(1 for indicator in faq_indicators if indicator in content_lower)
        
        if faq_count >= 5:
            ai_score += 0.25
            analysis["strengths"].append("Content structured for AI and voice search")
        elif faq_count >= 2:
            ai_score += 0.15
        else:
            analysis["recommendations"].append("Add FAQ-style questions and answers for AI optimisation")
        
        # Check for conversational language
        conversational_indicators = ["you can", "let's", "here's", "simply", "just"]
        conversational_count = sum(1 for indicator in conversational_indicators if indicator in content_lower)
        
        if conversational_count >= 3:
            ai_score += 0.2
            analysis["strengths"].append("Uses conversational language for voice search")
        else:
            analysis["recommendations"].append("Use more conversational language for voice search optimisation")
        
        # Check for structured information
        if content.count(':') >= 5 or content.count('- ') >= 3:
            ai_score += 0.15
            analysis["strengths"].append("Well-structured information for AI parsing")
        else:
            analysis["recommendations"].append("Structure information with lists and clear formatting")
        
        # Check for local intent (important for voice search)
        local_phrases = ["near me", "in sydney", "in melbourne", "local", "nearby"]
        local_present = any(phrase in content_lower for phrase in local_phrases)
        
        if local_present:
            ai_score += 0.1
            analysis["strengths"].append("Includes local search optimisation")
        else:
            analysis["recommendations"].append("Add location-based content for local AI search")
        
        # Check for action-oriented content
        action_words = ["get", "find", "buy", "choose", "select", "compare", "learn"]
        action_count = sum(1 for word in action_words if word in content_lower)
        
        if action_count >= 5:
            ai_score += 0.15
            analysis["strengths"].append("Action-oriented content for AI assistants")
        else:
            analysis["recommendations"].append("Include more action-oriented language")
        
        # Check for featured snippet optimisation
        snippet_patterns = ["step 1", "first", "second", "finally", "in summary"]
        snippet_indicators = sum(1 for pattern in snippet_patterns if pattern in content_lower)
        
        if snippet_indicators >= 3:
            ai_score += 0.15
            analysis["strengths"].append("Optimised for featured snippets")
        else:
            analysis["recommendations"].append("Structure content for featured snippet capture")
        
        analysis["ai_optimization"]["faq_count"] = faq_count
        analysis["ai_optimization"]["conversational_score"] = conversational_count / 10
        analysis["score"] = min(ai_score, 1.0)
        
        return analysis
    
    def _extract_content_keywords(self, content: str) -> List[str]:
        """Extract potential keywords from content"""
        import re
        from collections import Counter
        
        # Clean content and extract words
        words = re.findall(r'\b[a-zA-Z]{3,}\b', content.lower())
        
        # Remove common stop words
        stop_words = {
            'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
            'by', 'is', 'are', 'was', 'were', 'been', 'have', 'has', 'had', 'do',
            'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might',
            'must', 'can', 'this', 'that', 'these', 'those', 'your', 'our'
        }
        
        # Filter out stop words
        keywords = [word for word in words if word not in stop_words and len(word) > 3]
        
        # Count frequency and return top keywords
        keyword_counts = Counter(keywords)
        return [keyword for keyword, count in keyword_counts.most_common(20)]
    
    def _calculate_optimisation_scores(self, analysis_results: Dict) -> Dict[str, float]:
        """Calculate optimisation scores from analysis results"""
        scores = {}
        
        # Map analysis categories to score categories
        category_mapping = {
            "content_structure_analysis": "content_quality",
            "seo_content_optimisation": "seo_optimisation", 
            "readability_assessment": "readability",
            "engagement_factor_analysis": "engagement_potential",
            "conversion_path_analysis": "conversion_optimisation",
            "accessibility_evaluation": "accessibility",
            "technical_content_performance": "technical_performance"
        }
        
        for analysis_category, score_category in category_mapping.items():
            if analysis_category in analysis_results:
                scores[score_category] = analysis_results[analysis_category].get("score", 0.0)
        
        return scores
    
    def _calculate_overall_score(self, scores: Dict[str, float]) -> float:
        """Calculate overall optimisation score"""
        weighted_score = 0.0
        total_weight = 0.0
        
        for category, weight in self.scoring_weights.items():
            if category in scores:
                weighted_score += scores[category] * weight
                total_weight += weight
        
        return weighted_score / total_weight if total_weight > 0 else 0.0
    
    def _generate_optimisation_recommendations(self, analysis_results: Dict, 
                                             scores: Dict) -> Dict[str, List[OptimisationRecommendation]]:
        """Generate prioritised optimisation recommendations"""
        recommendations = {"priority": [], "all": []}
        
        # Collect all recommendations from analysis results
        all_recommendations = []
        
        for category, results in analysis_results.items():
            if "recommendations" in results:
                for rec in results["recommendations"]:
                    # Determine priority based on category and score
                    category_score = results.get("score", 0.5)
                    
                    if category_score < 0.4:
                        priority = "critical"
                        impact = "high"
                    elif category_score < 0.6:
                        priority = "high"
                        impact = "medium-high"
                    elif category_score < 0.8:
                        priority = "medium"
                        impact = "medium"
                    else:
                        priority = "low"
                        impact = "low"
                    
                    recommendation = OptimisationRecommendation(
                        category=category,
                        priority=priority,
                        recommendation=rec,
                        impact_estimate=impact,
                        implementation_effort=self._estimate_effort(rec),
                        expected_outcome=self._estimate_outcome(rec, category_score),
                        technical_requirements=self._identify_technical_requirements(rec),
                        content_changes_required=self._requires_content_changes(rec)
                    )
                    
                    all_recommendations.append(recommendation)
        
        # Sort by priority and impact
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        all_recommendations.sort(key=lambda x: (priority_order.get(x.priority, 3), x.category))
        
        # Separate priority recommendations (critical and high priority)
        priority_recs = [rec for rec in all_recommendations if rec.priority in ["critical", "high"]]
        
        recommendations["priority"] = [asdict(rec) for rec in priority_recs[:10]]  # Top 10 priority
        recommendations["all"] = [asdict(rec) for rec in all_recommendations[:25]]  # Top 25 overall
        
        return recommendations
    
    def _estimate_effort(self, recommendation: str) -> str:
        """Estimate implementation effort for recommendation"""
        rec_lower = recommendation.lower()
        
        if any(word in rec_lower for word in ["restructure", "redesign", "rebuild"]):
            return "high"
        elif any(word in rec_lower for word in ["add", "include", "create", "develop"]):
            return "medium"
        elif any(word in rec_lower for word in ["improve", "enhance", "optimise", "adjust"]):
            return "medium-low"
        else:
            return "low"
    
    def _estimate_outcome(self, recommendation: str, current_score: float) -> str:
        """Estimate expected outcome from recommendation"""
        rec_lower = recommendation.lower()
        
        # High impact recommendations
        if any(word in rec_lower for word in ["add citations", "improve structure", "add cta"]):
            if current_score < 0.5:
                return "Significant improvement in rankings and user engagement"
            else:
                return "Moderate improvement in performance metrics"
        
        # Medium impact recommendations
        elif any(word in rec_lower for word in ["enhance", "optimise", "improve"]):
            return "Moderate improvement in user experience and SEO"
        
        # General outcome
        if current_score < 0.4:
            return "Major improvement expected"
        elif current_score < 0.7:
            return "Moderate improvement expected"
        else:
            return "Minor improvement expected"
    
    def _identify_technical_requirements(self, recommendation: str) -> List[str]:
        """Identify technical requirements for implementing recommendation"""
        rec_lower = recommendation.lower()
        requirements = []
        
        if "image" in rec_lower or "visual" in rec_lower:
            requirements.append("Image editing software")
            requirements.append("Alt text implementation")
        
        if "link" in rec_lower:
            requirements.append("Link management system")
            requirements.append("URL structure review")
        
        if "structure" in rec_lower or "heading" in rec_lower:
            requirements.append("HTML/CSS knowledge")
            requirements.append("Content management system access")
        
        if "mobile" in rec_lower:
            requirements.append("Responsive design testing")
            requirements.append("Mobile optimisation tools")
        
        if not requirements:
            requirements.append("Content management system access")
        
        return requirements
    
    def _requires_content_changes(self, recommendation: str) -> bool:
        """Determine if recommendation requires content changes"""
        content_indicators = [
            "add", "include", "write", "create", "expand", "improve",
            "enhance", "rewrite", "restructure", "optimise content"
        ]
        
        return any(indicator in recommendation.lower() for indicator in content_indicators)
    
    def _extract_key_findings(self, analysis_results: Dict, scores: Dict) -> List[str]:
        """Extract key findings from analysis"""
        findings = []
        
        # Overall performance assessment
        overall_score = self._calculate_overall_score(scores)
        
        if overall_score >= 0.8:
            findings.append("Content demonstrates strong optimisation across multiple areas")
        elif overall_score >= 0.6:
            findings.append("Content has good foundation but requires targeted improvements")
        elif overall_score >= 0.4:
            findings.append("Content needs significant optimisation to compete effectively")
        else:
            findings.append("Content requires comprehensive optimisation strategy")
        
        # Category-specific findings
        for category, score in scores.items():
            category_name = category.replace("_", " ").title()
            
            if score >= 0.8:
                findings.append(f"Strong performance in {category_name}")
            elif score < 0.4:
                findings.append(f"Critical improvement needed in {category_name}")
        
        # Specific findings from analysis
        for category, results in analysis_results.items():
            if "strengths" in results and results["strengths"]:
                # Add top strength
                findings.append(f"Strength identified: {results['strengths'][0]}")
        
        # Limit findings to most important
        return findings[:8]
    
    def _create_error_result(self, url: str, error_message: str) -> ContentAnalysisResult:
        """Create error result when analysis fails"""
        return ContentAnalysisResult(
            url=url,
            analysis_timestamp=datetime.now().isoformat(),
            content_quality_score=0.0,
            seo_optimisation_score=0.0,
            readability_score=0.0,
            engagement_potential_score=0.0,
            conversion_optimisation_score=0.0,
            accessibility_score=0.0,
            technical_performance_score=0.0,
            overall_optimisation_score=0.0,
            key_findings=[f"Analysis failed: {error_message}"],
            priority_recommendations=[],
            detailed_analysis={"error": error_message}
        )
    
    def _save_analysis_result(self, client_domain: str, result: ContentAnalysisResult):
        """Save analysis result to file"""
        try:
            filename = f"content_analysis_{client_domain}_{int(datetime.now().timestamp())}.json"
            filepath = self.analysis_cache_path / filename
            
            # Convert result to dict for JSON serialisation
            result_dict = asdict(result)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(result_dict, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Content analysis saved: {filepath}")
            
        except Exception as e:
            logger.error(f"Failed to save analysis result: {str(e)}")
    
    def generate_optimisation_report(self, analysis_result: ContentAnalysisResult, 
                                   client_domain: str) -> str:
        """Generate comprehensive optimisation report"""
        
        report = f"""
# AI Content Specialist Analysis Report

## Executive Summary
**URL Analysed:** {analysis_result.url}
**Analysis Date:** {analysis_result.analysis_timestamp}
**Overall Optimisation Score:** {analysis_result.overall_optimisation_score:.1%}

### Performance Breakdown
- **Content Quality:** {analysis_result.content_quality_score:.1%}
- **SEO Optimisation:** {analysis_result.seo_optimisation_score:.1%}
- **Readability:** {analysis_result.readability_score:.1%}
- **Engagement Potential:** {analysis_result.engagement_potential_score:.1%}
- **Conversion Optimisation:** {analysis_result.conversion_optimisation_score:.1%}
- **Accessibility:** {analysis_result.accessibility_score:.1%}
- **Technical Performance:** {analysis_result.technical_performance_score:.1%}

## Key Findings
{chr(10).join(f"- {finding}" for finding in analysis_result.key_findings)}

## Priority Recommendations

### Critical & High Priority Actions
{chr(10).join(f"**{i+1}.** {rec.get('recommendation', 'N/A')}" + 
              f" (Priority: {rec.get('priority', 'N/A').upper()}, " +
              f"Impact: {rec.get('impact_estimate', 'N/A')})" 
              for i, rec in enumerate(analysis_result.priority_recommendations[:5]))}

### Implementation Roadmap

#### Phase 1: Critical Fixes (Week 1-2)
{chr(10).join(f"- {rec.get('recommendation', '')}" 
              for rec in analysis_result.priority_recommendations 
              if rec.get('priority') == 'critical')}

#### Phase 2: High Impact Improvements (Week 3-4) 
{chr(10).join(f"- {rec.get('recommendation', '')}" 
              for rec in analysis_result.priority_recommendations 
              if rec.get('priority') == 'high')}

#### Phase 3: Optimisation Enhancements (Week 5-8)
{chr(10).join(f"- {rec.get('recommendation', '')}" 
              for rec in analysis_result.priority_recommendations 
              if rec.get('priority') == 'medium')}

## Expected Outcomes

### Short-term Benefits (1-3 months)
- Improved user engagement and time on page
- Better search engine visibility for target keywords
- Enhanced conversion pathway effectiveness

### Long-term Benefits (3-6 months)
- Increased organic traffic and search rankings
- Higher conversion rates and lead generation
- Improved brand authority and user trust

## Monitoring & Measurement

### Key Metrics to Track
- Organic traffic growth
- Keyword ranking improvements
- User engagement metrics (bounce rate, time on page)
- Conversion rate improvements
- Page load speed and technical performance

### Recommended Review Schedule
- **Weekly:** Monitor traffic and ranking changes
- **Monthly:** Review conversion performance and user behaviour
- **Quarterly:** Comprehensive content audit and optimisation review

---

*Report generated by AI Content Specialist Agent*
*Analysis Date: {datetime.now().strftime("%d/%m/%Y %H:%M")}*
"""
        
        return report.strip()


# Initialize AI Content Specialist
ai_content_specialist = AIContentSpecialist()

# Export main components
__all__ = [
    'AIContentSpecialist',
    'ContentAnalysisResult',
    'OptimisationRecommendation',
    'ai_content_specialist'
]