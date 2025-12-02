# MCP Integration Guide for Weekly Report

## Overview

The weekly report script has been set up to execute live SQL queries via MCP Hubble tools. The integration is ready, but requires execution through Cursor's chat interface where MCP tools are available.

## Current Status

✅ **Query Generation**: Complete - generates SQL queries with New Pax calculation
✅ **MCP Integration**: Ready - function structure in place
⚠️ **Direct Execution**: Requires Cursor chat interface

## How MCP Tools Work in Cursor

MCP (Model Context Protocol) tools in Cursor are available through the chat interface, not directly from Python code. When you run commands in Cursor chat, the AI assistant can call MCP tools on your behalf.

## Execution Methods

### Method 1: Execute via Cursor Chat (Recommended)

When you type `/weekly_report` in Cursor chat, the AI will:
1. Generate the SQL queries
2. Execute them via MCP Hubble tool
3. Process the results
4. Send to Slack

**This is the recommended approach** - the MCP tools are automatically available in Cursor chat.

### Method 2: Manual Query Execution

1. Run the script to generate queries:
   ```bash
   py process_and_send_weekly_report.py
   ```

2. Queries are saved to `weekly_report_queries_current.sql`

3. In Cursor chat, execute queries manually:
   - Copy the OC query
   - Use: `mcp_mcp-hubble_run_presto_query` with the query
   - Copy the Top Cities query  
   - Use: `mcp_mcp-hubble_run_presto_query` with the query

4. Provide results back to the script

### Method 3: Direct Python Execution (Future)

For fully automated execution from Python, you would need:
- MCP client library integration
- Direct access to MCP server
- Custom wrapper functions

This is more complex and typically not needed since Cursor chat provides MCP access.

## What's Been Implemented

1. **Query Generation** (`generate_weekly_queries_with_new_pax.py`):
   - Generates OC query with New Pax
   - Generates Top 5 Cities query with New Pax
   - Calculates date ranges automatically

2. **MCP Execution Function** (`execute_queries_via_mcp()`):
   - Generates queries
   - Attempts to execute via MCP (when available)
   - Falls back to hardcoded data if MCP not available
   - Processes results into expected format

3. **Error Handling**:
   - Graceful fallback to hardcoded data
   - Clear error messages
   - Query files saved for manual execution

## Next Steps

To enable full automation:

1. **Run `/weekly_report` in Cursor chat** - MCP tools will execute automatically
2. **Or execute queries manually** using MCP tools in Cursor chat
3. **Results will be processed** and sent to Slack automatically

## Testing

Test the integration:

1. Run: `py process_and_send_weekly_report.py`
2. Check that queries are generated in `weekly_report_queries_current.sql`
3. In Cursor chat, execute one query via MCP tool
4. Verify the script processes results correctly

## Troubleshooting

**MCP tools not available?**
- Make sure you're running in Cursor chat, not standalone Python
- Check MCP server configuration
- Verify MCP Hubble is connected

**Queries not executing?**
- Check query syntax in `weekly_report_queries_current.sql`
- Verify date ranges are correct
- Test queries manually in Presto/your query tool

**New Pax still showing 0?**
- Verify SQL queries include New Pax calculation
- Check that query results include `this_week_new_pax` fields
- Test New Pax subquery separately

