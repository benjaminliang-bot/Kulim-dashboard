-- Full SQL Query: Penang Mainland Merchants with Readable Cuisine Names
-- This query returns all active merchants from Mainland areas with human-readable cuisine names

WITH mainland_areas AS (
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
        CASE 
            WHEN m.is_halal = TRUE THEN 'Halal'
            WHEN m.is_halal = FALSE THEN 'Non-Halal'
            ELSE 'Unknown'
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

