-- ============================================================================
-- PENANG MAINLAND GROWTH ANALYSIS - DATA EXTRACTION QUERIES
-- ============================================================================
-- Purpose: Extract granular data to identify hyper-growth opportunities
-- Location: Penang Mainland (city_id = 13, filtered by Mainland areas)
-- Date Range: Last 12 months (adjust date_id filters as needed)
-- ============================================================================

-- ============================================================================
-- QUERY 1: MERCHANT LIST WITH CUISINE & HALAL STATUS (Mainland Only)
-- ============================================================================
-- Data Point: Merchant list filtered for Mainland, with Cuisine_Type and Halal_Status
-- Insight: Map cuisine gaps and Halal coverage by area
-- ============================================================================

WITH mainland_areas AS (
    -- Mainland areas based on QGIS classification
    SELECT DISTINCT area_id, area_name
    FROM ocd_adw.d_area
    WHERE city_id = 13  -- Penang
        AND (
            area_name LIKE 'Kepala Batas%' OR area_name = 'Kepala Batas'
            OR area_name LIKE 'Prai%' OR area_name = 'Prai'
            OR area_name LIKE 'Tasek Gelugor%' OR area_name = 'Tasek Gelugor'
            OR area_name LIKE 'Bandar Cassia%' OR area_name = 'Bandar Cassia'
            OR area_name LIKE 'Bukit Mertajam%' OR area_name = 'Bukit Mertajam'
            OR area_name LIKE 'Penaga%' OR area_name = 'Penaga'
            OR area_name LIKE 'Kubang Semang%' OR area_name = 'Kubang Semang'
            OR area_name LIKE 'Simpang Ampat%' OR area_name = 'Simpang Ampat'
            OR area_name LIKE 'Bukit Tengah%' OR area_name = 'Bukit Tengah'
            OR area_name LIKE 'Bukit Teh%' OR area_name = 'Bukit Teh'
            OR area_name LIKE 'Kws Perusahaan Bebas Perai%' OR area_name = 'Kws Perusahaan Bebas Perai'
            OR area_name LIKE 'Batu Kawan Industrial Park%' OR area_name = 'Batu Kawan Industrial Park'
            OR area_name LIKE 'Sungai Bakap%' OR area_name = 'Sungai Bakap'
            OR area_name LIKE 'Padang Serai%' OR area_name = 'Padang Serai'
            OR area_name LIKE 'Bandar Tasek Mutiara%' OR area_name = 'Bandar Tasek Mutiara'
            OR area_name LIKE 'Parit Buntar%' OR area_name = 'Parit Buntar'
            OR area_name LIKE 'Bukit Minyak%' OR area_name = 'Bukit Minyak'
            OR area_name LIKE 'Permatang Pauh%' OR area_name = 'Permatang Pauh'
            OR area_name LIKE 'Seberang Jaya%' OR area_name = 'Seberang Jaya'
            OR area_name LIKE 'Kulim%' OR area_name = 'Kulim'
            OR area_name LIKE 'Sungai Jawi%' OR area_name = 'Sungai Jawi'
            OR area_name LIKE 'Taman Widuri%' OR area_name = 'Taman Widuri'
            OR area_name LIKE 'Bagan Serai%' OR area_name = 'Bagan Serai'
            OR area_name LIKE 'Telok Air Tawar%' OR area_name = 'Telok Air Tawar'
            OR area_name LIKE 'Nibong Tebal%' OR area_name = 'Nibong Tebal'
            OR area_name LIKE 'Alma Jaya%' OR area_name = 'Alma Jaya'
            OR area_name LIKE 'Beringin%' OR area_name = 'Beringin'
            OR area_name LIKE 'Kuala Kurau%' OR area_name = 'Kuala Kurau'
            OR area_name LIKE 'Karangan%' OR area_name = 'Karangan'
            OR area_name LIKE 'Gurun_Sala Besar%' OR area_name = 'Gurun_Sala Besar'
            OR area_name LIKE 'Butterworth%' OR area_name = 'Butterworth'
        )
),
mainland_merchants AS (
    SELECT DISTINCT 
        m.merchant_id_nk,
        m.merchant_name,
        m.is_halal,
        m.primary_cuisine_id,
        m.array_primary_cuisine_id,
        m.status,
        m.last_order_date,
        a.area_name,
        a.area_id,
        m.segment,
        m.custom_segment,
        m.am_name
    FROM ocd_adw.d_merchant m
    INNER JOIN ocd_adw.d_area a 
        ON m.city_id = a.city_id 
        AND SUBSTRING(m.geohash, 1, 6) = SUBSTRING(a.geohash, 1, 6)
    INNER JOIN mainland_areas ma ON a.area_id = ma.area_id
    WHERE m.city_id = 13
        AND m.status = 'ACTIVE'
        AND m.geohash IS NOT NULL
)
SELECT 
    merchant_id_nk,
    merchant_name,
    area_name,
    halal_status,
    primary_cuisine_id,
    segment,
    custom_segment,
    am_name,
    last_order_date,
    merchant_status
