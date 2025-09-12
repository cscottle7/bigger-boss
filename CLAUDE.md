# Bigger Boss Agent System - CLAUDE Configuration

## Project Overview
This system provides comprehensive marketing analysis, content strategy, and website optimization services for Australian businesses through specialized AI agents.

## File Organization Standards

### CLIENT FOLDER STRUCTURE
**All client work MUST be organized within the `clients/` folder using this standardized structure:**

```
clients/
└── {client_domain_name}/
    ├── README.md                    # Project navigation hub
    ├── PROJECT_OVERVIEW.md          # Executive summary
    ├── strategy/                    # Strategic planning documents
    │   ├── research_brief.md
    │   ├── current_website_analysis.md
    │   └── implementation_plan.md
    ├── research/                    # Market intelligence & analysis
    │   ├── competitive_analysis.md
    │   ├── audience_personas.md
    │   └── keyword_research.md
    ├── content/                     # Content strategy & guidelines
    │   ├── comprehensive_website_content_plans.md
    │   ├── content_research.md
    │   └── audience_style_guide.md
    ├── technical/                   # Technical audits & recommendations
    │   ├── technical_audit.md
    │   ├── ai_optimization_guide.md
    │   └── ux_ui_analysis.md
    └── implementation/              # Execution tracking
        ├── task_deps.md             # Task dependency plan with feedback loops
        └── execution_tracking_report.md
```

### MANDATORY REQUIREMENTS FOR ALL AGENTS:
1. **ALWAYS create client files in `clients/{client_domain}/` folder**
2. **NEVER create files in root directory or random folders**
3. **Use the standardized subfolder structure above**
4. **Create README.md as project navigation hub**
5. **Follow consistent file naming conventions**

## Iterative Feedback Loop System

### MANDATORY FEEDBACK LOOP INTEGRATION
**All content creation MUST use iterative feedback loops instead of linear QA:**

#### Required Feedback Loop Agents
1. **clarity_conciseness_editor** (Threshold: 8/10)
   - Grammar, spelling, sentence structure optimization
   - Flow enhancement and conciseness improvement
   - Australian English compliance verification

2. **cognitive_load_minimizer** (Threshold: 7/10)
   - Information hierarchy optimization
   - Cognitive complexity reduction using cognitive science principles
   - Scanability and processing ease enhancement

3. **content_critique_specialist** (Threshold: 7/10)
   - Argument strengthening and logical consistency verification
   - Evidence support verification and assumption clarity
   - Critical analysis using Toulmin Model framework

4. **ai_text_naturalizer** (Threshold: 8/10)
   - AI artifact removal and natural flow optimization
   - Human expression enhancement and personality injection
   - Conversational tone balancing while maintaining professionalism

#### Feedback Loop Process
```yaml
iterative_workflow:
  sequence: [clarity_conciseness_editor → cognitive_load_minimizer → content_critique_specialist → ai_text_naturalizer]
  max_iterations: 3
  loop_back_trigger: score_below_threshold
  refinement_agent: content_refiner
  final_gate: enhanced_content_auditor
  safety_mechanisms: [progress_tracking, human_escalation, time_limits]
```

#### Quality Scoring Requirements
- **Individual Agent Thresholds**: Must be met before proceeding to next agent
- **Aggregate Score Target**: ≥8.5/10 for final approval
- **Improvement Tracking**: Measurable progress required between iterations
- **Human Escalation**: Triggered after 2 cycles with no improvement

### task_deps.md Template Integration
**All projects MUST include feedback loop phases:**
```yaml
feedback_loop_[content_name]:
  type: IterativeImprovement
  description: Multi-agent iterative feedback loop for content optimization
  dependencies: [create_content]
  agent_sequence: [clarity_conciseness_editor, cognitive_load_minimizer, content_critique_specialist, ai_text_naturalizer]
  max_iterations: 3
  success_criteria:
    - All agent thresholds met
    - Aggregate score ≥8.5/10
```

## Content Quality Standards

### CITATION REQUIREMENTS
**All content MUST include credible source citations for:**
- Statistics and data points
- Industry research findings
- Performance benchmarks
- Market trend claims
- Technical specifications
- Best practice recommendations

### CITATION FORMAT:
```
**Source:** [Organization Name - Report Title](URL) - Date
```

Example:
```
Australian businesses spend an average of $2,400 monthly on digital marketing.
**Source:** [Salesforce Australia - State of Marketing Report 2024](https://salesforce.com/au/resources/research-reports/state-of-marketing/) - January 2024
```

## Agent Instructions

### BEFORE STARTING ANY CLIENT PROJECT:
1. ✅ Create proper folder structure in `clients/{client_domain}/`
2. ✅ Use standardized subfolder organization
3. ✅ **COMPLETE MANDATORY RESEARCH WORKFLOW** (4 phases) before any content creation
4. ✅ Create task_deps.md with integrated feedback loops AND research phases
5. ✅ Include source citations for all claims and statistics
6. ✅ Create README.md for project navigation
7. ✅ Follow Australian English spelling and terminology

### MANDATORY RESEARCH VERIFICATION:
Before content creation begins, verify completion of:

#### Phase 1 Verification:
- [ ] SOP compliance check completed
- [ ] Audience research and style guide created
- [ ] Market research and analysis completed
- [ ] USP analysis and competitive differentiation defined
- [ ] Brand SWOT analysis completed
- [ ] Competitor SWOT analysis (top 5 competitors) completed

