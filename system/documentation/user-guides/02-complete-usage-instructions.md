# Complete Usage Instructions

## System Requirements & Setup

### Prerequisites
- Python 3.9 or higher
- 8GB RAM minimum (16GB recommended for concurrent workflows)
- Active internet connection for web crawling and API integrations
- Access to target websites (publicly accessible URLs)

### Installation

1. **Clone and Setup Environment**
```bash
# Navigate to system directory
cd "C:\Users\cscot\Documents\Agents\Bigger Boss Agent"

# Install dependencies
pip install -r requirements.txt

# Verify installation
python system_status.py
```

2. **Configure Environment Variables**
Create `.env` file with required API keys:
```env
ANTHROPIC_API_KEY=your_anthropic_key
GTMETRIX_API_KEY=your_gtmetrix_key (optional)
SEMRUSH_API_KEY=your_semrush_key (optional)
```

3. **Verify System Health**
```bash
python system_status.py --detailed
```

Expected output: All systems operational, agents ready, tool library loaded.

---

## Command Reference

### Website Audit Commands (SiteSpect Squad)

#### Basic Website Audit
```bash
python workflows/run_site_audit.py --url "https://example.com"
```

#### Advanced Audit Options
```bash
# Focused technical SEO audit
python workflows/run_site_audit.py --url "https://example.com" --focus technical_seo

# Performance-only audit
python workflows/run_site_audit.py --url "https://example.com" --focus performance

# Accessibility compliance check
python workflows/run_site_audit.py --url "https://example.com" --focus accessibility

# High priority audit with detailed reporting
python workflows/run_site_audit.py --url "https://example.com" --priority urgent --report_detail comprehensive

# Comparative audit (requires previous audit results)
python workflows/run_site_audit.py --url "https://example.com" --compare_previous --baseline_file "previous_audit.json"
```

#### Batch Processing
```bash
# Multiple URL audit
python workflows/run_site_audit.py --url_file "site_list.csv" --batch_processing

# Staging environment validation
python workflows/run_site_audit.py --url "https://staging.example.com" --environment staging --pre_launch_checklist
```

---

### Content Creation Commands (ContentForge Squad)

#### Basic Content Brief Generation
```bash
python workflows/run_content_creation.py --topic "artificial intelligence in healthcare"
```

#### Advanced Content Creation
```bash
# With keyword targeting
python workflows/run_content_creation.py --topic "sustainable fashion" --keywords_file "keywords.csv"

# With brand guidelines integration
python workflows/run_content_creation.py --topic "B2B SaaS marketing" --keywords_file "keywords.csv" --brand_guidelines "brand_guide.pdf"

# Industry-specific content strategy
python workflows/run_content_creation.py --topic "fintech innovation" --industry_focus "financial_services" --compliance_requirements "fintech_compliance.pdf"

# Campaign-specific content development
python workflows/run_content_creation.py --topic "product launch campaign" --campaign_type "product_launch" --launch_timeline "Q2_2024"
```

#### Content Refresh Workflow
```bash
# Basic content refresh
python workflows/run_content_refresh.py --existing_content "content_audit.csv"

# Performance-focused refresh
python workflows/run_content_refresh.py --existing_content "content_audit.csv" --objectives "performance_improvement" --metrics_focus "organic_traffic"

# Competitive refresh analysis  
python workflows/run_content_refresh.py --existing_content "content_audit.csv" --competitor_analysis --competitors "comp1.com,comp2.com"
```

---

### Strategic Analysis Commands (StrategyNexus Squad)

#### Basic Strategic Analysis
```bash
python workflows/run_website_strategy.py --primary_url "https://yoursite.com"
```

#### Competitive Intelligence
```bash
# Multi-competitor analysis
python workflows/run_website_strategy.py --primary_url "https://yoursite.com" --competitors "comp1.com,comp2.com,comp3.com"

# Deep competitive analysis
python workflows/run_website_strategy.py --primary_url "https://yoursite.com" --competitors "comp1.com,comp2.com" --analysis_depth comprehensive --competitive_focus

# Market positioning analysis
python workflows/run_website_strategy.py --primary_url "https://yoursite.com" --competitors "comp1.com,comp2.com,comp3.com,comp4.com" --market_analysis --geographic_focus "north_america"
```

