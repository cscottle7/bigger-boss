# Agent Tool Mappings: Specific Tool Assignments for Actual Data Collection

## Overview

This document provides specific tool assignments for each agent to eliminate estimated data and ensure actual measurements. Each mapping includes the required tools, their specific purpose, and expected outputs.

---

## SiteSpect Squad: Website Analysis Agents

### technical_seo_analyst
**Mission**: Comprehensive technical SEO analysis using actual website data

**Critical Tool Requirements**:
```
✅ REQUIRED TOOLS:
├── browser_navigate (Playwright MCP)     # Navigate to all site pages
├── browser_evaluate (Playwright MCP)     # Extract meta tags, headings, structure
├── browser_take_screenshot (Playwright)  # Document visual issues
├── browser_network_requests (Playwright) # Analyze load times, resources
├── Write                                 # Create technical reports
├── Read                                  # Access existing site data
├── Edit                                  # Update analysis reports
├── WebSearch                            # Research technical SEO best practices
└── Glob                                 # Search for existing analyses

❌ FORBIDDEN TOOLS:
├── WebFetch                             # Use browser tools for website analysis
├── Task                                 # Specialist agent - doesn't coordinate others
└── Bash                                 # Not required for SEO analysis
```

**Implementation Focus**:
- **Full Site Crawling**: Use Playwright to navigate entire site structure, not just homepage
- **Real Meta Extraction**: Browser evaluation to extract actual meta tags, titles, descriptions
- **Actual Performance Data**: Network request monitoring for real load times
- **Visual Documentation**: Screenshots of actual pages for client reports

**Output Transformation**:
- **Before**: "Estimated 15-20 pages with assumed meta tag issues"
- **After**: "Analyzed 47 pages, found 12 missing meta descriptions on [specific URLs]"

### performance_tester
**Mission**: Actual website performance measurement using GTMetrix API and browser automation

**Critical Tool Requirements**:
```
✅ REQUIRED TOOLS:
├── browser_navigate (Playwright MCP)     # Navigate to test pages
├── browser_evaluate (Playwright MCP)     # Performance metrics collection
├── browser_network_requests (Playwright) # Network performance analysis  
├── browser_take_screenshot (Playwright)  # Visual performance documentation
├── WebFetch                             # GTMetrix API integration
├── Write                                # Performance reports
├── Read                                 # Historical performance data
├── WebSearch                            # Performance optimization research
└── Bash (if needed)                     # GTMetrix API commands

❌ FORBIDDEN TOOLS:
├── Task                                 # Specialist agent
└── [No other restrictions]
```

**GTMetrix Integration Protocol**:
```
1. Use WebFetch to trigger GTMetrix API test: 
   POST https://gtmetrix.com/api/2.0/tests
   
2. Monitor test completion:
   GET https://gtmetrix.com/api/2.0/tests/{test_id}
   
3. Retrieve actual performance data:
   - Real PageSpeed score (not estimated 75-85)
   - Actual Core Web Vitals measurements
   - Genuine performance recommendations
   - Historical performance trends
```

**Output Transformation**:
- **Before**: "Estimated PageSpeed score: 78, estimated load time: 2.3s"
- **After**: "GTMetrix measured PageSpeed score: 82, actual load time: 1.87s"

### accessibility_checker
**Mission**: WCAG compliance assessment using actual accessibility scanning

**Critical Tool Requirements**:
```
✅ REQUIRED TOOLS:
├── browser_navigate (Playwright MCP)     # Navigate to pages for testing
├── browser_evaluate (Playwright MCP)     # Accessibility tree analysis
├── browser_snapshot (Playwright)        # CRITICAL: Accessibility tree capture
├── browser_take_screenshot (Playwright) # Document accessibility issues
├── browser_click (Playwright)           # Test keyboard navigation
├── browser_press_key (Playwright)       # Keyboard accessibility testing
├── Write                                # Accessibility reports
├── Read                                 # Existing accessibility data
├── WebSearch                            # WCAG guidelines research
└── Glob                                # Search for previous assessments

❌ FORBIDDEN TOOLS:
├── Task                                 # Specialist agent
├── WebFetch                             # Use browser tools for site analysis
└── Bash                                 # Not needed for accessibility
```