#### Phase 2 Verification:
- [ ] Brand and competitor positioning analysis completed
- [ ] Trending topics research conducted
- [ ] Content gap analysis identified
- [ ] Search landscape analysis (market size, competition levels, seasonal trends) completed
- [ ] Competitor content audit (websites, mobile experience, user journeys) finished

#### Phase 3 Verification:
- [ ] Comprehensive keyword research completed
- [ ] Search intent analysis and user journey mapping finished
- [ ] Keyword gap analysis identified
- [ ] Funnel stage keywords mapped (awareness, consideration, decision)
- [ ] Untapped angle keywords (zero/low competition) identified
- [ ] Emerging trends keywords researched and documented

#### Phase 4 Verification:
- [ ] Detailed content briefs with page layouts created
- [ ] Content structure specifications (headlines, sections, CTAs) defined
- [ ] AI optimization and voice search specifications completed
- [ ] Content ideas generation based on research foundation finished
- [ ] 12-month future content calendar developed
- [ ] Related content mapping and topic clusters planned

### CONTENT REQUEST ROUTING PROTOCOL:
**⚠️ CRITICAL**: All content-related requests MUST be routed through Glenn for proper workflow orchestration:
- Glenn ensures mandatory research phases are completed before content creation
- Glenn routes to `master_orchestrator` with comprehensive research requirements
- Glenn validates proper agent selection and workflow sequencing
- This prevents content creation without proper research foundation

### QUALITY CHECKPOINTS:
- [ ] All files in correct client folder structure
- [ ] task_deps.md includes iterative feedback loop phases
- [ ] Feedback loop agent thresholds configured properly
- [ ] All statistics have credible source citations
- [ ] README.md provides clear project navigation
- [ ] Australian English compliance throughout
- [ ] Consistent file naming conventions used

### ORCHESTRATOR ROLES CLARIFICATION:
- **master_orchestrator**: Primary orchestrator for ALL content-related tasks (content strategy, blog posts, page content, Google Ads, marketing analysis). Coordinates mandatory research phases and specialist agents across SiteSpect, ContentForge, and StrategyNexus squads
- **workflow-orchestrator**: Software development tasks only (code implementation, technical development, CI/CD pipelines)
- **quality_gate_orchestrator**: Manages iterative feedback loops, coordinates agent sequences, tracks scoring, and handles loop termination
- **sitespect_orchestrator**: Coordinates comprehensive website audits through specialized agents with browser automation
- **strategy_orchestrator**: Coordinates strategic analysis across multiple domains with cross-domain integration
- **enhanced_content_auditor**: Final multi-perspective quality review after feedback loops complete
- **content_refiner**: Applies targeted improvements based on specific agent feedback

### MANDATORY RESEARCH WORKFLOW:
**All content requests MUST complete comprehensive research phases before content creation:**

#### Phase 1: Foundation Research & Strategic Analysis
- **SOP Compliance Check**: Verify against existing brand and content standards
- **Audience Research**: Create detailed audience personas and style guides
- **Market Research**: Current market conditions, opportunities, and challenges
- **USP Analysis**: Define unique selling propositions and competitive differentiation
- **Brand SWOT Analysis**: Strengths, weaknesses, opportunities, threats assessment
- **Competitor SWOT Analysis**: Strategic positioning analysis of top 5 competitors

#### Phase 2: Competitive Intelligence & Search Landscape
- **Brand & Competitor Analysis**: Positioning, messaging, and differentiation analysis
- **Trending Topics Research**: Current industry trends and hot topics in the niche
- **Content Gap Analysis**: Identify missing content opportunities in the market
- **Search Landscape Analysis**: Market size, competition levels, seasonal trends, local SEO gaps
- **Competitor Content Audit**: Website analysis, content gaps, mobile experience, user journey mapping

#### Phase 3: Advanced SEO & Keyword Strategy
- **Keyword Research**: Comprehensive SEO-focused keyword identification and mapping
- **Search Intent Analysis**: User intent mapping and content journey optimization
- **Keyword Gap Analysis**: SEO opportunity identification and competitive gaps
- **Funnel Stage Keywords**: Top (awareness), middle (consideration), bottom (decision) funnel mapping
- **Untapped Angle Keywords**: Zero or low-competition keyword opportunities
- **Emerging Trends Keywords**: Future-proofing content with trending search terms

#### Phase 4: Content Planning, Briefs & AI Optimization
- **Detailed Content Briefs**: Page layouts, wireframes, word counts, conversion paths
- **Content Structure Specifications**: Headlines, sections, CTAs, internal linking strategy
- **AI Readiness Optimization**: Content structure optimized for AI systems and voice search
- **Content Ideas Generation**: Creative ideation based on comprehensive research foundation
- **Future Content Calendar**: 12-month strategic content planning with series development
- **Related Content Mapping**: Content clusters and topic authority building strategy

**All phases must be completed before any content creation begins. This ensures research-backed, strategically aligned content that meets client objectives and market demands.**

This configuration ensures all agents maintain organizational consistency, iterative quality improvement, and content credibility across all client projects.

## System-Wide Implementation Requirements

### AGENT DEPLOYMENT:
All projects must have access to these feedback loop agents:
- `clarity_conciseness_editor`
- `cognitive_load_minimizer` 
- `content_critique_specialist`
- `ai_text_naturalizer`
- `content_refiner`
- `quality_gate_orchestrator`
- `enhanced_content_auditor`

### WORKFLOW INTEGRATION:
Replace all linear QA processes with iterative feedback loops in:
- Content creation workflows
- Documentation generation
- Strategic planning documents
- Technical analysis reports
- Implementation guides

This ensures consistent, high-quality output through systematic iterative improvement across all client engagements.