FROM (
    SELECT 
        merchant_id_nk,
        merchant_name,
        area_name,
        CASE 
            WHEN is_halal = TRUE THEN 'Halal'
            WHEN is_halal = FALSE THEN 'Non-Halal'
            ELSE 'Unknown'
        END as halal_status,
        CAST(primary_cuisine_id AS VARCHAR) as primary_cuisine_id,
        -- Note: To get cuisine names, join with d_cuisine table if available
        segment,
        custom_segment,
        am_name,
        last_order_date,
        CASE 
            WHEN last_order_date < CURRENT_DATE - INTERVAL '12' MONTH 
            THEN 'Churned'
            WHEN last_order_date IS NULL 
            THEN 'Never Ordered'
            ELSE 'Active'
        END as merchant_status
    FROM mainland_merchants
) t
ORDER BY 3, 4, 2
LIMIT 10000;


-- ============================================================================
-- QUERY 2: HOURLY ORDER DISTRIBUTION (Island vs Mainland Comparison)
-- ============================================================================
-- Data Point: Orders by hour of day, split by Island vs. Mainland
-- Insight: Identify if Mainland is a "Supper Market" (10 PM - 2 AM) or "Family Dinner Market"
-- ============================================================================

WITH mainland_areas AS (
    SELECT DISTINCT area_id
    FROM ocd_adw.d_area
    WHERE city_id = 13
        AND area_name IN (
            'Alma Jaya', 'Bukit Mertajam', 'Butterworth', 'Perai', 
            'Kulim', 'Kepala Batas', 'Seberang Jaya', 'Prai',
            'Simpang Ampat', 'Nibong Tebal', 'Batu Kawan', 'Jawi'
        )
),
island_areas AS (
    -- Island areas based on QGIS classification
    SELECT DISTINCT area_id
    FROM ocd_adw.d_area
    WHERE city_id = 13
        AND (
            area_name LIKE 'Bayan Lepas%' OR area_name = 'Bayan Lepas'
            OR area_name LIKE 'Gelugor%' OR area_name = 'Gelugor'
            OR area_name LIKE 'Air Itam%' OR area_name = 'Air Itam'
            OR area_name LIKE 'Jelutong%' OR area_name = 'Jelutong'
            OR area_name LIKE 'Georgetown%' OR area_name = 'Georgetown'
            OR area_name LIKE 'Tanjung Bungah%' OR area_name = 'Tanjung Bungah'
            OR area_name LIKE 'Desa Ria%' OR area_name = 'Desa Ria'
            OR area_name LIKE 'Bayan Baru%' OR area_name = 'Bayan Baru'
            OR area_name LIKE 'Sungai Dua%' OR area_name = 'Sungai Dua'
            OR area_name LIKE 'Teluk Kumbar%' OR area_name = 'Teluk Kumbar'
            OR area_name LIKE 'Batu Feringgi%' OR area_name = 'Batu Feringgi'
            OR area_name LIKE 'Balik Pulau%' OR area_name = 'Balik Pulau'
            OR area_name LIKE 'Gurney%' OR area_name = 'Gurney'
            OR area_name LIKE 'Teluk Bahang%' OR area_name = 'Teluk Bahang'
            OR area_name LIKE 'Gertak Sanggul%' OR area_name = 'Gertak Sanggul'
        )
),
mainland_orders_by_hour AS (
    SELECT 
        f.hour_local,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END) as completed_orders,
        COUNT(DISTINCT f.order_id) as total_orders,
        SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.gross_merchandise_value ELSE 0 END) as gmv,
        AVG(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.basket_size END) as avg_basket_size,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.passenger_id END) as unique_passengers
    FROM ocd_adw.f_food_metrics f
    WHERE f.city_id = 13
        AND f.country_id = 1
        AND f.business_type = 0
        AND f.dropoff_area_id IN (SELECT area_id FROM mainland_areas)
        AND f.date_id >= CAST(DATE_FORMAT(DATE_ADD('month', -12, CURRENT_DATE), '%Y%m%d') AS INTEGER)
    GROUP BY f.hour_local
),
island_orders_by_hour AS (
    SELECT 
        f.hour_local,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END) as completed_orders,
        COUNT(DISTINCT f.order_id) as total_orders,
        SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.gross_merchandise_value ELSE 0 END) as gmv,
        AVG(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.basket_size END) as avg_basket_size,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.passenger_id END) as unique_passengers
    FROM ocd_adw.f_food_metrics f
    WHERE f.city_id = 13
        AND f.country_id = 1
        AND f.business_type = 0
        AND f.dropoff_area_id IN (SELECT area_id FROM island_areas)
        AND f.date_id >= CAST(DATE_FORMAT(DATE_ADD('month', -12, CURRENT_DATE), '%Y%m%d') AS INTEGER)
    GROUP BY f.hour_local
)
SELECT 
    COALESCE(m.hour_local, i.hour_local) as hour_of_day,
    COALESCE(m.completed_orders, 0) as mainland_orders,
    COALESCE(m.gmv, 0) as mainland_gmv,
    COALESCE(m.avg_basket_size, 0) as mainland_avg_basket_size,
    COALESCE(i.completed_orders, 0) as island_orders,
    COALESCE(i.gmv, 0) as island_gmv,
    COALESCE(i.avg_basket_size, 0) as island_avg_basket_size,
    CASE 
        WHEN COALESCE(m.completed_orders, 0) > 0 AND COALESCE(i.completed_orders, 0) > 0
        THEN ROUND((COALESCE(m.completed_orders, 0) / CAST(COALESCE(i.completed_orders, 0) AS DOUBLE)) * 100, 2)
        ELSE NULL
    END as mainland_vs_island_order_pct
