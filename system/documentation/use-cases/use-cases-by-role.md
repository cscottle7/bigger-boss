# Use Cases by Role

## Marketing Director

### Primary Use Cases

#### 1. Campaign Strategy Development
**When to use**: Planning major campaigns or quarterly initiatives
**Squad**: StrategyNexus → ContentForge → SiteSpect
**Workflow**:
```bash
# Step 1: Strategic analysis
python workflows/run_website_strategy.py --primary_url "yoursite.com" --competitors "comp1.com,comp2.com"

# Step 2: Content strategy development  
python workflows/run_content_creation.py --topic "campaign theme" --strategy_file "strategic_analysis.json"

# Step 3: Technical readiness audit
python workflows/run_site_audit.py --url "yoursite.com" --focus "campaign_readiness"
```

**Value Delivered**:
- Data-driven strategic decisions
- Competitive intelligence
- Integrated campaign planning
- Technical implementation roadmap

#### 2. Competitive Intelligence
**When to use**: Monthly competitive reviews, market positioning updates
**Squad**: StrategyNexus
**Workflow**:
```bash
python workflows/run_website_strategy.py --analysis_type "competitive_deep_dive" --competitors "comp1.com,comp2.com,comp3.com,comp4.com"
```

**Value Delivered**:
- Market positioning analysis
- Feature gap identification
- Opportunity assessment
- Strategic recommendations

---

## SEO Specialist

### Primary Use Cases

#### 1. Technical SEO Audit
**When to use**: Monthly site health checks, pre-launch audits, performance troubleshooting
**Squad**: SiteSpect
**Workflow**:
```bash
python workflows/run_site_audit.py --url "target-site.com" --focus "technical_seo" --depth comprehensive
```

**Value Delivered**:
- Complete technical analysis
- Prioritized fix recommendations
- Performance benchmarking
- Accessibility compliance report

#### 2. Content Gap Analysis
**When to use**: Quarterly content strategy reviews, keyword opportunity identification
**Squad**: ContentForge
**Workflow**:
```bash
python workflows/run_content_creation.py --analysis_type "gap_analysis" --competitors_content "competitor_analysis.csv"
```

**Value Delivered**:
- Keyword opportunity identification
- Content format recommendations
- Competitive content analysis
- SEO optimization strategies

#### 3. Performance Monitoring
**When to use**: Regular performance tracking, post-update validation
**Squad**: SiteSpect (Performance focus)
**Workflow**:
```bash
python workflows/run_site_audit.py --url "yoursite.com" --focus "performance_tracking" --compare_previous
```

**Value Delivered**:
- Performance trend analysis
- Core Web Vitals monitoring
- Speed optimization recommendations
- Mobile performance insights

---

## Content Manager

### Primary Use Cases

#### 1. Content Brief Generation
**When to use**: New content projects, campaign content planning
**Squad**: ContentForge
**Workflow**:
```bash
python workflows/run_content_creation.py --topic "content topic" --keywords_file "target_keywords.csv" --brand_guidelines "brand_guide.pdf"
```

**Value Delivered**:
- Research-backed content briefs
- SEO keyword integration
- Brand-aligned recommendations
- Content calendar planning

#### 2. Content Refresh Strategy
**When to use**: Quarterly content audits, performance improvement initiatives
**Squad**: ContentForge (Refresh workflow)
**Workflow**:
```bash
python workflows/run_content_refresh.py --existing_content "content_audit.csv" --performance_goals "traffic_increase"
```

**Value Delivered**:
- Content performance analysis
- Refresh priority ranking
- Optimization recommendations
- Resource allocation planning

#### 3. Audience Research
**When to use**: New target market exploration, persona development
**Squad**: ContentForge (Research Corps focus)
**Workflow**:
```bash
python workflows/run_content_creation.py --analysis_type "audience_research" --target_market "market_description"
```

**Value Delivered**:
- Detailed audience personas
- Intent mapping
- Content preference analysis
- Channel recommendation

---

## Web Developer

### Primary Use Cases

#### 1. Pre-Launch Site Audit
**When to use**: Before major releases, staging environment validation
**Squad**: SiteSpect
**Workflow**:
```bash
python workflows/run_site_audit.py --url "staging.yoursite.com" --focus "pre_launch_checklist" --severity_threshold "medium"
```

