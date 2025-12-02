-- Weekly Report Queries for OC Cities and Penang
-- These queries should be executed via MCP tools in Cursor

-- ============================================================
-- 1. OC CITIES OVERALL (This Week vs Last Week)
-- ============================================================
-- Replace {THIS_WEEK_START}, {THIS_WEEK_END}, {LAST_WEEK_START}, {LAST_WEEK_END} with actual dates

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
      AND f.date_id >= {THIS_WEEK_START} AND f.date_id <= {THIS_WEEK_END}
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
      AND f.date_id >= {LAST_WEEK_START} AND f.date_id <= {LAST_WEEK_END}
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
CROSS JOIN last_week l;

-- ============================================================
-- 2. TOP 5 CITIES BY GMV (OC) - This Week vs Last Week
-- ============================================================

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
      AND f.date_id >= {THIS_WEEK_START} AND f.date_id <= {THIS_WEEK_END}
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
      AND f.date_id >= {LAST_WEEK_START} AND f.date_id <= {LAST_WEEK_END}
      AND f.business_type = 0
    GROUP BY f.city_id, dc.city_name
)
SELECT 
    tw.city_name,
    tw.city_id,
    lw.gmv as last_week_gmv,
    tw.gmv as this_week_gmv,
    tw.gmv - lw.gmv as gmv_delta,
    ROUND((tw.gmv - lw.gmv) / NULLIF(lw.gmv, 0) * 100, 2) as gmv_growth_pct,
    lw.orders as last_week_orders,
    tw.orders as this_week_orders,
    lw.unique_eaters as last_week_eaters,
    tw.unique_eaters as this_week_eaters
FROM this_week_cities tw
LEFT JOIN last_week_cities lw ON tw.city_id = lw.city_id
ORDER BY tw.gmv DESC
LIMIT 5;

-- ============================================================
-- 3. DAILY METRICS (This Week) - OC Cities
-- ============================================================

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
  AND f.date_id >= {THIS_WEEK_START} AND f.date_id <= {THIS_WEEK_END}
  AND f.business_type = 0
GROUP BY CAST(date_format(from_iso8601_date(CAST(f.date_id AS VARCHAR)), '%Y%m%d') AS INT)
ORDER BY date_id;

-- ============================================================
-- 4. PENANG (This Week vs Last Week)
-- ============================================================

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
      AND f.date_id >= {THIS_WEEK_START} AND f.date_id <= {THIS_WEEK_END}
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
      AND f.date_id >= {LAST_WEEK_START} AND f.date_id <= {LAST_WEEK_END}
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
CROSS JOIN last_week l;



