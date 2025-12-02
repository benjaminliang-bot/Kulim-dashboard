"""
Generate Weekly Report Queries with New Pax Calculation
Includes queries for OC Overall and Top 5 Cities with New Pax metrics
"""

import sys
from datetime import datetime, timedelta
from calendar import monthrange

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_week_dates():
    """Get date ranges for last 7 days (current_date -1 to -8), same period last month, and same period last year, plus month ranges for MTM"""
    today = datetime.now()
    
    # Calculate period: current_date -1 to -8 (last 7 days)
    # Period end = yesterday (current_date - 1)
    # Period start = 8 days ago (current_date - 8)
    period_end = today - timedelta(days=1)  # Yesterday
    period_start = today - timedelta(days=8)  # 8 days ago (7 days total: -8 to -1)
    
    # Calculate same period last month (MoM - same dates, previous month)
    def subtract_month(date):
        """Subtract one month from a date, handling edge cases"""
        if date.month == 1:
            prev_month = 12
            prev_year = date.year - 1
        else:
            prev_month = date.month - 1
            prev_year = date.year
        
        # Handle month-end edge cases (e.g., Jan 31 -> Feb 28/29)
        last_day = monthrange(prev_year, prev_month)[1]
        day = min(date.day, last_day)
        
        return date.replace(year=prev_year, month=prev_month, day=day)
    
    same_period_last_month_start = subtract_month(period_start)
    same_period_last_month_end = subtract_month(period_end)
    
    # Calculate same period last year (YoY - same dates, previous year)
    same_period_last_year_start = period_start.replace(year=period_start.year - 1)
    same_period_last_year_end = period_end.replace(year=period_end.year - 1)
    
    # Calculate month ranges for MTM (Monthly Transacting Merchant)
    # Current month (month containing period_end, i.e., yesterday)
    current_month_start = period_end.replace(day=1)
    days_in_current_month = monthrange(current_month_start.year, current_month_start.month)[1]
    current_month_end = current_month_start.replace(day=days_in_current_month)
    
    # Last month (same month last year for YoY comparison)
    if current_month_start.month == 1:
        last_month_start = current_month_start.replace(year=current_month_start.year - 1, month=12)
    else:
        last_month_start = current_month_start.replace(month=current_month_start.month - 1)
    days_in_last_month = monthrange(last_month_start.year, last_month_start.month)[1]
    last_month_end = last_month_start.replace(day=days_in_last_month)
    
    # Same month last year
    same_month_last_year_start = current_month_start.replace(year=current_month_start.year - 1)
    days_in_same_month_last_year = monthrange(same_month_last_year_start.year, same_month_last_year_start.month)[1]
    same_month_last_year_end = same_month_last_year_start.replace(day=days_in_same_month_last_year)
    
    # Format as YYYYMMDD
    def format_date(d):
        return d.strftime('%Y%m%d')
    
    return {
        'this_week_start': format_date(period_start),  # Last 7 days (current_date -8)
        'this_week_end': format_date(period_end),  # Last 7 days (current_date -1)
        'same_week_last_month_start': format_date(same_period_last_month_start),
        'same_week_last_month_end': format_date(same_period_last_month_end),
        'same_week_last_year_start': format_date(same_period_last_year_start),
        'same_week_last_year_end': format_date(same_period_last_year_end),
        'current_month_start': format_date(current_month_start),
        'current_month_end': format_date(current_month_end),
        'last_month_start': format_date(last_month_start),
        'last_month_end': format_date(last_month_end),
        'same_month_last_year_start': format_date(same_month_last_year_start),
        'same_month_last_year_end': format_date(same_month_last_year_end)
    }

def generate_new_pax_subquery(week_start, week_end, city_filter=""):
    """
    Generate New Pax subquery
    Definition: Unique passenger_id where last transaction was more than a year ago OR first order was within the week
    """
    if city_filter:
        city_condition = f"AND city_id = {city_filter}"
    else:
        city_condition = "AND city_id != 1"
    
    return f"""
    -- New Pax calculation for week {week_start} to {week_end}
    (
        SELECT COUNT(DISTINCT new_pax.passenger_id) as new_pax_count
        FROM (
            SELECT DISTINCT f.passenger_id
            FROM ocd_adw.f_food_metrics f
            WHERE f.country_id = 1 
              {city_condition}
              AND f.date_id >= {week_start} 
              AND f.date_id <= {week_end}
              AND f.business_type = 0
              AND f.booking_state_simple = 'COMPLETED'
              AND (
                  -- First order was within this week
                  f.passenger_id IN (
                      SELECT passenger_id
                      FROM (
                          SELECT 
                              passenger_id,
                              MIN(date_id) as first_order_date
                          FROM ocd_adw.f_food_metrics
                          WHERE country_id = 1
                            {city_condition}
                            AND business_type = 0
                            AND booking_state_simple = 'COMPLETED'
                          GROUP BY passenger_id
                      ) first_orders
                      WHERE first_order_date >= {week_start}
                        AND first_order_date <= {week_end}
                  )
                  OR
                  -- Last transaction before this week was more than a year ago
                  f.passenger_id IN (
                      SELECT passenger_id
                      FROM (
                          SELECT 
                              passenger_id,
                              MAX(date_id) as last_order_date
                          FROM ocd_adw.f_food_metrics
                          WHERE country_id = 1
                            {city_condition}
                            AND business_type = 0
                            AND booking_state_simple = 'COMPLETED'
                            AND date_id < {week_start}
                          GROUP BY passenger_id
                      ) last_orders
                      WHERE last_order_date < {week_start} - 36500  -- More than 365 days ago
                        AND passenger_id NOT IN (
                            -- Exclude passengers who ordered in the last year (before this week)
                            SELECT DISTINCT passenger_id
                            FROM ocd_adw.f_food_metrics
                            WHERE country_id = 1
                              {city_condition}
                              AND business_type = 0
                              AND booking_state_simple = 'COMPLETED'
                              AND date_id >= {week_start} - 36500
                              AND date_id < {week_start}
                        )
                  )
              )
        ) new_pax
    )"""

