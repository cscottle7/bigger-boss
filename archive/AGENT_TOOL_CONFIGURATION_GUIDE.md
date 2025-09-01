# Agent Tool Configuration Guide

## Overview
This guide provides the exact tool selections for each agent in the Autonomous Marketing System. Use this checklist when manually configuring agents through the Claude Code UI.

---

## Core Orchestrator Agents

### sitespect_orchestrator
**Purpose**: Coordinates comprehensive website audits through specialist agents

**Required Tools:**
```
☑ Task                              # CRITICAL - calls other agents
☑ Bash                              # System commands
☑ Glob                              # File pattern matching
☑ Grep                              # Search files
☑ Read                              # Read files
☑ Edit                              # Edit files
☑ MultiEdit                         # Multiple edits
☑ Write                             # Create files
☑ WebFetch                          # Basic HTTP requests
☑ TodoWrite                         # Task management
☑ WebSearch                         # Search web
☑ browser_navigate (playwright)     # Navigate websites
☑ browser_evaluate (playwright)     # Execute JavaScript
☑ browser_take_screenshot (playwright)  # Visual documentation
☑ browser_network_requests (playwright) # Network analysis
☑ browser_wait_for (playwright)     # Wait for elements
☑ browser_snapshot (playwright)     # Page accessibility snapshot
☐ NotebookEdit                      # Not needed
☐ BashOutput                        # Not needed
☐ KillBash                          # Not needed
☐ Other browser tools               # Only if specifically needed
```

### master_orchestrator
**Purpose**: High-level business analysis coordination

**Required Tools:**
```
☑ Task                              # CRITICAL - calls other agents
☑ Read                              # Read files
☑ Write                             # Create files
☑ Edit                              # Edit files
☑ Glob                              # File searching
☑ TodoWrite                         # Task management
☑ WebSearch                         # Research
☐ Browser tools                     # Delegates to specialists
☐ Bash                              # Delegates to specialists
```

### strategy_orchestrator
**Purpose**: Market analysis and strategic planning coordination

**Required Tools:**
```
☑ Task                              # CRITICAL - calls other agents
☑ Read                              # Read files
☑ Write                             # Create files
☑ Edit                              # Edit files
☑ Glob                              # File searching
☑ TodoWrite                         # Task management
☑ WebSearch                         # Market research
☐ Browser tools                     # Delegates to specialists
☐ Bash                              # Not needed
```

### content_workflow_orchestrator
**Purpose**: Content strategy and editorial planning coordination

**Required Tools:**
```
☑ Task                              # CRITICAL - calls other agents
☑ Read                              # Read files
☑ Write                             # Create files
☑ Edit                              # Edit files
☑ MultiEdit                         # Multiple edits
☑ Glob                              # File searching
☑ TodoWrite                         # Task management
☑ WebSearch                         # Content research
☐ Browser tools                     # Delegates to specialists
☐ Bash                              # Not needed
```

---

## Technical Specialist Agents

### technical_seo_analyst
**Purpose**: Comprehensive technical SEO analysis using browser automation

**Required Tools:**
```
☑ browser_navigate (playwright)     # CRITICAL - navigate to websites
☑ browser_evaluate (playwright)     # CRITICAL - extract meta tags, HTML
☑ browser_take_screenshot (playwright)  # CRITICAL - visual documentation
☑ browser_network_requests (playwright) # Network analysis
☑ browser_wait_for (playwright)     # Wait for page load
☑ browser_snapshot (playwright)     # Page structure analysis
☑ browser_console_messages (playwright) # Debug info
☑ Write                             # Create reports
☑ Read                              # Read existing files
☑ Edit                              # Update reports
☑ Glob                              # Search files
☑ WebSearch                         # SEO research
☐ Task                              # Specialist doesn't call others
☐ WebFetch                          # NEVER - use browser tools instead
☐ Bash                              # Not needed for SEO analysis
```

### performance_tester
**Purpose**: Website performance and Core Web Vitals analysis

**Required Tools:**
```
☑ browser_navigate (playwright)     # Navigate to test site
☑ browser_evaluate (playwright)     # Performance metrics
☑ browser_take_screenshot (playwright)  # Visual documentation
☑ browser_network_requests (playwright) # Network performance
☑ browser_wait_for (playwright)     # Performance timing
☑ Write                             # Performance reports
☑ Read                              # Read existing files
☑ WebSearch                         # Performance research
☐ Task                              # Specialist doesn't call others
☐ WebFetch                          # Use browser tools instead
☐ Bash                              # Not needed
```

### accessibility_checker
**Purpose**: WCAG compliance and accessibility analysis

