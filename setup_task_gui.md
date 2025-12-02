
# 📅 Manual Task Scheduler Setup (No Admin Scripts Needed!)

If you can't run PowerShell scripts, use the **Task Scheduler GUI** instead:

## 🎯 Step-by-Step GUI Setup

### Step 1: Open Task Scheduler
1. Press `Windows Key + R`
2. Type: `taskschd.msc`
3. Press Enter

### Step 2: Create Basic Task
1. In the right panel, click **"Create Basic Task..."**
2. Name: `Weekly OC Performance Report`
3. Description: `Automated weekly report for Outer Cities performance metrics`
4. Click **Next**

### Step 3: Set Trigger
1. Select **"Weekly"**
2. Click **Next**
3. Set:
   - **Start date**: Today's date (or next Monday)
   - **Time**: `9:00:00 AM`
   - **Recur every**: `1` weeks
   - **On**: Check **Monday** only
4. Click **Next**

### Step 4: Set Action
1. Select **"Start a program"**
2. Click **Next**
3. Fill in:
   - **Program/script**: `C:\Users\benjamin.liang\Documents\Python\run_weekly_report.bat`
   - **Start in**: `C:\Users\benjamin.liang\Documents\Python`
4. Click **Next**

### Step 5: Finish
1. Review the summary
2. Check **"Open the Properties dialog for this task when I click Finish"**
3. Click **Finish**

### Step 6: Configure Advanced Settings
In the Properties window:

**General Tab:**
- ✅ Check **"Run whether user is logged on or not"** (optional)
- ✅ Check **"Run with highest privileges"** (if available)
- Select **"Configure for: Windows 10"**

**Conditions Tab:**
- ✅ Check **"Start the task only if the computer is on AC power"** (uncheck if you want it on battery)
- ✅ Check **"Start the task only if the following network connection is available"** → Select **"Any connection"**

**Settings Tab:**
- ✅ Check **"Allow task to be run on demand"**
- ✅ Check **"Run task as soon as possible after a scheduled start is missed"**
- ✅ Check **"If the task fails, restart every"** → Set to `5 minutes` → Set **"Attempt to restart up to"** → `3 times`

**Actions Tab:**
- Verify the action points to: `C:\Users\benjamin.liang\Documents\Python\run_weekly_report.bat`
- **Start in**: `C:\Users\benjamin.liang\Documents\Python`

Click **OK**

### Step 7: Test It!
1. Find your task in the Task Scheduler Library
2. Right-click **"Weekly OC Performance Report"**
3. Select **"Run"**
4. Check `weekly_report.log` to verify it worked

## ✅ Done!

Your task is now scheduled to run every Monday at 9:00 AM!

## 🔍 Verify It's Working

1. **Check Task Status**: Task Scheduler → Find your task → Check "Last Run Result" (should be "0x0" for success)
2. **Check Logs**: Open `C:\Users\benjamin.liang\Documents\Python\weekly_report.log`
3. **Check Slack**: Look for the report in your Slack channel

## 🛠️ Troubleshooting

**Task shows "Last Run Result: 0x1" (Failed)**
- Check `weekly_report.log` for errors
- Verify Python is accessible: Open CMD, type `py --version`
- Verify the batch file path is correct

**Task doesn't run automatically**
- Check Task Scheduler → History tab for errors
- Verify the trigger is set correctly (Monday, 9:00 AM)
- Check if your computer is on at that time

**No Slack message**
- Check `weekly_report.log` for errors
- Verify Slack webhook URL in the script
- Test manually: `py process_and_send_weekly_report.py`

---

**That's it!** No admin scripts needed - just use the GUI! 🎉