FROM mainland_orders_by_hour m
FULL OUTER JOIN island_orders_by_hour i ON m.hour_local = i.hour_local
ORDER BY hour_of_day;


-- ============================================================================
-- QUERY 3: BASKET SIZE DISTRIBUTION (Mainland vs Island)
-- ============================================================================
-- Data Point: Histogram of basket sizes for Mainland vs. Island
-- Insight: If Mainland baskets are larger, validates "Family Meal" strategy
-- ============================================================================

WITH mainland_areas AS (
    SELECT DISTINCT area_id
    FROM ocd_adw.d_area
    WHERE city_id = 13
        AND area_name IN (
            'Alma Jaya', 'Bukit Mertajam', 'Butterworth', 'Perai', 
            'Kulim', 'Kepala Batas', 'Seberang Jaya', 'Prai',
            'Simpang Ampat', 'Nibong Tebal', 'Batu Kawan', 'Jawi'
        )
),
island_areas AS (
    -- Island areas based on QGIS classification
    SELECT DISTINCT area_id
    FROM ocd_adw.d_area
    WHERE city_id = 13
        AND (
            area_name LIKE 'Bayan Lepas%' OR area_name = 'Bayan Lepas'
            OR area_name LIKE 'Gelugor%' OR area_name = 'Gelugor'
            OR area_name LIKE 'Air Itam%' OR area_name = 'Air Itam'
            OR area_name LIKE 'Jelutong%' OR area_name = 'Jelutong'
            OR area_name LIKE 'Georgetown%' OR area_name = 'Georgetown'
            OR area_name LIKE 'Tanjung Bungah%' OR area_name = 'Tanjung Bungah'
            OR area_name LIKE 'Desa Ria%' OR area_name = 'Desa Ria'
            OR area_name LIKE 'Bayan Baru%' OR area_name = 'Bayan Baru'
            OR area_name LIKE 'Sungai Dua%' OR area_name = 'Sungai Dua'
            OR area_name LIKE 'Teluk Kumbar%' OR area_name = 'Teluk Kumbar'
            OR area_name LIKE 'Batu Feringgi%' OR area_name = 'Batu Feringgi'
            OR area_name LIKE 'Balik Pulau%' OR area_name = 'Balik Pulau'
            OR area_name LIKE 'Gurney%' OR area_name = 'Gurney'
            OR area_name LIKE 'Teluk Bahang%' OR area_name = 'Teluk Bahang'
            OR area_name LIKE 'Gertak Sanggul%' OR area_name = 'Gertak Sanggul'
        )
),
mainland_baskets AS (
    SELECT 
        CASE 
            WHEN f.basket_size < 15 THEN '0-15'
            WHEN f.basket_size < 25 THEN '15-25'
            WHEN f.basket_size < 40 THEN '25-40'
            WHEN f.basket_size < 60 THEN '40-60'
            ELSE '60+'
        END as basket_size_bucket,
        COUNT(DISTINCT f.order_id) as order_count,
        SUM(f.gross_merchandise_value) as total_gmv,
        AVG(f.basket_size) as avg_basket_size
    FROM ocd_adw.f_food_metrics f
    WHERE f.city_id = 13
        AND f.country_id = 1
        AND f.business_type = 0
        AND f.booking_state_simple = 'COMPLETED'
        AND f.dropoff_area_id IN (SELECT area_id FROM mainland_areas)
        AND f.date_id >= CAST(DATE_FORMAT(DATE_ADD('month', -12, CURRENT_DATE), '%Y%m%d') AS INTEGER)
        AND f.basket_size IS NOT NULL
    GROUP BY 
        CASE 
            WHEN f.basket_size < 15 THEN '0-15'
            WHEN f.basket_size < 25 THEN '15-25'
            WHEN f.basket_size < 40 THEN '25-40'
            WHEN f.basket_size < 60 THEN '40-60'
            ELSE '60+'
        END
),
island_baskets AS (
    SELECT 
        CASE 
            WHEN f.basket_size < 15 THEN '0-15'
            WHEN f.basket_size < 25 THEN '15-25'
            WHEN f.basket_size < 40 THEN '25-40'
            WHEN f.basket_size < 60 THEN '40-60'
            ELSE '60+'
        END as basket_size_bucket,
        COUNT(DISTINCT f.order_id) as order_count,
        SUM(f.gross_merchandise_value) as total_gmv,
        AVG(f.basket_size) as avg_basket_size
    FROM ocd_adw.f_food_metrics f
    WHERE f.city_id = 13
        AND f.country_id = 1
        AND f.business_type = 0
        AND f.booking_state_simple = 'COMPLETED'
        AND f.dropoff_area_id IN (SELECT area_id FROM island_areas)
        AND f.date_id >= CAST(DATE_FORMAT(DATE_ADD('month', -12, CURRENT_DATE), '%Y%m%d') AS INTEGER)
        AND f.basket_size IS NOT NULL
    GROUP BY 
        CASE 
            WHEN f.basket_size < 15 THEN '0-15'
            WHEN f.basket_size < 25 THEN '15-25'
            WHEN f.basket_size < 40 THEN '25-40'
            WHEN f.basket_size < 60 THEN '40-60'
            ELSE '60+'
        END
)
SELECT 
    COALESCE(m.basket_size_bucket, i.basket_size_bucket) as basket_size_bucket,
    COALESCE(m.order_count, 0) as mainland_orders,
    COALESCE(m.total_gmv, 0) as mainland_gmv,
    COALESCE(m.avg_basket_size, 0) as mainland_avg_basket_size,
    COALESCE(i.order_count, 0) as island_orders,
    COALESCE(i.total_gmv, 0) as island_gmv,
    COALESCE(i.avg_basket_size, 0) as island_avg_basket_size,
    CASE 
        WHEN COALESCE(m.order_count, 0) > 0 
        THEN ROUND((COALESCE(m.order_count, 0) * 100.0 / SUM(COALESCE(m.order_count, 0)) OVER ()), 2)
        ELSE 0
    END as mainland_pct_of_total,
    CASE 
        WHEN COALESCE(i.order_count, 0) > 0 
        THEN ROUND((COALESCE(i.order_count, 0) * 100.0 / SUM(COALESCE(i.order_count, 0)) OVER ()), 2)
        ELSE 0
    END as island_pct_of_total
