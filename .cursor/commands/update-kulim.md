# update-kulim

Update Kulim dashboard - generates SQL query and updates metrics

## Quick Start

**Just type `/update-kulim` in Cursor chat!**

The command will automatically:
1. Generate SQL query for latest Kulim commercial metrics
2. Display the query for execution via MCP tools
3. Show instructions for updating the HTML dashboard

## What It Does

The command executes `update_kulim.py` which:
- Generates SQL query using `area_name = 'Kulim'` (exact match)
- Uses `COUNT(DISTINCT order_id)` for accurate order counting
- Queries `ocd_adw.f_food_metrics` table
- Covers September, October, November 2025

## Output

The command displays:
- **SQL Query**: Ready to execute via Hubble/Presto MCP tools
- **Expected Data Format**: JSON structure for results
- **Instructions**: Step-by-step guide for updating the dashboard

## Manual Execution (Alternative)

If you prefer to run manually:

```bash
py update_kulim.py
```

Or with JSON data to auto-update:

```bash
py update_kulim.py '{"202510": {"total_gmv": 568189.00, ...}}'
```

## Next Steps After Running

1. Copy the SQL query displayed
2. Execute via Hubble/Presto MCP tools
3. Update `kulim_penang_comprehensive_analysis.html` with results
4. Commit and push to GitHub (optional)

## Command Handler

The command uses: `.cursor/commands/update-kulim.py`

This handler script:
- Changes to the correct directory
- Executes `update_kulim.py`
- Handles errors gracefully

## Troubleshooting

**Command not found?**
- Make sure you're in the Cursor chat
- Type exactly: `/update-kulim`
- The command should auto-complete

**Script fails?**
- Verify Python is accessible: `py --version`
- Check that `update_kulim.py` exists in the workspace root
- Ensure you're in the correct directory

