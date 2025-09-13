"""
Fact Verification Protocols for Bigger Boss Agent System
Prevents unsupported business claims and ensures content accuracy.
"""

import os
import json
import re
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
from urllib.parse import urlparse

from .enhanced_api_integrations import serpapi

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class FactClaim:
    """Structure for individual fact claims"""
    id: str
    claim_text: str
    claim_type: str  # statistic, assertion, quote, data_point
    source_required: bool
    verification_status: str  # verified, unverified, disputed, pending
    confidence_score: float
    supporting_evidence: List[Dict[str, Any]]
    verification_sources: List[str]
    last_verified: str
    risk_level: str  # low, medium, high, critical


@dataclass
class VerificationResult:
    """Result of fact verification process"""
    claim_id: str
    original_claim: str
    verification_status: str
    confidence_score: float
    evidence_quality: str
    sources_found: int
    credible_sources: int
    verification_notes: List[str]
    recommended_action: str
    alternative_phrasing: Optional[str]


class FactVerificationProtocols:
    """Comprehensive fact verification and claim validation system"""
    
    def __init__(self):
        self.verification_cache_path = Path("C:/Apps/Agents/Bigger Boss/bigger-boss/system/fact_verification")
        self.verification_cache_path.mkdir(exist_ok=True)
        
        # Credible source domains for Australian context
        self.credible_domains = {
            "government": [
                "gov.au", "abs.gov.au", "austrade.gov.au", "acma.gov.au",
                "treasury.gov.au", "dfat.gov.au", "industry.gov.au"
            ],
            "education": [
                ".edu.au", ".edu", "university.", "research.", "institute."
            ],
            "industry_bodies": [
                "ama.com.au", "aicd.com.au", "cpa.org.au", "charteredaccountants.com.au",
                "lawcouncil.asn.au", "engineers.org.au"
            ],
            "reputable_media": [
                "abc.net.au", "smh.com.au", "theage.com.au", "afr.com",
                "reuters.com", "bloomberg.com", "economist.com"
            ],
            "research_orgs": [
                "csiro.au", "grattan.edu.au", "pc.gov.au", "rba.gov.au"
            ]
        }
        
        # Claim patterns that require verification
        self.high_risk_patterns = [
            r'\d+%\s+(?:of|increase|decrease|growth|decline)',  # Percentages
            r'\$\d+(?:,\d{3})*(?:\.\d{2})?\s+(?:million|billion|thousand)',  # Money amounts
            r'(?:studies|research|survey)\s+(?:shows?|indicates?|finds?)',  # Research claims
            r'(?:leading|#1|top|best|most|fastest|largest)',  # Superlative claims
            r'(?:proven|guaranteed|always|never|all|every)',  # Absolute claims
            r'\d+(?:x|times)\s+(?:more|less|better|faster)',  # Comparison claims
        ]
        
        # Warning phrases for unsupported claims
        self.warning_phrases = [
            "industry-leading", "market-leading", "award-winning", "proven results",
            "guaranteed success", "100% effective", "never fails", "always works",
            "best in class", "world-class", "cutting-edge", "revolutionary"
        ]
    
    def verify_content_claims(self, content: str, client_domain: str) -> Tuple[List[FactClaim], List[VerificationResult]]:
        """Verify all factual claims in content"""
        logger.info(f"Verifying factual claims for {client_domain}")
        
        # Extract claims from content
        claims = self._extract_claims(content)
        
        # Verify each claim
        verification_results = []
        
        for claim in claims:
            result = self._verify_individual_claim(claim)
            verification_results.append(result)
        
        # Save verification report
        self._save_verification_report(client_domain, claims, verification_results)
        
        return claims, verification_results
    
    def _extract_claims(self, content: str) -> List[FactClaim]:
        """Extract factual claims from content that require verification"""
        claims = []
        sentences = self._split_into_sentences(content)
        
        for i, sentence in enumerate(sentences):
            claim_types = self._identify_claim_types(sentence)
            
            if claim_types:
                for claim_type in claim_types:
                    claim_id = f"claim_{i}_{claim_type}"
                    
                    claim = FactClaim(
                        id=claim_id,
                        claim_text=sentence.strip(),
                        claim_type=claim_type,
                        source_required=self._requires_source(sentence, claim_type),
                        verification_status="pending",
                        confidence_score=0.0,
                        supporting_evidence=[],
                        verification_sources=[],
                        last_verified="",
                        risk_level=self._assess_risk_level(sentence, claim_type)
                    )
                    
                    claims.append(claim)
        
        return claims
    
    def _split_into_sentences(self, content: str) -> List[str]:
        """Split content into sentences for analysis"""
        # Basic sentence splitting with common abbreviations handling
        sentence_endings = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s'
        sentences = re.split(sentence_endings, content)
        
        # Clean and filter sentences
        cleaned_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 10 and not sentence.startswith('#'):  # Skip headings and very short text
                cleaned_sentences.append(sentence)
        
        return cleaned_sentences
    
    def _identify_claim_types(self, sentence: str) -> List[str]:
        """Identify types of claims in a sentence"""
        claim_types = []
        sentence_lower = sentence.lower()
        
        # Statistical claims
        if any(re.search(pattern, sentence) for pattern in self.high_risk_patterns):
            claim_types.append("statistic")
        
        # Percentage claims
        if re.search(r'\d+%', sentence):
            claim_types.append("percentage")
        
        # Research claims
        research_keywords = ["study", "research", "survey", "report", "analysis"]
        if any(keyword in sentence_lower for keyword in research_keywords):
            claim_types.append("research_claim")
        
        # Superlative claims
        superlative_keywords = ["best", "leading", "top", "most", "largest", "fastest", "#1"]
        if any(keyword in sentence_lower for keyword in superlative_keywords):
            claim_types.append("superlative")
        
        # Financial claims
        if re.search(r'\$\d+', sentence) or any(word in sentence_lower for word in ["revenue", "profit", "cost", "price"]):
            claim_types.append("financial")
        
        # Temporal claims
        temporal_keywords = ["since", "in 2024", "last year", "recently", "latest"]
        if any(keyword in sentence_lower for keyword in temporal_keywords):
            claim_types.append("temporal")
        
        # Industry claims
        industry_keywords = ["industry", "market", "sector", "field"]
        if any(keyword in sentence_lower for keyword in industry_keywords):
            claim_types.append("industry_assertion")
        
        return claim_types
    
    def _requires_source(self, sentence: str, claim_type: str) -> bool:
        """Determine if claim requires source citation"""
        high_source_requirement = ["statistic", "research_claim", "financial", "percentage"]
        medium_source_requirement = ["superlative", "industry_assertion"]
        
        if claim_type in high_source_requirement:
            return True
        elif claim_type in medium_source_requirement:
            # Check if it's a strong claim
            strong_indicators = ["proven", "guaranteed", "always", "never", "all", "every"]
            return any(indicator in sentence.lower() for indicator in strong_indicators)
        
        return False
    
    def _assess_risk_level(self, sentence: str, claim_type: str) -> str:
        """Assess risk level of making unsupported claim"""
        sentence_lower = sentence.lower()
        
        # Critical risk indicators
        critical_indicators = [
            "100%", "always", "never", "guaranteed", "proven", "all", "every",
            "best in the world", "industry leader", "#1", "market leader"
        ]
        
        if any(indicator in sentence_lower for indicator in critical_indicators):
            return "critical"
        
        # High risk indicators
        high_risk_indicators = [
            "leading", "top", "most", "fastest", "largest", "award-winning",
            "cutting-edge", "revolutionary", "breakthrough"
        ]
        
        if claim_type in ["statistic", "percentage", "financial"] or \
           any(indicator in sentence_lower for indicator in high_risk_indicators):
            return "high"
        
        # Medium risk indicators
        if claim_type in ["research_claim", "superlative", "industry_assertion"]:
            return "medium"
        
        return "low"
    
    def _verify_individual_claim(self, claim: FactClaim) -> VerificationResult:
        """Verify an individual factual claim"""
        logger.info(f"Verifying claim: {claim.claim_text[:100]}...")
        
        verification_notes = []
        evidence_quality = "poor"
        sources_found = 0
        credible_sources = 0
        confidence_score = 0.0
        verification_status = "unverified"
        recommended_action = "require_source"
        alternative_phrasing = None
        
        try:
            # Search for supporting evidence
            search_query = self._create_verification_query(claim)
            
            search_result = serpapi.search_google(
                query=search_query,
                location="Australia",
                num_results=15,
                date_restrict="past_year"
            )
            
            if search_result.success:
                search_results = search_result.data.get("search_results", [])
                sources_found = len(search_results)
                
                # Analyse search results for credibility
                credible_results = self._filter_credible_sources(search_results)
                credible_sources = len(credible_results)
                
                # Look for direct evidence of the claim
                evidence_analysis = self._analyse_evidence_in_results(claim, credible_results)
                
                if evidence_analysis["direct_evidence"]:
                    verification_status = "verified"
                    confidence_score = min(0.9, 0.6 + (credible_sources * 0.1))
                    evidence_quality = "strong" if credible_sources >= 3 else "moderate"
                    recommended_action = "approved_with_citation"
                    verification_notes.append(f"Found direct evidence in {credible_sources} credible sources")
                    
                elif evidence_analysis["partial_evidence"]:
                    verification_status = "partially_verified"
                    confidence_score = min(0.7, 0.4 + (credible_sources * 0.1))
                    evidence_quality = "moderate" if credible_sources >= 2 else "weak"
                    recommended_action = "revise_and_cite"
                    alternative_phrasing = self._suggest_alternative_phrasing(claim, evidence_analysis)
                    verification_notes.append(f"Found partial evidence requiring claim modification")
                    
                else:
                    verification_status = "disputed" if sources_found > 5 else "unverified"
                    confidence_score = 0.1
                    evidence_quality = "poor"
                    recommended_action = "remove_or_replace"
                    alternative_phrasing = self._suggest_conservative_phrasing(claim)
                    verification_notes.append("No supporting evidence found in credible sources")
                
                # Additional verification for high-risk claims
                if claim.risk_level in ["high", "critical"]:
                    additional_verification = self._additional_high_risk_verification(claim)
                    verification_notes.extend(additional_verification["notes"])
                    if additional_verification["downgrade_confidence"]:
                        confidence_score *= 0.8
                        if recommended_action == "approved_with_citation":
                            recommended_action = "revise_and_cite"
            
            else:
                verification_notes.append("Search verification failed - manual verification required")
                recommended_action = "manual_verification_required"
        
        except Exception as e:
            logger.error(f"Claim verification error: {str(e)}")
            verification_notes.append(f"Verification error: {str(e)}")
            recommended_action = "manual_verification_required"
        
        return VerificationResult(
            claim_id=claim.id,
            original_claim=claim.claim_text,
            verification_status=verification_status,
            confidence_score=confidence_score,
            evidence_quality=evidence_quality,
            sources_found=sources_found,
            credible_sources=credible_sources,
            verification_notes=verification_notes,
            recommended_action=recommended_action,
            alternative_phrasing=alternative_phrasing
        )
    
    def _create_verification_query(self, claim: FactClaim) -> str:
        """Create search query to verify claim"""
        claim_text = claim.claim_text.lower()
        
        # Extract key elements from claim
        numbers = re.findall(r'\d+(?:\.\d+)?%?', claim_text)
        key_terms = self._extract_key_terms(claim_text)
        
        # Build verification query
        if claim.claim_type == "statistic" and numbers:
            query = f'"{numbers[0]}" {" ".join(key_terms[:3])} statistics data study'
        elif claim.claim_type == "research_claim":
            query = f'{" ".join(key_terms[:4])} research study report findings'
        elif claim.claim_type == "financial":
            query = f'{" ".join(key_terms[:3])} financial data revenue cost analysis'
        else:
            query = f'"{" ".join(key_terms[:5])}" verification evidence'
        
        # Add Australian context if relevant
        if any(term in claim_text for term in ["australia", "australian", "sydney", "melbourne"]):
            query += " Australia"
        
        return query
    
    def _extract_key_terms(self, text: str) -> List[str]:
        """Extract key terms from claim text"""
        # Remove common stop words and extract meaningful terms
        stop_words = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
            "of", "with", "by", "is", "are", "was", "were", "been", "have", "has",
            "had", "do", "does", "did", "will", "would", "could", "should", "may",
            "might", "must", "can", "this", "that", "these", "those"
        }
        
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        key_terms = [word for word in words if word not in stop_words]
        
        return key_terms[:10]  # Return up to 10 key terms
    
    def _filter_credible_sources(self, search_results: List[Dict]) -> List[Dict]:
        """Filter search results to include only credible sources"""
        credible_results = []
        
        for result in search_results:
            domain = result.get("domain", "").lower()
            
            # Check against credible domain lists
            is_credible = False
            for category, domains in self.credible_domains.items():
                if any(credible_domain in domain for credible_domain in domains):
                    result["credibility_category"] = category
                    is_credible = True
                    break
            
            if is_credible:
                credible_results.append(result)
        
        return credible_results
    
    def _analyse_evidence_in_results(self, claim: FactClaim, credible_results: List[Dict]) -> Dict[str, Any]:
        """Analyse search results for evidence supporting the claim"""
        analysis = {
            "direct_evidence": False,
            "partial_evidence": False,
            "contradictory_evidence": False,
            "evidence_details": []
        }
        
        claim_lower = claim.claim_text.lower()
        
        # Extract key elements to look for
        numbers = re.findall(r'\d+(?:\.\d+)?%?', claim.claim_text)
        key_terms = self._extract_key_terms(claim_lower)
        
        direct_evidence_count = 0
        partial_evidence_count = 0
        
        for result in credible_results:
            title = result.get("title", "").lower()
            snippet = result.get("snippet", "").lower()
            combined_text = f"{title} {snippet}"
            
            # Check for direct number matches
            if numbers:
                for number in numbers:
                    if number in combined_text:
                        direct_evidence_count += 1
                        analysis["evidence_details"].append({
                            "type": "direct_number_match",
                            "source": result.get("domain", ""),
                            "evidence": f"Found '{number}' in {result.get('title', '')}"
                        })
            
            # Check for key term matches
            term_matches = sum(1 for term in key_terms[:5] if term in combined_text)
            if term_matches >= 3:
                partial_evidence_count += 1
                analysis["evidence_details"].append({
                    "type": "contextual_match",
                    "source": result.get("domain", ""),
                    "evidence": f"Found {term_matches}/{len(key_terms[:5])} key terms"
                })
        
        # Determine evidence levels
        if direct_evidence_count >= 2:
            analysis["direct_evidence"] = True
        elif direct_evidence_count >= 1 or partial_evidence_count >= 3:
            analysis["partial_evidence"] = True
        
        return analysis
    
    def _suggest_alternative_phrasing(self, claim: FactClaim, evidence_analysis: Dict) -> str:
        """Suggest alternative phrasing based on available evidence"""
        original = claim.claim_text
        
        # Make claim more conservative based on evidence quality
        if claim.claim_type == "statistic":
            # Add uncertainty qualifiers
            if "studies show" in original.lower():
                return original.replace("studies show", "some studies suggest")
            elif re.search(r'\d+%', original):
                return f"Research indicates that approximately {original}"
        
        elif claim.claim_type == "superlative":
            # Soften superlatives
            replacements = {
                "best": "among the leading",
                "leading": "recognised",
                "#1": "highly regarded",
                "top": "respected",
                "most": "highly"
            }
            
            modified = original
            for strong, soft in replacements.items():
                if strong in original.lower():
                    modified = re.sub(rf'\b{strong}\b', soft, modified, flags=re.IGNORECASE)
                    break
            
            return modified
        
        elif claim.claim_type == "research_claim":
            # Add qualifying language
            if "proves" in original.lower():
                return original.replace("proves", "suggests")
            elif "shows" in original.lower():
                return original.replace("shows", "indicates")
        
        # Generic softening
        return f"According to available research, {original.lower()}"
    
    def _suggest_conservative_phrasing(self, claim: FactClaim) -> str:
        """Suggest conservative phrasing for unverified claims"""
        original = claim.claim_text
        
        conservative_replacements = {
            "proven": "reported",
            "guaranteed": "aimed to achieve",
            "always": "typically",
            "never": "rarely",
            "best": "among the quality",
            "leading": "established",
            "#1": "recognised",
            "100%": "highly",
            "all": "many",
            "every": "most"
        }
        
        modified = original
        for strong, conservative in conservative_replacements.items():
            if strong in original.lower():
                modified = re.sub(rf'\b{strong}\b', conservative, modified, flags=re.IGNORECASE)
        
        # Add qualifying prefix if still strong
        strong_indicators = ["industry-leading", "world-class", "cutting-edge"]
        if any(indicator in modified.lower() for indicator in strong_indicators):
            modified = f"We strive to provide {modified.lower()}"
        
        return modified
    
    def _additional_high_risk_verification(self, claim: FactClaim) -> Dict[str, Any]:
        """Additional verification for high-risk claims"""
        verification = {
            "downgrade_confidence": False,
            "notes": []
        }
        
        claim_lower = claim.claim_text.lower()
        
        # Check for absolute statements
        absolute_terms = ["always", "never", "all", "every", "100%", "guaranteed", "proven"]
        if any(term in claim_lower for term in absolute_terms):
            verification["downgrade_confidence"] = True
            verification["notes"].append("Contains absolute statements requiring exceptional evidence")
        
        # Check for competitive claims
        competitive_terms = ["best", "leading", "#1", "top", "fastest", "largest"]
        if any(term in claim_lower for term in competitive_terms):
            verification["notes"].append("Competitive claim requires comparative evidence")
            
            # Try to find comparative data
            comparison_query = f"market share comparison {' '.join(self._extract_key_terms(claim_lower)[:3])}"
            try:
                comparison_search = serpapi.search_google(
                    query=comparison_query,
                    location="Australia",
                    num_results=10
                )
                
                if comparison_search.success:
                    results = comparison_search.data.get("search_results", [])
                    credible_comparisons = self._filter_credible_sources(results)
                    
                    if len(credible_comparisons) < 2:
                        verification["downgrade_confidence"] = True
                        verification["notes"].append("Insufficient comparative data found")
                
            except Exception as e:
                verification["notes"].append(f"Comparative verification failed: {str(e)}")
        
        return verification
    
    def _save_verification_report(self, client_domain: str, claims: List[FactClaim], 
                                results: List[VerificationResult]):
        """Save fact verification report"""
        try:
            report = {
                "client_domain": client_domain,
                "verification_timestamp": datetime.now().isoformat(),
                "total_claims": len(claims),
                "claims_verified": sum(1 for r in results if r.verification_status == "verified"),
                "claims_requiring_revision": sum(1 for r in results if "revise" in r.recommended_action),
                "high_risk_claims": sum(1 for c in claims if c.risk_level in ["high", "critical"]),
                "overall_confidence": sum(r.confidence_score for r in results) / max(len(results), 1),
                "claims": [asdict(claim) for claim in claims],
                "verification_results": [asdict(result) for result in results],
                "summary_recommendations": self._generate_summary_recommendations(results)
            }
            
            filename = f"fact_verification_{client_domain}_{int(datetime.now().timestamp())}.json"
            filepath = self.verification_cache_path / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Fact verification report saved: {filepath}")
            
        except Exception as e:
            logger.error(f"Failed to save verification report: {str(e)}")
    
    def _generate_summary_recommendations(self, results: List[VerificationResult]) -> List[str]:
        """Generate summary recommendations based on verification results"""
        recommendations = []
        
        # Count recommendation types
        action_counts = {}
        for result in results:
            action = result.recommended_action
            action_counts[action] = action_counts.get(action, 0) + 1
        
        # Generate recommendations based on common issues
        if action_counts.get("remove_or_replace", 0) > 0:
            recommendations.append(f"Remove or replace {action_counts['remove_or_replace']} unsubstantiated claims")
        
        if action_counts.get("revise_and_cite", 0) > 0:
            recommendations.append(f"Revise and add citations for {action_counts['revise_and_cite']} partially verified claims")
        
        if action_counts.get("approved_with_citation", 0) > 0:
            recommendations.append(f"Add proper citations for {action_counts['approved_with_citation']} verified claims")
        
        if action_counts.get("manual_verification_required", 0) > 0:
            recommendations.append(f"Conduct manual verification for {action_counts['manual_verification_required']} claims")
        
        # Overall content quality recommendation
        overall_confidence = sum(r.confidence_score for r in results) / max(len(results), 1)
        
        if overall_confidence >= 0.8:
            recommendations.append("Content has strong factual foundation - proceed with citation additions")
        elif overall_confidence >= 0.6:
            recommendations.append("Content requires moderate revision for factual accuracy")
        else:
            recommendations.append("Content requires significant fact-checking and revision before publication")
        
        return recommendations
    
    def generate_citation_requirements(self, verification_results: List[VerificationResult]) -> Dict[str, Any]:
        """Generate citation requirements for verified claims"""
        citation_requirements = {
            "immediate_citations_needed": [],
            "source_research_needed": [],
            "alternative_phrasing_suggested": [],
            "removal_recommended": []
        }
        
        for result in verification_results:
            if result.recommended_action == "approved_with_citation":
                citation_requirements["immediate_citations_needed"].append({
                    "claim": result.original_claim,
                    "confidence": result.confidence_score,
                    "credible_sources_found": result.credible_sources
                })
            
            elif result.recommended_action == "revise_and_cite":
                citation_requirements["source_research_needed"].append({
                    "claim": result.original_claim,
                    "alternative": result.alternative_phrasing,
                    "evidence_quality": result.evidence_quality
                })
            
            elif result.alternative_phrasing and result.recommended_action != "approved_with_citation":
                citation_requirements["alternative_phrasing_suggested"].append({
                    "original": result.original_claim,
                    "suggested": result.alternative_phrasing,
                    "reason": "Insufficient evidence for original claim"
                })
            
            elif result.recommended_action == "remove_or_replace":
                citation_requirements["removal_recommended"].append({
                    "claim": result.original_claim,
                    "reason": f"No credible evidence found ({result.credible_sources} sources)"
                })
        
        return citation_requirements
    
    def validate_business_claims_compliance(self, content: str) -> Dict[str, Any]:
        """Validate content for common business compliance issues"""
        compliance_issues = {
            "unsupported_superlatives": [],
            "unsubstantiated_guarantees": [],
            "missing_disclaimers": [],
            "competitive_claims_unverified": [],
            "regulatory_compliance_flags": []
        }
        
        content_lower = content.lower()
        
        # Check for unsupported superlatives
        for phrase in self.warning_phrases:
            if phrase in content_lower:
                compliance_issues["unsupported_superlatives"].append({
                    "phrase": phrase,
                    "recommendation": "Add qualification or provide supporting evidence"
                })
        
        # Check for guarantees without disclaimers
        guarantee_patterns = [r'guarantee\w*', r'100% effective', r'always works', r'never fails']
        for pattern in guarantee_patterns:
            matches = re.finditer(pattern, content_lower)
            for match in matches:
                compliance_issues["unsubstantiated_guarantees"].append({
                    "text": match.group(),
                    "recommendation": "Add appropriate disclaimers or soften language"
                })
        
        # Check for competitive claims
        competitive_patterns = [r'better than \w+', r'vs\.? \w+', r'compared to \w+']
        for pattern in competitive_patterns:
            matches = re.finditer(pattern, content_lower)
            for match in matches:
                compliance_issues["competitive_claims_unverified"].append({
                    "text": match.group(),
                    "recommendation": "Provide comparative data or remove comparison"
                })
        
        return compliance_issues


# Initialize fact verification system
fact_verification = FactVerificationProtocols()

# Export main components
__all__ = [
    'FactVerificationProtocols',
    'FactClaim',
    'VerificationResult', 
    'fact_verification'
]