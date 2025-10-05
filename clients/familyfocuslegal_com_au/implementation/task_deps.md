# Family Focus Legal - Task Dependencies & Workflow Integration

## Project Workflow with Mandatory Research Phases & Feedback Loops

### Phase 1: Foundation Research & Strategic Analysis
```yaml
sop_compliance_check_legal:
  type: ComplianceVerification
  description: Verify Family Focus Legal against existing legal industry standards and content compliance
  agent: brand_compliance_auditor
  dependencies: []
  outputs: [legal_compliance_baseline, industry_standards_verification]
  estimated_duration: 2 hours
  success_criteria:
    - Legal industry standards identified
    - Compliance gaps documented
    - Brand consistency requirements established

audience_research_legal_services:
  type: AudienceAnalysis
  description: Develop detailed buyer personas (3-7) for legal services clients in Camden, NSW
  agent: audience_intent_researcher
  dependencies: []
  outputs: [legal_client_personas, behavioral_patterns, content_preferences]
  estimated_duration: 3 hours
  success_criteria:
    - Minimum 3 detailed personas created
    - Legal client journey mapping completed
    - Content preference analysis finished

market_research_camden_legal:
  type: MarketIntelligence
  description: Camden, NSW legal services market analysis including opportunities and challenges
  agent: brand_sentiment_researcher
  dependencies: []
  outputs: [market_conditions_analysis, opportunity_assessment, challenge_identification]
  estimated_duration: 3 hours
  success_criteria:
    - Local market conditions documented
    - Growth opportunities identified
    - Competitive challenges assessed

usp_brand_swot_analysis:
  type: StrategicAnalysis
  description: USP analysis and brand SWOT for Family Focus Legal competitive differentiation
  agent: brand_analyst
  dependencies: []
  outputs: [usp_definition, brand_swot_matrix, differentiation_strategy]
  estimated_duration: 2.5 hours
  success_criteria:
    - Unique selling propositions defined
    - SWOT analysis completed
    - Competitive differentiation identified

competitor_swot_analysis:
  type: CompetitiveIntelligence
  description: Top 5 competitors SWOT analysis and strategic positioning assessment
  agent: competitive_intelligence_searcher
  dependencies: []
  outputs: [competitor_swot_matrices, positioning_analysis, strategic_insights]
  estimated_duration: 4 hours
  success_criteria:
    - 5 competitors identified and analysed
    - Strategic positioning mapped
    - Competitive advantages documented
```

### Phase 2: Competitive Intelligence & Search Landscape
```yaml
brand_competitor_positioning:
  type: PositioningAnalysis
  description: Legal services brand positioning and competitive differentiation analysis
  agent: brand_strategy_researcher
  dependencies: [usp_brand_swot_analysis, competitor_swot_analysis]
  outputs: [positioning_strategy, messaging_analysis, differentiation_framework]
  estimated_duration: 3 hours
  success_criteria:
    - Brand positioning defined
    - Competitive messaging analysis completed
    - Differentiation strategy established

trending_topics_legal_industry:
  type: TrendResearch
  description: Current legal industry trends and hot topics identification
  agent: technical_research_specialist
  dependencies: []
  outputs: [industry_trends_report, hot_topics_analysis, emerging_themes]
  estimated_duration: 2.5 hours
  success_criteria:
    - Current trends identified
    - Hot topics documented
    - Emerging themes mapped

content_gap_analysis_legal:
  type: ContentGapAnalysis
  description: Legal services market content gap identification and opportunities
  agent: competitor_analyzer
  dependencies: [competitor_swot_analysis]
  outputs: [content_gaps_report, opportunity_matrix, differentiation_possibilities]
  estimated_duration: 3.5 hours
  success_criteria:
    - Content gaps identified
    - Market opportunities mapped
    - Content differentiation possibilities documented

search_landscape_legal_services:
  type: SearchLandscapeAnalysis
  description: Legal services search landscape including market size and competition analysis
  agent: seo_strategist
  dependencies: []
  outputs: [search_market_analysis, competition_levels, seasonal_trends, local_seo_gaps]
  estimated_duration: 3 hours
  success_criteria:
    - Search market size documented
    - Competition levels assessed
    - Local SEO opportunities identified

competitor_content_audit:
  type: ContentAudit
  description: Competitor content audit including website analysis and user journey mapping
  agent: competitive_intelligence_searcher
  dependencies: [competitor_swot_analysis]
  outputs: [competitor_content_analysis, user_journey_maps, mobile_experience_audit]
  estimated_duration: 4 hours
  success_criteria:
    - Competitor content analysed
    - User journeys mapped
    - Mobile experience assessed
```

