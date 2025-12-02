"""
Enhanced Weekly Report to Slack
Includes: OC Cities, Top 5 Cities by GMV, Daily Metrics, and Penang
"""

import os
import sys
import json
import requests
import csv
from datetime import datetime, timedelta
from typing import Dict, Optional, List

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Configuration
SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL', 'https://hooks.slack.com/services/aaaajqkcgywrijyttf45nfhyma')
SLACK_CHANNEL = os.getenv('SLACK_CHANNEL', 'oc_weekly_performance_update')
SLACK_USERNAME = os.getenv('SLACK_USERNAME', 'Weekly Report Bot')

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

def format_slack_message_enhanced(oc_data: Dict, penang_data: Dict, 
                                   top_cities_data: Optional[List[Dict]] = None,
                                   daily_metrics: Optional[Dict] = None) -> Dict:
    """Format enhanced reports into Slack message format"""
    
    # Get date ranges
    this_week_start, this_week_end, last_week_start, last_week_end = get_week_dates()
    
    # Format dates for display
    def format_date_display(date_str):
        """Format YYYYMMDD to readable format"""
        try:
            dt = datetime.strptime(date_str, '%Y%m%d')
            return dt.strftime('%b %d')
        except:
            return date_str
    
    this_week_display = f"{format_date_display(this_week_start)} - {format_date_display(this_week_end)}"
    last_week_display = f"{format_date_display(last_week_start)} - {format_date_display(last_week_end)}"
    
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
                    "text": f"*Period:* This Week ({this_week_display}) vs Last Week ({last_week_display}) | *Generated:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                }
            ]
        },
        {"type": "divider"}
    ]
    
    # OC Cities Section
    oc_orders = oc_data.get('Total_Orders', {})
    oc_gmv = oc_data.get('Total_GMV_MYR', {})
    oc_wtu = oc_data.get('WTU_Weekly_Transaction_Users', {})
    oc_basket = oc_data.get('Avg_Basket_Size_MYR', {})
    oc_completion = oc_data.get('Completion_Rate_Pct', {})
    oc_sessions = oc_data.get('Unique_Sessions', {})
    oc_cops = oc_data.get('COPS_Completed_Orders_Per_Session', {})
    oc_promo = oc_data.get('Promo_Penetration_Pct', {})
    
    oc_blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "🏙️ Outer Cities (OC) - Overall",
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
    
    # Top 5 Cities by GMV Section
    if top_cities_data:
        top_cities_blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "🏆 Top 5 Cities by GMV (OC)",
                    "emoji": True
                }
            }
        ]
        
        # Create a table-like format for top cities
        city_text = "*City* | *GMV (MYR)* | *Growth*\n"
        city_text += "--- | --- | ---\n"
        
        for i, city in enumerate(top_cities_data[:5], 1):
            city_name = city.get('city_name', 'Unknown')
            gmv = city.get('this_week_gmv', 0)
            growth = city.get('gmv_growth_pct', 0)
            emoji = get_status_emoji(growth)
            city_text += f"{i}. {city_name} | {format_number(gmv)} | {emoji} {growth:+.1f}%\n"
        
        top_cities_blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": city_text
            }
        })
        
        blocks.extend(top_cities_blocks)
        blocks.append({"type": "divider"})
    
    # Daily Metrics Section
    if daily_metrics:
        daily_blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "📅 Daily Metrics (This Week)",
                    "emoji": True
                }
            }
        ]
        
        # Format daily metrics
        daily_text = "*Day* | *Orders* | *GMV (MYR)* | *WTU*\n"
        daily_text += "--- | --- | --- | ---\n"
        
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for i, day in enumerate(days):
            if i < len(daily_metrics.get('daily_data', [])):
                day_data = daily_metrics['daily_data'][i]
                orders = day_data.get('orders', 0)
                gmv = day_data.get('gmv', 0)
                wtu = day_data.get('wtu', 0)
                daily_text += f"{day} | {format_number(orders)} | {format_number(gmv)} | {format_number(wtu)}\n"
        
        daily_blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": daily_text
            }
        })
        
        blocks.extend(daily_blocks)
        blocks.append({"type": "divider"})
    
    # Penang Section
    penang_orders = penang_data.get('Total_Orders', {})
    penang_gmv = penang_data.get('Total_GMV_MYR', {})
    penang_wtu = penang_data.get('WTU_Weekly_Transaction_Users', {}) or penang_data.get('Unique_Eaters', {})
    penang_basket = penang_data.get('Avg_Basket_Size_MYR', {})
    penang_completion = penang_data.get('Completion_Rate_Pct', {})
    penang_sessions = penang_data.get('Unique_Sessions', {})
    penang_cops = penang_data.get('COPS_Completed_Orders_Per_Session', {})
    penang_promo = penang_data.get('Promo_Penetration_Pct', {})
    
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
    print("Enhanced Weekly Report to Slack - OC Cities & Penang")
    print("=" * 60)
    
    # Get date ranges
    this_week_start, this_week_end, last_week_start, last_week_end = get_week_dates()
    print(f"\n📅 Date Ranges:")
    print(f"   This Week: {this_week_start} - {this_week_end}")
    print(f"   Last Week: {last_week_start} - {last_week_end}")
    
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
    
    # Note: Top 5 cities and daily metrics would need to be queried
    # For now, we'll use placeholder data structure
    # In production, these would come from MCP queries
    top_cities_data = None  # Will be populated from queries
    daily_metrics = None    # Will be populated from queries
    
    print("\n⚠️  Note: Top 5 cities and daily metrics need to be queried")
    print("   These will be added when queries are executed")
    
    # Format Slack message
    print("\n📝 Formatting Slack message...")
    slack_message = format_slack_message_enhanced(
        oc_data, 
        penang_data,
        top_cities_data,
        daily_metrics
    )
    print("   ✅ Message formatted")
    
    # Send to Slack
    print("\n📤 Sending to Slack...")
    success = send_to_slack(slack_message)
    
    if success:
        print("\n✅ Enhanced weekly report sent successfully to Slack!")
        return 0
    else:
        print("\n❌ Failed to send report to Slack")
        return 1

if __name__ == '__main__':
    sys.exit(main())