**Value Delivered**:
- Complete technical validation
- Performance optimization checklist
- Accessibility compliance verification
- SEO readiness confirmation

#### 2. Performance Debugging
**When to use**: Performance issues, Core Web Vitals failures
**Squad**: SiteSpect (Performance focus)
**Workflow**:
```bash
python workflows/run_site_audit.py --url "problematic-site.com" --focus "performance_diagnostic" --priority critical
```

**Value Delivered**:
- Performance bottleneck identification
- Specific optimization recommendations
- Resource loading analysis
- Mobile performance assessment

#### 3. Accessibility Compliance
**When to use**: ADA compliance checks, accessibility improvement projects
**Squad**: SiteSpect (Accessibility focus)
**Workflow**:
```bash
python workflows/run_site_audit.py --url "yoursite.com" --focus "accessibility_audit" --standards "WCAG_2.1_AA"
```

**Value Delivered**:
- WCAG compliance assessment
- Accessibility issue prioritization
- Implementation guidelines
- User experience impact analysis

---

## Account Manager

### Primary Use Cases

#### 1. Client Presentation Material
**When to use**: Client meetings, proposal development, campaign reporting
**Squad**: All squads (integrated approach)
**Workflow**:
```bash
# Comprehensive client analysis
python workflows/run_website_strategy.py --primary_url "client-site.com" --presentation_mode
python workflows/run_site_audit.py --url "client-site.com" --report_type "executive_summary"
```

**Value Delivered**:
- Executive-ready reports
- Visual performance summaries
- Competitive positioning insights
- ROI projections

#### 2. Opportunity Identification
**When to use**: Account growth planning, upselling preparation
**Squad**: StrategyNexus + SiteSpect
**Workflow**:
```bash
python workflows/run_website_strategy.py --analysis_type "opportunity_assessment" --client_goals "growth_targets.json"
```

**Value Delivered**:
- Growth opportunity identification
- Service expansion recommendations
- Competitive gap analysis
- Implementation roadmaps

---

## Agency Owner

### Primary Use Cases

#### 1. Service Standardization
**When to use**: Creating repeatable service offerings, training new team members
**Squad**: All squads (template creation)
**Workflow**:
```bash
python workflows/create_service_template.py --service_type "website_audit" --client_tier "enterprise"
```

**Value Delivered**:
- Standardized service deliverables
- Quality assurance frameworks
- Training materials
- Scalable processes

#### 2. Operational Efficiency Analysis
**When to use**: Process optimization, resource allocation planning
**Squad**: System analytics
**Workflow**:
```bash
python monitor_workflows.py --analysis_type "efficiency_metrics" --time_period "monthly"
```

**Value Delivered**:
- Process efficiency metrics
- Resource utilization analysis
- Quality consistency tracking
- ROI measurement

---

## Use Cases by Industry

### E-commerce
- **Primary Focus**: SiteSpect for performance + ContentForge for product content
- **Key Workflows**: Performance optimization, product page audits, seasonal content planning
- **Success Metrics**: Conversion rate improvement, page speed optimization

### SaaS/Technology  
- **Primary Focus**: StrategyNexus for positioning + ContentForge for thought leadership
- **Key Workflows**: Competitive analysis, technical content creation, lead generation content
- **Success Metrics**: Lead quality improvement, market share analysis

### Professional Services
- **Primary Focus**: ContentForge for expertise demonstration + SiteSpect for credibility
- **Key Workflows**: Authority content creation, website credibility audits, local SEO optimization
- **Success Metrics**: Brand authority building, local search visibility

### Manufacturing/Industrial
- **Primary Focus**: SiteSpect for technical performance + StrategyNexus for market positioning  
- **Key Workflows**: Technical site audits, B2B content strategy, competitive positioning
- **Success Metrics**: Lead generation improvement, technical authority establishment

---

## Getting Started by Role

**First-Time Users**: Start with your primary use case above
**Experienced Users**: Combine workflows for comprehensive campaigns
**Power Users**: Customize agent prompts for industry-specific analysis

**Next Steps**: Review detailed workflow documentation in `/workflows/` folder