**Accessibility Testing Protocol**:
```
1. Use browser_snapshot to get actual accessibility tree
2. Use browser_evaluate to run accessibility audit scripts:
   - Check for actual missing alt tags
   - Test real color contrast ratios
   - Identify actual keyboard navigation issues
3. Use browser_click and browser_press_key for interaction testing
4. Document real accessibility barriers with screenshots
```

**Output Transformation**:
- **Before**: "Estimated 5-10 accessibility issues"
- **After**: "Found 7 accessibility violations: 3 missing alt tags on images, 2 insufficient color contrast areas (specific elements identified)"

---

## ContentForge Squad: Content Strategy and Creation Agents

### competitive_intelligence_searcher
**Mission**: Deep competitive analysis using Scrapy and browser automation

**Critical Tool Requirements**:
```
✅ REQUIRED TOOLS:
├── browser_navigate (Playwright MCP)     # Navigate competitor websites
├── browser_evaluate (Playwright MCP)     # Extract competitor content strategies
├── browser_take_screenshot (Playwright) # Document competitor approaches
├── Bash                                 # CRITICAL: Scrapy command execution
├── WebSearch                            # Competitive research
├── WebFetch                             # API integrations for data
├── Write                                # Competitive intelligence reports
├── Read                                 # Existing competitive data
├── Edit                                 # Update competitive analyses
└── Glob                                 # Search competitive research files

❌ FORBIDDEN TOOLS:
├── Task                                 # Specialist agent
└── [No other restrictions]
```

**Scrapy Integration Protocol**:
```bash
# Use Bash tool to execute Scrapy commands:

# 1. Competitor content analysis
scrapy crawl competitor_spider -a domain=competitor.com -a depth=3

# 2. Content strategy extraction
scrapy crawl content_strategy_spider -a urls=competitor_urls.txt

# 3. Social media monitoring
scrapy crawl social_spider -a platforms=linkedin,twitter -a brand=competitor
```

**Output Transformation**:
- **Before**: "Estimated competitor posts 2-3 times per week"
- **After**: "Scrapy analysis shows competitor published 47 blog posts in last 90 days, avg 5.2 per week"

### keyword_researcher
**Mission**: Actual keyword research using SERPAPI and search analysis

**Critical Tool Requirements**:
```
✅ REQUIRED TOOLS:
├── WebSearch                            # Primary keyword research
├── WebFetch                            # SERPAPI integration
├── browser_navigate (Playwright MCP)   # Search result page analysis
├── browser_evaluate (Playwright MCP)   # Extract SERP features
├── Write                               # Keyword research reports
├── Read                                # Existing keyword data
├── Edit                                # Update keyword lists
└── Glob                                # Search existing research

❌ FORBIDDEN TOOLS:
├── Task                                # Specialist agent
├── Bash                                # Not required for keyword research
└── [No browser screenshot needed]
```

**SERPAPI Integration Protocol**:
```javascript
// Use WebFetch for actual search data:
fetch('https://serpapi.com/search', {
  params: {
    q: 'target keyword',
    location: 'Australia',
    api_key: process.env.SERPAPI_KEY
  }
})

// Extract real search volumes, competition, related keywords
// Analyze actual SERP features, competitors ranking
```

**Output Transformation**:
- **Before**: "Estimated search volume: 2,000/month"
- **After**: "SERPAPI data shows actual search volume: 1,847/month, 23 related keywords identified"

### content_performance_analyst
**Mission**: Actual content performance tracking across channels