### Phase 3: Advanced SEO & Keyword Strategy
```yaml
comprehensive_keyword_research:
  type: KeywordResearch
  description: Legal services keyword research and content-keyword optimisation
  agent: keyword_researcher
  dependencies: [search_landscape_legal_services]
  outputs: [keyword_strategy, search_intent_analysis, content_keyword_mapping]
  estimated_duration: 4 hours
  success_criteria:
    - Comprehensive keyword list created
    - Search intent mapped
    - Content-keyword alignment established

keyword_gap_analysis:
  type: KeywordGapAnalysis
  description: SEO opportunity identification and competitive keyword gaps
  agent: seo_strategist
  dependencies: [comprehensive_keyword_research, competitor_content_audit]
  outputs: [keyword_opportunities, competitive_gaps, untapped_angles]
  estimated_duration: 3 hours
  success_criteria:
    - Keyword gaps identified
    - Competitive opportunities mapped
    - Untapped angles documented

funnel_stage_keyword_mapping:
  type: FunnelKeywordMapping
  description: Legal client funnel keyword mapping (awareness → consideration → decision)
  agent: keyword_researcher
  dependencies: [comprehensive_keyword_research, audience_research_legal_services]
  outputs: [funnel_keyword_matrix, client_journey_keywords, conversion_path_mapping]
  estimated_duration: 3.5 hours
  success_criteria:
    - Funnel stages mapped to keywords
    - Client journey keywords identified
    - Conversion paths optimised

emerging_trends_keywords:
  type: EmergingTrendsResearch
  description: Future-proofing legal content with trending search terms
  agent: technical_research_specialist
  dependencies: [trending_topics_legal_industry, comprehensive_keyword_research]
  outputs: [emerging_keyword_trends, future_content_opportunities, voice_search_optimization]
  estimated_duration: 2.5 hours
  success_criteria:
    - Emerging keyword trends identified
    - Future content opportunities mapped
    - Voice search optimisation planned
```

### Phase 4: Content Planning & AI Optimization
```yaml
detailed_content_briefs:
  type: ContentBriefDevelopment
  description: Legal services content briefs with page layouts and conversion paths
  agent: content_strategist
  dependencies: [all_phase_3_tasks]
  outputs: [content_brief_templates, page_layouts, conversion_paths, wireframes]
  estimated_duration: 4 hours
  success_criteria:
    - Content briefs created
    - Page layouts designed
    - Conversion paths optimised

content_structure_specifications:
  type: ContentStructureDesign
  description: Headlines, sections, CTAs, and internal linking strategy
  agent: page_content_brief_agent
  dependencies: [detailed_content_briefs]
  outputs: [content_structures, headline_frameworks, cta_strategy, linking_strategy]
  estimated_duration: 3.5 hours
  success_criteria:
    - Content structures defined
    - Headline frameworks established
    - Internal linking strategy created

ai_readiness_optimization:
  type: AIOptimization
  description: Content structure optimised for AI systems and voice search
  agent: ai_specialist_agent
  dependencies: [content_structure_specifications]
  outputs: [ai_optimization_guide, voice_search_specs, schema_markup_plan]
  estimated_duration: 3 hours
  success_criteria:
    - AI optimisation completed
    - Voice search compatibility ensured
    - Schema markup planned

strategic_content_ideas:
  type: ContentIdeation
  description: Creative legal content ideation based on research foundation
  agent: blog_ideation_specialist
  dependencies: [all_phase_3_tasks, detailed_content_briefs]
  outputs: [content_ideas_bank, blog_topics, series_concepts]
  estimated_duration: 3 hours
  success_criteria:
    - Content ideas generated
    - Blog topics planned
    - Content series concepts developed

content_calendar_development:
  type: ContentCalendarCreation
  description: 12-month strategic content planning with legal industry focus
  agent: content_strategist
  dependencies: [strategic_content_ideas, funnel_stage_keyword_mapping]
  outputs: [annual_content_calendar, publishing_schedule, content_series_planning]
  estimated_duration: 3.5 hours
  success_criteria:
    - 12-month calendar created
    - Publishing schedule established
    - Content series planned

content_mapping_clusters:
  type: ContentClusterMapping
  description: Content clusters and topic authority building strategy
  agent: content_strategist
  dependencies: [content_calendar_development, ai_readiness_optimization]
  outputs: [content_cluster_map, topic_authority_strategy, content_interconnection]
  estimated_duration: 3 hours
  success_criteria:
    - Content clusters mapped
    - Topic authority strategy defined
    - Content interconnection planned
```