FROM mainland_baskets m
FULL OUTER JOIN island_baskets i ON m.basket_size_bucket = i.basket_size_bucket
ORDER BY 
    CASE basket_size_bucket
        WHEN '0-15' THEN 1
        WHEN '15-25' THEN 2
        WHEN '25-40' THEN 3
        WHEN '40-60' THEN 4
        WHEN '60+' THEN 5
    END;


-- ============================================================================
-- QUERY 4: OPERATIONAL FRICTION METRICS (Cancellation & No Driver Rates by Zone)
-- ============================================================================
-- Data Point: Order cancellation rates and no-driver rates by Mainland sub-area
-- Insight: Identify areas with driver shortages or operational issues
-- ============================================================================

WITH mainland_areas AS (
    SELECT DISTINCT area_id, area_name
    FROM ocd_adw.d_area
    WHERE city_id = 13
        AND area_name IN (
            'Alma Jaya', 'Bukit Mertajam', 'Butterworth', 'Perai', 
            'Kulim', 'Kepala Batas', 'Seberang Jaya', 'Prai',
            'Simpang Ampat', 'Nibong Tebal', 'Batu Kawan', 'Jawi'
        )
),
order_metrics_by_area AS (
    SELECT 
        a.area_name,
        a.area_id,
        COUNT(DISTINCT f.order_id) as total_orders,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END) as completed_orders,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'CANCELLED' THEN f.order_id END) as cancelled_orders,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'CANCELLED' AND f.cancel_reason LIKE '%driver%' THEN f.order_id END) as no_driver_cancellations,
        COUNT(DISTINCT CASE WHEN f.is_allocated = FALSE AND f.booking_state_simple = 'CANCELLED' THEN f.order_id END) as unallocated_cancellations,
        AVG(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.actual_distance_of_trip END) as avg_delivery_distance_km,
        AVG(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.actual_trip_time END) as avg_delivery_time_seconds,
        SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.gross_merchandise_value ELSE 0 END) as total_gmv,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.merchant_id END) as active_merchants
    FROM ocd_adw.f_food_metrics f
    INNER JOIN mainland_areas a ON f.dropoff_area_id = a.area_id
    WHERE f.city_id = 13
        AND f.country_id = 1
        AND f.business_type = 0
        AND f.date_id >= CAST(DATE_FORMAT(DATE_ADD('month', -12, CURRENT_DATE), '%Y%m%d') AS INTEGER)
    GROUP BY a.area_name, a.area_id
)
SELECT 
    area_name,
    total_orders,
    completed_orders,
    cancelled_orders,
    no_driver_cancellations,
    unallocated_cancellations,
    CASE 
        WHEN total_orders > 0 
        THEN ROUND((cancelled_orders * 100.0 / total_orders), 2)
        ELSE 0
    END as cancellation_rate_pct,
    CASE 
        WHEN total_orders > 0 
        THEN ROUND((no_driver_cancellations * 100.0 / total_orders), 2)
        ELSE 0
    END as no_driver_rate_pct,
    CASE 
        WHEN total_orders > 0 
        THEN ROUND((unallocated_cancellations * 100.0 / total_orders), 2)
        ELSE 0
    END as unallocated_rate_pct,
    ROUND(avg_delivery_distance_km / 1000.0, 2) as avg_delivery_distance_km,
    ROUND(avg_delivery_time_seconds / 60.0, 2) as avg_delivery_time_minutes,
    total_gmv,
    active_merchants,
    CASE 
        WHEN completed_orders > 0 
        THEN ROUND((total_gmv / completed_orders), 2)
        ELSE 0
    END as avg_order_value
