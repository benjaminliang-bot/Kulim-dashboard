# Weekly Report Automation in Cursor

This guide shows you how to run weekly reports directly within Cursor using MCP tools.

## 🚀 Quick Start

### Step 1: Set Slack Webhook URL

Set your Slack webhook URL as an environment variable or in the script:

```python
# In cursor_weekly_report.py, update:
SLACK_WEBHOOK_URL = 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL'
```

Or set environment variable:
```powershell
$env:SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

### Step 2: Run the Report

In Cursor, you can run the weekly report in two ways:

#### Option A: Use Cursor's Command Palette

1. Open Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P`)
2. Type "Run Python File" or "Execute Python Script"
3. Select `cursor_weekly_report.py`

#### Option B: Use Cursor's Terminal

1. Open terminal in Cursor (`Ctrl+`` or `Cmd+``)
2. Run: `python cursor_weekly_report.py`

### Step 3: Execute Queries via MCP Tools

Since the script uses MCP tools, you'll need to:

1. **Get the queries** from `generate_oc_report()` and `generate_penang_report()`
2. **Execute them using MCP tools** in Cursor
3. **Process the results** using `process_query_results()`
4. **Format and send** using `format_slack_message()` and `send_to_slack()`

## 📝 Manual Execution Workflow

Here's the step-by-step process to run the weekly report:

### 1. Get Date Ranges

```python
from cursor_weekly_report import get_week_dates
this_week_start, this_week_end, last_week_start, last_week_end = get_week_dates()
print(f"This Week: {this_week_start} - {this_week_end}")
print(f"Last Week: {last_week_start} - {last_week_end}")
```

### 2. Execute OC Report Query

Use MCP tools in Cursor to execute the OC report query:

```python
# The query is in generate_oc_report() function
# Execute it via MCP mcp-hubble server
# Store results in oc_results variable
```

### 3. Execute Penang Report Query

Use MCP tools in Cursor to execute the Penang report query:

```python
# The query is in generate_penang_report() function
# Execute it via MCP mcp-hubble server
# Store results in penang_results variable
```

### 4. Process Results

```python
from cursor_weekly_report import process_query_results

oc_report = process_query_results(oc_results)
penang_report = process_query_results(penang_results)
```

### 5. Format and Send to Slack

```python
from cursor_weekly_report import format_slack_message, send_to_slack

slack_message = format_slack_message(
    oc_report, 
    penang_report,
    this_week_start,
    this_week_end,
    last_week_start,
    last_week_end
)

success = send_to_slack(slack_message)
```

## 🔄 Automated Execution Script

For easier execution, create a helper script that uses MCP tools:

```python
# run_weekly_report_helper.py
from cursor_weekly_report import *
import subprocess
import json

def execute_mcp_query(query):
    """
    Execute query using MCP tools
    This is a placeholder - adjust based on your MCP setup
    """
    # Use your MCP tool execution method here
    # For example, if you have a CLI tool:
    # result = subprocess.run(['mcp', 'query', query], capture_output=True)
    # return json.loads(result.stdout)
    pass

def run_weekly_report():
    """Run the complete weekly report workflow"""
    # Get dates
    this_week_start, this_week_end, last_week_start, last_week_end = get_week_dates()
    
    # Get queries
    oc_query = generate_oc_report(this_week_start, this_week_end, last_week_start, last_week_end)
    penang_query = generate_penang_report(this_week_start, this_week_end, last_week_start, last_week_end)
    
    # Execute queries (via MCP)
    oc_results = execute_mcp_query(oc_query)
    penang_results = execute_mcp_query(penang_query)
    
    # Process results
    oc_report = process_query_results(oc_results)
    penang_report = process_query_results(penang_results)
    
    # Format and send
    slack_message = format_slack_message(
        oc_report, penang_report,
        this_week_start, this_week_end,
        last_week_start, last_week_end
    )
    
    success = send_to_slack(slack_message)
    return success

if __name__ == '__main__':
    run_weekly_report()
```

## ⏰ Scheduling in Cursor

### Option 1: Cursor Tasks (if available)

If Cursor supports tasks, create a `.cursor/tasks.json`:

```json
{
  "tasks": [
    {
      "label": "Weekly Report",
      "type": "shell",
      "command": "python cursor_weekly_report.py",
      "schedule": "0 9 * * 1"
    }
  ]
}
```

### Option 2: Use Cursor's Built-in Scheduler

If Cursor has a built-in scheduler, configure it to run the script weekly.

### Option 3: External Scheduler

Use Windows Task Scheduler or cron to run the script, but execute it within Cursor's environment.

## 🧪 Testing

Before scheduling, test the report:

1. **Test Slack Connection**:
   ```python
   from cursor_weekly_report import send_to_slack
   test_message = {"text": "🧪 Test message", "channel": "#food-analytics"}
   send_to_slack(test_message)
   ```

2. **Test Query Execution**:
   - Run a simple query via MCP tools
   - Verify results are returned correctly

3. **Test Full Workflow**:
   - Run the complete workflow manually
   - Verify Slack message is received

## 📊 Report Format

The Slack message includes:

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

1. **Save queries**: Save the generated queries for reference
2. **Test first**: Always test manually before scheduling
3. **Monitor logs**: Check for errors in execution
4. **Verify dates**: Ensure date ranges are correct (Monday-Sunday)

## 📅 Recommended Schedule

- **Day**: Monday (to review previous week)
- **Time**: 9:00 AM (start of work week)
- **Frequency**: Weekly

---

**Files:**
- `cursor_weekly_report.py` - Main report script
- `run_weekly_report.md` - This guide

**Last Updated**: November 2025