**Required Tools:**
```
☑ browser_navigate (playwright)     # Navigate to website
☑ browser_evaluate (playwright)     # Accessibility checks
☑ browser_snapshot (playwright)     # CRITICAL - accessibility tree
☑ browser_take_screenshot (playwright)  # Visual documentation
☑ browser_click (playwright)        # Test interactions
☑ browser_press_key (playwright)    # Keyboard navigation
☑ Write                             # Accessibility reports
☑ Read                              # Read existing files
☑ WebSearch                         # WCAG guidelines
☐ Task                              # Specialist doesn't call others
☐ WebFetch                          # Use browser tools instead
☐ Bash                              # Not needed
```

### ux_flow_validator
**Purpose**: User experience and conversion optimization analysis

**Required Tools:**
```
☑ browser_navigate (playwright)     # Navigate website
☑ browser_evaluate (playwright)     # UX metrics
☑ browser_click (playwright)        # Test user flows
☑ browser_take_screenshot (playwright)  # Visual UX documentation
☑ browser_snapshot (playwright)     # Page structure
☑ browser_fill_form (playwright)    # Test forms
☑ browser_hover (playwright)        # Test interactions
☑ Write                             # UX reports
☑ Read                              # Read existing files
☑ WebSearch                         # UX research
☐ Task                              # Specialist doesn't call others
☐ WebFetch                          # Use browser tools instead
☐ Bash                              # Not needed
```

---

## Research and Intelligence Agents

### competitive_intelligence_searcher
**Purpose**: Multi-platform competitive research using Scrapy and browser automation

**Required Tools:**
```
☑ browser_navigate (playwright)     # Navigate competitor sites
☑ browser_evaluate (playwright)     # Extract competitor data
☑ browser_take_screenshot (playwright)  # Visual documentation
☑ browser_network_requests (playwright) # Competitor tech analysis
☑ Bash                              # CRITICAL - run Scrapy commands
☑ Write                             # Competitive reports
☑ Read                              # Read existing data
☑ Edit                              # Update reports
☑ Glob                              # Search files
☑ WebSearch                         # Competitive research
☑ WebFetch                          # Basic HTTP for APIs
☐ Task                              # Specialist doesn't call others
☐ TodoWrite                         # Not needed for research
```

### technical_research_specialist
**Purpose**: Advanced technical documentation and implementation research

**Required Tools:**
```
☑ browser_navigate (playwright)     # Navigate technical sites
☑ browser_evaluate (playwright)     # Extract technical data
☑ browser_take_screenshot (playwright)  # Documentation
☑ WebSearch                         # Technical research
☑ WebFetch                          # API documentation
☑ Write                             # Technical reports
☑ Read                              # Read documentation
☑ Edit                              # Update reports
☑ Glob                              # Search files
☑ Bash                              # Technical commands if needed
☐ Task                              # Specialist doesn't call others
```

### brand_sentiment_researcher
**Purpose**: Social media monitoring and brand sentiment analysis

**Required Tools:**
```
☑ WebSearch                         # CRITICAL - social media research
☑ browser_navigate (playwright)     # Navigate social platforms
☑ browser_evaluate (playwright)     # Extract social data
☑ browser_take_screenshot (playwright)  # Evidence documentation
☑ Write                             # Sentiment reports
☑ Read                              # Read existing data
☑ Edit                              # Update reports
☑ WebFetch                          # Social APIs
☐ Task                              # Specialist doesn't call others
☐ Bash                              # Not needed for sentiment
```

---

## Content and Strategy Agents

### keyword_researcher
**Required Tools:**
```
☑ WebSearch ☑ browser_navigate ☑ browser_evaluate ☑ Write ☑ Read ☑ Edit ☑ Glob
☐ Task ☐ Bash
```

### content_strategist
**Required Tools:**
```
☑ Write ☑ Read ☑ Edit ☑ MultiEdit ☑ WebSearch ☑ Glob ☑ TodoWrite
☐ Task ☐ Browser tools ☐ Bash
```

### content_generator
**Required Tools:**
```
☑ Write ☑ Read ☑ Edit ☑ MultiEdit ☑ WebSearch ☑ Glob
☐ Task ☐ Browser tools ☐ Bash
```

### content_director
**Required Tools:**
```
☑ Task ☑ Write ☑ Read ☑ Edit ☑ MultiEdit ☑ Glob ☑ TodoWrite
☐ Browser tools ☐ Bash
```

### content_optimizer
**Required Tools:**
```
☑ browser_navigate ☑ browser_evaluate ☑ browser_take_screenshot ☑ Write ☑ Read ☑ Edit ☑ WebSearch
☐ Task ☐ Bash
```

### content_auditor
**Required Tools:**
```
☑ browser_navigate ☑ browser_evaluate ☑ browser_take_screenshot ☑ Write ☑ Read ☑ Edit ☑ Glob ☑ WebSearch
☐ Task ☐ Bash
```

