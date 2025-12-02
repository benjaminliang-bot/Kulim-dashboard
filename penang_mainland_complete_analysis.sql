-- ============================================================================
-- PENANG MAINLAND COMPLETE GROWTH ANALYSIS - COMPREHENSIVE SQL SCRIPT
-- ============================================================================
-- Purpose: Complete merchant list + all growth analysis insights in one script
-- Location: Penang Mainland (city_id = 13, filtered by Mainland areas)
-- Date Range: Last 12 months (adjust date_id filters as needed)
-- 
-- KEY CHANGE: Halal status is determined by merchant name
-- Rule: If merchant name does NOT contain "[Non-Halal]", it is considered Halal
-- ============================================================================

-- ============================================================================
-- QUERY 1: COMPLETE MERCHANT LIST WITH READABLE CUISINE NAMES
-- ============================================================================
-- Data Point: All active merchants from Mainland with cuisine names and halal status
-- Insight: Map cuisine gaps and Halal coverage by area
-- Halal Classification: Based on merchant name (if name doesn't contain "[Non-Halal]", it's Halal)
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
),
merchant_cuisines AS (
    SELECT 
        m.merchant_id_nk,
        m.merchant_name,
        m.area_name,
        m.is_halal,
        m.primary_cuisine_id,
        m.segment,
        m.custom_segment,
        m.am_name,
        m.last_order_date,
        -- HALAL STATUS: Based on merchant name, not cuisine
        -- If merchant name does NOT contain "[Non-Halal]", it is considered Halal
        CASE 
            WHEN UPPER(m.merchant_name) LIKE '%[NON-HALAL]%' 
                OR UPPER(m.merchant_name) LIKE '%[NON HALAL]%'
                OR UPPER(m.merchant_name) LIKE '%(NON-HALAL)%'
                OR UPPER(m.merchant_name) LIKE '%(NON HALAL)%'
            THEN 'Non-Halal'
            ELSE 'Halal'
        END as halal_status,
        CASE 
            WHEN m.last_order_date < CURRENT_DATE - INTERVAL '12' MONTH 
            THEN 'Churned'
            WHEN m.last_order_date IS NULL 
            THEN 'Never Ordered'
            ELSE 'Active'
        END as merchant_status,
        cuisine_id
    FROM mainland_merchants m
    CROSS JOIN UNNEST(m.array_primary_cuisine_id) AS t(cuisine_id)
),
merchant_cuisine_names AS (
    SELECT 
        mc.merchant_id_nk,
        mc.merchant_name,
        mc.area_name,
        mc.halal_status,
        mc.segment,
        mc.custom_segment,
        mc.am_name,
        mc.last_order_date,
        mc.merchant_status,
        ARRAY_JOIN(ARRAY_AGG(DISTINCT c.name ORDER BY c.name), ', ') as cuisine_names
    FROM merchant_cuisines mc
    LEFT JOIN ocd_adw.d_cuisine c ON mc.cuisine_id = c.cuisine_id
    GROUP BY 
        mc.merchant_id_nk,
        mc.merchant_name,
        mc.area_name,
        mc.halal_status,
        mc.segment,
        mc.custom_segment,
        mc.am_name,
        mc.last_order_date,
        mc.merchant_status
)
SELECT 
    merchant_id_nk,
    merchant_name,
    area_name,
    halal_status,
    COALESCE(cuisine_names, 'Unknown') as cuisine_names,
    segment,
    custom_segment,
    am_name,
    last_order_date,
    merchant_status
FROM merchant_cuisine_names
ORDER BY area_name, halal_status, merchant_name;


-- ============================================================================
-- QUERY 2: HALAL COVERAGE ANALYSIS BY AREA
-- ============================================================================
-- Insight: Identifies areas with critical Halal supply gaps
-- Key Finding: Only 0.67% of merchants are Halal (159 out of 23,583)
-- Action: Priority areas for Halal merchant acquisition
-- ============================================================================

