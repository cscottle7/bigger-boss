# Dr Graeme Brown - Content Reorganization Plan

**Issue Identified:** Standard deliverable files contain template placeholders instead of actual research content.

**Solution:** Extract content from PHASE files and reorganize into required deliverable structure.

---

## Current State vs Required State

### PHASE Files (Current - 148KB of real content)
```
research/
├── PHASE_1_FOUNDATION_RESEARCH_STRATEGIC_ANALYSIS.md (44KB)
├── PHASE_2_COMPETITIVE_INTELLIGENCE_SEARCH_LANDSCAPE.md (36KB)
├── PHASE_3_ADVANCED_SEO_KEYWORD_STRATEGY.md (28KB)
content/
└── PHASE_4_CONTENT_PLANNING_12_MONTH_CALENDAR.md (40KB)
```

### Required Deliverables Structure
```
research/
├── audience_personas.md ← Extract from PHASE_1 Section 2
├── competitive_analysis.md ← Extract from PHASE_1 Section 6 + PHASE_2 Section 1
├── keyword_research.md ← Extract from PHASE_3 Section 1
└── search_landscape_analysis.md ← Extract from PHASE_2 Section 4

strategy/
├── research_brief.md ← Keep existing (has content)
├── current_website_analysis.md ← Extract from PHASE_2 Section 5
├── user_journey_mapping.md ← NEW: Extract from PHASE_1 Section 2
└── implementation_plan.md ← Keep existing (has content)

content/
├── audience_style_guide.md ← ENHANCE: Currently generic, add Dr Brown specifics
├── content_research.md ← Extract from PHASE_2 Section 3 (Content Gap Analysis)
├── comprehensive_website_content_plans.md ← Extract from PHASE_4
├── annual_content_calendar.md ← Extract from PHASE_4 Section 1
├── content_hubs_pillar_strategy.md ← NEW: Extract from PHASE_4 Section 2
└── detailed_page_layouts.md ← NEW: Create from content planning

technical/
├── ai_optimization_guide.md ← Extract from PHASE_4 Section 3
├── technical_audit.md ← NEEDS CREATION (if requested)
├── ux_ui_analysis.md ← NEEDS CREATION (if requested)
└── site_architecture_proposal.md ← NEW: Create from content planning

implementation/
├── execution_tracking_report.md ← Keep existing
└── task_deps.md ← Keep existing
```

---

## Content Extraction Mapping

### From PHASE_1_FOUNDATION_RESEARCH_STRATEGIC_ANALYSIS.md

**Extract to: `research/audience_personas.md`**
- Section 2: Audience Research & Detailed Personas
  - Persona 1: Active Retiree - "Margaret"
  - Persona 2: Working Professional - "David"
  - Persona 3: Sports Enthusiast - "Sarah"

**Extract to: `strategy/user_journey_mapping.md`** (NEW)
- Section 2: Patient Journey Stages (6 stages)
- Persona-specific journey flows
- Touchpoint mapping

**Extract to: `research/competitive_analysis.md`**
- Section 6: Competitor SWOT Analysis (Top 5 Competitors)
  - Barwon Orthopaedic Group
  - Dr Adrian Tai
  - Dr Simon Journeaux
  - Geelong Orthopaedics
  - Ocean Grove Orthopaedics

**Extract to: `strategy/brand_swot_analysis.md`** (NEW)
- Section 5: Brand SWOT Analysis

**Extract to: `research/market_analysis.md`** (NEW)
- Section 3: Market Research & Analysis

**Extract to: `research/usp_competitive_differentiation.md`** (NEW)
- Section 4: USP Analysis & Competitive Differentiation

---

### From PHASE_2_COMPETITIVE_INTELLIGENCE_SEARCH_LANDSCAPE.md

**Extract to: `research/competitive_positioning.md`** (NEW)
- Section 1: Brand & Competitor Positioning Analysis

**Extract to: `research/trending_topics.md`** (NEW)
- Section 2: Trending Topics Research
  - Sports injury recovery innovations
  - Minimally invasive techniques
  - Patient education priorities

**Extract to: `content/content_research.md`** (REPLACE TEMPLATE)
- Section 3: Content Gap Analysis
  - Missing content opportunities
  - Competitor content strengths

**Extract to: `research/search_landscape_analysis.md`** (NEW)
- Section 4: Search Landscape Analysis
  - Market size and opportunity
  - Competition levels
  - Seasonal trends
  - Local SEO gaps

**Extract to: `strategy/current_website_analysis.md`** (REPLACE TEMPLATE)
- Section 5: Competitor Content Audit Summary
  - Website analysis findings
  - Mobile experience assessment
  - User journey evaluation

---

### From PHASE_3_ADVANCED_SEO_KEYWORD_STRATEGY.md

**Extract to: `research/keyword_research.md`** (REPLACE TEMPLATE)
- Section 1: Comprehensive Keyword Research
  - Primary keywords
  - Secondary keywords
  - Long-tail opportunities

**Extract to: `research/search_intent_analysis.md`** (NEW)
- Section 2: Search Intent Analysis & User Intent Mapping
  - Informational intent
  - Navigational intent
  - Transactional intent
  - Commercial investigation

**Extract to: `research/keyword_gap_analysis.md`** (NEW)
- Section 3: Keyword Gap Analysis
  - Competitor keyword advantages
  - Untapped opportunities

**Extract to: `research/funnel_keywords.md`** (NEW)
- Section 4: Funnel Stage Keywords Mapping
  - Top of funnel (Awareness)
  - Middle of funnel (Consideration)
  - Bottom of funnel (Decision)

