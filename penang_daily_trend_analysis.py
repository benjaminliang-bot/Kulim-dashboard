"""
Penang Daily GMV & Orders Trend Analysis
Compare last completed week vs same week last year
Identify anomalies and perform causal inference analysis
"""

import sys
from datetime import datetime, timedelta
from calendar import monthrange

def get_week_dates():
    """Get date ranges for last completed week and same week last year"""
    today = datetime.now()
    
    # Calculate last completed week (Monday to Sunday)
    yesterday = today - timedelta(days=1)
    days_since_sunday = (yesterday.weekday() + 1) % 7
    if days_since_sunday == 0:
        last_week_end = yesterday
    else:
        last_week_end = yesterday - timedelta(days=days_since_sunday)
    
    last_week_start = last_week_end - timedelta(days=6)
    
    # Same week last year
    same_week_last_year_start = last_week_start.replace(year=last_week_start.year - 1)
    same_week_last_year_end = last_week_end.replace(year=last_week_end.year - 1)
    
    def format_date(d):
        return d.strftime('%Y%m%d')
    
    return {
        'this_week_start': format_date(last_week_start),
        'this_week_end': format_date(last_week_end),
        'same_week_last_year_start': format_date(same_week_last_year_start),
        'same_week_last_year_end': format_date(same_week_last_year_end)
    }

def generate_penang_daily_query(dates):
    """Generate SQL query for daily Penang GMV and orders for both periods"""
    return f"""
-- Penang Daily GMV & Orders Trend Analysis
-- Last Completed Week vs Same Week Last Year

WITH this_week_data AS (
    SELECT 
        f.date_id,
        CAST(date_format(from_iso8601_date(CAST(f.date_id AS VARCHAR)), '%Y%m%d') AS INT) AS formatted_date,
        COUNT(DISTINCT f.order_id) as daily_orders,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END) as daily_completed_orders,
        SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN COALESCE(f.gross_merchandise_value, 0) ELSE 0 END) as daily_gmv,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.passenger_id END) as daily_wtu,
        AVG(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.basket_size END) as avg_basket_size,
        SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN COALESCE(f.promo_expense, 0) ELSE 0 END) as daily_promo_expense,
        COUNT(DISTINCT CASE WHEN f.is_promotion = TRUE AND f.booking_state_simple = 'COMPLETED' THEN f.order_id END) as daily_promo_orders,
        COUNT(DISTINCT f.scribe_session_id) as daily_sessions,
        COUNT(DISTINCT f.merchant_id) as daily_active_merchants
    FROM ocd_adw.f_food_metrics f
    WHERE f.country_id = 1 
      AND f.city_id = 13  -- Penang
      AND f.date_id >= {dates['this_week_start']} 
      AND f.date_id <= {dates['this_week_end']}
      AND f.business_type = 0
    GROUP BY f.date_id
),
same_week_last_year_data AS (
    SELECT 
        f.date_id,
        CAST(date_format(from_iso8601_date(CAST(f.date_id AS VARCHAR)), '%Y%m%d') AS INT) AS formatted_date,
        COUNT(DISTINCT f.order_id) as daily_orders,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END) as daily_completed_orders,
        SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN COALESCE(f.gross_merchandise_value, 0) ELSE 0 END) as daily_gmv,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.passenger_id END) as daily_wtu,
        AVG(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.basket_size END) as avg_basket_size,
        SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN COALESCE(f.promo_expense, 0) ELSE 0 END) as daily_promo_expense,
        COUNT(DISTINCT CASE WHEN f.is_promotion = TRUE AND f.booking_state_simple = 'COMPLETED' THEN f.order_id END) as daily_promo_orders,
        COUNT(DISTINCT f.scribe_session_id) as daily_sessions,
        COUNT(DISTINCT f.merchant_id) as daily_active_merchants
    FROM ocd_adw.f_food_metrics f
    WHERE f.country_id = 1 
      AND f.city_id = 13  -- Penang
      AND f.date_id >= {dates['same_week_last_year_start']} 
      AND f.date_id <= {dates['same_week_last_year_end']}
      AND f.business_type = 0
    GROUP BY f.date_id
)
SELECT 
    'This Week' as period,
    tw.formatted_date as date_id,
    tw.daily_orders,
    tw.daily_completed_orders,
    tw.daily_gmv,
    tw.daily_wtu,
    tw.avg_basket_size,
    tw.daily_promo_expense,
    tw.daily_promo_orders,
    tw.daily_sessions,
    tw.daily_active_merchants,
    CASE 
        WHEN tw.daily_orders > 0 
        THEN ROUND(100.0 * tw.daily_promo_orders / tw.daily_completed_orders, 2)
        ELSE 0 
    END as promo_penetration_pct,
    CASE 
        WHEN tw.daily_sessions > 0 
        THEN ROUND(CAST(tw.daily_completed_orders AS DOUBLE) / CAST(tw.daily_sessions AS DOUBLE), 3)
        ELSE 0 
    END as cops
FROM this_week_data tw

UNION ALL

SELECT 
    'Same Week Last Year' as period,
    ly.formatted_date as date_id,
    ly.daily_orders,
    ly.daily_completed_orders,
    ly.daily_gmv,
    ly.daily_wtu,
    ly.avg_basket_size,
    ly.daily_promo_expense,
    ly.daily_promo_orders,
    ly.daily_sessions,
    ly.daily_active_merchants,
    CASE 
        WHEN ly.daily_orders > 0 
        THEN ROUND(100.0 * ly.daily_promo_orders / ly.daily_completed_orders, 2)
        ELSE 0 
    END as promo_penetration_pct,
    CASE 
        WHEN ly.daily_sessions > 0 
        THEN ROUND(CAST(ly.daily_completed_orders AS DOUBLE) / CAST(ly.daily_sessions AS DOUBLE), 3)
        ELSE 0 
    END as cops
FROM same_week_last_year_data ly

ORDER BY period, date_id;
"""

if __name__ == '__main__':
    dates = get_week_dates()
    query = generate_penang_daily_query(dates)
    
    print("=" * 80)
    print("PENANG DAILY TREND ANALYSIS QUERY")
    print("=" * 80)
    print(f"This Week: {dates['this_week_start']} to {dates['this_week_end']}")
    print(f"Same Week Last Year: {dates['same_week_last_year_start']} to {dates['same_week_last_year_end']}")
    print("\n" + "=" * 80)
    print(query)
    
    # Save query to file
    with open('penang_daily_trend_query.sql', 'w', encoding='utf-8') as f:
        f.write(query)
    
    print("\n✅ Query saved to: penang_daily_trend_query.sql")
    print("\n📊 Next step: Execute this query via MCP Hubble tool to get the data")

