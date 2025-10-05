@echo off
REM Remove Bigger Boss Auto-Start Scheduled Task

echo ========================================
echo Bigger Boss - Remove Auto-Start
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

echo Removing scheduled task...
echo.

schtasks /delete /tn "Bigger Boss File Watcher" /f

if %errorLevel% equ 0 (
    echo.
    echo SUCCESS - Auto-start removed
    echo The watcher will no longer start automatically on login
    echo.
) else (
    echo.
    echo ERROR: Failed to remove scheduled task (it may not exist)
    echo.
)

pause
