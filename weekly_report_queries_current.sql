-- OC Cities Query

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
      AND f.date_id >= 20251124 AND f.date_id <= 20251201
      AND f.business_type = 0
),
-- MTM (Monthly Transacting Merchant) for current month
mtm_current_month AS (
    SELECT 
        COUNT(DISTINCT f.merchant_id) as mtm_count
    FROM ocd_adw.f_food_metrics f
    WHERE f.country_id = 1 
      AND f.city_id != 1
      AND f.date_id >= 20251201 AND f.date_id <= 20251231
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
      AND f.date_id >= 20251201 AND f.date_id <= 20251231
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
      AND f.date_id >= 20251101 AND f.date_id <= 20251130
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
      AND f.date_id >= 20251101 AND f.date_id <= 20251130
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
      AND f.date_id >= 20241201 AND f.date_id <= 20241231
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
      AND f.date_id >= 20241201 AND f.date_id <= 20241231
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
      AND f.date_id >= 20251024 AND f.date_id <= 20251101
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
      AND f.date_id >= 20241124 AND f.date_id <= 20241201
      AND f.business_type = 0
),
-- Sessions calculation using ocd_adw.agg_food_cops_metrics (high intent sessions = preorder_sessions)
sessions_this_week AS (
    SELECT 
        CAST(SUM(preorder_sessions) AS DOUBLE) as sessions_value
    FROM ocd_adw.agg_food_cops_metrics
    WHERE country_id = 1 
      AND city_id != 1
      AND date_id >= 20251124 AND date_id <= 20251201
      AND business = 'food'
),
sessions_same_week_last_month AS (
    SELECT 
        CAST(SUM(preorder_sessions) AS DOUBLE) as sessions_value
    FROM ocd_adw.agg_food_cops_metrics
    WHERE country_id = 1 
      AND city_id != 1
      AND date_id >= 20251024 AND date_id <= 20251101
      AND business = 'food'
),
sessions_same_week_last_year AS (
    SELECT 
        CAST(SUM(preorder_sessions) AS DOUBLE) as sessions_value
    FROM ocd_adw.agg_food_cops_metrics
    WHERE country_id = 1 
      AND city_id != 1
      AND date_id >= 20241124 AND date_id <= 20241201
      AND business = 'food'
),
-- COPS calculation using ocd_adw.agg_food_cops_metrics (underlying table for midas_analytics.v_agg_food_cops_metrics)
cops_this_week AS (
    SELECT 
        CAST(SUM(completed_orders) AS DOUBLE) / CAST(SUM(preorder_sessions) AS DOUBLE) as cops_value
    FROM ocd_adw.agg_food_cops_metrics
    WHERE country_id = 1 
      AND city_id != 1
      AND date_id >= 20251124 AND date_id <= 20251201
      AND business = 'food'
),
cops_same_week_last_month AS (
    SELECT 
        CAST(SUM(completed_orders) AS DOUBLE) / CAST(SUM(preorder_sessions) AS DOUBLE) as cops_value
    FROM ocd_adw.agg_food_cops_metrics
    WHERE country_id = 1 
      AND city_id != 1
      AND date_id >= 20251024 AND date_id <= 20251101
      AND business = 'food'
),
cops_same_week_last_year AS (
    SELECT 
        CAST(SUM(completed_orders) AS DOUBLE) / CAST(SUM(preorder_sessions) AS DOUBLE) as cops_value
    FROM ocd_adw.agg_food_cops_metrics
    WHERE country_id = 1 
      AND city_id != 1
      AND date_id >= 20241124 AND date_id <= 20241201
      AND business = 'food'
),
new_pax_this_week AS 
    -- New Pax calculation for week 20251124 to 20251201
    (
        SELECT COUNT(DISTINCT new_pax.passenger_id) as new_pax_count
        FROM (
            SELECT DISTINCT f.passenger_id
            FROM ocd_adw.f_food_metrics f
            WHERE f.country_id = 1 
              AND city_id != 1
              AND f.date_id >= 20251124 
              AND f.date_id <= 20251201
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
                            AND city_id != 1
                            AND business_type = 0
                            AND booking_state_simple = 'COMPLETED'
                          GROUP BY passenger_id
                      ) first_orders
                      WHERE first_order_date >= 20251124
                        AND first_order_date <= 20251201
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
                            AND city_id != 1
                            AND business_type = 0
                            AND booking_state_simple = 'COMPLETED'
                            AND date_id < 20251124
                          GROUP BY passenger_id
                      ) last_orders
                      WHERE last_order_date < 20251124 - 36500  -- More than 365 days ago
                        AND passenger_id NOT IN (
                            -- Exclude passengers who ordered in the last year (before this week)
                            SELECT DISTINCT passenger_id
                            FROM ocd_adw.f_food_metrics
                            WHERE country_id = 1
                              AND city_id != 1
                              AND business_type = 0
                              AND booking_state_simple = 'COMPLETED'
                              AND date_id >= 20251124 - 36500
                              AND date_id < 20251124
                        )
                  )
              )
        ) new_pax
    ),
