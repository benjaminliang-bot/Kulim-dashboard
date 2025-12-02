# Live SQL Queries Setup for Weekly Report

## Overview

The weekly report script has been updated to support **live SQL queries with New Pax calculation**. The system generates SQL queries dynamically and can execute them via MCP Hubble tools.

## What's Been Set Up

### 1. Query Generation Module (`generate_weekly_queries_with_new_pax.py`)

- **Date Calculation**: Automatically calculates:
  - This week (Monday to Sunday)
  - Same week last month
  - Same week last year

- **New Pax Calculation**: Implements the definition:
  - Unique `passenger_id` where:
    - Last transaction was more than a year ago, OR
    - First order was within the week

- **Query Types**:
  - OC Cities Overall query (with New Pax)
  - Top 5 Cities by GMV query (with New Pax)

### 2. Main Script Updates (`process_and_send_weekly_report.py`)

- **Dual Mode**: Supports both:
  - Live SQL queries (via MCP)
  - Hardcoded test data (fallback)

- **Query Execution**: Attempts to execute queries first, falls back to hardcoded data if:
  - MCP tools are not available
  - Query execution fails
  - Results are empty

## How to Use

### Option 1: Execute Queries Manually via MCP

1. **Run the script** to generate queries:
   ```bash
   py process_and_send_weekly_report.py
   ```

2. **Check the output** - queries are saved to `weekly_report_queries_current.sql`

3. **Execute queries in Cursor chat**:
   - Copy the OC query from the file
   - Use: `mcp_mcp-hubble_run_presto_query` with the query
   - Copy the Top Cities query
   - Use: `mcp_mcp-hubble_run_presto_query` with the query

4. **Provide results** to the script (or integrate MCP execution directly)

### Option 2: Integrate MCP Execution Directly

Update `process_and_send_weekly_report.py` in the `execute_queries_via_mcp()` function:

```python
# Uncomment and configure:
from mcp import mcp_hubble_run_presto_query  # Or your MCP integration method

oc_results = mcp_hubble_run_presto_query(query=oc_query)
top_cities_results = mcp_hubble_run_presto_query(query=top_cities_query)

if oc_results and top_cities_results:
    oc_data = [dict(row) for row in oc_results]
    top_cities_data = [dict(row) for row in top_cities_results]
    return oc_data, top_cities_data
```

## Query Structure

### OC Cities Query
- Includes all standard metrics (orders, GMV, WTU, basket, etc.)
- Includes New Pax for:
  - This week
  - Same week last month
  - Same week last year

### Top Cities Query
- Returns top 5 cities by GMV
- Includes all standard metrics per city
- New Pax calculation per city (currently returns 0, needs per-city subquery)

## New Pax SQL Logic

The New Pax calculation uses this logic:

```sql
-- Passengers who ordered in the current week AND:
-- 1. First order was within this week, OR
-- 2. Last order before this week was more than 365 days ago
--    (and they didn't order in the last year before this week)
```

## Files Created

1. **`generate_weekly_queries_with_new_pax.py`**: Query generation module
2. **`execute_weekly_report_with_queries.py`**: Standalone execution script
3. **`weekly_report_queries_current.sql`**: Generated queries (updated on each run)
4. **`LIVE_QUERIES_SETUP.md`**: This documentation

## Next Steps

1. **Test query generation**: Run `py generate_weekly_queries_with_new_pax.py` to verify queries
2. **Execute queries**: Use MCP tools to run the queries
3. **Verify results**: Check that New Pax values are populated correctly
4. **Integrate MCP**: Update the script to call MCP tools directly (if possible)

## Troubleshooting

**Queries not executing?**
- Check MCP tool availability
- Verify query syntax (run `generate_weekly_queries_with_new_pax.py` to see queries)
- Check date ranges are correct

**New Pax showing 0?**
- Verify the SQL logic matches your definition
- Check that date calculations are correct (36500 = 365 days in YYYYMMDD format)
- Test the New Pax subquery separately

**Script using hardcoded data?**
- This is expected if MCP execution is not configured
- The script will automatically fall back to hardcoded data
- To use live queries, integrate MCP execution as shown above

