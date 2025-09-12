# SiteSpect Squad: Website Audit Specialists

## Squad Overview

The SiteSpect Squad automates comprehensive website audits through coordinated AI agents, delivering technical analysis in ~20 seconds that traditionally requires hours of manual work.

**Primary Goal**: Complete website technical, performance, and UX analysis
**Coordination Model**: Parallel execution with synthesis reporting
**Average Execution Time**: 19.25 seconds
**Success Rate**: 95%+

---

## Agent Roster

### @sitespect_orchestrator
**Role**: Central coordinator for all website audit activities

**Responsibilities**:
- Coordinates parallel execution of specialist agents
- Validates URL inputs and accessibility
- Synthesizes specialist reports into unified audit
- Manages error handling and quality assurance
- Generates executive summary and recommendations

**Tools Used**:
- `validate_url()` - URL accessibility verification
- `coordinate_parallel_agents()` - Multi-agent coordination
- `synthesize_reports()` - Report aggregation
- `generate_executive_summary()` - High-level summary creation
- `prioritize_recommendations()` - Issue prioritization

**Input Requirements**:
- Target URL (required)
- Audit scope (optional: full, technical, performance, accessibility)
- Priority level (optional: normal, urgent, critical)

**Output Format**:
- Executive summary with key findings
- Prioritized recommendation list
- Individual specialist reports
- Implementation timeline

---

### @technical_seo_analyst
**Role**: Technical SEO analysis and optimization recommendations

**Core Capabilities**:
- Meta tag analysis and optimization suggestions
- URL structure evaluation
- Internal linking assessment
- Schema markup validation
- Crawlability and indexability analysis
- Core Web Vitals technical factors

**Tools Used**:
- `analyze_meta_tags()` - Meta description, title tag analysis
- `evaluate_url_structure()` - URL SEO assessment
- `assess_internal_linking()` - Link architecture analysis
- `validate_schema_markup()` - Structured data verification
- `check_robots_txt()` - Crawling directive analysis
- `analyze_site_architecture()` - Information architecture assessment

**Specialized Focus Areas**:
- **On-Page SEO**: Title tags, meta descriptions, header structure
- **Technical Structure**: URL optimization, canonical tags, redirects
- **Crawling**: Robots.txt, sitemap.xml, internal linking
- **Schema**: Structured data implementation and validation

**Typical Findings**:
- Missing or duplicate meta descriptions
- Suboptimal URL structures
- Internal linking opportunities
- Schema markup gaps
- Crawling inefficiencies

---

### @performance_tester
**Role**: Website speed and performance analysis

**Core Capabilities**:
- Page load time measurement
- Core Web Vitals assessment
- Resource optimization analysis
- Mobile performance evaluation
- Server response time analysis
- Caching effectiveness review

**Tools Used**:
- `measure_page_load_time()` - Speed measurement
- `analyze_core_web_vitals()` - CWV assessment
- `evaluate_resource_loading()` - Asset optimization analysis
- `assess_mobile_performance()` - Mobile-specific testing
- `check_server_response()` - Backend performance analysis
- `analyze_caching_strategy()` - Cache configuration review

**Performance Metrics Tracked**:
- **Load Times**: First Contentful Paint, Largest Contentful Paint
- **Interactivity**: First Input Delay, Cumulative Layout Shift
- **Resource Metrics**: Total page size, number of requests
- **Mobile Metrics**: Mobile-specific performance scores

**Optimization Recommendations**:
- Image compression and format optimization
- JavaScript and CSS minification
- Caching strategy improvements
- CDN implementation suggestions
- Server configuration optimizations

---

### @accessibility_checker
**Role**: Website accessibility compliance and user experience validation

**Core Capabilities**:
- WCAG compliance assessment
- Keyboard navigation testing
- Screen reader compatibility analysis
- Color contrast validation
- Alternative text assessment
- Form accessibility evaluation

**Tools Used**:
- `run_wcag_audit()` - WCAG 2.1 compliance check
- `test_keyboard_navigation()` - Keyboard accessibility testing
- `analyze_color_contrast()` - Color accessibility assessment
- `validate_alt_text()` - Image accessibility verification
- `assess_form_accessibility()` - Form usability analysis
- `check_aria_implementation()` - ARIA attribute validation

