# Automatic Markdown to DOCX Conversion - Setup Guide

## Problem Summary

The automation system has all components functional, but **automatic conversion doesn't happen because the file system watcher is not running as a background service**.

When you manually trigger it (as in the Australian Dental Specialists test), it works perfectly. But for automatic conversion when files are naturally created, the watcher must be continuously monitoring the `clients/` folder.

## Root Cause

**The file system watcher requires manual start** - there is no background service or auto-start mechanism configured to keep it running continuously.

---

## Solution Options

### Option 1: Windows Task Scheduler (RECOMMENDED FOR PRODUCTION)

This creates a Windows background service that starts automatically when your computer boots.

#### Setup Steps:

1. **Create PowerShell Start Script**

   Create `C:\Apps\Agents\Bigger Boss\bigger-boss\scripts\start_watcher_service.ps1`:
   ```powershell
   # Start File System Watcher as Background Service
   Set-Location "C:\Apps\Agents\Bigger Boss\bigger-boss"

   # Log file location
   $logFile = "logs\watcher_service.log"

   # Start the watcher
   python scripts\automation\file_system_watcher.py --monitor --log-level=INFO 2>&1 | Out-File -FilePath $logFile -Append
   ```

2. **Create Batch File Wrapper**

   Create `C:\Apps\Agents\Bigger Boss\bigger-boss\scripts\start_watcher.bat`:
   ```batch
   @echo off
   cd /d "C:\Apps\Agents\Bigger Boss\bigger-boss"
   python scripts\automation\file_system_watcher.py --monitor
   ```

3. **Configure Windows Task Scheduler**

   a. Open **Task Scheduler** (search in Windows Start menu)

   b. Click **"Create Task"** (not "Create Basic Task")

   c. **General Tab**:
      - Name: `Bigger Boss File Watcher Service`
      - Description: `Monitors client folders for automatic markdown to DOCX conversion`
      - User account: Your Windows account
      - ✅ Run only when user is logged on
      - ⚠️ DO NOT check "Run with highest privileges" (causes permission issues)

   d. **Triggers Tab**:
      - Click "New..."
      - Begin the task: **At log on**
      - Delay task for: **1 minute**
      - ✅ Enabled

   e. **Actions Tab**:
      - Click "New..."
      - Action: **Start a program**
      - Program/script: `C:\Windows\System32\cmd.exe`
      - Add arguments: `/c "cd /d "C:\Apps\Agents\Bigger Boss\bigger-boss" && python scripts\automation\file_system_watcher.py --monitor"`
      - Start in: `C:\Apps\Agents\Bigger Boss\bigger-boss`

   f. **Conditions Tab**:
      - ❌ UNCHECK "Start the task only if the computer is on AC power"
      - ❌ UNCHECK "Stop if the computer switches to battery power"

   g. **Settings Tab**:
      - ✅ Allow task to be run on demand
      - ✅ Run task as soon as possible after a scheduled start is missed
      - If the task fails, restart every: **5 minutes**
      - Attempt to restart up to: **3 times**
      - Stop the task if it runs longer than: **Do not stop**
      - If the running task does not end when requested: **Do not stop**

4. **Test the Scheduled Task**

   - Right-click the task and select **"Run"**
   - Check `logs\file_system_watcher.log` to verify it started
   - Create a test .md file in `clients\test_client\test.md`
   - Verify automation workflow triggers

5. **Verify Continuous Operation**

   ```powershell
   # Check if process is running
   Get-Process python | Where-Object {$_.CommandLine -like "*file_system_watcher*"}

   # View recent log entries
   Get-Content "logs\file_system_watcher.log" -Tail 20
   ```

---

### Option 2: Manual Start (Quick Testing)

For immediate testing or occasional use:

```bash
# Start in foreground (see output in terminal)
python scripts\automation\file_system_watcher.py --monitor

# Start in background (Windows)
start /B python scripts\automation\file_system_watcher.py --monitor

# Start with polling mode (more compatible but slower)
python scripts\automation\file_system_watcher.py --monitor --polling-only
```

**Keep the terminal window open** - closing it will stop the watcher.

---

### Option 3: Startup Folder (Simple Auto-Start)

For basic auto-start when you log in:

1. Create shortcut to `scripts\start_watcher.bat`
2. Press `Win+R`, type `shell:startup`, press Enter
3. Copy the shortcut to the Startup folder
4. Restart computer to test

**Downside**: Terminal window will appear on startup (can be minimized).

---

### Option 4: Python Background Service (Advanced)

Create a proper Windows service using `pywin32`:

```bash
# Install pywin32
pip install pywin32

# Register as service
python scripts\automation\install_service.py install
python scripts\automation\install_service.py start
```

**Note**: Requires administrative privileges and additional setup.

---

## How to Know It's Working

### 1. Check Process is Running

**PowerShell**:
```powershell
Get-Process python | Where-Object {$_.CommandLine -like "*file_system_watcher*"}
```

**Task Manager**:
- Open Task Manager (Ctrl+Shift+Esc)
- Look for Python process with command line containing "file_system_watcher.py"

### 2. Monitor Log Files

```powershell
# Real-time log monitoring
Get-Content "logs\file_system_watcher.log" -Wait -Tail 20

# Check recent activity
Get-Content "logs\automation_orchestrator.log" -Tail 50
```

### 3. Test with Real File

```bash
# Create test markdown file
echo "# Test Content" > clients\test_client\test_file.md

# Check logs within 10 seconds - should see:
# - File detection message
# - Workflow orchestrator execution
# - Pre-delivery audit results
# - Document conversion
# - Google Drive upload
```

