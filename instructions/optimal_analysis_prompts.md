# Optimal Analysis Prompts for Comprehensive System Testing

**Document**: Optimal Analysis Prompts Guide  
**Version**: 1.0  
**Date**: 31/08/2025  
**Purpose**: Provide optimal prompts for triggering comprehensive analysis and audit workflows

---

## 🎯 **Primary Full Analysis Prompt**

### Complete Comprehensive Analysis
```
@master_orchestrator Please conduct a comprehensive marketing analysis and audit for [WEBSITE_URL]. I need a complete assessment covering:

1. Technical SEO and website performance analysis
2. Content strategy and optimization opportunities  
3. Competitive positioning and market analysis
4. User experience and conversion optimization
5. Brand compliance and credibility assessment
6. AI readiness and optimization strategy

Generate all required deliverables including technical audits, content strategies, competitive analysis, audience personas, performance baselines, and implementation roadmaps. Ensure all reports include proper folder organization, visual documentation, and British English compliance.

Please coordinate all specialist squads (SiteSpect, ContentForge, StrategyNexus) to provide the most comprehensive analysis possible.
```

---

## 🔥 **Squad-Specific Analysis Prompts**

### SiteSpect Squad - Technical Analysis
```
@sitespect_orchestrator Perform a comprehensive website audit for [WEBSITE_URL] including:

- Technical SEO analysis using Playwright MCP browser automation
- UX/UI analysis with multi-device responsive testing
- AI readiness assessment and optimization strategy  
- Performance testing and Core Web Vitals analysis
- Accessibility compliance evaluation
- Brand compliance and visual standards assessment

Use Playwright MCP for all browser automation, provide visual documentation with screenshots, and organize all reports in website-specific folders. Ensure British English compliance across all deliverables.
```

### ContentForge Squad - Content Strategy
```
@content_workflow_orchestrator Create a complete content strategy for [WEBSITE_URL] including:

- Comprehensive audience research and persona development (3-7 personas)
- Competitive content analysis and positioning opportunities
- Complete keyword strategy with search volumes and intent analysis
- Audience style guide with voice, tone, and communication preferences
- Current page SEO analysis and optimization recommendations
- Content brief with structure and implementation guidelines
- AI optimization guide for content discovery and featured snippets
- Task completion checklist for quality assurance

Generate all research files with actionable data and implementation timelines.
```

### StrategyNexus Squad - Strategic Analysis
```
@strategy_orchestrator Conduct comprehensive strategic analysis for [COMPANY/WEBSITE] including:

- Competitive positioning and market opportunity assessment
- Audience persona development with behavioral analysis
- Content performance baseline establishment and KPI framework
- Brand positioning analysis and competitive differentiation
- Strategic recommendations with ROI projections and timelines
- Implementation roadmap with resource requirements
- Performance measurement framework and success metrics

Coordinate all StrategyNexus specialist agents to provide integrated strategic intelligence.
```

---

## 💡 **Specialized Focus Prompts**

### AI Readiness and Optimization
```
@ai_specialist_agent Conduct a comprehensive AI readiness audit for [WEBSITE_URL]. Analyze:

- AI citability score and content structure optimization
- E-E-A-T authority assessment for AI systems
- Technical infrastructure for AI crawler accessibility
- Competitive AI sourcing and gap analysis
- 90-day AI optimization roadmap with implementation phases

Generate detailed AI optimization guide with specific recommendations for AI search visibility.
```

### Brand Compliance Assessment
```
@brand_compliance_auditor Perform comprehensive brand compliance assessment for [WEBSITE_URL] including:

- Visual brand compliance audit with screenshot documentation
- 100% British English verification and correction matrix
- E-E-A-T credibility evaluation (Experience, Expertise, Authoritativeness, Trustworthiness)
- Content freshness audit with update recommendations
- Australian business context compliance verification

Use Playwright MCP for visual documentation and provide specific correction recommendations.
```

### Technical SEO Deep Dive
```
@technical_seo_analyst Perform detailed technical SEO analysis for [WEBSITE_URL] using ONLY Playwright MCP browser automation. Generate:

- Comprehensive technical SEO audit with implementation priorities
- Detailed on-page SEO extraction report with raw meta tag data
- Schema markup analysis and optimization opportunities
- URL structure and site architecture assessment
- Mobile-first optimization recommendations

MANDATORY: Use browser_navigate, browser_evaluate, and browser_take_screenshot. NEVER use WebFetch. Extract all technical elements using browser JavaScript execution.
```