### enhanced_content_auditor
**Required Tools:**
```
☑ browser_navigate ☑ browser_evaluate ☑ browser_take_screenshot ☑ Write ☑ Read ☑ Edit ☑ Glob ☑ WebSearch
☐ Task ☐ Bash
```

### content_reviewer
**Required Tools:**
```
☑ Read ☑ Edit ☑ MultiEdit ☑ Write ☑ Glob ☑ WebSearch
☐ Task ☐ Browser tools ☐ Bash
```

### content_refiner
**Required Tools:**
```
☑ Read ☑ Edit ☑ MultiEdit ☑ Write ☑ WebSearch
☐ Task ☐ Browser tools ☐ Bash
```

### content_finaliser
**Required Tools:**
```
☑ Read ☑ Edit ☑ MultiEdit ☑ Write ☑ Glob
☐ Task ☐ Browser tools ☐ Bash
```

### content_performance_analyst
**Required Tools:**
```
☑ browser_navigate ☑ browser_evaluate ☑ browser_network_requests ☑ Write ☑ Read ☑ Edit ☑ WebSearch
☐ Task ☐ Bash
```

### content_refresh_orchestrator
**Required Tools:**
```
☑ Task ☑ Write ☑ Read ☑ Edit ☑ Glob ☑ TodoWrite ☑ WebSearch
☐ Browser tools ☐ Bash
```

### blog_ideation_specialist
**Required Tools:**
```
☑ Write ☑ Read ☑ Edit ☑ WebSearch ☑ Glob
☐ Task ☐ Browser tools ☐ Bash
```

### page_content_brief_agent
**Required Tools:**
```
☑ Write ☑ Read ☑ Edit ☑ MultiEdit ☑ WebSearch ☑ Glob
☐ Task ☐ Browser tools ☐ Bash
```

---

## Quality Control Agents

### quality_gate_orchestrator
**Required Tools:**
```
☑ Task ☑ Write ☑ Read ☑ Edit ☑ TodoWrite ☑ Glob
☐ Browser tools ☐ Bash
```

### universal_quality_gate_orchestrator
**Required Tools:**
```
☑ Task ☑ Write ☑ Read ☑ Edit ☑ MultiEdit ☑ TodoWrite ☑ Glob
☐ Browser tools ☐ Bash
```

---

## SEO and Analysis Agents

### seo_strategist
**Required Tools:**
```
☑ Read ☑ Write ☑ Edit ☑ WebSearch ☑ Glob ☑ browser_navigate ☑ browser_evaluate
☐ Task ☐ Bash
```

### advanced_seo_meta_extractor
**Required Tools:**
```
☑ browser_navigate ☑ browser_evaluate ☑ browser_take_screenshot ☑ Write ☑ Read ☑ Edit ☑ WebSearch
☐ Task ☐ Bash
```

### seo_enhanced_auditor
**Required Tools:**
```
☑ browser_navigate ☑ browser_evaluate ☑ browser_take_screenshot ☑ browser_network_requests ☑ Write ☑ Read ☑ Edit ☑ WebSearch ☑ Glob
☐ Task ☐ Bash
```

---

## Brand and Market Research Agents

### brand_analyst
**Required Tools:**
```
☑ WebSearch ☑ browser_navigate ☑ browser_evaluate ☑ browser_take_screenshot ☑ Write ☑ Read ☑ Edit ☑ Glob
☐ Task ☐ Bash
```

### brand_strategy_researcher
**Required Tools:**
```
☑ WebSearch ☑ browser_navigate ☑ browser_evaluate ☑ Write ☑ Read ☑ Edit ☑ Glob
☐ Task ☐ Bash
```

### competitor_analyzer
**Required Tools:**
```
☑ WebSearch ☑ browser_navigate ☑ browser_evaluate ☑ browser_take_screenshot ☑ Write ☑ Read ☑ Edit ☑ Glob ☑ Bash
☐ Task
```

### audience_intent_researcher
**Required Tools:**
```
☑ WebSearch ☑ browser_navigate ☑ browser_evaluate ☑ Write ☑ Read ☑ Edit ☑ Glob
☐ Task ☐ Bash
```

---

## AI and Enhancement Agents

### ai_specialist_agent
**Required Tools:**
```
☑ browser_navigate ☑ browser_evaluate ☑ browser_take_screenshot ☑ Write ☑ Read ☑ Edit ☑ WebSearch ☑ Glob
☐ Task ☐ Bash
```

### ai_enhanced_auditor
**Required Tools:**
```
☑ browser_navigate ☑ browser_evaluate ☑ browser_take_screenshot ☑ Write ☑ Read ☑ Edit ☑ WebSearch ☑ Glob
☐ Task ☐ Bash
```

