# Quick Start Guide - Bigger Boss System

**5-Minute Setup & Operation Reference**

---

## Initial Setup (One-Time)

### 1. Install Dependencies

```bash
pip install watchdog pandoc pypandoc python-docx python-decouple asyncio
```

### 2. Create Logs Directory

```bash
mkdir "C:\Apps\Agents\Bigger Boss\bigger-boss\logs"
```

### 3. Configure RClone

```bash
rclone config
```

Follow prompts:
- Name: `googledrive`
- Storage: `drive` (Google Drive)
- Scope: `1` (Full access)
- Configure as Shared Drive: `y`
- Select your Shared Drive from list

---

## Daily Operation

### Start Automatic Mode

```bash
# Start file system watcher
python scripts/automation/file_system_watcher.py --start
```

**That's it!** The system now automatically:
- Monitors for new client files
- Verifies compliance
- Converts to .docx
- Uploads to Google Drive

---

## Manual Processing

### Process a Specific Client

```bash
python scripts/emergency_automation_fix.py --client=example_com_au
```

---

## Verification

### Check System Status

```bash
# Verify watcher is running
python scripts/automation/file_system_watcher.py --status

# Check client compliance
python scripts/pre_delivery_audit.py clients/example_com_au

# Verify Google Drive sync
rclone lsl googledrive:example_com_au/
```

---

## Common Commands

### File System Watcher

```bash
# Start
python scripts/automation/file_system_watcher.py --start

# Check status
python scripts/automation/file_system_watcher.py --status

# Stop
python scripts/automation/file_system_watcher.py --stop
```

### Manual Workflows

```bash
# Complete workflow for client
python scripts/emergency_automation_fix.py --client={domain}

# Audit only
python scripts/pre_delivery_audit.py clients/{domain}

# Convert only
python scripts/convert_my_docs.py --client={domain}

# Upload only
python scripts/gdrive_upload.py folder --client={domain}
```

### Monitoring

```bash
# View live logs (Windows PowerShell)
Get-Content logs/automation_orchestrator.log -Wait -Tail 20

# View live logs (if tail available)
tail -f logs/automation_orchestrator.log
```

---

## Quick Troubleshooting

### Issue: Watcher won't start

```bash
pip install watchdog
python scripts/automation/file_system_watcher.py --start
```

### Issue: RClone not working

```bash
rclone config show googledrive
rclone lsd googledrive:
```

If config missing, run `rclone config` and set up "googledrive" remote.

### Issue: Files not uploading

```bash
# Test RClone connection
rclone lsd googledrive:

# Manually upload client
python scripts/gdrive_upload.py folder --client={domain}
```

### Issue: Missing files for client

```bash
# Run emergency fix to generate missing files
python scripts/emergency_automation_fix.py --client={domain}
```

---

## System Health Check

Run these commands to verify system is operational:

```bash
# 1. Check watcher status
python scripts/automation/file_system_watcher.py --status

# 2. Test workflow
python scripts/emergency_automation_fix.py --test

# 3. Verify RClone
rclone lsd googledrive:

# 4. Check recent logs
tail -n 20 logs/automation_orchestrator.log
```

All commands should complete without errors.

---

## Key File Locations

```
C:\Apps\Agents\Bigger Boss\bigger-boss\

clients/{domain}/                    # Client project folders
├── strategy/                        # Strategic documents
├── research/                        # Research & analysis
├── content/                         # Content strategies
├── technical/                       # Technical audits
└── implementation/                  # Execution tracking

scripts/
├── automation/
│   ├── file_system_watcher.py      # Auto-monitoring
│   └── workflow_orchestrator.py    # Workflow execution
├── pre_delivery_audit.py           # Compliance checking
├── convert_my_docs.py              # .md to .docx conversion
├── gdrive_upload.py                # Google Drive uploads
└── emergency_automation_fix.py     # Manual workflow trigger

logs/
├── file_system_watcher.log         # Watcher activity
├── automation_orchestrator.log     # Workflow execution
└── client_activity/                # Per-client tracking
```

---

## Expected Output - Successful Workflow

When automation runs successfully, you'll see:

```
🔄 Starting automation workflow for: example_com_au

Phase 1: Pre-delivery Audit
✅ 15 of 15 mandatory files present (100% compliant)

Phase 2: Document Conversion
✅ Converted 15 markdown files to .docx format

Phase 3: Google Drive Upload
✅ Uploaded 15 .docx files to googledrive:example_com_au/

Phase 4: Activity Tracking
✅ Recorded automation completion

🎉 Workflow completed successfully!
Duration: 45 seconds
```

---

## Getting Help

**For detailed instructions, see:**
- **Full User Manual**: `instructions/for_users/USER_MANUAL.md`
- **AI System Documentation**: `instructions/for_ai/SYSTEM_OPERATION_GUIDE.md`

**Log files for troubleshooting:**
- `logs/file_system_watcher.log`
- `logs/automation_orchestrator.log`
- `logs/client_activity/{client}_automation_activity.json`

---

**This quick reference covers 95% of daily operations. For advanced configuration and troubleshooting, refer to the full USER_MANUAL.md.**