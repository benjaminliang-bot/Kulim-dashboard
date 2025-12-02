# PowerShell script to create Windows Task Scheduler task for weekly report
# Run this script as Administrator to create the scheduled task

$TaskName = "Weekly OC Performance Report"
$ScriptPath = "c:\Users\benjamin.liang\Documents\Python\run_weekly_report.bat"
$WorkingDirectory = "c:\Users\benjamin.liang\Documents\Python"
$Description = "Automated weekly report for Outer Cities performance metrics sent to Slack"

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "⚠️  This script requires Administrator privileges." -ForegroundColor Yellow
    Write-Host "Please run PowerShell as Administrator and execute this script again." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To run as Admin:" -ForegroundColor Cyan
    Write-Host "1. Right-click PowerShell" -ForegroundColor Cyan
    Write-Host "2. Select 'Run as Administrator'" -ForegroundColor Cyan
    Write-Host "3. Navigate to: $WorkingDirectory" -ForegroundColor Cyan
    Write-Host "4. Run: .\setup_scheduled_task.ps1" -ForegroundColor Cyan
    exit 1
}

# Check if script exists
if (-not (Test-Path $ScriptPath)) {
    Write-Host "❌ Error: Script not found at $ScriptPath" -ForegroundColor Red
    exit 1
}

# Remove existing task if it exists
$existingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Write-Host "⚠️  Existing task found. Removing it..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# Create the action (run the batch file)
$action = New-ScheduledTaskAction -Execute $ScriptPath -WorkingDirectory $WorkingDirectory

# Create the trigger (Every Monday at 9:00 AM)
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 9:00AM

# Create settings
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 5)

# Create principal (run as current user)
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Highest

# Register the task
try {
    Register-ScheduledTask `
        -TaskName $TaskName `
        -Action $action `
        -Trigger $trigger `
        -Settings $settings `
        -Principal $principal `
        -Description $Description `
        -Force
    
    Write-Host ""
    Write-Host "✅ Scheduled task created successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Task Details:" -ForegroundColor Cyan
    Write-Host "  Name: $TaskName" -ForegroundColor White
    Write-Host "  Schedule: Every Monday at 9:00 AM" -ForegroundColor White
    Write-Host "  Script: $ScriptPath" -ForegroundColor White
    Write-Host ""
    Write-Host "To view the task:" -ForegroundColor Cyan
    Write-Host "  Open Task Scheduler > Task Scheduler Library > $TaskName" -ForegroundColor White
    Write-Host ""
    Write-Host "To test the task:" -ForegroundColor Cyan
    Write-Host "  Right-click the task in Task Scheduler > Run" -ForegroundColor White
    Write-Host ""
    Write-Host "To modify the schedule:" -ForegroundColor Cyan
    Write-Host "  Right-click the task > Properties > Triggers tab" -ForegroundColor White
    
} catch {
    Write-Host "❌ Error creating scheduled task: $_" -ForegroundColor Red
    exit 1
}

