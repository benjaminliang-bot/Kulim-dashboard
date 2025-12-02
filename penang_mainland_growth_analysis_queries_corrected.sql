-- ============================================================================
-- PENANG MAINLAND GROWTH ANALYSIS - DATA EXTRACTION QUERIES (CORRECTED)
-- ============================================================================
-- Purpose: Extract granular data to identify hyper-growth opportunities
-- Location: Penang Mainland (city_id = 13, classified by MERCHANT LOCATION)
-- Date Range: Last 12 months (adjust date_id filters as needed)
-- 
-- IMPORTANT: Classification uses MERCHANT LOCATION (pickup), not dropoff location
-- This matches your GMV data structure
-- ============================================================================

-- ============================================================================
-- SHARED CTEs: Island/Mainland Merchant Classification
-- ============================================================================

WITH mainland_areas AS (
    -- Mainland areas based on QGIS classification
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
mainland_merchants AS (
    -- Mainland merchants (by merchant location)
    SELECT DISTINCT m.merchant_id_nk
    FROM ocd_adw.d_merchant m
    INNER JOIN ocd_adw.d_area a 
        ON m.city_id = a.city_id 
        AND SUBSTRING(m.geohash, 1, 6) = SUBSTRING(a.geohash, 1, 6)
    WHERE m.city_id = 13
        AND a.area_id IN (SELECT area_id FROM mainland_areas)
        AND m.geohash IS NOT NULL
),
island_merchants AS (
    -- Island merchants (by merchant location)
    SELECT DISTINCT m.merchant_id_nk
    FROM ocd_adw.d_merchant m
    INNER JOIN ocd_adw.d_area a 
        ON m.city_id = a.city_id 
        AND SUBSTRING(m.geohash, 1, 6) = SUBSTRING(a.geohash, 1, 6)
    WHERE m.city_id = 13
        AND a.area_id IN (SELECT area_id FROM island_areas)
        AND m.geohash IS NOT NULL
),

-- ============================================================================
-- QUERY 1: MERCHANT LIST WITH CUISINE & HALAL STATUS (Mainland Only)
-- ============================================================================

mainland_merchant_details AS (
    SELECT DISTINCT 
        m.merchant_id_nk,
        m.merchant_name,
        m.is_halal,
        m.primary_cuisine_id,
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
        AND m.geohash IS NOT NULL
)
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
FROM mainland_merchant_details
ORDER BY area_name, halal_status, merchant_name
LIMIT 10000;


-- ============================================================================
-- QUERY 2: HOURLY ORDER DISTRIBUTION (Island vs Mainland Comparison)
-- ============================================================================
-- NOTE: Using merchant location for classification

WITH mainland_merchants AS (
    SELECT DISTINCT m.merchant_id_nk
    FROM ocd_adw.d_merchant m
    INNER JOIN ocd_adw.d_area a 
        ON m.city_id = a.city_id 
        AND SUBSTRING(m.geohash, 1, 6) = SUBSTRING(a.geohash, 1, 6)
    WHERE m.city_id = 13
        AND a.area_id IN (
            SELECT area_id FROM ocd_adw.d_area
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
        AND m.geohash IS NOT NULL
),
island_merchants AS (
    SELECT DISTINCT m.merchant_id_nk
    FROM ocd_adw.d_merchant m
    INNER JOIN ocd_adw.d_area a 
        ON m.city_id = a.city_id 
        AND SUBSTRING(m.geohash, 1, 6) = SUBSTRING(a.geohash, 1, 6)
    WHERE m.city_id = 13
        AND a.area_id IN (
            SELECT area_id FROM ocd_adw.d_area
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
        )
        AND m.geohash IS NOT NULL
),
mainland_orders_by_hour AS (
    SELECT 
        f.hour_local,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END) as completed_orders,
        SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.gross_merchandise_value ELSE 0 END) as gmv,
        AVG(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.basket_size END) as avg_basket_size
    FROM ocd_adw.f_food_metrics f
    WHERE f.city_id = 13
        AND f.country_id = 1
        AND f.business_type = 0
        AND f.merchant_id IN (SELECT merchant_id_nk FROM mainland_merchants)
        AND f.date_id >= CAST(DATE_FORMAT(DATE_ADD('month', -12, CURRENT_DATE), '%Y%m%d') AS INTEGER)
    GROUP BY f.hour_local
),
island_orders_by_hour AS (
    SELECT 
        f.hour_local,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END) as completed_orders,
        SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.gross_merchandise_value ELSE 0 END) as gmv,
        AVG(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.basket_size END) as avg_basket_size
    FROM ocd_adw.f_food_metrics f
    WHERE f.city_id = 13
        AND f.country_id = 1
        AND f.business_type = 0
        AND f.merchant_id IN (SELECT merchant_id_nk FROM island_merchants)
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