**Critical Tool Requirements**:
```
✅ REQUIRED TOOLS:
├── WebSearch                            # Content performance research
├── browser_navigate (Playwright MCP)   # Analyze content on various platforms
├── browser_evaluate (Playwright MCP)   # Extract engagement metrics
├── WebFetch                            # API integrations for analytics
├── Bash                                # Scrapy for social media data
├── Write                               # Performance reports
├── Read                                # Historical performance data
├── Edit                                # Update performance analyses
└── Glob                                # Search existing reports

❌ FORBIDDEN TOOLS:
├── Task                                # Specialist agent
└── [No other restrictions]
```

**Multi-Platform Performance Analysis**:
```
1. Use WebSearch to find content across platforms
2. Use Playwright to analyze social media engagement
3. Use Scrapy (via Bash) to collect engagement data systematically
4. Use WebFetch for available API data (LinkedIn, Twitter)
```

**Output Transformation**:
- **Before**: "Estimated engagement rate: 3-5%"
- **After**: "Measured engagement across 15 platforms: LinkedIn 4.7%, Twitter 2.3%, blog posts avg 6.1%"

---

## StrategyNexus Squad: Market Intelligence and Strategic Analysis

### brand_sentiment_researcher
**Mission**: Real-time brand sentiment monitoring across all channels

**Critical Tool Requirements**:
```
✅ REQUIRED TOOLS:
├── WebSearch                            # CRITICAL: Social media and review research
├── browser_navigate (Playwright MCP)   # Navigate social platforms, review sites
├── browser_evaluate (Playwright MCP)   # Extract sentiment data and mentions
├── browser_take_screenshot (Playwright) # Document brand mentions
├── WebFetch                            # Social media API integrations
├── Bash                                # Scrapy for comprehensive monitoring
├── Write                               # Sentiment reports
├── Read                                # Historical sentiment data
├── Edit                                # Update sentiment analyses
└── Glob                                # Search existing sentiment research

❌ FORBIDDEN TOOLS:
├── Task                                # Specialist agent
└── [No other restrictions]
```

**Comprehensive Sentiment Protocol**:
```
1. WebSearch: Find all brand mentions across platforms
2. Playwright: Navigate to review sites, social platforms
3. Scrapy (Bash): Systematic collection of mentions and sentiment
4. WebFetch: API data from accessible platforms
5. Aggregate actual sentiment scores, not estimates
```

**Output Transformation**:
- **Before**: "Generally positive brand sentiment"
- **After**: "147 brand mentions analyzed: 73% positive, 18% neutral, 9% negative. Key issues: pricing concerns (12 mentions), excellent service praise (45 mentions)"

### competitor_analyzer
**Mission**: Comprehensive competitive intelligence using full tool suite

**Critical Tool Requirements**:
```
✅ REQUIRED TOOLS:
├── WebSearch                            # Competitive research
├── browser_navigate (Playwright MCP)   # Competitor website analysis
├── browser_evaluate (Playwright MCP)   # Extract competitor strategies
├── browser_take_screenshot (Playwright) # Document competitor approaches
├── WebFetch                            # Competitor API data
├── Bash                                # Scrapy for deep analysis
├── Write                               # Competitive analysis reports
├── Read                                # Existing competitive intelligence
├── Edit                                # Update competitive profiles
└── Glob                                # Search competitive research

❌ FORBIDDEN TOOLS:
├── Task                                # Specialist agent
└── [No other restrictions]
```

**Multi-Tool Competitive Analysis**:
```
1. WebSearch: Identify all competitors and their digital presence
2. Scrapy: Deep crawl of competitor websites, content strategies
3. Playwright: Analyze competitor user experiences, conversion flows
4. WebFetch: Gather competitor performance data where available
5. Create comprehensive competitive intelligence profiles
```

**Output Transformation**:
- **Before**: "Main competitors appear to focus on similar services"
- **After**: "Analyzed 12 direct competitors: CompetitorA has 47% market share, posts 5x weekly, uses 15 unique value propositions we don't address"

---

## Enhanced Orchestrator Agents

### sitespect_orchestrator
**Mission**: Coordinate comprehensive website audits using specialist agents

