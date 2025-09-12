# Universal Feedback Loop Template for task_deps.md Files

## Template Overview
This template ensures all future projects include iterative feedback loops instead of linear QA processes.

## Universal task_deps.md Structure

### Phase 1: Content Creation Phase
```yaml
create_[content_name]:
  type: Implementation
  description: Create initial content draft following brief specifications
  dependencies: [prerequisite_tasks]
  estimated_time: [time_estimate]
  agent_type: content_generator
  success_criteria:
    - Brief specifications followed completely
    - Answer First methodology implemented
    - Australian English compliance verified
    - Core message integrity maintained
```

### Phase 2: Iterative Feedback Loop Phase (MANDATORY)
```yaml
feedback_loop_[content_name]:
  type: IterativeImprovement
  description: Multi-agent iterative feedback loop for [content_name] optimization
  dependencies: [create_[content_name]]
  estimated_time: [base_time * 1.5]  # Account for iterations
  agent_sequence: [clarity_conciseness_editor, cognitive_load_minimizer, content_critique_specialist, ai_text_naturalizer]
  max_iterations: 3
  orchestrator: quality_gate_orchestrator
  success_criteria:
    - clarity_conciseness_editor score ≥ 8/10
    - cognitive_load_minimizer score ≥ 7/10
    - content_critique_specialist score ≥ 7/10
    - ai_text_naturalizer score ≥ 8/10
    - Aggregate quality score ≥ 8.5/10
    - Measurable improvement between iterations
  loop_termination:
    - success: all_thresholds_met
    - safety: max_iterations_reached
    - escalation: no_improvement_after_2_cycles
```

### Phase 3: Final Quality Assurance Phase
```yaml
final_qa_[content_name]:
  type: Testing
  description: Final comprehensive multi-perspective quality review post-feedback loops
  dependencies: [feedback_loop_[content_name]]
  estimated_time: [reduced_time]  # Less time needed after feedback loops
  agent_type: enhanced_content_auditor
  success_criteria:
    - 4-perspective systematic review completed
    - All feedback loop improvements validated
    - Publication readiness confirmed
    - Implementation guidelines included
```

## Content Type Templates

### Website Content Pages
```yaml
# HOME PAGE EXAMPLE
create_home_page_content:
  type: Implementation
  description: Create HOME page content from copywriter brief
  dependencies: [content_brief_approved]
  estimated_time: 90min
  agent_type: content_generator
  
feedback_loop_home_page:
  type: IterativeImprovement
  description: Multi-agent iterative feedback loop for HOME page optimization
  dependencies: [create_home_page_content]
  estimated_time: 135min
  agent_sequence: [clarity_conciseness_editor, cognitive_load_minimizer, content_critique_specialist, ai_text_naturalizer]
  max_iterations: 3
  priority: CRITICAL
  
final_qa_home_page:
  type: Testing
  description: Final HOME page quality review post-feedback loops
  dependencies: [feedback_loop_home_page]
  estimated_time: 30min
  agent_type: enhanced_content_auditor
```

### Blog Posts/Articles
```yaml
create_blog_post_[topic]:
  type: Implementation
  description: Create blog post about [topic]
  dependencies: [keyword_research, content_outline]
  estimated_time: 120min
  agent_type: content_generator
  
feedback_loop_blog_post_[topic]:
  type: IterativeImprovement
  description: Multi-agent iterative feedback loop for blog post optimization
  dependencies: [create_blog_post_[topic]]
  estimated_time: 180min
  agent_sequence: [clarity_conciseness_editor, cognitive_load_minimizer, content_critique_specialist, ai_text_naturalizer]
  max_iterations: 3
  
final_qa_blog_post_[topic]:
  type: Testing
  description: Final blog post quality review post-feedback loops
  dependencies: [feedback_loop_blog_post_[topic]]
  estimated_time: 25min
  agent_type: enhanced_content_auditor
```

