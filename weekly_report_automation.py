"""
Automated Weekly Report Generator for OC Cities and Penang
Sends weekly performance reports via Slack every week

Setup:
1. Install required packages: pip install requests pandas
2. Set SLACK_WEBHOOK_URL environment variable or update in script
3. Schedule to run weekly (see instructions at bottom)

Author: Automated Weekly Report System
Date: November 2025
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pandas as pd

# Configuration
SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL', '')  # Set your Slack webhook URL
SLACK_CHANNEL = os.getenv('SLACK_CHANNEL', '#food-analytics')  # Default channel
SLACK_USERNAME = os.getenv('SLACK_USERNAME', 'Weekly Report Bot')

# Presto/Hubble Connection (adjust based on your setup)
# Note: You may need to use your organization's Presto connection method
# This is a template - adjust connection details as needed

def get_presto_connection():
    """
    Get Presto connection - adjust based on your organization's setup
    You may need to use:
    - Presto Python client
    - SQLAlchemy
    - Your organization's internal query tool
    """
    # TODO: Configure your Presto connection here
    # Example using presto-python-client:
    # from presto.dbapi import connect
    # conn = connect(
    #     host='your-presto-host',
    #     port=8080,
    #     user='your-username',
    #     catalog='hive',
    #     schema='ocd_adw'
    # )
    # return conn
    pass

def run_presto_query(query: str) -> List[Dict]:
    """
    Execute Presto query and return results
    
    Args:
        query: SQL query string
        
    Returns:
        List of dictionaries with query results
    """
    # TODO: Implement your Presto query execution
    # This is a placeholder - you'll need to use your organization's method
    # Example:
    # conn = get_presto_connection()
    # cursor = conn.cursor()
    # cursor.execute(query)
    # columns = [desc[0] for desc in cursor.description]
    # results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    # return results
    
    # For now, return empty - you'll need to implement this
    return []

def get_week_dates():
    """
    Get date ranges for this week and last week
    
    Returns:
        Tuple of (this_week_start, this_week_end, last_week_start, last_week_end)
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
                      last_week_start: str, last_week_end: str) -> Dict:
    """
    Generate OC Cities weekly report
    
    Returns:
        Dictionary with report data
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
    
    # Execute query and get results
    results = run_presto_query(query)
    
    if not results:
        return None
    
    data = results[0]
    
    # Calculate deltas and growth percentages
    report = {
        'region': 'Outer Cities (OC)',
        'period': f'This Week ({this_week_start} - {this_week_end}) vs Last Week ({last_week_start} - {last_week_end})',
        'orders': {
            'last_week': int(data['last_week_orders']),
            'this_week': int(data['this_week_orders']),
            'delta': int(data['this_week_orders']) - int(data['last_week_orders']),
            'growth_pct': round((int(data['this_week_orders']) - int(data['last_week_orders'])) / data['last_week_orders'] * 100, 2) if data['last_week_orders'] > 0 else 0
        },
        'gmv': {
            'last_week': round(data['last_week_gmv'], 2),
            'this_week': round(data['this_week_gmv'], 2),
            'delta': round(data['this_week_gmv'] - data['last_week_gmv'], 2),
            'growth_pct': round((data['this_week_gmv'] - data['last_week_gmv']) / data['last_week_gmv'] * 100, 2) if data['last_week_gmv'] > 0 else 0
        },
        'eaters': {
            'last_week': int(data['last_week_eaters']),
            'this_week': int(data['this_week_eaters']),
            'delta': int(data['this_week_eaters']) - int(data['last_week_eaters']),
            'growth_pct': round((int(data['this_week_eaters']) - int(data['last_week_eaters'])) / data['last_week_eaters'] * 100, 2) if data['last_week_eaters'] > 0 else 0
        },
        'basket_size': {
            'last_week': round(data['last_week_basket'], 2),
            'this_week': round(data['this_week_basket'], 2),
            'delta': round(data['this_week_basket'] - data['last_week_basket'], 2),
            'growth_pct': round((data['this_week_basket'] - data['last_week_basket']) / data['last_week_basket'] * 100, 2) if data['last_week_basket'] > 0 else 0
        },
        'completion_rate': {
            'last_week': round(data['last_week_completion_rate'], 1),
            'this_week': round(data['this_week_completion_rate'], 1),
            'delta_pp': round(data['this_week_completion_rate'] - data['last_week_completion_rate'], 1)
        },
        'sessions': {
            'last_week': int(data['last_week_sessions']),
            'this_week': int(data['this_week_sessions']),
            'delta': int(data['this_week_sessions']) - int(data['last_week_sessions']),
            'growth_pct': round((int(data['this_week_sessions']) - int(data['last_week_sessions'])) / data['last_week_sessions'] * 100, 2) if data['last_week_sessions'] > 0 else 0
        },
        'cops': {
            'last_week': round(data['last_week_cops'], 2),
            'this_week': round(data['this_week_cops'], 2),
            'delta': round(data['this_week_cops'] - data['last_week_cops'], 2)
        },
        'promo': {
            'expense_last_week': round(data['last_week_promo_expense'], 2),
            'expense_this_week': round(data['this_week_promo_expense'], 2),
            'penetration_last_week': round(data['last_week_promo_penetration'], 1),
            'penetration_this_week': round(data['this_week_promo_penetration'], 1)
        }
    }
    
    return report

def generate_penang_report(this_week_start: str, this_week_end: str,
                          last_week_start: str, last_week_end: str) -> Dict:
    """
    Generate Penang weekly report
    
    Returns:
        Dictionary with report data
    """
    # Similar query but for Penang (city_id = 13)
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
    
    results = run_presto_query(query)
    
    if not results:
        return None
    
    data = results[0]
    
    # Calculate deltas and growth percentages
    report = {
        'region': 'Penang',
        'period': f'This Week ({this_week_start} - {this_week_end}) vs Last Week ({last_week_start} - {last_week_end})',
        'orders': {
            'last_week': int(data['last_week_orders']),
            'this_week': int(data['this_week_orders']),
            'delta': int(data['this_week_orders']) - int(data['last_week_orders']),
            'growth_pct': round((int(data['this_week_orders']) - int(data['last_week_orders'])) / data['last_week_orders'] * 100, 2) if data['last_week_orders'] > 0 else 0
        },
        'gmv': {
            'last_week': round(data['last_week_gmv'], 2),
            'this_week': round(data['this_week_gmv'], 2),
            'delta': round(data['this_week_gmv'] - data['last_week_gmv'], 2),
            'growth_pct': round((data['this_week_gmv'] - data['last_week_gmv']) / data['last_week_gmv'] * 100, 2) if data['last_week_gmv'] > 0 else 0
        },
        'eaters': {
            'last_week': int(data['last_week_eaters']),
            'this_week': int(data['this_week_eaters']),
            'delta': int(data['this_week_eaters']) - int(data['last_week_eaters']),
            'growth_pct': round((int(data['this_week_eaters']) - int(data['last_week_eaters'])) / data['last_week_eaters'] * 100, 2) if data['last_week_eaters'] > 0 else 0
        },
        'basket_size': {
            'last_week': round(data['last_week_basket'], 2),
            'this_week': round(data['this_week_basket'], 2),
            'delta': round(data['this_week_basket'] - data['last_week_basket'], 2),
            'growth_pct': round((data['this_week_basket'] - data['last_week_basket']) / data['last_week_basket'] * 100, 2) if data['last_week_basket'] > 0 else 0
        },
        'completion_rate': {
            'last_week': round(data['last_week_completion_rate'], 1),
            'this_week': round(data['this_week_completion_rate'], 1),
            'delta_pp': round(data['this_week_completion_rate'] - data['last_week_completion_rate'], 1)
        },
        'sessions': {
            'last_week': int(data['last_week_sessions']),
            'this_week': int(data['this_week_sessions']),
            'delta': int(data['this_week_sessions']) - int(data['last_week_sessions']),
            'growth_pct': round((int(data['this_week_sessions']) - int(data['last_week_sessions'])) / data['last_week_sessions'] * 100, 2) if data['last_week_sessions'] > 0 else 0
        },
        'cops': {
            'last_week': round(data['last_week_cops'], 2),
            'this_week': round(data['this_week_cops'], 2),
            'delta': round(data['this_week_cops'] - data['last_week_cops'], 2)
        },
        'promo': {
            'expense_last_week': round(data['last_week_promo_expense'], 2),
            'expense_this_week': round(data['this_week_promo_expense'], 2),
            'penetration_last_week': round(data['last_week_promo_penetration'], 1),
            'penetration_this_week': round(data['this_week_promo_penetration'], 1)
        }
    }
    
    return report

def format_slack_message(oc_report: Dict, penang_report: Dict) -> Dict:
    """
    Format reports into Slack message format
    
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
                    "text": f"*Generated:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
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
                    "text": f"🏙️ {oc_report['region']}",
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
                        "text": f"*Eaters (WTU)*\n{format_number(oc_report['eaters']['this_week'])} ({get_status_emoji(oc_report['eaters']['growth_pct'])} {oc_report['eaters']['growth_pct']:+.1f}%)"
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
                    "text": f"🏝️ {penang_report['region']}",
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
                        "text": f"*Eaters (WTU)*\n{format_number(penang_report['eaters']['this_week'])} ({get_status_emoji(penang_report['eaters']['growth_pct'])} {penang_report['eaters']['growth_pct']:+.1f}%)"
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
            headers={'Content-Type': 'application/json'}
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
    """
    print("=" * 60)
    print("Weekly Report Automation - OC Cities & Penang")
    print("=" * 60)
    
    # Get date ranges
    this_week_start, this_week_end, last_week_start, last_week_end = get_week_dates()
    print(f"\n📅 Date Ranges:")
    print(f"   This Week: {this_week_start} - {this_week_end}")
    print(f"   Last Week: {last_week_start} - {last_week_end}")
    
    # Generate reports
    print("\n📊 Generating OC Cities Report...")
    oc_report = generate_oc_report(this_week_start, this_week_end, last_week_start, last_week_end)
    
    if oc_report:
        print("   ✅ OC Cities report generated")
    else:
        print("   ❌ Failed to generate OC Cities report")
    
    print("\n📊 Generating Penang Report...")
    penang_report = generate_penang_report(this_week_start, this_week_end, last_week_start, last_week_end)
    
    if penang_report:
        print("   ✅ Penang report generated")
    else:
        print("   ❌ Failed to generate Penang report")
    
    # Format and send to Slack
    if oc_report and penang_report:
        print("\n📤 Sending reports to Slack...")
        slack_message = format_slack_message(oc_report, penang_report)
        success = send_to_slack(slack_message)
        
        if success:
            print("\n✅ Weekly reports sent successfully!")
        else:
            print("\n❌ Failed to send reports to Slack")
    else:
        print("\n❌ Cannot send reports - one or more reports failed to generate")
        sys.exit(1)
    
    sys.exit(0)

if __name__ == '__main__':
    sys.exit(main())

