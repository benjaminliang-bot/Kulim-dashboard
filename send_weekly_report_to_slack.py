"""
Send Weekly Report to Slack
This script reads the existing weekly report data and sends it to Slack
"""

import os
import sys
import json
import requests
import csv
from datetime import datetime
from typing import Dict, Optional

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Configuration
SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL', 'https://hooks.slack.com/services/aaaajqkcgywrijyttf45nfhyma')
SLACK_CHANNEL = os.getenv('SLACK_CHANNEL', 'oc_weekly_performance_update')
SLACK_USERNAME = os.getenv('SLACK_USERNAME', 'Weekly Report Bot')

def read_csv_data(filepath: str) -> Dict:
    """Read CSV data and convert to dictionary"""
    data = {}
    try:
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                metric = row['Metric']
                data[metric] = {
                    'last_week': float(row.get('Last_Week_Oct_18_24', 0) or 0),
                    'this_week': float(row.get('This_Week_Oct_25_31', 0) or 0),
                    'change': float(row.get('Change', 0) or 0),
                    'growth_pct': float(row.get('Growth_Pct', 0) or 0)
                }
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    return data

def format_slack_message_from_csv(oc_data: Dict, penang_data: Dict) -> Dict:
    """Format reports into Slack message format from CSV data"""
    def format_number(num):
        """Format large numbers"""
        if isinstance(num, float):
            if num >= 1000000:
                return f"{num/1000000:.1f}M"
            elif num >= 1000:
                return f"{num/1000:.1f}K"
            return f"{num:.2f}"
        if num >= 1000000:
            return f"{num/1000000:.1f}M"
        elif num >= 1000:
            return f"{num/1000:.1f}K"
        return f"{num:,}"
    
    def get_status_emoji(growth_pct):
        """Get emoji based on growth"""
        if growth_pct >= 15:
            return "🚀"
        elif growth_pct >= 10:
            return "✅"
        elif growth_pct >= 5:
            return "📈"
        elif growth_pct >= 0:
            return "➡️"
        else:
            return "⚠️"
    
    # Extract OC data
    oc_orders = oc_data.get('Total_Orders', {})
    oc_gmv = oc_data.get('Total_GMV_MYR', {})
    oc_wtu = oc_data.get('WTU_Weekly_Transaction_Users', {})
    oc_basket = oc_data.get('Avg_Basket_Size_MYR', {})
    oc_completion = oc_data.get('Completion_Rate_Pct', {})
    oc_sessions = oc_data.get('Unique_Sessions', {})
    oc_cops = oc_data.get('COPS_Completed_Orders_Per_Session', {})
    oc_promo = oc_data.get('Promo_Penetration_Pct', {})
    
    # Extract Penang data (use Unique_Eaters if WTU not available)
    penang_orders = penang_data.get('Total_Orders', {})
    penang_gmv = penang_data.get('Total_GMV_MYR', {})
    penang_wtu = penang_data.get('WTU_Weekly_Transaction_Users', {}) or penang_data.get('Unique_Eaters', {})
    penang_basket = penang_data.get('Avg_Basket_Size_MYR', {})
    penang_completion = penang_data.get('Completion_Rate_Pct', {})
    penang_sessions = penang_data.get('Unique_Sessions', {})
    penang_cops = penang_data.get('COPS_Completed_Orders_Per_Session', {})
    penang_promo = penang_data.get('Promo_Penetration_Pct', {})
    
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "📊 Weekly Performance Report",
                "emoji": True
            }
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"*Period:* This Week (Oct 25-31) vs Last Week (Oct 18-24) | *Generated:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                }
            ]
        },
        {"type": "divider"}
    ]
    
    # OC Cities Section
    oc_blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "🏙️ Outer Cities (OC)",
                "emoji": True
            }
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*Orders*\n{format_number(oc_orders.get('this_week', 0))} ({get_status_emoji(oc_orders.get('growth_pct', 0))} {oc_orders.get('growth_pct', 0):+.1f}%)"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*GMV (MYR)*\n{format_number(oc_gmv.get('this_week', 0))} ({get_status_emoji(oc_gmv.get('growth_pct', 0))} {oc_gmv.get('growth_pct', 0):+.1f}%)"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*WTU*\n{format_number(oc_wtu.get('this_week', 0))} ({get_status_emoji(oc_wtu.get('growth_pct', 0))} {oc_wtu.get('growth_pct', 0):+.1f}%)"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Basket Size (MYR)*\n{format_number(oc_basket.get('this_week', 0))} ({get_status_emoji(oc_basket.get('growth_pct', 0))} {oc_basket.get('growth_pct', 0):+.1f}%)"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Completion Rate*\n{oc_completion.get('this_week', 0):.1f}% ({oc_completion.get('change', 0):+.1f}pp)"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Sessions*\n{format_number(oc_sessions.get('this_week', 0))} ({get_status_emoji(oc_sessions.get('growth_pct', 0))} {oc_sessions.get('growth_pct', 0):+.1f}%)"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*COPS*\n{oc_cops.get('this_week', 0):.2f} ({oc_cops.get('change', 0):+.2f})"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Promo Penetration*\n{oc_promo.get('this_week', 0):.1f}% ({oc_promo.get('change', 0):+.1f}pp)"
                }
            ]
        }
    ]
    blocks.extend(oc_blocks)
    blocks.append({"type": "divider"})
    
    # Penang Section
    penang_blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "🏝️ Penang",
                "emoji": True
            }
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*Orders*\n{format_number(penang_orders.get('this_week', 0))} ({get_status_emoji(penang_orders.get('growth_pct', 0))} {penang_orders.get('growth_pct', 0):+.1f}%)"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*GMV (MYR)*\n{format_number(penang_gmv.get('this_week', 0))} ({get_status_emoji(penang_gmv.get('growth_pct', 0))} {penang_gmv.get('growth_pct', 0):+.1f}%)"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*WTU*\n{format_number(penang_wtu.get('this_week', 0))} ({get_status_emoji(penang_wtu.get('growth_pct', 0))} {penang_wtu.get('growth_pct', 0):+.1f}%)"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Basket Size (MYR)*\n{format_number(penang_basket.get('this_week', 0))} ({get_status_emoji(penang_basket.get('growth_pct', 0))} {penang_basket.get('growth_pct', 0):+.1f}%)"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Completion Rate*\n{penang_completion.get('this_week', 0):.1f}% ({penang_completion.get('change', 0):+.1f}pp)"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Sessions*\n{format_number(penang_sessions.get('this_week', 0))} ({get_status_emoji(penang_sessions.get('growth_pct', 0))} {penang_sessions.get('growth_pct', 0):+.1f}%)"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*COPS*\n{penang_cops.get('this_week', 0):.2f} ({penang_cops.get('change', 0):+.2f})"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Promo Penetration*\n{penang_promo.get('this_week', 0):.1f}% ({penang_promo.get('change', 0):+.1f}pp)"
                }
            ]
        }
    ]
    blocks.extend(penang_blocks)
    
    return {
        "blocks": blocks,
        "channel": SLACK_CHANNEL,
        "username": SLACK_USERNAME
    }

