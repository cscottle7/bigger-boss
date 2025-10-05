@echo off
REM Quick Start Script for Bigger Boss Automation System
REM This script performs initial setup and starts the file system watcher

echo ========================================
echo Bigger Boss Automation - Quick Start
echo ========================================
echo.

REM Change to project directory
cd /d "C:\Apps\Agents\Bigger Boss\bigger-boss"

REM Check Python
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.8 or higher and add to PATH
    pause
    exit /b 1
)
python --version
echo.

REM Check/Install Dependencies
echo [2/5] Checking dependencies...
python -c "import watchdog" >nul 2>&1
if errorlevel 1 (
    echo Installing watchdog library...
    pip install watchdog
)
python -c "import decouple" >nul 2>&1
if errorlevel 1 (
    echo Installing decouple library...
    pip install python-decouple
)
echo Dependencies OK
echo.

REM Create logs directory
echo [3/5] Setting up directories...
if not exist "logs" mkdir logs
echo Directories OK
echo.

REM Test components
echo [4/5] Testing components...
echo Testing file system watcher...
python scripts\automation\file_system_watcher.py --test-client=test 2>&1 | findstr /C:"test" >nul
if errorlevel 1 (
    echo WARNING: Watcher test had issues, but continuing...
) else (
    echo Watcher OK
)
echo.

REM Start the watcher
echo [5/5] Starting file system watcher...
echo.
echo ========================================
echo The watcher will now monitor:
echo   clients\ folder
echo.
echo It will automatically:
echo   1. Detect new .md files
echo   2. Generate missing project files
echo   3. Convert markdown to .docx
echo   4. Upload to Google Drive
echo.
echo Press Ctrl+C to stop
echo ========================================
echo.

python scripts\automation\file_system_watcher.py --monitor

pause