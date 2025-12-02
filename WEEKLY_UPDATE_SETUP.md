# Weekly Update Command Setup - `/weekly-update`

## ✅ Setup Complete!

The `/weekly-update` command has been created and is ready to use.

## 📋 What It Does

When you type `/weekly-update` in Cursor chat, it will:

1. **Calculate Date Ranges** - Automatically determines:
   - This Week: Monday to Sunday of current week
   - Last Week: Previous Monday to Sunday

2. **Execute 4 Queries**:
   - **OC Cities Overall** - Weekly metrics comparison
   - **Top 5 Cities by GMV** - Top performing cities in OC
   - **Daily Metrics** - Day-by-day breakdown for this week
   - **Penang** - Weekly metrics comparison

3. **Process Results** - Calculates:
   - Growth percentages
   - Deltas and changes
   - Formatted metrics

4. **Format Report** - Creates enhanced Slack message with:
   - OC Cities overall section
   - Top 5 cities by GMV table
   - Daily metrics table
   - Penang section

5. **Send to Slack** - Automatically sends formatted report

## 🚀 How to Use

Simply type in Cursor chat:
```
/weekly-update
```

I'll automatically:
- Calculate current week dates
- Execute all queries via MCP tools
- Process all results
- Format the enhanced report
- Send to Slack

## 📊 Report Sections

### 1. OC Cities - Overall
- Orders, GMV, WTU, Basket Size
- Completion Rate, Sessions, COPS
- Promo Penetration
- All with week-over-week growth percentages

### 2. Top 5 Cities by GMV (OC)
- City name, GMV, Growth percentage
- Ranked by this week's GMV

### 3. Daily Metrics (This Week)
- Day-by-day breakdown (Mon-Sun)
- Orders, GMV, WTU for each day

### 4. Penang
- Same metrics as OC Cities
- Week-over-week comparison

## ⚙️ Configuration

### Slack Webhook URL

Currently configured in `execute_weekly_update.py`:
```python
SLACK_WEBHOOK_URL = 'https://hooks.slack.com/services/aaaajqkcgywrijyttf45nfhyma'
```

To change, update the script or set environment variable:
```powershell
$env:SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

### Slack Channel

Default: `#food-analytics`

To change:
```python
SLACK_CHANNEL = '#your-channel'
```

## 📁 Files Created

1. **`.cursor/commands/weekly-update.md`** - Command definition
2. **`execute_weekly_update.py`** - Main execution script
3. **`generate_weekly_report_queries.py`** - Query generator
4. **`weekly_report_queries_current.sql`** - Generated queries with current dates
5. **`WEEKLY_UPDATE_COMMAND_README.md`** - Detailed documentation

## 🔄 Current Week Dates

The command automatically calculates dates:
- **This Week**: Nov 03 - Nov 09, 2025
- **Last Week**: Oct 27 - Nov 02, 2025

Dates are recalculated each time the command runs.

## 📝 Example Usage

```
You: /weekly-update

Auto: 📊 Generating weekly report...
      📅 Calculating date ranges...
      🔍 Executing OC Cities query...
      🔍 Executing Top 5 Cities query...
      🔍 Executing Daily Metrics query...
      🔍 Executing Penang query...
      📊 Processing results...
      📝 Formatting report...
      📤 Sending to Slack...
      ✅ Weekly report sent successfully!
```

## 🎯 Next Steps

1. **Test the Command**: Type `/weekly-update` in Cursor chat
2. **Verify Execution**: Check that all queries execute successfully
3. **Check Slack**: Verify the formatted report appears in your channel
4. **Schedule Reminders**: Set up weekly reminders to run the command

## 🔧 Troubleshooting

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

---

**Command**: `/weekly-update`  
**Status**: ✅ Ready to use  
**Last Updated**: November 2025



