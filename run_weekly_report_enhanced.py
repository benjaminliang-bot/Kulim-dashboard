"""
Run Enhanced Weekly Report
Executes queries for OC Cities, Top 5 Cities, Daily Metrics, and Penang
Then sends formatted report to Slack

Usage in Cursor:
1. Ask: "Run the weekly report for OC and Penang"
2. I'll execute all queries and send to Slack
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
SLACK_CHANNEL = os.getenv('SLACK_CHANNEL', '#food-analytics')
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

def process_query_results(results: List[Dict]) -> Optional[Dict]:
    """Process query results into report format"""
    if not results or len(results) == 0:
        return None
    
    data = results[0]
    
    # Calculate deltas and growth percentages
    report = {
        'orders': {
            'last_week': int(data.get('last_week_orders', 0)),
            'this_week': int(data.get('this_week_orders', 0)),
            'delta': int(data.get('this_week_orders', 0)) - int(data.get('last_week_orders', 0)),
            'growth_pct': round((int(data.get('this_week_orders', 0)) - int(data.get('last_week_orders', 0))) / data.get('last_week_orders', 1) * 100, 2) if data.get('last_week_orders', 0) > 0 else 0
        },
        'gmv': {
            'last_week': round(float(data.get('last_week_gmv', 0)), 2),
            'this_week': round(float(data.get('this_week_gmv', 0)), 2),
            'delta': round(float(data.get('this_week_gmv', 0)) - float(data.get('last_week_gmv', 0)), 2),
            'growth_pct': round((float(data.get('this_week_gmv', 0)) - float(data.get('last_week_gmv', 0))) / float(data.get('last_week_gmv', 1)) * 100, 2) if data.get('last_week_gmv', 0) > 0 else 0
        },
        'eaters': {
            'last_week': int(data.get('last_week_eaters', 0)),
            'this_week': int(data.get('this_week_eaters', 0)),
            'delta': int(data.get('this_week_eaters', 0)) - int(data.get('last_week_eaters', 0)),
            'growth_pct': round((int(data.get('this_week_eaters', 0)) - int(data.get('last_week_eaters', 0))) / data.get('last_week_eaters', 1) * 100, 2) if data.get('last_week_eaters', 0) > 0 else 0
        },
        'basket_size': {
            'last_week': round(float(data.get('last_week_basket', 0)), 2),
            'this_week': round(float(data.get('this_week_basket', 0)), 2),
            'delta': round(float(data.get('this_week_basket', 0)) - float(data.get('last_week_basket', 0)), 2),
            'growth_pct': round((float(data.get('this_week_basket', 0)) - float(data.get('last_week_basket', 0))) / float(data.get('last_week_basket', 1)) * 100, 2) if data.get('last_week_basket', 0) > 0 else 0
        },
        'completion_rate': {
            'last_week': round(float(data.get('last_week_completion_rate', 0)), 1),
            'this_week': round(float(data.get('this_week_completion_rate', 0)), 1),
            'delta_pp': round(float(data.get('this_week_completion_rate', 0)) - float(data.get('last_week_completion_rate', 0)), 1)
        },
        'sessions': {
            'last_week': int(data.get('last_week_sessions', 0)),
            'this_week': int(data.get('this_week_sessions', 0)),
            'delta': int(data.get('this_week_sessions', 0)) - int(data.get('last_week_sessions', 0)),
            'growth_pct': round((int(data.get('this_week_sessions', 0)) - int(data.get('last_week_sessions', 0))) / data.get('last_week_sessions', 1) * 100, 2) if data.get('last_week_sessions', 0) > 0 else 0
        },
        'cops': {
            'last_week': round(float(data.get('last_week_cops', 0)), 2),
            'this_week': round(float(data.get('this_week_cops', 0)), 2),
            'delta': round(float(data.get('this_week_cops', 0)) - float(data.get('last_week_cops', 0)), 2)
        },
        'promo': {
            'expense_last_week': round(float(data.get('last_week_promo_expense', 0)), 2),
            'expense_this_week': round(float(data.get('this_week_promo_expense', 0)), 2),
            'penetration_last_week': round(float(data.get('last_week_promo_penetration', 0)), 1),
            'penetration_this_week': round(float(data.get('this_week_promo_penetration', 0)), 1)
        }
    }
    
    return report

def process_top_cities_results(results: List[Dict]) -> List[Dict]:
    """Process top cities query results"""
    if not results:
        return []
    
    cities = []
    for row in results:
        city = {
            'city_name': row.get('city_name', 'Unknown'),
            'city_id': int(row.get('city_id', 0)),
            'last_week_gmv': round(float(row.get('last_week_gmv', 0)), 2),
            'this_week_gmv': round(float(row.get('this_week_gmv', 0)), 2),
            'gmv_delta': round(float(row.get('gmv_delta', 0)), 2),
            'gmv_growth_pct': round(float(row.get('gmv_growth_pct', 0)), 2),
            'last_week_orders': int(row.get('last_week_orders', 0)),
            'this_week_orders': int(row.get('this_week_orders', 0)),
            'last_week_eaters': int(row.get('last_week_eaters', 0)),
            'this_week_eaters': int(row.get('this_week_eaters', 0))
        }
        cities.append(city)
    
    return cities

def process_daily_metrics_results(results: List[Dict]) -> Dict:
    """Process daily metrics query results"""
    if not results:
        return {'daily_data': []}
    
    daily_data = []
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    
    for i, row in enumerate(results):
        day_info = {
            'day': days[i] if i < len(days) else f'Day {i+1}',
            'date_id': int(row.get('date_id', 0)),
            'orders': int(row.get('daily_orders', 0)),
            'completed_orders': int(row.get('daily_completed_orders', 0)),
            'gmv': round(float(row.get('daily_gmv', 0)), 2),
            'wtu': int(row.get('daily_wtu', 0)),
            'sessions': int(row.get('daily_sessions', 0)),
            'completion_rate': round(float(row.get('daily_completion_rate', 0)), 1)
        }
        daily_data.append(day_info)
    
    return {'daily_data': daily_data}

def format_slack_message_enhanced(oc_report: Dict, penang_report: Dict,
                                   top_cities: List[Dict],
                                   daily_metrics: Dict) -> Dict:
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
    if oc_report:
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
                        "text": f"*Orders*\n{format_number(oc_report['orders']['this_week'])} ({get_status_emoji(oc_report['orders']['growth_pct'])} {oc_report['orders']['growth_pct']:+.1f}%)"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*GMV (MYR)*\n{format_number(oc_report['gmv']['this_week'])} ({get_status_emoji(oc_report['gmv']['growth_pct'])} {oc_report['gmv']['growth_pct']:+.1f}%)"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*WTU*\n{format_number(oc_report['eaters']['this_week'])} ({get_status_emoji(oc_report['eaters']['growth_pct'])} {oc_report['eaters']['growth_pct']:+.1f}%)"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Basket Size (MYR)*\n{format_number(oc_report['basket_size']['this_week'])} ({get_status_emoji(oc_report['basket_size']['growth_pct'])} {oc_report['basket_size']['growth_pct']:+.1f}%)"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Completion Rate*\n{oc_report['completion_rate']['this_week']}% ({oc_report['completion_rate']['delta_pp']:+.1f}pp)"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Sessions*\n{format_number(oc_report['sessions']['this_week'])} ({get_status_emoji(oc_report['sessions']['growth_pct'])} {oc_report['sessions']['growth_pct']:+.1f}%)"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*COPS*\n{oc_report['cops']['this_week']} ({oc_report['cops']['delta']:+.2f})"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Promo Penetration*\n{oc_report['promo']['penetration_this_week']}% ({oc_report['promo']['penetration_this_week'] - oc_report['promo']['penetration_last_week']:+.1f}pp)"
                    }
                ]
            }
        ]
        blocks.extend(oc_blocks)
        blocks.append({"type": "divider"})
    
    # Top 5 Cities by GMV Section
    if top_cities and len(top_cities) > 0:
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
        
        for i, city in enumerate(top_cities[:5], 1):
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
    if daily_metrics and daily_metrics.get('daily_data'):
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
        
        for day_data in daily_metrics['daily_data']:
            day = day_data.get('day', 'N/A')
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
    if penang_report:
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
                        "text": f"*Orders*\n{format_number(penang_report['orders']['this_week'])} ({get_status_emoji(penang_report['orders']['growth_pct'])} {penang_report['orders']['growth_pct']:+.1f}%)"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*GMV (MYR)*\n{format_number(penang_report['gmv']['this_week'])} ({get_status_emoji(penang_report['gmv']['growth_pct'])} {penang_report['gmv']['growth_pct']:+.1f}%)"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*WTU*\n{format_number(penang_report['eaters']['this_week'])} ({get_status_emoji(penang_report['eaters']['growth_pct'])} {penang_report['eaters']['growth_pct']:+.1f}%)"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Basket Size (MYR)*\n{format_number(penang_report['basket_size']['this_week'])} ({get_status_emoji(penang_report['basket_size']['growth_pct'])} {penang_report['basket_size']['growth_pct']:+.1f}%)"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Completion Rate*\n{penang_report['completion_rate']['this_week']}% ({penang_report['completion_rate']['delta_pp']:+.1f}pp)"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Sessions*\n{format_number(penang_report['sessions']['this_week'])} ({get_status_emoji(penang_report['sessions']['growth_pct'])} {penang_report['sessions']['growth_pct']:+.1f}%)"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*COPS*\n{penang_report['cops']['this_week']} ({penang_report['cops']['delta']:+.2f})"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Promo Penetration*\n{penang_report['promo']['penetration_this_week']}% ({penang_report['promo']['penetration_this_week'] - penang_report['promo']['penetration_last_week']:+.1f}pp)"
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
    """Main function - placeholder for query execution"""
    print("=" * 60)
    print("Enhanced Weekly Report - OC Cities & Penang")
    print("=" * 60)
    
    # Get date ranges
    this_week_start, this_week_end, last_week_start, last_week_end = get_week_dates()
    print(f"\n📅 Date Ranges:")
    print(f"   This Week: {this_week_start} - {this_week_end}")
    print(f"   Last Week: {last_week_start} - {last_week_end}")
    
    print("\n" + "=" * 60)
    print("📋 INSTRUCTIONS:")
    print("=" * 60)
    print("\nTo complete the enhanced report, you need to:")
    print("1. Execute OC Cities query (overall metrics)")
    print("2. Execute Top 5 Cities by GMV query")
    print("3. Execute Daily Metrics query")
    print("4. Execute Penang query")
    print("\n" + "=" * 60)
    print("💡 Ask in Cursor chat:")
    print("   'Run the weekly report for OC and Penang'")
    print("   I'll execute all queries and send to Slack automatically")
    print("=" * 60)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())