FROM order_metrics_by_area
ORDER BY cancellation_rate_pct DESC, area_name;


-- ============================================================================
-- QUERY 5: CHURNED / INACTIVE MERCHANTS (Mainland Only)
-- ============================================================================
-- Data Point: Merchants in Mainland areas who went inactive in last 12 months
-- Insight: Win-back opportunities (faster than new acquisition)
-- ============================================================================

WITH mainland_areas AS (
    SELECT DISTINCT area_id, area_name
    FROM ocd_adw.d_area
    WHERE city_id = 13
        AND area_name IN (
            'Alma Jaya', 'Bukit Mertajam', 'Butterworth', 'Perai', 
            'Kulim', 'Kepala Batas', 'Seberang Jaya', 'Prai',
            'Simpang Ampat', 'Nibong Tebal', 'Batu Kawan', 'Jawi'
        )
),
mainland_merchants AS (
    SELECT DISTINCT 
        m.merchant_id_nk,
        m.merchant_name,
        m.is_halal,
        m.status,
        m.last_order_date,
        m.last_completed_order_date,
        a.area_name,
        m.segment,
        m.am_name
    FROM ocd_adw.d_merchant m
    INNER JOIN ocd_adw.d_area a 
        ON m.city_id = a.city_id 
        AND SUBSTRING(m.geohash, 1, 6) = SUBSTRING(a.geohash, 1, 6)
    INNER JOIN mainland_areas ma ON a.area_id = ma.area_id
    WHERE m.city_id = 13
        AND m.geohash IS NOT NULL
),
merchant_last_activity AS (
    SELECT 
        f.merchant_id,
        MAX(f.date_id) as last_order_date_id,
        MAX(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.date_id END) as last_completed_order_date_id
    FROM ocd_adw.f_food_metrics f
    WHERE f.city_id = 13
        AND f.country_id = 1
        AND f.business_type = 0
        AND f.date_id >= CAST(DATE_FORMAT(DATE_ADD('month', -24, CURRENT_DATE), '%Y%m%d') AS INTEGER)
    GROUP BY f.merchant_id
)
SELECT 
    m.merchant_id_nk,
    m.merchant_name,
    m.area_name,
    CASE 
        WHEN m.is_halal = TRUE THEN 'Halal'
        WHEN m.is_halal = FALSE THEN 'Non-Halal'
        ELSE 'Unknown'
    END as halal_status,
    m.status as current_status,
    m.last_order_date as merchant_last_order_date,
    m.last_completed_order_date as merchant_last_completed_date,
    CAST(mla.last_order_date_id AS VARCHAR) as last_order_date_id,
    CAST(mla.last_completed_order_date_id AS VARCHAR) as last_completed_order_date_id,
    CASE 
        WHEN mla.last_completed_order_date_id IS NULL THEN 'Never Completed'
        WHEN mla.last_completed_order_date_id < CAST(DATE_FORMAT(DATE_ADD('month', -12, CURRENT_DATE), '%Y%m%d') AS INTEGER) 
        THEN 'Churned (>12 months)'
        WHEN mla.last_completed_order_date_id < CAST(DATE_FORMAT(DATE_ADD('month', -6, CURRENT_DATE), '%Y%m%d') AS INTEGER) 
        THEN 'Inactive (6-12 months)'
        ELSE 'Active'
    END as churn_status,
    m.segment,
    m.am_name
