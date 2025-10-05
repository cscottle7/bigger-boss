# Bigger Boss Agent System - Quick Start Guide

## 🚀 Getting Started

This quick start guide will help you set up and begin using the enhanced Bigger Boss Agent System immediately.

### Prerequisites
- Python 3.8+ installed
- Node.js 16+ installed
- Git installed
- Internet connection for package installation

## 📦 Installation

### 1. Automated Setup
Run the comprehensive installation script:

```bash
python scripts/install/install.py
```

This will:
- ✅ Install all system dependencies
- ✅ Set up directory structure
- ✅ Configure Python and Node.js packages
- ✅ Create environment templates
- ✅ Test system functionality

### 2. Configuration

#### Create Environment File
Copy `.env.template` to `.env` and configure:

```bash
# Essential API Keys
JINA_API_KEY=your_jina_api_key_here
GOOGLE_DRIVE_CLIENT_ID=your_client_id
GOOGLE_DRIVE_CLIENT_SECRET=your_client_secret
```

#### Set Up Google Drive Integration
```bash
python scripts/gdrive_upload.py setup --interactive
```

## 🎯 First Project Setup

### 1. Create Client Project
```bash
# Validate and create client structure
python scripts/validate_client_structure.py clients/example_com_au --auto-fix
```

This creates:
- ✅ Standardised folder structure
- ✅ Template files for all research phases
- ✅ Project checklist and tracking documents

### 2. Content Planning Workflow
```bash
# Generate comprehensive content strategy
python scripts/workflow_orchestration/content_planning_workflows.py example_com_au
```

This generates:
- 📊 Audience personas and style guides
- 🗺️ User journey mapping
- 📈 Trending topic analysis
- 📝 6-month content calendar
- 🎯 Pillar page strategy

## 🔄 Daily Operations

### Content Creation Workflow

#### 1. Ensure Research Completion
```bash
python scripts/validate_research_phases.py example_com_au validate --require-phases 1 2 3 4
```

#### 2. Create Content (Markdown)
Write your content in markdown format with British English spelling.

#### 3. Automatic Processing
The hook system automatically:
- 📄 Converts markdown to professional DOCX
- ☁️ Uploads to client's Google Drive folder
- ✅ Validates British English compliance
- 📁 Organises in correct folder structure

### Web Research Operations

#### SEO Analysis
```bash
python scripts/web_scraper_cli.py seo https://client-website.com.au --mode=comprehensive
```

#### Competitor Analysis
```bash
python scripts/web_scraper_cli.py competitor https://competitor1.com,https://competitor2.com --depth=standard
```

#### Bulk SEO Analysis
```bash
# Create urls.txt with one URL per line
python scripts/web_scraper_cli.py bulk urls.txt --mode=basic
```

## 🔍 Quality Assurance

### Validate Client Structure
```bash
# Single client
python scripts/validate_client_structure.py clients/example_com_au --auto-fix

# All clients
python scripts/validate_client_structure.py clients/ --batch --auto-fix
```

### British English Compliance
```bash
# Single file
python scripts/validate_british_english.py document.md --auto-correct

# Batch validation
python scripts/validate_british_english.py clients/example_com_au/ --batch --pattern="*.md" --auto-correct
```

### Research Phase Verification
```bash
python scripts/validate_research_phases.py example_com_au validate
```

## 📊 Common Commands Reference

### Document Processing
```bash
# Convert markdown to DOCX
python scripts/md_to_docx.py document.md --style=professional

# Upload to Google Drive
python scripts/gdrive_upload.py upload document.docx --client=example_com_au
```

### System Maintenance
```bash
# Error statistics
python scripts/error_handler.py --stats 7

# Generate style guide
python scripts/validate_british_english.py --generate-guide --report=style_guide.md

# Installation test
python scripts/install/install.py --test-only
```

### Web Scraping
```bash
# List available spiders
python scripts/web_scraper_cli.py list

# Generate SEO report
python scripts/web_scraper_cli.py report scraped_data.json --output=seo_report.json
```

## 🎛️ Hook System

The hook system automatically handles:

- **Glenn Routing** - All requests route through Glenn for proper agent selection
- **File Conversion** - Markdown files automatically convert to DOCX
- **Google Drive Upload** - DOCX files automatically upload to client folders
- **Quality Validation** - British English and structure validation
- **Error Recovery** - Automatic error handling and recovery

### Manual Hook Testing
```bash
# Test specific hook
echo '{"test": "content"}' | python scripts/custom_mcp_server.py

# View hook logs
tail -f logs/hooks.log
```

## 🔧 Troubleshooting

### Installation Issues
```bash
# Verbose installation for debugging
python scripts/install/install.py --verbose

# Check individual components
python scripts/install/install.py --test-components
```

### Permission Errors
```bash
# Fix file permissions (Unix/Mac)
chmod +x scripts/*.py

# Windows: Run as administrator
```

### API Configuration Issues
```bash
# Test Jina MCP integration
python scripts/custom_mcp_server.py --test

# Test Google Drive connection
python scripts/gdrive_upload.py setup --test
```

### Client Structure Issues
```bash
# Auto-fix all structure issues
python scripts/validate_client_structure.py clients/ --batch --auto-fix

# Generate missing templates
python scripts/validate_research_phases.py client_domain templates
```

## 📈 Best Practices

### 1. Project Workflow
1. ✅ Always start with Glenn routing: `@glenn "Create content strategy for..."`
2. ✅ Validate research phases before content creation
3. ✅ Use British English spelling throughout
4. ✅ Follow standardised client folder structure

### 2. Content Creation
1. 📝 Write in markdown for automatic processing
2. 📊 Include statistics with proper citations
3. 🎯 Use appropriate headings (H1, H2, H3) for structure
4. 📱 Ensure mobile-friendly content length

### 3. Quality Management
1. 🔍 Run validation scripts regularly
2. 📋 Complete all research phases before content creation
3. ✅ Use auto-correction for British English compliance
4. 📊 Review error logs weekly

## 🆘 Quick Help

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Import errors | `pip install -r scripts/requirements.txt` |
| Permission denied | Run with elevated privileges or check file ownership |
| API rate limits | Implement delays, check API quotas |
| File not found | Use auto-fix option or create templates |
| Google Drive issues | Re-run setup: `python scripts/gdrive_upload.py setup` |

### Getting Help
1. 📖 Check full documentation: `BIGGER_BOSS_SYSTEM_DOCUMENTATION.md`
2. 🔍 Search logs: `logs/` directory
3. 📊 View error statistics: `python scripts/error_handler.py --stats 7`
4. 🧪 Run system tests: `python scripts/install/install.py --test`

---

## 🎉 You're Ready!

You now have a fully functional Bigger Boss Agent System with:
- ✅ Automated workflow orchestration
- ✅ Professional document processing
- ✅ Google Drive integration
- ✅ Web scraping capabilities
- ✅ Quality assurance automation
- ✅ British English compliance
- ✅ Comprehensive error handling

Start by creating your first client project and experience the power of automated marketing excellence!

---

**Quick Start Guide Version:** 2.0.0
**Last Updated:** 25 September 2024
**Next Update:** December 2024

*For detailed technical documentation, see `BIGGER_BOSS_SYSTEM_DOCUMENTATION.md`*