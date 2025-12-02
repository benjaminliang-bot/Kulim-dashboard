# Weekly Report Automation in Cursor - Quick Guide

## 🚀 Quick Start

### Step 1: Set Slack Webhook URL

Set your Slack webhook URL:

```python
# In cursor_weekly_report_workflow.py, update:
SLACK_WEBHOOK_URL = 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL'
```

Or set environment variable:
```powershell
$env:SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

### Step 2: Run the Workflow in Cursor

In Cursor, you can run the weekly report in two ways:

#### Option A: Use Cursor Chat (Recommended)

Simply ask in Cursor chat:
```
"Run the weekly report for OC and Penang and send to Slack"
```

I'll execute the queries using MCP tools and send the report to Slack.

#### Option B: Manual Execution

1. **Get the queries**:
   ```python
   from cursor_weekly_report_workflow import get_oc_query, get_penang_query, get_week_dates
   
   this_week_start, this_week_end, last_week_start, last_week_end = get_week_dates()
   oc_query = get_oc_query(this_week_start, this_week_end, last_week_start, last_week_end)
   penang_query = get_penang_query(this_week_start, this_week_end, last_week_start, last_week_end)
   ```

2. **Execute queries via MCP tools** (in Cursor chat):
   - Use MCP tools to execute `oc_query`
   - Use MCP tools to execute `penang_query`
   - Store results in variables

3. **Process and send**:
   ```python
   from cursor_weekly_report_workflow import process_query_results, format_slack_message, send_to_slack
   
   oc_report = process_query_results(oc_results)
   penang_report = process_query_results(penang_results)
   
   slack_message = format_slack_message(
       oc_report, penang_report,
       this_week_start, this_week_end,
       last_week_start, last_week_end
   )
   
   send_to_slack(slack_message)
   ```

## ⏰ Scheduling in Cursor

### Option 1: Ask in Cursor Chat (Easiest)

Simply ask me in Cursor chat every week:
```
"Run the weekly report for OC and Penang"
```

I'll execute the queries, process the results, and send to Slack automatically.

### Option 2: Create a Cursor Task

If Cursor supports tasks, create a task that runs the workflow script.

### Option 3: Set a Reminder

Set a weekly reminder in your calendar to run the report in Cursor.

## 📊 What the Report Includes

### OC Cities Section:
- Orders (with growth %)
- GMV (MYR) (with growth %)
- WTU (with growth %)
- Basket Size (with growth %)
- Completion Rate (with delta)
- Sessions (with growth %)
- COPS (with delta)
- Promo Penetration (with delta)

### Penang Section:
- Same metrics as OC Cities

## 🔧 Troubleshooting

### Issue: "SLACK_WEBHOOK_URL not set"
**Solution**: Set the environment variable or update the script

### Issue: "MCP query failed"
**Solution**: 
- Check MCP server connection
- Verify query syntax
- Check date ranges

### Issue: "No results returned"
**Solution**:
- Verify data exists for the date ranges
- Check query filters (city_id, business_type, etc.)
- Verify table permissions

## 💡 Tips

1. **Save queries**: The queries are generated automatically each week
2. **Test first**: Always test manually before scheduling
3. **Monitor logs**: Check for errors in execution
4. **Verify dates**: Ensure date ranges are correct (Monday-Sunday)

## 📅 Recommended Schedule

- **Day**: Monday (to review previous week)
- **Time**: 9:00 AM (start of work week)
- **Frequency**: Weekly

---

**Files:**
- `cursor_weekly_report_workflow.py` - Main workflow script
- `CURSOR_WEEKLY_REPORT_GUIDE.md` - This guide

**Last Updated**: November 2025