FROM mainland_merchants m
LEFT JOIN merchant_last_activity mla ON m.merchant_id_nk = mla.merchant_id
WHERE mla.last_completed_order_date_id IS NULL 
    OR mla.last_completed_order_date_id < CAST(DATE_FORMAT(DATE_ADD('month', -12, CURRENT_DATE), '%Y%m%d') AS INTEGER)
ORDER BY 
    CASE 
        WHEN mla.last_completed_order_date_id IS NULL THEN 1
        WHEN mla.last_completed_order_date_id < CAST(DATE_FORMAT(DATE_ADD('month', -12, CURRENT_DATE), '%Y%m%d') AS INTEGER) 
        THEN 2
        WHEN mla.last_completed_order_date_id < CAST(DATE_FORMAT(DATE_ADD('month', -6, CURRENT_DATE), '%Y%m%d') AS INTEGER) 
        THEN 3
        ELSE 4
    END,
    m.area_name,
    m.merchant_name
LIMIT 5000;


-- ============================================================================
-- QUERY 6: DELIVERY DISTANCE ANALYSIS (Mainland)
-- ============================================================================
-- Data Point: Average delivery distance for Mainland orders
-- Insight: If distances are too long, delivery fees might be growth blocker
-- ============================================================================

WITH mainland_areas AS (
    SELECT DISTINCT area_id, area_name
    FROM ocd_adw.d_area
    WHERE city_id = 13
        AND area_name IN (
            'Alma Jaya', 'Bukit Mertajam', 'Butterworth', 'Perai', 
            'Kulim', 'Kepala Batas', 'Seberang Jaya', 'Prai',
            'Simpang Ampat', 'Nibong Tebal', 'Batu Kawan', 'Jawi'
        )
)
SELECT 
    a.area_name,
    COUNT(DISTINCT f.order_id) as completed_orders,
    AVG(f.actual_distance_of_trip) / 1000.0 as avg_delivery_distance_km,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY f.actual_distance_of_trip) / 1000.0 as median_delivery_distance_km,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY f.actual_distance_of_trip) / 1000.0 as p75_delivery_distance_km,
    PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY f.actual_distance_of_trip) / 1000.0 as p90_delivery_distance_km,
    MAX(f.actual_distance_of_trip) / 1000.0 as max_delivery_distance_km,
    AVG(f.pax_delivery_fee) as avg_delivery_fee,
    AVG(f.pax_delivery_fee) / NULLIF(AVG(f.actual_distance_of_trip) / 1000.0, 0) as delivery_fee_per_km,
    COUNT(DISTINCT CASE WHEN f.actual_distance_of_trip > 10000 THEN f.order_id END) as orders_over_10km,
    ROUND(COUNT(DISTINCT CASE WHEN f.actual_distance_of_trip > 10000 THEN f.order_id END) * 100.0 / 
          NULLIF(COUNT(DISTINCT f.order_id), 0), 2) as pct_orders_over_10km
