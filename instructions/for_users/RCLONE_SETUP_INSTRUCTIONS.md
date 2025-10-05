# rclone Google Drive Setup Instructions

**Note:** rclone is already installed and configured in your system. These instructions are provided for reference or if you need to reconfigure.

---

## Current Status ✅

Your system already has:
- ✅ rclone v1.71.1 installed at `tools/rclone.exe`
- ✅ Google Drive remote 'googledrive' configured and operational
- ✅ Integration with Bigger Boss automation system

**If everything is working, no further setup is needed.**

---

## Manual rclone Configuration (If Needed)

### Step 1: Access rclone Configuration

Open Command Prompt or PowerShell in your project directory and run:

```bash
# Using the local rclone installation
tools\rclone.exe config

# Or if you have rclone in your system PATH
rclone config
```

### Step 2: Create Google Drive Remote

When the rclone config menu opens:

1. **Choose option:** `n` (New remote)
2. **Enter name:** `googledrive` (or your preferred name)
3. **Choose storage type:** Enter `drive` (for Google Drive)
4. **Client ID:** Press Enter to use rclone's default (or enter your own)
5. **Client Secret:** Press Enter to use rclone's default (or enter your own)
6. **Scope:** Choose `1` (Full access to all files)
7. **Root folder ID:** Press Enter (leave empty for root)
8. **Service Account File:** Press Enter (leave empty)
9. **Advanced config:** Choose `n` (No)
10. **Remote config:** Choose `y` (Yes, for web browser authentication)

### Step 3: Web Authentication

1. rclone will open your web browser
2. **Sign in to Google** with the account that has access to your shared drive
3. **Grant permissions** to rclone
4. **Copy the verification code** back to the terminal

### Step 4: Verify Configuration

```bash
# Test the connection
tools\rclone.exe lsd googledrive:

# Should show your Google Drive folders
```

---

## Shared Google Drive Access

### For Shared/Team Drives:

If you need to access a specific shared drive:

```bash
# List all team drives
tools\rclone.exe backend drives googledrive:

# Configure for specific team drive
tools\rclone.exe config update googledrive team_drive "TEAM_DRIVE_ID"
```

### Current Configuration

Your system is set up to upload to:
```
SEO/Content/{Client Name}/{YYYY-MM}/Content/
```

For example:
- Luna Digital Marketing → `SEO/Content/Luna Digital Marketing/2025-09/Content/`
- Sydney Coach Charter → `SEO/Content/Sydney Coach Charter/2025-09/Content/`

---

## Testing Your Setup

### Test Basic Connection
```bash
# List root directories
tools\rclone.exe lsd googledrive:

# Check if SEO folder exists
tools\rclone.exe lsd googledrive:SEO

# Check Content subfolder
tools\rclone.exe lsd googledrive:SEO/Content
```

### Test File Upload
```bash
# Create test file
echo "Test content" > test.txt

# Upload to test location
tools\rclone.exe copy test.txt googledrive:SEO/Content/Test/

# Verify upload
tools\rclone.exe ls googledrive:SEO/Content/Test/

# Clean up
tools\rclone.exe delete googledrive:SEO/Content/Test/test.txt
del test.txt
```

---

## Advanced Configuration Options

### Custom Client ID/Secret (Optional)

For better performance and to avoid rate limits:

1. **Go to:** [Google Cloud Console](https://console.cloud.google.com/)
2. **Create project** or select existing
3. **Enable Google Drive API**
4. **Create OAuth 2.0 credentials**
5. **Add your credentials:**

```bash
tools\rclone.exe config update googledrive client_id "YOUR_CLIENT_ID"
tools\rclone.exe config update googledrive client_secret "YOUR_CLIENT_SECRET"
```

### Environment Variables (Alternative Method)

Add to your `.env` file:
```env
GOOGLE_DRIVE_CLIENT_ID=your_client_id_here
GOOGLE_DRIVE_CLIENT_SECRET=your_client_secret_here
```

Then use the automated setup:
```bash
python scripts/gdrive_upload.py setup --non-interactive
```

---

## Troubleshooting

### Common Issues:

**1. "Remote not found" error:**
```bash
# Check existing remotes
tools\rclone.exe config show

# Recreate remote if missing
tools\rclone.exe config create googledrive drive
```

**2. Authentication expired:**
```bash
# Refresh authentication
tools\rclone.exe config reconnect googledrive
```

**3. Permission denied:**
```bash
# Check if you have access to the shared drive
tools\rclone.exe lsd googledrive:
```

**4. Slow uploads:**
```bash
# Optimize transfer settings
tools\rclone.exe copy file.txt googledrive:path/ --transfers=4 --checkers=8
```

### Getting Help:

```bash
# rclone help
tools\rclone.exe help

# Google Drive specific help
tools\rclone.exe help drive

# Configuration help
tools\rclone.exe config help
```

---

## Integration with Bigger Boss System

### Automatic Usage

The system automatically uses rclone when:
- Any `.md` file is created in `clients/` folder
- The file gets converted to `.docx`
- rclone uploads to appropriate Google Drive folder

### Manual Upload

You can also manually upload files:

```bash
# Upload specific client file
python scripts/gdrive_upload.py upload client_document.docx --client=lunadigitalmarketing_com_au

# Check upload status
python scripts/gdrive_upload.py status
```

### Configuration Check

Verify your setup is working:
```bash
# Quick system test
python quick_test.py

# Test Google Drive integration specifically
python -c "from scripts.gdrive_upload import GoogleDriveUploader; u = GoogleDriveUploader(); print('Config OK:', u._check_rclone_config())"
```

---

## Security Notes

- **Never commit rclone.conf** to version control
- **Use service accounts** for production environments
- **Regularly rotate** OAuth tokens if using custom credentials
- **Monitor access logs** in Google Drive admin console

---

## Summary

Your rclone setup enables:
✅ Automatic document uploads to shared Google Drive
✅ Organized folder structure (SEO/Content/{Client}/{Date})
✅ Integration with the Bigger Boss automation system
✅ Professional document processing pipeline

**Current Status: Fully configured and operational**