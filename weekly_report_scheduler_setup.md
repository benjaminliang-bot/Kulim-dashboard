# Weekly Report Automation Setup Guide

This guide will help you set up automated weekly reports for OC Cities and Penang that are sent to Slack every week.

---

## 📋 Prerequisites

1. **Python 3.7+** installed
2. **Slack Webhook URL** (see setup instructions below)
3. **Presto/Hubble Database Access** (your organization's connection method)
4. **Required Python packages**: `requests`, `pandas`

---

## 🔧 Step 1: Install Dependencies

```bash
pip install requests pandas
```

If you're using Presto Python client:
```bash
pip install presto-python-client
```

---

## 🔗 Step 2: Set Up Slack Webhook

1. **Go to Slack App Directory**: https://api.slack.com/apps
2. **Create a New App** or use existing app
3. **Enable Incoming Webhooks**:
   - Go to "Incoming Webhooks" in your app settings
   - Toggle "Activate Incoming Webhooks" to ON
   - Click "Add New Webhook to Workspace"
   - Select your channel (e.g., `#food-analytics`)
   - Copy the webhook URL

4. **Set Environment Variable**:
   ```bash
   # Windows PowerShell
   $env:SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
   
   # Windows CMD
   set SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
   
   # Linux/Mac
   export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
   ```

   Or add to your script:
   ```python
   SLACK_WEBHOOK_URL = 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL'
   ```

---

## 🗄️ Step 3: Configure Presto Connection

Edit `weekly_report_automation.py` and implement the `get_presto_connection()` and `run_presto_query()` functions based on your organization's setup.

### Option A: Using Presto Python Client

```python
from presto.dbapi import connect

def get_presto_connection():
    conn = connect(
        host='your-presto-host.grab.com',
        port=8080,
        user='your-username',
        catalog='hive',
        schema='ocd_adw'
    )
    return conn

def run_presto_query(query: str) -> List[Dict]:
    conn = get_presto_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [desc[0] for desc in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return results
```

### Option B: Using Your Organization's Query Tool

If your organization has a specific query execution method (e.g., via MCP tools, internal API), implement that in `run_presto_query()`.

---

## ⏰ Step 4: Schedule the Report

### Option A: Windows Task Scheduler

1. **Open Task Scheduler** (search "Task Scheduler" in Windows)

2. **Create Basic Task**:
   - Name: "Weekly OC & Penang Report"
   - Description: "Weekly performance report for OC Cities and Penang"
   - Trigger: Weekly
   - Day: Monday (or your preferred day)
   - Time: 9:00 AM (or your preferred time)

3. **Action**: Start a program
   - Program: `python` (or full path to python.exe)
   - Arguments: `C:\Users\benjamin.liang\Documents\Python\weekly_report_automation.py`
   - Start in: `C:\Users\benjamin.liang\Documents\Python`

4. **Conditions** (optional):
   - Uncheck "Start the task only if the computer is on AC power"
   - Check "Wake the computer to run this task" (if needed)

5. **Settings**:
   - Check "Allow task to be run on demand"
   - Check "Run task as soon as possible after a scheduled start is missed"

### Option B: Linux/Mac Cron Job

1. **Open crontab**:
   ```bash
   crontab -e
   ```

2. **Add cron job** (runs every Monday at 9:00 AM):
   ```bash
   0 9 * * 1 cd /path/to/your/script && /usr/bin/python3 weekly_report_automation.py >> weekly_report.log 2>&1
   ```

   Or if you want to run at a specific time:
   ```bash
   # Run every Monday at 9:00 AM
   0 9 * * 1 /usr/bin/python3 /path/to/weekly_report_automation.py
   ```

### Option C: Cloud Scheduling (AWS, GCP, Azure)

#### AWS Lambda + EventBridge
1. Package script as Lambda function
2. Create EventBridge rule for weekly schedule
3. Set Lambda function as target

#### Google Cloud Functions + Cloud Scheduler
1. Deploy script as Cloud Function
2. Create Cloud Scheduler job for weekly schedule
3. Set Cloud Function as target

#### Azure Functions + Timer Trigger
1. Deploy script as Azure Function
2. Configure timer trigger for weekly schedule

---

## 🧪 Step 5: Test the Script

Before scheduling, test the script manually:

```bash
python weekly_report_automation.py
```

**Expected Output:**
```
============================================================
Weekly Report Automation - OC Cities & Penang
============================================================

📅 Date Ranges:
   This Week: 20251104 - 20251110
   Last Week: 20251028 - 20251103

📊 Generating OC Cities Report...
   ✅ OC Cities report generated

📊 Generating Penang Report...
   ✅ Penang report generated

📤 Sending reports to Slack...
✅ Successfully sent message to Slack

✅ Weekly reports sent successfully!
```

---

## 📝 Step 6: Customization

### Change Report Day/Time

- **Windows**: Edit Task Scheduler trigger
- **Linux/Mac**: Edit cron job schedule
- **Cloud**: Edit scheduler configuration

### Change Slack Channel

Set environment variable:
```bash
export SLACK_CHANNEL="#your-channel"
```

Or edit in script:
```python
SLACK_CHANNEL = '#your-channel'
```

### Add More Metrics

Edit the `generate_oc_report()` and `generate_penang_report()` functions to include additional metrics.

### Add Email Notifications

Add email sending functionality using `smtplib` or a service like SendGrid.

---

## 🔍 Troubleshooting

### Issue: "SLACK_WEBHOOK_URL not set"
**Solution**: Set the environment variable or update the script with your webhook URL.

### Issue: "Failed to connect to Presto"
**Solution**: 
- Check your network connection
- Verify Presto host and credentials
- Test connection manually

### Issue: "No results returned from query"
**Solution**:
- Check date ranges (ensure data exists for those dates)
- Verify query syntax
- Check table permissions

### Issue: "Slack message not received"
**Solution**:
- Verify webhook URL is correct
- Check Slack app permissions
- Verify channel name is correct
- Check Slack webhook status

---

## 📊 Report Format

The Slack message will include:

### OC Cities Section:
- Orders (with growth %)
- GMV (MYR) (with growth %)
- Eaters/WTU (with growth %)
- Basket Size (with growth %)
- Completion Rate (with delta)
- Sessions (with growth %)
- COPS (with delta)
- Promo Penetration (with delta)

### Penang Section:
- Same metrics as OC Cities

---

## 📅 Schedule Recommendations

- **Recommended Day**: Monday (to review previous week)
- **Recommended Time**: 9:00 AM (start of work week)
- **Frequency**: Weekly

---

## 🔐 Security Notes

1. **Never commit** webhook URLs or credentials to version control
2. **Use environment variables** for sensitive information
3. **Restrict file permissions** on script files
4. **Use secure connections** (HTTPS) for all API calls

---

## 📞 Support

If you encounter issues:
1. Check the logs (if logging is enabled)
2. Verify all prerequisites are met
3. Test each component individually (Presto connection, Slack webhook)
4. Check network/firewall settings

---

**Last Updated**: November 2025  
**Script Location**: `weekly_report_automation.py`  
**Configuration File**: Update script with your specific connection details




