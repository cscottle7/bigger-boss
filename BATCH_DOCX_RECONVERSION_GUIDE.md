# Batch DOCX Reconversion Guide

## Overview

This guide explains how to reconvert existing .docx files that were created with the old plain-text converter and still contain visible markdown syntax instead of proper rich text formatting.

## Problem Statement

**Before Fix (Old Converter)**:
- Markdown→DOCX conversion created plain text files
- Visible markdown syntax in .docx files: `**text**` instead of **text**
- No bold, italic, or code formatting applied

**After Fix (New Converter)**:
- Enhanced python-docx converter with inline formatting parser
- Proper rich text formatting applied
- **Bold**, *italic*, `code` formatting correctly rendered

## Solution

The `scripts/reconvert_existing_docx.py` script provides batch reconversion of existing files.

### Features

✅ **Automatic Detection**: Finds all .docx files with corresponding .md source files
✅ **Backup System**: Creates timestamped backups before reconversion
✅ **Dry-Run Mode**: Preview changes before execution
✅ **Progress Tracking**: Real-time conversion statistics
✅ **Error Handling**: Robust error recovery and logging

## Usage

### Step 1: Preview Changes (Dry-Run)

```bash
python scripts/reconvert_existing_docx.py --dry-run
```

**Output Example**:
```
Found 700 .docx files with .md sources

capitalsmiles_com_au/
  - capitalsmiles_com_au\content\audience_style_guide.md
  - capitalsmiles_com_au\content\comprehensive_website_content_plans.md
  ...

Total files to reconvert: 700
Backup location: backups/docx_backup_20250905_143022
```

### Step 2: Execute Batch Reconversion

```bash
python scripts/reconvert_existing_docx.py --execute
```

**Process**:
1. ✅ Script scans for all .md files with .docx counterparts
2. ✅ Creates backup folder: `backups/docx_backup_YYYYMMDD_HHMMSS/`
3. ✅ Backs up each .docx file before reconversion
4. ✅ Deletes old .docx file
5. ✅ Reconverts from .md source using new enhanced converter
6. ✅ Tracks success/failure statistics

**Confirmation Prompt**:
```
Found 700 files to reconvert.
Backups will be saved to: backups/docx_backup_20250905_143022

Proceed with batch reconversion? (yes/no):
```

### Step 3: Review Results

```
RECONVERSION STATISTICS
======================================================================
Total files found:        700
Successfully reconverted: 695
Failed conversions:       5
Skipped files:            0
Files backed up:          700
Backup location:          backups/docx_backup_20250905_143022
Success rate:             99.3%
```

## Command Options

### Basic Options

| Option | Description |
|--------|-------------|
| `--dry-run` | Preview changes without modifying files |
| `--execute` | Execute batch reconversion |
| `--no-backup` | Disable backups (NOT RECOMMENDED) |
| `--verbose` | Enable detailed logging |

### Examples

**Preview changes**:
```bash
python scripts/reconvert_existing_docx.py --dry-run
```

**Execute with backups** (RECOMMENDED):
```bash
python scripts/reconvert_existing_docx.py --execute
```

**Execute without backups** (DANGEROUS):
```bash
python scripts/reconvert_existing_docx.py --execute --no-backup
```

**Verbose mode for debugging**:
```bash
python scripts/reconvert_existing_docx.py --execute --verbose
```

## Files Excluded from Reconversion

The script automatically skips:
- System files (anything starting with `.`)
- Temporary files (`temp/`, `tmp/`, `__pycache__/`)
- Template files (`templates/` folder)
- Files without corresponding .md source

## Backup System

### Backup Location

Backups are stored in timestamped folders:
```
backups/
└── docx_backup_20250905_143022/
    └── clients/
        ├── capitalsmiles_com_au/
        │   └── content/
        │       └── audience_style_guide.docx (ORIGINAL)
        └── greenpowersolutions_com_au/
            └── research/
                └── keyword_research.docx (ORIGINAL)
```

### Restore from Backup

If needed, restore original files:

**Single file**:
```bash
copy "backups\docx_backup_20250905_143022\clients\capitalsmiles_com_au\content\audience_style_guide.docx" "clients\capitalsmiles_com_au\content\audience_style_guide.docx"
```

**Entire backup folder**:
```bash
xcopy /E /Y "backups\docx_backup_20250905_143022\clients" "clients"
```

## Google Drive Upload

After reconversion, upload updated files to Google Drive:

### Automatic Upload (Recommended)

The file watcher system automatically detects changes and uploads:
1. ✅ Reconversion completes
2. ✅ File watcher detects modified .docx files
3. ✅ Workflow orchestrator triggers upload
4. ✅ RClone syncs to `googledrive:SEO/Content`

### Manual Upload

```bash
rclone sync clients "googledrive:SEO/Content" --exclude "CLIENT_FOLDER_TEMPLATE/**" --exclude "*.pyc" --exclude "__pycache__/**" --exclude ".git/**" --exclude "convert.py" --progress
```

## Troubleshooting

### Issue: "Converter script not found"

**Solution**: Verify converter script exists:
```bash
dir scripts\convert_my_docs.py
```

If missing, restore from repository.

### Issue: "Permission denied"

**Solution**: Close any open .docx files:
1. ✅ Close all Microsoft Word windows
2. ✅ Close any file explorers viewing client folders
3. ✅ Re-run reconversion script

### Issue: High failure rate

**Solution**: Enable verbose logging to diagnose:
```bash
python scripts/reconvert_existing_docx.py --execute --verbose
```

Check logs for specific error messages.

### Issue: Backup folder too large

**Solution**: Old backups can be deleted after verification:
```bash
# Verify new .docx files are correct
# Then delete old backups
rmdir /s /q "backups\docx_backup_20250905_143022"
```

## Best Practices

1. ✅ **Always run dry-run first** to preview changes
2. ✅ **Keep backups enabled** (default behaviour)
3. ✅ **Verify sample files** after reconversion before deleting backups
4. ✅ **Monitor success rate** - investigate if below 95%
5. ✅ **Use verbose mode** if troubleshooting issues

## Technical Details

### Conversion Process

1. **Find Pairs**: Scan `clients/` for .md files with .docx counterparts
2. **Backup**: Copy .docx to `backups/docx_backup_TIMESTAMP/`
3. **Delete**: Remove old .docx file
4. **Reconvert**: Execute `python scripts/convert_my_docs.py path/to/file.md`
5. **Track**: Update statistics (success/failure counts)

### Enhanced Converter Features

The new converter includes:
- **Inline Markdown Parser**: Regex-based `**bold**`, `*italic*`, `` `code` `` parsing
- **Heading Support**: H1, H2, H3 with proper Word styles
- **List Support**: Bullet points and numbered lists
- **Code Blocks**: Courier New font for inline code
- **Horizontal Rules**: Centered separator lines

### File Statistics

**Current Count** (as of dry-run):
- Total .docx files found: **684** (excludes CLIENT_FOLDER_TEMPLATE)
- Client folders affected: **17**
- Top clients by file count:
  - lunadigitalmarketing_com_au: 170 files
  - greenpowersolutions_com_au: 95 files
  - capitalsmiles_com_au: 55 files
- Estimated conversion time: **5-10 minutes**
- Estimated backup size: **50-100 MB**

## Next Steps

After batch reconversion:

1. ✅ Verify sample files from different clients
2. ✅ Check rich text formatting is applied correctly
3. ✅ Confirm Google Drive sync completes
4. ✅ Delete old backups after verification (optional)
5. ✅ Document any failures for investigation

---

**Created**: 5 September 2024
**Last Updated**: 5 September 2024
**Version**: 1.0.0
