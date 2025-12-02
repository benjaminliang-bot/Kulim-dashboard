"""
Execute Weekly Report - Run this script to generate and send weekly reports
This script will execute queries and send results to Slack
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Import from workflow script
from cursor_weekly_report_workflow import (
    get_week_dates,
    get_oc_query,
    get_penang_query,
    process_query_results,
    format_slack_message,
    send_to_slack
)

# Configuration
SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL', '')
if not SLACK_WEBHOOK_URL:
    # Try to read from a config file or prompt user
    print("⚠️  SLACK_WEBHOOK_URL not set. Please set it:")
    print("   Option 1: Set environment variable: $env:SLACK_WEBHOOK_URL = 'your-url'")
    print("   Option 2: Update SLACK_WEBHOOK_URL in this script")
    print("\n   You can get your webhook URL from: https://api.slack.com/apps")
    sys.exit(1)

def execute_query_via_mcp(query: str) -> Optional[List[Dict]]:
    """
    Execute query - This function needs to be implemented based on your MCP setup
    For now, it returns None and queries should be executed manually via Cursor chat
    """
    print(f"\n📊 Query to execute:\n{query[:200]}...")
    print("\n⚠️  Note: This script requires MCP tools to execute queries.")
    print("   Please execute the queries in Cursor chat using MCP tools.")
    return None

def main():
    """Main function to execute weekly report"""
    print("=" * 60)
    print("Weekly Report Automation - OC Cities & Penang")
    print("=" * 60)
    
    # Get date ranges
    this_week_start, this_week_end, last_week_start, last_week_end = get_week_dates()
    print(f"\n📅 Date Ranges:")
    print(f"   This Week: {this_week_start} - {this_week_end}")
    print(f"   Last Week: {last_week_start} - {last_week_end}")
    
    # Get queries
    oc_query = get_oc_query(this_week_start, this_week_end, last_week_start, last_week_end)
    penang_query = get_penang_query(this_week_start, this_week_end, last_week_start, last_week_end)
    
    print("\n" + "=" * 60)
    print("📋 INSTRUCTIONS:")
    print("=" * 60)
    print("\nTo complete the report, you need to:")
    print("1. Execute the OC query in Cursor chat")
    print("2. Execute the Penang query in Cursor chat")
    print("3. Provide the results to this script")
    print("\n" + "=" * 60)
    print("💡 Alternative: Ask in Cursor chat:")
    print("   'Run the weekly report for OC and Penang'")
    print("   I'll execute the queries and send to Slack automatically")
    print("=" * 60)
    
    # Save queries to file for reference
    with open('weekly_report_queries.txt', 'w') as f:
        f.write("=" * 60 + "\n")
        f.write("OC CITIES QUERY\n")
        f.write("=" * 60 + "\n")
        f.write(oc_query)
        f.write("\n\n" + "=" * 60 + "\n")
        f.write("PENANG QUERY\n")
        f.write("=" * 60 + "\n")
        f.write(penang_query)
    
    print(f"\n✅ Queries saved to: weekly_report_queries.txt")
    print("\nTo execute manually, copy the queries and run them in Cursor chat.")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())