#### Strategic Planning Focus
```bash
# Brand positioning analysis
python workflows/run_website_strategy.py --primary_url "https://yoursite.com" --analysis_type brand_positioning --brand_guidelines "brand_guide.pdf"

# SEO strategy development
python workflows/run_website_strategy.py --primary_url "https://yoursite.com" --analysis_type seo_strategy --keyword_focus --content_gap_analysis

# User experience strategy
python workflows/run_website_strategy.py --primary_url "https://yoursite.com" --analysis_type user_experience --conversion_focus --journey_mapping
```

---

## File Format Requirements

### Keyword Files (CSV Format)
Required columns:
- `keyword` - Target keyword phrase
- `search_volume` - Monthly search volume (optional)
- `difficulty` - Keyword difficulty score (optional)
- `intent` - Search intent classification (optional)

Example structure:
```csv
keyword,search_volume,difficulty,intent
"sustainable fashion brands",1200,45,commercial
"eco-friendly clothing",890,38,informational
"ethical fashion guide",560,25,informational
```

### Content Audit Files (CSV Format)
Required columns:
- `url` - Content URL
- `title` - Content title
- `publish_date` - Publication date
- `last_updated` - Last modification date
- `organic_traffic` - Monthly organic traffic (optional)
- `rankings` - Current keyword rankings (optional)

### Brand Guidelines (PDF Format)
Should include:
- Brand voice and tone guidelines
- Visual identity standards
- Messaging framework
- Target audience definitions
- Brand positioning statements

---

## Output File Locations

### Default Output Directory Structure
```
outputs/
├── site_audits/
│   ├── YYYYMMDD_HHMMSS_domain_audit.pdf
│   ├── YYYYMMDD_HHMMSS_domain_data.json
│   └── executive_summaries/
├── content_briefs/
│   ├── YYYYMMDD_HHMMSS_topic_master_brief.pdf
│   ├── YYYYMMDD_HHMMSS_topic_content_outlines.pdf
│   └── research_data/
└── strategic_analysis/
    ├── YYYYMMDD_HHMMSS_domain_website_blueprint.pdf
    ├── YYYYMMDD_HHMMSS_domain_competitive_analysis.pdf
    └── implementation_roadmaps/
```

### Custom Output Configuration
```bash
# Specify custom output directory
python workflows/run_site_audit.py --url "https://example.com" --output_dir "/custom/path/outputs"

# Custom report naming
python workflows/run_site_audit.py --url "https://example.com" --report_name "client_name_audit" --timestamp_format "YYYY-MM-DD"
```

---

## Monitoring and Status Checking

### Workflow Status Commands
```bash
# Check all active workflows
python monitor_workflows.py

# Check specific workflow
python monitor_workflows.py --workflow_id "SA_20241201_001"

# View workflow history
python monitor_workflows.py --history --days 7

# Performance metrics
python monitor_workflows.py --performance_metrics --time_period monthly
```

### System Health Monitoring
```bash
# Complete system status
python system_status.py --comprehensive

# Agent availability check
python system_status.py --agents_only

# Tool library status
python system_status.py --tools_only

# Performance metrics
python system_status.py --performance --benchmark
```

---

## Human Review Gates Management

### Review Gate Configuration
```bash
# Configure review SLAs
python configure_review_gates.py --strategic_sla 24 --quality_sla 12 --notification_reminder 12

# Set up review notifications
python configure_review_gates.py --email_notifications --slack_integration --review_dashboard_url
```

### Manual Review Gate Interaction
```bash
# List pending reviews
python review_gates.py --list_pending

# Approve pending review
python review_gates.py --approve --review_id "RG_20241201_001" --comments "Approved with minor suggestions"

# Request revisions
python review_gates.py --revise --review_id "RG_20241201_001" --revision_notes "Please adjust brand voice in section 3"

# Review history
python review_gates.py --history --reviewer "your_name"
```

---

## Advanced Configuration

### Agent Customization
```bash
# Customize agent prompts (requires restart)
# Edit files in .claude/agents/ directory
nano .claude/agents/sitespect_orchestrator.md

# Reload agent configurations
python reload_agents.py --validate_prompts
```

### Workflow Customization
```bash
# Create custom workflow templates
python create_workflow_template.py --template_name "custom_audit" --base_workflow "site_audit" --modifications "custom_modifications.json"

# Industry-specific workflow configuration
python configure_industry_workflows.py --industry "ecommerce" --specializations "performance,conversion,mobile"
```

### Integration Setup
```bash
# Configure webhook integrations
python setup_integrations.py --webhook_url "https://your-system.com/webhook" --events "workflow_complete,review_required"

# API endpoint configuration
python setup_integrations.py --api_integration --endpoint_url "https://your-api.com/receive" --auth_token "your_token"

# Slack integration setup
python setup_integrations.py --slack_integration --webhook_url "https://hooks.slack.com/your-webhook" --channels "marketing,seo"
```

