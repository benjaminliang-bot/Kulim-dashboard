import pandas as pd
import numpy as np

print("REVISED TEAM COMMISSION ANALYSIS WITH MONTHLY AM MAPPING")
print("="*70)
print("Using monthly AM mapping for Darren, CY, and Suki")
print("EK and XR remain based on tracker file (MGS and NMA)")
print()

# This will be done via SQL query that joins with the monthly mapping table
# Let me create the SQL query

sql_query = """
-- Revised calculation using monthly AM mapping for Darren, CY, and Suki
WITH monthly_am_mapping AS (
    -- Get monthly AM assignments for Darren, CY, and Suki
    SELECT DISTINCT
        m.merchant_id,
        DATE_TRUNC('month', m.date_local) as month_date,
        CAST(TO_CHAR(DATE_TRUNC('month', m.date_local), 'YYYYMM') AS INTEGER) as month_id,
        CASE 
            WHEN m.am_name LIKE '%chiayee.leong%' THEN 'CY'
            WHEN m.am_name LIKE '%darren.ng%' THEN 'Darren'
            WHEN m.am_name LIKE '%suki.teoh%' THEN 'Suki'
        END as owner
    FROM slide_mex_analytics_mnpi.ami_ace_am_mapping m
    INNER JOIN ocd_adw.d_merchant dm ON m.merchant_id = dm.merchant_id_nk
    WHERE dm.city_id = 13  -- Penang
        AND m.date_local >= DATE '2025-01-01'
        AND m.date_local < DATE '2025-11-01'
        AND (
            m.am_name LIKE '%chiayee.leong%'
            OR m.am_name LIKE '%darren.ng%'
            OR m.am_name LIKE '%suki.teoh%'
        )
),
-- EK and XR from tracker (static assignment)
tracker_assignments AS (
    -- This would need to be loaded from the tracker file
    -- For now, we'll handle EK and XR separately in the main query
    SELECT merchant_id_nk, 'EK' as owner FROM (VALUES ('dummy')) t WHERE 1=0
    UNION ALL
    SELECT merchant_id_nk, 'XR' as owner FROM (VALUES ('dummy')) t WHERE 1=0
),
-- Get merchant-level GMV and commission
monthly_merchant_gmv AS (
    SELECT 
        CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER) as month_id,
        f.merchant_id as merchant_id_nk,
        SUM(CASE 
            WHEN f.booking_state_simple = 'COMPLETED' 
            THEN COALESCE(f.gross_merchandise_value, 0) 
            ELSE 0 
        END) as merchant_gmv,
        SUM(CASE 
            WHEN f.booking_state_simple = 'COMPLETED' 
            THEN COALESCE(f.commission_from_merchant, 0) 
            ELSE 0 
        END) as merchant_commission_billing
    FROM ocd_adw.f_food_metrics f
    WHERE f.city_id = 13
        AND f.country_id = 1
        AND f.business_type = 0
        AND f.date_id >= 20250101
        AND f.date_id < 20251101
    GROUP BY CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER), f.merchant_id
),
-- Assign owners using monthly mapping for Darren/CY/Suki
merchant_with_owner AS (
    SELECT 
        mmg.month_id,
        mmg.merchant_id_nk,
        mmg.merchant_gmv,
        mmg.merchant_commission_billing,
        COALESCE(mam.owner, NULL) as owner  -- From monthly mapping
    FROM monthly_merchant_gmv mmg
    LEFT JOIN monthly_am_mapping mam 
        ON mmg.merchant_id_nk = mam.merchant_id 
        AND mmg.month_id = mam.month_id
),
monthly_total_penang_gmv AS (
    SELECT 
        CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER) as month_id,
        SUM(CASE 
            WHEN f.booking_state_simple = 'COMPLETED' 
            THEN COALESCE(f.gross_merchandise_value, 0) 
            ELSE 0 
        END) as total_penang_gmv
    FROM ocd_adw.f_food_metrics f
    WHERE f.city_id = 13
        AND f.country_id = 1
        AND f.business_type = 0
        AND f.date_id >= 20250101
        AND f.date_id < 20251101
    GROUP BY CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER)
)
SELECT 
    mwo.month_id,
    mwo.owner,
    SUM(mwo.merchant_gmv) as team_gmv,
    SUM(mwo.merchant_commission_billing) as team_commission_billing,
    MAX(mtp.total_penang_gmv) as total_penang_gmv,
    ROUND(SUM(mwo.merchant_gmv) * 100.0 / NULLIF(MAX(mtp.total_penang_gmv), 0), 2) as gmv_pct_of_penang,
    ROUND(SUM(mwo.merchant_commission_billing) * 100.0 / NULLIF(SUM(mwo.merchant_gmv), 0), 4) as commission_rate_pct
FROM merchant_with_owner mwo
INNER JOIN monthly_total_penang_gmv mtp ON mwo.month_id = mtp.month_id
WHERE mwo.owner IN ('CY', 'Darren', 'Suki')
GROUP BY mwo.month_id, mwo.owner
ORDER BY mwo.month_id, mwo.owner
"""

print("SQL Query created. Now executing...")
print("Note: EK and XR will be calculated separately using tracker file")