FROM ocd_adw.f_food_metrics f
INNER JOIN mainland_areas a ON f.dropoff_area_id = a.area_id
WHERE f.city_id = 13
    AND f.country_id = 1
    AND f.business_type = 0
    AND f.booking_state_simple = 'COMPLETED'
    AND f.actual_distance_of_trip IS NOT NULL
    AND f.actual_distance_of_trip > 0
    AND f.date_id >= CAST(DATE_FORMAT(DATE_ADD('month', -12, CURRENT_DATE), '%Y%m%d') AS INTEGER)
GROUP BY a.area_name
ORDER BY avg_delivery_distance_km DESC;


-- ============================================================================
-- NOTES & LIMITATIONS
-- ============================================================================
-- 
-- 1. SEARCH DATA (Failed Searches):
--    - Search query data is typically stored in separate analytics tables
--    - May need to access: scribe_session data, search_log tables, or 
--      user behavior analytics tables
--    - Query 7 below provides a template if search data is available
--
-- 2. CUISINE NAMES:
--    - primary_cuisine_id is numeric - need to join with d_cuisine table
--    - If d_cuisine table exists, add join:
--      LEFT JOIN ocd_adw.d_cuisine c ON m.primary_cuisine_id = c.cuisine_id
--
-- 3. MAINLAND AREA DEFINITION:
--    - Adjust area_name list in mainland_areas CTE based on actual d_area data
--    - Verify area names match exactly (case-sensitive)
--
-- 4. DATE RANGES:
--    - All queries use last 12 months - adjust date_id filters as needed
--    - Current date format: YYYYMMDD (integer)
--
-- ============================================================================
-- QUERY 7: FAILED SEARCHES / SESSIONS WITH NO ORDERS
-- ============================================================================
-- Data Point: Sessions in Mainland with no completed orders (proxy for failed searches)
-- Insight: Identifies areas with high session-to-order drop-off (potential unmet demand)
-- 
-- NOTE: This is an ALTERNATIVE APPROACH since direct search query data may not be available.
-- This identifies sessions where users browsed but didn't order, which could indicate:
-- 1. No search results found
-- 2. Search results didn't match expectations
-- 3. High delivery fees or other friction
-- ============================================================================