---

## Troubleshooting Guide

### Common Issues and Solutions

#### Issue: "URL not accessible" Error
**Symptoms**: Workflow fails with URL accessibility error
**Solutions**:
```bash
# Test URL accessibility
python test_url_accessibility.py --url "https://problematic-site.com"

# Check for specific issues
python test_url_accessibility.py --url "https://problematic-site.com" --detailed --check_robots --check_ssl
```

#### Issue: "Workflow stuck at review gate"
**Symptoms**: Workflow shows "pending_review" status indefinitely
**Solutions**:
```bash
# Check review gate status
python review_gates.py --status --workflow_id "stuck_workflow_id"

# Force review gate timeout (emergency use)
python review_gates.py --force_timeout --workflow_id "stuck_workflow_id" --justification "emergency_deployment"

# Resend review notifications
python review_gates.py --resend_notifications --review_id "review_id"
```

#### Issue: "File parsing failed" Error
**Symptoms**: CSV or PDF file processing errors
**Solutions**:
```bash
# Test file parsing
python test_file_parsing.py --file "problematic_file.csv" --file_type csv

# Validate file format
python validate_file_format.py --file "problematic_file.csv" --expected_format keyword_file

# Fix common file issues
python fix_file_format.py --file "problematic_file.csv" --auto_fix --backup
```

#### Issue: Performance Degradation
**Symptoms**: Workflows taking longer than expected
**Solutions**:
```bash
# Performance diagnostics
python diagnose_performance.py --workflow_type site_audit --recent_executions 10

# Resource utilization check
python system_status.py --resource_usage --detailed

# Clear caches and restart
python maintenance.py --clear_caches --restart_agents
```

---

## Maintenance and Updates

### Regular Maintenance Commands
```bash
# Daily maintenance routine
python maintenance.py --daily --clear_temp_files --update_metrics

# Weekly comprehensive maintenance
python maintenance.py --weekly --deep_clean --performance_analysis --system_optimization

# Monthly system health check
python maintenance.py --monthly --comprehensive_audit --security_check --backup_verification
```

### System Updates
```bash
# Check for system updates
python check_updates.py --system_components

# Update agent definitions
python update_system.py --agents_only --validate_after_update

# Full system update
python update_system.py --full_update --backup_before_update --validate_after_update
```

---

## Best Practices

### Workflow Execution
1. **Always test URLs first**: Use `test_url_accessibility.py` for new domains
2. **Prepare files properly**: Validate CSV/PDF formats before execution
3. **Monitor execution**: Use `monitor_workflows.py` for long-running analyses
4. **Review outputs**: Human review gates are critical for quality assurance

### Performance Optimization
1. **Batch processing**: Use batch commands for multiple similar tasks
2. **Schedule appropriately**: Run intensive workflows during off-peak hours
3. **Cache management**: Regular cache clearing prevents performance degradation
4. **Resource monitoring**: Monitor system resources during peak usage

### Quality Assurance
1. **Review gate management**: Respond to review requests within SLA timeframes
2. **Output validation**: Verify outputs match expected quality standards
3. **Feedback integration**: Use revision capabilities for iterative improvement
4. **Documentation**: Maintain records of customizations and configurations

---

## Support and Advanced Features

### Getting Help
```bash
# Built-in help system
python help_system.py --topic workflows
python help_system.py --topic agents
python help_system.py --topic troubleshooting

# Generate diagnostic report
python generate_diagnostic_report.py --comprehensive --include_logs --include_performance_data
```

### Advanced Analytics
```bash
# Workflow performance analytics
python analytics.py --workflow_performance --time_range "30_days" --export_csv

# Quality metrics analysis
python analytics.py --quality_metrics --comparison_baseline --trend_analysis

# ROI analysis
python analytics.py --roi_analysis --manual_time_comparison --efficiency_gains
```

### Custom Development
```bash
# Create custom agent
python create_custom_agent.py --agent_name "custom_agent" --base_template "content_analyst" --specialization "industry_specific"

# Develop custom tool
python create_custom_tool.py --tool_name "custom_analysis" --integration_points "external_api" --validation_tests
```

---

This comprehensive usage guide provides all necessary commands and configurations for operating the Autonomous Agentic Marketing System. For role-specific usage patterns, refer to the use-cases documentation. For technical troubleshooting, consult the troubleshooting section or generate a diagnostic report.