### 4. Expected Log Output

When working correctly, you should see:
```
2025-09-30 14:23:15 - file_system_watcher - INFO - Started watchdog monitoring of: C:\Apps\Agents\Bigger Boss\bigger-boss\clients
2025-09-30 14:23:15 - file_system_watcher - INFO - File system monitoring active - Press Ctrl+C to stop

[When .md file created:]
2025-09-30 14:25:30 - file_system_watcher - INFO - New client content detected: clients\client_name\file.md
2025-09-30 14:25:30 - file_system_watcher - INFO - Triggering automation workflow for: clients\client_name\file.md
2025-09-30 14:25:35 - workflow_orchestrator - INFO - Starting complete automation workflow
2025-09-30 14:25:40 - workflow_orchestrator - INFO - Phase 1: Pre-delivery audit completed
2025-09-30 14:25:45 - workflow_orchestrator - INFO - Phase 2: Document conversion completed - 15 files converted
2025-09-30 14:25:50 - workflow_orchestrator - INFO - Phase 3: Google Drive upload completed
2025-09-30 14:25:51 - workflow_orchestrator - INFO - Complete automation workflow succeeded in 21.5s
```

---

## Troubleshooting

### Issue: "Watcher starts but immediately stops"

**Cause**: Python path or dependencies missing

**Solution**:
```bash
# Install required dependencies
pip install watchdog decouple

# Test watcher manually first
python scripts\automation\file_system_watcher.py --test-client=test_client
```

### Issue: "Files detected but workflow doesn't run"

**Cause**: Workflow orchestrator path incorrect or missing dependencies

**Solution**:
```bash
# Test orchestrator manually
python scripts\automation\workflow_orchestrator.py --trigger-file="clients\test\test.md"

# Check dependencies
pip install watchdog decouple
```

### Issue: "Conversion works manually but not automatically"

**Cause**: File system watcher not running

**Solution**:
```powershell
# Check if watcher is running
Get-Process python | Where-Object {$_.CommandLine -like "*file_system_watcher*"}

# If not running, start it
python scripts\automation\file_system_watcher.py --monitor
```

### Issue: "Permission denied" errors

**Cause**: Task Scheduler running with wrong permissions

**Solution**:
- Edit task in Task Scheduler
- Change "Run only when user is logged on"
- UNCHECK "Run with highest privileges"
- Use your user account, not SYSTEM

### Issue: "Files created but no .docx appears"

**Cause**: Converter dependencies missing

**Solution**:
```bash
# Install conversion tools
pip install pandoc pypandoc python-docx

# Test converter
python scripts\convert_my_docs.py --test
```

---

## Monitoring & Maintenance

### Daily Checks

```powershell
# Quick health check
Get-Process python | Where-Object {$_.CommandLine -like "*file_system_watcher*"}
Get-Content "logs\file_system_watcher.log" -Tail 5
```

### Weekly Review

```bash
# Review automation activity
cat logs\automation_orchestrator.log | grep "workflow succeeded" | wc -l

# Check for errors
cat logs\automation_orchestrator.log | grep "ERROR"
```

### Monthly Maintenance

1. Archive old log files
2. Review and clean up test client folders
3. Update dependencies: `pip install --upgrade watchdog decouple`
4. Verify Task Scheduler task still active

---

## Verification Checklist

Before considering setup complete, verify:

- [ ] File system watcher starts without errors
- [ ] Process remains running for at least 5 minutes
- [ ] Creating test .md file triggers workflow
- [ ] .docx files appear within 30 seconds of .md creation
- [ ] Logs show successful workflow completion
- [ ] Google Drive receives uploaded files
- [ ] Task Scheduler task is enabled and running
- [ ] System survives reboot (auto-start works)

---

## Performance Expectations

**Normal Operation**:
- Detection latency: 1-5 seconds
- Full workflow time: 15-45 seconds (depends on file count)
- Memory usage: 50-100 MB
- CPU usage: < 5% idle, 10-30% during conversion

**When to Investigate**:
- Detection latency > 30 seconds
- Workflow time > 2 minutes
- Memory usage > 500 MB
- Frequent "ERROR" entries in logs

---

## Quick Reference Commands

```bash
# Start watcher (foreground)
python scripts\automation\file_system_watcher.py --monitor

# Start watcher (background - Windows)
start /B python scripts\automation\file_system_watcher.py --monitor

# Test with specific client
python scripts\automation\file_system_watcher.py --test-client=client_domain

# Manual workflow trigger
python scripts\automation\workflow_orchestrator.py --trigger-file="path\to\file.md"

# Check if running
Get-Process python | Where-Object {$_.CommandLine -like "*file_system_watcher*"}

# View live logs
Get-Content "logs\file_system_watcher.log" -Wait -Tail 20

# Stop watcher
Get-Process python | Where-Object {$_.CommandLine -like "*file_system_watcher*"} | Stop-Process
```

---

## Next Steps

1. **Choose implementation option** (Task Scheduler recommended)
2. **Follow setup steps** for chosen option
3. **Test with real client file** to verify automation
4. **Monitor logs** for first few days to ensure stability
5. **Set up monitoring alerts** (optional) for production use

---

**Status After Setup**: ✅ Automatic conversion will work whenever:
- File system watcher is running (check with `Get-Process`)
- New .md files are created in `clients/` folder
- System has required dependencies installed
- No file permission issues

**Remember**: The watcher MUST be running for automation to work. If your computer restarts, ensure Task Scheduler restarts the watcher automatically.