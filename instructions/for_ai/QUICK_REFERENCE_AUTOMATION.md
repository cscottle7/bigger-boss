# Bigger Boss Automation - Quick Reference Card

## ⚡ Quick Start (30 Seconds)

```bash
cd "C:\Apps\Agents\Bigger Boss\bigger-boss"
python scripts\automation\file_system_watcher.py --monitor
```

**Keep terminal open** - Watcher is now active! 🟢

---

## 🔍 Check if Running

**PowerShell**:
```powershell
.\scripts\check_watcher_status.ps1
```

**Expected Output**:
```
Status: RUNNING ✓
PID: 12345
Memory: 75.5 MB
```

---

## 🎯 Test Automatic Conversion

```bash
# Create test file
echo "# Test Document" > clients\test_client\test.md

# Wait 10 seconds...

# Check for .docx file
dir clients\test_client\test.docx
```

**Success**: File `test.docx` should exist! ✅

---

## 📊 Monitor Activity

**Real-time logs**:
```powershell
Get-Content "logs\file_system_watcher.log" -Wait -Tail 20
```

**Recent activity**:
```powershell
Get-Content "logs\automation_orchestrator.log" -Tail 50
```

---

## 🚀 Service Management

| Action | Command |
|--------|---------|
| **Start** | `.\scripts\start_watcher_service.ps1` |
| **Stop** | `.\scripts\stop_watcher_service.ps1` |
| **Status** | `.\scripts\check_watcher_status.ps1` |
| **Quick Start** | `.\scripts\quick_start_automation.bat` |

---

## 🛠️ Common Commands

### Start Watcher (Foreground)
```bash
python scripts\automation\file_system_watcher.py --monitor
```

### Start Watcher (Background - Windows)
```bash
start /B python scripts\automation\file_system_watcher.py --monitor
```

### Test with Specific Client
```bash
python scripts\automation\file_system_watcher.py --test-client=client_domain
```

### Manual Workflow Trigger
```bash
python scripts\automation\workflow_orchestrator.py --trigger-file="clients\client\file.md"
```

### Check Running Processes
```powershell
Get-Process python | Where-Object {$_.CommandLine -like "*file_system_watcher*"}
```

---

## 🔧 Troubleshooting

### ❌ Nothing happens when creating .md files

**Cause**: Watcher not running

**Fix**:
```powershell
.\scripts\check_watcher_status.ps1  # Check status
.\scripts\start_watcher_service.ps1  # Start if needed
```

---

### ❌ Watcher starts then stops immediately

**Cause**: Missing dependencies

**Fix**:
```bash
pip install watchdog decouple
python scripts\automation\file_system_watcher.py --monitor
```

---

### ❌ Files detected but no .docx created

**Cause**: Converter dependencies missing

**Fix**:
```bash
pip install pandoc pypandoc python-docx
python scripts\convert_my_docs.py --test
```

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `AUTOMATIC_CONVERSION_SETUP_GUIDE.md` | Complete setup instructions |
| `AUTOMATION_FIX_IMPLEMENTATION_SUMMARY.md` | What was fixed and why |
| `AUTOMATION_SYSTEM_DOCUMENTATION.md` | Full system documentation |
| `logs\file_system_watcher.log` | Watcher activity log |
| `logs\automation_orchestrator.log` | Workflow execution log |

---

## ⏱️ Expected Performance

| Metric | Normal Value |
|--------|-------------|
| **Detection Time** | 1-5 seconds |
| **Full Workflow** | 30-60 seconds |
| **Memory Usage** | 50-100 MB |
| **CPU Usage** | < 5% idle |

---

## ✅ Success Indicators

When working correctly, you'll see:

1. ✅ Watcher process running continuously
2. ✅ `.docx` files appear within 30 seconds of `.md` creation
3. ✅ Logs show "workflow succeeded" messages
4. ✅ 15 mandatory project files auto-generated
5. ✅ Files uploaded to Google Drive

---

## 🎯 What Gets Automated

**When you create**: `clients\client_name\document.md`

**Automatically happens**:
1. ✅ File detection (1-5 seconds)
2. ✅ Generate 15 mandatory project files (if missing)
3. ✅ Convert all .md files to .docx
4. ✅ Upload to Google Drive
5. ✅ Log activity
6. ✅ Total time: 30-60 seconds

**Zero manual intervention required!** 🎉

---

## 🚨 Emergency Commands

### Stop Everything
```powershell
Get-Process python | Where-Object {$_.CommandLine -like "*file_system_watcher*"} | Stop-Process
```

### Clear Logs
```bash
del logs\*.log
```

### Reset System
```bash
.\scripts\stop_watcher_service.ps1
del logs\watcher.pid
.\scripts\start_watcher_service.ps1
```

---

## 📞 Getting Help

1. **Check status**: `.\scripts\check_watcher_status.ps1`
2. **Read logs**: `Get-Content "logs\file_system_watcher.log" -Tail 50`
3. **Review setup**: `AUTOMATIC_CONVERSION_SETUP_GUIDE.md`
4. **Test components**: `python scripts\convert_my_docs.py --test`

---

## 🎓 Remember

**The watcher MUST be running for automation to work!**

If your computer restarts, you must:
- **Option A**: Manually restart watcher
- **Option B**: Set up Task Scheduler for auto-start

**Quick check**:
```powershell
.\scripts\check_watcher_status.ps1
```

If status shows "NOT RUNNING", start it:
```powershell
.\scripts\start_watcher_service.ps1
```

---

**🟢 Status**: Ready to use!

**📅 Last Updated**: 30 September 2025