new_pax_last_month AS 
    -- New Pax calculation for week 20251024 to 20251101
    (
        SELECT COUNT(DISTINCT new_pax.passenger_id) as new_pax_count
        FROM (
            SELECT DISTINCT f.passenger_id
            FROM ocd_adw.f_food_metrics f
            WHERE f.country_id = 1 
              AND city_id != 1
              AND f.date_id >= 20251024 
              AND f.date_id <= 20251101
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
                            AND city_id != 1
                            AND business_type = 0
                            AND booking_state_simple = 'COMPLETED'
                          GROUP BY passenger_id
                      ) first_orders
                      WHERE first_order_date >= 20251024
                        AND first_order_date <= 20251101
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
                            AND city_id != 1
                            AND business_type = 0
                            AND booking_state_simple = 'COMPLETED'
                            AND date_id < 20251024
                          GROUP BY passenger_id
                      ) last_orders
                      WHERE last_order_date < 20251024 - 36500  -- More than 365 days ago
                        AND passenger_id NOT IN (
                            -- Exclude passengers who ordered in the last year (before this week)
                            SELECT DISTINCT passenger_id
                            FROM ocd_adw.f_food_metrics
                            WHERE country_id = 1
                              AND city_id != 1
                              AND business_type = 0
                              AND booking_state_simple = 'COMPLETED'
                              AND date_id >= 20251024 - 36500
                              AND date_id < 20251024
                        )
                  )
              )
        ) new_pax
    ),
new_pax_last_year AS 
    -- New Pax calculation for week 20241124 to 20241201
    (
        SELECT COUNT(DISTINCT new_pax.passenger_id) as new_pax_count
        FROM (
            SELECT DISTINCT f.passenger_id
            FROM ocd_adw.f_food_metrics f
            WHERE f.country_id = 1 
              AND city_id != 1
              AND f.date_id >= 20241124 
              AND f.date_id <= 20241201
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
                            AND city_id != 1
                            AND business_type = 0
                            AND booking_state_simple = 'COMPLETED'
                          GROUP BY passenger_id
                      ) first_orders
                      WHERE first_order_date >= 20241124
                        AND first_order_date <= 20241201
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
                            AND city_id != 1
                            AND business_type = 0
                            AND booking_state_simple = 'COMPLETED'
                            AND date_id < 20241124
                          GROUP BY passenger_id
                      ) last_orders
                      WHERE last_order_date < 20241124 - 36500  -- More than 365 days ago
                        AND passenger_id NOT IN (
                            -- Exclude passengers who ordered in the last year (before this week)
                            SELECT DISTINCT passenger_id
                            FROM ocd_adw.f_food_metrics
                            WHERE country_id = 1
                              AND city_id != 1
                              AND business_type = 0
                              AND booking_state_simple = 'COMPLETED'
                              AND date_id >= 20241124 - 36500
                              AND date_id < 20241124
                        )
                  )
              )
        ) new_pax
    )
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


-- Top 5 Cities Query

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
      AND f.date_id >= 20251124 AND f.date_id <= 20251201
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
      AND f.date_id >= 20251024 AND f.date_id <= 20251101
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
      AND f.date_id >= 20241124 AND f.date_id <= 20241201
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
      AND f.date_id >= 20251124 
      AND f.date_id <= 20251201
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
              WHERE first_order_date >= 20251124
                AND first_order_date <= 20251201
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
                    AND date_id < 20251124
                  GROUP BY passenger_id, city_id
              ) last_orders
              WHERE last_order_date < 20251124 - 36500
                AND (passenger_id, city_id) NOT IN (
                    SELECT DISTINCT passenger_id, city_id
                    FROM ocd_adw.f_food_metrics
                    WHERE country_id = 1
                      AND city_id != 1
                      AND business_type = 0
                      AND booking_state_simple = 'COMPLETED'
                      AND date_id >= 20251124 - 36500
                      AND date_id < 20251124
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
      AND f.date_id >= 20251024 
      AND f.date_id <= 20251101
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
              WHERE first_order_date >= 20251024
                AND first_order_date <= 20251101
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
                    AND date_id < 20251024
                  GROUP BY passenger_id, city_id
              ) last_orders
              WHERE last_order_date < 20251024 - 36500
                AND (passenger_id, city_id) NOT IN (
                    SELECT DISTINCT passenger_id, city_id
                    FROM ocd_adw.f_food_metrics
                    WHERE country_id = 1
                      AND city_id != 1
                      AND business_type = 0
                      AND booking_state_simple = 'COMPLETED'
                      AND date_id >= 20251024 - 36500
                      AND date_id < 20251024
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
      AND f.date_id >= 20241124 
      AND f.date_id <= 20241201
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
              WHERE first_order_date >= 20241124
                AND first_order_date <= 20241201
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
                    AND date_id < 20241124
                  GROUP BY passenger_id, city_id
              ) last_orders
              WHERE last_order_date < 20241124 - 36500
                AND (passenger_id, city_id) NOT IN (
                    SELECT DISTINCT passenger_id, city_id
                    FROM ocd_adw.f_food_metrics
                    WHERE country_id = 1
                      AND city_id != 1
                      AND business_type = 0
                      AND booking_state_simple = 'COMPLETED'
                      AND date_id >= 20241124 - 36500
                      AND date_id < 20241124
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
      AND date_id >= 20251124 AND date_id <= 20251201
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
      AND date_id >= 20251024 AND date_id <= 20251101
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
      AND date_id >= 20241124 AND date_id <= 20241201
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
      AND date_id >= 20251124 AND date_id <= 20251201
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
      AND date_id >= 20251024 AND date_id <= 20251101
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
      AND date_id >= 20241124 AND date_id <= 20241201
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
      AND f.date_id >= 20251201 AND f.date_id <= 20251231
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
      AND f.date_id >= 20251101 AND f.date_id <= 20251130
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
      AND f.date_id >= 20241201 AND f.date_id <= 20241231
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
      AND f.date_id >= 20251201 AND f.date_id <= 20251231
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
      AND f.date_id >= 20251101 AND f.date_id <= 20251130
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
      AND f.date_id >= 20241201 AND f.date_id <= 20241231
      AND f.business_type = 0
      AND f.booking_state_simple = 'COMPLETED'
      AND f.merchant_id IS NOT NULL
      AND f.basket_size IS NOT NULL
    GROUP BY f.city_id
) median_yoy ON tc.city_id = median_yoy.city_id
ORDER BY t.gmv DESC
