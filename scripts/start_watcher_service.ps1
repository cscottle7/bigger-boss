# Bigger Boss File System Watcher - PowerShell Service Starter
# This script starts the file system watcher as a background service

# Configuration
$ProjectRoot = "C:\Apps\Agents\Bigger Boss\bigger-boss"
$LogFile = Join-Path $ProjectRoot "logs\watcher_service.log"
$PidFile = Join-Path $ProjectRoot "logs\watcher.pid"

# Ensure logs directory exists
$LogsDir = Join-Path $ProjectRoot "logs"
if (-not (Test-Path $LogsDir)) {
    New-Item -ItemType Directory -Path $LogsDir -Force | Out-Null
}

# Change to project directory
Set-Location $ProjectRoot

# Log startup
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
"[$timestamp] Starting Bigger Boss File System Watcher Service" | Out-File -FilePath $LogFile -Append

# Check if watcher is already running
if (Test-Path $PidFile) {
    $existingPid = Get-Content $PidFile
    $existingProcess = Get-Process -Id $existingPid -ErrorAction SilentlyContinue

    if ($existingProcess) {
        "[$timestamp] WARNING: Watcher already running with PID $existingPid" | Out-File -FilePath $LogFile -Append
        Write-Host "File system watcher is already running (PID: $existingPid)"
        exit 0
    }
}

# Check Python availability
try {
    $pythonVersion = python --version 2>&1
    "[$timestamp] Python detected: $pythonVersion" | Out-File -FilePath $LogFile -Append
}
catch {
    "[$timestamp] ERROR: Python not found in PATH" | Out-File -FilePath $LogFile -Append
    Write-Error "Python not found. Please install Python and add it to PATH."
    exit 1
}

# Check required dependencies
try {
    python -c "import watchdog; import decouple" 2>&1 | Out-Null
    "[$timestamp] Dependencies verified" | Out-File -FilePath $LogFile -Append
}
catch {
    "[$timestamp] WARNING: Installing missing dependencies..." | Out-File -FilePath $LogFile -Append
    pip install watchdog decouple 2>&1 | Out-File -FilePath $LogFile -Append
}

# Start the file system watcher as background process
"[$timestamp] Launching file system watcher..." | Out-File -FilePath $LogFile -Append

$watcherScript = Join-Path $ProjectRoot "scripts\automation\file_system_watcher.py"

# Start process and capture PID
$process = Start-Process -FilePath "python" `
    -ArgumentList "$watcherScript --monitor --log-level=INFO" `
    -WorkingDirectory $ProjectRoot `
    -WindowStyle Hidden `
    -PassThru

# Save PID for monitoring
$process.Id | Out-File -FilePath $PidFile

"[$timestamp] File system watcher started with PID: $($process.Id)" | Out-File -FilePath $LogFile -Append
Write-Host "File system watcher started successfully (PID: $($process.Id))"
Write-Host "Monitor logs at: $LogFile"

# Wait a few seconds to ensure process started correctly
Start-Sleep -Seconds 3

# Verify process is still running
if ($process.HasExited) {
    "[$timestamp] ERROR: Watcher process exited immediately" | Out-File -FilePath $LogFile -Append
    Write-Error "File system watcher failed to start. Check logs for details."
    exit 1
}

"[$timestamp] File system watcher service is running and monitoring clients\ folder" | Out-File -FilePath $LogFile -Append
Write-Host "Service is running. Monitoring: clients\ folder"
exit 0