# ✅ Cursor Command Setup Complete!

## 🎯 How to Use

**Simply type in Cursor chat:**
```
/weekly-update
```

That's it! The command will automatically run your weekly report and send it to Slack.

## 📋 What Was Set Up

1. **Command Handler**: `.cursor/commands/weekly-update.py`
   - Automatically executes the weekly report script
   - Handles directory changes and error handling

2. **Command Documentation**: `.cursor/commands/weekly-update.md`
   - Provides command description and usage
   - Available in Cursor's command palette

## 🚀 Testing the Command

1. **Open Cursor**
2. **Open the chat** (usually `Ctrl+L` or `Cmd+L`)
3. **Type**: `/weekly-update`
4. **Press Enter**

The command should:
- ✅ Execute the Python script
- ✅ Process all data
- ✅ Send report to Slack
- ✅ Show success message

## 🔍 How It Works

When you type `/weekly-update`:

1. Cursor recognizes the command
2. Executes `.cursor/commands/weekly-update.py`
3. The handler script:
   - Changes to the correct directory
   - Runs `process_and_send_weekly_report.py`
   - Returns success/failure status

## 📝 Command Details

**Command Name**: `weekly-update`  
**Handler**: `.cursor/commands/weekly-update.py`  
**Main Script**: `process_and_send_weekly_report.py`  
**Output**: Slack channel `oc_weekly_performance_update`

## 🛠️ Troubleshooting

### Command Not Appearing?

1. **Restart Cursor** - Commands are loaded on startup
2. **Check file location** - Ensure files are in `.cursor/commands/`
3. **Verify syntax** - Command name should match filename

### Command Runs But Fails?

1. **Check Python path** - Verify `py` command works
2. **Check script location** - Ensure `process_and_send_weekly_report.py` exists
3. **Check logs** - Review `weekly_report.log` for errors

### Command Not Executing?

1. **Check permissions** - Ensure Python scripts can execute
2. **Test manually** - Run `py process_and_send_weekly_report.py` directly
3. **Check Cursor settings** - Verify command execution is enabled

## 💡 Pro Tips

1. **Use autocomplete** - Type `/` and Cursor will show available commands
2. **Check command history** - Previous commands are saved
3. **Combine with other commands** - Use in workflows

## ✅ Setup Complete!

Your `/weekly-update` command is ready to use!

**Try it now**: Open Cursor chat and type `/weekly-update` 🚀

---

**Files Created:**
- `.cursor/commands/weekly-update.py` - Command handler
- `.cursor/commands/weekly-update.md` - Command documentation (updated)
- `CURSOR_COMMAND_SETUP.md` - This guide

