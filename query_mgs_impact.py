"""
Query Individual MGS Impact - Penang
Last 6 Months (May 2025 - October 2025)
"""

import json

# MGS names
mgs_names = ['Low Jia Ying', 'Teoh Jun Ling', 'Hon Yi Ni', 'Lee Sook Chin']

# Load segmentation mapping to get merchant-to-MGS assignments
print("Loading segmentation mapping...")
with open('penang_segmentation_mapping.json', 'r', encoding='utf-8') as f:
    segmentation_mapping = json.load(f)

# Create MGS to merchant mapping
mgs_merchants = {mgs: [] for mgs in mgs_names}

for merchant_id, seg_data in segmentation_mapping.items():
    mgs_name = seg_data.get('mgs', '').strip()
    if mgs_name in mgs_names:
        mgs_merchants[mgs_name].append(merchant_id)

print("\nMGS Merchant Counts:")
for mgs, merchants in mgs_merchants.items():
    print(f"  {mgs}: {len(merchants)} merchants")

# Generate SQL query for each MGS
print("\nGenerating SQL queries...")

# Create merchant ID lists for SQL
queries = []
for mgs_name, merchant_ids in mgs_merchants.items():
    if not merchant_ids:
        continue
    
    # Create SQL IN clause (limit to first 1000 for query size)
    merchant_ids_sample = merchant_ids[:1000]
    merchant_ids_sql = "', '".join(merchant_ids_sample)
    
    query = f"""
-- ============================================================================
-- {mgs_name} - Individual Impact Analysis
-- Last 6 Months (May 2025 - October 2025)
-- ============================================================================

WITH {mgs_name.replace(' ', '_').lower()}_merchants AS (
    SELECT merchant_id_nk
    FROM (VALUES {', '.join([f"('{mid}')" for mid in merchant_ids_sample])}) AS t(merchant_id_nk)
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
        AND f.merchant_id IN (SELECT merchant_id_nk FROM {mgs_name.replace(' ', '_').lower()}_merchants)
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
    queries.append((mgs_name, query, len(merchant_ids)))

# Save queries
with open('query_mgs_impact.sql', 'w', encoding='utf-8') as f:
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

print(f"\n[OK] Generated SQL queries saved to: query_mgs_impact.sql")
print(f"\n[INFO] MGS Summary:")
for mgs_name, _, merchant_count in queries:
    print(f"   {mgs_name}: {merchant_count} merchants")

print("\n[WARNING] Note: Queries use sample of up to 1000 merchants per MGS")
print("          To use all merchants, update the merchant_ids_sample limit")


