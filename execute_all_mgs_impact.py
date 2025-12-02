"""
Execute All MGS Impact Queries
Query individual impact for each MGS using all merchant IDs
"""

import json

# Load MGS assignments
with open('mgs_merchant_assignments.json', 'r', encoding='utf-8') as f:
    mgs_assignments = json.load(f)

print("="*80)
print("EXECUTING ALL MGS IMPACT QUERIES")
print("="*80)
print()

# MGS names sorted by merchant count
mgs_list = sorted(mgs_assignments.items(), key=lambda x: -len(x[1]))

# For each MGS, we'll create a query with all merchant IDs
# Since some have many merchants, we'll use a VALUES clause approach
# For very large lists, we might need to batch, but let's try with all first

all_results = {}

for mgs_name, merchant_ids in mgs_list:
    merchant_ids_clean = [mid.strip() for mid in merchant_ids if mid.strip()]
    
    if not merchant_ids_clean:
        continue
    
    print(f"Processing {mgs_name} ({len(merchant_ids_clean)} merchants)...")
    
    # Create VALUES clause - we'll use all merchant IDs
    # For large lists, we'll create the query in chunks if needed
    values_clause = ', '.join([f"('{mid}')" for mid in merchant_ids_clean])
    mgs_var_name = mgs_name.replace(' ', '_').replace('.', '').lower()
    
    query = f"""
WITH {mgs_var_name}_merchants AS (
    SELECT merchant_id_nk
    FROM (VALUES {values_clause}) AS t(merchant_id_nk)
),
monthly_gmv AS (
    SELECT 
        CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER) as month_id,
        COUNT(DISTINCT f.merchant_id) as unique_merchants,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END) as orders,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.passenger_id END) as unique_eaters,
        SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.gross_merchandise_value ELSE 0 END) as gmv
    FROM ocd_adw.f_food_metrics f
    WHERE f.city_id = 13
        AND f.country_id = 1
        AND f.date_id >= 20250501
        AND f.date_id < 20251101
        AND f.business_type = 0
        AND f.merchant_id IN (SELECT merchant_id_nk FROM {mgs_var_name}_merchants)
    GROUP BY CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER)
),
total_penang_gmv AS (
    SELECT 
        CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER) as month_id,
        SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.gross_merchandise_value ELSE 0 END) as total_penang_gmv
    FROM ocd_adw.f_food_metrics f
    WHERE f.city_id = 13
        AND f.country_id = 1
        AND f.date_id >= 20250501
        AND f.date_id < 20251101
        AND f.business_type = 0
    GROUP BY CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER)
)
SELECT 
    mg.month_id,
    '{mgs_name}' as mgs_name,
    mg.unique_merchants,
    mg.orders,
    mg.unique_eaters,
    mg.gmv,
    tp.total_penang_gmv,
    ROUND(mg.gmv * 100.0 / NULLIF(tp.total_penang_gmv, 0), 2) as gmv_pct_of_penang,
    ROUND(mg.gmv / NULLIF(mg.unique_merchants, 0), 2) as avg_gmv_per_merchant,
    ROUND(mg.gmv / NULLIF(mg.orders, 0), 2) as avg_gmv_per_order,
    ROUND(mg.gmv / NULLIF(mg.unique_eaters, 0), 2) as avg_gmv_per_eater
FROM monthly_gmv mg
INNER JOIN total_penang_gmv tp ON mg.month_id = tp.month_id
ORDER BY mg.month_id;
"""
    
    # Save query to file
    query_file = f"query_{mgs_var_name}_impact.sql"
    with open(query_file, 'w', encoding='utf-8') as f:
        f.write(query)
    
    print(f"  Saved query to: {query_file}")
    print(f"  Query ready for execution (contains {len(merchant_ids_clean)} merchant IDs)")

print("\n[OK] All queries generated and saved")
print("[INFO] Ready to execute queries via Presto/Hubble")
print("\n[INFO] Note: Queries contain all merchant IDs for each MGS")
print("       For Teoh Jun Ling (576 merchants), query may be large but should work")


