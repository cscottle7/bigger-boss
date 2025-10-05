# Bigger Boss System - User Manual

**Version**: 1.0
**Last Updated**: 30 September 2025
**Audience**: System Operators & End Users
**Purpose**: Complete setup, operation, and maintenance guide

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Initial Setup](#initial-setup)
3. [RClone Configuration](#rclone-configuration)
4. [Starting the Automation System](#starting-the-automation-system)
5. [Manual Workflow Triggering](#manual-workflow-triggering)
6. [Monitoring & Verification](#monitoring--verification)
7. [Troubleshooting](#troubleshooting)
8. [Maintenance & Updates](#maintenance--updates)

---

## System Overview

### What This System Does

The Bigger Boss system is an **automated marketing content generation and delivery platform** designed for Australian businesses. It provides:

✅ **Automated Content Creation**: AI agents create comprehensive marketing strategies, research documents, and content plans
✅ **Quality Assurance**: Multi-agent feedback loops ensure high-quality, compliant deliverables
✅ **Document Conversion**: Automatically converts markdown files to .docx format
✅ **Google Drive Integration**: Uploads completed deliverables to client folders on Google Shared Drive
✅ **Compliance Verification**: Ensures all mandatory files are present and meet SOP standards

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   AI AGENT LAYER                             │
│  (master_orchestrator, glenn, specialist agents)            │
│  Creates research, strategies, content plans                │
└──────────────────┬──────────────────────────────────────────┘
                   │ Creates .md files
                   ▼
┌─────────────────────────────────────────────────────────────┐
│              FILE SYSTEM WATCHER                             │
│  (file_system_watcher.py)                                    │
│  Monitors clients/ folder for new files                     │
└──────────────────┬──────────────────────────────────────────┘
                   │ Triggers on .md creation
                   ▼
┌─────────────────────────────────────────────────────────────┐
│            WORKFLOW ORCHESTRATOR                             │
│  (workflow_orchestrator.py)                                  │
│  Executes: audit → convert → upload → track                 │
└──────────────────┬──────────────────────────────────────────┘
                   │
        ┌──────────┴───────────┬──────────────────┐
        ▼                      ▼                  ▼
┌──────────────┐      ┌──────────────┐    ┌──────────────┐
│ PRE-DELIVERY │      │  MARKDOWN    │    │ GOOGLE DRIVE │
│    AUDIT     │      │  TO .DOCX    │    │   UPLOAD     │
│              │      │  CONVERSION  │    │              │
│ Generates    │      │              │    │ Uploads to   │
│ missing files│      │ Converts all │    │ client folder│
└──────────────┘      └──────────────┘    └──────────────┘
```

### Key File Locations

```
C:\Apps\Agents\Bigger Boss\bigger-boss\
├── clients/                          # All client project folders
│   └── {client_domain}/              # Individual client folder
│       ├── strategy/                 # Strategic planning documents
│       ├── research/                 # Market intelligence
│       ├── content/                  # Content strategies
│       ├── technical/                # Technical audits
│       └── implementation/           # Execution tracking
│
├── scripts/                          # Automation scripts
│   ├── automation/
│   │   ├── file_system_watcher.py   # Monitors for new files
│   │   └── workflow_orchestrator.py # Executes automation chain
│   ├── pre_delivery_audit.py        # Compliance verification
│   ├── convert_my_docs.py           # Markdown to .docx conversion
│   ├── gdrive_upload.py             # Google Drive uploads
│   └── emergency_automation_fix.py  # Manual workflow trigger
│
├── logs/                             # System logs
│   ├── file_system_watcher.log      # Watcher activity log
│   ├── automation_orchestrator.log  # Workflow execution log
│   └── client_activity/             # Per-client activity tracking
│
├── .claude/                          # AI agent configurations
│   └── agents/
│       ├── master_orchestrator.md   # Primary content orchestrator
│       └── glenn.md                 # Request routing agent
│
└── instructions/                     # Documentation hub
    ├── for_ai/                      # AI agent instructions
    └── for_users/                   # User manuals (you are here)
```

---

## Initial Setup

### Prerequisites

1. **Python 3.8+** installed
2. **RClone** installed and configured (see next section)
3. **Required Python packages** installed

### Step 1: Install Python Dependencies

Open Command Prompt or PowerShell in the project directory and run:

```bash
pip install watchdog pandoc pypandoc python-docx python-decouple asyncio
```

**Required packages:**
- `watchdog` - File system monitoring
- `pandoc` / `pypandoc` - Document conversion
- `python-docx` - .docx file creation
- `python-decouple` - Configuration management
- `asyncio` - Asynchronous processing

### Step 2: Create Logs Directory

```bash
mkdir "C:\Apps\Agents\Bigger Boss\bigger-boss\logs"
```

### Step 3: Verify Directory Structure

Ensure this structure exists:

```bash
C:\Apps\Agents\Bigger Boss\bigger-boss\
├── clients/        # Should exist
├── scripts/        # Should exist with automation/ subfolder
└── logs/           # Just created
```

### Step 4: Test System Components

```bash
# Test pre-delivery audit
python scripts/pre_delivery_audit.py --test

# Test document conversion
python scripts/convert_my_docs.py --test

# Expected output: No errors, confirmation messages
```

---

## RClone Configuration

### What is RClone?

RClone is a command-line tool for syncing files to cloud storage services. This system uses it to automatically upload completed deliverables to your Google Shared Drive.

### Step 1: Install RClone

**Option A: Download and extract**
1. Go to https://rclone.org/downloads/
2. Download Windows version
3. Extract to a permanent location (e.g., `C:\rclone\`)
4. Add to system PATH

**Option B: Using package manager**
```bash
winget install Rclone.Rclone
```

### Step 2: Configure Google Shared Drive

**Run the configuration wizard:**

```bash
rclone config
```

**Follow these steps:**

```
n) New remote
name> googledrive

Storage> drive
(Select "Google Drive")

client_id> [Press Enter for default]
client_secret> [Press Enter for default]

scope> 1
(Select "Full access")

root_folder_id> [Press Enter]
service_account_file> [Press Enter]

Edit advanced config? n

Use web browser to automatically authenticate? y
(Browser opens - log in to Google account)

Configure as Shared Drive? y

Shared Drive number> [Select your Shared Drive from list]

Configuration complete? y

Quit config? q
```

### Step 3: Verify RClone Setup

```bash
# List Shared Drive contents
rclone lsd googledrive:

# Expected output: List of folders in your Shared Drive
```

### Step 4: Test Upload Functionality

```bash
# Test upload to Shared Drive
python scripts/gdrive_upload.py --test

# Expected output:
# ✅ RClone configuration verified
# ✅ Google Shared Drive accessible
# ✅ Test upload successful
```

**If test fails, check:**
- RClone configuration name matches "googledrive"
- You selected Shared Drive during configuration
- You have write permissions to the Shared Drive

---

## Starting the Automation System

### Automatic Mode (Recommended)

**The file system watcher monitors for new files and triggers automation automatically.**

#### Start the Watcher

```bash
# Start file system watcher in background
python scripts/automation/file_system_watcher.py --start
```

**Expected output:**
```
✅ File system watcher started successfully
📁 Monitoring: C:\Apps\Agents\Bigger Boss\bigger-boss\clients
📝 Log file: C:\Apps\Agents\Bigger Boss\bigger-boss\logs\file_system_watcher.log
🔄 Process ID: 12345

The watcher will now automatically trigger workflows when new .md files are created.
```

#### Verify Watcher is Running

```bash
# Check watcher status
python scripts/automation/file_system_watcher.py --status
```

**Expected output:**
```
✅ File system watcher is running
📊 Process ID: 12345
⏰ Running time: 2 hours, 34 minutes
📁 Monitored path: C:\Apps\Agents\Bigger Boss\bigger-boss\clients
```

#### Stop the Watcher

```bash
# Stop file system watcher
python scripts/automation/file_system_watcher.py --stop
```

### How Automatic Mode Works

1. **Agent Creates File**: AI agent writes a new .md file to `clients/{client_domain}/`
2. **Watcher Detects**: File system watcher detects the new file within 1 second
3. **Workflow Triggers**: Watcher executes workflow_orchestrator.py
4. **Automation Chain Executes**:
   - **Phase 1**: Pre-delivery audit (verifies compliance, generates missing files)
   - **Phase 2**: Markdown to .docx conversion (converts all .md files)
   - **Phase 3**: Google Drive upload (uploads .docx files to client folder)
   - **Phase 4**: Activity tracking (records automation completion)
5. **Results Logged**: All activities logged to `logs/automation_orchestrator.log`

---

## Manual Workflow Triggering

### When to Use Manual Mode

Use manual triggering when:
- File system watcher is not running
- You need to reprocess an existing client
- Testing automation workflow
- Troubleshooting issues

### Emergency Automation Fix Script

**Primary tool for manual workflow execution:**

```bash
python scripts/emergency_automation_fix.py --client=example_com_au
```

### Command Options

#### Trigger Workflow for Specific Client

```bash
# Process a specific client domain
python scripts/emergency_automation_fix.py --client=drgraemebrown_com_au
```

**What this does:**
1. Finds the client folder at `clients/drgraemebrown_com_au/`
2. Runs pre-delivery audit to check compliance
3. Generates any missing mandatory files
4. Converts all .md files to .docx format
5. Uploads .docx files to Google Drive
6. Records activity in client activity log

**Expected output:**
```
🔄 Starting automation workflow for: drgraemebrown_com_au

Phase 1: Pre-delivery Audit
✅ 15 of 15 mandatory files present (100% compliant)
✅ Word count compliance: 100%

Phase 2: Document Conversion
✅ Converted 15 markdown files to .docx format

Phase 3: Google Drive Upload
✅ Uploaded 15 .docx files to googledrive:drgraemebrown_com_au/

Phase 4: Activity Tracking
✅ Recorded automation completion

🎉 Workflow completed successfully!
```

#### Test Automation Workflow

```bash
# Test with a sample client
python scripts/emergency_automation_fix.py --test
```

Creates a test client folder and verifies all automation phases work correctly.

#### Enable File System Watcher

```bash
# Start the file system watcher
python scripts/emergency_automation_fix.py --enable-watcher
```

Starts the background monitoring process for automatic workflow triggering.

### Individual Component Execution

**If you need to run specific phases only:**

#### Run Pre-Delivery Audit Only

```bash
python scripts/pre_delivery_audit.py clients/drgraemebrown_com_au
```

Checks compliance and generates missing files without conversion/upload.

#### Run Document Conversion Only

```bash
python scripts/convert_my_docs.py --client=drgraemebrown_com_au
```

Converts .md to .docx without audit or upload.

#### Run Google Drive Upload Only

```bash
python scripts/gdrive_upload.py folder --client=drgraemebrown_com_au
```

Uploads .docx files to Google Drive without audit or conversion.

---

## Monitoring & Verification

### Real-Time Log Monitoring

**View live automation activity:**

```bash
# Monitor file system watcher log
tail -f "C:\Apps\Agents\Bigger Boss\bigger-boss\logs\file_system_watcher.log"

# Monitor workflow orchestrator log
tail -f "C:\Apps\Agents\Bigger Boss\bigger-boss\logs\automation_orchestrator.log"
```

**For Windows (if tail not available):**

```powershell
Get-Content "C:\Apps\Agents\Bigger Boss\bigger-boss\logs\file_system_watcher.log" -Wait -Tail 20
```

### Client Activity Tracking

**Each client has an activity tracking file:**

```
logs/client_activity/{client_domain}_automation_activity.json
```

**View client activity:**

```bash
cat "logs/client_activity/drgraemebrown_com_au_automation_activity.json"
```

**Example activity log:**

```json
{
  "client_domain": "drgraemebrown_com_au",
  "total_workflows_executed": 3,
  "last_execution": "2025-09-30T09:47:23",
  "workflows": [
    {
      "timestamp": "2025-09-30T09:47:23",
      "trigger_file": "clients/drgraemebrown_com_au/content/comprehensive_content_plan.md",
      "phases": {
        "audit": {
          "success": true,
          "compliance_score": 100,
          "files_generated": 12
        },
        "conversion": {
          "success": true,
          "files_converted": 15
        },
        "upload": {
          "success": true,
          "files_uploaded": 15
        }
      },
      "duration_seconds": 47,
      "status": "completed"
    }
  ]
}
```

### Compliance Verification

**Check client folder compliance:**

```bash
python scripts/pre_delivery_audit.py clients/drgraemebrown_com_au
```

**Expected output:**

```
════════════════════════════════════════════════════════════
  PRE-DELIVERY AUDIT REPORT
  Client: drgraemebrown_com_au
  Date: 2025-09-30 10:15:43
════════════════════════════════════════════════════════════

📋 MANDATORY FILES COMPLIANCE:

✅ 15 of 15 mandatory files present (100.0% compliant)

📊 WORD COUNT COMPLIANCE:

Strategy Documents:
✅ strategy/research_brief.md: 1,234 words (within 800-1,500 range)
✅ strategy/implementation_plan.md: 987 words (within 800-1,500 range)
✅ strategy/current_website_analysis.md: 1,456 words (within 800-1,500 range)

Word Count Compliance: 100%

✅ OVERALL COMPLIANCE: 100%
```

### Google Drive Verification

**Verify files uploaded to Google Drive:**

```bash
# List client folder contents on Google Drive
rclone lsl googledrive:drgraemebrown_com_au/
```

**Expected output:**
```
  1234567 2025-09-30 09:47:23 README.docx
  2345678 2025-09-30 09:47:24 PROJECT_OVERVIEW.docx
  3456789 2025-09-30 09:47:25 research_brief.docx
  ...
```

---

## Troubleshooting

### Common Issues & Solutions

#### Issue 1: File System Watcher Not Starting

**Error:**
```
NameError: name 'FileSystemEventHandler' is not defined
```

**Cause**: watchdog library not installed

**Solution:**
```bash
pip install watchdog
```

---

#### Issue 2: Unicode Encoding Errors

**Error:**
```
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705'
```

**Cause**: Windows console using cp1252 encoding instead of UTF-8

**Solution**: This is handled automatically in updated scripts. If you see this error, the script needs the Unicode fix:

```python
# Add to top of script
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
```

---

#### Issue 3: RClone Configuration Not Found

**Error:**
```
Config file "C:\Users\cscot\AppData\Roaming\rclone\rclone.conf" not found
didn't find section in config file ("googledrive")
```

**Cause**: RClone not configured or configuration name incorrect

**Solution:**
1. Run `rclone config` to configure Google Drive
2. Ensure configuration name is exactly "googledrive"
3. Verify with: `rclone lsd googledrive:`

---

#### Issue 4: Pre-Delivery Audit Failures

**Error:**
```
❌ Only 6 of 15 mandatory files present (40% compliant)
```

**Cause**: Client folder incomplete, automation may not have run

**Solution:**
```bash
# Manually trigger workflow to generate missing files
python scripts/emergency_automation_fix.py --client={client_domain}
```

The pre-delivery audit will automatically generate missing files using templates.

---

#### Issue 5: Document Conversion Failures

**Error:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'pandoc'
```

**Cause**: Pandoc not installed or not in system PATH

**Solution:**
```bash
# Install pandoc
pip install pypandoc

# Or download from https://pandoc.org/installing.html
```

---

#### Issue 6: Logs Directory Missing

**Error:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'logs/automation_orchestrator.log'
```

**Cause**: Logs directory not created

**Solution:**
```bash
mkdir "C:\Apps\Agents\Bigger Boss\bigger-boss\logs"
```

---

#### Issue 7: Permission Denied on File Operations

**Error:**
```
PermissionError: [Errno 13] Permission denied: 'clients/example_com_au/README.md'
```

**Cause**: File open in another program (Word, text editor)

**Solution**: Close all programs that might have the file open, then retry.

---

#### Issue 8: Google Drive Upload Fails

**Error:**
```
Failed to upload clients/example_com_au/README.docx to googledrive:
```

**Cause**: Network issue, permissions issue, or RClone configuration problem

**Solution:**
1. Verify internet connection
2. Test RClone: `rclone lsd googledrive:`
3. Check Shared Drive permissions
4. Retry upload: `python scripts/gdrive_upload.py folder --client=example_com_au`

---

### Diagnostic Commands

**Check system health:**

```bash
# 1. Verify Python packages installed
pip list | grep -E "watchdog|pandoc|python-docx"

# 2. Check file system watcher status
python scripts/automation/file_system_watcher.py --status

# 3. Verify RClone configuration
rclone config show googledrive

# 4. Test complete workflow
python scripts/emergency_automation_fix.py --test

# 5. Check recent logs
tail -n 50 "C:\Apps\Agents\Bigger Boss\bigger-boss\logs\automation_orchestrator.log"
```

---

## Maintenance & Updates

### Daily Monitoring

**Recommended daily checks:**

1. **Verify watcher is running**:
   ```bash
   python scripts/automation/file_system_watcher.py --status
   ```

2. **Review automation logs**:
   ```bash
   tail -n 100 "C:\Apps\Agents\Bigger Boss\bigger-boss\logs\automation_orchestrator.log"
   ```

3. **Check client compliance** (spot-check recent clients):
   ```bash
   python scripts/pre_delivery_audit.py clients/{recent_client}/
   ```

### Weekly Maintenance

1. **Archive old logs** (keep logs under 100MB):
   ```bash
   # Move logs older than 30 days to archive
   # (Create archival script if needed)
   ```

2. **Verify Google Drive sync**:
   ```bash
   rclone check clients/ googledrive: --one-way
   ```

3. **Review client activity tracking**:
   ```bash
   ls -lh logs/client_activity/
   ```

### Monthly Maintenance

1. **Update Python packages**:
   ```bash
   pip install --upgrade watchdog pandoc pypandoc python-docx
   ```

2. **Review system performance**:
   - Average workflow completion time
   - Compliance rates across all clients
   - Error frequency in logs

3. **Update RClone** (if new version available):
   ```bash
   rclone selfupdate
   ```

### System Updates

**When updating automation scripts:**

1. **Stop file system watcher**:
   ```bash
   python scripts/automation/file_system_watcher.py --stop
   ```

2. **Apply updates** (git pull or manual file replacement)

3. **Test updated scripts**:
   ```bash
   python scripts/emergency_automation_fix.py --test
   ```

4. **Restart file system watcher**:
   ```bash
   python scripts/automation/file_system_watcher.py --start
   ```

---

## Quick Reference Commands

### Starting System

```bash
# Start file system watcher (automatic mode)
python scripts/automation/file_system_watcher.py --start

# Check watcher status
python scripts/automation/file_system_watcher.py --status
```

### Manual Workflow Execution

```bash
# Process specific client
python scripts/emergency_automation_fix.py --client={client_domain}

# Run pre-delivery audit only
python scripts/pre_delivery_audit.py clients/{client_domain}

# Convert to .docx only
python scripts/convert_my_docs.py --client={client_domain}

# Upload to Google Drive only
python scripts/gdrive_upload.py folder --client={client_domain}
```

### Monitoring & Verification

```bash
# View live logs
tail -f logs/automation_orchestrator.log

# Check compliance
python scripts/pre_delivery_audit.py clients/{client_domain}

# Verify Google Drive sync
rclone lsl googledrive:{client_domain}/
```

### Troubleshooting

```bash
# Test complete workflow
python scripts/emergency_automation_fix.py --test

# Verify RClone setup
rclone lsd googledrive:

# Check system health
python scripts/automation/file_system_watcher.py --status
```

---

## Getting Help

### Log Files for Troubleshooting

When reporting issues, provide these log files:

1. `logs/file_system_watcher.log` - Watcher activity
2. `logs/automation_orchestrator.log` - Workflow execution
3. `logs/client_activity/{client}_automation_activity.json` - Client-specific activity

### Support Resources

- **System Documentation**: `instructions/` folder
- **AI Agent Instructions**: `instructions/for_ai/`
- **Issue Tracking**: Project issue tracker

---

**This manual provides complete operational guidance for the Bigger Boss automated marketing content system. Follow these procedures to ensure reliable, consistent system operation.**