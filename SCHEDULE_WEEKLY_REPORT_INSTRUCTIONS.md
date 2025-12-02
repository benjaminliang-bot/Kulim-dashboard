# Schedule Weekly Report - Instructions

## Option 1: Using Task Scheduler GUI (Recommended - No Admin Required)

1. **Open Task Scheduler**
   - Press `Win + R`, type `taskschd.msc`, press Enter
   - Or search "Task Scheduler" in Start menu

2. **Create Basic Task**
   - Click "Create Basic Task..." in the right panel
   - Name: `OC Weekly Performance Report`
   - Description: `Automatically runs OC Weekly Performance Report every Monday`

3. **Set Trigger**
   - Select "Weekly"
   - Click Next
   - Check "Monday"
   - Set time: `9:00 AM` (or your preferred time)
   - Click Next

4. **Set Action**
   - Select "Start a program"
   - Click Next
   - Program/script: `py` (or full path: `C:\Users\benjamin.liang\AppData\Local\Programs\Python\Python313\python.exe`)
   - Add arguments: `"c:\Users\benjamin.liang\Documents\Python\process_and_send_weekly_report.py"`
   - Start in: `c:\Users\benjamin.liang\Documents\Python`
   - Click Next

5. **Review and Finish**
   - Review settings
   - Check "Open the Properties dialog for this task when I click Finish"
   - Click Finish

6. **Configure Advanced Settings** (in Properties dialog)
   - General tab:
     - Check "Run whether user is logged on or not" (optional)
     - Check "Run with highest privileges" (if needed)
   - Conditions tab:
     - Uncheck "Start the task only if the computer is on AC power" (if you want it to run on battery)
     - Check "Start the task only if the following network connection is available" (if needed)
   - Settings tab:
     - Check "Allow task to be run on demand"
     - Check "Run task as soon as possible after a scheduled start is missed"
   - Click OK

7. **Test the Task**
   - Right-click the task → "Run"
   - Check if the report is sent to Slack

## Option 2: Using PowerShell (Requires Admin)

If you have administrator privileges, you can run:

```powershell
powershell -ExecutionPolicy Bypass -File schedule_weekly_report.ps1
```

Or run PowerShell as Administrator and execute:
```powershell
cd c:\Users\benjamin.liang\Documents\Python
.\schedule_weekly_report.ps1
```

## Option 3: Using Batch File

You can also schedule `run_weekly_report.bat` instead of the Python script directly:

1. Follow Option 1 steps above
2. In "Start a program" step:
   - Program/script: `c:\Users\benjamin.liang\Documents\Python\run_weekly_report.bat`
   - No arguments needed

## Verify Task is Scheduled

To check if the task is scheduled:
```powershell
Get-ScheduledTask -TaskName "OC Weekly Performance Report"
```

To test the task manually:
```powershell
Start-ScheduledTask -TaskName "OC Weekly Performance Report"
```

To view task history:
- Open Task Scheduler
- Find your task
- Click "History" tab

## Troubleshooting

1. **Task doesn't run**
   - Check Task Scheduler → Task Scheduler Library → Your task → History tab for errors
   - Verify Python path is correct
   - Check if script path is correct

2. **Permission errors**
   - Make sure the task is set to run with your user account
   - Check "Run with highest privileges" if needed

3. **Script not found**
   - Verify the script path: `c:\Users\benjamin.liang\Documents\Python\process_and_send_weekly_report.py`
   - Make sure Python is in PATH or use full Python path

4. **Slack not receiving messages**
   - Check if SLACK_WEBHOOK_URL is set correctly in the script
   - Test the script manually first: `py process_and_send_weekly_report.py`

## Current Schedule

- **Frequency**: Every Monday
- **Time**: 9:00 AM (you can change this)
- **Script**: `process_and_send_weekly_report.py`
- **Location**: `c:\Users\benjamin.liang\Documents\Python`