def send_to_slack(message: Dict) -> bool:
    """Send message to Slack via webhook"""
    if not SLACK_WEBHOOK_URL:
        print("ERROR: SLACK_WEBHOOK_URL not set. Please set it as an environment variable or in the script.")
        print("\nTo set it:")
        print("  PowerShell: $env:SLACK_WEBHOOK_URL = 'your-webhook-url'")
        print("  Or update SLACK_WEBHOOK_URL in this script")
        return False
    
    try:
        response = requests.post(
            SLACK_WEBHOOK_URL,
            json=message,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Successfully sent message to Slack")
            return True
        else:
            print(f"❌ Failed to send to Slack. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error sending to Slack: {str(e)}")
        return False

def main():
    """Main function"""
    print("=" * 60)
    print("Weekly Report to Slack - OC Cities & Penang")
    print("=" * 60)
    
    # Read CSV data
    print("\n📊 Reading report data...")
    oc_data = read_csv_data('oc_cities_week_over_week_summary.csv')
    penang_data = read_csv_data('penang_week_over_week_summary.csv')
    
    if not oc_data or not penang_data:
        print("❌ Error: Could not read report data files")
        print("   Make sure oc_cities_week_over_week_summary.csv and penang_week_over_week_summary.csv exist")
        return 1
    
    print("   ✅ OC Cities data loaded")
    print("   ✅ Penang data loaded")
    
    # Format Slack message
    print("\n📝 Formatting Slack message...")
    slack_message = format_slack_message_from_csv(oc_data, penang_data)
    print("   ✅ Message formatted")
    
    # Send to Slack
    print("\n📤 Sending to Slack...")
    success = send_to_slack(slack_message)
    
    if success:
        print("\n✅ Weekly report sent successfully to Slack!")
        return 0
    else:
        print("\n❌ Failed to send report to Slack")
        return 1

if __name__ == '__main__':
    sys.exit(main())

