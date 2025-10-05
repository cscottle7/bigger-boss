@echo off
REM Initial Google Drive Sync - Upload All Client Folders
REM This uploads all existing client folders to Google Drive SEO/Content

echo ========================================
echo Bigger Boss - Initial Google Drive Sync
echo ========================================
echo.

echo This will upload ALL client folders to Google Drive
echo Destination: googledrive:SEO/Content/
echo.
echo Press Ctrl+C to cancel, or
pause

echo.
echo Starting sync...
echo.

REM Sync each client folder to Google Drive
REM Using sync instead of copy to maintain structure and avoid duplicates

cd /d "C:\Apps\Agents\Bigger Boss\bigger-boss"

echo Syncing clients folder to Google Drive...
echo.

rclone sync clients "googledrive:SEO/Content" ^
    --exclude "CLIENT_FOLDER_TEMPLATE/**" ^
    --exclude "*.pyc" ^
    --exclude "__pycache__/**" ^
    --exclude ".git/**" ^
    --exclude "convert.py" ^
    --progress ^
    --verbose

if %errorLevel% equ 0 (
    echo.
    echo ========================================
    echo SUCCESS - Sync Complete!
    echo ========================================
    echo.
    echo All client folders uploaded to:
    echo googledrive:SEO/Content/
    echo.
    echo To verify, run:
    echo rclone lsd "googledrive:SEO/Content"
    echo.
) else (
    echo.
    echo ERROR - Sync failed
    echo Error code: %errorLevel%
    echo.
)

pause