WITH mainland_areas AS (
    SELECT DISTINCT area_id, area_name
    FROM ocd_adw.d_area
    WHERE city_id = 13
        AND area_name IN (
            'Alma Jaya', 'Bukit Mertajam', 'Butterworth', 'Perai', 
            'Kulim', 'Kepala Batas', 'Seberang Jaya', 'Prai',
            'Simpang Ampat', 'Nibong Tebal', 'Batu Kawan', 'Jawi'
        )
),
-- Get all sessions in Mainland areas
mainland_sessions AS (
    SELECT 
        f.scribe_session_id,
        f.dropoff_area_id,
        f.date_id,
        f.hour_local,
        f.passenger_id,
        COUNT(DISTINCT f.order_id) as total_orders_in_session,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END) as completed_orders_in_session,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'CANCELLED' THEN f.order_id END) as cancelled_orders_in_session,
        MAX(f.created_at_local) as session_start_time
    FROM ocd_adw.f_food_metrics f
    WHERE f.city_id = 13
        AND f.country_id = 1
        AND f.business_type = 0
        AND f.dropoff_area_id IN (SELECT area_id FROM mainland_areas)
        AND f.scribe_session_id IS NOT NULL
        AND f.date_id >= CAST(DATE_FORMAT(DATE_ADD('month', -3, CURRENT_DATE), '%Y%m%d') AS INTEGER)
    GROUP BY f.scribe_session_id, f.dropoff_area_id, f.date_id, f.hour_local, f.passenger_id
),
-- Sessions with no completed orders (potential failed searches)
failed_sessions AS (
    SELECT 
        ms.scribe_session_id,
        ms.dropoff_area_id,
        a.area_name,
        ms.date_id,
        ms.hour_local,
        ms.passenger_id,
        ms.total_orders_in_session,
        ms.completed_orders_in_session,
        ms.cancelled_orders_in_session
    FROM mainland_sessions ms
    INNER JOIN mainland_areas a ON ms.dropoff_area_id = a.area_id
    WHERE ms.completed_orders_in_session = 0
),
-- Aggregate by area and hour
failed_sessions_summary AS (
    SELECT 
        area_name,
        hour_local,
        COUNT(DISTINCT scribe_session_id) as sessions_with_no_orders,
        COUNT(DISTINCT passenger_id) as unique_users_with_no_orders,
        SUM(total_orders_in_session) as total_attempted_orders,
        SUM(cancelled_orders_in_session) as total_cancelled_orders
    FROM failed_sessions
    GROUP BY area_name, hour_local
),
-- Compare with successful sessions for context
successful_sessions AS (
    SELECT 
        a.area_name,
        f.hour_local,
        COUNT(DISTINCT f.scribe_session_id) as sessions_with_orders,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END) as completed_orders
    FROM ocd_adw.f_food_metrics f
    INNER JOIN mainland_areas a ON f.dropoff_area_id = a.area_id
    WHERE f.city_id = 13
        AND f.country_id = 1
        AND f.business_type = 0
        AND f.booking_state_simple = 'COMPLETED'
        AND f.date_id >= CAST(DATE_FORMAT(DATE_ADD('month', -3, CURRENT_DATE), '%Y%m%d') AS INTEGER)
    GROUP BY a.area_name, f.hour_local
)
SELECT 
    COALESCE(f.area_name, s.area_name) as area_name,
    COALESCE(f.hour_local, s.hour_local) as hour_of_day,
    COALESCE(f.sessions_with_no_orders, 0) as sessions_with_no_orders,
    COALESCE(f.unique_users_with_no_orders, 0) as unique_users_with_no_orders,
    COALESCE(s.sessions_with_orders, 0) as sessions_with_orders,
    COALESCE(s.completed_orders, 0) as completed_orders,
    CASE 
        WHEN COALESCE(f.sessions_with_no_orders, 0) + COALESCE(s.sessions_with_orders, 0) > 0
        THEN ROUND((COALESCE(f.sessions_with_no_orders, 0) * 100.0 / 
                    (COALESCE(f.sessions_with_no_orders, 0) + COALESCE(s.sessions_with_orders, 0))), 2)
        ELSE 0
    END as session_drop_off_rate_pct,
    COALESCE(f.total_attempted_orders, 0) as total_attempted_orders,
    COALESCE(f.total_cancelled_orders, 0) as total_cancelled_orders
FROM failed_sessions_summary f
FULL OUTER JOIN successful_sessions s 
    ON f.area_name = s.area_name AND f.hour_local = s.hour_local
ORDER BY sessions_with_no_orders DESC, area_name, hour_of_day
LIMIT 100;


-- ============================================================================
-- ALTERNATIVE: If track_events_v2 table exists with search events
-- ============================================================================
-- Check if grab_x.track_events_v2 contains search query data
-- NOTE: This table requires scope filter - adjust scope as needed
/*
WITH mainland_areas AS (
    SELECT DISTINCT area_id, area_name
    FROM ocd_adw.d_area
    WHERE city_id = 13
        AND area_name IN (
            'Alma Jaya', 'Bukit Mertajam', 'Butterworth', 'Perai', 
            'Kulim', 'Kepala Batas', 'Seberang Jaya', 'Prai',
            'Simpang Ampat', 'Nibong Tebal', 'Batu Kawan', 'Jawi'
        )
),
search_events AS (
    SELECT 
        event_name,
        event_properties['search_query'] as search_query,
        event_properties['has_results'] as has_results,
        event_properties['result_count'] as result_count,
        area_id,
        date_id,
        user_id
    FROM grab_x.track_events_v2
    WHERE scope = 'grab_food'  -- ADJUST SCOPE AS NEEDED
        AND event_name LIKE '%search%'
        AND ingestion_date >= CURRENT_DATE - INTERVAL '3' MONTH
        AND area_id IN (SELECT area_id FROM mainland_areas)
)
SELECT 
    search_query,
    COUNT(DISTINCT user_id) as unique_searchers,
    COUNT(*) as total_searches,
    COUNT(DISTINCT CASE WHEN has_results = 'false' OR result_count = 0 THEN user_id END) as searches_with_no_results,
    COUNT(DISTINCT CASE WHEN has_results = 'true' AND result_count > 0 THEN user_id END) as searches_with_results
FROM search_events
WHERE search_query IS NOT NULL
GROUP BY search_query
ORDER BY total_searches DESC
LIMIT 20;
*/