### UX/UI Analysis
```
@ux_ui_analyst Conduct comprehensive UX/UI analysis for [WEBSITE_URL] using Playwright MCP browser automation:

- Multi-device responsive testing (desktop 1920x1080, tablet 768x1024, mobile 375x667)
- Visual design assessment with screenshot documentation
- Navigation and user journey analysis
- Conversion optimization evaluation
- Accessibility assessment from UX perspective

MANDATORY: Use browser_resize for responsive testing, browser_take_screenshot for visual documentation, and browser_click/hover for interaction testing.
```

---

## 🎯 **Expected Deliverables**

### Complete Analysis Should Generate (16-20 Files):

#### **Core Research Files:**
- `[PROJECT]_research_brief.md` - Comprehensive research findings
- `[PROJECT]_implementation_plan.md` - Step-by-step action items
- `[PROJECT]_competitive_analysis.md` - Market analysis and positioning
- `[PROJECT]_keyword_research.md` - Complete keyword strategy
- `[PROJECT]_content_strategy.md` - Editorial calendar and recommendations
- `[PROJECT]_technical_audit.md` - Website technical findings

#### **Mandatory Analysis Files:**
- `[PROJECT]_ux_ui_analysis.md` - User experience assessment
- `[PROJECT]_ai_optimization_guide.md` - AI readiness audit
- `[PROJECT]_onpage_seo_extraction.md` - Detailed technical data
- `[PROJECT]_execution_tracking_report.md` - Agent activity log
- `[PROJECT]_assumptions_and_methodology.md` - Data sources and critique
- `[PROJECT]_current_page_seo_analysis.md` - SEO baseline assessment

#### **SOP-Required Files:**
- `[PROJECT]_audience_personas.md` - Detailed persona documentation
- `[PROJECT]_eat_credibility_audit.md` - E-E-A-T credibility assessment  
- `[PROJECT]_content_performance_baseline.md` - Performance metrics baseline
- `[PROJECT]_visual_brand_compliance_audit.md` - Brand consistency assessment
- `[PROJECT]_british_english_compliance_report.md` - Language standards verification
- `[PROJECT]_content_freshness_audit.md` - Content update recommendations

---

## 📋 **Quality Assurance Checklist**

### Before Running Analysis:
- [ ] Website URL is accessible and fully functional
- [ ] Industry context provided (healthcare, legal, tech, etc.)
- [ ] Specific analysis goals defined
- [ ] Expected deliverable count confirmed (16-20 files)

### After Analysis Completion:
- [ ] All files organized in website-specific folder
- [ ] Visual documentation included (screenshots, etc.)
- [ ] British English compliance verified
- [ ] Agent execution tracking documented
- [ ] Playwright MCP usage confirmed (not WebFetch)
- [ ] Table of contents included in all reports
- [ ] Data sources and methodology documented

---

## 🚀 **Pro Tips for Optimal Results**

### 1. **Provide Complete Context:**
```
@master_orchestrator Analyze https://drjuliacrawford.com.au/ - this is a medical ENT specialist practice in Sydney, Australia, specializing in robotic surgery, sleep apnoea treatment, and head/neck cancer. Generate comprehensive analysis with all deliverables.
```

### 2. **Request Specific Focus Areas:**
```
Focus particularly on local SEO opportunities, medical industry compliance, and professional credibility signals for this healthcare website.
```

### 3. **Emphasize Quality Requirements:**
```
Ensure 100% British English compliance, comprehensive visual documentation using Playwright MCP, and detailed implementation timelines for all recommendations.
```

### 4. **Verify Tool Usage:**
```
CRITICAL: All website analysis must use Playwright MCP browser automation. Reject any analysis using WebFetch instead of actual browser interaction.
```

---

**Document Control:**
- **Created**: 31/08/2025
- **Purpose**: Comprehensive system testing and analysis execution
- **Usage**: Copy and paste optimal prompts for different analysis scenarios
- **Updates**: Modify prompts based on specific testing requirements and system improvements