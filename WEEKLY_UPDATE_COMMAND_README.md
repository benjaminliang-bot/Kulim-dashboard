# Weekly Update Command - `/weekly-update`

## Overview

The `/weekly-update` command in Cursor will automatically generate and send the enhanced weekly report for OC Cities and Penang to Slack.

## What It Does

When you type `/weekly-update` in Cursor chat, it will:

1. **Calculate Date Ranges** - Automatically determines this week (Monday-Sunday) and last week
2. **Execute 4 Queries**:
   - OC Cities Overall (weekly metrics comparison)
   - Top 5 Cities by GMV (OC)
   - Daily Metrics (day-by-day breakdown for this week)
   - Penang (weekly metrics comparison)
3. **Process Results** - Calculates growth percentages, deltas, and formats data
4. **Format Report** - Creates an enhanced Slack message with all sections
5. **Send to Slack** - Automatically sends the formatted report to your Slack channel

## Report Sections

### 1. OC Cities - Overall
- Orders, GMV, WTU, Basket Size
- Completion Rate, Sessions, COPS
- Promo Penetration
- All with week-over-week growth percentages

### 2. Top 5 Cities by GMV (OC)
- City name, GMV, Growth percentage
- Ranked by this week's GMV

### 3. Daily Metrics (This Week)
- Day-by-day breakdown
- Orders, GMV, WTU for each day

### 4. Penang
- Same metrics as OC Cities
- Week-over-week comparison

## Usage

Simply type in Cursor chat:
```
/weekly-update
```

The command will automatically:
- Calculate current week dates
- Execute all queries
- Process results
- Send formatted report to Slack

## Configuration

### Slack Webhook URL

The script uses the Slack webhook URL configured in `execute_weekly_update.py`:
```python
SLACK_WEBHOOK_URL = 'https://hooks.slack.com/services/aaaajqkcgywrijyttf45nfhyma'
```

Or set as environment variable:
```powershell
$env:SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

### Slack Channel

Default channel: `#food-analytics`

To change, update in script or set environment variable:
```python
SLACK_CHANNEL = '#your-channel'
```

## Files

- `.cursor/commands/weekly-update.md` - Command definition
- `execute_weekly_update.py` - Main execution script
- `generate_weekly_report_queries.py` - Query generator
- `weekly_report_queries_current.sql` - Generated queries with current dates

## Date Calculation

The command automatically calculates:
- **This Week**: Monday to Sunday of current week
- **Last Week**: Previous Monday to Sunday

Dates are formatted as `YYYYMMDD` for query execution.

## Example Output

The Slack message will include:

```
📊 Weekly Performance Report
Period: This Week (Nov 03 - Nov 09) vs Last Week (Oct 27 - Nov 02)

🏙️ Outer Cities (OC) - Overall
Orders: 1.9M (+9.6%)
GMV (MYR): 70.0M (+17.0%)
WTU: 848.4K (+6.2%)
...

🏆 Top 5 Cities by GMV (OC)
1. City A | 10.5M | 🚀 +15.2%
2. City B | 8.3M | ✅ +12.1%
...

📅 Daily Metrics (This Week)
Mon | 250K | 8.5M | 120K
Tue | 270K | 9.2M | 130K
...

🏝️ Penang
Orders: 317.5K (+17.2%)
GMV (MYR): 12.9M (+34.7%)
...
```

## Troubleshooting

### Command Not Found
- Make sure `.cursor/commands/weekly-update.md` exists
- Restart Cursor if needed

### Queries Not Executing
- Check MCP tools are available in Cursor
- Verify query syntax in `weekly_report_queries_current.sql`

### Slack Not Receiving Messages
- Verify `SLACK_WEBHOOK_URL` is correct
- Check Slack webhook is active
- Verify channel name is correct

## Next Steps

1. **Test the Command**: Type `/weekly-update` in Cursor chat
2. **Verify Queries**: Check that all 4 queries execute successfully
3. **Check Slack**: Verify the formatted report appears in your channel
4. **Schedule**: Set up weekly reminders to run the command

---

**Last Updated**: November 2025  
**Command**: `/weekly-update`  
**Script**: `execute_weekly_update.py`



