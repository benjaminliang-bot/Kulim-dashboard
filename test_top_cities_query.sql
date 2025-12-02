
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
        COUNT(DISTINCT f.scribe_session_id) as unique_sessions,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.scribe_session_id END) as completed_sessions,
        ROUND(100.0 * COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END) / 
              NULLIF(COUNT(DISTINCT f.order_id), 0), 2) as completion_rate
    FROM ocd_adw.f_food_metrics f
    JOIN ocd_adw.d_city dc ON f.city_id = dc.city_id
    WHERE f.country_id = 1 
      AND f.city_id != 1
      AND f.date_id >= 20251103 AND f.date_id <= 20251109
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
        COUNT(DISTINCT f.scribe_session_id) as unique_sessions,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.scribe_session_id END) as completed_sessions,
        ROUND(100.0 * COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END) / 
              NULLIF(COUNT(DISTINCT f.order_id), 0), 2) as completion_rate
    FROM ocd_adw.f_food_metrics f
    JOIN ocd_adw.d_city dc ON f.city_id = dc.city_id
    WHERE f.country_id = 1 
      AND f.city_id != 1
      AND f.date_id >= 20250930 AND f.date_id <= 20251006
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
        COUNT(DISTINCT f.scribe_session_id) as unique_sessions,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.scribe_session_id END) as completed_sessions,
        ROUND(100.0 * COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END) / 
              NULLIF(COUNT(DISTINCT f.order_id), 0), 2) as completion_rate
    FROM ocd_adw.f_food_metrics f
    JOIN ocd_adw.d_city dc ON f.city_id = dc.city_id
    WHERE f.country_id = 1 
      AND f.city_id != 1
      AND f.date_id >= 20241103 AND f.date_id <= 20241109
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
      AND f.date_id >= 20251103 
      AND f.date_id <= 20251109
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
              WHERE first_order_date >= 20251103
                AND first_order_date <= 20251109
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
                    AND date_id < 20251103
                  GROUP BY passenger_id, city_id
              ) last_orders
              WHERE last_order_date < 20251103 - 36500
                AND (passenger_id, city_id) NOT IN (
                    SELECT DISTINCT passenger_id, city_id
                    FROM ocd_adw.f_food_metrics
                    WHERE country_id = 1
                      AND city_id != 1
                      AND business_type = 0
                      AND booking_state_simple = 'COMPLETED'
                      AND date_id >= 20251103 - 36500
                      AND date_id < 20251103
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
      AND f.date_id >= 20250930 
      AND f.date_id <= 20251006
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
              WHERE first_order_date >= 20250930
                AND first_order_date <= 20251006
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
                    AND date_id < 20250930
                  GROUP BY passenger_id, city_id
              ) last_orders
              WHERE last_order_date < 20250930 - 36500
                AND (passenger_id, city_id) NOT IN (
                    SELECT DISTINCT passenger_id, city_id
                    FROM ocd_adw.f_food_metrics
                    WHERE country_id = 1
                      AND city_id != 1
                      AND business_type = 0
                      AND booking_state_simple = 'COMPLETED'
                      AND date_id >= 20250930 - 36500
                      AND date_id < 20250930
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
      AND f.date_id >= 20241103 
      AND f.date_id <= 20241109
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
              WHERE first_order_date >= 20241103
                AND first_order_date <= 20241109
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
                    AND date_id < 20241103
                  GROUP BY passenger_id, city_id
              ) last_orders
              WHERE last_order_date < 20241103 - 36500
                AND (passenger_id, city_id) NOT IN (
                    SELECT DISTINCT passenger_id, city_id
                    FROM ocd_adw.f_food_metrics
                    WHERE country_id = 1
                      AND city_id != 1
                      AND business_type = 0
                      AND booking_state_simple = 'COMPLETED'
                      AND date_id >= 20241103 - 36500
                      AND date_id < 20241103
                )
          )
      )
    GROUP BY f.city_id
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
    t.unique_sessions as this_week_sessions,
    m.unique_sessions as same_week_last_month_sessions,
    y.unique_sessions as ytd_avg_sessions,
    t.completed_sessions as this_week_completed_sessions,
    m.completed_sessions as same_week_last_month_completed_sessions,
    y.completed_sessions as ytd_avg_completed_sessions,
    ROUND(1.0 * t.orders / NULLIF(t.unique_sessions, 0), 2) as this_week_orders_per_session,
    ROUND(1.0 * m.orders / NULLIF(m.unique_sessions, 0), 2) as same_week_last_month_orders_per_session,
    ROUND(1.0 * y.orders / NULLIF(y.unique_sessions, 0), 2) as ytd_avg_orders_per_session,
    ROUND(1.0 * t.completed_orders / NULLIF(t.completed_sessions, 0), 2) as this_week_cops,
    ROUND(1.0 * m.completed_orders / NULLIF(m.completed_sessions, 0), 2) as same_week_last_month_cops,
    ROUND(1.0 * y.completed_orders / NULLIF(y.completed_sessions, 0), 2) as ytd_avg_cops,
    COALESCE(npw.new_pax_count, 0) as this_week_new_pax,
    COALESCE(npm.new_pax_count, 0) as same_week_last_month_new_pax,
    COALESCE(npy.new_pax_count, 0) as ytd_avg_new_pax,
    COALESCE(mtm_curr.mtm_count, 0) as current_month_mtm,
    COALESCE(mtm_last.mtm_count, 0) as last_month_mtm,
    COALESCE(mtm_yoy.mtm_count, 0) as same_month_last_year_mtm,
    COALESCE(mtm_curr.total_earnings, 0) as current_month_total_earnings,
    COALESCE(mtm_last.total_earnings, 0) as last_month_total_earnings,
    COALESCE(mtm_yoy.total_earnings, 0) as same_month_last_year_total_earnings,
    ROUND(COALESCE(mtm_curr.total_earnings, 0) / NULLIF(mtm_curr.mtm_count, 0), 2) as current_month_earning_per_mex,
    ROUND(COALESCE(mtm_last.total_earnings, 0) / NULLIF(mtm_last.mtm_count, 0), 2) as last_month_earning_per_mex,
    ROUND(COALESCE(mtm_yoy.total_earnings, 0) / NULLIF(mtm_yoy.mtm_count, 0), 2) as same_month_last_year_earning_per_mex
