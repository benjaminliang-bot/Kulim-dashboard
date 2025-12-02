# 🚀 Quick Start: Weekly Report Command

## ✅ Setup Complete!

Your `/weekly-update` command is ready to use!

## 🎯 How to Use

**In Cursor chat, simply type:**
```
/weekly-update
```

The command will:
1. ✅ Execute the weekly report script
2. ✅ Process all OC and city data
3. ✅ Format and send to Slack
4. ✅ Show you the results

## 📋 What Happens

When you type `/weekly-update`, the system will:

1. **Run** `process_and_send_weekly_report.py`
2. **Process**:
   - OC Overall metrics (Orders, GMV, WTU, Basket, etc.)
   - Top 5 Cities (Johor Bahru, Penang, Kota Kinabalu, Ipoh, Kuching)
   - Daily metrics breakdown
3. **Calculate**:
   - MoM (Month-over-Month) comparisons
   - YoY (Year-over-Year) comparisons
   - Monthly run rate forecasts
4. **Send** formatted report to Slack channel `oc_weekly_performance_update`

## 🧪 Test It Now!

1. Open Cursor
2. Open chat (usually `Ctrl+L` or `Cmd+L`)
3. Type: `/weekly-update`
4. Press Enter

You should see the report execute and get sent to Slack!

## 📁 Files Created

- ✅ `.cursor/commands/weekly-update.py` - Command handler (tested & working)
- ✅ `.cursor/commands/weekly-update.md` - Command documentation
- ✅ `CURSOR_COMMAND_SETUP.md` - Detailed setup guide
- ✅ `QUICK_START.md` - This file

## 🔍 Verification

The command handler has been tested and works correctly:
- ✅ Finds the correct script path
- ✅ Executes the report script
- ✅ Sends to Slack successfully

## 💡 Tips

1. **Use autocomplete**: Type `/` and Cursor will suggest commands
2. **Check Slack**: The report appears in `oc_weekly_performance_update` channel
3. **Check logs**: Review `weekly_report.log` if needed

## 🎉 Ready to Use!

Just type `/weekly-update` in Cursor chat and you're done! 🚀

---

**Need help?** Check `CURSOR_COMMAND_SETUP.md` for detailed troubleshooting.

