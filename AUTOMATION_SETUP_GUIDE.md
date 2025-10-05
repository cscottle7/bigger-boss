# Bigger Boss Automation System - Setup Guide

## What This System Does

The automation system monitors your `clients/` folder and automatically:

1. **Detects** new or modified `.md` files
2. **Generates** missing project files (PROJECT_OVERVIEW.md, README.md, etc.)
3. **Converts** markdown files to `.docx` format
4. **Uploads** to Google Drive `SEO/Content` folder via RClone
5. **Tracks** client activity and maintains automation logs

## Quick Start (First Time Setup)

### Option 1: Auto-Start on Login (Recommended)

1. **Right-click** `scripts/setup_auto_start.bat`
2. Select **"Run as administrator"**
3. Follow the prompts
4. The watcher will start automatically whenever you log in

### Option 2: Manual Start (Run When Needed)

Simply double-click: `scripts/quick_start_automation.bat`

The watcher runs in the foreground - close the window to stop it.

## Management Scripts

### Check Status
**File:** `scripts/check_automation_status.bat`

Shows:
- Is scheduled task configured?
- Is watcher currently running?
- Is RClone configured?
- Recent log activity
- Component status

### Remove Auto-Start
**File:** `scripts/remove_auto_start.bat`

Removes the scheduled task (requires admin).

## How It Works

```
Content Created in clients/
         ↓
File System Watcher Detects Change
         ↓
Workflow Orchestrator Triggers
         ↓
┌────────────────────────────────┐
│ 1. Pre-Delivery Audit          │
│    - Check required files      │
│    - Auto-generate missing     │
└────────────────────────────────┘
         ↓
┌────────────────────────────────┐
│ 2. Document Conversion         │
│    - Convert .md → .docx       │
│    - Preserve formatting       │
└────────────────────────────────┘
         ↓
┌────────────────────────────────┐
│ 3. Google Drive Upload         │
│    - Use RClone sync           │
│    - Upload to SEO/Content     │
│    - Organize by client        │
└────────────────────────────────┘
         ↓
┌────────────────────────────────┐
│ 4. Activity Tracking           │
│    - Log automation activity   │
│    - Update client records     │
└────────────────────────────────┘
```

## File Locations

### Automation Scripts
- **Main watcher:** `scripts/automation/file_system_watcher.py`
- **Orchestrator:** `scripts/automation/workflow_orchestrator.py`
- **Quick start:** `scripts/quick_start_automation.bat`

### Configuration
- **Environment:** `.env` (API keys, RClone config)
- **RClone config:** `~/.config/rclone/rclone.conf`

### Logs
- **Watcher log:** `logs/file_system_watcher.log`
- **Orchestrator log:** `logs/automation_orchestrator.log`
- **Client activity:** `clients/{domain}/automation_activity.json`

## Monitoring & Troubleshooting

### View Real-Time Logs

**Windows PowerShell:**
```powershell
Get-Content logs\file_system_watcher.log -Wait -Tail 20
```

**Git Bash:**
```bash
tail -f logs/file_system_watcher.log
```

### Check If Watcher Is Running

```bash
tasklist | findstr python
```

Look for `python3.13.exe` processes.

### Manually Trigger Upload for Specific Client

```bash
python scripts/automation/workflow_orchestrator.py --client="clientdomain_com_au" --full-audit
```

### Test RClone Connection

```bash
rclone lsd googledrive:SEO/Content
```

Should show all client folders in Google Drive.

## Common Issues

### Issue: Watcher Not Starting

**Solution:**
1. Run `scripts/check_automation_status.bat`
2. Check if Python dependencies installed:
   ```bash
   pip install watchdog python-decouple
   ```
3. Check logs for errors: `logs/file_system_watcher.log`

### Issue: Files Not Uploading to Google Drive

**Solution:**
1. Check RClone configuration:
   ```bash
   rclone listremotes
   ```
   Should show: `googledrive:`

2. Test manual upload:
   ```bash
   rclone copy "clients/test_client_com_au" "googledrive:SEO/Content/Test Client" -v
   ```

3. Check RClone credentials haven't expired:
   ```bash
   rclone config reconnect googledrive:
   ```

### Issue: Scheduled Task Won't Create

**Solution:**
1. Ensure running `setup_auto_start.bat` as **Administrator**
2. Check Windows Task Scheduler manually:
   - Open Task Scheduler
   - Look for "Bigger Boss File Watcher"
3. Check for group policy restrictions

## Manual Commands

### Start Watcher (Foreground)
```bash
python scripts/automation/file_system_watcher.py --monitor
```

### Test with Specific Client
```bash
python scripts/automation/file_system_watcher.py --test-client=capitalsmiles_com_au
```

### Use Polling Mode (If Watchdog Fails)
```bash
python scripts/automation/file_system_watcher.py --monitor --polling-only
```

### Run Full Audit for Client
```bash
python scripts/automation/workflow_orchestrator.py --client=lunadigitalmarketing_com_au --full-audit
```

## Scheduled Task Details

**Task Name:** `Bigger Boss File Watcher`

**Trigger:** User logon (runs when you log in to Windows)

**Action:** Runs `scripts/quick_start_automation.bat`

**Permissions:** Highest available (runs with your admin privileges)

### Manage via Command Line

**Query task:**
```cmd
schtasks /query /tn "Bigger Boss File Watcher" /fo list
```

**Run task now:**
```cmd
schtasks /run /tn "Bigger Boss File Watcher"
```

**Delete task:**
```cmd
schtasks /delete /tn "Bigger Boss File Watcher" /f
```

## What Gets Uploaded

The system uploads **all files** from `clients/{domain}/` to `googledrive:SEO/Content/{Client Name}/`

This includes:
- ✅ All `.md` files
- ✅ All `.docx` files (converted from .md)
- ✅ All `.json` files (tracking data)
- ✅ All subdirectories (`research/`, `content/`, `strategy/`, etc.)

## Performance Notes

- **Debouncing:** 5 seconds (prevents duplicate processing on rapid saves)
- **Polling interval:** 10 seconds (when using polling mode)
- **Upload batch size:** All changed files in single client folder
- **Log rotation:** Logs are appended (manual cleanup needed)

## Next Steps After Setup

1. ✅ Run `scripts/setup_auto_start.bat` (as admin)
2. ✅ Run `scripts/check_automation_status.bat` to verify
3. ✅ Create or edit a test file in `clients/test_client_com_au/`
4. ✅ Check `logs/file_system_watcher.log` for activity
5. ✅ Verify upload in Google Drive `SEO/Content` folder
6. ✅ Review automation workflow with real client content

## Support

If automation isn't working:
1. Run `scripts/check_automation_status.bat`
2. Check `logs/file_system_watcher.log` for errors
3. Verify RClone connection: `rclone listremotes`
4. Test manual workflow: `python scripts/automation/workflow_orchestrator.py --test-client=test_client_com_au`