WITH mainland_areas AS (
    SELECT DISTINCT area_id, area_name
    FROM ocd_adw.d_area
    WHERE city_id = 13
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
        a.area_name,
        CASE 
            WHEN UPPER(m.merchant_name) LIKE '%[NON-HALAL]%' 
                OR UPPER(m.merchant_name) LIKE '%[NON HALAL]%'
                OR UPPER(m.merchant_name) LIKE '%(NON-HALAL)%'
                OR UPPER(m.merchant_name) LIKE '%(NON HALAL)%'
            THEN 'Non-Halal'
            ELSE 'Halal'
        END as halal_status,
        m.last_order_date
    FROM ocd_adw.d_merchant m
    INNER JOIN ocd_adw.d_area a 
        ON m.city_id = a.city_id 
        AND SUBSTRING(m.geohash, 1, 6) = SUBSTRING(a.geohash, 1, 6)
    INNER JOIN mainland_areas ma ON a.area_id = ma.area_id
    WHERE m.city_id = 13
        AND m.status = 'ACTIVE'
        AND m.geohash IS NOT NULL
),
halal_coverage AS (
    SELECT 
        area_name,
        COUNT(DISTINCT merchant_id_nk) as total_merchants,
        COUNT(DISTINCT CASE WHEN halal_status = 'Halal' THEN merchant_id_nk END) as halal_merchants,
        COUNT(DISTINCT CASE WHEN halal_status = 'Non-Halal' THEN merchant_id_nk END) as non_halal_merchants,
        COUNT(DISTINCT CASE WHEN halal_status = 'Halal' 
            AND last_order_date >= CURRENT_DATE - INTERVAL '30' DAY 
            THEN merchant_id_nk END) as active_halal_30d,
        COUNT(DISTINCT CASE WHEN halal_status = 'Halal' 
            AND last_order_date >= CURRENT_DATE - INTERVAL '90' DAY 
            THEN merchant_id_nk END) as active_halal_90d
    FROM mainland_merchants
    GROUP BY area_name
)
SELECT 
    area_name,
    total_merchants,
    halal_merchants,
    non_halal_merchants,
    CASE 
        WHEN total_merchants > 0 
        THEN ROUND((halal_merchants * 100.0 / total_merchants), 2)
        ELSE 0
    END as halal_pct,
    active_halal_30d,
    active_halal_90d,
    CASE 
        WHEN halal_merchants > 0 
        THEN ROUND((active_halal_30d * 100.0 / halal_merchants), 2)
        ELSE 0
    END as halal_active_rate_30d_pct,
    CASE 
        WHEN halal_merchants = 0 THEN 'PRIORITY: Zero Halal Coverage'
        WHEN halal_pct < 1.0 THEN 'PRIORITY: Low Halal Coverage'
        ELSE 'OK'
    END as acquisition_priority
FROM halal_coverage
ORDER BY 
    CASE 
        WHEN halal_merchants = 0 THEN 1
        WHEN halal_pct < 1.0 THEN 2
        ELSE 3
    END,
    total_merchants DESC;


-- ============================================================================
-- QUERY 3: HOURLY ORDER DISTRIBUTION (Island vs Mainland Comparison)
-- ============================================================================
-- Insight: Mainland is a LUNCH MARKET (not supper market)
-- Key Finding: 12-1 PM accounts for 19% of daily orders (highest volume)
-- Action: Target lunch merchants (11 AM - 2 PM operations)
-- ============================================================================

