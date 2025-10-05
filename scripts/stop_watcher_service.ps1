# Bigger Boss File System Watcher - Stop Service Script
# This script stops the running file system watcher service

# Configuration
$ProjectRoot = "C:\Apps\Agents\Bigger Boss\bigger-boss"
$LogFile = Join-Path $ProjectRoot "logs\watcher_service.log"
$PidFile = Join-Path $ProjectRoot "logs\watcher.pid"

# Log stop attempt
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
"[$timestamp] Attempting to stop file system watcher service" | Out-File -FilePath $LogFile -Append

# Check if PID file exists
if (-not (Test-Path $PidFile)) {
    Write-Host "No watcher service PID file found. Service may not be running."

    # Try to find process by command line
    $watcherProcesses = Get-Process python -ErrorAction SilentlyContinue |
        Where-Object { $_.CommandLine -like "*file_system_watcher*" }

    if ($watcherProcesses) {
        Write-Host "Found $($watcherProcesses.Count) watcher process(es) running"
        foreach ($proc in $watcherProcesses) {
            Write-Host "Stopping process PID: $($proc.Id)"
            Stop-Process -Id $proc.Id -Force
            "[$timestamp] Stopped orphaned watcher process PID: $($proc.Id)" | Out-File -FilePath $LogFile -Append
        }
        Write-Host "File system watcher stopped successfully"
    }
    else {
        Write-Host "No file system watcher processes found running"
    }
    exit 0
}

# Read PID from file
$watcherPid = Get-Content $PidFile

# Check if process is running
$process = Get-Process -Id $watcherPid -ErrorAction SilentlyContinue

if ($process) {
    Write-Host "Stopping file system watcher (PID: $watcherPid)..."

    # Try graceful shutdown first
    Stop-Process -Id $watcherPid -ErrorAction SilentlyContinue

    # Wait up to 10 seconds for graceful shutdown
    $waited = 0
    while ((Get-Process -Id $watcherPid -ErrorAction SilentlyContinue) -and ($waited -lt 10)) {
        Start-Sleep -Seconds 1
        $waited++
    }

    # Force kill if still running
    if (Get-Process -Id $watcherPid -ErrorAction SilentlyContinue) {
        Write-Host "Process did not stop gracefully, forcing shutdown..."
        Stop-Process -Id $watcherPid -Force -ErrorAction SilentlyContinue
    }

    "[$timestamp] File system watcher stopped (PID: $watcherPid)" | Out-File -FilePath $LogFile -Append
    Write-Host "File system watcher stopped successfully"
}
else {
    Write-Host "Watcher process (PID: $watcherPid) is not running"
    "[$timestamp] Watcher process not found (PID: $watcherPid)" | Out-File -FilePath $LogFile -Append
}

# Remove PID file
if (Test-Path $PidFile) {
    Remove-Item $PidFile -Force
}

Write-Host "Service stopped"
exit 0