### ai_readiness_enhanced_auditor
**Required Tools:**
```
☑ browser_navigate ☑ browser_evaluate ☑ browser_take_screenshot ☑ Write ☑ Read ☑ Edit ☑ WebSearch ☑ Glob
☐ Task ☐ Bash
```

### ai_refiner
**Required Tools:**
```
☑ Read ☑ Edit ☑ MultiEdit ☑ Write ☑ WebSearch
☐ Task ☐ Browser tools ☐ Bash
```

### ai_readiness_refiner
**Required Tools:**
```
☑ Read ☑ Edit ☑ MultiEdit ☑ Write ☑ WebSearch
☐ Task ☐ Browser tools ☐ Bash
```

### ai_finaliser
**Required Tools:**
```
☑ Read ☑ Edit ☑ MultiEdit ☑ Write ☑ Glob
☐ Task ☐ Browser tools ☐ Bash
```

### ai_readiness_finaliser
**Required Tools:**
```
☑ Read ☑ Edit ☑ MultiEdit ☑ Write ☑ Glob
☐ Task ☐ Browser tools ☐ Bash
```

---

## Technical Enhancement Agents

### technical_enhanced_auditor
**Required Tools:**
```
☑ browser_navigate ☑ browser_evaluate ☑ browser_take_screenshot ☑ browser_network_requests ☑ Write ☑ Read ☑ Edit ☑ WebSearch ☑ Glob
☐ Task ☐ Bash
```

---

## User Experience Agents

### user_journey_mapper
**Required Tools:**
```
☑ browser_navigate ☑ browser_click ☑ browser_take_screenshot ☑ browser_fill_form ☑ Write ☑ Read ☑ Edit ☑ WebSearch
☐ Task ☐ Bash
```

---

## Utility and Support Agents

### text_sitemap_generator
**Required Tools:**
```
☑ browser_navigate ☑ browser_evaluate ☑ Write ☑ Read ☑ Edit ☑ Glob ☑ Bash
☐ Task
```

### universal_prompt_creator
**Required Tools:**
```
☑ Write ☑ Read ☑ Edit ☑ MultiEdit ☑ Glob ☑ WebSearch
☐ Task ☐ Browser tools ☐ Bash
```

---

## Google Drive Integration Agents

### google_drive_manager
**Required Tools:**
```
☑ Write ☑ Read ☑ Edit ☑ Bash ☑ Glob
☐ Task ☐ Browser tools
```

### google_drive_publisher
**Required Tools:**
```
☑ Write ☑ Read ☑ Bash ☑ Glob
☐ Task ☐ Browser tools
```

### google_drive_assistant
**Required Tools:**
```
☑ Write ☑ Read ☑ Edit ☑ Bash ☑ Glob
☐ Task ☐ Browser tools
```

---

## Tool Assignment Priority

### CRITICAL Tools (Must Have)
- **Task**: For all orchestrator agents
- **browser_navigate**: For all technical analysis agents
- **browser_evaluate**: For all technical analysis agents
- **Write**: For all agents creating reports
- **Read**: For all agents reading existing data

### HIGH Priority Tools
- **browser_take_screenshot**: For documentation
- **WebSearch**: For research agents
- **Edit**: For agents updating existing content
- **Glob**: For file searching

### MEDIUM Priority Tools
- **MultiEdit**: For bulk operations
- **browser_snapshot**: For accessibility analysis
- **Bash**: For competitive intelligence (Scrapy)
- **TodoWrite**: For task management

### LOW Priority Tools
- **WebFetch**: Only when browser tools insufficient
- **NotebookEdit**: Rarely needed
- **BashOutput/KillBash**: Only for background processes

---

## Configuration Verification

After configuring each agent, verify:

1. **Orchestrators have Task tool** - Critical for calling specialists
2. **Technical agents have browser tools** - No WebFetch for website analysis
3. **Research agents have WebSearch** - For data gathering
4. **All agents have Write/Read** - For report generation
5. **Competitive agents have Bash** - For Scrapy integration

## Common Mistakes to Avoid

❌ **Don't give Task tool to specialist agents** - Only orchestrators coordinate
❌ **Don't use WebFetch for website analysis** - Always use browser tools
❌ **Don't forget browser_navigate** - Required for all website analysis
❌ **Don't skip Write tool** - All agents need to create reports
❌ **Don't give browser tools to content agents** - They work with text, not websites

✅ **Do give comprehensive tools to orchestrators** - They coordinate everything
✅ **Do give browser tools to all technical agents** - For accurate analysis
✅ **Do give WebSearch to research agents** - For data gathering
✅ **Do verify tool assignments match agent purpose** - Each tool should have a reason