WITH mainland_areas AS (
    SELECT DISTINCT area_id
    FROM ocd_adw.d_area
    WHERE city_id = 13
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
    END as mainland_vs_island_order_pct,
    CASE 
        WHEN COALESCE(m.completed_orders, 0) >= (
            SELECT MAX(completed_orders) FROM mainland_orders_by_hour
        ) * 0.9
        THEN 'PEAK HOUR'
        ELSE ''
    END as peak_indicator
FROM mainland_orders_by_hour m
FULL OUTER JOIN island_orders_by_hour i ON m.hour_local = i.hour_local
ORDER BY hour_of_day;


-- ============================================================================
-- QUERY 4: BASKET SIZE DISTRIBUTION (Mainland vs Island)
-- ============================================================================
-- Insight: Family Meal Strategy VALIDATED
-- Key Finding: 41.8% of orders are 25+ MYR (family meal segment)
-- Action: Launch "Family Bundle" campaigns targeting 25-40 MYR segment
-- ============================================================================

WITH mainland_areas AS (
    SELECT DISTINCT area_id
    FROM ocd_adw.d_area
    WHERE city_id = 13
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
island_areas AS (
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
    END as island_pct_of_total,
    CASE 
        WHEN COALESCE(m.order_count, 0) >= (
            SELECT SUM(order_count) FROM mainland_baskets WHERE basket_size_bucket IN ('25-40', '40-60', '60+')
        ) * 0.4
        THEN 'FAMILY MEAL SEGMENT'
        ELSE ''
    END as segment_type
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
-- QUERY 5: OPERATIONAL FRICTION METRICS (Cancellation & No Driver Rates)
-- ============================================================================
-- Insight: ZERO OPERATIONAL BLOCKERS - Infrastructure Ready
-- Key Finding: 0% cancellation rate across all areas
-- Action: No operational fixes needed - proceed with growth initiatives
-- ============================================================================

WITH mainland_areas AS (
    SELECT DISTINCT area_id, area_name
    FROM ocd_adw.d_area
    WHERE city_id = 13
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
    END as avg_order_value,
    CASE 
        WHEN cancellation_rate_pct = 0 THEN '✅ NO OPERATIONAL BLOCKERS'
        WHEN cancellation_rate_pct < 5 THEN '✅ HEALTHY'
        WHEN cancellation_rate_pct < 10 THEN '⚠️ MONITOR'
        ELSE '❌ NEEDS ATTENTION'
    END as operational_status
FROM order_metrics_by_area
ORDER BY cancellation_rate_pct DESC, area_name;


-- ============================================================================
-- QUERY 6: CHURNED / INACTIVE MERCHANTS (Mainland Only)
-- ============================================================================
-- Insight: Win-back opportunities (faster than new acquisition)
-- Key Finding: Many merchants are inactive or churned
-- Action: Target top 100 dormant merchants by historical GMV for reactivation
-- ============================================================================

WITH mainland_areas AS (
    SELECT DISTINCT area_id, area_name
    FROM ocd_adw.d_area
    WHERE city_id = 13
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
        CASE 
            WHEN UPPER(m.merchant_name) LIKE '%[NON-HALAL]%' 
                OR UPPER(m.merchant_name) LIKE '%[NON HALAL]%'
                OR UPPER(m.merchant_name) LIKE '%(NON-HALAL)%'
                OR UPPER(m.merchant_name) LIKE '%(NON HALAL)%'
            THEN 'Non-Halal'
            ELSE 'Halal'
        END as halal_status,
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
        MAX(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.date_id END) as last_completed_order_date_id,
        SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.gross_merchandise_value ELSE 0 END) as historical_gmv
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
    m.halal_status,
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
    COALESCE(mla.historical_gmv, 0) as historical_gmv,
    m.segment,
    m.am_name,
    CASE 
        WHEN mla.historical_gmv > 10000 THEN 'HIGH VALUE - PRIORITY WIN-BACK'
        WHEN mla.historical_gmv > 5000 THEN 'MEDIUM VALUE'
        WHEN mla.historical_gmv > 0 THEN 'LOW VALUE'
        ELSE 'NO HISTORY'
    END as win_back_priority
FROM mainland_merchants m
LEFT JOIN merchant_last_activity mla ON m.merchant_id_nk = mla.merchant_id
WHERE mla.last_completed_order_date_id IS NULL 
    OR mla.last_completed_order_date_id < CAST(DATE_FORMAT(DATE_ADD('month', -12, CURRENT_DATE), '%Y%m%d') AS INTEGER)
ORDER BY 
    COALESCE(mla.historical_gmv, 0) DESC,
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
-- QUERY 7: DELIVERY DISTANCE ANALYSIS (Mainland)
-- ============================================================================
-- Insight: If distances are too long, delivery fees might be growth blocker
-- Key Finding: Average delivery distance by area
-- Action: Monitor delivery fees and distance correlation
-- ============================================================================

WITH mainland_areas AS (
    SELECT DISTINCT area_id, area_name
    FROM ocd_adw.d_area
    WHERE city_id = 13
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
)
SELECT 
    a.area_name,
    COUNT(DISTINCT f.order_id) as completed_orders,
    ROUND(AVG(f.actual_distance_of_trip) / 1000.0, 2) as avg_delivery_distance_km,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY f.actual_distance_of_trip) / 1000.0, 2) as median_delivery_distance_km,
    ROUND(PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY f.actual_distance_of_trip) / 1000.0, 2) as p75_delivery_distance_km,
    ROUND(PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY f.actual_distance_of_trip) / 1000.0, 2) as p90_delivery_distance_km,
    ROUND(MAX(f.actual_distance_of_trip) / 1000.0, 2) as max_delivery_distance_km,
    ROUND(AVG(f.pax_delivery_fee), 2) as avg_delivery_fee,
    ROUND(AVG(f.pax_delivery_fee) / NULLIF(AVG(f.actual_distance_of_trip) / 1000.0, 0), 2) as delivery_fee_per_km,
    COUNT(DISTINCT CASE WHEN f.actual_distance_of_trip > 10000 THEN f.order_id END) as orders_over_10km,
    ROUND(COUNT(DISTINCT CASE WHEN f.actual_distance_of_trip > 10000 THEN f.order_id END) * 100.0 / 
          NULLIF(COUNT(DISTINCT f.order_id), 0), 2) as pct_orders_over_10km,
    CASE 
        WHEN AVG(f.actual_distance_of_trip) / 1000.0 > 8 THEN '⚠️ LONG DISTANCES - Monitor fees'
        WHEN AVG(f.actual_distance_of_trip) / 1000.0 > 5 THEN '⚠️ MODERATE DISTANCES'
        ELSE '✅ SHORT DISTANCES'
    END as distance_insight
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
-- QUERY 8: ACTIVE MERCHANT RATE COMPARISON (Mainland vs Island)
-- ============================================================================
-- Insight: Compare merchant health and supply utilization between Mainland and Island
-- Key Finding: Active merchant rate indicates supply efficiency
-- Action: Identify if Mainland has lower active rates (opportunity for win-back)
-- ============================================================================

