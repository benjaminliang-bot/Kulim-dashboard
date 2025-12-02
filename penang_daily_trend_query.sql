
-- Penang Daily GMV & Orders Trend Analysis
-- Last Completed Week vs Same Week Last Year

WITH this_week_data AS (
    SELECT 
        f.date_id,
        f.date_id AS formatted_date,
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
      AND f.date_id >= 20251110 
      AND f.date_id <= 20251116
      AND f.business_type = 0
    GROUP BY f.date_id
),
same_week_last_year_data AS (
    SELECT 
        f.date_id,
        f.date_id AS formatted_date,
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
      AND f.date_id >= 20241110 
      AND f.date_id <= 20241116
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
