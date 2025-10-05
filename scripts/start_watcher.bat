@echo off
REM Bigger Boss File System Watcher - Startup Script
REM This script starts the file system watcher for automatic markdown to DOCX conversion

echo ========================================
echo Bigger Boss File System Watcher
echo ========================================
echo.

REM Change to project directory
cd /d "C:\Apps\Agents\Bigger Boss\bigger-boss"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found in PATH
    echo Please install Python or add it to your PATH
    pause
    exit /b 1
)

REM Check if required dependencies are installed
python -c "import watchdog" >nul 2>&1
if errorlevel 1 (
    echo WARNING: watchdog library not installed
    echo Installing required dependencies...
    pip install watchdog decouple
)

echo Starting file system watcher...
echo.
echo Monitoring: clients\ folder
echo.
echo Press Ctrl+C to stop the watcher
echo.

REM Start the file system watcher
python scripts\automation\file_system_watcher.py --monitor

REM If watcher exits, pause so user can see any error messages
if errorlevel 1 (
    echo.
    echo ERROR: File system watcher exited with error
    pause
)