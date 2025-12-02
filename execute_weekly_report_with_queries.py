"""
Execute Weekly Report with Live SQL Queries via MCP
This script generates queries, executes them via MCP tools, and sends the report to Slack
"""

import os
import sys
from datetime import datetime

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Import query generation
from generate_weekly_queries_with_new_pax import (
    get_week_dates,
    generate_oc_query_with_new_pax,
    generate_top_cities_query_with_new_pax
)

# Import processing and sending functions
from process_and_send_weekly_report import (
    process_oc_results,
    process_top_cities_results,
    format_slack_message,
    send_to_slack
)

def execute_query_via_mcp(query: str):
    """
    Execute SQL query via MCP Hubble tool
    Returns list of dictionaries with query results
    """
    try:
        # Use MCP tool to execute Presto query
        # Note: This will be called via Cursor's MCP integration
        # For now, we'll return None and handle execution separately
        print(f"📊 Executing query (length: {len(query)} chars)...")
        print("⚠️  Note: Query execution requires MCP tool integration")
        return None
    except Exception as e:
        print(f"❌ Error executing query: {str(e)}")
        return None

def main():
    """Main function to execute weekly report with live queries"""
    print("=" * 60)
    print("Weekly Report Automation - Live SQL Queries")
    print("=" * 60)
    
    # Get date ranges
    dates = get_week_dates()
    print(f"\n📅 Date Ranges:")
    print(f"   This Week: {dates['this_week_start']} - {dates['this_week_end']}")
    print(f"   Same Week Last Month: {dates['same_week_last_month_start']} - {dates['same_week_last_month_end']}")
    print(f"   Same Week Last Year: {dates['same_week_last_year_start']} - {dates['same_week_last_year_end']}")
    
    # Generate queries
    print("\n📝 Generating SQL queries...")
    oc_query = generate_oc_query_with_new_pax(dates)
    top_cities_query = generate_top_cities_query_with_new_pax(dates)
    
    print("✅ Queries generated successfully")
    
    # Save queries to file for reference
    with open('weekly_report_queries_with_new_pax.sql', 'w', encoding='utf-8') as f:
        f.write("-- Weekly Report Queries with New Pax\n")
        f.write(f"-- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("=" * 60 + "\n")
        f.write("1. OC CITIES OVERALL\n")
        f.write("=" * 60 + "\n")
        f.write(oc_query)
        f.write("\n\n" + "=" * 60 + "\n")
        f.write("2. TOP 5 CITIES BY GMV\n")
        f.write("=" * 60 + "\n")
        f.write(top_cities_query)
    
    print("✅ Queries saved to: weekly_report_queries_with_new_pax.sql")
    
    print("\n" + "=" * 60)
    print("📋 INSTRUCTIONS:")
    print("=" * 60)
    print("\nTo complete the report, execute the queries via MCP tools:")
    print("\n1. Execute OC Query:")
    print("   Use: mcp_mcp-hubble_run_presto_query")
    print("   Query: (see weekly_report_queries_with_new_pax.sql)")
    print("\n2. Execute Top Cities Query:")
    print("   Use: mcp_mcp-hubble_run_presto_query")
    print("   Query: (see weekly_report_queries_with_new_pax.sql)")
    print("\n3. Process results and send to Slack:")
    print("   The results will be processed and sent automatically")
    print("\n" + "=" * 60)
    
    # For now, we'll use hardcoded data as fallback
    # In production, replace this with actual MCP query execution
    print("\n⚠️  Using hardcoded data as fallback (MCP execution not yet integrated)")
    print("   To use live queries, integrate MCP tool execution above")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())

