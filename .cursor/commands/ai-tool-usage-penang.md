# ai-tool-usage-penang

Check AI Tools usage and adoption statistics for the Penang team by querying the `ai_tooling_usage.grabbers_ai_usage_summary` table.

## Quick Start

**Just type `/ai-tool-usage-penang` in Cursor chat!**

The command will automatically:
1. Generate SQL query for all 10 Penang team members
2. Display the query for execution via MCP tools
3. Generate comprehensive dashboard report

## Workflow

When this command is executed:

1. **Verify MCP Availability**
   - Checks if `mcp-grab-data` or `mcp-hubble` MCP is available
   - If neither is available, informs user to set up MCP first

2. **Generate Team Query**
   - Queries all 12 Penang team members:
     - Benjamin Liang
     - Chia Yee
     - Darren
     - Suki
     - Earnest Koe
     - Xin Rong Chong
     - Xin Yu Lin (Jamie)
     - Teoh Jun Ling
     - Lee Sook Chin
     - Low Jia Ying
     - Hon Yi Ni
     - Jess (Hsin Tsi Lim)
     - Maggie (Mei Yan Chui)

3. **Query AI Tooling Data**
   - Uses available MCP to query: `ai_tooling_usage.grabbers_ai_usage_summary`
   - Filters by all team member email addresses
   - Retrieves all relevant usage metrics

4. **Present Results**
   - Displays usage statistics in executive dashboard format
   - Includes metrics: usage frequency, tool adoption rate, active tools, trends
   - Formats results for executive-level consumption
   - Highlights actionable insights

## Example Query

```sql
SELECT 
    email_work,
    MAX(as_of_date) as latest_date,
    MAX(CASE WHEN as_of_date = ... THEN is_used_cursor ELSE NULL END) as is_used_cursor,
    MAX(CASE WHEN as_of_date = ... THEN is_used_gpt ELSE NULL END) as is_used_gpt,
    -- ... other metrics
FROM ai_tooling_usage.grabbers_ai_usage_summary
WHERE email_work IN (
    'benjamin.liang@grabtaxi.com',
    'darren.ng@grabtaxi.com',
    -- ... all team members
)
GROUP BY email_work
ORDER BY email_work
```

## Output

The command generates:

1. **Executive Dashboard** (`PENANG_TEAM_AI_USAGE_DASHBOARD_COMPLETE.md`)
   - Overall team adoption metrics
   - Individual usage status for all 10 members
   - Tool adoption analysis
   - Key insights and recommendations
   - Strategic action plan

2. **Key Metrics Tracked**
   - Tool usage (Cursor, GPT, GPT Prompt, Gemini, Jarvis)
   - Active days per week
   - Streak metrics (DAU5)
   - Adoption rates by tool and individual

## Manual Execution (Alternative)

If you prefer to run manually:

```bash
cd "c:\Users\benjamin.liang\Documents\Python"
py query_penang_team_ai_usage.py
```

Then execute the generated query via MCP tools.

## Command Handler

The command uses: `.cursor/commands/ai-tool-usage-penang.py`

This handler script:
- Changes to the correct directory
- Generates the team query
- Displays instructions for MCP execution
- The AI assistant then executes the query and generates the dashboard

## Error Handling

- If MCP is unavailable: "MCP (mcp-grab-data or mcp-hubble) is required. Set it up first."
- If query fails: "Query execution failed. Check MCP connection."
- If no data found: "No AI tooling usage data found for team members."

## Troubleshooting

**Command not found?**
- Make sure you're in the Cursor chat
- Type exactly: `/ai-tool-usage-penang`
- The command should auto-complete

**Query fails?**
- Verify MCP tools are available
- Check that `mcp-grab-data` or `mcp-hubble` is configured
- Ensure you have access to `ai_tooling_usage.grabbers_ai_usage_summary` table

**No results?**
- Verify team member email addresses are correct
- Check if data exists in the table for those emails
- Review query syntax

## Related Files

- `generate_penang_team_ai_dashboard.py` - Query generator script
- `PENANG_TEAM_AI_USAGE_DASHBOARD_COMPLETE.md` - Generated dashboard report
- `format_ai_usage_results.py` - Dashboard formatting utilities
- `check_ai_tools_usage.py` - Individual usage checker

