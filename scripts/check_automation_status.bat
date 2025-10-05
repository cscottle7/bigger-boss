@echo off
REM Check Bigger Boss Automation Status

echo ========================================
echo Bigger Boss Automation - Status Check
echo ========================================
echo.

echo [1] Checking Scheduled Task...
schtasks /query /tn "Bigger Boss File Watcher" /fo list 2>nul
if %errorLevel% equ 0 (
    echo Status: Scheduled task EXISTS
) else (
    echo Status: Scheduled task NOT FOUND
    echo Run setup_auto_start.bat to configure auto-start
)
echo.

echo [2] Checking Running Processes...
tasklist /fi "imagename eq python3.13.exe" /fi "windowtitle eq file_system_watcher*" 2>nul | find /i "python" >nul
if %errorLevel% equ 0 (
    echo Status: File watcher IS RUNNING
) else (
    echo Status: File watcher NOT RUNNING
    echo Run quick_start_automation.bat to start manually
    echo Or run: schtasks /run /tn "Bigger Boss File Watcher"
)
echo.

echo [3] Checking RClone Configuration...
rclone listremotes 2>nul | find /i "googledrive" >nul
if %errorLevel% equ 0 (
    echo Status: RClone configured for Google Drive
) else (
    echo Status: RClone NOT configured
    echo Run: rclone config to set up Google Drive
)
echo.

echo [4] Checking Recent Logs...
if exist "logs\file_system_watcher.log" (
    echo Status: Log file exists
    echo Last 5 log entries:
    powershell -Command "Get-Content 'logs\file_system_watcher.log' -Tail 5"
) else (
    echo Status: No log file found (watcher hasn't run yet)
)
echo.

echo [5] Checking Automation Components...
echo Checking file_system_watcher.py...
if exist "scripts\automation\file_system_watcher.py" (
    echo   OK - File watcher exists
) else (
    echo   ERROR - File watcher missing
)

echo Checking workflow_orchestrator.py...
if exist "scripts\automation\workflow_orchestrator.py" (
    echo   OK - Workflow orchestrator exists
) else (
    echo   ERROR - Workflow orchestrator missing
)

echo Checking quick_start_automation.bat...
if exist "scripts\quick_start_automation.bat" (
    echo   OK - Quick start script exists
) else (
    echo   ERROR - Quick start script missing
)
echo.

echo ========================================
echo Status Check Complete
echo ========================================
echo.
pause