FROM top_cities tc
LEFT JOIN this_week_cities t ON tc.city_id = t.city_id
LEFT JOIN same_week_last_month_cities m ON tc.city_id = m.city_id
LEFT JOIN same_week_last_year_cities y ON tc.city_id = y.city_id
LEFT JOIN new_pax_this_week_by_city npw ON tc.city_id = npw.city_id
LEFT JOIN new_pax_last_month_by_city npm ON tc.city_id = npm.city_id
LEFT JOIN new_pax_last_year_by_city npy ON tc.city_id = npy.city_id
LEFT JOIN (
    SELECT 
        f.city_id,
        COUNT(DISTINCT f.merchant_id) as mtm_count,
        SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN COALESCE(f.commission_from_merchant, 0) ELSE 0 END) as total_earnings
    FROM ocd_adw.f_food_metrics f
    WHERE f.country_id = 1 
      AND f.city_id != 1
      AND f.date_id >= 20251101 AND f.date_id <= 20251130
      AND f.business_type = 0
      AND f.booking_state_simple = 'COMPLETED'
      AND f.merchant_id IS NOT NULL
    GROUP BY f.city_id
) mtm_curr ON tc.city_id = mtm_curr.city_id
LEFT JOIN (
    SELECT 
        f.city_id,
        COUNT(DISTINCT f.merchant_id) as mtm_count,
        SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN COALESCE(f.commission_from_merchant, 0) ELSE 0 END) as total_earnings
    FROM ocd_adw.f_food_metrics f
    WHERE f.country_id = 1 
      AND f.city_id != 1
      AND f.date_id >= 20251001 AND f.date_id <= 20251031
      AND f.business_type = 0
      AND f.booking_state_simple = 'COMPLETED'
      AND f.merchant_id IS NOT NULL
    GROUP BY f.city_id
) mtm_last ON tc.city_id = mtm_last.city_id
LEFT JOIN (
    SELECT 
        f.city_id,
        COUNT(DISTINCT f.merchant_id) as mtm_count,
        SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN COALESCE(f.commission_from_merchant, 0) ELSE 0 END) as total_earnings
    FROM ocd_adw.f_food_metrics f
    WHERE f.country_id = 1 
      AND f.city_id != 1
      AND f.date_id >= 20241101 AND f.date_id <= 20241130
      AND f.business_type = 0
      AND f.booking_state_simple = 'COMPLETED'
      AND f.merchant_id IS NOT NULL
    GROUP BY f.city_id
) mtm_yoy ON tc.city_id = mtm_yoy.city_id
ORDER BY t.gmv DESC
