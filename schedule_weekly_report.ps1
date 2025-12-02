# PowerShell script to schedule weekly report task
# This will create a Windows Task Scheduler task to run the weekly report every Monday at 9:00 AM

$scriptPath = "c:\Users\benjamin.liang\Documents\Python\process_and_send_weekly_report.py"
$pythonPath = "py"  # Will use 'py' launcher, or specify full path if needed

# Get full Python path
try {
    $pythonFullPath = (Get-Command py).Source
    Write-Host "Found Python at: $pythonFullPath"
} catch {
    # Try to find Python in common locations
    $pythonFullPath = "py"
    Write-Host "Using 'py' launcher"
}

# Task name
$taskName = "OC_Weekly_Performance_Report"

# Check if task already exists
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue

if ($existingTask) {
    Write-Host "Task '$taskName' already exists. Updating..."
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

# Create action (run Python script)
$action = New-ScheduledTaskAction -Execute $pythonFullPath -Argument "`"$scriptPath`"" -WorkingDirectory "c:\Users\benjamin.liang\Documents\Python"

# Create trigger (every Monday at 9:00 AM)
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At "9:00AM"

# Create settings
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RunOnlyIfNetworkAvailable

# Create principal (run as current user)
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive -RunLevel Highest

# Register the task
try {
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Description "Automatically runs OC Weekly Performance Report every Monday at 9:00 AM"
    Write-Host "`n✅ Successfully scheduled task: $taskName" -ForegroundColor Green
    Write-Host "   Schedule: Every Monday at 9:00 AM" -ForegroundColor Green
    Write-Host "   Script: $scriptPath" -ForegroundColor Green
    Write-Host "`nTo view the task, run: Get-ScheduledTask -TaskName '$taskName'" -ForegroundColor Yellow
    Write-Host "To test the task, run: Start-ScheduledTask -TaskName '$taskName'" -ForegroundColor Yellow
    Write-Host "To remove the task, run: Unregister-ScheduledTask -TaskName '$taskName' -Confirm:`$false" -ForegroundColor Yellow
} catch {
    Write-Host "`n❌ Error creating scheduled task: $_" -ForegroundColor Red
    Write-Host "You may need to run PowerShell as Administrator" -ForegroundColor Yellow
}