def generate_oc_query_with_new_pax(dates):
    """Generate OC Cities overall query with New Pax"""
    return f"""
-- OC CITIES OVERALL with New Pax, MTM, and Earning per MEX
WITH this_week AS (
    SELECT 
        COUNT(DISTINCT f.order_id) as orders,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END) as completed_orders,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.passenger_id END) as unique_eaters,
        SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.gross_merchandise_value ELSE 0 END) as gmv,
        AVG(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.basket_size END) as avg_basket,
        SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.promo_expense ELSE 0 END) as promo_expense,
        COUNT(DISTINCT CASE WHEN f.is_promotion = TRUE THEN f.order_id END) as promo_orders,
        ROUND(100.0 * COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END) / 
              NULLIF(COUNT(DISTINCT f.order_id), 0), 2) as completion_rate
    FROM ocd_adw.f_food_metrics f
    WHERE f.country_id = 1 
      AND f.city_id != 1
      AND f.date_id >= {dates['this_week_start']} AND f.date_id <= {dates['this_week_end']}
      AND f.business_type = 0
),
-- MTM (Monthly Transacting Merchant) for current month
mtm_current_month AS (
    SELECT 
        COUNT(DISTINCT f.merchant_id) as mtm_count
    FROM ocd_adw.f_food_metrics f
    WHERE f.country_id = 1 
      AND f.city_id != 1
      AND f.date_id >= {dates['current_month_start']} AND f.date_id <= {dates['current_month_end']}
      AND f.business_type = 0
      AND f.booking_state_simple = 'COMPLETED'
      AND f.merchant_id IS NOT NULL
),
-- Median MEX Earnings for current month (median of basket_size - commission_from_merchant per order)
median_mex_earnings_current_month AS (
    SELECT 
        APPROX_PERCENTILE(
            CASE 
                WHEN f.booking_state_simple = 'COMPLETED' 
                THEN COALESCE(f.basket_size, 0) - COALESCE(f.commission_from_merchant, 0)
                ELSE NULL
            END,
            0.5
        ) as median_earnings
    FROM ocd_adw.f_food_metrics f
    WHERE f.country_id = 1 
      AND f.city_id != 1
      AND f.date_id >= {dates['current_month_start']} AND f.date_id <= {dates['current_month_end']}
      AND f.business_type = 0
      AND f.booking_state_simple = 'COMPLETED'
      AND f.merchant_id IS NOT NULL
      AND f.basket_size IS NOT NULL
),
-- MTM for last month
mtm_last_month AS (
    SELECT 
        COUNT(DISTINCT f.merchant_id) as mtm_count
    FROM ocd_adw.f_food_metrics f
    WHERE f.country_id = 1 
      AND f.city_id != 1
      AND f.date_id >= {dates['last_month_start']} AND f.date_id <= {dates['last_month_end']}
      AND f.business_type = 0
      AND f.booking_state_simple = 'COMPLETED'
      AND f.merchant_id IS NOT NULL
),
-- Median MEX Earnings for last month
median_mex_earnings_last_month AS (
    SELECT 
        APPROX_PERCENTILE(
            CASE 
                WHEN f.booking_state_simple = 'COMPLETED' 
                THEN COALESCE(f.basket_size, 0) - COALESCE(f.commission_from_merchant, 0)
                ELSE NULL
            END,
            0.5
        ) as median_earnings
    FROM ocd_adw.f_food_metrics f
    WHERE f.country_id = 1 
      AND f.city_id != 1
      AND f.date_id >= {dates['last_month_start']} AND f.date_id <= {dates['last_month_end']}
      AND f.business_type = 0
      AND f.booking_state_simple = 'COMPLETED'
      AND f.merchant_id IS NOT NULL
      AND f.basket_size IS NOT NULL
),
-- MTM for same month last year
mtm_same_month_last_year AS (
    SELECT 
        COUNT(DISTINCT f.merchant_id) as mtm_count
    FROM ocd_adw.f_food_metrics f
    WHERE f.country_id = 1 
      AND f.city_id != 1
      AND f.date_id >= {dates['same_month_last_year_start']} AND f.date_id <= {dates['same_month_last_year_end']}
      AND f.business_type = 0
      AND f.booking_state_simple = 'COMPLETED'
      AND f.merchant_id IS NOT NULL
),
-- Median MEX Earnings for same month last year
median_mex_earnings_same_month_last_year AS (
    SELECT 
        APPROX_PERCENTILE(
            CASE 
                WHEN f.booking_state_simple = 'COMPLETED' 
                THEN COALESCE(f.basket_size, 0) - COALESCE(f.commission_from_merchant, 0)
                ELSE NULL
            END,
            0.5
        ) as median_earnings
    FROM ocd_adw.f_food_metrics f
    WHERE f.country_id = 1 
      AND f.city_id != 1
      AND f.date_id >= {dates['same_month_last_year_start']} AND f.date_id <= {dates['same_month_last_year_end']}
      AND f.business_type = 0
      AND f.booking_state_simple = 'COMPLETED'
      AND f.merchant_id IS NOT NULL
      AND f.basket_size IS NOT NULL
),
same_week_last_month AS (
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
      AND f.date_id >= {dates['same_week_last_month_start']} AND f.date_id <= {dates['same_week_last_month_end']}
      AND f.business_type = 0
),
same_week_last_year AS (
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
      AND f.date_id >= {dates['same_week_last_year_start']} AND f.date_id <= {dates['same_week_last_year_end']}
      AND f.business_type = 0
),
-- Sessions calculation using ocd_adw.agg_food_cops_metrics (high intent sessions = preorder_sessions)
sessions_this_week AS (
    SELECT 
        CAST(SUM(preorder_sessions) AS DOUBLE) as sessions_value
    FROM ocd_adw.agg_food_cops_metrics
    WHERE country_id = 1 
      AND city_id != 1
      AND date_id >= {dates['this_week_start']} AND date_id <= {dates['this_week_end']}
      AND business = 'food'
),
sessions_same_week_last_month AS (
    SELECT 
        CAST(SUM(preorder_sessions) AS DOUBLE) as sessions_value
    FROM ocd_adw.agg_food_cops_metrics
    WHERE country_id = 1 
      AND city_id != 1
      AND date_id >= {dates['same_week_last_month_start']} AND date_id <= {dates['same_week_last_month_end']}
      AND business = 'food'
),
sessions_same_week_last_year AS (
    SELECT 
        CAST(SUM(preorder_sessions) AS DOUBLE) as sessions_value
    FROM ocd_adw.agg_food_cops_metrics
    WHERE country_id = 1 
      AND city_id != 1
      AND date_id >= {dates['same_week_last_year_start']} AND date_id <= {dates['same_week_last_year_end']}
      AND business = 'food'
),
-- COPS calculation using ocd_adw.agg_food_cops_metrics (underlying table for midas_analytics.v_agg_food_cops_metrics)
cops_this_week AS (
    SELECT 
        CAST(SUM(completed_orders) AS DOUBLE) / CAST(SUM(preorder_sessions) AS DOUBLE) as cops_value
    FROM ocd_adw.agg_food_cops_metrics
    WHERE country_id = 1 
      AND city_id != 1
      AND date_id >= {dates['this_week_start']} AND date_id <= {dates['this_week_end']}
      AND business = 'food'
),
cops_same_week_last_month AS (
    SELECT 
        CAST(SUM(completed_orders) AS DOUBLE) / CAST(SUM(preorder_sessions) AS DOUBLE) as cops_value
    FROM ocd_adw.agg_food_cops_metrics
    WHERE country_id = 1 
      AND city_id != 1
      AND date_id >= {dates['same_week_last_month_start']} AND date_id <= {dates['same_week_last_month_end']}
      AND business = 'food'
),
cops_same_week_last_year AS (
    SELECT 
        CAST(SUM(completed_orders) AS DOUBLE) / CAST(SUM(preorder_sessions) AS DOUBLE) as cops_value
    FROM ocd_adw.agg_food_cops_metrics
    WHERE country_id = 1 
      AND city_id != 1
      AND date_id >= {dates['same_week_last_year_start']} AND date_id <= {dates['same_week_last_year_end']}
      AND business = 'food'
),
new_pax_this_week AS {generate_new_pax_subquery(dates['this_week_start'], dates['this_week_end'])},
new_pax_last_month AS {generate_new_pax_subquery(dates['same_week_last_month_start'], dates['same_week_last_month_end'])},
new_pax_last_year AS {generate_new_pax_subquery(dates['same_week_last_year_start'], dates['same_week_last_year_end'])}
SELECT 
    t.orders as this_week_orders,
    m.orders as same_week_last_month_orders,
    y.orders as ytd_avg_orders,
    t.completed_orders as this_week_completed_orders,
    m.completed_orders as same_week_last_month_completed_orders,
    y.completed_orders as ytd_avg_completed_orders,
    t.completion_rate as this_week_completion_rate,
    m.completion_rate as same_week_last_month_completion_rate,
    y.completion_rate as ytd_avg_completion_rate,
    t.unique_eaters as this_week_eaters,
    m.unique_eaters as same_week_last_month_eaters,
    y.unique_eaters as ytd_avg_eaters,
    t.gmv as this_week_gmv,
    m.gmv as same_week_last_month_gmv,
    y.gmv as ytd_avg_gmv,
    t.avg_basket as this_week_basket,
    m.avg_basket as same_week_last_month_basket,
    y.avg_basket as ytd_avg_basket,
    t.promo_expense as this_week_promo_expense,
    m.promo_expense as same_week_last_month_promo_expense,
    y.promo_expense as ytd_avg_promo_expense,
    t.promo_orders as this_week_promo_orders,
    m.promo_orders as same_week_last_month_promo_orders,
    y.promo_orders as ytd_avg_promo_orders,
    ROUND(100.0 * t.promo_orders / NULLIF(t.orders, 0), 1) as this_week_promo_penetration,
    ROUND(100.0 * m.promo_orders / NULLIF(m.orders, 0), 1) as same_week_last_month_promo_penetration,
    ROUND(100.0 * y.promo_orders / NULLIF(y.orders, 0), 1) as ytd_avg_promo_penetration,
    COALESCE(sess_tw.sessions_value, 0) as this_week_sessions,
    COALESCE(sess_m.sessions_value, 0) as same_week_last_month_sessions,
    COALESCE(sess_y.sessions_value, 0) as ytd_avg_sessions,
    COALESCE(sess_tw.sessions_value, 0) as this_week_completed_sessions,
    COALESCE(sess_m.sessions_value, 0) as same_week_last_month_completed_sessions,
    COALESCE(sess_y.sessions_value, 0) as ytd_avg_completed_sessions,
    ROUND(1.0 * t.orders / NULLIF(COALESCE(sess_tw.sessions_value, 0), 0), 2) as this_week_orders_per_session,
    ROUND(1.0 * m.orders / NULLIF(COALESCE(sess_m.sessions_value, 0), 0), 2) as same_week_last_month_orders_per_session,
    ROUND(1.0 * y.orders / NULLIF(COALESCE(sess_y.sessions_value, 0), 0), 2) as ytd_avg_orders_per_session,
    ROUND(COALESCE(cops_tw.cops_value, 0), 2) as this_week_cops,
    ROUND(COALESCE(cops_m.cops_value, 0), 2) as same_week_last_month_cops,
    ROUND(COALESCE(cops_y.cops_value, 0), 2) as ytd_avg_cops,
    COALESCE(npw.new_pax_count, 0) as this_week_new_pax,
    COALESCE(npm.new_pax_count, 0) as same_week_last_month_new_pax,
    COALESCE(npy.new_pax_count, 0) as ytd_avg_new_pax,
    COALESCE(mtm_curr.mtm_count, 0) as current_month_mtm,
    COALESCE(mtm_last.mtm_count, 0) as last_month_mtm,
    COALESCE(mtm_yoy.mtm_count, 0) as same_month_last_year_mtm,
    ROUND(COALESCE(median_curr.median_earnings, 0), 2) as current_month_earning_per_mex,
    ROUND(COALESCE(median_last.median_earnings, 0), 2) as last_month_earning_per_mex,
    ROUND(COALESCE(median_yoy.median_earnings, 0), 2) as same_month_last_year_earning_per_mex
FROM this_week t
CROSS JOIN same_week_last_month m
CROSS JOIN same_week_last_year y
CROSS JOIN sessions_this_week sess_tw
CROSS JOIN sessions_same_week_last_month sess_m
CROSS JOIN sessions_same_week_last_year sess_y
CROSS JOIN cops_this_week cops_tw
CROSS JOIN cops_same_week_last_month cops_m
CROSS JOIN cops_same_week_last_year cops_y
CROSS JOIN new_pax_this_week npw
CROSS JOIN new_pax_last_month npm
CROSS JOIN new_pax_last_year npy
CROSS JOIN mtm_current_month mtm_curr
CROSS JOIN mtm_last_month mtm_last
CROSS JOIN mtm_same_month_last_year mtm_yoy
CROSS JOIN median_mex_earnings_current_month median_curr
CROSS JOIN median_mex_earnings_last_month median_last
CROSS JOIN median_mex_earnings_same_month_last_year median_yoy
"""