WITH mainland_areas AS (
    SELECT DISTINCT area_id
    FROM ocd_adw.d_area
    WHERE city_id = 13
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
island_areas AS (
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
mainland_merchant_base AS (
    SELECT DISTINCT 
        m.merchant_id_nk,
        m.status
    FROM ocd_adw.d_merchant m
    INNER JOIN ocd_adw.d_area a 
        ON m.city_id = a.city_id 
        AND SUBSTRING(m.geohash, 1, 6) = SUBSTRING(a.geohash, 1, 6)
    INNER JOIN mainland_areas ma ON a.area_id = ma.area_id
    WHERE m.city_id = 13
        AND m.status = 'ACTIVE'
        AND m.geohash IS NOT NULL
),
island_merchant_base AS (
    SELECT DISTINCT 
        m.merchant_id_nk,
        m.status
    FROM ocd_adw.d_merchant m
    INNER JOIN ocd_adw.d_area a 
        ON m.city_id = a.city_id 
        AND SUBSTRING(m.geohash, 1, 6) = SUBSTRING(a.geohash, 1, 6)
    INNER JOIN island_areas ia ON a.area_id = ia.area_id
    WHERE m.city_id = 13
        AND m.status = 'ACTIVE'
        AND m.geohash IS NOT NULL
),
mainland_active_merchants AS (
    SELECT 
        COUNT(DISTINCT mb.merchant_id_nk) as total_merchants,
        COUNT(DISTINCT CASE WHEN f.date_id >= CAST(DATE_FORMAT(DATE_ADD('day', -7, CURRENT_DATE), '%Y%m%d') AS INTEGER) 
            AND f.booking_state_simple = 'COMPLETED' THEN f.merchant_id END) as active_7d,
        COUNT(DISTINCT CASE WHEN f.date_id >= CAST(DATE_FORMAT(DATE_ADD('day', -30, CURRENT_DATE), '%Y%m%d') AS INTEGER) 
            AND f.booking_state_simple = 'COMPLETED' THEN f.merchant_id END) as active_30d,
        COUNT(DISTINCT CASE WHEN f.date_id >= CAST(DATE_FORMAT(DATE_ADD('day', -90, CURRENT_DATE), '%Y%m%d') AS INTEGER) 
            AND f.booking_state_simple = 'COMPLETED' THEN f.merchant_id END) as active_90d
    FROM mainland_merchant_base mb
    LEFT JOIN ocd_adw.f_food_metrics f 
        ON mb.merchant_id_nk = f.merchant_id
        AND f.city_id = 13
        AND f.country_id = 1
        AND f.business_type = 0
        AND f.booking_state_simple = 'COMPLETED'
),
island_active_merchants AS (
    SELECT 
        COUNT(DISTINCT mb.merchant_id_nk) as total_merchants,
        COUNT(DISTINCT CASE WHEN f.date_id >= CAST(DATE_FORMAT(DATE_ADD('day', -7, CURRENT_DATE), '%Y%m%d') AS INTEGER) 
            AND f.booking_state_simple = 'COMPLETED' THEN f.merchant_id END) as active_7d,
        COUNT(DISTINCT CASE WHEN f.date_id >= CAST(DATE_FORMAT(DATE_ADD('day', -30, CURRENT_DATE), '%Y%m%d') AS INTEGER) 
            AND f.booking_state_simple = 'COMPLETED' THEN f.merchant_id END) as active_30d,
        COUNT(DISTINCT CASE WHEN f.date_id >= CAST(DATE_FORMAT(DATE_ADD('day', -90, CURRENT_DATE), '%Y%m%d') AS INTEGER) 
            AND f.booking_state_simple = 'COMPLETED' THEN f.merchant_id END) as active_90d
    FROM island_merchant_base mb
    LEFT JOIN ocd_adw.f_food_metrics f 
        ON mb.merchant_id_nk = f.merchant_id
        AND f.city_id = 13
        AND f.country_id = 1
        AND f.business_type = 0
        AND f.booking_state_simple = 'COMPLETED'
)
SELECT 
    'Mainland' as region,
    m.total_merchants,
    m.active_7d,
    m.active_30d,
    m.active_90d,
    CASE 
        WHEN m.total_merchants > 0 
        THEN ROUND((m.active_7d * 100.0 / m.total_merchants), 2)
        ELSE 0
    END as active_rate_7d_pct,
    CASE 
        WHEN m.total_merchants > 0 
        THEN ROUND((m.active_30d * 100.0 / m.total_merchants), 2)
        ELSE 0
    END as active_rate_30d_pct,
    CASE 
        WHEN m.total_merchants > 0 
        THEN ROUND((m.active_90d * 100.0 / m.total_merchants), 2)
        ELSE 0
    END as active_rate_90d_pct
FROM mainland_active_merchants m

UNION ALL

SELECT 
    'Island' as region,
    i.total_merchants,
    i.active_7d,
    i.active_30d,
    i.active_90d,
    CASE 
        WHEN i.total_merchants > 0 
        THEN ROUND((i.active_7d * 100.0 / i.total_merchants), 2)
        ELSE 0
    END as active_rate_7d_pct,
    CASE 
        WHEN i.total_merchants > 0 
        THEN ROUND((i.active_30d * 100.0 / i.total_merchants), 2)
        ELSE 0
    END as active_rate_30d_pct,
    CASE 
        WHEN i.total_merchants > 0 
        THEN ROUND((i.active_90d * 100.0 / i.total_merchants), 2)
        ELSE 0
    END as active_rate_90d_pct
FROM island_active_merchants i

ORDER BY region;


-- ============================================================================
-- QUERY 9: ACTIVE MERCHANT RATE - SIDE-BY-SIDE COMPARISON
-- ============================================================================
-- Insight: Direct comparison of Mainland vs Island active merchant rates
-- Shows the gap and opportunity for improvement
-- ============================================================================

WITH mainland_areas AS (
    SELECT DISTINCT area_id
    FROM ocd_adw.d_area
    WHERE city_id = 13
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
island_areas AS (
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
mainland_merchant_base AS (
    SELECT DISTINCT 
        m.merchant_id_nk
    FROM ocd_adw.d_merchant m
    INNER JOIN ocd_adw.d_area a 
        ON m.city_id = a.city_id 
        AND SUBSTRING(m.geohash, 1, 6) = SUBSTRING(a.geohash, 1, 6)
    INNER JOIN mainland_areas ma ON a.area_id = ma.area_id
    WHERE m.city_id = 13
        AND m.status = 'ACTIVE'
        AND m.geohash IS NOT NULL
),
island_merchant_base AS (
    SELECT DISTINCT 
        m.merchant_id_nk
    FROM ocd_adw.d_merchant m
    INNER JOIN ocd_adw.d_area a 
        ON m.city_id = a.city_id 
        AND SUBSTRING(m.geohash, 1, 6) = SUBSTRING(a.geohash, 1, 6)
    INNER JOIN island_areas ia ON a.area_id = ia.area_id
    WHERE m.city_id = 13
        AND m.status = 'ACTIVE'
        AND m.geohash IS NOT NULL
),
mainland_metrics AS (
    SELECT 
        COUNT(DISTINCT mb.merchant_id_nk) as total_merchants,
        COUNT(DISTINCT CASE WHEN f.date_id >= CAST(DATE_FORMAT(DATE_ADD('day', -7, CURRENT_DATE), '%Y%m%d') AS INTEGER) 
            AND f.booking_state_simple = 'COMPLETED' THEN f.merchant_id END) as active_7d,
        COUNT(DISTINCT CASE WHEN f.date_id >= CAST(DATE_FORMAT(DATE_ADD('day', -30, CURRENT_DATE), '%Y%m%d') AS INTEGER) 
            AND f.booking_state_simple = 'COMPLETED' THEN f.merchant_id END) as active_30d,
        COUNT(DISTINCT CASE WHEN f.date_id >= CAST(DATE_FORMAT(DATE_ADD('day', -90, CURRENT_DATE), '%Y%m%d') AS INTEGER) 
            AND f.booking_state_simple = 'COMPLETED' THEN f.merchant_id END) as active_90d
    FROM mainland_merchant_base mb
    LEFT JOIN ocd_adw.f_food_metrics f 
        ON mb.merchant_id_nk = f.merchant_id
        AND f.city_id = 13
        AND f.country_id = 1
        AND f.business_type = 0
        AND f.booking_state_simple = 'COMPLETED'
),
island_metrics AS (
    SELECT 
        COUNT(DISTINCT mb.merchant_id_nk) as total_merchants,
        COUNT(DISTINCT CASE WHEN f.date_id >= CAST(DATE_FORMAT(DATE_ADD('day', -7, CURRENT_DATE), '%Y%m%d') AS INTEGER) 
            AND f.booking_state_simple = 'COMPLETED' THEN f.merchant_id END) as active_7d,
        COUNT(DISTINCT CASE WHEN f.date_id >= CAST(DATE_FORMAT(DATE_ADD('day', -30, CURRENT_DATE), '%Y%m%d') AS INTEGER) 
            AND f.booking_state_simple = 'COMPLETED' THEN f.merchant_id END) as active_30d,
        COUNT(DISTINCT CASE WHEN f.date_id >= CAST(DATE_FORMAT(DATE_ADD('day', -90, CURRENT_DATE), '%Y%m%d') AS INTEGER) 
            AND f.booking_state_simple = 'COMPLETED' THEN f.merchant_id END) as active_90d
    FROM island_merchant_base mb
    LEFT JOIN ocd_adw.f_food_metrics f 
        ON mb.merchant_id_nk = f.merchant_id
        AND f.city_id = 13
        AND f.country_id = 1
        AND f.business_type = 0
        AND f.booking_state_simple = 'COMPLETED'
)
SELECT 
    'Total Active Merchants' as metric,
    m.total_merchants as mainland_value,
    i.total_merchants as island_value,
    (m.total_merchants - i.total_merchants) as difference,
    ROUND(((m.total_merchants - i.total_merchants) * 100.0 / NULLIF(i.total_merchants, 0)), 2) as mainland_vs_island_pct
FROM mainland_metrics m, island_metrics i

UNION ALL

SELECT 
    'Active Merchants (7D)' as metric,
    m.active_7d as mainland_value,
    i.active_7d as island_value,
    (m.active_7d - i.active_7d) as difference,
    ROUND(((m.active_7d - i.active_7d) * 100.0 / NULLIF(i.active_7d, 0)), 2) as mainland_vs_island_pct
FROM mainland_metrics m, island_metrics i

UNION ALL

SELECT 
    'Active Merchants (30D)' as metric,
    m.active_30d as mainland_value,
    i.active_30d as island_value,
    (m.active_30d - i.active_30d) as difference,
    ROUND(((m.active_30d - i.active_30d) * 100.0 / NULLIF(i.active_30d, 0)), 2) as mainland_vs_island_pct
FROM mainland_metrics m, island_metrics i

UNION ALL

SELECT 
    'Active Merchants (90D)' as metric,
    m.active_90d as mainland_value,
    i.active_90d as island_value,
    (m.active_90d - i.active_90d) as difference,
    ROUND(((m.active_90d - i.active_90d) * 100.0 / NULLIF(i.active_90d, 0)), 2) as mainland_vs_island_pct
FROM mainland_metrics m, island_metrics i

UNION ALL

SELECT 
    'Active Rate 7D (%)' as metric,
    ROUND((m.active_7d * 100.0 / NULLIF(m.total_merchants, 0)), 2) as mainland_value,
    ROUND((i.active_7d * 100.0 / NULLIF(i.total_merchants, 0)), 2) as island_value,
    ROUND((m.active_7d * 100.0 / NULLIF(m.total_merchants, 0)), 2) - 
    ROUND((i.active_7d * 100.0 / NULLIF(i.total_merchants, 0)), 2) as difference,
    ROUND(((ROUND((m.active_7d * 100.0 / NULLIF(m.total_merchants, 0)), 2) - 
           ROUND((i.active_7d * 100.0 / NULLIF(i.total_merchants, 0)), 2)) * 100.0 / 
          NULLIF(ROUND((i.active_7d * 100.0 / NULLIF(i.total_merchants, 0)), 2), 0)), 2) as mainland_vs_island_pct
FROM mainland_metrics m, island_metrics i

UNION ALL

SELECT 
    'Active Rate 30D (%)' as metric,
    ROUND((m.active_30d * 100.0 / NULLIF(m.total_merchants, 0)), 2) as mainland_value,
    ROUND((i.active_30d * 100.0 / NULLIF(i.total_merchants, 0)), 2) as island_value,
    ROUND((m.active_30d * 100.0 / NULLIF(m.total_merchants, 0)), 2) - 
    ROUND((i.active_30d * 100.0 / NULLIF(i.total_merchants, 0)), 2) as difference,
    ROUND(((ROUND((m.active_30d * 100.0 / NULLIF(m.total_merchants, 0)), 2) - 
           ROUND((i.active_30d * 100.0 / NULLIF(i.total_merchants, 0)), 2)) * 100.0 / 
          NULLIF(ROUND((i.active_30d * 100.0 / NULLIF(i.total_merchants, 0)), 2), 0)), 2) as mainland_vs_island_pct
FROM mainland_metrics m, island_metrics i

UNION ALL

SELECT 
    'Active Rate 90D (%)' as metric,
    ROUND((m.active_90d * 100.0 / NULLIF(m.total_merchants, 0)), 2) as mainland_value,
    ROUND((i.active_90d * 100.0 / NULLIF(i.total_merchants, 0)), 2) as island_value,
    ROUND((m.active_90d * 100.0 / NULLIF(m.total_merchants, 0)), 2) - 
    ROUND((i.active_90d * 100.0 / NULLIF(i.total_merchants, 0)), 2) as difference,
    ROUND(((ROUND((m.active_90d * 100.0 / NULLIF(m.total_merchants, 0)), 2) - 
           ROUND((i.active_90d * 100.0 / NULLIF(i.total_merchants, 0)), 2)) * 100.0 / 
          NULLIF(ROUND((i.active_90d * 100.0 / NULLIF(i.total_merchants, 0)), 2), 0)), 2) as mainland_vs_island_pct
FROM mainland_metrics m, island_metrics i

ORDER BY 
    CASE metric
        WHEN 'Total Active Merchants' THEN 1
        WHEN 'Active Merchants (7D)' THEN 2
        WHEN 'Active Merchants (30D)' THEN 3
        WHEN 'Active Merchants (90D)' THEN 4
        WHEN 'Active Rate 7D (%)' THEN 5
        WHEN 'Active Rate 30D (%)' THEN 6
        WHEN 'Active Rate 90D (%)' THEN 7
    END;


-- ============================================================================
-- SUMMARY INSIGHTS FOR REVIEW
-- ============================================================================
-- 
-- KEY FINDINGS FROM ANALYSIS:
--
-- 1. HALAL COVERAGE GAP (CRITICAL):
--    - Only 0.67% of merchants are Halal (159 out of 23,583)
--    - Many areas have ZERO Halal merchants (Bukit Minyak, Bukit Teh, etc.)
--    - Action: Priority Halal merchant acquisition in Butterworth, Bukit Minyak
--
-- 2. LUNCH MARKET DOMINANCE:
--    - 12-1 PM accounts for 19% of daily orders (highest volume)
--    - Mainland is NOT a supper market (10 PM - 2 AM = only 5.3%)
--    - Action: Target lunch merchants (11 AM - 2 PM operations)
--
-- 3. FAMILY MEAL STRATEGY VALIDATED:
--    - 41.8% of orders are 25+ MYR (family meal segment)
--    - 21.8% of orders are 40+ MYR (high-value segment)
--    - Action: Launch "Family Bundle" campaigns targeting 25-40 MYR segment
--
-- 4. ZERO OPERATIONAL BLOCKERS:
--    - 0% cancellation rate across all areas
--    - Infrastructure is ready for growth
--    - Action: No operational fixes needed - proceed with growth initiatives
--
-- 5. WIN-BACK OPPORTUNITIES:
--    - 500+ churned merchants identified
--    - Many with historical GMV > 10,000 MYR
--    - Action: Target top 100 dormant merchants for reactivation
--
-- 6. DELIVERY DISTANCE:
--    - Monitor areas with avg distance > 8km
--    - High delivery fees may be growth blocker
--    - Action: Review delivery fee structure for long-distance orders
--
-- 7. ACTIVE MERCHANT RATE (Mainland vs Island):
--    - Compare active merchant rates across different time periods (7D, 30D, 90D)
--    - Identifies if Mainland has lower utilization (opportunity for win-back)
--    - Action: If Mainland rate is lower, prioritize merchant reactivation campaigns
--
-- ============================================================================

