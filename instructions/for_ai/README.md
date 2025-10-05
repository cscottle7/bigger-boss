# AI/Agent Instructions

**Audience:** AI Agents, Automation Systems, Agent Orchestrators
**Purpose:** Operational instructions for system understanding and autonomous operation
**Last Updated:** 30 September 2025

---

## Quick Start for AI Agents

### Essential Reading (Priority Order)

1. **System Operation Guide** → [SYSTEM_OPERATION_GUIDE.md](SYSTEM_OPERATION_GUIDE.md)
   - Comprehensive overview of system operation
   - Automation workflows and coordination
   - Error handling and recovery protocols

2. **CLAUDE.md** (in root directory)
   - Primary agent configuration
   - Client folder structure standards
   - Mandatory research workflow
   - Quality assurance requirements

3. **Automation System Documentation** → [AUTOMATION_SYSTEM_DOCUMENTATION.md](AUTOMATION_SYSTEM_DOCUMENTATION.md)
   - File system watcher details
   - Workflow orchestrator operation
   - Pre-delivery audit system
   - Document conversion processes

---

## Documentation Index

### System Architecture & Operation

| Document | Purpose | When to Read |
|----------|---------|--------------|
| `SYSTEM_OPERATION_GUIDE.md` | Consolidated operational guide | **Start here** |
| `AUTOMATION_SYSTEM_DOCUMENTATION.md` | Complete automation system details | Understanding automation |
| `BIGGER_BOSS_SYSTEM_DOCUMENTATION.md` | Full system architecture | Deep system understanding |
| `SYSTEM_IMPLEMENTATION_GUIDE.md` | Implementation procedures | System setup and deployment |
| `SYSTEM_RELIABILITY_GUIDE.md` | Error handling and recovery | Troubleshooting and resilience |

### Hook System & Automation

| Document | Purpose | When to Read |
|----------|---------|--------------|
| `HOOK_SYSTEM_OVERVIEW_AND_TESTING.md` | Hook system overview | Understanding triggers |
| `DETAILED_HOOK_FUNCTIONALITY_EXPLAINED.md` | Hook technical details | Deep hook understanding |
| `ADVANCED_HOOK_OPPORTUNITIES.md` | Advanced automation capabilities | Extending automation |

### Specialized Tools & Integrations

| Document | Purpose | When to Read |
|----------|---------|--------------|
| `NATURAL_LANGUAGE_CONVERTER_GUIDE.md` | Document conversion tool | Converting documents |
| `WEBFETCH_BYPASS_SOLUTION.md` | Web fetch workarounds | Accessing web content |
| `CLAUDE_CODE_PERMISSIONS_GUIDE.md` | Permission requirements | Access control issues |

### Quality & Review Protocols

| Document | Purpose | When to Read |
|----------|---------|--------------|
| `reviewer-prompt.md` | Quality review guidelines | Reviewing content |
| `SYSTEM_IMPROVEMENTS_IMPLEMENTATION_GUIDE.md` | System enhancement procedures | Implementing improvements |
| `AUTONOMOUS_ANALYSIS_IMPLEMENTATION_PLAN.md` | Autonomous analysis features | Analysis automation |
| `AUTONOMOUS_ANALYSIS_IMPLEMENTATION_COMPLETE.md` | Analysis implementation details | Analysis implementation |

---

## Key Concepts for AI Agents

### 1. Glenn Routing System
**Purpose:** Intelligent request routing to appropriate specialist agents

- **All requests must route through Glenn first**
- Glenn analyzes intent and selects appropriate orchestrator
- Prevents incorrect agent selection and workflow failures
- Ensures mandatory research phases before content creation

**Reference:** CLAUDE.md (root) - Content Request Routing Protocol

### 2. Mandatory Research Workflow
**Critical:** All content requests MUST complete 4 research phases before content creation

**Phase 1:** Foundation Research (SOP compliance, audience, market, USP, SWOT)
**Phase 2:** Competitive Intelligence (positioning, trends, gaps, landscape)
**Phase 3:** SEO Strategy (keywords, search intent, funnel mapping)
**Phase 4:** Content Planning (briefs, structure, AI optimization, calendar)

**Reference:** CLAUDE.md (root) - Mandatory Research Workflow

### 3. Iterative Feedback Loop System
**Purpose:** Multi-agent quality optimization instead of linear QA

**Agent Sequence:**
1. clarity_conciseness_editor (Threshold: 8/10)
2. cognitive_load_minimizer (Threshold: 7/10)
3. content_critique_specialist (Threshold: 7/10)
4. ai_text_naturalizer (Threshold: 8/10)

**Success Criteria:** Aggregate score ≥8.5/10

**Reference:** CLAUDE.md (root) - Iterative Feedback Loop System

### 4. Client Folder Structure
**Mandatory:** All client work MUST be in standardized structure

```
clients/{client_domain}/
├── README.md
├── PROJECT_OVERVIEW.md
├── strategy/
├── research/
├── content/
├── technical/
└── implementation/
```

**Reference:** CLAUDE.md (root) - File Organization Standards

### 5. British English Compliance
**Mandatory:** 100% British English throughout all content

- Spelling: optimise, realise, colour, centre, analyse
- Terminology: mobile, lift, CV, postcode
- Australian context: AUD pricing, local market focus
- Date format: DD/MM/YYYY

