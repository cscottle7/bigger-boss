@echo off
REM Setup Windows Scheduled Task for Bigger Boss Automation
REM This creates a task that starts the file watcher on system startup

echo ========================================
echo Bigger Boss - Auto-Start Setup
echo ========================================
echo.

REM Check for admin privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This script requires administrator privileges
    echo Please right-click and select "Run as administrator"
    pause
    exit /b 1
)

echo Creating scheduled task...
echo.

REM Create the scheduled task
schtasks /create ^
    /tn "Bigger Boss File Watcher" ^
    /tr "\"C:\Apps\Agents\Bigger Boss\bigger-boss\scripts\quick_start_automation.bat\"" ^
    /sc onlogon ^
    /rl highest ^
    /f

if %errorLevel% equ 0 (
    echo.
    echo ========================================
    echo SUCCESS - Auto-start configured!
    echo ========================================
    echo.
    echo The Bigger Boss File Watcher will now:
    echo   - Start automatically when you log in
    echo   - Monitor clients\ folder for new content
    echo   - Auto-convert MD to DOCX
    echo   - Auto-upload to Google Drive via RClone
    echo.
    echo To manage the task:
    echo   - View: schtasks /query /tn "Bigger Boss File Watcher"
    echo   - Delete: schtasks /delete /tn "Bigger Boss File Watcher" /f
    echo   - Run now: schtasks /run /tn "Bigger Boss File Watcher"
    echo.
    echo ========================================
    echo.
    echo Would you like to start the watcher now? (Y/N)
    choice /c YN /n
    if errorlevel 2 goto :end
    if errorlevel 1 goto :start_now
) else (
    echo.
    echo ERROR: Failed to create scheduled task
    echo Error code: %errorLevel%
    pause
    exit /b 1
)

:start_now
echo.
echo Starting the watcher now...
schtasks /run /tn "Bigger Boss File Watcher"
echo.
echo Task started! Check the logs folder for activity.
goto :end

:end
echo.
pause