**Enhanced Tool Requirements**:
```
✅ REQUIRED TOOLS:
├── Task                                # CRITICAL: Coordinate specialist agents
├── browser_navigate (Playwright MCP)  # Direct site navigation when needed
├── browser_evaluate (Playwright MCP)  # Quick assessments
├── browser_take_screenshot (Playwright) # Document overall site status
├── Write                              # Audit coordination reports
├── Read                               # Previous audit data
├── Edit                               # Update audit reports
├── MultiEdit                          # Bulk report updates
├── Glob                               # Find existing audits
├── WebSearch                          # Research audit methodologies
├── WebFetch                           # Direct tool integrations
└── TodoWrite                          # Manage audit task lists

❌ FORBIDDEN TOOLS:
├── Bash                               # Delegate technical tasks to specialists
└── [No other restrictions]
```

**Orchestration Protocol with Actual Data**:
```
1. Use Task tool to call @technical_seo_analyst with specific URLs
2. Use Task tool to call @performance_tester for GTMetrix integration
3. Use Task tool to call @accessibility_checker for WCAG analysis
4. Coordinate all specialist outputs into comprehensive audit
5. Ensure all data is actual measurements, not estimates
```

### master_orchestrator
**Mission**: High-level coordination ensuring all squads use actual data

**Enhanced Tool Requirements**:
```
✅ REQUIRED TOOLS:
├── Task                               # CRITICAL: Coordinate all squads
├── Read                              # Review all squad outputs  
├── Write                             # Master coordination reports
├── Edit                              # Update coordination strategies
├── MultiEdit                         # Bulk updates across squads
├── Glob                              # Search all project data
├── WebSearch                         # High-level market research
├── WebFetch                          # Direct integrations when needed
└── TodoWrite                         # Master project management

❌ FORBIDDEN TOOLS:
├── Browser tools                     # Delegate to specialist squads
├── Bash                              # Delegate technical operations
└── [No other restrictions]
```

**Quality Assurance Protocol**:
```
1. Review all squad outputs for estimated vs. actual data
2. Flag any reports containing estimates or assumptions
3. Coordinate re-analysis with proper tool utilization
4. Ensure comprehensive actual data integration
```

---

## Implementation Validation Checklist

### Phase 1 Validation: Tool Assignment Verification
- [ ] All technical agents have Playwright MCP access
- [ ] Performance agents have GTMetrix API integration
- [ ] Research agents have WebSearch + Scrapy access
- [ ] Orchestrators have Task tool for coordination
- [ ] All agents have Write/Read for reporting

### Phase 2 Validation: Output Quality Verification
- [ ] No "estimated" or "approximately" language in reports
- [ ] All data points have tool source attribution
- [ ] Screenshots and documentation from actual tools
- [ ] Measurable, reproducible results
- [ ] Cross-referencing between multiple tool sources

### Phase 3 Validation: Performance Verification
- [ ] Tool response times within acceptable limits
- [ ] Error handling and fallback procedures working
- [ ] Quality gates preventing estimated data regression
- [ ] Monitoring and alerting for tool failures
- [ ] User satisfaction with actual vs. estimated results

---

## Success Metrics by Agent Type

### Technical Analysis Agents
**Baseline**: Homepage-only analysis with estimated performance
**Target**: Full site analysis with actual measurements
**Measurement**: Pages analyzed, actual performance scores, real accessibility issues found

### Research Intelligence Agents  
**Baseline**: Surface-level competitive analysis with assumptions
**Target**: Deep multi-platform intelligence with verified data
**Measurement**: Data sources utilized, mentions analyzed, competitors profiled

### Orchestration Agents
**Baseline**: Coordination with mixed estimated/actual data
**Target**: Coordination ensuring 100% actual data integration
**Measurement**: Reports with verified data, tool utilization rates, quality scores

This comprehensive mapping ensures every agent transforms from estimated to actual data collection through proper tool integration and utilization.