**Extract to: `research/emerging_trends_keywords.md`** (NEW)
- Section 5: Emerging Trends Keywords & Future-Proofing

---

### From PHASE_4_CONTENT_PLANNING_12_MONTH_CALENDAR.md

**Extract to: `content/annual_content_calendar.md`** (NEW)
- Section 1: Detailed 12-Month Content Calendar
  - Monthly content themes
  - Blog post schedule
  - Seasonal opportunities

**Extract to: `content/content_hubs_pillar_strategy.md`** (NEW)
- Section 2: Topic Cluster Mapping & Internal Linking Strategy
  - Content hub architecture
  - Pillar page topics
  - Supporting content clusters

**Extract to: `technical/ai_optimization_guide.md`** (REPLACE TEMPLATE)
- Section 3: AI Optimization & Voice Search Strategy
  - AI citability framework
  - Voice search optimization
  - Featured snippet targeting

**Extract to: `content/comprehensive_website_content_plans.md`** (REPLACE TEMPLATE)
- All sections combined
- Content recommendations
- Page specifications

---

## New Deliverables to Create

### 1. Site Architecture Proposal
**File:** `technical/site_architecture_proposal.md`

**Content Sources:**
- PHASE_4 topic clusters
- PHASE_2 competitor site structures
- Content calendar page requirements

**Structure:**
```markdown
# Site Architecture Proposal
## Homepage
## Service Pages (Knee, Shoulder, Hip)
## Condition Pages
## Procedure Pages
## Patient Resources
## About/Contact
## Navigation Structure
## Internal Linking Strategy
```

---

### 2. Detailed Page Layouts
**File:** `content/detailed_page_layouts.md`

**Content Sources:**
- PHASE_4 content planning
- Industry best practices
- Competitor analysis findings

**Structure:**
```markdown
# Detailed Page Content Layouts

## Homepage Layout
### Hero Section
### Services Overview
### About Dr Brown
### Patient Testimonials
### CTA Sections

## Service Page Template
### Page Header
### Overview Section
### Treatment Approach
### What to Expect
### FAQs
### CTA

[Repeat for each page type]
```

---

### 3. User Journey Mapping
**File:** `strategy/user_journey_mapping.md`

**Content Sources:**
- PHASE_1 patient journey stages
- PHASE_1 persona journeys
- PHASE_3 search intent mapping

**Structure:**
```markdown
# Comprehensive User Journey Mapping

## Patient Journey Stages
1. Problem Awareness
2. Research Phase
3. Evaluation Phase
4. Decision Phase
5. Pre-Surgery
6. Post-Surgery

## Persona-Specific Journeys
### Margaret's Journey
### David's Journey
### Sarah's Journey

## Touchpoint Mapping
## Content Alignment by Stage
```

---

## Implementation Steps

### Step 1: Extract & Replace Templates (Priority 1)
1. ✅ Extract audience personas from PHASE_1 → `research/audience_personas.md`
2. ✅ Extract keyword research from PHASE_3 → `research/keyword_research.md`
3. ✅ Extract content gap analysis from PHASE_2 → `content/content_research.md`
4. ✅ Extract website analysis from PHASE_2 → `strategy/current_website_analysis.md`
5. ✅ Extract AI optimization from PHASE_4 → `technical/ai_optimization_guide.md`
6. ✅ Extract competitive analysis from PHASE_1 → `research/competitive_analysis.md`

### Step 2: Create New Deliverables (Priority 2)
7. ✅ Create user journey mapping from PHASE_1
8. ✅ Create content hubs strategy from PHASE_4
9. ✅ Create annual content calendar from PHASE_4
10. ✅ Create search landscape analysis from PHASE_2
11. ✅ Create search intent analysis from PHASE_3

### Step 3: Create Missing Deliverables (Priority 3)
12. ✅ Create site architecture proposal
13. ✅ Create detailed page layouts
14. ⚠️ Technical audit (if requested by client)
15. ⚠️ UX/UI analysis (if requested by client)

### Step 4: Enhance Existing Files (Priority 4)
16. ✅ Enhance audience style guide with Dr Brown specifics
17. ✅ Review and enhance implementation plan
18. ✅ Review and enhance research brief

### Step 5: Clean Up (Final)
19. ✅ Archive or delete PHASE files (keep as reference)
20. ✅ Update PROJECT_OVERVIEW.md with new structure
21. ✅ Create comprehensive README.md with file index

---

## Estimated Timeline

- **Step 1:** 2-3 hours (extract and replace 6 files)
- **Step 2:** 2-3 hours (create 5 new deliverables)
- **Step 3:** 3-4 hours (create site architecture and page layouts)
- **Step 4:** 1-2 hours (enhance 3 existing files)
- **Step 5:** 30 minutes (cleanup and documentation)

**Total:** 8-12 hours for complete reorganization

---

## Quality Assurance Checklist

- [ ] All required deliverables present
- [ ] No template placeholder text remaining
- [ ] All content sourced from PHASE research
- [ ] Citations and sources preserved
- [ ] File sizes appropriate (5-20KB per file)
- [ ] Cross-references between documents work
- [ ] README.md provides clear navigation
- [ ] PROJECT_OVERVIEW.md updated
- [ ] British English compliance throughout
- [ ] Professional medical terminology correct

---

**Next Action:** Proceed with Step 1 extraction and replacement of template files with actual PHASE content?