### Strategic Documents
```yaml
create_strategy_document:
  type: Implementation
  description: Create strategic planning document
  dependencies: [research_completed, stakeholder_input]
  estimated_time: 150min
  agent_type: content_generator
  
feedback_loop_strategy_document:
  type: IterativeImprovement
  description: Multi-agent iterative feedback loop for strategy document optimization
  dependencies: [create_strategy_document]
  estimated_time: 225min
  agent_sequence: [clarity_conciseness_editor, cognitive_load_minimizer, content_critique_specialist, ai_text_naturalizer]
  max_iterations: 3
  success_criteria:
    - All standard thresholds met
    - Strategic logic validated
    - Executive readiness confirmed
    
final_qa_strategy_document:
  type: Testing
  description: Final strategy document quality review post-feedback loops
  dependencies: [feedback_loop_strategy_document]
  estimated_time: 35min
  agent_type: enhanced_content_auditor
```

### Technical Documentation
```yaml
create_technical_guide:
  type: Implementation
  description: Create technical implementation guide
  dependencies: [technical_analysis, requirements_defined]
  estimated_time: 180min
  agent_type: content_generator
  
feedback_loop_technical_guide:
  type: IterativeImprovement
  description: Multi-agent iterative feedback loop for technical guide optimization
  dependencies: [create_technical_guide]
  estimated_time: 270min
  agent_sequence: [clarity_conciseness_editor, cognitive_load_minimizer, content_critique_specialist, ai_text_naturalizer]
  max_iterations: 3
  success_criteria:
    - All standard thresholds met
    - Technical accuracy verified
    - Implementation clarity confirmed
    
final_qa_technical_guide:
  type: Testing
  description: Final technical guide quality review post-feedback loops
  dependencies: [feedback_loop_technical_guide]
  estimated_time: 40min
  agent_type: enhanced_content_auditor
```

## Execution Parameters Template

### Concurrency Rules
```yaml
concurrency_rules:
  content_creation_phase: 
    max_parallel: 3
    resource_allocation: normal
    
  feedback_loop_phase:
    max_parallel: 2  # Resource intensive
    resource_allocation: high
    priority_management: enabled
    
  final_qa_phase:
    max_parallel: 3
    resource_allocation: normal
```

### Quality Gates
```yaml
quality_gates:
  content_creation_gate:
    - brief_compliance_verified
    - initial_self_review_passed
    - core_requirements_met
    
  feedback_loop_gate:
    - all_agent_thresholds_met
    - aggregate_score_achieved
    - improvement_progression_validated
    
  final_qa_gate:
    - multi_perspective_review_completed
    - publication_readiness_confirmed
    - implementation_guidelines_included
```

### Agent Coordination Strategy
```yaml
agent_coordination:
  primary_orchestrator: quality_gate_orchestrator
  feedback_loop_management:
    - iteration_tracking
    - score_monitoring
    - loop_termination_control
    - safety_mechanism_enforcement
    
  refinement_coordination:
    - targeted_improvement_application
    - quality_preservation
    - progress_validation
    
  escalation_protocols:
    - human_escalation_triggers
    - performance_monitoring
    - resource_optimization
```

## Time Estimation Guidelines

### Base Time Multipliers
- **Content Creation**: 1.0x (baseline)
- **Feedback Loop Phase**: 1.5x content creation time
- **Final QA**: 0.3x content creation time

### Example Calculations
```yaml
home_page_example:
  create_content: 90min
  feedback_loop: 135min (90 × 1.5)
  final_qa: 30min (90 × 0.33)
  total: 255min
  
blog_post_example:
  create_content: 120min
  feedback_loop: 180min (120 × 1.5)
  final_qa: 25min (120 × 0.2)
  total: 325min
```

## Implementation Checklist

### For Each New Project:
- [ ] Copy appropriate content type template
- [ ] Customize content names and dependencies
- [ ] Adjust time estimates based on complexity
- [ ] Verify all feedback loop phases included
- [ ] Configure agent thresholds appropriately
- [ ] Set up escalation protocols
- [ ] Test workflow with sample content

### Quality Validation:
- [ ] No linear QA processes remain
- [ ] All content goes through feedback loops
- [ ] Scoring thresholds properly configured
- [ ] Safety mechanisms in place
- [ ] Resource allocation optimized

This template ensures consistent, high-quality iterative improvement across all future projects.