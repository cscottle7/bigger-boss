# Bigger Boss - Quick Start Guide

## ⚡ First Time Setup (5 Minutes)

### 1. Activate Automation
Right-click and **"Run as administrator":**
```
scripts/setup_auto_start.bat
```

This configures auto-start on login. The watcher will:
- Monitor `clients/` folder for changes
- Auto-convert MD → DOCX
- Auto-upload to Google Drive
- Track all activity

### 2. Verify It's Working
Double-click:
```
scripts/check_automation_status.bat
```

Should show all green checkmarks.

### 3. Clean Up Google Drive Duplicates
```bash
python system/maintenance/deduplicate_google_drive_folders.py --execute
```

Merges duplicate folders (Capital Smiles x2, Green Power Solutions x5, etc.)

**Done!** The system is now fully automated.

---

## 📋 Daily Usage

### Request Full Website Content
```
"Generate all website content for [CLIENT_DOMAIN]"
```

**Example:**
```
"Generate all website content for lunadigitalmarketing.com.au"
```

**What happens:**
1. System reads research files
2. Creates all pages from content plan
3. Quality loops ensure 8/10+ scores
4. Saves to `clients/{domain}/content/website_pages/*.md`
5. Auto-converts to .docx
6. Auto-uploads to Google Drive

---

### Request Single Blog Post
```
"Write a blog post about [TOPIC] for [CLIENT]"
```

**Example:**
```
"Write a blog post about 'SEO for dental practices' for Capital Smiles"
```

**What happens:**
1. Creates comprehensive content brief
2. Writes full optimized blog post
3. Quality assurance checks
4. Saves to `clients/{domain}/content/blog/*.md`
5. Auto-converts & uploads

---

### Update Existing Content
```
"Update [PAGE] for [CLIENT] using content from [URL]"
```

**Example:**
```
"Update the homepage for Capital Smiles using content from capitalsmiles.com.au"
```

**What happens:**
1. Extracts current content via JINA Reader
2. Creates gap analysis
3. Merges old + new (preserves brand voice)
4. Saves to `clients/{domain}/content/updates/*.md`
5. Auto-converts & uploads

---

## 🔧 Management Commands

### Check System Status
```
scripts/check_automation_status.bat
```

### Start Watcher Manually (No Auto-Start)
```
scripts/quick_start_automation.bat
```

### Remove Auto-Start
```
scripts/remove_auto_start.bat
```
(Run as admin)

### View Live Logs
**PowerShell:**
```powershell
Get-Content logs\file_system_watcher.log -Wait -Tail 20
```

**Git Bash:**
```bash
tail -f logs/file_system_watcher.log
```

### Test RClone Connection
```bash
rclone lsd googledrive:SEO/Content
```

---

## 📁 File Structure

```
clients/{client_domain}/
├── README.md                    # Project navigation
├── PROJECT_OVERVIEW.md          # Executive summary
├── automation_activity.json     # Automation tracking
├── strategy/                    # Strategic planning
│   ├── research_brief.md
│   ├── implementation_plan.md
│   └── current_website_analysis.md
├── research/                    # Market intelligence
│   ├── competitive_analysis.md
│   ├── audience_personas.md
│   └── keyword_research.md
├── content/                     # Content deliverables
│   ├── website_pages/           # Full website content
│   ├── blog/                    # Blog posts
│   ├── updates/                 # Content refreshes
│   └── comprehensive_website_content_plans.md
├── technical/                   # Technical audits
│   ├── technical_audit.md
│   ├── ai_optimization_guide.md
│   └── ux_ui_analysis.md
└── implementation/              # Execution tracking
    ├── task_deps.md
    └── execution_tracking_report.md
```

---

## 🚨 Troubleshooting

### Watcher Not Running
1. Run `scripts/check_automation_status.bat`
2. Check logs: `logs/file_system_watcher.log`
3. Restart: `scripts/quick_start_automation.bat`

### Files Not Uploading
1. Test RClone: `rclone listremotes` (should show `googledrive:`)
2. Manual test: `rclone lsd googledrive:SEO/Content`
3. Re-authenticate: `rclone config reconnect googledrive:`

### Duplicate Folders in Google Drive
```bash
python system/maintenance/deduplicate_google_drive_folders.py --execute
```

---

## 📖 Full Documentation

- **Complete setup guide:** `AUTOMATION_SETUP_GUIDE.md`
- **Next steps:** `SETUP_COMPLETE_NEXT_STEPS.md`
- **Project standards:** `CLAUDE.md`

---

## ✨ Quick Tips

- **Research MUST be completed first** - All content workflows require the 4-phase research foundation
- **Citations required** - All statistics need credible sources
- **Australian English** - All content uses Australian spelling
- **Feedback loops** - Quality improvement is iterative (3 max cycles per piece)
- **Auto-upload delay** - 5 second debounce prevents duplicate processing

---

## 🎯 Content Quality Standards

Every piece of content goes through:

1. **clarity_conciseness_editor** (Threshold: 8/10)
2. **cognitive_load_minimizer** (Threshold: 7/10)
3. **content_critique_specialist** (Threshold: 7/10)
4. **ai_text_naturalizer** (Threshold: 8/10)

**Target:** Aggregate score ≥8.5/10 before publication

---

**Need help?** Check `AUTOMATION_SETUP_GUIDE.md` or review `SETUP_COMPLETE_NEXT_STEPS.md`
