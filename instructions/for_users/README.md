# User Instructions & Setup Guides

**Audience:** Human Operators, System Administrators, Content Creators
**Purpose:** Manual setup procedures and operational guides
**Last Updated:** 30 September 2025

---

## Quick Start for New Users

### Getting Started (5 Minutes)

1. **Read the Overview**
   - Start with [README_CLEAN_SYSTEM.md](../../README_CLEAN_SYSTEM.md) in root directory
   - Understand what the system does

2. **Follow Quick Start Guide**
   - [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md)
   - Install dependencies and run first project

3. **Configure Google Drive (Optional)**
   - [RCLONE_SETUP_INSTRUCTIONS.md](RCLONE_SETUP_INSTRUCTIONS.md)
   - Set up automatic document upload

4. **Enable Automation (Optional)**
   - [AUTOMATIC_CONVERSION_SETUP_GUIDE.md](AUTOMATIC_CONVERSION_SETUP_GUIDE.md)
   - Configure file system watcher for automatic processing

---

## Documentation Index

### Essential Guides

| Document | Purpose | Time Required | Priority |
|----------|---------|---------------|----------|
| `USER_MANUAL.md` | Complete user manual | 30-45 min | **High** |
| `QUICK_START_GUIDE.md` | Fast onboarding | 10-15 min | **Essential** |
| `QUICK_REFERENCE_AUTOMATION.md` | Command reference | 5 min | **High** |

### Setup Guides

| Document | Purpose | Time Required | When Needed |
|----------|---------|---------------|-------------|
| `RCLONE_SETUP_INSTRUCTIONS.md` | Google Drive setup | 10-15 min | For automated uploads |
| `AUTOMATIC_CONVERSION_SETUP_GUIDE.md` | Automation setup | 15-30 min | For automatic processing |

---

## Common Tasks

### 1. First Time Setup

**Prerequisites:**
- Python 3.8+ installed
- Node.js 16+ installed
- Git installed
- Internet connection

**Steps:**
```bash
# 1. Install dependencies
python scripts/install/install.py

# 2. Configure environment
# Copy .env.template to .env and add API keys

# 3. Test installation
python scripts/install/install.py --test-only
```

**Reference:** [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md) - Installation Section

---

### 2. Creating a Client Project

**Workflow:**
```bash
# 1. Validate and create structure
python scripts/validate_client_structure.py clients/example_com_au --auto-fix

# 2. Generate content strategy
python scripts/workflow_orchestration/content_planning_workflows.py example_com_au

# 3. Verify research phases
python scripts/validate_research_phases.py example_com_au validate
```

**Reference:** [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md) - First Project Setup

---

### 3. Converting Documents

**Manual Conversion:**
```bash
# Single file
python scripts/md_to_docx.py document.md --style=professional

# Batch conversion
python scripts/convert_my_docs.py clients/example_com_au/ --batch
```

**Automatic Conversion:**
- Enable file system watcher (see AUTOMATIC_CONVERSION_SETUP_GUIDE.md)
- Files automatically convert when created/modified

**Reference:** [AUTOMATIC_CONVERSION_SETUP_GUIDE.md](AUTOMATIC_CONVERSION_SETUP_GUIDE.md)

---

### 4. Uploading to Google Drive

**Prerequisites:**
- rclone configured (see RCLONE_SETUP_INSTRUCTIONS.md)

**Commands:**
```bash
# Single file
python scripts/gdrive_upload.py upload document.docx --client=example_com_au

# Entire folder
python scripts/gdrive_upload.py folder clients/example_com_au/
```

**Reference:** [RCLONE_SETUP_INSTRUCTIONS.md](RCLONE_SETUP_INSTRUCTIONS.md)

---

### 5. Quality Validation

**Structure Validation:**
```bash
# Single client
python scripts/validate_client_structure.py clients/example_com_au --auto-fix

# All clients
python scripts/validate_client_structure.py clients/ --batch --auto-fix
```

**British English Compliance:**
```bash
# Single file
python scripts/validate_british_english.py document.md --auto-correct

# Batch validation
python scripts/validate_british_english.py clients/example_com_au/ --batch --auto-correct
```

**Research Phase Verification:**
```bash
python scripts/validate_research_phases.py example_com_au validate --require-phases 1 2 3 4
```

**Reference:** [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md) - Quality Assurance Section

---

### 6. Web Research & SEO Analysis

**SEO Analysis:**
```bash
python scripts/web_scraper_cli.py seo https://client-website.com.au --mode=comprehensive
```

**Competitor Analysis:**
```bash
python scripts/web_scraper_cli.py competitor https://competitor1.com,https://competitor2.com
```

**Bulk Analysis:**
```bash
# Create urls.txt with one URL per line
python scripts/web_scraper_cli.py bulk urls.txt --mode=basic
```

**Reference:** [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md) - Web Research Operations

---

## Setup Procedures

### Google Drive Integration

**Why:** Automatically upload client deliverables to organized Google Drive folders

**Steps:**
1. Install rclone (included in tools/rclone.exe)
2. Configure Google Drive remote
3. Test connection
4. Map client folders