def generate_top_cities_query_with_new_pax(dates):
    """Generate Top 5 Cities query with New Pax, MTM, and Earning per MEX"""
    return f"""
-- TOP 5 CITIES BY GMV with New Pax, MTM, and Earning per MEX
WITH this_week_cities AS (
    SELECT 
        f.city_id,
        dc.city_name,
        COUNT(DISTINCT f.order_id) as orders,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END) as completed_orders,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.passenger_id END) as unique_eaters,
        SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.gross_merchandise_value ELSE 0 END) as gmv,
        AVG(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.basket_size END) as avg_basket,
        SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.promo_expense ELSE 0 END) as promo_expense,
        COUNT(DISTINCT CASE WHEN f.is_promotion = TRUE THEN f.order_id END) as promo_orders,
        ROUND(100.0 * COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END) / 
              NULLIF(COUNT(DISTINCT f.order_id), 0), 2) as completion_rate
    FROM ocd_adw.f_food_metrics f
    JOIN ocd_adw.d_city dc ON f.city_id = dc.city_id
    WHERE f.country_id = 1 
      AND f.city_id != 1
      AND f.date_id >= {dates['this_week_start']} AND f.date_id <= {dates['this_week_end']}
      AND f.business_type = 0
    GROUP BY f.city_id, dc.city_name
),
same_week_last_month_cities AS (
    SELECT 
        f.city_id,
        dc.city_name,
        COUNT(DISTINCT f.order_id) as orders,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END) as completed_orders,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.passenger_id END) as unique_eaters,
        SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.gross_merchandise_value ELSE 0 END) as gmv,
        AVG(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.basket_size END) as avg_basket,
        SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.promo_expense ELSE 0 END) as promo_expense,
        COUNT(DISTINCT CASE WHEN f.is_promotion = TRUE THEN f.order_id END) as promo_orders,
        ROUND(100.0 * COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END) / 
              NULLIF(COUNT(DISTINCT f.order_id), 0), 2) as completion_rate
    FROM ocd_adw.f_food_metrics f
    JOIN ocd_adw.d_city dc ON f.city_id = dc.city_id
    WHERE f.country_id = 1 
      AND f.city_id != 1
      AND f.date_id >= {dates['same_week_last_month_start']} AND f.date_id <= {dates['same_week_last_month_end']}
      AND f.business_type = 0
    GROUP BY f.city_id, dc.city_name
),
same_week_last_year_cities AS (
    SELECT 
        f.city_id,
        dc.city_name,
        COUNT(DISTINCT f.order_id) as orders,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END) as completed_orders,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.passenger_id END) as unique_eaters,
        SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.gross_merchandise_value ELSE 0 END) as gmv,
        AVG(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.basket_size END) as avg_basket,
        SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.promo_expense ELSE 0 END) as promo_expense,
        COUNT(DISTINCT CASE WHEN f.is_promotion = TRUE THEN f.order_id END) as promo_orders,
        ROUND(100.0 * COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END) / 
              NULLIF(COUNT(DISTINCT f.order_id), 0), 2) as completion_rate
    FROM ocd_adw.f_food_metrics f
    JOIN ocd_adw.d_city dc ON f.city_id = dc.city_id
    WHERE f.country_id = 1 
      AND f.city_id != 1
      AND f.date_id >= {dates['same_week_last_year_start']} AND f.date_id <= {dates['same_week_last_year_end']}
      AND f.business_type = 0
    GROUP BY f.city_id, dc.city_name
),
top_cities AS (
    SELECT city_id, city_name
    FROM this_week_cities
    ORDER BY gmv DESC
    LIMIT 5
),
-- New Pax per city for this week
new_pax_this_week_by_city AS (
    SELECT 
        f.city_id,
        COUNT(DISTINCT f.passenger_id) as new_pax_count
    FROM ocd_adw.f_food_metrics f
    WHERE f.country_id = 1 
      AND f.city_id != 1
      AND f.date_id >= {dates['this_week_start']} 
      AND f.date_id <= {dates['this_week_end']}
      AND f.business_type = 0
      AND f.booking_state_simple = 'COMPLETED'
      AND (
          -- First order in this city was within this week
          (f.passenger_id, f.city_id) IN (
              SELECT passenger_id, city_id
              FROM (
                  SELECT 
                      passenger_id,
                      city_id,
                      MIN(date_id) as first_order_date
                  FROM ocd_adw.f_food_metrics
                  WHERE country_id = 1
                    AND city_id != 1
                    AND business_type = 0
                    AND booking_state_simple = 'COMPLETED'
                  GROUP BY passenger_id, city_id
              ) first_orders
              WHERE first_order_date >= {dates['this_week_start']}
                AND first_order_date <= {dates['this_week_end']}
          )
          OR
          -- Last transaction in this city before this week was more than a year ago
          (f.passenger_id, f.city_id) IN (
              SELECT passenger_id, city_id
              FROM (
                  SELECT 
                      passenger_id,
                      city_id,
                      MAX(date_id) as last_order_date
                  FROM ocd_adw.f_food_metrics
                  WHERE country_id = 1
                    AND city_id != 1
                    AND business_type = 0
                    AND booking_state_simple = 'COMPLETED'
                    AND date_id < {dates['this_week_start']}
                  GROUP BY passenger_id, city_id
              ) last_orders
              WHERE last_order_date < {dates['this_week_start']} - 36500
                AND (passenger_id, city_id) NOT IN (
                    SELECT DISTINCT passenger_id, city_id
                    FROM ocd_adw.f_food_metrics
                    WHERE country_id = 1
                      AND city_id != 1
                      AND business_type = 0
                      AND booking_state_simple = 'COMPLETED'
                      AND date_id >= {dates['this_week_start']} - 36500
                      AND date_id < {dates['this_week_start']}
                )
          )
      )
    GROUP BY f.city_id
),
-- New Pax per city for same week last month
new_pax_last_month_by_city AS (
    SELECT 
        f.city_id,
        COUNT(DISTINCT f.passenger_id) as new_pax_count
    FROM ocd_adw.f_food_metrics f
    WHERE f.country_id = 1 
      AND f.city_id != 1
      AND f.date_id >= {dates['same_week_last_month_start']} 
      AND f.date_id <= {dates['same_week_last_month_end']}
      AND f.business_type = 0
      AND f.booking_state_simple = 'COMPLETED'
      AND (
          (f.passenger_id, f.city_id) IN (
              SELECT passenger_id, city_id
              FROM (
                  SELECT 
                      passenger_id,
                      city_id,
                      MIN(date_id) as first_order_date
                  FROM ocd_adw.f_food_metrics
                  WHERE country_id = 1
                    AND city_id != 1
                    AND business_type = 0
                    AND booking_state_simple = 'COMPLETED'
                  GROUP BY passenger_id, city_id
              ) first_orders
              WHERE first_order_date >= {dates['same_week_last_month_start']}
                AND first_order_date <= {dates['same_week_last_month_end']}
          )
          OR
          (f.passenger_id, f.city_id) IN (
              SELECT passenger_id, city_id
              FROM (
                  SELECT 
                      passenger_id,
                      city_id,
                      MAX(date_id) as last_order_date
                  FROM ocd_adw.f_food_metrics
                  WHERE country_id = 1
                    AND city_id != 1
                    AND business_type = 0
                    AND booking_state_simple = 'COMPLETED'
                    AND date_id < {dates['same_week_last_month_start']}
                  GROUP BY passenger_id, city_id
              ) last_orders
              WHERE last_order_date < {dates['same_week_last_month_start']} - 36500
                AND (passenger_id, city_id) NOT IN (
                    SELECT DISTINCT passenger_id, city_id
                    FROM ocd_adw.f_food_metrics
                    WHERE country_id = 1
                      AND city_id != 1
                      AND business_type = 0
                      AND booking_state_simple = 'COMPLETED'
                      AND date_id >= {dates['same_week_last_month_start']} - 36500
                      AND date_id < {dates['same_week_last_month_start']}
                )
          )
      )
    GROUP BY f.city_id
),
-- New Pax per city for same week last year
new_pax_last_year_by_city AS (
    SELECT 
        f.city_id,
        COUNT(DISTINCT f.passenger_id) as new_pax_count
    FROM ocd_adw.f_food_metrics f
    WHERE f.country_id = 1 
      AND f.city_id != 1
      AND f.date_id >= {dates['same_week_last_year_start']} 
      AND f.date_id <= {dates['same_week_last_year_end']}
      AND f.business_type = 0
      AND f.booking_state_simple = 'COMPLETED'
      AND (
          (f.passenger_id, f.city_id) IN (
              SELECT passenger_id, city_id
              FROM (
                  SELECT 
                      passenger_id,
                      city_id,
                      MIN(date_id) as first_order_date
                  FROM ocd_adw.f_food_metrics
                  WHERE country_id = 1
                    AND city_id != 1
                    AND business_type = 0
                    AND booking_state_simple = 'COMPLETED'
                  GROUP BY passenger_id, city_id
              ) first_orders
              WHERE first_order_date >= {dates['same_week_last_year_start']}
                AND first_order_date <= {dates['same_week_last_year_end']}
          )
          OR
          (f.passenger_id, f.city_id) IN (
              SELECT passenger_id, city_id
              FROM (
                  SELECT 
                      passenger_id,
                      city_id,
                      MAX(date_id) as last_order_date
                  FROM ocd_adw.f_food_metrics
                  WHERE country_id = 1
                    AND city_id != 1
                    AND business_type = 0
                    AND booking_state_simple = 'COMPLETED'
                    AND date_id < {dates['same_week_last_year_start']}
                  GROUP BY passenger_id, city_id
              ) last_orders
              WHERE last_order_date < {dates['same_week_last_year_start']} - 36500
                AND (passenger_id, city_id) NOT IN (
                    SELECT DISTINCT passenger_id, city_id
                    FROM ocd_adw.f_food_metrics
                    WHERE country_id = 1
                      AND city_id != 1
                      AND business_type = 0
                      AND booking_state_simple = 'COMPLETED'
                      AND date_id >= {dates['same_week_last_year_start']} - 36500
                      AND date_id < {dates['same_week_last_year_start']}
                )
          )
      )
    GROUP BY f.city_id
),
-- Sessions calculation per city using ocd_adw.agg_food_cops_metrics (high intent sessions = preorder_sessions)
sessions_this_week_by_city AS (
    SELECT 
        city_id,
        CAST(SUM(preorder_sessions) AS DOUBLE) as sessions_value
    FROM ocd_adw.agg_food_cops_metrics
    WHERE country_id = 1 
      AND city_id != 1
      AND date_id >= {dates['this_week_start']} AND date_id <= {dates['this_week_end']}
      AND business = 'food'
    GROUP BY city_id
),
sessions_same_week_last_month_by_city AS (
    SELECT 
        city_id,
        CAST(SUM(preorder_sessions) AS DOUBLE) as sessions_value
    FROM ocd_adw.agg_food_cops_metrics
    WHERE country_id = 1 
      AND city_id != 1
      AND date_id >= {dates['same_week_last_month_start']} AND date_id <= {dates['same_week_last_month_end']}
      AND business = 'food'
    GROUP BY city_id
),
sessions_same_week_last_year_by_city AS (
    SELECT 
        city_id,
        CAST(SUM(preorder_sessions) AS DOUBLE) as sessions_value
    FROM ocd_adw.agg_food_cops_metrics
    WHERE country_id = 1 
      AND city_id != 1
      AND date_id >= {dates['same_week_last_year_start']} AND date_id <= {dates['same_week_last_year_end']}
      AND business = 'food'
    GROUP BY city_id
),
-- COPS calculation per city using ocd_adw.agg_food_cops_metrics (underlying table for midas_analytics.v_agg_food_cops_metrics)
cops_this_week_by_city AS (
    SELECT 
        city_id,
        CAST(SUM(completed_orders) AS DOUBLE) / CAST(SUM(preorder_sessions) AS DOUBLE) as cops_value
    FROM ocd_adw.agg_food_cops_metrics
    WHERE country_id = 1 
      AND city_id != 1
      AND date_id >= {dates['this_week_start']} AND date_id <= {dates['this_week_end']}
      AND business = 'food'
    GROUP BY city_id
),
cops_same_week_last_month_by_city AS (
    SELECT 
        city_id,
        CAST(SUM(completed_orders) AS DOUBLE) / CAST(SUM(preorder_sessions) AS DOUBLE) as cops_value
    FROM ocd_adw.agg_food_cops_metrics
    WHERE country_id = 1 
      AND city_id != 1
      AND date_id >= {dates['same_week_last_month_start']} AND date_id <= {dates['same_week_last_month_end']}
      AND business = 'food'
    GROUP BY city_id
),
cops_same_week_last_year_by_city AS (
    SELECT 
        city_id,
        CAST(SUM(completed_orders) AS DOUBLE) / CAST(SUM(preorder_sessions) AS DOUBLE) as cops_value
    FROM ocd_adw.agg_food_cops_metrics
    WHERE country_id = 1 
      AND city_id != 1
      AND date_id >= {dates['same_week_last_year_start']} AND date_id <= {dates['same_week_last_year_end']}
      AND business = 'food'
    GROUP BY city_id
)
SELECT 
    tc.city_id,
    tc.city_name,
    t.orders as this_week_orders,
    m.orders as same_week_last_month_orders,
    y.orders as ytd_avg_orders,
    t.completed_orders as this_week_completed_orders,
    m.completed_orders as same_week_last_month_completed_orders,
    y.completed_orders as ytd_avg_completed_orders,
    t.completion_rate as this_week_completion_rate,
    m.completion_rate as same_week_last_month_completion_rate,
    y.completion_rate as ytd_avg_completion_rate,
    t.unique_eaters as this_week_eaters,
    m.unique_eaters as same_week_last_month_eaters,
    y.unique_eaters as ytd_avg_eaters,
    t.gmv as this_week_gmv,
    m.gmv as same_week_last_month_gmv,
    y.gmv as ytd_avg_gmv,
    t.avg_basket as this_week_basket,
    m.avg_basket as same_week_last_month_basket,
    y.avg_basket as ytd_avg_basket,
    t.promo_expense as this_week_promo_expense,
    m.promo_expense as same_week_last_month_promo_expense,
    y.promo_expense as ytd_avg_promo_expense,
    t.promo_orders as this_week_promo_orders,
    m.promo_orders as same_week_last_month_promo_orders,
    y.promo_orders as ytd_avg_promo_orders,
    ROUND(100.0 * t.promo_orders / NULLIF(t.orders, 0), 1) as this_week_promo_penetration,
    ROUND(100.0 * m.promo_orders / NULLIF(m.orders, 0), 1) as same_week_last_month_promo_penetration,
    ROUND(100.0 * y.promo_orders / NULLIF(y.orders, 0), 1) as ytd_avg_promo_penetration,
    COALESCE(sess_tw.sessions_value, 0) as this_week_sessions,
    COALESCE(sess_m.sessions_value, 0) as same_week_last_month_sessions,
    COALESCE(sess_y.sessions_value, 0) as ytd_avg_sessions,
    COALESCE(sess_tw.sessions_value, 0) as this_week_completed_sessions,
    COALESCE(sess_m.sessions_value, 0) as same_week_last_month_completed_sessions,
    COALESCE(sess_y.sessions_value, 0) as ytd_avg_completed_sessions,
    ROUND(1.0 * t.orders / NULLIF(COALESCE(sess_tw.sessions_value, 0), 0), 2) as this_week_orders_per_session,
    ROUND(1.0 * m.orders / NULLIF(COALESCE(sess_m.sessions_value, 0), 0), 2) as same_week_last_month_orders_per_session,
    ROUND(1.0 * y.orders / NULLIF(COALESCE(sess_y.sessions_value, 0), 0), 2) as ytd_avg_orders_per_session,
    ROUND(COALESCE(cops_tw.cops_value, 0), 2) as this_week_cops,
    ROUND(COALESCE(cops_m.cops_value, 0), 2) as same_week_last_month_cops,
    ROUND(COALESCE(cops_y.cops_value, 0), 2) as ytd_avg_cops,
    COALESCE(npw.new_pax_count, 0) as this_week_new_pax,
    COALESCE(npm.new_pax_count, 0) as same_week_last_month_new_pax,
    COALESCE(npy.new_pax_count, 0) as ytd_avg_new_pax,
    COALESCE(mtm_curr.mtm_count, 0) as current_month_mtm,
    COALESCE(mtm_last.mtm_count, 0) as last_month_mtm,
    COALESCE(mtm_yoy.mtm_count, 0) as same_month_last_year_mtm,
    ROUND(COALESCE(median_curr.median_earnings, 0), 2) as current_month_earning_per_mex,
    ROUND(COALESCE(median_last.median_earnings, 0), 2) as last_month_earning_per_mex,
    ROUND(COALESCE(median_yoy.median_earnings, 0), 2) as same_month_last_year_earning_per_mex
FROM top_cities tc
LEFT JOIN this_week_cities t ON tc.city_id = t.city_id
LEFT JOIN same_week_last_month_cities m ON tc.city_id = m.city_id
LEFT JOIN same_week_last_year_cities y ON tc.city_id = y.city_id
LEFT JOIN sessions_this_week_by_city sess_tw ON tc.city_id = sess_tw.city_id
LEFT JOIN sessions_same_week_last_month_by_city sess_m ON tc.city_id = sess_m.city_id
LEFT JOIN sessions_same_week_last_year_by_city sess_y ON tc.city_id = sess_y.city_id
LEFT JOIN new_pax_this_week_by_city npw ON tc.city_id = npw.city_id
LEFT JOIN new_pax_last_month_by_city npm ON tc.city_id = npm.city_id
LEFT JOIN new_pax_last_year_by_city npy ON tc.city_id = npy.city_id
LEFT JOIN cops_this_week_by_city cops_tw ON tc.city_id = cops_tw.city_id
LEFT JOIN cops_same_week_last_month_by_city cops_m ON tc.city_id = cops_m.city_id
LEFT JOIN cops_same_week_last_year_by_city cops_y ON tc.city_id = cops_y.city_id
LEFT JOIN (
    SELECT 
        f.city_id,
        COUNT(DISTINCT f.merchant_id) as mtm_count
    FROM ocd_adw.f_food_metrics f
    WHERE f.country_id = 1 
      AND f.city_id != 1
      AND f.date_id >= {dates['current_month_start']} AND f.date_id <= {dates['current_month_end']}
      AND f.business_type = 0
      AND f.booking_state_simple = 'COMPLETED'
      AND f.merchant_id IS NOT NULL
    GROUP BY f.city_id
) mtm_curr ON tc.city_id = mtm_curr.city_id
LEFT JOIN (
    SELECT 
        f.city_id,
        COUNT(DISTINCT f.merchant_id) as mtm_count
    FROM ocd_adw.f_food_metrics f
    WHERE f.country_id = 1 
      AND f.city_id != 1
      AND f.date_id >= {dates['last_month_start']} AND f.date_id <= {dates['last_month_end']}
      AND f.business_type = 0
      AND f.booking_state_simple = 'COMPLETED'
      AND f.merchant_id IS NOT NULL
    GROUP BY f.city_id
) mtm_last ON tc.city_id = mtm_last.city_id
LEFT JOIN (
    SELECT 
        f.city_id,
        COUNT(DISTINCT f.merchant_id) as mtm_count
    FROM ocd_adw.f_food_metrics f
    WHERE f.country_id = 1 
      AND f.city_id != 1
      AND f.date_id >= {dates['same_month_last_year_start']} AND f.date_id <= {dates['same_month_last_year_end']}
      AND f.business_type = 0
      AND f.booking_state_simple = 'COMPLETED'
      AND f.merchant_id IS NOT NULL
    GROUP BY f.city_id
) mtm_yoy ON tc.city_id = mtm_yoy.city_id
LEFT JOIN (
    SELECT 
        f.city_id,
        APPROX_PERCENTILE(
            CASE 
                WHEN f.booking_state_simple = 'COMPLETED' 
                THEN COALESCE(f.basket_size, 0) - COALESCE(f.commission_from_merchant, 0)
                ELSE NULL
            END,
            0.5
        ) as median_earnings
    FROM ocd_adw.f_food_metrics f
    WHERE f.country_id = 1 
      AND f.city_id != 1
      AND f.date_id >= {dates['current_month_start']} AND f.date_id <= {dates['current_month_end']}
      AND f.business_type = 0
      AND f.booking_state_simple = 'COMPLETED'
      AND f.merchant_id IS NOT NULL
      AND f.basket_size IS NOT NULL
    GROUP BY f.city_id
) median_curr ON tc.city_id = median_curr.city_id
LEFT JOIN (
    SELECT 
        f.city_id,
        APPROX_PERCENTILE(
            CASE 
                WHEN f.booking_state_simple = 'COMPLETED' 
                THEN COALESCE(f.basket_size, 0) - COALESCE(f.commission_from_merchant, 0)
                ELSE NULL
            END,
            0.5
        ) as median_earnings
    FROM ocd_adw.f_food_metrics f
    WHERE f.country_id = 1 
      AND f.city_id != 1
      AND f.date_id >= {dates['last_month_start']} AND f.date_id <= {dates['last_month_end']}
      AND f.business_type = 0
      AND f.booking_state_simple = 'COMPLETED'
      AND f.merchant_id IS NOT NULL
      AND f.basket_size IS NOT NULL
    GROUP BY f.city_id
) median_last ON tc.city_id = median_last.city_id
LEFT JOIN (
    SELECT 
        f.city_id,
        APPROX_PERCENTILE(
            CASE 
                WHEN f.booking_state_simple = 'COMPLETED' 
                THEN COALESCE(f.basket_size, 0) - COALESCE(f.commission_from_merchant, 0)
                ELSE NULL
            END,
            0.5
        ) as median_earnings
    FROM ocd_adw.f_food_metrics f
    WHERE f.country_id = 1 
      AND f.city_id != 1
      AND f.date_id >= {dates['same_month_last_year_start']} AND f.date_id <= {dates['same_month_last_year_end']}
      AND f.business_type = 0
      AND f.booking_state_simple = 'COMPLETED'
      AND f.merchant_id IS NOT NULL
      AND f.basket_size IS NOT NULL
    GROUP BY f.city_id
) median_yoy ON tc.city_id = median_yoy.city_id
ORDER BY t.gmv DESC
"""

if __name__ == '__main__':
    dates = get_week_dates()
    print("=" * 60)
    print("Weekly Report Queries with New Pax")
    print("=" * 60)
    print(f"\n📅 Date Ranges:")
    print(f"   This Week: {dates['this_week_start']} - {dates['this_week_end']}")
    print(f"   Same Week Last Month: {dates['same_week_last_month_start']} - {dates['same_week_last_month_end']}")
    print(f"   Same Week Last Year: {dates['same_week_last_year_start']} - {dates['same_week_last_year_end']}")
    
    print("\n" + "=" * 60)
    print("OC Query:")
    print("=" * 60)
    print(generate_oc_query_with_new_pax(dates))
    
    print("\n" + "=" * 60)
    print("Top Cities Query:")
    print("=" * 60)
    print(generate_top_cities_query_with_new_pax(dates))

