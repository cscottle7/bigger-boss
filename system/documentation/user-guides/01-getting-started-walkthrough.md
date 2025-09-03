# Getting Started: User Walkthrough

## Welcome to the Autonomous Agentic Marketing System

This system transforms complex marketing workflows into automated processes managed by specialized AI agents. This walkthrough will guide you through your first interactions with each squad.

## System Overview

The system consists of three specialized squads:

- **SiteSpect Squad**: Website auditing and analysis
- **ContentForge Squad**: Content creation and optimization
- **StrategyNexus Squad**: Strategic analysis and planning

## Quick Start Guide

### 1. Environment Setup

First, ensure your environment is ready:

```bash
# Install dependencies
pip install -r requirements.txt

# Verify system status
python system_status.py
```

### 2. Your First Website Audit (SiteSpect)

Let's start with the most straightforward workflow:

```bash
# Run a complete website audit
python workflows/run_site_audit.py --url "https://example.com"
```

**What happens next:**
1. The system validates the URL
2. @sitespect_orchestrator coordinates 5 specialist agents
3. Each agent performs their analysis in parallel
4. Results are synthesized into a comprehensive audit report
5. You receive a detailed PDF report in ~20 seconds

**Expected Output:**
- Technical SEO analysis
- Performance metrics
- Accessibility compliance report
- UX flow validation
- Actionable recommendations

### 3. Your First Content Brief (ContentForge)

Create a master content brief for your next campaign:

```bash
# Generate content brief from topic and keywords
python workflows/run_content_creation.py --topic "sustainable fashion" --keywords_file "keywords.csv"
```

**What happens next:**
1. @content_director receives your request
2. Research Corps (4 agents) conducts parallel research
3. @content-strategist synthesizes findings into master brief
4. Human review gate activates for approval
5. Upon approval, content generation begins

**Expected Output:**
- Comprehensive content strategy document
- Target audience analysis
- Competitive landscape insights
- SEO-optimized content recommendations

### 4. Your First Strategic Analysis (StrategyNexus)

Analyze your competitive landscape:

```bash
# Run comprehensive strategic analysis
python workflows/run_website_strategy.py --primary_url "https://yoursite.com" --competitors "competitor1.com,competitor2.com"
```

**What happens next:**
1. @strategy_orchestrator coordinates analysis
2. Multi-layered competitive analysis begins
3. Brand positioning assessment
4. Strategic recommendations generated
5. Website blueprint created

## Navigation Tips

### Understanding Agent Coordination

Each squad uses a hybrid hierarchical-sequential model:

**Phase 1 (Research)**: Multiple agents work in parallel
- Faster execution
- Comprehensive data gathering
- Redundancy for reliability

**Phase 2 (Synthesis)**: Sequential processing
- Quality assurance
- Logical flow
- Human oversight points

### Human Review Gates

The system includes strategic pause points for your approval:

**Gate 1 - Strategic Approval**: 
- Reviews research synthesis
- 24-hour SLA for response
- Automated reminders after 12 hours

**Gate 2 - Final Quality Review**:
- Complete output review
- Brand alignment check
- Final approval before delivery

### Monitoring Your Workflows

Check workflow status:

```bash
# View active workflows
python monitor_workflows.py

# Check specific workflow
python monitor_workflows.py --workflow_id "SW_20241201_001"
```

## Common First-Time Scenarios

### Scenario 1: "I need a quick website audit for a client presentation"

```bash
python workflows/run_site_audit.py --url "https://client-site.com" --priority high
```
*Result: Complete audit in ~20 seconds*

### Scenario 2: "I need content ideas for our Q1 campaign"

1. Prepare your keyword research file (CSV format)
2. Run: `python workflows/run_content_creation.py --topic "Q1 campaign theme"`
3. Review the generated brief at the approval gate
4. Approve to generate content outlines

### Scenario 3: "I want to understand how we stack up against competitors"

```bash
python workflows/run_website_strategy.py --primary_url "https://oursite.com" --competitors "comp1.com,comp2.com,comp3.com"
```
*Result: Comprehensive competitive analysis with actionable insights*

## Troubleshooting Common Issues

### Issue: "Workflow stuck at human review gate"

**Solution**: Check your email for approval requests. The system sends notifications with approval links.

### Issue: "URL crawling failed"

**Solution**: Ensure the URL is publicly accessible. The system currently supports public websites only.

### Issue: "File parsing error"

**Solution**: Verify your CSV/PDF files are not corrupted. The system includes pre-flight validation.

## Next Steps

1. **Explore Advanced Features**: Try combining workflows for comprehensive campaigns
2. **Customize Agent Behavior**: Modify agent prompts in `.claude/agents/` for your specific needs
3. **Set Up Automation**: Configure triggers for automatic workflow execution
4. **Review Performance**: Use the monitoring dashboard to track efficiency gains

## Getting Help

- **Documentation**: Check `documentation/` folder for detailed guides
- **System Status**: Run `python system_status.py` for health checks
- **Agent Logs**: Review `logs/` folder for detailed execution traces
- **Community**: Join our internal Slack channel for tips and best practices

---

**Ready to transform your marketing workflows? Start with a simple website audit and experience the power of autonomous agent coordination!**