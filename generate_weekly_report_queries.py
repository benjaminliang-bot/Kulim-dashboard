"""
Generate Weekly Report Queries with Current Dates
This script generates all queries needed for the enhanced weekly report
"""

import sys
from datetime import datetime, timedelta

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

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

def generate_oc_query(this_week_start, this_week_end, last_week_start, last_week_end):
    """Generate OC Cities overall query"""
    return f"""
-- OC CITIES OVERALL (This Week vs Last Week)
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

def generate_top_cities_query(this_week_start, this_week_end, last_week_start, last_week_end):
    """Generate Top 5 Cities by GMV query"""
    return f"""
-- TOP 5 CITIES BY GMV (OC) - This Week vs Last Week
WITH this_week_cities AS (
    SELECT 
        f.city_id,
        dc.city_name,
        SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.gross_merchandise_value ELSE 0 END) as gmv,
        COUNT(DISTINCT f.order_id) as orders,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.passenger_id END) as unique_eaters
    FROM ocd_adw.f_food_metrics f
    JOIN ocd_adw.d_city dc ON f.city_id = dc.city_id
    WHERE f.country_id = 1 
      AND f.city_id != 1
      AND f.date_id >= {this_week_start} AND f.date_id <= {this_week_end}
      AND f.business_type = 0
    GROUP BY f.city_id, dc.city_name
),
last_week_cities AS (
    SELECT 
        f.city_id,
        dc.city_name,
        SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.gross_merchandise_value ELSE 0 END) as gmv,
        COUNT(DISTINCT f.order_id) as orders,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.passenger_id END) as unique_eaters
    FROM ocd_adw.f_food_metrics f
    JOIN ocd_adw.d_city dc ON f.city_id = dc.city_id
    WHERE f.country_id = 1 
      AND f.city_id != 1
      AND f.date_id >= {last_week_start} AND f.date_id <= {last_week_end}
      AND f.business_type = 0
    GROUP BY f.city_id, dc.city_name
)
SELECT 
    tw.city_name,
    tw.city_id,
    COALESCE(lw.gmv, 0) as last_week_gmv,
    tw.gmv as this_week_gmv,
    tw.gmv - COALESCE(lw.gmv, 0) as gmv_delta,
    ROUND((tw.gmv - COALESCE(lw.gmv, 0)) / NULLIF(COALESCE(lw.gmv, 0), 0) * 100, 2) as gmv_growth_pct,
    COALESCE(lw.orders, 0) as last_week_orders,
    tw.orders as this_week_orders,
    COALESCE(lw.unique_eaters, 0) as last_week_eaters,
    tw.unique_eaters as this_week_eaters
FROM this_week_cities tw
LEFT JOIN last_week_cities lw ON tw.city_id = lw.city_id
ORDER BY tw.gmv DESC
LIMIT 5
"""

def generate_daily_metrics_query(this_week_start, this_week_end):
    """Generate Daily Metrics query"""
    return f"""
-- DAILY METRICS (This Week) - OC Cities
SELECT 
    CAST(date_format(from_iso8601_date(CAST(f.date_id AS VARCHAR)), '%Y%m%d') AS INT) AS date_id,
    COUNT(DISTINCT f.order_id) as daily_orders,
    COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END) as daily_completed_orders,
    SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.gross_merchandise_value ELSE 0 END) as daily_gmv,
    COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.passenger_id END) as daily_wtu,
    COUNT(DISTINCT f.scribe_session_id) as daily_sessions,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END) / 
          NULLIF(COUNT(DISTINCT f.order_id), 0), 2) as daily_completion_rate
FROM ocd_adw.f_food_metrics f
WHERE f.country_id = 1 
  AND f.city_id != 1
  AND f.date_id >= {this_week_start} AND f.date_id <= {this_week_end}
  AND f.business_type = 0
GROUP BY CAST(date_format(from_iso8601_date(CAST(f.date_id AS VARCHAR)), '%Y%m%d') AS INT)
ORDER BY date_id
"""

def generate_penang_query(this_week_start, this_week_end, last_week_start, last_week_end):
    """Generate Penang query"""
    return f"""
-- PENANG (This Week vs Last Week)
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

def main():
    """Generate all queries with current dates"""
    this_week_start, this_week_end, last_week_start, last_week_end = get_week_dates()
    
    print("=" * 60)
    print("Weekly Report Queries Generator")
    print("=" * 60)
    print(f"\n📅 Date Ranges:")
    print(f"   This Week: {this_week_start} - {this_week_end}")
    print(f"   Last Week: {last_week_start} - {last_week_end}")
    
    # Generate queries
    oc_query = generate_oc_query(this_week_start, this_week_end, last_week_start, last_week_end)
    top_cities_query = generate_top_cities_query(this_week_start, this_week_end, last_week_start, last_week_end)
    daily_metrics_query = generate_daily_metrics_query(this_week_start, this_week_end)
    penang_query = generate_penang_query(this_week_start, this_week_end, last_week_start, last_week_end)
    
    # Save to file
    with open('weekly_report_queries_current.sql', 'w') as f:
        f.write("-- Weekly Report Queries with Current Dates\n")
        f.write(f"-- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"-- This Week: {this_week_start} - {this_week_end}\n")
        f.write(f"-- Last Week: {last_week_start} - {last_week_end}\n\n")
        f.write("=" * 60 + "\n")
        f.write("1. OC CITIES OVERALL\n")
        f.write("=" * 60 + "\n")
        f.write(oc_query)
        f.write("\n\n" + "=" * 60 + "\n")
        f.write("2. TOP 5 CITIES BY GMV\n")
        f.write("=" * 60 + "\n")
        f.write(top_cities_query)
        f.write("\n\n" + "=" * 60 + "\n")
        f.write("3. DAILY METRICS\n")
        f.write("=" * 60 + "\n")
        f.write(daily_metrics_query)
        f.write("\n\n" + "=" * 60 + "\n")
        f.write("4. PENANG\n")
        f.write("=" * 60 + "\n")
        f.write(penang_query)
    
    print("\n✅ Queries generated and saved to: weekly_report_queries_current.sql")
    print("\n📋 Next Steps:")
    print("   1. Execute these queries via MCP tools in Cursor")
    print("   2. Process results using run_weekly_report_enhanced.py")
    print("   3. Send to Slack")
    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())

