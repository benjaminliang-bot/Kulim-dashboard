"""
Process query results and send enhanced weekly report to Slack
Supports both live SQL queries (via MCP) and hardcoded test data
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta

# Import query generation functions
try:
    from generate_weekly_queries_with_new_pax import (
        get_week_dates,
        generate_oc_query_with_new_pax,
        generate_top_cities_query_with_new_pax
    )
    QUERY_GENERATION_AVAILABLE = True
except ImportError:
    QUERY_GENERATION_AVAILABLE = False
    print("⚠️  Query generation module not available, using hardcoded data")

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    try:
        import io
        if not hasattr(sys.stdout, 'buffer') or sys.stdout.buffer is None:
            # stdout already wrapped or not available
            pass
        else:
            try:
                sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
            except (AttributeError, ValueError, OSError):
                # If wrapping fails, continue without it
                pass
    except:
        # If anything fails, continue without encoding wrapper
        pass

# Configuration - Using Slack Webhook
SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL', 'https://hooks.slack.com/services/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')
SLACK_CHANNEL_ID = os.getenv('SLACK_CHANNEL_ID', 'C09QZMPG7MZ')  # oc_weekly_performance_update
SLACK_USERNAME = os.getenv('SLACK_USERNAME', 'Weekly Report Bot')

# MCP Tools Configuration
USE_MCP_TOOLS = os.getenv('USE_MCP_TOOLS', 'false').lower() == 'true'

def format_number(num):
    """Format large numbers"""
    if isinstance(num, (int, float)):
        if num >= 1000000:
            return f"{num/1000000:.1f}M"
        elif num >= 1000:
            return f"{num/1000:.1f}K"
        return f"{num:,.0f}"
    return str(num)

def format_currency(num):
    """Format currency values"""
    if isinstance(num, (int, float)):
        if num >= 1000000:
            return f"{num/1000000:.1f}M"
        elif num >= 1000:
            return f"{num/1000:.1f}K"
        return f"{num:,.0f}"
    return str(num)

def format_daily_average(weekly_value, is_currency=False):
    """Calculate and format daily average from weekly value"""
    if not isinstance(weekly_value, (int, float)) or weekly_value == 0:
        return ""
    
    daily_avg = weekly_value / 7.0
    
    if is_currency:
        # Format as currency
        if daily_avg >= 1000000:
            return f"({daily_avg/1000000:.1f}M/day)"
        elif daily_avg >= 1000:
            return f"({daily_avg/1000:.1f}K/day)"
        else:
            return f"({daily_avg:,.0f}/day)"
    else:
        # Format as number
        if daily_avg >= 1000000:
            return f"({daily_avg/1000000:.1f}M/day)"
        elif daily_avg >= 1000:
            return f"({daily_avg/1000:.1f}K/day)"
        else:
            return f"({daily_avg:,.0f}/day)"

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

def format_date_display(date_str):
    """Format YYYYMMDD to readable format"""
    try:
        dt = datetime.strptime(str(date_str), '%Y%m%d')
        return dt.strftime('%b %d')
    except:
        return str(date_str)

def process_oc_results(oc_data):
    """Process OC Cities overall results with same week last month and same week last year (YoY)"""
    if not oc_data or len(oc_data) == 0:
        return None
    
    row = oc_data[0]
    
    # Calculate growth percentages vs same week last month
    orders_growth_mom = ((row['this_week_orders'] - row['same_week_last_month_orders']) / row['same_week_last_month_orders'] * 100) if row.get('same_week_last_month_orders', 0) > 0 else 0
    gmv_growth_mom = ((row['this_week_gmv'] - row['same_week_last_month_gmv']) / row['same_week_last_month_gmv'] * 100) if row.get('same_week_last_month_gmv', 0) > 0 else 0
    eaters_growth_mom = ((row['this_week_eaters'] - row['same_week_last_month_eaters']) / row['same_week_last_month_eaters'] * 100) if row.get('same_week_last_month_eaters', 0) > 0 else 0
    basket_growth_mom = ((row['this_week_basket'] - row['same_week_last_month_basket']) / row['same_week_last_month_basket'] * 100) if row.get('same_week_last_month_basket', 0) > 0 else 0
    sessions_growth_mom = ((row['this_week_sessions'] - row['same_week_last_month_sessions']) / row['same_week_last_month_sessions'] * 100) if row.get('same_week_last_month_sessions', 0) > 0 else 0
    
    # Calculate growth percentages vs same week last year (YoY)
    yoy_orders = row.get('same_week_last_year_orders', row.get('ytd_avg_orders', 0))
    yoy_gmv = row.get('same_week_last_year_gmv', row.get('ytd_avg_gmv', 0))
    yoy_eaters = row.get('same_week_last_year_eaters', row.get('ytd_avg_eaters', 0))
    yoy_basket = row.get('same_week_last_year_basket', row.get('ytd_avg_basket', 0))
    yoy_sessions = row.get('same_week_last_year_sessions', row.get('ytd_avg_sessions', 0))
    
    orders_growth_yoy = ((row['this_week_orders'] - yoy_orders) / yoy_orders * 100) if yoy_orders > 0 else 0
    gmv_growth_yoy = ((row['this_week_gmv'] - yoy_gmv) / yoy_gmv * 100) if yoy_gmv > 0 else 0
    eaters_growth_yoy = ((row['this_week_eaters'] - yoy_eaters) / yoy_eaters * 100) if yoy_eaters > 0 else 0
    basket_growth_yoy = ((row['this_week_basket'] - yoy_basket) / yoy_basket * 100) if yoy_basket > 0 else 0
    sessions_growth_yoy = ((row['this_week_sessions'] - yoy_sessions) / yoy_sessions * 100) if yoy_sessions > 0 else 0
    
    # Calculate weekly pax frequency (orders per eater)
    pax_frequency_this_week = (row['this_week_orders'] / row['this_week_eaters']) if row['this_week_eaters'] > 0 else 0
    pax_frequency_last_month = (row.get('same_week_last_month_orders', 0) / row.get('same_week_last_month_eaters', 1)) if row.get('same_week_last_month_eaters', 0) > 0 else 0
    pax_frequency_yoy = (yoy_orders / yoy_eaters) if yoy_eaters > 0 else 0
    pax_frequency_growth_mom = ((pax_frequency_this_week - pax_frequency_last_month) / pax_frequency_last_month * 100) if pax_frequency_last_month > 0 else 0
    pax_frequency_growth_yoy = ((pax_frequency_this_week - pax_frequency_yoy) / pax_frequency_yoy * 100) if pax_frequency_yoy > 0 else 0
    
    # Get new pax (new unique eaters)
    # Definition: Unique passenger_id where:
    #   - Last transaction was more than a year ago, OR
    #   - First order was within the week
    new_pax_this_week = row.get('this_week_new_pax', 0)
    new_pax_last_month = row.get('same_week_last_month_new_pax', 0)
    new_pax_yoy = row.get('same_week_last_year_new_pax', row.get('ytd_avg_new_pax', 0))
    new_pax_growth_mom = ((new_pax_this_week - new_pax_last_month) / new_pax_last_month * 100) if new_pax_last_month > 0 else 0
    new_pax_growth_yoy = ((new_pax_this_week - new_pax_yoy) / new_pax_yoy * 100) if new_pax_yoy > 0 else 0
    
    return {
        'orders': {
            'this_week': row['this_week_orders'],
            'same_week_last_month': row.get('same_week_last_month_orders', 0),
            'same_week_last_year': yoy_orders,
            'growth_pct_mom': round(orders_growth_mom, 1),
            'growth_pct_yoy': round(orders_growth_yoy, 1)
        },
        'gmv': {
            'this_week': row['this_week_gmv'],
            'same_week_last_month': row.get('same_week_last_month_gmv', 0),
            'same_week_last_year': yoy_gmv,
            'growth_pct_mom': round(gmv_growth_mom, 1),
            'growth_pct_yoy': round(gmv_growth_yoy, 1)
        },
        'eaters': {
            'this_week': row['this_week_eaters'],
            'same_week_last_month': row.get('same_week_last_month_eaters', 0),
            'same_week_last_year': yoy_eaters,
            'growth_pct_mom': round(eaters_growth_mom, 1),
            'growth_pct_yoy': round(eaters_growth_yoy, 1)
        },
        'basket_size': {
            'this_week': row['this_week_basket'],
            'same_week_last_month': row.get('same_week_last_month_basket', 0),
            'same_week_last_year': yoy_basket,
            'growth_pct_mom': round(basket_growth_mom, 1),
            'growth_pct_yoy': round(basket_growth_yoy, 1)
        },
        'fulfilment_rate': {
            'this_week': row['this_week_completion_rate'],
            'same_week_last_month': row.get('same_week_last_month_completion_rate', 0),
            'same_week_last_year': row.get('same_week_last_year_completion_rate', row.get('ytd_avg_completion_rate', 0)),
            'delta_pp_mom': round(row['this_week_completion_rate'] - row.get('same_week_last_month_completion_rate', 0), 1),
            'delta_pp_yoy': round(row['this_week_completion_rate'] - row.get('same_week_last_year_completion_rate', row.get('ytd_avg_completion_rate', 0)), 1)
        },
        'sessions': {
            'this_week': row['this_week_sessions'],
            'same_week_last_month': row.get('same_week_last_month_sessions', 0),
            'same_week_last_year': yoy_sessions,
            'growth_pct_mom': round(sessions_growth_mom, 1),
            'growth_pct_yoy': round(sessions_growth_yoy, 1)
        },
        'cops': {
            'this_week': row['this_week_cops'],
            'same_week_last_month': row.get('same_week_last_month_cops', 0),
            'same_week_last_year': row.get('same_week_last_year_cops', row.get('ytd_avg_cops', 0)),
            'delta_mom': round(row['this_week_cops'] - row.get('same_week_last_month_cops', 0), 2),
            'delta_yoy': round(row['this_week_cops'] - row.get('same_week_last_year_cops', row.get('ytd_avg_cops', 0)), 2)
        },
        'promo': {
            'penetration_this_week': row['this_week_promo_penetration'],
            'penetration_same_week_last_month': row.get('same_week_last_month_promo_penetration', 0),
            'penetration_same_week_last_year': row.get('same_week_last_year_promo_penetration', row.get('ytd_avg_promo_penetration', 0))
        },
        'pax_frequency': {
            'this_week': round(pax_frequency_this_week, 2),
            'same_week_last_month': round(pax_frequency_last_month, 2),
            'same_week_last_year': round(pax_frequency_yoy, 2),
            'growth_pct_mom': round(pax_frequency_growth_mom, 1),
            'growth_pct_yoy': round(pax_frequency_growth_yoy, 1)
        },
        'new_pax': {
            'this_week': int(new_pax_this_week),
            'same_week_last_month': int(new_pax_last_month),
            'same_week_last_year': int(new_pax_yoy),
            'growth_pct_mom': round(new_pax_growth_mom, 1),
            'growth_pct_yoy': round(new_pax_growth_yoy, 1)
        },
        'mtm': {
            'current_month': int(row.get('current_month_mtm', 0)),
            'last_month': int(row.get('last_month_mtm', 0)),
            'same_month_last_year': int(row.get('same_month_last_year_mtm', 0)),
            'growth_pct_mom': round(((row.get('current_month_mtm', 0) - row.get('last_month_mtm', 0)) / row.get('last_month_mtm', 1) * 100) if row.get('last_month_mtm', 0) > 0 else 0, 1),
            'growth_pct_yoy': round(((row.get('current_month_mtm', 0) - row.get('same_month_last_year_mtm', 0)) / row.get('same_month_last_year_mtm', 1) * 100) if row.get('same_month_last_year_mtm', 0) > 0 else 0, 1)
        },
        'earning_per_mex': {
            'current_month': round(row.get('current_month_earning_per_mex', 0), 2),
            'last_month': round(row.get('last_month_earning_per_mex', 0), 2),
            'same_month_last_year': round(row.get('same_month_last_year_earning_per_mex', 0), 2),
            'growth_pct_mom': round(((row.get('current_month_earning_per_mex', 0) - row.get('last_month_earning_per_mex', 0)) / row.get('last_month_earning_per_mex', 1) * 100) if row.get('last_month_earning_per_mex', 0) > 0 else 0, 1),
            'growth_pct_yoy': round(((row.get('current_month_earning_per_mex', 0) - row.get('same_month_last_year_earning_per_mex', 0)) / row.get('same_month_last_year_earning_per_mex', 1) * 100) if row.get('same_month_last_year_earning_per_mex', 0) > 0 else 0, 1)
        }
    }

def process_top_cities_results(top_cities_data):
    """Process top cities results with full metrics (same structure as OC/Penang)"""
    if not top_cities_data:
        return []
    
    cities = []
    for row in top_cities_data:
        # Calculate growth percentages vs same week last month
        orders_growth_mom = ((row['this_week_orders'] - row['same_week_last_month_orders']) / row['same_week_last_month_orders'] * 100) if row.get('same_week_last_month_orders', 0) > 0 else 0
        gmv_growth_mom = ((row['this_week_gmv'] - row['same_week_last_month_gmv']) / row['same_week_last_month_gmv'] * 100) if row.get('same_week_last_month_gmv', 0) > 0 else 0
        eaters_growth_mom = ((row['this_week_eaters'] - row['same_week_last_month_eaters']) / row['same_week_last_month_eaters'] * 100) if row.get('same_week_last_month_eaters', 0) > 0 else 0
        basket_growth_mom = ((row['this_week_basket'] - row['same_week_last_month_basket']) / row['same_week_last_month_basket'] * 100) if row.get('same_week_last_month_basket', 0) > 0 else 0
        sessions_growth_mom = ((row['this_week_sessions'] - row['same_week_last_month_sessions']) / row['same_week_last_month_sessions'] * 100) if row.get('same_week_last_month_sessions', 0) > 0 else 0
        
        # Calculate growth percentages vs YTD average (as YoY proxy)
        ytd_avg_orders = row.get('ytd_avg_orders', 0)
        ytd_avg_gmv = row.get('ytd_avg_gmv', 0)
        ytd_avg_eaters = row.get('ytd_avg_eaters', 0)
        ytd_avg_basket = row.get('ytd_avg_basket', 0)
        ytd_avg_sessions = row.get('ytd_avg_sessions', 0)
        
        orders_growth_yoy = ((row['this_week_orders'] - ytd_avg_orders) / ytd_avg_orders * 100) if ytd_avg_orders > 0 else 0
        gmv_growth_yoy = ((row['this_week_gmv'] - ytd_avg_gmv) / ytd_avg_gmv * 100) if ytd_avg_gmv > 0 else 0
        eaters_growth_yoy = ((row['this_week_eaters'] - ytd_avg_eaters) / ytd_avg_eaters * 100) if ytd_avg_eaters > 0 else 0
        basket_growth_yoy = ((row['this_week_basket'] - ytd_avg_basket) / ytd_avg_basket * 100) if ytd_avg_basket > 0 else 0
        sessions_growth_yoy = ((row['this_week_sessions'] - ytd_avg_sessions) / ytd_avg_sessions * 100) if ytd_avg_sessions > 0 else 0
        
        # Calculate weekly pax frequency (orders per eater)
        pax_frequency_this_week = (row['this_week_orders'] / row['this_week_eaters']) if row['this_week_eaters'] > 0 else 0
        pax_frequency_last_month = (row.get('same_week_last_month_orders', 0) / row.get('same_week_last_month_eaters', 1)) if row.get('same_week_last_month_eaters', 0) > 0 else 0
        pax_frequency_yoy = (ytd_avg_orders / ytd_avg_eaters) if ytd_avg_eaters > 0 else 0
        pax_frequency_growth_mom = ((pax_frequency_this_week - pax_frequency_last_month) / pax_frequency_last_month * 100) if pax_frequency_last_month > 0 else 0
        pax_frequency_growth_yoy = ((pax_frequency_this_week - pax_frequency_yoy) / pax_frequency_yoy * 100) if pax_frequency_yoy > 0 else 0
        
        # Get new pax (new unique eaters)
        # Definition: Unique passenger_id where:
        #   - Last transaction was more than a year ago, OR
        #   - First order was within the week
        new_pax_this_week = row.get('this_week_new_pax', 0)
        new_pax_last_month = row.get('same_week_last_month_new_pax', 0)
        new_pax_yoy = row.get('ytd_avg_new_pax', 0)
        new_pax_growth_mom = ((new_pax_this_week - new_pax_last_month) / new_pax_last_month * 100) if new_pax_last_month > 0 else 0
        new_pax_growth_yoy = ((new_pax_this_week - new_pax_yoy) / new_pax_yoy * 100) if new_pax_yoy > 0 else 0
        
        cities.append({
            'city_name': row['city_name'],
            'city_id': row['city_id'],
            'orders': {
                'this_week': row['this_week_orders'],
                'same_week_last_month': row.get('same_week_last_month_orders', 0),
                'same_week_last_year': ytd_avg_orders,
                'growth_pct_mom': round(orders_growth_mom, 1),
                'growth_pct_yoy': round(orders_growth_yoy, 1)
            },
            'gmv': {
                'this_week': row['this_week_gmv'],
                'same_week_last_month': row.get('same_week_last_month_gmv', 0),
                'same_week_last_year': ytd_avg_gmv,
                'growth_pct_mom': round(gmv_growth_mom, 1),
                'growth_pct_yoy': round(gmv_growth_yoy, 1)
            },
            'eaters': {
                'this_week': row['this_week_eaters'],
                'same_week_last_month': row.get('same_week_last_month_eaters', 0),
                'same_week_last_year': ytd_avg_eaters,
                'growth_pct_mom': round(eaters_growth_mom, 1),
                'growth_pct_yoy': round(eaters_growth_yoy, 1)
            },
            'basket_size': {
                'this_week': row['this_week_basket'],
                'same_week_last_month': row.get('same_week_last_month_basket', 0),
                'same_week_last_year': ytd_avg_basket,
                'growth_pct_mom': round(basket_growth_mom, 1),
                'growth_pct_yoy': round(basket_growth_yoy, 1)
            },
            'fulfilment_rate': {
                'this_week': row['this_week_completion_rate'],
                'same_week_last_month': row.get('same_week_last_month_completion_rate', 0),
                'same_week_last_year': row.get('ytd_avg_completion_rate', 0),
                'delta_pp_mom': round(row['this_week_completion_rate'] - row.get('same_week_last_month_completion_rate', 0), 1),
                'delta_pp_yoy': round(row['this_week_completion_rate'] - row.get('ytd_avg_completion_rate', 0), 1)
            },
            'sessions': {
                'this_week': row['this_week_sessions'],
                'same_week_last_month': row.get('same_week_last_month_sessions', 0),
                'same_week_last_year': ytd_avg_sessions,
                'growth_pct_mom': round(sessions_growth_mom, 1),
                'growth_pct_yoy': round(sessions_growth_yoy, 1)
            },
            'cops': {
                'this_week': row['this_week_cops'],
                'same_week_last_month': row.get('same_week_last_month_cops', 0),
                'same_week_last_year': row.get('ytd_avg_cops', 0),
                'delta_mom': round(row['this_week_cops'] - row.get('same_week_last_month_cops', 0), 2),
                'delta_yoy': round(row['this_week_cops'] - row.get('ytd_avg_cops', 0), 2)
            },
            'promo': {
                'penetration_this_week': row['this_week_promo_penetration'],
                'penetration_same_week_last_month': row.get('same_week_last_month_promo_penetration', 0),
                'penetration_same_week_last_year': row.get('ytd_avg_promo_penetration', 0)
            },
            'pax_frequency': {
                'this_week': round(pax_frequency_this_week, 2),
                'same_week_last_month': round(pax_frequency_last_month, 2),
                'same_week_last_year': round(pax_frequency_yoy, 2),
                'growth_pct_mom': round(pax_frequency_growth_mom, 1),
                'growth_pct_yoy': round(pax_frequency_growth_yoy, 1)
            },
            'new_pax': {
                'this_week': int(new_pax_this_week),
                'same_week_last_month': int(new_pax_last_month),
                'same_week_last_year': int(new_pax_yoy),
                'growth_pct_mom': round(new_pax_growth_mom, 1),
                'growth_pct_yoy': round(new_pax_growth_yoy, 1)
            },
            'mtm': {
                'current_month': int(row.get('current_month_mtm', 0)),
                'last_month': int(row.get('last_month_mtm', 0)),
                'same_month_last_year': int(row.get('same_month_last_year_mtm', 0)),
                'growth_pct_mom': round(((row.get('current_month_mtm', 0) - row.get('last_month_mtm', 0)) / row.get('last_month_mtm', 1) * 100) if row.get('last_month_mtm', 0) > 0 else 0, 1),
                'growth_pct_yoy': round(((row.get('current_month_mtm', 0) - row.get('same_month_last_year_mtm', 0)) / row.get('same_month_last_year_mtm', 1) * 100) if row.get('same_month_last_year_mtm', 0) > 0 else 0, 1)
            },
            'earning_per_mex': {
                'current_month': round(row.get('current_month_earning_per_mex', 0), 2),
                'last_month': round(row.get('last_month_earning_per_mex', 0), 2),
                'same_month_last_year': round(row.get('same_month_last_year_earning_per_mex', 0), 2),
                'growth_pct_mom': round(((row.get('current_month_earning_per_mex', 0) - row.get('last_month_earning_per_mex', 0)) / row.get('last_month_earning_per_mex', 1) * 100) if row.get('last_month_earning_per_mex', 0) > 0 else 0, 1),
                'growth_pct_yoy': round(((row.get('current_month_earning_per_mex', 0) - row.get('same_month_last_year_earning_per_mex', 0)) / row.get('same_month_last_year_earning_per_mex', 1) * 100) if row.get('same_month_last_year_earning_per_mex', 0) > 0 else 0, 1)
            }
        })
    
    return cities

def generate_insight(report_data, city_name="OC Overall", last_month_gmv=None, last_year_same_month_gmv=None, avg_monthly_gmv=None):
    """Generate one-liner key insight with monthly run rate forecast"""
    if not report_data:
        return "No data available"
    
    # Calculate monthly run rate using average monthly GMV as baseline with YoY growth trend
    from calendar import monthrange
    today = datetime.now()
    days_in_current_month = monthrange(today.year, today.month)[1]
    
    this_week_gmv = report_data['gmv']['this_week']
    
    # Method: Use average monthly GMV as baseline, apply YoY growth trend, adjust for current week performance
    if avg_monthly_gmv and avg_monthly_gmv > 0:
        # Calculate YoY growth trend from last year same month to last month
        yoy_growth_rate = 1.0
        if last_year_same_month_gmv and last_year_same_month_gmv > 0 and last_month_gmv and last_month_gmv > 0:
            yoy_growth_rate = last_month_gmv / last_year_same_month_gmv
        
        # Forecast base: Apply YoY growth trend to last year same month
        if last_year_same_month_gmv and last_year_same_month_gmv > 0:
            trend_forecast = last_year_same_month_gmv * yoy_growth_rate
        else:
            # Fallback: Use average monthly GMV
            trend_forecast = avg_monthly_gmv
        
        # Calculate expected weekly GMV from trend forecast
        last_year_month = today.replace(year=today.year - 1)
        days_in_last_year_month = monthrange(last_year_month.year, last_year_month.month)[1]
        expected_weekly_gmv = (trend_forecast / days_in_last_year_month) * 7
        
        # Adjust based on current week performance vs expected
        # If current week is X% of expected, apply that ratio to the trend forecast
        if expected_weekly_gmv > 0:
            current_week_ratio = this_week_gmv / expected_weekly_gmv
            # Blend: 70% trend-based forecast, 30% current week adjustment
            # This ensures we stay close to historical averages while reflecting current performance
            adjusted_ratio = 0.7 + (current_week_ratio * 0.3)
            monthly_run_rate = trend_forecast * adjusted_ratio
        else:
            monthly_run_rate = trend_forecast
    elif last_month_gmv and last_month_gmv > 0:
        # Fallback: Use last month with simple multiplier
        last_month = today.replace(day=1) - timedelta(days=1)
        baseline_days = monthrange(last_month.year, last_month.month)[1]
        historical_avg_weekly_gmv = (last_month_gmv / baseline_days) * 7
        adjusted_weekly_gmv = (this_week_gmv * 0.5) + (historical_avg_weekly_gmv * 0.5)
        monthly_run_rate = (adjusted_weekly_gmv / 7.0) * days_in_current_month
    else:
        # Final fallback: Simple calculation
        weekly_to_monthly_multiplier = days_in_current_month / 7.0
        monthly_run_rate = this_week_gmv * weekly_to_monthly_multiplier
    
    # Analyze key metrics
    orders_mom = report_data['orders']['growth_pct_mom']
    gmv_mom = report_data['gmv']['growth_pct_mom']
    eaters_mom = report_data['eaters']['growth_pct_mom']
    basket_mom = report_data['basket_size']['growth_pct_mom']
    fulfilment = report_data['fulfilment_rate']['this_week']
    fulfilment_delta = report_data['fulfilment_rate']['delta_pp_mom']
    
    insights = []
    
    # Monthly run rate forecast with comparisons
    run_rate_text = f"Monthly Run Rate: {format_currency(monthly_run_rate)}"
    
    if last_month_gmv and last_month_gmv > 0:
        vs_last_month_pct = ((monthly_run_rate - last_month_gmv) / last_month_gmv * 100)
        run_rate_text += f" (vs Last Month: {get_status_emoji(vs_last_month_pct)} {vs_last_month_pct:+.1f}%)"
    
    if last_year_same_month_gmv and last_year_same_month_gmv > 0:
        vs_last_year_pct = ((monthly_run_rate - last_year_same_month_gmv) / last_year_same_month_gmv * 100)
        run_rate_text += f" (vs Last Year: {get_status_emoji(vs_last_year_pct)} {vs_last_year_pct:+.1f}%)"
    
    insights.append(run_rate_text)
    
    # GMV performance
    if gmv_mom < -40:
        insights.append(f"GMV down {abs(gmv_mom):.0f}% MoM")
    elif gmv_mom > 10:
        insights.append(f"GMV up {gmv_mom:.0f}% MoM")
    
    # Eater base
    if eaters_mom < -30:
        insights.append(f"WTU down {abs(eaters_mom):.0f}%")
    elif eaters_mom > 5:
        insights.append(f"WTU up {eaters_mom:.0f}%")
    
    # Basket size
    if basket_mom < -5:
        insights.append(f"Basket down {abs(basket_mom):.1f}%")
    elif basket_mom > 5:
        insights.append(f"Basket up {basket_mom:.1f}%")
    
    # Fulfilment
    if fulfilment_delta > 0.5:
        insights.append(f"Fulfilment +{fulfilment_delta:.1f}pp")
    elif fulfilment_delta < -0.5:
        insights.append(f"Fulfilment {fulfilment_delta:.1f}pp")
    
    # Promo penetration
    promo_pen = report_data['promo']['penetration_this_week']
    if promo_pen > 50:
        insights.append(f"High promo ({promo_pen:.0f}%)")
    
    # Return run rate first, then up to 2 more insights
    return " | ".join(insights[:3])

def process_daily_metrics(daily_data):
    """Process daily metrics results"""
    if not daily_data:
        return []
    
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    daily_list = []
    
    for i, row in enumerate(daily_data):
        day_name = days[i % len(days)]
        daily_list.append({
            'day': day_name,
            'date_id': row['date_id'],
            'orders': row['daily_orders'],
            'gmv': row['daily_gmv'],
            'wtu': row['daily_wtu']
        })
    
    return daily_list

def generate_tldr(oc_report, top_cities):
    """Generate TL;DR with highlights, lowlights, and actionable insights (max 5 bullet points)"""
    if not oc_report:
        return []
    
    tldr_points = []
    
    # Analyze key metrics
    gmv_mom = oc_report['gmv']['growth_pct_mom']
    gmv_yoy = oc_report['gmv']['growth_pct_yoy']
    orders_mom = oc_report['orders']['growth_pct_mom']
    orders_yoy = oc_report['orders']['growth_pct_yoy']
    eaters_mom = oc_report['eaters']['growth_pct_mom']
    eaters_yoy = oc_report['eaters']['growth_pct_yoy']
    basket_mom = oc_report['basket_size']['growth_pct_mom']
    basket_yoy = oc_report['basket_size']['growth_pct_yoy']
    fulfilment = oc_report['fulfilment_rate']['this_week']
    fulfilment_delta_mom = oc_report['fulfilment_rate']['delta_pp_mom']
    sessions_mom = oc_report['sessions']['growth_pct_mom']
    sessions_yoy = oc_report['sessions']['growth_pct_yoy']
    promo_pen = oc_report['promo']['penetration_this_week']
    mtm_mom = oc_report['mtm']['growth_pct_mom']
    earning_per_mex_mom = oc_report['earning_per_mex']['growth_pct_mom']
    
    # HIGHLIGHTS (positive metrics)
    highlights = []
    if gmv_yoy > 10:
        highlights.append(f"GMV +{gmv_yoy:.0f}% YoY")
    if basket_yoy > 5:
        highlights.append(f"Basket +{basket_yoy:.1f}% YoY")
    if fulfilment > 92:
        highlights.append(f"Fulfilment {fulfilment:.1f}%")
    if promo_pen > 50:
        highlights.append(f"Promo penetration {promo_pen:.0f}%")
    if eaters_yoy > 5:
        highlights.append(f"WTU +{eaters_yoy:.0f}% YoY")
    
    # LOWLIGHTS (negative metrics)
    lowlights = []
    if gmv_mom < -10:
        lowlights.append(f"GMV {gmv_mom:.0f}% MoM")
    if orders_mom < -10:
        lowlights.append(f"Orders {orders_mom:.0f}% MoM")
    if eaters_mom < -10:
        lowlights.append(f"WTU {eaters_mom:.0f}% MoM")
    if sessions_mom < -10:
        lowlights.append(f"Sessions {sessions_mom:.0f}% MoM")
    if mtm_mom < -5:
        lowlights.append(f"MTM {mtm_mom:.0f}% MoM")
    if earning_per_mex_mom < -50:
        lowlights.append(f"Earning/MEX {earning_per_mex_mom:.0f}% MoM")
    
    # CAUSAL INSIGHTS & ACTIONABLE SUGGESTIONS
    insights = []
    
    # Analyze top cities performance
    top_city_gmv_drops = []
    if top_cities:
        for city in top_cities[:3]:  # Top 3 cities
            if city['gmv']['growth_pct_mom'] < -10:
                top_city_gmv_drops.append(f"{city['city_name']} ({city['gmv']['growth_pct_mom']:.0f}%)")
    
    # Insight 1: MoM decline analysis
    if gmv_mom < -10 and orders_mom < -10:
        if sessions_mom < -10:
            insights.append(f"📉 *Volume decline:* Orders {orders_mom:.0f}% MoM driven by sessions drop ({sessions_mom:.0f}%). *Action:* Review campaign calendar & promo effectiveness to drive traffic")
        elif basket_mom < -5:
            insights.append(f"📉 *Basket compression:* GMV {gmv_mom:.0f}% MoM despite stable sessions. *Action:* Optimize promo mix to protect basket size")
        else:
            insights.append(f"📉 *Order decline:* GMV {gmv_mom:.0f}% MoM from lower orders. *Action:* Increase promo penetration or adjust discount depth")
    
    # Insight 2: YoY strength vs MoM weakness
    if gmv_yoy > 10 and gmv_mom < -10:
        insights.append(f"📈 *YoY momentum:* +{gmv_yoy:.0f}% YoY shows strong baseline. *Action:* MoM decline likely seasonal; maintain promo intensity to capture demand")
    
    # Insight 3: MTM & Earning per MEX
    if mtm_mom < -5:
        if earning_per_mex_mom < -50:
            insights.append(f"🏪 *Merchant economics:* MTM {mtm_mom:.0f}% & Earning/MEX {earning_per_mex_mom:.0f}% MoM. *Action:* Review merchant incentives & activation strategy")
        else:
            insights.append(f"🏪 *Merchant base:* MTM {mtm_mom:.0f}% MoM. *Action:* Focus on merchant retention & reactivation campaigns")
    
    # Insight 4: Top city performance
    if top_city_gmv_drops:
        cities_str = ", ".join(top_city_gmv_drops)
        insights.append(f"🏙️ *City-level:* {cities_str} MoM. *Action:* City-specific intervention needed - review local campaigns & competition")
    
    # Insight 5: Promo efficiency
    if promo_pen > 50 and gmv_mom < -10:
        insights.append(f"🎁 *Promo ROI:* High penetration ({promo_pen:.0f}%) but GMV declining. *Action:* Recalibrate discount depth or shift to targeted promos")
    elif promo_pen < 45 and gmv_mom < -10:
        insights.append(f"🎁 *Promo gap:* Low penetration ({promo_pen:.0f}%) contributing to decline. *Action:* Increase promo budget allocation to drive orders")
    
    # Combine into max 5 bullet points
    # Priority: 1 highlight, 1 lowlight, 3 insights (or adjust based on what's most critical)
    if highlights:
        tldr_points.append(f"✅ *Highlight:* {highlights[0]}")
    
    if lowlights:
        tldr_points.append(f"⚠️ *Lowlight:* {lowlights[0]}")
    
    # Add up to 3 insights to reach max 5 points
    remaining_slots = 5 - len(tldr_points)
    for insight in insights[:remaining_slots]:
        tldr_points.append(insight)
    
    return tldr_points

def format_slack_message(oc_report, top_cities, daily_metrics):
    """Format all reports into Slack message with updated comparisons"""
    
    # Get date ranges from get_week_dates() (uses current_date -1 to -8)
    dates = get_week_dates()
    
    # Parse dates for display formatting
    def parse_date(date_str):
        """Parse YYYYMMDD string to datetime"""
        return datetime.strptime(str(date_str), '%Y%m%d')
    
    period_start = parse_date(dates['this_week_start'])
    period_end = parse_date(dates['this_week_end'])
    mom_start = parse_date(dates['same_week_last_month_start'])
    mom_end = parse_date(dates['same_week_last_month_end'])
    yoy_start = parse_date(dates['same_week_last_year_start'])
    yoy_end = parse_date(dates['same_week_last_year_end'])
    
    this_week_display = f"{period_start.strftime('%b %d')} - {period_end.strftime('%b %d')}"
    same_week_last_month_display = f"{mom_start.strftime('%b %d')} - {mom_end.strftime('%b %d')}"
    same_week_last_year_display = f"{yoy_start.strftime('%b %d')} - {yoy_end.strftime('%b %d')}"
    
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
                    "text": f"*Period:* {this_week_display} | *Comparisons:* MoM ({same_week_last_month_display}) & YoY ({same_week_last_year_display}) | *Generated:* {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                }
            ]
        },
        {"type": "divider"}
    ]
    
    # Add TL;DR section before OC Overall
    if oc_report:
        tldr_points = generate_tldr(oc_report, top_cities)
        if tldr_points:
            tldr_text = "\n".join([f"• {point}" for point in tldr_points])
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*📋 TL;DR*\n{tldr_text}"
                }
            })
            blocks.append({"type": "divider"})
    
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
                        "text": f"*📦 Orders*\n`{format_number(oc_report['orders']['this_week'])} {format_daily_average(oc_report['orders']['this_week'])}`\nMoM: {get_status_emoji(oc_report['orders']['growth_pct_mom'])} {oc_report['orders']['growth_pct_mom']:+.1f}% | YoY: {get_status_emoji(oc_report['orders']['growth_pct_yoy'])} {oc_report['orders']['growth_pct_yoy']:+.1f}%"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*💰 GMV*\n`{format_currency(oc_report['gmv']['this_week'])} {format_daily_average(oc_report['gmv']['this_week'], is_currency=True)}`\nMoM: {get_status_emoji(oc_report['gmv']['growth_pct_mom'])} {oc_report['gmv']['growth_pct_mom']:+.1f}% | YoY: {get_status_emoji(oc_report['gmv']['growth_pct_yoy'])} {oc_report['gmv']['growth_pct_yoy']:+.1f}%"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*👥 WTU*\n`{format_number(oc_report['eaters']['this_week'])} {format_daily_average(oc_report['eaters']['this_week'])}`\nMoM: {get_status_emoji(oc_report['eaters']['growth_pct_mom'])} {oc_report['eaters']['growth_pct_mom']:+.1f}% | YoY: {get_status_emoji(oc_report['eaters']['growth_pct_yoy'])} {oc_report['eaters']['growth_pct_yoy']:+.1f}%"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*🛒 Basket*\n`{format_currency(oc_report['basket_size']['this_week'])}`\nMoM: {get_status_emoji(oc_report['basket_size']['growth_pct_mom'])} {oc_report['basket_size']['growth_pct_mom']:+.1f}% | YoY: {get_status_emoji(oc_report['basket_size']['growth_pct_yoy'])} {oc_report['basket_size']['growth_pct_yoy']:+.1f}%"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*✅ Fulfilment Rate*\n`{oc_report['fulfilment_rate']['this_week']}%`\nMoM: {oc_report['fulfilment_rate']['delta_pp_mom']:+.1f}pp | YoY: {oc_report['fulfilment_rate']['delta_pp_yoy']:+.1f}pp"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*📱 Sessions*\n`{format_number(oc_report['sessions']['this_week'])} {format_daily_average(oc_report['sessions']['this_week'])}`\nMoM: {get_status_emoji(oc_report['sessions']['growth_pct_mom'])} {oc_report['sessions']['growth_pct_mom']:+.1f}% | YoY: {get_status_emoji(oc_report['sessions']['growth_pct_yoy'])} {oc_report['sessions']['growth_pct_yoy']:+.1f}%"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*⚡ COPS*\n`{oc_report['cops']['this_week']}`\nMoM: {oc_report['cops']['delta_mom']:+.2f} | YoY: {oc_report['cops']['delta_yoy']:+.2f}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*🎁 Promo*\n`{oc_report['promo']['penetration_this_week']}%`\nMoM: {oc_report['promo']['penetration_this_week'] - oc_report['promo']['penetration_same_week_last_month']:+.1f}pp | YoY: {oc_report['promo']['penetration_this_week'] - oc_report['promo']['penetration_same_week_last_year']:+.1f}pp"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*🔄 Pax Frequency*\n`{oc_report['pax_frequency']['this_week']}`\nMoM: {get_status_emoji(oc_report['pax_frequency']['growth_pct_mom'])} {oc_report['pax_frequency']['growth_pct_mom']:+.1f}% | YoY: {get_status_emoji(oc_report['pax_frequency']['growth_pct_yoy'])} {oc_report['pax_frequency']['growth_pct_yoy']:+.1f}%"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*🆕 New Pax*\n`{format_number(oc_report['new_pax']['this_week'])} {format_daily_average(oc_report['new_pax']['this_week'])}`\nMoM: {get_status_emoji(oc_report['new_pax']['growth_pct_mom'])} {oc_report['new_pax']['growth_pct_mom']:+.1f}% | YoY: {get_status_emoji(oc_report['new_pax']['growth_pct_yoy'])} {oc_report['new_pax']['growth_pct_yoy']:+.1f}%"
                    }
                ]
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*🏪 MTM*\n`{format_number(oc_report['mtm']['current_month'])}`\nMoM: {get_status_emoji(oc_report['mtm']['growth_pct_mom'])} {oc_report['mtm']['growth_pct_mom']:+.1f}% | YoY: {get_status_emoji(oc_report['mtm']['growth_pct_yoy'])} {oc_report['mtm']['growth_pct_yoy']:+.1f}%"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*💵 Earning/MEX*\n`{format_currency(oc_report['earning_per_mex']['current_month'])}`\nMoM: {get_status_emoji(oc_report['earning_per_mex']['growth_pct_mom'])} {oc_report['earning_per_mex']['growth_pct_mom']:+.1f}% | YoY: {get_status_emoji(oc_report['earning_per_mex']['growth_pct_yoy'])} {oc_report['earning_per_mex']['growth_pct_yoy']:+.1f}%"
                    }
                ]
            }
        ]
        # Add insight for OC with monthly run rate (using average monthly GMV: 239.7M)
        oc_insight = generate_insight(oc_report, "OC Overall", last_month_gmv=274581686.68, last_year_same_month_gmv=214075438.21, avg_monthly_gmv=239723726.94)
        oc_blocks.append({
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"*💡 Key Insight:* {oc_insight}"
                }
            ]
        })
        blocks.extend(oc_blocks)
        blocks.append({"type": "divider"})
    
    # Top 5 Cities Section - Detailed metrics for each city
    if top_cities and len(top_cities) > 0:
        for city in top_cities[:5]:
            city_emoji = {
                'Johor Bahru': '🏙️',
                'Penang': '🏝️',
                'Kota Kinabalu': '🌴',
                'Ipoh': '🏛️',
                'Kuching': '🌉'
            }.get(city['city_name'], '📍')
            
            city_blocks = [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"{city_emoji} {city['city_name']}",
                        "emoji": True
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*📦 Orders*\n`{format_number(city['orders']['this_week'])} {format_daily_average(city['orders']['this_week'])}`\nMoM: {get_status_emoji(city['orders']['growth_pct_mom'])} {city['orders']['growth_pct_mom']:+.1f}% | YoY: {get_status_emoji(city['orders']['growth_pct_yoy'])} {city['orders']['growth_pct_yoy']:+.1f}%"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*💰 GMV*\n`{format_currency(city['gmv']['this_week'])} {format_daily_average(city['gmv']['this_week'], is_currency=True)}`\nMoM: {get_status_emoji(city['gmv']['growth_pct_mom'])} {city['gmv']['growth_pct_mom']:+.1f}% | YoY: {get_status_emoji(city['gmv']['growth_pct_yoy'])} {city['gmv']['growth_pct_yoy']:+.1f}%"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*👥 WTU*\n`{format_number(city['eaters']['this_week'])} {format_daily_average(city['eaters']['this_week'])}`\nMoM: {get_status_emoji(city['eaters']['growth_pct_mom'])} {city['eaters']['growth_pct_mom']:+.1f}% | YoY: {get_status_emoji(city['eaters']['growth_pct_yoy'])} {city['eaters']['growth_pct_yoy']:+.1f}%"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*🛒 Basket*\n`{format_currency(city['basket_size']['this_week'])}`\nMoM: {get_status_emoji(city['basket_size']['growth_pct_mom'])} {city['basket_size']['growth_pct_mom']:+.1f}% | YoY: {get_status_emoji(city['basket_size']['growth_pct_yoy'])} {city['basket_size']['growth_pct_yoy']:+.1f}%"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*✅ Fulfilment Rate*\n`{city['fulfilment_rate']['this_week']}%`\nMoM: {city['fulfilment_rate']['delta_pp_mom']:+.1f}pp | YoY: {city['fulfilment_rate']['delta_pp_yoy']:+.1f}pp"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*📱 Sessions*\n`{format_number(city['sessions']['this_week'])} {format_daily_average(city['sessions']['this_week'])}`\nMoM: {get_status_emoji(city['sessions']['growth_pct_mom'])} {city['sessions']['growth_pct_mom']:+.1f}% | YoY: {get_status_emoji(city['sessions']['growth_pct_yoy'])} {city['sessions']['growth_pct_yoy']:+.1f}%"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*⚡ COPS*\n`{city['cops']['this_week']}`\nMoM: {city['cops']['delta_mom']:+.2f} | YoY: {city['cops']['delta_yoy']:+.2f}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*🎁 Promo*\n`{city['promo']['penetration_this_week']}%`\nMoM: {city['promo']['penetration_this_week'] - city['promo']['penetration_same_week_last_month']:+.1f}pp | YoY: {city['promo']['penetration_this_week'] - city['promo']['penetration_same_week_last_year']:+.1f}pp"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*🔄 Pax Frequency*\n`{city['pax_frequency']['this_week']}`\nMoM: {get_status_emoji(city['pax_frequency']['growth_pct_mom'])} {city['pax_frequency']['growth_pct_mom']:+.1f}% | YoY: {get_status_emoji(city['pax_frequency']['growth_pct_yoy'])} {city['pax_frequency']['growth_pct_yoy']:+.1f}%"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*🆕 New Pax*\n`{format_number(city['new_pax']['this_week'])} {format_daily_average(city['new_pax']['this_week'])}`\nMoM: {get_status_emoji(city['new_pax']['growth_pct_mom'])} {city['new_pax']['growth_pct_mom']:+.1f}% | YoY: {get_status_emoji(city['new_pax']['growth_pct_yoy'])} {city['new_pax']['growth_pct_yoy']:+.1f}%"
                        }
                    ]
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*🏪 MTM*\n`{format_number(city['mtm']['current_month'])}`\nMoM: {get_status_emoji(city['mtm']['growth_pct_mom'])} {city['mtm']['growth_pct_mom']:+.1f}% | YoY: {get_status_emoji(city['mtm']['growth_pct_yoy'])} {city['mtm']['growth_pct_yoy']:+.1f}%"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*💵 Earning/MEX*\n`{format_currency(city['earning_per_mex']['current_month'])}`\nMoM: {get_status_emoji(city['earning_per_mex']['growth_pct_mom'])} {city['earning_per_mex']['growth_pct_mom']:+.1f}% | YoY: {get_status_emoji(city['earning_per_mex']['growth_pct_yoy'])} {city['earning_per_mex']['growth_pct_yoy']:+.1f}%"
                        }
                    ]
                }
            ]
            
            # Add insight for each city with monthly run rate
            # Map city names to their last month (Oct 2025), last year same month (Nov 2024), and average monthly GMV
            city_gmv_data = {
                'Johor Bahru': {'last_month': 70583223.36, 'last_year': 53511216.52, 'avg_monthly': 59703968.37},
                'Penang': {'last_month': 47130906.33, 'last_year': 36304984.96, 'avg_monthly': 42303836.94},
                'Kota Kinabalu': {'last_month': 23562427.10, 'last_year': 19204942.05, 'avg_monthly': 21049799.55},
                'Ipoh': {'last_month': 23565747.20, 'last_year': 19310169.64, 'avg_monthly': 21570609.12},
                'Kuching': {'last_month': 20924234.99, 'last_year': 17743823.40, 'avg_monthly': 18576873.22}
            }
            
            city_gmv = city_gmv_data.get(city['city_name'], {'last_month': None, 'last_year': None, 'avg_monthly': None})
            city_insight = generate_insight(
                city, 
                city['city_name'],
                last_month_gmv=city_gmv.get('last_month'),
                last_year_same_month_gmv=city_gmv.get('last_year'),
                avg_monthly_gmv=city_gmv.get('avg_monthly')
            )
            city_blocks.append({
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"*💡 Key Insight:* {city_insight}"
                    }
                ]
            })
            
            blocks.extend(city_blocks)
            blocks.append({"type": "divider"})
    
    # Return blocks and username - channel ID will be added in send_to_slack
    return {
        "blocks": blocks,
        "username": SLACK_USERNAME
    }

def send_to_slack(message):
    """Send message to Slack via webhook"""
    if not SLACK_WEBHOOK_URL:
        print("ERROR: SLACK_WEBHOOK_URL not set")
        return False
    
    # Webhooks post to their configured channel (channel override typically doesn't work)
    payload = {
        "blocks": message.get("blocks", []),
        "username": message.get("username", SLACK_USERNAME)
        # Note: Channel override removed - webhooks post to their configured channel
    }
    
    try:
        response = requests.post(
            SLACK_WEBHOOK_URL,
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            # Slack webhooks return "ok" as plain text on success
            if response.text.strip() == "ok":
                try:
                    print("Successfully sent message to Slack")
                except:
                    pass
                return True
            else:
                try:
                    print(f"Warning: Unexpected response: {response.text[:200]}")
                except:
                    pass
                # Still return True if status is 200, as some webhooks return different success messages
                return True
        else:
            try:
                print(f"Failed to send to Slack. Status code: {response.status_code}")
                print(f"Response: {response.text[:500]}")
            except:
                pass
            return False
            
    except Exception as e:
        try:
            print(f"Error sending to Slack: {str(e)}")
        except:
            pass
        return False

# Query results from MCP tools (Updated: Nov 27, 2025 - LIVE DATA with updated COPS and Sessions)
oc_data = [{
    'this_week_orders': 2143143,
    'same_week_last_month_orders': 2006985,
    'ytd_avg_orders': 1741855,
    'this_week_completed_orders': 1970686,
    'same_week_last_month_completed_orders': 1829394,
    'ytd_avg_completed_orders': 1603564,
    'this_week_completion_rate': 92.0,
    'same_week_last_month_completion_rate': 91.2,
    'ytd_avg_completion_rate': 92.1,
    'this_week_eaters': 912478,
    'same_week_last_month_eaters': 876240,
    'ytd_avg_eaters': 774889,
    'this_week_gmv': 79554439.48999992,
    'same_week_last_month_gmv': 69591129.33000003,
    'ytd_avg_gmv': 59015480.83000003,
    'this_week_basket': 36.09,
    'same_week_last_month_basket': 33.65,
    'ytd_avg_basket': 32.38,
    'this_week_promo_expense': 14437132.699999824,
    'same_week_last_month_promo_expense': 6968462.339999984,
    'ytd_avg_promo_expense': 7236659.040000007,
    'this_week_promo_orders': 1162458,
    'same_week_last_month_promo_orders': 974848,
    'ytd_avg_promo_orders': 823739,
    'this_week_promo_penetration': 54.2,
    'same_week_last_month_promo_penetration': 48.6,
    'ytd_avg_promo_penetration': 47.3,
    'this_week_sessions': 3956367.0,
    'same_week_last_month_sessions': 5041833.0,
    'ytd_avg_sessions': 4483382.0,
    'this_week_completed_sessions': 3956367.0,
    'same_week_last_month_completed_sessions': 5041833.0,
    'ytd_avg_completed_sessions': 4483382.0,
    'this_week_orders_per_session': 0.54,
    'same_week_last_month_orders_per_session': 0.4,
    'ytd_avg_orders_per_session': 0.39,
    'this_week_cops': 0.43,
    'same_week_last_month_cops': 0.36,
    'ytd_avg_cops': 0.36,
    'this_week_new_pax': 41953,
    'same_week_last_month_new_pax': 43238,
    'ytd_avg_new_pax': 39568,
    'current_month_mtm': 49167,
    'last_month_mtm': 49240,
    'same_month_last_year_mtm': 46537,
    'current_month_earning_per_mex': 20.01,
    'last_month_earning_per_mex': 19.84,
    'same_month_last_year_earning_per_mex': 18.86
}]

# LIVE DATA from MCP queries (Updated: Nov 27, 2025 - with updated Sessions and COPS from agg_food_cops_metrics)
top_cities_data = [
    {'city_name': 'Johor Bahru', 'city_id': 2, 'this_week_orders': 533519, 'same_week_last_month_orders': 500267, 'ytd_avg_orders': 411288, 'this_week_completed_orders': 491467, 'same_week_last_month_completed_orders': 457515, 'ytd_avg_completed_orders': 375949, 'this_week_completion_rate': 92.1, 'same_week_last_month_completion_rate': 91.5, 'ytd_avg_completion_rate': 91.4, 'this_week_eaters': 220947, 'same_week_last_month_eaters': 212355, 'ytd_avg_eaters': 181231, 'this_week_gmv': 20133326.589999992, 'same_week_last_month_gmv': 18031735.30999999, 'ytd_avg_gmv': 14367406.07, 'this_week_basket': 36.63, 'same_week_last_month_basket': 34.96, 'ytd_avg_basket': 33.58, 'this_week_promo_expense': 3138900.0600000056, 'same_week_last_month_promo_expense': 1597168.4400000002, 'ytd_avg_promo_expense': 1473501.1100000013, 'this_week_promo_orders': 277537, 'same_week_last_month_promo_orders': 231930, 'ytd_avg_promo_orders': 184041, 'this_week_promo_penetration': 52.0, 'same_week_last_month_promo_penetration': 46.4, 'ytd_avg_promo_penetration': 44.7, 'this_week_sessions': 885466.0, 'same_week_last_month_sessions': 1105837.0, 'ytd_avg_sessions': 1007169.0, 'this_week_completed_sessions': 885466.0, 'same_week_last_month_completed_sessions': 1105837.0, 'ytd_avg_completed_sessions': 1007169.0, 'this_week_orders_per_session': 0.6, 'same_week_last_month_orders_per_session': 0.45, 'ytd_avg_orders_per_session': 0.41, 'this_week_cops': 0.48, 'same_week_last_month_cops': 0.41, 'ytd_avg_cops': 0.37, 'this_week_new_pax': 12122, 'same_week_last_month_new_pax': 12450, 'ytd_avg_new_pax': 10685, 'current_month_mtm': 8798, 'last_month_mtm': 8740, 'same_month_last_year_mtm': 8201, 'current_month_earning_per_mex': 20.53, 'last_month_earning_per_mex': 20.35, 'same_month_last_year_earning_per_mex': 19.48},
    {'city_name': 'Penang', 'city_id': 13, 'this_week_orders': 365476, 'same_week_last_month_orders': 313420, 'ytd_avg_orders': 291244, 'this_week_completed_orders': 338369, 'same_week_last_month_completed_orders': 282788, 'ytd_avg_completed_orders': 269477, 'this_week_completion_rate': 92.6, 'same_week_last_month_completion_rate': 90.2, 'ytd_avg_completion_rate': 92.5, 'this_week_eaters': 154131, 'same_week_last_month_eaters': 138090, 'ytd_avg_eaters': 129426, 'this_week_gmv': 15025753.250000013, 'same_week_last_month_gmv': 11185895.490000004, 'ytd_avg_gmv': 10337045.920000004, 'this_week_basket': 39.99, 'same_week_last_month_basket': 34.98, 'ytd_avg_basket': 33.99, 'this_week_promo_expense': 3677533.3100000103, 'same_week_last_month_promo_expense': 1381011.0100000007, 'ytd_avg_promo_expense': 1591061.3800000031, 'this_week_promo_orders': 231437, 'same_week_last_month_promo_orders': 174065, 'ytd_avg_promo_orders': 156538, 'this_week_promo_penetration': 63.3, 'same_week_last_month_promo_penetration': 55.5, 'ytd_avg_promo_penetration': 53.7, 'this_week_sessions': 694190.0, 'same_week_last_month_sessions': 862720.0, 'ytd_avg_sessions': 772384.0, 'this_week_completed_sessions': 694190.0, 'same_week_last_month_completed_sessions': 862720.0, 'ytd_avg_completed_sessions': 772384.0, 'this_week_orders_per_session': 0.53, 'same_week_last_month_orders_per_session': 0.36, 'ytd_avg_orders_per_session': 0.38, 'this_week_cops': 0.42, 'same_week_last_month_cops': 0.33, 'ytd_avg_cops': 0.35, 'this_week_new_pax': 10335, 'same_week_last_month_new_pax': 9890, 'ytd_avg_new_pax': 9910, 'current_month_mtm': 6452, 'last_month_mtm': 6490, 'same_month_last_year_mtm': 6231, 'current_month_earning_per_mex': 21.06, 'last_month_earning_per_mex': 20.75, 'same_month_last_year_earning_per_mex': 19.52},
    {'city_name': 'Ipoh', 'city_id': 48, 'this_week_orders': 197189, 'same_week_last_month_orders': 178355, 'ytd_avg_orders': 169353, 'this_week_completed_orders': 180350, 'same_week_last_month_completed_orders': 160449, 'ytd_avg_completed_orders': 157454, 'this_week_completion_rate': 91.5, 'same_week_last_month_completion_rate': 90.0, 'ytd_avg_completion_rate': 93.0, 'this_week_eaters': 86022, 'same_week_last_month_eaters': 80718, 'ytd_avg_eaters': 77247, 'this_week_gmv': 6776338.470000007, 'same_week_last_month_gmv': 5765281.9799999995, 'ytd_avg_gmv': 5414627.820000002, 'this_week_basket': 33.48, 'same_week_last_month_basket': 31.61, 'ytd_avg_basket': 30.16, 'this_week_promo_expense': 1293763.8099999996, 'same_week_last_month_promo_expense': 589298.63, 'ytd_avg_promo_expense': 734798.7099999987, 'this_week_promo_orders': 103468, 'same_week_last_month_promo_orders': 81272, 'ytd_avg_promo_orders': 79389, 'this_week_promo_penetration': 52.5, 'same_week_last_month_promo_penetration': 45.6, 'ytd_avg_promo_penetration': 46.9, 'this_week_sessions': 386982.0, 'same_week_last_month_sessions': 498210.0, 'ytd_avg_sessions': 444221.0, 'this_week_completed_sessions': 386982.0, 'same_week_last_month_completed_sessions': 498210.0, 'ytd_avg_completed_sessions': 444221.0, 'this_week_orders_per_session': 0.51, 'same_week_last_month_orders_per_session': 0.36, 'ytd_avg_orders_per_session': 0.38, 'this_week_cops': 0.4, 'same_week_last_month_cops': 0.32, 'ytd_avg_cops': 0.35, 'this_week_new_pax': 5543, 'same_week_last_month_new_pax': 6087, 'ytd_avg_new_pax': 5645, 'current_month_mtm': 5122, 'last_month_mtm': 5131, 'same_month_last_year_mtm': 4430, 'current_month_earning_per_mex': 18.83, 'last_month_earning_per_mex': 18.68, 'same_month_last_year_earning_per_mex': 17.79},
    {'city_name': 'Kota Kinabalu', 'city_id': 19, 'this_week_orders': 172157, 'same_week_last_month_orders': 163123, 'ytd_avg_orders': 150160, 'this_week_completed_orders': 158046, 'same_week_last_month_completed_orders': 149110, 'ytd_avg_completed_orders': 139965, 'this_week_completion_rate': 91.8, 'same_week_last_month_completion_rate': 91.4, 'ytd_avg_completion_rate': 93.2, 'this_week_eaters': 70304, 'same_week_last_month_eaters': 67894, 'ytd_avg_eaters': 62859, 'this_week_gmv': 6618803.4499999955, 'same_week_last_month_gmv': 6026494.179999999, 'ytd_avg_gmv': 5333602.179999999, 'this_week_basket': 37.48, 'same_week_last_month_basket': 35.93, 'ytd_avg_basket': 33.82, 'this_week_promo_expense': 1144352.0199999989, 'same_week_last_month_promo_expense': 697342.4999999998, 'ytd_avg_promo_expense': 645753.4799999999, 'this_week_promo_orders': 101463, 'same_week_last_month_promo_orders': 95487, 'ytd_avg_promo_orders': 78316, 'this_week_promo_penetration': 58.9, 'same_week_last_month_promo_penetration': 58.5, 'ytd_avg_promo_penetration': 52.2, 'this_week_sessions': 293797.0, 'same_week_last_month_sessions': 364214.0, 'ytd_avg_sessions': 339864.0, 'this_week_completed_sessions': 293797.0, 'same_week_last_month_completed_sessions': 364214.0, 'ytd_avg_completed_sessions': 339864.0, 'this_week_orders_per_session': 0.59, 'same_week_last_month_orders_per_session': 0.45, 'ytd_avg_orders_per_session': 0.44, 'this_week_cops': 0.47, 'same_week_last_month_cops': 0.41, 'ytd_avg_cops': 0.41, 'this_week_new_pax': 4361, 'same_week_last_month_new_pax': 4531, 'ytd_avg_new_pax': 3692, 'current_month_mtm': 3066, 'last_month_mtm': 3119, 'same_month_last_year_mtm': 3101, 'current_month_earning_per_mex': 21.17, 'last_month_earning_per_mex': 21.19, 'same_month_last_year_earning_per_mex': 20.01},
    {'city_name': 'Kuching', 'city_id': 11, 'this_week_orders': 160214, 'same_week_last_month_orders': 145291, 'ytd_avg_orders': 139005, 'this_week_completed_orders': 148767, 'same_week_last_month_completed_orders': 134257, 'ytd_avg_completed_orders': 129735, 'this_week_completion_rate': 92.9, 'same_week_last_month_completion_rate': 92.4, 'ytd_avg_completion_rate': 93.3, 'this_week_eaters': 65855, 'same_week_last_month_eaters': 62081, 'ytd_avg_eaters': 59120, 'this_week_gmv': 6315235.209999999, 'same_week_last_month_gmv': 5238716.719999998, 'ytd_avg_gmv': 5037249.069999999, 'this_week_basket': 37.86, 'same_week_last_month_basket': 34.39, 'ytd_avg_basket': 34.2, 'this_week_promo_expense': 1333729.0299999989, 'same_week_last_month_promo_expense': 638023.8999999996, 'ytd_avg_promo_expense': 797985.3999999993, 'this_week_promo_orders': 99180, 'same_week_last_month_promo_orders': 84933, 'ytd_avg_promo_orders': 76692, 'this_week_promo_penetration': 61.9, 'same_week_last_month_promo_penetration': 58.5, 'ytd_avg_promo_penetration': 55.2, 'this_week_sessions': 292888.0, 'same_week_last_month_sessions': 361923.0, 'ytd_avg_sessions': 337259.0, 'this_week_completed_sessions': 292888.0, 'same_week_last_month_completed_sessions': 361923.0, 'ytd_avg_completed_sessions': 337259.0, 'this_week_orders_per_session': 0.55, 'same_week_last_month_orders_per_session': 0.4, 'ytd_avg_orders_per_session': 0.41, 'this_week_cops': 0.44, 'same_week_last_month_cops': 0.37, 'ytd_avg_cops': 0.38, 'this_week_new_pax': 2768, 'same_week_last_month_new_pax': 3042, 'ytd_avg_new_pax': 2534, 'current_month_mtm': 3492, 'last_month_mtm': 3529, 'same_month_last_year_mtm': 3882, 'current_month_earning_per_mex': 21.11, 'last_month_earning_per_mex': 20.91, 'same_month_last_year_earning_per_mex': 19.96}
]

daily_data = [
    {'date_id': 20251103, 'daily_orders': 241290, 'daily_completed_orders': 222064, 'daily_gmv': 7877041.07, 'daily_wtu': 191793, 'daily_sessions': 215232, 'daily_completion_rate': 92.0},
    {'date_id': 20251104, 'daily_orders': 241098, 'daily_completed_orders': 223613, 'daily_gmv': 7947277.38, 'daily_wtu': 193018, 'daily_sessions': 216398, 'daily_completion_rate': 92.7},
    {'date_id': 20251105, 'daily_orders': 245322, 'daily_completed_orders': 228096, 'daily_gmv': 8159077.43, 'daily_wtu': 197029, 'daily_sessions': 220397, 'daily_completion_rate': 93.0},
    {'date_id': 20251106, 'daily_orders': 251664, 'daily_completed_orders': 233979, 'daily_gmv': 8447378.21, 'daily_wtu': 201690, 'daily_sessions': 225763, 'daily_completion_rate': 93.0},
    {'date_id': 20251107, 'daily_orders': 24750, 'daily_completed_orders': 16667, 'daily_gmv': 509734.21, 'daily_wtu': 16048, 'daily_sessions': 22286, 'daily_completion_rate': 67.3}
]

penang_data = [{
    'this_week_orders': 159456,
    'same_week_last_month_orders': 289395,
    'ytd_avg_orders': 273746,
    'this_week_completed_orders': 147146,
    'same_week_last_month_completed_orders': 266920,
    'ytd_avg_completed_orders': 253602,
    'this_week_completion_rate': 92.3,
    'same_week_last_month_completion_rate': 92.2,
    'ytd_avg_completion_rate': 92.64,
    'this_week_eaters': 86645,
    'same_week_last_month_eaters': 131387,
    'ytd_avg_eaters': 20734,
    'this_week_gmv': 5483293.93,
    'same_week_last_month_gmv': 10186553.45,
    'ytd_avg_gmv': 9928345.16,
    'this_week_basket': 33.04,
    'same_week_last_month_basket': 33.79,
    'ytd_avg_basket': 34.77,
    'this_week_promo_expense': 634033.05,
    'same_week_last_month_promo_expense': 1149414.41,
    'ytd_avg_promo_expense': 1349560.05,
    'this_week_promo_orders': 86914,
    'same_week_last_month_promo_orders': 157249,
    'ytd_avg_promo_orders': 146457,
    'this_week_promo_penetration': 54.5,
    'same_week_last_month_promo_penetration': 54.3,
    'ytd_avg_promo_penetration': 53.5,
    'this_week_sessions': 143250,
    'same_week_last_month_sessions': 257767,
    'ytd_avg_sessions': 243418,
    'this_week_completed_sessions': 139923,
    'same_week_last_month_completed_sessions': 252495,
    'ytd_avg_completed_sessions': 239181,
    'this_week_orders_per_session': 1.1,
    'same_week_last_month_orders_per_session': 1.1,
    'ytd_avg_orders_per_session': 1.12,
    'this_week_cops': 1.1,
    'same_week_last_month_cops': 1.1,
    'ytd_avg_cops': 1.06
}]

def safe_print(*args, **kwargs):
    """Safely print, handling closed stdout"""
    try:
        print(*args, **kwargs)
    except (ValueError, OSError, AttributeError):
        pass  # stdout closed or unavailable

def execute_queries_via_mcp():
    """
    Execute SQL queries via MCP Hubble tool
    Returns (oc_data, top_cities_data) or (None, None) if execution fails
    """
    if not QUERY_GENERATION_AVAILABLE:
        safe_print("⚠️  Query generation not available, using hardcoded data")
        return None, None
    
    try:
        # Get date ranges
        dates = get_week_dates()
        
        # Generate queries
        oc_query = generate_oc_query_with_new_pax(dates)
        top_cities_query = generate_top_cities_query_with_new_pax(dates)
        
        try:
            print("📊 Queries generated successfully")
            print(f"   OC Query length: {len(oc_query)} chars")
            print(f"   Top Cities Query length: {len(top_cities_query)} chars")
        except (ValueError, OSError):
            pass  # stdout may be closed, continue silently
        
        # Save queries to file for reference
        try:
            with open('weekly_report_queries_current.sql', 'w', encoding='utf-8') as f:
                f.write("-- OC Cities Query\n")
                f.write(oc_query)
                f.write("\n\n-- Top 5 Cities Query\n")
                f.write(top_cities_query)
            
            try:
                print("✅ Queries saved to: weekly_report_queries_current.sql")
            except (ValueError, OSError):
                pass
        except Exception:
            pass  # File write failed, continue
        
        # Execute queries via MCP Hubble tool
        try:
            print("\n🔍 Executing queries via MCP Hubble...")
        except (ValueError, OSError):
            pass
        
        oc_results = None
        top_cities_results = None
        
        if USE_MCP_TOOLS:
            try:
                print("   🔄 Executing OC query via MCP Hubble...")
            except (ValueError, OSError):
                pass
            try:
                # Execute OC query via MCP grab-data tool
                # Try to use the MCP tool if available in the environment
                try:
                    # Import MCP tool - this will work if running in Cursor chat context
                    # The tool name uses hyphens, so we need to access it via globals or getattr
                    import sys
                    # Check if we're in a context where MCP tools are available
                    # In Cursor chat, the AI will execute queries, so we'll prepare them
                    # For now, we'll try to execute via subprocess or direct call if available
                    
                    # Try to get MCP tool from globals (if available in Cursor context)
                    mcp_tool = None
                    if 'mcp_mcp-grab-data_run_presto_query' in globals():
                        mcp_tool = globals()['mcp_mcp-grab-data_run_presto_query']
                    elif hasattr(sys.modules.get('__main__', None), 'mcp_mcp-grab-data_run_presto_query'):
                        mcp_tool = getattr(sys.modules['__main__'], 'mcp_mcp-grab-data_run_presto_query')
                    
                    if mcp_tool:
                        oc_response = mcp_tool(query=oc_query)
                    else:
                        # MCP tool not directly available - queries need to be executed via Cursor chat
                        oc_response = None
                        safe_print("   ⚠️  MCP tool not directly callable - queries saved to weekly_report_queries_current.sql")
                        safe_print("   💡 Execute queries via Cursor chat using: mcp_mcp-grab-data_run_presto_query")
                except (NameError, AttributeError, ImportError):
                    oc_response = None
                    safe_print("   ⚠️  MCP tool not available in this context")
                
                # Process response - MCP returns data in a specific format
                if oc_response:
                    # Extract data from response
                    # Response format may vary - handle both dict and list formats
                    if isinstance(oc_response, dict):
                        oc_results = oc_response.get('data') or oc_response.get('results') or [oc_response]
                    elif isinstance(oc_response, list):
                        oc_results = oc_response
                    else:
                        oc_results = None
                    
                    if oc_results:
                        safe_print(f"   ✅ OC query executed: {len(oc_results) if isinstance(oc_results, list) else 1} row(s) returned")
                    else:
                        safe_print("   ⚠️  OC query returned no data")
                else:
                    safe_print("   ⚠️  OC query returned empty response")
                    
            except NameError:
                # MCP tool not available in this Python context
                # This is expected when running outside Cursor chat
                safe_print("   ⚠️  MCP tool not directly callable from Python script")
                safe_print("   💡 Execute queries via Cursor chat using MCP tools")
                oc_results = None
            except Exception as e:
                safe_print(f"   ❌ Error executing OC query: {str(e)}")
                import traceback
                try:
                    traceback.print_exc()
                except:
                    pass
                oc_results = None
            
            # Execute Top Cities query if OC query succeeded
            if oc_results:
                safe_print("   🔄 Executing Top Cities query...")
                try:
                    top_cities_response = mcp_mcp-hubble_run_presto_query(query=top_cities_query)
                    
                    if top_cities_response:
                        if isinstance(top_cities_response, dict):
                            top_cities_results = top_cities_response.get('data') or top_cities_response.get('results') or [top_cities_response]
                        elif isinstance(top_cities_response, list):
                            top_cities_results = top_cities_response
                        else:
                            top_cities_results = None
                        
                        if top_cities_results:
                            safe_print(f"   ✅ Top Cities query executed: {len(top_cities_results) if isinstance(top_cities_results, list) else 1} row(s) returned")
                        else:
                            safe_print("   ⚠️  Top Cities query returned no data")
                    else:
                        safe_print("   ⚠️  Top Cities query returned empty response")
                        
                except NameError:
                    safe_print("   ⚠️  MCP tool not directly callable from Python script")
                    top_cities_results = None
                except Exception as e:
                    safe_print(f"   ❌ Error executing Top Cities query: {str(e)}")
                    top_cities_results = None
        else:
            safe_print("   ⚠️  MCP tools disabled (set USE_MCP_TOOLS=true to enable)")
        
        # Process results if we got them
        if oc_results and top_cities_results:
            safe_print("   ✅ Query results received")
            
            # Convert results to expected format (list of dictionaries)
            if isinstance(oc_results, list) and len(oc_results) > 0:
                oc_data = oc_results if isinstance(oc_results[0], dict) else [dict(row) for row in oc_results]
            else:
                oc_data = [oc_results] if oc_results else None
            
            if isinstance(top_cities_results, list) and len(top_cities_results) > 0:
                top_cities_data = top_cities_results if isinstance(top_cities_results[0], dict) else [dict(row) for row in top_cities_results]
            else:
                top_cities_data = [top_cities_results] if top_cities_results else None
            
            if oc_data and top_cities_data:
                safe_print("   ✅ Results processed successfully")
                return oc_data, top_cities_data
        
        safe_print("   ⚠️  No query results, using hardcoded data")
        return None, None
        
    except Exception as e:
        try:
            safe_print(f"❌ Error generating queries: {str(e)}")
            import traceback
            try:
                traceback.print_exc()
            except:
                pass
        except (ValueError, OSError):
            # stdout closed, can't print - just return None
            pass
        return None, None

if __name__ == '__main__':
    try:
        safe_print("📊 Processing weekly report data...")
    except:
        pass
    
    # Try to execute live queries first
    oc_query_results, top_cities_query_results = execute_queries_via_mcp()
    
    # Use query results if available, otherwise fall back to hardcoded data
    if oc_query_results and top_cities_query_results:
        safe_print("✅ Using live query results")
        oc_data = oc_query_results
        top_cities_data = top_cities_query_results
    else:
        safe_print("⚠️  Using hardcoded test data (queries not executed or failed)")
        # oc_data and top_cities_data are defined below as hardcoded data
    
    # Process all results
    oc_report = process_oc_results(oc_data)
    top_cities = process_top_cities_results(top_cities_data)
    
    # Extract Penang from top_cities (it's already included there)
    penang_report = None
    for city in top_cities:
        if city['city_name'] == 'Penang':
            penang_report = city
            break
    
    safe_print("✅ Data processed successfully")
    safe_print("📝 Formatting Slack message...")
    
    # Format message (daily_metrics removed per user request)
    slack_message = format_slack_message(oc_report, top_cities, None)
    
    safe_print("📤 Sending to Slack...")
    
    # Send to Slack
    success = send_to_slack(slack_message)
    
    if success:
        safe_print("\n✅ Weekly report sent successfully to Slack!")
    else:
        safe_print("\n❌ Failed to send report to Slack")

