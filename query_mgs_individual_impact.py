"""
Query Individual MGS Impact - Penang
Last 6 Months (May 2025 - October 2025)
"""

import json

# Load MGS assignments
print("Loading MGS assignments...")
with open('mgs_merchant_assignments.json', 'r', encoding='utf-8') as f:
    mgs_assignments = json.load(f)

print("\nMGS Merchant Counts:")
for mgs, merchants in sorted(mgs_assignments.items(), key=lambda x: -len(x[1])):
    print(f"  {mgs}: {len(merchants)} merchants")

# Generate queries for each MGS
print("\nGenerating impact queries...")

# For large merchant lists, we'll use subqueries or batch approach
# Let's create queries that can handle all merchants

queries = []

for mgs_name, merchant_ids in sorted(mgs_assignments.items(), key=lambda x: -len(x[1])):
    # Create merchant ID list for SQL
    # For very large lists, we'll use a VALUES clause or subquery
    merchant_ids_clean = [mid.strip() for mid in merchant_ids if mid.strip()]
    
    if not merchant_ids_clean:
        continue
    
    # Create VALUES clause (limit to 1000 for query size, but we can batch if needed)
    # Actually, let's use a subquery approach with d_merchant to handle all merchants
    query = f"""
-- ============================================================================
-- {mgs_name} - Individual Impact Analysis
-- Last 6 Months (May 2025 - October 2025)
-- {len(merchant_ids_clean)} merchants
-- ============================================================================

WITH {mgs_name.replace(' ', '_').replace('.', '').lower()}_merchants AS (
    SELECT merchant_id_nk
    FROM (VALUES {', '.join([f"('{mid}')" for mid in merchant_ids_clean[:1000]])}) AS t(merchant_id_nk)
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
        AND f.merchant_id IN (SELECT merchant_id_nk FROM {mgs_name.replace(' ', '_').replace('.', '').lower()}_merchants)
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
    
    queries.append((mgs_name, query, len(merchant_ids_clean)))

# Save queries
with open('query_mgs_individual_impact.sql', 'w', encoding='utf-8') as f:
    f.write("-- ============================================================================\n")
    f.write("-- MGS INDIVIDUAL IMPACT ANALYSIS - PENANG\n")
    f.write("-- Last 6 Months (May 2025 - October 2025)\n")
    f.write("-- ============================================================================\n\n")
    
    for mgs_name, query, merchant_count in queries:
        f.write(f"\n{'='*80}\n")
        f.write(f"MGS: {mgs_name} ({merchant_count} merchants)\n")
        f.write(f"{'='*80}\n\n")
        f.write(query)
        f.write("\n\n")

print(f"\n[OK] Generated SQL queries saved to: query_mgs_individual_impact.sql")
print(f"\n[INFO] Note: Queries use up to 1000 merchants per MGS")
print(f"       For MGS with >1000 merchants, queries may need batching")

# Now let's execute the queries
print("\n[INFO] Executing queries to get impact metrics...")
