# weekly_report

Run the weekly performance report for Outer Cities (OC) and top cities

## Quick Start

**Just type `/weekly_report` in Cursor chat!**

The command will automatically:
1. Execute `process_and_send_weekly_report.py`
2. Process OC overall metrics
3. Process top 5 cities (Johor Bahru, Penang, Kota Kinabalu, Ipoh, Kuching)
4. Process daily metrics
5. Format and send to Slack channel `oc_weekly_performance_update`

## What Gets Sent

The report includes:
- **OC Overall**: Orders, GMV, WTU, Basket, Fulfilment Rate, Sessions, COPS, Promo
- **Top 5 Cities**: Detailed metrics for each city with MoM & YoY comparisons
- **Daily Metrics**: Day-by-day breakdown for the week
- **Key Insights**: Monthly run rate forecasts and performance highlights

## Command Handler

The command uses: `.cursor/commands/weekly_report.py`

This handler script:
- Changes to the correct directory
- Executes the main report script
- Handles errors gracefully
- Shows progress and results

## Manual Execution (Alternative)

If you prefer to run manually:

```bash
cd "c:\Users\benjamin.liang\Documents\Python"
py process_and_send_weekly_report.py
```

Or use the simple wrapper:
```bash
py run_weekly_report_simple.py
```

## Troubleshooting

**Command not found?**
- Make sure you're in the Cursor chat
- Type exactly: `/weekly_report`
- The command should auto-complete

**Script fails?**
- Check `weekly_report.log` for errors
- Verify Python is accessible: `py --version`
- Check Slack webhook URL in the script

**No Slack message?**
- Verify webhook URL is correct
- Check network connection
- Review log file for errors

## Related Commands

- `/weekly-update` - Alternative command name (same functionality)

