"""
Generate Weekly Report Queries with Updated Comparison Logic
- This Week vs Same Week Last Month
- This Week vs YTD Average of Same Week
"""

import sys
from datetime import datetime, timedelta

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_week_dates():
    """Get date ranges for this week, same week last month, and calculate YTD average"""
    today = datetime.now()
    
    # Calculate this week (Monday to Sunday)
    days_since_monday = today.weekday()
    this_week_start = today - timedelta(days=days_since_monday)
    this_week_end = this_week_start + timedelta(days=6)
    
    # Calculate same week last month
    # Go back approximately 4 weeks (28 days) to get same week last month
    same_week_last_month_start = this_week_start - timedelta(days=28)
    same_week_last_month_end = same_week_last_month_start + timedelta(days=6)
    
    # For YTD average, we need to get all weeks from start of year up to (but not including) this week
    # Get the week number of the year
    year_start = datetime(this_week_start.year, 1, 1)
    days_from_year_start = (this_week_start - year_start).days
    week_number = (days_from_year_start // 7) + 1
    
    # YTD: All weeks from week 1 to (week_number - 1) of the same year
    ytd_start = datetime(this_week_start.year, 1, 1)
    # Find first Monday of the year
    first_monday = ytd_start
    while first_monday.weekday() != 0:
        first_monday += timedelta(days=1)
    
    # Format dates
    def format_date(d):
        return d.strftime('%Y%m%d')
    
    return (
        format_date(this_week_start),
        format_date(this_week_end),
        format_date(same_week_last_month_start),
        format_date(same_week_last_month_end),
        this_week_start.year,
        week_number
    )

def generate_oc_cities_query(this_week_start, this_week_end, last_month_start, last_month_end, year, week_num):
    """Generate OC Cities query with same week last month and YTD average"""
    
    query = f"""
-- OC CITIES OVERALL (This Week vs Same Week Last Month & YTD Average)
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
      AND f.date_id >= {last_month_start} AND f.date_id <= {last_month_end}
      AND f.business_type = 0
),
ytd_weeks AS (
    -- Get all weeks from start of year up to (but not including) this week
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
              NULLIF(COUNT(DISTINCT f.order_id), 0), 2) as completion_rate,
        COUNT(DISTINCT DATE_TRUNC('week', CAST(f.date_id AS VARCHAR)::DATE)) as week_count
    FROM ocd_adw.f_food_metrics f
    WHERE f.country_id = 1 
      AND f.city_id != 1
      AND f.date_id >= {year}0101 
      AND f.date_id < {this_week_start}
      AND f.business_type = 0
)
SELECT 
    t.orders as this_week_orders,
    l.orders as same_week_last_month_orders,
    y.orders / NULLIF(y.week_count, 0) as ytd_avg_orders,
    t.completed_orders as this_week_completed_orders,
    l.completed_orders as same_week_last_month_completed_orders,
    y.completed_orders / NULLIF(y.week_count, 0) as ytd_avg_completed_orders,
    t.completion_rate as this_week_completion_rate,
    l.completion_rate as same_week_last_month_completion_rate,
    y.completion_rate as ytd_avg_completion_rate,
    t.unique_eaters as this_week_eaters,
    l.unique_eaters as same_week_last_month_eaters,
    y.unique_eaters / NULLIF(y.week_count, 0) as ytd_avg_eaters,
    t.gmv as this_week_gmv,
    l.gmv as same_week_last_month_gmv,
    y.gmv / NULLIF(y.week_count, 0) as ytd_avg_gmv,
    t.avg_basket as this_week_basket,
    l.avg_basket as same_week_last_month_basket,
    y.avg_basket as ytd_avg_basket,
    t.promo_expense as this_week_promo_expense,
    l.promo_expense as same_week_last_month_promo_expense,
    y.promo_expense / NULLIF(y.week_count, 0) as ytd_avg_promo_expense,
    t.promo_orders as this_week_promo_orders,
    l.promo_orders as same_week_last_month_promo_orders,
    y.promo_orders / NULLIF(y.week_count, 0) as ytd_avg_promo_orders,
    ROUND(100.0 * t.promo_orders / NULLIF(t.orders, 0), 1) as this_week_promo_penetration,
    ROUND(100.0 * l.promo_orders / NULLIF(l.orders, 0), 1) as same_week_last_month_promo_penetration,
    ROUND(100.0 * (y.promo_orders / NULLIF(y.week_count, 0)) / NULLIF((y.orders / NULLIF(y.week_count, 0)), 0), 1) as ytd_avg_promo_penetration,
    t.unique_sessions as this_week_sessions,
    l.unique_sessions as same_week_last_month_sessions,
    y.unique_sessions / NULLIF(y.week_count, 0) as ytd_avg_sessions,
    t.completed_sessions as this_week_completed_sessions,
    l.completed_sessions as same_week_last_month_completed_sessions,
    y.completed_sessions / NULLIF(y.week_count, 0) as ytd_avg_completed_sessions,
    ROUND(1.0 * t.orders / NULLIF(t.unique_sessions, 0), 2) as this_week_orders_per_session,
    ROUND(1.0 * l.orders / NULLIF(l.unique_sessions, 0), 2) as same_week_last_month_orders_per_session,
    ROUND(1.0 * (y.orders / NULLIF(y.week_count, 0)) / NULLIF((y.unique_sessions / NULLIF(y.week_count, 0)), 0), 2) as ytd_avg_orders_per_session,
    ROUND(1.0 * t.completed_orders / NULLIF(t.completed_sessions, 0), 2) as this_week_cops,
    ROUND(1.0 * l.completed_orders / NULLIF(l.completed_sessions, 0), 2) as same_week_last_month_cops,
    ROUND(1.0 * (y.completed_orders / NULLIF(y.week_count, 0)) / NULLIF((y.completed_sessions / NULLIF(y.week_count, 0)), 0), 2) as ytd_avg_cops
FROM this_week t
CROSS JOIN same_week_last_month l
CROSS JOIN ytd_weeks y
"""
    return query

if __name__ == '__main__':
    this_week_start, this_week_end, last_month_start, last_month_end, year, week_num = get_week_dates()
    
    print("=" * 60)
    print("Weekly Report Queries - Updated Comparison Logic")
    print("=" * 60)
    print(f"\nThis Week: {this_week_start} - {this_week_end}")
    print(f"Same Week Last Month: {last_month_start} - {last_month_end}")
    print(f"YTD Average: All weeks from {year}0101 to {this_week_start} (exclusive)")
    print(f"\nWeek Number: {week_num}")
    print("\n" + "=" * 60)
    
    # Generate OC Cities query
    oc_query = generate_oc_cities_query(this_week_start, this_week_end, last_month_start, last_month_end, year, week_num)
    print("\nOC CITIES QUERY:")
    print(oc_query)


