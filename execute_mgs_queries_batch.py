"""
Execute MGS Impact Queries in Batches
Read merchant IDs and execute queries via Presto
"""

import json
from mcp import mcp_hubble_run_presto_query

# Load MGS assignments
with open('mgs_merchant_assignments.json', 'r', encoding='utf-8') as f:
    mgs_assignments = json.load(f)

# MGS names sorted by merchant count (smallest first for testing)
mgs_list = sorted(mgs_assignments.items(), key=lambda x: len(x[1]))

print("="*80)
print("EXECUTING MGS IMPACT QUERIES")
print("="*80)
print()

all_results = {}

for mgs_name, merchant_ids in mgs_list:
    merchant_ids_clean = [mid.strip() for mid in merchant_ids if mid.strip()]
    
    if not merchant_ids_clean:
        continue
    
    print(f"\n{'='*80}")
    print(f"Querying {mgs_name} ({len(merchant_ids_clean)} merchants)...")
    print(f"{'='*80}")
    
    # Create VALUES clause
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
    
    # Save query for reference
    query_file = f"query_{mgs_var_name}_impact_exec.sql"
    with open(query_file, 'w', encoding='utf-8') as f:
        f.write(query)
    
    print(f"Query saved to: {query_file}")
    print(f"Ready to execute...")
    
    # Note: Actual execution would be done via MCP tool
    # For now, we'll save the queries and note that they need to be executed
    all_results[mgs_name] = {
        'merchant_count': len(merchant_ids_clean),
        'query_file': query_file
    }

print("\n" + "="*80)
print("SUMMARY")
print("="*80)
for mgs_name, info in all_results.items():
    print(f"{mgs_name}: {info['merchant_count']} merchants - Query: {info['query_file']}")

print("\n[INFO] All queries generated. Execute them via Presto/Hubble MCP tool.")