**Time Required:** 10-15 minutes
**Reference:** [RCLONE_SETUP_INSTRUCTIONS.md](RCLONE_SETUP_INSTRUCTIONS.md)

---

### Automation System

**Why:** Automatically convert and upload files when created

**Options:**
1. **Windows Task Scheduler** (Recommended) - Auto-start on login
2. **Manual Start** - Simple, for testing
3. **Startup Folder** - Quick setup
4. **Windows Service** - Enterprise deployment

**Time Required:** 15-30 minutes
**Reference:** [AUTOMATIC_CONVERSION_SETUP_GUIDE.md](AUTOMATIC_CONVERSION_SETUP_GUIDE.md)

---

## Troubleshooting

### Common Issues

#### Installation Errors
**Problem:** Dependencies fail to install
**Solution:**
```bash
# Verbose installation for debugging
python scripts/install/install.py --verbose

# Check individual components
python scripts/install/install.py --test-components
```

#### Permission Errors
**Problem:** Cannot access files or folders
**Solution:**
- Windows: Run Command Prompt as Administrator
- Check file ownership and permissions

#### Google Drive Not Working
**Problem:** Files not uploading to Google Drive
**Solution:**
```bash
# Reconfigure rclone
python scripts/gdrive_upload.py setup --interactive

# Test connection
rclone lsd googledrive:
```

#### Automation Not Triggering
**Problem:** Files not automatically processing
**Solution:**
- Ensure file system watcher is running
- Check logs: `logs/file_system_watcher.log`
- Restart watcher service

**Reference:** [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md) - Troubleshooting Section

---

## Command Quick Reference

### System Maintenance
```bash
# Error statistics
python scripts/error_handler.py --stats 7

# Generate style guide
python scripts/validate_british_english.py --generate-guide --report=style_guide.md

# Installation test
python scripts/install/install.py --test-only
```

### Document Processing
```bash
# Convert markdown to DOCX
python scripts/md_to_docx.py document.md --style=professional

# Upload to Google Drive
python scripts/gdrive_upload.py upload document.docx --client=example_com_au
```

### Automation Control
```bash
# Start file system watcher
python scripts/automation/file_system_watcher.py --monitor

# Stop watcher (Ctrl+C)

# Check watcher status
tail -f logs/file_system_watcher.log
```

**Full Command Reference:** [QUICK_REFERENCE_AUTOMATION.md](QUICK_REFERENCE_AUTOMATION.md)

---

## Best Practices

### 1. Project Organization
✅ Always use standardized client folder structure
✅ Complete research phases before content creation
✅ Use descriptive file names
✅ Include README.md in each client folder

### 2. Content Creation
✅ Write in Markdown for automatic processing
✅ Use British English spelling throughout
✅ Include citations for all statistics
✅ Follow heading hierarchy (H1, H2, H3)

### 3. Quality Management
✅ Run validation scripts regularly
✅ Review error logs weekly
✅ Use auto-correction for British English
✅ Verify research completion before content

### 4. System Maintenance
✅ Update dependencies monthly
✅ Review automation logs weekly
✅ Backup client data regularly
✅ Test automation after changes

**Reference:** [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md) - Best Practices Section

---

## Getting Help

### Documentation Resources

1. **Quick Issues:** Check [QUICK_REFERENCE_AUTOMATION.md](QUICK_REFERENCE_AUTOMATION.md)
2. **Setup Problems:** Review setup guide for specific component
3. **Historical Context:** See [Archive](../archive/README.md) for past issues
4. **System Logs:** Check `logs/` directory for error details

### Log Locations
- **Automation:** `logs/automation_orchestrator.log`
- **File Watcher:** `logs/file_system_watcher.log`
- **Google Drive:** `logs/gdrive_uploads.log`
- **Client Activity:** `clients/{client}/automation_activity.json`

### Command Help
```bash
# Script-specific help
python scripts/[script_name].py --help

# System test
python scripts/install/install.py --test

# Error statistics
python scripts/error_handler.py --stats 30
```

---

## Related Documentation

- **System Overview:** [README_CLEAN_SYSTEM.md](../../README_CLEAN_SYSTEM.md) (root)
- **Agent Configuration:** [CLAUDE.md](../../CLAUDE.md) (root)
- **AI Instructions:** [../for_ai/README.md](../for_ai/README.md)
- **Historical Archive:** [../archive/README.md](../archive/README.md)

---

## Next Steps

### For New Users
1. ✅ Read [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md)
2. ✅ Complete installation
3. ✅ Create first client project
4. ✅ Set up Google Drive (optional)
5. ✅ Enable automation (optional)

### For Experienced Users
1. ✅ Reference [QUICK_REFERENCE_AUTOMATION.md](QUICK_REFERENCE_AUTOMATION.md) for commands
2. ✅ Review [USER_MANUAL.md](USER_MANUAL.md) for advanced features
3. ✅ Configure custom automation workflows

---

**For AI/Agent operational details, see:** [AI Instructions](../for_ai/README.md)