**Compliance Standards**:
- **WCAG 2.1 Level AA**: Primary compliance target
- **Section 508**: Government accessibility standards
- **ADA Compliance**: Americans with Disabilities Act requirements

**Common Issues Identified**:
- Missing alternative text for images
- Insufficient color contrast ratios
- Keyboard navigation barriers
- Missing or incorrect ARIA labels
- Form accessibility problems

---

### @ux_flow_validator
**Role**: User experience and conversion optimization analysis

**Core Capabilities**:
- User journey mapping
- Conversion funnel analysis
- Mobile user experience assessment
- Navigation structure evaluation
- Call-to-action effectiveness review
- User interface consistency analysis

**Tools Used**:
- `map_user_journeys()` - User path analysis
- `analyze_conversion_funnels()` - Conversion optimization assessment
- `evaluate_mobile_ux()` - Mobile experience validation
- `assess_navigation_structure()` - Site navigation analysis
- `review_cta_placement()` - Call-to-action optimization
- `check_ui_consistency()` - Interface consistency validation

**UX Analysis Areas**:
- **Navigation**: Menu structure, breadcrumbs, search functionality
- **Content Layout**: Information hierarchy, readability, visual design
- **Conversion Elements**: Forms, CTAs, checkout processes
- **Mobile Experience**: Responsive design, touch targets, mobile-specific features

**Improvement Recommendations**:
- Navigation simplification suggestions
- Content layout optimizations
- Conversion rate improvement opportunities
- Mobile experience enhancements

---

## Workflow Coordination

### Parallel Execution Phase
1. **@sitespect_orchestrator** validates input and initiates parallel analysis
2. All specialist agents execute simultaneously:
   - @technical_seo_analyst performs SEO analysis
   - @performance_tester measures performance metrics
   - @accessibility_checker runs compliance audit
   - @ux_flow_validator evaluates user experience
3. Individual reports generated in JSON format

### Synthesis Phase
4. **@sitespect_orchestrator** aggregates specialist findings
5. Cross-analysis performed to identify interconnected issues
6. Priority matrix created based on impact and implementation difficulty
7. Executive summary generated with actionable recommendations

### Quality Assurance
8. Validation checks ensure all areas covered
9. Recommendation feasibility assessment
10. Final report formatting and delivery

---

## Integration Points

### Input Sources
- **Direct URL**: Single website audit
- **Batch Processing**: Multiple URL analysis
- **Staging Environment**: Pre-launch validation
- **Comparative Analysis**: Before/after comparisons

### Output Integrations
- **ContentForge Integration**: Technical findings inform content strategy
- **StrategyNexus Integration**: Performance data supports strategic analysis
- **Reporting Systems**: Automated report generation and delivery
- **Project Management**: Issue tracking and implementation monitoring

### Trigger Mechanisms
- **Manual Execution**: Script-based audit initiation
- **Automated Triggers**: GitHub Actions, webhook integration
- **Scheduled Audits**: Regular monitoring and reporting
- **Alert-Based**: Performance threshold monitoring

---

## Customization Options

### Focus Areas
- **Technical SEO Only**: SEO-focused analysis
- **Performance Only**: Speed and optimization focus
- **Accessibility Only**: Compliance-focused audit
- **Full Spectrum**: Comprehensive analysis (default)

### Reporting Levels
- **Executive Summary**: High-level findings and recommendations
- **Technical Detail**: Implementation-specific guidance
- **Comparative Analysis**: Historical or competitive comparison
- **Custom Format**: Client-specific reporting requirements

### Integration Settings
- **API Endpoints**: Custom webhook configurations
- **Notification Settings**: Alert and reporting preferences
- **Data Retention**: Historical analysis storage options
- **Access Controls**: Team-based permission management

---

## Performance Metrics

**Speed**: 19.25 second average execution (95% faster than manual)
**Accuracy**: 95%+ issue identification rate
**Coverage**: 100% of major audit areas addressed
**Reliability**: 99.2% uptime with error handling

**Business Impact**:
- 8+ hours of manual work → 20 seconds automated
- Consistent audit quality across all analyses  
- Scalable to unlimited concurrent audits
- Integration-ready for operational workflows