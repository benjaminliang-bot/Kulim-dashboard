# Weekly Report Scheduling Guide

This guide explains how to set up automated weekly reports using Windows Task Scheduler.

## 📋 Prerequisites

1. **Python installed** (accessible via `py` command)
2. **Required packages**: `requests` (install via `pip install requests`)
3. **Slack webhook URL** configured in the script or environment variable
4. **Administrator privileges** to create scheduled tasks

## 🚀 Quick Setup

### Step 1: Run the Setup Script

1. **Open PowerShell as Administrator**:
   - Right-click on PowerShell
   - Select "Run as Administrator"

2. **Navigate to the script directory**:
   ```powershell
   cd "c:\Users\benjamin.liang\Documents\Python"
   ```

3. **Run the setup script**:
   ```powershell
   .\setup_scheduled_task.ps1
   ```

### Step 2: Verify the Task

1. Open **Task Scheduler** (search in Start menu)
2. Navigate to **Task Scheduler Library**
3. Find **"Weekly OC Performance Report"**
4. Right-click > **Run** to test it immediately

## ⚙️ Task Configuration

The scheduled task is configured with:

- **Schedule**: Every Monday at 9:00 AM
- **Script**: `run_weekly_report.bat`
- **Working Directory**: `c:\Users\benjamin.liang\Documents\Python`
- **Run As**: Current user (with highest privileges)
- **Settings**:
  - Runs even if on battery
  - Requires network connection
  - Will retry up to 3 times if it fails (with 5-minute intervals)

## 📝 Manual Execution

You can also run the report manually:

### Option 1: Run the Batch File
```cmd
cd "c:\Users\benjamin.liang\Documents\Python"
run_weekly_report.bat
```

### Option 2: Run Python Directly
```cmd
cd "c:\Users\benjamin.liang\Documents\Python"
py process_and_send_weekly_report.py
```

## 🔧 Modifying the Schedule

To change when the report runs:

1. Open **Task Scheduler**
2. Find **"Weekly OC Performance Report"**
3. Right-click > **Properties**
4. Go to **Triggers** tab
5. Edit the trigger:
   - Change day/time
   - Change frequency (daily, weekly, monthly)
6. Click **OK**

## 📊 Logging

The script logs output to:
- **File**: `weekly_report.log` in the script directory
- **Format**: Timestamped entries with success/failure status

To view logs:
```powershell
Get-Content "c:\Users\benjamin.liang\Documents\Python\weekly_report.log" -Tail 50
```

## 🧪 Testing

### Test the Batch File
```cmd
cd "c:\Users\benjamin.liang\Documents\Python"
run_weekly_report.bat
```

### Test via Task Scheduler
1. Open Task Scheduler
2. Find "Weekly OC Performance Report"
3. Right-click > **Run**
4. Check the **History** tab for execution status

## 🗑️ Removing the Scheduled Task

To remove the scheduled task:

### Option 1: Via PowerShell (as Admin)
```powershell
Unregister-ScheduledTask -TaskName "Weekly OC Performance Report" -Confirm:$false
```

### Option 2: Via Task Scheduler GUI
1. Open Task Scheduler
2. Find "Weekly OC Performance Report"
3. Right-click > **Delete**

## 🔍 Troubleshooting

### Issue: Task doesn't run
**Solutions**:
- Check Task Scheduler History tab for errors
- Verify Python is accessible (`py --version`)
- Check if network is available (task requires network)
- Verify Slack webhook URL is correct

### Issue: "Access Denied" error
**Solution**: Run PowerShell as Administrator when creating the task

### Issue: Script runs but no Slack message
**Solutions**:
- Check `weekly_report.log` for errors
- Verify Slack webhook URL in the script
- Test Slack connection manually
- Check if script has correct data (hardcoded data may need updating)

### Issue: Python not found
**Solution**: 
- Verify Python is installed
- Check if `py` launcher works: `py --version`
- If not, update `run_weekly_report.bat` to use full Python path

## 📅 Recommended Schedule

- **Day**: Monday (to review previous week's performance)
- **Time**: 9:00 AM (start of work week)
- **Frequency**: Weekly

## 📁 Files

- `process_and_send_weekly_report.py` - Main Python script
- `run_weekly_report.bat` - Batch file wrapper for Task Scheduler
- `setup_scheduled_task.ps1` - PowerShell script to create the scheduled task
- `weekly_report.log` - Execution log file (created automatically)
- `README_SCHEDULING.md` - This guide

---

**Last Updated**: November 2025

