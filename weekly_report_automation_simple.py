"""
Simplified Weekly Report Automation
Uses MCP tools to query data and send to Slack

This version assumes you have MCP tools available or can modify to use direct Presto connection.
For scheduled execution, you'll need to implement direct Presto connection.

Usage:
    python weekly_report_automation_simple.py

Or schedule via cron/task scheduler after implementing Presto connection.
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, Optional

# Configuration
SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL', '')
SLACK_CHANNEL = os.getenv('SLACK_CHANNEL', '#food-analytics')
SLACK_USERNAME = os.getenv('SLACK_USERNAME', 'Weekly Report Bot')

# NOTE: This script needs to be modified to use direct Presto connection
# For now, it's a template showing the structure

def get_week_dates():
    """Get date ranges for this week and last week"""
    today = datetime.now()
    
    # Calculate this week (Monday to Sunday)
    days_since_monday = today.weekday()
    this_week_start = today - timedelta(days=days_since_monday)
    this_week_end = this_week_start + timedelta(days=6)
    
    # Calculate last week
    last_week_start = this_week_start - timedelta(days=7)
    last_week_end = this_week_end - timedelta(days=7)
    
    # Format as YYYYMMDD
    def format_date(d):
        return d.strftime('%Y%m%d')
    
    return (
        format_date(this_week_start),
        format_date(this_week_end),
        format_date(last_week_start),
        format_date(last_week_end)
    )

def format_slack_message_simple(oc_data: Dict, penang_data: Dict) -> Dict:
    """Format simple Slack message"""
    
    def format_growth(num):
        if num >= 0:
            return f"+{num:.1f}%"
        return f"{num:.1f}%"
    
    def get_emoji(growth):
        if growth >= 15:
            return "🚀"
        elif growth >= 10:
            return "✅"
        elif growth >= 5:
            return "📈"
        elif growth >= 0:
            return "➡️"
        return "⚠️"
    
    text = f"""*📊 Weekly Performance Report - {datetime.now().strftime('%Y-%m-%d')}*

*🏙️ Outer Cities (OC)*
• Orders: {oc_data.get('orders_this_week', 0):,} ({get_emoji(oc_data.get('orders_growth', 0))} {format_growth(oc_data.get('orders_growth', 0))})
• GMV: MYR {oc_data.get('gmv_this_week', 0):,.0f} ({get_emoji(oc_data.get('gmv_growth', 0))} {format_growth(oc_data.get('gmv_growth', 0))})
• WTU: {oc_data.get('eaters_this_week', 0):,} ({get_emoji(oc_data.get('eaters_growth', 0))} {format_growth(oc_data.get('eaters_growth', 0))})
• Basket: MYR {oc_data.get('basket_this_week', 0):.2f} ({get_emoji(oc_data.get('basket_growth', 0))} {format_growth(oc_data.get('basket_growth', 0))})
• Completion: {oc_data.get('completion_this_week', 0):.1f}% ({oc_data.get('completion_delta', 0):+.1f}pp)
• Sessions: {oc_data.get('sessions_this_week', 0):,} ({get_emoji(oc_data.get('sessions_growth', 0))} {format_growth(oc_data.get('sessions_growth', 0))})
• COPS: {oc_data.get('cops_this_week', 0):.2f} ({oc_data.get('cops_delta', 0):+.2f})

*🏝️ Penang*
• Orders: {penang_data.get('orders_this_week', 0):,} ({get_emoji(penang_data.get('orders_growth', 0))} {format_growth(penang_data.get('orders_growth', 0))})
• GMV: MYR {penang_data.get('gmv_this_week', 0):,.0f} ({get_emoji(penang_data.get('gmv_growth', 0))} {format_growth(penang_data.get('gmv_growth', 0))})
• WTU: {penang_data.get('eaters_this_week', 0):,} ({get_emoji(penang_data.get('eaters_growth', 0))} {format_growth(penang_data.get('eaters_growth', 0))})
• Basket: MYR {penang_data.get('basket_this_week', 0):.2f} ({get_emoji(penang_data.get('basket_growth', 0))} {format_growth(penang_data.get('basket_growth', 0))})
• Completion: {penang_data.get('completion_this_week', 0):.1f}% ({penang_data.get('completion_delta', 0):+.1f}pp)
• Sessions: {penang_data.get('sessions_this_week', 0):,} ({get_emoji(penang_data.get('sessions_growth', 0))} {format_growth(penang_data.get('sessions_growth', 0))})
• COPS: {penang_data.get('cops_this_week', 0):.2f} ({penang_data.get('cops_delta', 0):+.2f})
"""
    
    return {
        "text": text,
        "channel": SLACK_CHANNEL,
        "username": SLACK_USERNAME
    }

def send_to_slack(message: Dict) -> bool:
    """Send message to Slack"""
    if not SLACK_WEBHOOK_URL:
        print("ERROR: SLACK_WEBHOOK_URL not set")
        return False
    
    try:
        response = requests.post(
            SLACK_WEBHOOK_URL,
            json=message,
            headers={'Content-Type': 'application/json'}
        )
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Main function - placeholder for actual implementation"""
    print("Weekly Report Automation")
    print("=" * 60)
    print("\n⚠️  NOTE: This script needs to be implemented with:")
    print("   1. Direct Presto/Hubble connection")
    print("   2. Query execution logic")
    print("   3. Data processing")
    print("\nSee weekly_report_automation.py for full template")
    print("=" * 60)
    
    # TODO: Implement actual query execution
    # For now, this is a placeholder
    
    return 0

if __name__ == '__main__':
    exit(main())




