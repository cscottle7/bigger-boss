# Bigger Boss File System Watcher - Status Check Script
# This script checks if the file system watcher service is running

# Configuration
$ProjectRoot = "C:\Apps\Agents\Bigger Boss\bigger-boss"
$LogFile = Join-Path $ProjectRoot "logs\watcher_service.log"
$PidFile = Join-Path $ProjectRoot "logs\watcher.pid"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Bigger Boss File System Watcher Status" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if PID file exists
if (Test-Path $PidFile) {
    $watcherPid = Get-Content $PidFile
    $process = Get-Process -Id $watcherPid -ErrorAction SilentlyContinue

    if ($process) {
        Write-Host "Status: " -NoNewline
        Write-Host "RUNNING" -ForegroundColor Green
        Write-Host "PID: $watcherPid"
        Write-Host "Memory: $([math]::Round($process.WorkingSet64 / 1MB, 2)) MB"
        Write-Host "CPU Time: $($process.TotalProcessorTime.ToString('hh\:mm\:ss'))"
        Write-Host "Started: $($process.StartTime)"

        # Calculate uptime
        $uptime = (Get-Date) - $process.StartTime
        Write-Host "Uptime: $($uptime.Days) days, $($uptime.Hours) hours, $($uptime.Minutes) minutes"
    }
    else {
        Write-Host "Status: " -NoNewline
        Write-Host "STOPPED" -ForegroundColor Red
        Write-Host "PID file exists but process not running (PID: $watcherPid)"
        Write-Host "Cleaning up stale PID file..."
        Remove-Item $PidFile -Force
    }
}
else {
    # Try to find process by command line
    $watcherProcesses = Get-Process python -ErrorAction SilentlyContinue |
        Where-Object { $_.CommandLine -like "*file_system_watcher*" }

    if ($watcherProcesses) {
        Write-Host "Status: " -NoNewline
        Write-Host "RUNNING (no PID file)" -ForegroundColor Yellow
        Write-Host "Found $($watcherProcesses.Count) process(es):"
        foreach ($proc in $watcherProcesses) {
            Write-Host "  PID: $($proc.Id) - Memory: $([math]::Round($proc.WorkingSet64 / 1MB, 2)) MB"
        }
    }
    else {
        Write-Host "Status: " -NoNewline
        Write-Host "NOT RUNNING" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "----------------------------------------" -ForegroundColor Cyan
Write-Host "Recent Activity (Last 10 log entries):" -ForegroundColor Cyan
Write-Host "----------------------------------------" -ForegroundColor Cyan

if (Test-Path $LogFile) {
    Get-Content $LogFile -Tail 10 | ForEach-Object {
        Write-Host $_
    }
}
else {
    Write-Host "No log file found at: $LogFile" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan

# Check automation orchestrator logs
$orchestratorLog = Join-Path $ProjectRoot "logs\automation_orchestrator.log"
if (Test-Path $orchestratorLog) {
    $recentWorkflows = Get-Content $orchestratorLog | Select-String "workflow succeeded" -SimpleMatch | Select-Object -Last 5

    if ($recentWorkflows.Count -gt 0) {
        Write-Host ""
        Write-Host "Recent Successful Workflows:" -ForegroundColor Green
        $recentWorkflows | ForEach-Object {
            Write-Host "  $_"
        }
    }
}

Write-Host ""
Write-Host "Commands:" -ForegroundColor Cyan
Write-Host "  Start:  .\scripts\start_watcher_service.ps1"
Write-Host "  Stop:   .\scripts\stop_watcher_service.ps1"
Write-Host "  Logs:   Get-Content 'logs\file_system_watcher.log' -Wait -Tail 20"
Write-Host ""