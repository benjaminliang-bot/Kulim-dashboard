"""
Weekly Report Automation for Cursor
Uses MCP tools to query data and send reports to Slack

This script is designed to run within Cursor using MCP tools.
It can be executed manually or scheduled via Cursor's task runner.

Usage:
    Run this script in Cursor to generate and send weekly reports
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

# Note: This script uses MCP tools which are available in Cursor
# The queries will be executed via MCP mcp-hubble server

def get_week_dates():
    """
    Get date ranges for this week and last week
    
    Returns:
        Tuple of (this_week_start, this_week_end, last_week_start, last_week_end) as YYYYMMDD strings
    """
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

def generate_oc_report(this_week_start: str, this_week_end: str, 
                      last_week_start: str, last_week_end: str) -> Optional[Dict]:
    """
    Generate OC Cities weekly report using MCP tools
    
    Note: This function should be called from within Cursor where MCP tools are available
    """
    # Main metrics query for OC
    query = f"""
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
    
    # NOTE: In Cursor, you would use MCP tools to execute this query
    # For now, return None - the actual execution will be done via MCP tools
    # This is a template showing the structure
    
    print(f"[INFO] OC Report Query prepared for dates: {this_week_start} - {this_week_end}")
    return None  # Placeholder - actual execution via MCP

def generate_penang_report(this_week_start: str, this_week_end: str,
                          last_week_start: str, last_week_end: str) -> Optional[Dict]:
    """
    Generate Penang weekly report using MCP tools
    """
    query = f"""
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
    
    print(f"[INFO] Penang Report Query prepared for dates: {this_week_start} - {this_week_end}")
    return None  # Placeholder - actual execution via MCP

def process_query_results(results: List[Dict]) -> Optional[Dict]:
    """
    Process query results into report format
    
    Args:
        results: List of dictionaries from query results
        
    Returns:
        Dictionary with formatted report data
    """
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
    """
    Format reports into Slack message format with blocks
    
    Returns:
        Slack message payload dictionary
    """
    def format_number(num):
        """Format large numbers with commas"""
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
        """Get emoji based on growth percentage"""
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
        {
            "type": "divider"
        }
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
    """
    Send message to Slack via webhook
    
    Args:
        message: Slack message payload
        
    Returns:
        True if successful, False otherwise
    """
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
    """
    Main function to generate and send weekly reports
    
    This function should be called from within Cursor where MCP tools are available.
    The actual query execution will be done via MCP tools.
    """
    print("=" * 60)
    print("Weekly Report Automation - OC Cities & Penang")
    print("=" * 60)
    
    # Get date ranges
    this_week_start, this_week_end, last_week_start, last_week_end = get_week_dates()
    print(f"\n📅 Date Ranges:")
    print(f"   This Week: {this_week_start} - {this_week_end}")
    print(f"   Last Week: {last_week_start} - {last_week_end}")
    
    print("\n" + "=" * 60)
    print("NOTE: This script is designed to run within Cursor")
    print("The queries will be executed using MCP tools")
    print("=" * 60)
    
    print("\n📊 To generate reports:")
    print("1. Use MCP tools to execute the queries from generate_oc_report() and generate_penang_report()")
    print("2. Process the results using process_query_results()")
    print("3. Format and send using format_slack_message() and send_to_slack()")
    
    print("\n💡 Example workflow:")
    print("   - Run MCP query for OC report")
    print("   - Run MCP query for Penang report")
    print("   - Process both results")
    print("   - Format and send to Slack")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())



