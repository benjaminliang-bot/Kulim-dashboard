# Quick Setup Guide: Weekly Report Automation

## 🚀 Quick Start (Using Existing MCP Tools)

Since you're using MCP tools in Cursor, here's the fastest way to set up weekly reports:

### Option 1: Use MCP Server Scheduling (Recommended)

If your organization has MCP server scheduling capabilities, you can set up the weekly report to run automatically through the MCP infrastructure.

### Option 2: Create a Simple Wrapper Script

Create a script that calls the MCP tools or uses your organization's query execution method.

---

## 📝 Step-by-Step Setup

### 1. Get Your Slack Webhook URL

1. Go to https://api.slack.com/apps
2. Create or select your app
3. Enable "Incoming Webhooks"
4. Create webhook for your channel
5. Copy the webhook URL

### 2. Set Environment Variable

**Windows PowerShell:**
```powershell
# Temporary (current session)
$env:SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

# Permanent (user-level)
[System.Environment]::SetEnvironmentVariable('SLACK_WEBHOOK_URL', 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL', 'User')
```

**Windows CMD:**
```cmd
setx SLACK_WEBHOOK_URL "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

**Linux/Mac:**
```bash
# Add to ~/.bashrc or ~/.zshrc
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

### 3. Test Slack Connection

Create a test script `test_slack.py`:

```python
import os
import requests

webhook_url = os.getenv('SLACK_WEBHOOK_URL', '')
if not webhook_url:
    print("ERROR: SLACK_WEBHOOK_URL not set")
    exit(1)

message = {
    "text": "🧪 Test message from Weekly Report Bot",
    "channel": "#food-analytics"
}

response = requests.post(webhook_url, json=message)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    print("✅ Slack connection successful!")
else:
    print(f"❌ Failed: {response.text}")
```

Run: `python test_slack.py`

### 4. Schedule the Report

#### Windows Task Scheduler:

1. Open Task Scheduler
2. Create Basic Task
3. Name: "Weekly OC Penang Report"
4. Trigger: Weekly, Monday, 9:00 AM
5. Action: Start a program
   - Program: `python`
   - Arguments: `weekly_report_automation.py`
   - Start in: `C:\Users\benjamin.liang\Documents\Python`

#### Or use PowerShell to create scheduled task:

```powershell
$action = New-ScheduledTaskAction -Execute "python" -Argument "weekly_report_automation.py" -WorkingDirectory "C:\Users\benjamin.liang\Documents\Python"
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 9:00AM
Register-ScheduledTask -TaskName "Weekly OC Penang Report" -Action $action -Trigger $trigger -Description "Weekly performance report for OC Cities and Penang"
```

---

## 🔧 Implementation Notes

### For MCP Users:

If you're using MCP tools (like in Cursor), you may need to:

1. **Create a wrapper script** that uses your organization's query execution method
2. **Use internal APIs** if available for Presto queries
3. **Set up a service account** with proper permissions

### For Direct Presto Connection:

Modify `weekly_report_automation.py` to use your Presto connection:

```python
from presto.dbapi import connect

def run_presto_query(query: str):
    conn = connect(
        host='your-presto-host',
        port=8080,
        user='your-username',
        catalog='hive',
        schema='ocd_adw'
    )
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [desc[0] for desc in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return results
```

---

## 📧 Alternative: Email Reports

If Slack is not available, you can modify the script to send emails instead:

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_report(oc_report, penang_report):
    # Email configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "your-email@grab.com"
    sender_password = "your-password"
    receiver_email = "benjamin.liang@grab.com"
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Weekly OC & Penang Report"
    
    # Format report as HTML or text
    body = format_report_as_text(oc_report, penang_report)
    msg.attach(MIMEText(body, 'plain'))
    
    # Send email
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)
    server.send_message(msg)
    server.quit()
```

---

## ✅ Verification

After setup, verify:

1. ✅ Script runs without errors
2. ✅ Slack message is received
3. ✅ Scheduled task is created and runs
4. ✅ Reports are generated correctly

---

## 📞 Need Help?

If you encounter issues:
1. Check the logs
2. Verify environment variables
3. Test Slack webhook separately
4. Verify Presto connection separately

---

**Files Created:**
- `weekly_report_automation.py` - Full automation script (needs Presto connection implementation)
- `weekly_report_automation_simple.py` - Simplified template
- `weekly_report_scheduler_setup.md` - Detailed setup guide
- `setup_weekly_report.md` - Quick setup guide (this file)




