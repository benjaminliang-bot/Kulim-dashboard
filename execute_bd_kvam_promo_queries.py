"""
Execute BD, KVAM, and SD Promo Code Analysis Queries
"""

import json

# Load merchant IDs
with open('t20_merchant_ids.json', 'r') as f:
    t20_merchant_ids = json.load(f)

# SD Promo Codes
sd_promo_codes = [
    'Voucher', 'Hairstory', 'GPFF5', 'PSDC5', 'SMEC', 'INNPLX', 'GBSMH', 'GBSMY', 
    'GBSEA', 'GBTECH', 'GPDC', 'TARPNG', 'PSULA', 'UOWPG', 'BDOPG', 'WOUPG', 
    'QBPG2', 'PERKESO', 'INFINITY8PG', 'O2PG', 'TUG20', 'PRITECH', 'MALVEST', 
    'ART20', 'PENTA', 'MBPP20', 'GSDL', 'GIMM20', 'JAZZ20', 'QANOVA', 'ICONIC', 
    'IQI20', 'SHERYN', 'RFS20', 'CTG20', 'HOSPRAI', 'AKV2', 'UNITAR2', 'UITM', 
    'MEA20', 'LCOPG', 'IHOS', 'MAINPG', 'ORANGE', 'XILNEX', 'GWM2', 'BELL20', 
    'KAMI20', 'E2P', 'ASPEN'
]

# Create merchant ID list for SQL IN clause (first 100 for testing, then we can expand)
merchant_ids_sample = t20_merchant_ids[:100]
merchant_ids_sql = "', '".join(merchant_ids_sample)

# Create promo code list for SQL IN clause
promo_codes_sql = "', '".join(sd_promo_codes)

print("="*80)
print("EXECUTING BD, KVAM, AND SD PROMO CODE ANALYSIS")
print("="*80)
print(f"Using {len(merchant_ids_sample)} T20/T3 merchant IDs (sample)")
print(f"Using {len(sd_promo_codes)} SD promo codes")
print()

# QUESTION 1: BD GMV % Trends
bd_query = f"""
WITH t20_t3_merchants AS (
    SELECT merchant_id_nk
    FROM (VALUES {', '.join([f"('{mid}')" for mid in merchant_ids_sample])}) AS t(merchant_id_nk)
),
bd_merchants AS (
    SELECT DISTINCT merchant_id_nk
    FROM ocd_adw.d_merchant
    WHERE city_id = 13
        AND (is_bd_account = TRUE OR is_bd_partner = TRUE)
),
monthly_gmv AS (
    SELECT 
        CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER) as month_id,
        SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.gross_merchandise_value ELSE 0 END) as total_penang_gmv,
        SUM(CASE 
            WHEN f.booking_state_simple = 'COMPLETED' 
            AND f.merchant_id IN (SELECT merchant_id_nk FROM bd_merchants)
            THEN f.gross_merchandise_value 
            ELSE 0 
        END) as bd_gmv,
        SUM(CASE 
            WHEN f.booking_state_simple = 'COMPLETED' 
            AND f.merchant_id IN (SELECT merchant_id_nk FROM t20_t3_merchants)
            THEN f.gross_merchandise_value 
            ELSE 0 
        END) as t20_t3_gmv,
        SUM(CASE 
            WHEN f.booking_state_simple = 'COMPLETED' 
            AND f.merchant_id IN (SELECT merchant_id_nk FROM bd_merchants)
            AND f.merchant_id IN (SELECT merchant_id_nk FROM t20_t3_merchants)
            THEN f.gross_merchandise_value 
            ELSE 0 
        END) as bd_t20_t3_gmv
    FROM ocd_adw.f_food_metrics f
    WHERE f.city_id = 13
        AND f.country_id = 1
        AND f.date_id >= 20250501
        AND f.date_id < 20251101
        AND f.business_type = 0
    GROUP BY CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER)
)
SELECT 
    month_id,
    total_penang_gmv,
    bd_gmv,
    t20_t3_gmv,
    bd_t20_t3_gmv,
    ROUND(bd_gmv * 100.0 / NULLIF(total_penang_gmv, 0), 2) as bd_gmv_pct,
    ROUND(t20_t3_gmv * 100.0 / NULLIF(total_penang_gmv, 0), 2) as t20_t3_gmv_pct,
    ROUND(bd_t20_t3_gmv * 100.0 / NULLIF(total_penang_gmv, 0), 2) as bd_t20_t3_overlap_pct,
    LAG(bd_gmv * 100.0 / NULLIF(total_penang_gmv, 0)) OVER (ORDER BY month_id) as prev_bd_gmv_pct,
    ROUND((bd_gmv * 100.0 / NULLIF(total_penang_gmv, 0)) - 
          LAG(bd_gmv * 100.0 / NULLIF(total_penang_gmv, 0)) OVER (ORDER BY month_id), 2) as bd_gmv_pct_change
FROM monthly_gmv
ORDER BY month_id;
"""

print("Executing Question 1: BD GMV % Trends...")
print("Query saved - ready to execute via Presto/Hubble")
print()

# Save queries to file for execution
with open('execute_bd_kvam_promo_queries.sql', 'w', encoding='utf-8') as f:
    f.write("-- QUESTION 1: BD GMV % TRENDS\n")
    f.write(bd_query)
    f.write("\n\n")

print("[OK] Queries prepared and saved to: execute_bd_kvam_promo_queries.sql")
print("[INFO] Note: Using sample of 100 T20/T3 merchants for testing")
print("[INFO] To use all merchants, update merchant_ids_sample to use all t20_merchant_ids")