**Reference:** CLAUDE.md (root) - British English Compliance

### 6. Orchestrator Roles
**Understanding correct delegation:**

- **master_orchestrator**: Content-related tasks (strategy, content, SEO)
- **workflow-orchestrator**: Software development only
- **quality_gate_orchestrator**: Iterative feedback loop management
- **sitespect_orchestrator**: Website audits with browser automation
- **strategy_orchestrator**: Strategic analysis and cross-domain integration

**Reference:** CLAUDE.md (root) - Orchestrator Roles Clarification

---

## Automation Workflows

### Content Creation Workflow
```
User Request → Glenn Routing → Research Phase Validation → Content Creation →
Feedback Loop (4 agents) → British English Validation → Document Conversion →
Google Drive Upload → Client Notification
```

### File System Automation
```
.md File Created → File System Watcher → Pre-Delivery Audit →
Generate Missing Files → Convert to .docx → Upload to Google Drive
```

### Quality Assurance Workflow
```
Content Draft → clarity_conciseness_editor → cognitive_load_minimizer →
content_critique_specialist → ai_text_naturalizer → content_refiner →
enhanced_content_auditor → Final Approval
```

**Reference:** [AUTOMATION_SYSTEM_DOCUMENTATION.md](AUTOMATION_SYSTEM_DOCUMENTATION.md)

---

## Error Handling for AI Agents

### Common Issues and Automated Resolution

1. **Missing Research Phases**
   - **Detection:** Research phase validation check
   - **Resolution:** Generate missing research templates
   - **Reference:** SYSTEM_RELIABILITY_GUIDE.md

2. **British English Non-Compliance**
   - **Detection:** Automated spelling and terminology check
   - **Resolution:** Auto-correction with validation
   - **Reference:** CLAUDE.md - British English Compliance

3. **Incorrect Folder Structure**
   - **Detection:** Client structure validation
   - **Resolution:** Auto-fix with template generation
   - **Reference:** CLIENT_ORGANIZATION_STANDARDS.md (root)

4. **Quality Score Below Threshold**
   - **Detection:** Feedback loop scoring
   - **Resolution:** Additional refinement iteration
   - **Reference:** CLAUDE.md - Iterative Feedback Loop System

**Reference:** [SYSTEM_RELIABILITY_GUIDE.md](SYSTEM_RELIABILITY_GUIDE.md)

---

## Integration Points

### Document Processing
- **Input:** Markdown (.md) files in clients/ folder
- **Process:** Convert to professional .docx with British English
- **Output:** Styled document in Google Drive client folder

### Web Research
- **Tools:** Jina MCP, Scrapy spiders, web scraper CLI
- **Purpose:** SEO analysis, competitor research, market intelligence
- **Output:** Structured JSON/CSV data for analysis

### Quality Assurance
- **Validation:** Structure, research phases, British English, citations
- **Feedback:** Multi-agent iterative improvement
- **Approval:** Quality gate with aggregate scoring

**Reference:** [BIGGER_BOSS_SYSTEM_DOCUMENTATION.md](BIGGER_BOSS_SYSTEM_DOCUMENTATION.md)

---

## Best Practices for AI Agents

### 1. Always Route Through Glenn
✅ Start every request with Glenn analysis
✅ Trust Glenn's agent selection recommendations
✅ Follow Glenn's research phase requirements

### 2. Validate Before Processing
✅ Check research phase completion
✅ Verify client folder structure
✅ Validate British English compliance

### 3. Use Iterative Feedback Loops
✅ Never skip feedback loop phases
✅ Ensure all thresholds are met
✅ Track improvement between iterations

### 4. Maintain Quality Standards
✅ Aggregate score ≥8.5/10 required
✅ All statistics must have citations
✅ British English mandatory throughout

### 5. Follow Orchestrator Specialization
✅ Content tasks → master_orchestrator
✅ Software tasks → workflow-orchestrator
✅ Quality review → quality_gate_orchestrator

---

## Quick Reference Commands

### System Status Checks
```bash
# Validate client structure
python scripts/validate_client_structure.py clients/{client}/ --auto-fix

# Verify research phases
python scripts/validate_research_phases.py {client} validate

# Check British English compliance
python scripts/validate_british_english.py {file} --auto-correct
```

### Manual Workflow Triggers
```bash
# Trigger complete automation workflow
python scripts/automation/workflow_orchestrator.py --trigger-file="{file}"

# Run pre-delivery audit
python scripts/pre_delivery_audit.py "{file}" --auto-generate

# Convert documents
python scripts/convert_my_docs.py "{folder}" --batch

# Upload to Google Drive
python scripts/gdrive_upload.py folder "{folder}"
```

---

## Related Documentation

- **Primary Configuration:** [CLAUDE.md](../../CLAUDE.md) (root directory)
- **Client Standards:** [CLIENT_ORGANIZATION_STANDARDS.md](../../CLIENT_ORGANIZATION_STANDARDS.md) (root)
- **User Manual:** [../for_users/USER_MANUAL.md](../for_users/USER_MANUAL.md)
- **Historical Context:** [../archive/README.md](../archive/README.md)

---

**For human setup and operations, see:** [User Instructions](../for_users/README.md)