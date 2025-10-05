# AI Agent System Operation Guide

**Document Version**: 1.0
**Last Updated**: 30 September 2025
**Audience**: AI Agents & Autonomous Systems
**Purpose**: Complete operational reference for automated marketing content system

---

## Table of Contents

1. [System Architecture Overview](#system-architecture-overview)
2. [Agent Coordination Framework](#agent-coordination-framework)
3. [Mandatory Research Workflow](#mandatory-research-workflow)
4. [File Generation & Verification](#file-generation--verification)
5. [Automation Execution Layer](#automation-execution-layer)
6. [Quality Gate Checkpoints](#quality-gate-checkpoints)
7. [Iterative Feedback Loops](#iterative-feedback-loops)
8. [Error Handling & Recovery](#error-handling--recovery)

---

## System Architecture Overview

### Core Components

```yaml
system_architecture:
  automation_layer:
    file_system_watcher: scripts/automation/file_system_watcher.py
    workflow_orchestrator: scripts/automation/workflow_orchestrator.py
    emergency_fix: scripts/emergency_automation_fix.py

  compliance_verification:
    pre_delivery_audit: scripts/pre_delivery_audit.py
    template_generation: auto_generate_missing_files()

  conversion_pipeline:
    markdown_to_docx: scripts/convert_my_docs.py
    document_upload: scripts/gdrive_upload.py

  agent_coordination:
    master_orchestrator: .claude/agents/master_orchestrator.md
    glenn_router: .claude/agents/glenn.md
    quality_gate: quality_gate_orchestrator
```

### System Responsibilities

**Automation Layer**: Monitors file creation, triggers workflows, executes complete automation chain
**Compliance Layer**: Verifies mandatory deliverables, generates missing files, enforces SOP standards
**Conversion Layer**: Transforms markdown to .docx, uploads to Google Drive, tracks activity
**Agent Layer**: Coordinates specialist agents, enforces research phases, manages quality gates

---

## Agent Coordination Framework

### Primary Orchestrators

#### Master Orchestrator
**Role**: Execute all content-related tasks with mandatory research phases
**Location**: `.claude/agents/master_orchestrator.md`

**CRITICAL EXECUTION MANDATE:**

```markdown
⚠️ YOU MUST CREATE ACTUAL FILES - NOT DELEGATION PLANS

ABSOLUTE PROHIBITIONS:
❌ NEVER mark tasks complete without verifying files exist
❌ NEVER create "coordination plans" instead of deliverable files
❌ NEVER write "@agent_name should create X" without invoking agent
❌ NEVER delegate research without executing and verifying completion
❌ NEVER skip mandatory research phases before content creation

YOUR ROLE IS EXECUTION, NOT PLANNING:
✅ USE Write tool to create all mandatory research files
✅ INVOKE specialist agents and verify their output files exist
✅ VERIFY file existence before marking any phase complete
✅ BLOCK content creation until all research files confirmed present
✅ CREATE actual research documents, not task lists
```

#### Glenn Router
**Role**: Request routing with research verification blocking
**Location**: `.claude/agents/glenn.md`

**RESEARCH BLOCKING RULE:**

```markdown
❌ DO NOT ALLOW CONTENT CREATION WITHOUT RESEARCH VERIFICATION

BEFORE routing any content request:
1. Check if research files exist in client folder
2. If missing, REFUSE to proceed to content creation
3. State: "Research must be completed before content creation"
4. Route to research workflow FIRST, content creation SECOND

FILE VERIFICATION REQUIREMENT:
Use Glob tool to check for:
- clients/[CLIENT]/research/competitive_analysis.md
- clients/[CLIENT]/research/audience_personas.md
- clients/[CLIENT]/research/keyword_research.md
- clients/[CLIENT]/strategy/research_brief.md
- clients/[CLIENT]/content/content_research.md

IF FILES MISSING: Reject content request, require research first
```

### Multi-Layer Protection System

```yaml
protection_layers:
  layer_1_agent_instructions:
    enforcement: Explicit prohibitions in agent persona files
    validation: File existence verification before proceeding

  layer_2_routing:
    enforcement: Glenn blocks content requests without research
    validation: Glob tool checks for mandatory research files

  layer_3_automation:
    enforcement: Pre-delivery audit generates missing files
    validation: Template creation for incomplete deliverables

  layer_4_monitoring:
    enforcement: File system watcher triggers audit on creation
    validation: Workflow orchestrator executes complete chain
```

---

## Mandatory Research Workflow

### Four-Phase Research Framework

**ALL content creation MUST complete these phases in sequence:**

#### Phase 1: Foundation Research & Strategic Analysis
```yaml
deliverables:
  - research/competitive_analysis.md         # SOP compliance, market analysis
  - research/audience_personas.md            # Detailed audience research
  - strategy/research_brief.md               # USP analysis, brand SWOT

verification_checkpoint:
  tool: Glob
  pattern: "clients/[CLIENT]/research/*.md"
  required_count: 3
  block_if_missing: true
```

#### Phase 2: Competitive Intelligence & Search Landscape
```yaml
deliverables:
  - research/competitive_analysis.md (expanded)  # Competitor SWOT analysis
  - research/content_research.md                 # Trending topics, gaps
  - technical/technical_audit.md                 # Search landscape analysis

verification_checkpoint:
  content_required:
    - Brand positioning analysis
    - Content gap identification
    - Search landscape metrics
```

#### Phase 3: Advanced SEO & Keyword Strategy
```yaml
deliverables:
  - research/keyword_research.md             # Comprehensive keyword mapping
  - content/content_research.md (expanded)   # Search intent analysis

keyword_requirements:
  - Keyword gap analysis
  - Funnel stage keywords (awareness/consideration/decision)
  - Untapped angle keywords (zero/low competition)
  - Emerging trends keywords
```

#### Phase 4: Content Planning & AI Optimization
```yaml
deliverables:
  - content/comprehensive_website_content_plans.md  # Detailed briefs
  - technical/ai_optimization_guide.md              # AI readiness optimization

content_specifications:
  - Page layouts with wireframes
  - Word counts and conversion paths
  - Headlines, sections, CTAs
  - 12-month content calendar
  - Topic clusters and related content mapping
```

### MANDATORY VERIFICATION CHECKPOINT

**Before ANY content generation, execute this verification:**

```python
# Verification protocol - MUST execute before Phase 5
def verify_research_completion(client_domain: str) -> bool:
    """Verify all mandatory research files exist before content creation."""

    required_files = [
        f"clients/{client_domain}/research/competitive_analysis.md",
        f"clients/{client_domain}/research/audience_personas.md",
        f"clients/{client_domain}/research/keyword_research.md",
        f"clients/{client_domain}/strategy/research_brief.md",
        f"clients/{client_domain}/content/content_research.md",
        f"clients/{client_domain}/technical/technical_audit.md",
        f"clients/{client_domain}/technical/ai_optimization_guide.md",
        f"clients/{client_domain}/technical/ux_ui_analysis.md",
    ]

    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)

    if missing_files:
        print("❌ BLOCKING: Research files missing")
        print("Missing files:")
        for file in missing_files:
            print(f"  - {file}")
        print("\n🛑 STOP: Create missing files using Write tool with research content")
        print("🛑 DO NOT proceed to content generation")
        return False

    print("✅ All research files verified - proceeding to content generation")
    return True
```

---

## File Generation & Verification

### Standardized Client Folder Structure

**ALWAYS use this structure for ALL client work:**

```
clients/
└── {client_domain_name}/
    ├── README.md                           # Project navigation hub
    ├── PROJECT_OVERVIEW.md                 # Executive summary
    ├── PROJECT_CHECKLIST.md                # Progress tracking
    │
    ├── strategy/                           # Strategic planning
    │   ├── research_brief.md
    │   ├── current_website_analysis.md
    │   └── implementation_plan.md
    │
    ├── research/                           # Market intelligence
    │   ├── competitive_analysis.md
    │   ├── audience_personas.md
    │   └── keyword_research.md
    │
    ├── content/                            # Content strategy
    │   ├── comprehensive_website_content_plans.md
    │   ├── content_research.md
    │   └── audience_style_guide.md
    │
    ├── technical/                          # Technical audits
    │   ├── technical_audit.md
    │   ├── ai_optimization_guide.md
    │   └── ux_ui_analysis.md
    │
    └── implementation/                     # Execution tracking
        ├── task_deps.md                    # Task dependency plan
        └── execution_tracking_report.md
```

### Mandatory Deliverables (15 Files)

**Pre-delivery audit verifies these files exist:**

```yaml
mandatory_files:
  foundational:
    - README.md
    - PROJECT_OVERVIEW.md
    - PROJECT_CHECKLIST.md

  strategy:
    - strategy/research_brief.md
    - strategy/current_website_analysis.md
    - strategy/implementation_plan.md

  research:
    - research/competitive_analysis.md
    - research/audience_personas.md
    - research/keyword_research.md

  content:
    - content/comprehensive_website_content_plans.md
    - content/content_research.md
    - content/audience_style_guide.md

  technical:
    - technical/technical_audit.md
    - technical/ai_optimization_guide.md
    - technical/ux_ui_analysis.md
```

### SOP Compliance Requirements

**Word Count Standards:**

```yaml
word_count_sop:
  content_strategy:
    minimum: 800 words
    maximum: 1500 words
    enforcement: pre_delivery_audit.py

  research_documents:
    minimum: 500 words
    target: 1000 words

  technical_audits:
    minimum: 800 words
    target: 1200 words
```

### Auto-Generation Templates

**When files are missing, pre_delivery_audit.py creates them using these templates:**

Templates include:
- Research brief with SOP compliance framework
- Competitive analysis with SWOT methodology
- Audience personas with detailed demographics
- Keyword research with SEO mapping
- Content plans with strategic alignment
- Technical audits with performance metrics
- AI optimization with schema markup
- UX/UI analysis with accessibility standards

---

## Automation Execution Layer

### File System Watcher

**Purpose**: Real-time monitoring of client folder for new file creation
**Script**: `scripts/automation/file_system_watcher.py`

**Operation:**

```python
class ClientContentWatcher(FileSystemEventHandler):
    """Monitors clients/ folder and triggers automation on file creation."""

    def on_created(self, event):
        """Handle new file creation events."""
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # Trigger automation chain for client content
        if 'clients/' in str(file_path) and file_path.suffix == '.md':
            logger.info(f"New client content detected: {file_path}")
            self.trigger_automation_workflow(file_path)

    def trigger_automation_workflow(self, file_path: str):
        """Execute complete automation workflow."""
        cmd = [
            sys.executable,
            str(self.orchestrator_path),
            "--trigger-file",
            file_path
        ]
        subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
```

**Monitored Patterns:**
- `clients/**/*.md` - Triggers full automation chain
- `clients/**/*.docx` - Triggers upload only
- Excludes: `.git/`, `temp/`, `__pycache__/`

### Workflow Orchestrator

**Purpose**: Executes complete end-to-end automation workflow
**Script**: `scripts/automation/workflow_orchestrator.py`

**Automation Chain:**

```python
async def execute_complete_workflow(self, trigger_file_path: str) -> Dict:
    """Execute the complete automation workflow."""

    workflow_results = {
        'trigger_file': trigger_file_path,
        'phases': {}
    }

    # Phase 1: Pre-delivery audit and missing file generation
    logger.info("Phase 1: Running pre-delivery audit...")
    audit_result = await self.run_pre_delivery_audit(trigger_file_path)
    workflow_results['phases']['audit'] = audit_result

    # Phase 2: Convert all markdown files to .docx
    logger.info("Phase 2: Converting markdown to .docx...")
    conversion_result = await self.convert_client_files_to_docx(trigger_file_path)
    workflow_results['phases']['conversion'] = conversion_result

    # Phase 3: Upload to Google Drive
    logger.info("Phase 3: Uploading to Google Drive...")
    upload_result = await self.upload_client_files(trigger_file_path)
    workflow_results['phases']['upload'] = upload_result

    # Phase 4: Record automation activity
    logger.info("Phase 4: Recording automation activity...")
    activity_result = await self.record_automation_activity(trigger_file_path, workflow_results)
    workflow_results['phases']['activity_tracking'] = activity_result

    return workflow_results
```

**Execution Triggers:**
- Automatic: File system watcher detects new .md file
- Manual: `python scripts/emergency_automation_fix.py --client=[domain]`

### Emergency Automation Fix

**Purpose**: Manual workflow triggering and system recovery
**Script**: `scripts/emergency_automation_fix.py`

**Usage:**

```bash
# Trigger automation for specific client
python scripts/emergency_automation_fix.py --client=example_com_au

# Test automation workflow
python scripts/emergency_automation_fix.py --test

# Enable file system watcher
python scripts/emergency_automation_fix.py --enable-watcher
```

---

## Quality Gate Checkpoints

### Pre-Delivery Audit

**Script**: `scripts/pre_delivery_audit.py`

**Audit Phases:**

```python
def run_comprehensive_audit(client_domain: str) -> Dict:
    """Execute complete compliance verification."""

    audit_results = {
        'client': client_domain,
        'timestamp': datetime.now().isoformat(),
        'compliance': {}
    }

    # Phase 1: Check mandatory files (15 required)
    file_compliance = check_mandatory_files(client_domain)
    audit_results['compliance']['files'] = file_compliance

    # Phase 2: Verify word count compliance
    word_count_compliance = check_word_count_compliance(client_domain)
    audit_results['compliance']['word_counts'] = word_count_compliance

    # Phase 3: Verify research phase completion
    research_compliance = verify_research_phases(client_domain)
    audit_results['compliance']['research'] = research_compliance

    # Phase 4: Generate missing files if needed
    if file_compliance['missing_files']:
        generation_result = generate_missing_file_templates(client_domain, file_compliance['missing_files'])
        audit_results['auto_generation'] = generation_result

    return audit_results
```

**Compliance Metrics:**

```yaml
compliance_scoring:
  mandatory_files:
    weight: 60%
    calculation: (existing_files / 15) * 100

  word_count_compliance:
    weight: 25%
    calculation: (compliant_files / total_strategy_files) * 100

  research_completeness:
    weight: 15%
    calculation: (completed_phases / 4) * 100

  overall_compliance:
    calculation: weighted_average_of_all_metrics
    target: ≥95%
```

### Iterative Feedback Loop System

**Quality Gate Orchestrator manages multi-agent feedback cycles:**

```yaml
feedback_loop_sequence:
  agents:
    - clarity_conciseness_editor          # Threshold: 8/10
    - cognitive_load_minimizer            # Threshold: 7/10
    - content_critique_specialist         # Threshold: 7/10
    - ai_text_naturalizer                 # Threshold: 8/10

  process:
    max_iterations: 3
    loop_back_trigger: score_below_threshold
    refinement_agent: content_refiner
    final_gate: enhanced_content_auditor

  success_criteria:
    individual_thresholds: all_agents_must_pass
    aggregate_score: ≥8.5/10
    improvement_tracking: measurable_progress_required
    human_escalation: triggered_after_2_cycles_no_improvement
```

---

## Iterative Feedback Loops

### Agent Sequence & Thresholds

**ALL content creation MUST pass through this sequence:**

#### 1. Clarity & Conciseness Editor
**Threshold**: 8/10
**Focus**: Grammar, spelling, sentence structure, flow, Australian English compliance

**Evaluation Criteria:**
```yaml
grammar_spelling:
  score_range: 0-10
  criteria: accuracy, consistency, australian_english

sentence_structure:
  score_range: 0-10
  criteria: clarity, variety, readability

flow_cohesion:
  score_range: 0-10
  criteria: logical_progression, transitions, coherence
```

#### 2. Cognitive Load Minimizer
**Threshold**: 7/10
**Focus**: Information hierarchy, cognitive complexity reduction, scanability

**Evaluation Criteria:**
```yaml
information_hierarchy:
  score_range: 0-10
  criteria: logical_organization, progressive_disclosure

cognitive_complexity:
  score_range: 0-10
  criteria: processing_ease, mental_effort_required

scanability:
  score_range: 0-10
  criteria: visual_hierarchy, skimmability, findability
```

#### 3. Content Critique Specialist
**Threshold**: 7/10
**Focus**: Argument strengthening, logical consistency, evidence support

**Evaluation Criteria:**
```yaml
argument_strength:
  score_range: 0-10
  framework: toulmin_model
  criteria: claims, evidence, warrants

logical_consistency:
  score_range: 0-10
  criteria: coherence, non_contradiction, validity

evidence_support:
  score_range: 0-10
  criteria: credible_sources, citation_quality, relevance
```

#### 4. AI Text Naturalizer
**Threshold**: 8/10
**Focus**: AI artifact removal, natural flow, human expression

**Evaluation Criteria:**
```yaml
ai_artifact_detection:
  score_range: 0-10
  artifacts: cliche_phrases, generic_statements, formulaic_structure

natural_flow:
  score_range: 0-10
  criteria: conversational_tone, rhythm, authenticity

human_expression:
  score_range: 0-10
  criteria: personality, voice, relatability
```

### Refinement Cycle Process

```python
def execute_feedback_loop(content: str, content_type: str) -> Dict:
    """Execute iterative feedback loop with quality gates."""

    max_iterations = 3
    current_iteration = 0
    aggregate_score = 0.0

    agent_sequence = [
        'clarity_conciseness_editor',
        'cognitive_load_minimizer',
        'content_critique_specialist',
        'ai_text_naturalizer'
    ]

    while current_iteration < max_iterations:
        current_iteration += 1
        iteration_scores = {}

        # Execute each agent in sequence
        for agent in agent_sequence:
            evaluation = execute_agent_evaluation(agent, content)
            iteration_scores[agent] = evaluation['score']

            # If below threshold, trigger content_refiner
            if evaluation['score'] < agent_thresholds[agent]:
                content = execute_content_refinement(content, evaluation['feedback'])

        # Calculate aggregate score
        aggregate_score = sum(iteration_scores.values()) / len(iteration_scores)

        # Check if all thresholds met
        if all(score >= agent_thresholds[agent] for agent, score in iteration_scores.items()):
            if aggregate_score >= 8.5:
                # Success - proceed to final gate
                final_result = execute_enhanced_content_auditor(content)
                return {
                    'success': True,
                    'iterations': current_iteration,
                    'aggregate_score': aggregate_score,
                    'final_audit': final_result
                }

        # Check for improvement stagnation
        if current_iteration >= 2 and not measurable_improvement(iteration_scores):
            # Trigger human escalation
            return {
                'success': False,
                'reason': 'no_improvement_detected',
                'escalation': 'human_review_required',
                'iterations': current_iteration
            }

    # Max iterations reached without success
    return {
        'success': False,
        'reason': 'max_iterations_reached',
        'aggregate_score': aggregate_score,
        'iterations': current_iteration
    }
```

---

## Error Handling & Recovery

### Common Issues & Solutions

#### Issue 1: Unicode Encoding Errors (Windows)
**Error**: `'charmap' codec can't encode character`

**Solution**:
```python
# Add to all scripts using Unicode output
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
```

#### Issue 2: Watchdog Library Missing
**Error**: `NameError: name 'FileSystemEventHandler' is not defined`

**Solution**:
```bash
pip install watchdog
```

#### Issue 3: Logs Directory Missing
**Error**: `FileNotFoundError: 'logs/automation_orchestrator.log'`

**Solution**:
```bash
mkdir "C:\Apps\Agents\Bigger Boss\bigger-boss\logs"
```

#### Issue 4: RClone Configuration Missing
**Error**: `Config file not found, didn't find section in config file`

**Solution**: Follow rclone setup instructions in USER_MANUAL.md

### Workflow Recovery Protocol

```python
async def handle_workflow_error(self, file_path: str, error: Exception) -> Dict:
    """Robust error handling with automatic recovery."""

    error_type = type(error).__name__

    recovery_strategies = {
        'FileNotFoundError': self.retry_with_file_verification,
        'PermissionError': self.escalate_to_manual_intervention,
        'UnicodeEncodeError': self.apply_unicode_fix_and_retry,
        'subprocess.CalledProcessError': self.analyze_subprocess_failure,
    }

    # Log error
    logger.error(f"Workflow error: {error_type} - {str(error)}")

    # Attempt recovery
    if error_type in recovery_strategies:
        recovery_result = await recovery_strategies[error_type](file_path, error)

        if recovery_result['success']:
            logger.info(f"Automatic recovery successful: {error_type}")
            return recovery_result

    # If recovery fails, escalate
    return {
        'success': False,
        'error_type': error_type,
        'error_message': str(error),
        'escalation': 'manual_intervention_required',
        'file_path': file_path
    }
```

---

## Best Practices Summary

### Agent Execution Checklist

**Before starting ANY client project:**

- [ ] Create proper folder structure in `clients/{client_domain}/`
- [ ] Use standardized subfolder organization (strategy/, research/, content/, technical/, implementation/)
- [ ] Create README.md for project navigation
- [ ] Execute ALL 4 mandatory research phases BEFORE content creation
- [ ] Use Glob tool to verify ALL research files exist before proceeding
- [ ] Block content creation if any research files missing
- [ ] Create actual files using Write tool - NEVER just task lists
- [ ] Invoke specialist agents and verify their output files exist
- [ ] Include source citations for all claims and statistics
- [ ] Follow Australian English spelling and terminology
- [ ] Integrate iterative feedback loops in task_deps.md
- [ ] Verify SOP word count compliance (800-1,500 words for strategies)

### Multi-Layer Verification Protocol

```yaml
verification_layers:
  agent_level:
    - Explicit execution mandate in persona files
    - File existence verification before proceeding
    - Prohibition against coordination-only approach

  routing_level:
    - Glenn blocks content requests without research
    - Glob tool checks for mandatory research files
    - Refuse to proceed if files missing

  automation_level:
    - Pre-delivery audit generates missing files
    - Template creation for incomplete deliverables
    - Compliance scoring and reporting

  monitoring_level:
    - File system watcher triggers audit on creation
    - Workflow orchestrator executes complete chain
    - Error handling with automatic recovery
```

---

**This guide ensures consistent, compliant, high-quality automated execution across all client projects. All agents MUST adhere to these operational standards to maintain system integrity and client deliverable quality.**