### Phase 5: Website Analysis & Content Strategy Development
```yaml
current_website_analysis:
  type: WebsiteAnalysis
  description: Extract and analyse current familyfocuslegal.com.au content
  agent: sitespect_orchestrator
  dependencies: [all_phase_4_tasks]
  outputs: [current_content_audit, improvement_recommendations, technical_analysis]
  estimated_duration: 4 hours
  success_criteria:
    - Current content extracted
    - Improvement areas identified
    - Technical recommendations provided

comprehensive_content_strategy:
  type: ContentStrategyCreation
  description: Develop content hub architecture with pillar pages and blog strategy
  agent: content_strategist
  dependencies: [current_website_analysis, content_mapping_clusters]
  outputs: [content_hub_architecture, pillar_page_strategy, blog_content_plan]
  estimated_duration: 4 hours
  success_criteria:
    - Content hub architecture designed
    - Pillar page strategy created
    - Blog content plan established
```

### Phase 6: Iterative Feedback Loop Integration
```yaml
feedback_loop_content_strategy:
  type: IterativeImprovement
  description: Multi-agent iterative feedback loop for content strategy optimisation
  dependencies: [comprehensive_content_strategy]
  agent_sequence: [clarity_conciseness_editor, cognitive_load_minimizer, content_critique_specialist, ai_text_naturalizer]
  max_iterations: 3
  success_criteria:
    - clarity_conciseness_editor: ≥8/10
    - cognitive_load_minimizer: ≥7/10
    - content_critique_specialist: ≥7/10
    - ai_text_naturalizer: ≥8/10
    - Aggregate score: ≥8.5/10
  outputs: [optimised_content_strategy, quality_scores, improvement_tracking]

feedback_loop_pillar_pages:
  type: IterativeImprovement
  description: Multi-agent iterative feedback loop for pillar page optimisation
  dependencies: [comprehensive_content_strategy]
  agent_sequence: [clarity_conciseness_editor, cognitive_load_minimizer, content_critique_specialist, ai_text_naturalizer]
  max_iterations: 3
  success_criteria:
    - clarity_conciseness_editor: ≥8/10
    - cognitive_load_minimizer: ≥7/10
    - content_critique_specialist: ≥7/10
    - ai_text_naturalizer: ≥8/10
    - Aggregate score: ≥8.5/10
  outputs: [optimised_pillar_pages, quality_scores, improvement_tracking]

feedback_loop_blog_content:
  type: IterativeImprovement
  description: Multi-agent iterative feedback loop for blog content optimisation
  dependencies: [comprehensive_content_strategy]
  agent_sequence: [clarity_conciseness_editor, cognitive_load_minimizer, content_critique_specialist, ai_text_naturalizer]
  max_iterations: 3
  success_criteria:
    - clarity_conciseness_editor: ≥8/10
    - cognitive_load_minimizer: ≥7/10
    - content_critique_specialist: ≥7/10
    - ai_text_naturalizer: ≥8/10
    - Aggregate score: ≥8.5/10
  outputs: [optimised_blog_content, quality_scores, improvement_tracking]
```

### Phase 7: Quality Assurance & Compliance Verification
```yaml
australian_english_compliance:
  type: ComplianceVerification
  description: Verify 100% Australian English compliance across all deliverables
  agent: enhanced_content_auditor
  dependencies: [all_feedback_loops]
  outputs: [compliance_report, correction_recommendations, british_english_verification]
  estimated_duration: 2 hours
  success_criteria:
    - 100% Australian English compliance
    - British spellings verified
    - Legal terminology alignment confirmed

final_quality_assurance:
  type: QualityAssurance
  description: Final multi-perspective quality review and publication readiness
  agent: enhanced_content_auditor
  dependencies: [australian_english_compliance]
  outputs: [final_quality_report, publication_readiness_certification, delivery_recommendations]
  estimated_duration: 2.5 hours
  success_criteria:
    - Quality standards met
    - Publication readiness confirmed
    - Client delivery approved
```

## Workflow Execution Protocol

### Parallel Execution Phases
- **Phase 1 Tasks**: Execute simultaneously for comprehensive foundation
- **Phase 2 Tasks**: Parallel execution building on Phase 1 outputs
- **Phase 3 Tasks**: Coordinate keyword research and SEO strategy

### Sequential Dependencies
- **Phase 4**: Content planning depends on completed research phases
- **Phase 5**: Website analysis and strategy development sequential
- **Phase 6**: Iterative feedback loops applied to all content
- **Phase 7**: Final quality assurance and compliance verification

### Safety Mechanisms
- **Progress Tracking**: Monitor improvement between feedback iterations
- **Human Escalation**: Triggered after 2 cycles with insufficient progress
- **Time Limits**: Maximum iteration time per content piece
- **Quality Gates**: Threshold enforcement before proceeding

### Success Criteria
- **Research Completeness**: All 4 phases documented with sources
- **Quality Threshold**: ≥8.5/10 aggregate score achieved
- **Compliance Verification**: 100% Australian English standards
- **Iterative Improvement**: Measurable progress tracking implemented