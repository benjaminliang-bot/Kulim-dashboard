# 🚀 Weekly Report Automation - Setup Instructions

## ✅ Status: Ready to Schedule

Your weekly report script is working! Now you need to set up the scheduled task.

## 📋 Quick Setup (3 Steps)

### Step 1: Run as Administrator

You need Administrator privileges to create scheduled tasks. Choose one method:

**Method A: PowerShell (Recommended)**
1. Press `Windows Key + X`
2. Select **"Windows PowerShell (Admin)"** or **"Terminal (Admin)"**
3. Navigate to the script folder:
   ```powershell
   cd "c:\Users\benjamin.liang\Documents\Python"
   ```
4. Run the setup script:
   ```powershell
   .\setup_scheduled_task.ps1
   ```

**Method B: Batch File**
1. Right-click `create_task_simple.bat`
2. Select **"Run as administrator"**
3. Follow the prompts

### Step 2: Verify the Task

1. Open **Task Scheduler** (search in Start menu)
2. Go to **Task Scheduler Library**
3. Find **"Weekly OC Performance Report"**
4. Right-click it > **Run** to test immediately

### Step 3: Check Results

- Check Slack channel `oc_weekly_performance_update` for the report
- Check `weekly_report.log` for execution logs

## 📅 Current Schedule

- **Frequency**: Weekly
- **Day**: Monday
- **Time**: 9:00 AM
- **Script**: `process_and_send_weekly_report.py`

## 🔧 Manual Execution (No Scheduling Needed)

You can run the report anytime:

```cmd
cd "c:\Users\benjamin.liang\Documents\Python"
py process_and_send_weekly_report.py
```

Or use the batch file:

```cmd
cd "c:\Users\benjamin.liang\Documents\Python"
run_weekly_report.bat
```

## 📝 Files Created

1. **`run_weekly_report.bat`** - Batch wrapper for Task Scheduler
2. **`setup_scheduled_task.ps1`** - PowerShell setup script (requires Admin)
3. **`create_task_simple.bat`** - Alternative batch setup (requires Admin)
4. **`README_SCHEDULING.md`** - Detailed scheduling guide
5. **`SETUP_INSTRUCTIONS.md`** - This file

## ⚠️ Important Notes

1. **Admin Rights Required**: Creating scheduled tasks requires Administrator privileges
2. **Network Required**: The task requires network connection (for Slack API)
3. **Python Must Be Available**: Ensure `py` command works in your PATH
4. **Slack Webhook**: Already configured in the script (line 17)

## 🧪 Test Before Scheduling

The script has been tested and works! It successfully:
- ✅ Processed OC and city data
- ✅ Formatted Slack message
- ✅ Sent to Slack channel

## 🔍 Troubleshooting

### "Access Denied" Error
**Solution**: Run the setup script as Administrator (see Step 1)

### Task Doesn't Run
**Check**:
1. Task Scheduler > History tab for errors
2. `weekly_report.log` file for script errors
3. Network connection (required for Slack)

### No Slack Message Received
**Check**:
1. Slack webhook URL in script (line 17)
2. Slack channel permissions
3. Log file for error messages

## 📊 What Gets Scheduled

The task will:
1. Run `run_weekly_report.bat` every Monday at 9:00 AM
2. Execute `process_and_send_weekly_report.py`
3. Send formatted report to Slack
4. Log results to `weekly_report.log`

## 🎯 Next Steps

1. **Run setup as Administrator** (see Step 1 above)
2. **Test the task** (right-click > Run in Task Scheduler)
3. **Verify Slack message** arrives
4. **Monitor first few runs** to ensure reliability

---

**Ready to schedule?** Follow Step 1 above! 🚀

