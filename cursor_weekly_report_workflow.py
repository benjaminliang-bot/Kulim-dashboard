"""
Weekly Report Workflow for Cursor
This script can be run in Cursor to generate and send weekly reports

Usage in Cursor:
1. Set your SLACK_WEBHOOK_URL environment variable or update in script
2. Run this script in Cursor
3. The script will guide you through executing queries via MCP tools
4. Results will be processed and sent to Slack

Note: This script uses MCP tools which are available in Cursor's chat interface.
You can also run queries manually and use the processing functions.
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, Optional, List

# Configuration
SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL', '')
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

def get_oc_query(this_week_start: str, this_week_end: str, 
                 last_week_start: str, last_week_end: str) -> str:
    """Get OC Cities report query"""
    return f"""
    WITH this_week AS (
        SELECT 
            COUNT(DISTINCT f.order_id) as orders,
            COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END) as completed_orders,
            COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.passenger_id END) as unique_eaters,
            SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.gross_merchandise_value ELSE 0 END) as gmv,
            AVG(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.basket_size END) as avg_basket,
            SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.promo_expense ELSE 0 END) as promo_expense,
            COUNT(DISTINCT CASE WHEN f.is_promotion = TRUE THEN f.order_id END) as promo_orders,
            COUNT(DISTINCT f.scribe_session_id) as unique_sessions,
            COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.scribe_session_id END) as completed_sessions,
            ROUND(100.0 * COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END) / 
                  NULLIF(COUNT(DISTINCT f.order_id), 0), 2) as completion_rate
        FROM ocd_adw.f_food_metrics f
        WHERE f.country_id = 1 
          AND f.city_id != 1
          AND f.date_id >= {this_week_start} AND f.date_id <= {this_week_end}
          AND f.business_type = 0
    ),
    last_week AS (
        SELECT 
            COUNT(DISTINCT f.order_id) as orders,
            COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END) as completed_orders,
            COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.passenger_id END) as unique_eaters,
            SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.gross_merchandise_value ELSE 0 END) as gmv,
            AVG(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.basket_size END) as avg_basket,
            SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.promo_expense ELSE 0 END) as promo_expense,
            COUNT(DISTINCT CASE WHEN f.is_promotion = TRUE THEN f.order_id END) as promo_orders,
            COUNT(DISTINCT f.scribe_session_id) as unique_sessions,
            COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.scribe_session_id END) as completed_sessions,
            ROUND(100.0 * COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END) / 
                  NULLIF(COUNT(DISTINCT f.order_id), 0), 2) as completion_rate
        FROM ocd_adw.f_food_metrics f
        WHERE f.country_id = 1 
          AND f.city_id != 1
          AND f.date_id >= {last_week_start} AND f.date_id <= {last_week_end}
          AND f.business_type = 0
    )
    SELECT 
        l.orders as last_week_orders,
        t.orders as this_week_orders,
        l.completed_orders as last_week_completed_orders,
        t.completed_orders as this_week_completed_orders,
        l.completion_rate as last_week_completion_rate,
        t.completion_rate as this_week_completion_rate,
        l.unique_eaters as last_week_eaters,
        t.unique_eaters as this_week_eaters,
        l.gmv as last_week_gmv,
        t.gmv as this_week_gmv,
        l.avg_basket as last_week_basket,
        t.avg_basket as this_week_basket,
        l.promo_expense as last_week_promo_expense,
        t.promo_expense as this_week_promo_expense,
        l.promo_orders as last_week_promo_orders,
        t.promo_orders as this_week_promo_orders,
        ROUND(100.0 * l.promo_orders / NULLIF(l.orders, 0), 1) as last_week_promo_penetration,
        ROUND(100.0 * t.promo_orders / NULLIF(t.orders, 0), 1) as this_week_promo_penetration,
        l.unique_sessions as last_week_sessions,
        t.unique_sessions as this_week_sessions,
        l.completed_sessions as last_week_completed_sessions,
        t.completed_sessions as this_week_completed_sessions,
        ROUND(1.0 * l.orders / NULLIF(l.unique_sessions, 0), 2) as last_week_orders_per_session,
        ROUND(1.0 * t.orders / NULLIF(t.unique_sessions, 0), 2) as this_week_orders_per_session,
        ROUND(1.0 * l.completed_orders / NULLIF(l.completed_sessions, 0), 2) as last_week_cops,
        ROUND(1.0 * t.completed_orders / NULLIF(t.completed_sessions, 0), 2) as this_week_cops
    FROM this_week t
    CROSS JOIN last_week l
    """

def get_penang_query(this_week_start: str, this_week_end: str,
                     last_week_start: str, last_week_end: str) -> str:
    """Get Penang report query"""
    return f"""
    WITH this_week AS (
        SELECT 
            COUNT(DISTINCT f.order_id) as orders,
            COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END) as completed_orders,
            COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.passenger_id END) as unique_eaters,
            SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.gross_merchandise_value ELSE 0 END) as gmv,
            AVG(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.basket_size END) as avg_basket,
            SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.promo_expense ELSE 0 END) as promo_expense,
            COUNT(DISTINCT CASE WHEN f.is_promotion = TRUE THEN f.order_id END) as promo_orders,
            COUNT(DISTINCT f.scribe_session_id) as unique_sessions,
            COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.scribe_session_id END) as completed_sessions,
            ROUND(100.0 * COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END) / 
                  NULLIF(COUNT(DISTINCT f.order_id), 0), 2) as completion_rate
        FROM ocd_adw.f_food_metrics f
        WHERE f.country_id = 1 
          AND f.city_id = 13  -- Penang
          AND f.date_id >= {this_week_start} AND f.date_id <= {this_week_end}
          AND f.business_type = 0
    ),
    last_week AS (
        SELECT 
            COUNT(DISTINCT f.order_id) as orders,
            COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END) as completed_orders,
            COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.passenger_id END) as unique_eaters,
            SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.gross_merchandise_value ELSE 0 END) as gmv,
            AVG(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.basket_size END) as avg_basket,
            SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.promo_expense ELSE 0 END) as promo_expense,
            COUNT(DISTINCT CASE WHEN f.is_promotion = TRUE THEN f.order_id END) as promo_orders,
            COUNT(DISTINCT f.scribe_session_id) as unique_sessions,
            COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.scribe_session_id END) as completed_sessions,
            ROUND(100.0 * COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END) / 
                  NULLIF(COUNT(DISTINCT f.order_id), 0), 2) as completion_rate
        FROM ocd_adw.f_food_metrics f
        WHERE f.country_id = 1 
          AND f.city_id = 13  -- Penang
          AND f.date_id >= {last_week_start} AND f.date_id <= {last_week_end}
          AND f.business_type = 0
    )
    SELECT 
        l.orders as last_week_orders,
        t.orders as this_week_orders,
        l.completed_orders as last_week_completed_orders,
        t.completed_orders as this_week_completed_orders,
        l.completion_rate as last_week_completion_rate,
        t.completion_rate as this_week_completion_rate,
        l.unique_eaters as last_week_eaters,
        t.unique_eaters as this_week_eaters,
        l.gmv as last_week_gmv,
        t.gmv as this_week_gmv,
        l.avg_basket as last_week_basket,
        t.avg_basket as this_week_basket,
        l.promo_expense as last_week_promo_expense,
        t.promo_expense as this_week_promo_expense,
        l.promo_orders as last_week_promo_orders,
        t.promo_orders as this_week_promo_orders,
        ROUND(100.0 * l.promo_orders / NULLIF(l.orders, 0), 1) as last_week_promo_penetration,
        ROUND(100.0 * t.promo_orders / NULLIF(t.orders, 0), 1) as this_week_promo_penetration,
        l.unique_sessions as last_week_sessions,
        t.unique_sessions as this_week_sessions,
        l.completed_sessions as last_week_completed_sessions,
        t.completed_sessions as this_week_completed_sessions,
        ROUND(1.0 * l.orders / NULLIF(l.unique_sessions, 0), 2) as last_week_orders_per_session,
        ROUND(1.0 * t.orders / NULLIF(t.unique_sessions, 0), 2) as this_week_orders_per_session,
        ROUND(1.0 * l.completed_orders / NULLIF(l.completed_sessions, 0), 2) as last_week_cops,
        ROUND(1.0 * t.completed_orders / NULLIF(t.completed_sessions, 0), 2) as this_week_cops
    FROM this_week t
    CROSS JOIN last_week l
    """

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

def format_slack_message(oc_report: Dict, penang_report: Dict, 
                         this_week_start: str, this_week_end: str,
                         last_week_start: str, last_week_end: str) -> Dict:
    """Format reports into Slack message format"""
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
                    "text": f"*Period:* This Week ({this_week_start} - {this_week_end}) vs Last Week ({last_week_start} - {last_week_end}) | *Generated:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
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
                    "text": "🏙️ Outer Cities (OC)",
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
    """Main function - generates queries and instructions"""
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
    print("\n1. Execute the OC query using MCP tools in Cursor")
    print("2. Execute the Penang query using MCP tools in Cursor")
    print("3. Process the results using process_query_results()")
    print("4. Format and send using format_slack_message() and send_to_slack()")
    print("\n" + "=" * 60)
    print("💡 Example workflow:")
    print("=" * 60)
    print("""
# Step 1: Get queries
from cursor_weekly_report_workflow import get_oc_query, get_penang_query, get_week_dates
this_week_start, this_week_end, last_week_start, last_week_end = get_week_dates()
oc_query = get_oc_query(this_week_start, this_week_end, last_week_start, last_week_end)
penang_query = get_penang_query(this_week_start, this_week_end, last_week_start, last_week_end)

# Step 2: Execute queries via MCP tools (in Cursor chat)
# Use: mcp_mcp-hubble_run_presto_query with oc_query and penang_query
# Store results in oc_results and penang_results

# Step 3: Process results
from cursor_weekly_report_workflow import process_query_results
oc_report = process_query_results(oc_results)
penang_report = process_query_results(penang_results)

# Step 4: Format and send
from cursor_weekly_report_workflow import format_slack_message, send_to_slack
slack_message = format_slack_message(
    oc_report, penang_report,
    this_week_start, this_week_end,
    last_week_start, last_week_end
)
send_to_slack(slack_message)
    """)
    
    print("\n" + "=" * 60)
    print("📝 Queries are ready to execute")
    print("=" * 60)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())



