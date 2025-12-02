"""
Query Individual MGS Impact - Penang
Last 6 Months (May 2025 - October 2025)
Uses merchant IDs from segmentation mapping and Main Tracker V2
"""

import json

# Load segmentation mapping
print("Loading segmentation mapping...")
with open('penang_segmentation_mapping.json', 'r', encoding='utf-8') as f:
    segmentation_mapping = json.load(f)

# MGS names
mgs_names = ['Low Jia Ying', 'Teoh Jun Ling', 'Hon Yi Ni', 'Lee Sook Chin']

# Create MGS to merchant mapping from segmentation
mgs_merchants = {mgs: [] for mgs in mgs_names}

for merchant_id, seg_data in segmentation_mapping.items():
    mgs_name = seg_data.get('mgs', '').strip()
    if mgs_name in mgs_names:
        mgs_merchants[mgs_name].append(merchant_id)

print("\nMGS Merchant Counts (from segmentation mapping):")
for mgs, merchants in mgs_merchants.items():
    print(f"  {mgs}: {len(merchants)} merchants")

# Note: The user's list shows 494 merchants total:
# - Teoh Jun Ling: 179
# - Lee Sook Chin: 134
# - Low Jia Ying: 100
# - Hon Yi Ni: 81
# But segmentation mapping only has a few. We need to get merchant IDs from Main Tracker V2.

print("\n[INFO] Note: Segmentation mapping has limited merchants.")
print("       To get full impact, we need merchant IDs from Main Tracker V2 sheet.")
print("       For now, generating queries for available merchants...")

# Generate aggregated query for all MGSs
print("\nGenerating aggregated impact query...")

# Get all merchant IDs assigned to any MGS
all_mgs_merchant_ids = []
for merchants in mgs_merchants.values():
    all_mgs_merchant_ids.extend(merchants)

if all_mgs_merchant_ids:
    merchant_ids_sql = "', '".join(all_mgs_merchant_ids[:500])  # Limit for query size
    
    query = f"""
-- ============================================================================
-- ALL MGS IMPACT ANALYSIS - PENANG
-- Last 6 Months (May 2025 - October 2025)
-- Note: This uses merchants from segmentation mapping (limited coverage)
-- ============================================================================

WITH mgs_merchants AS (
    SELECT merchant_id_nk
    FROM (VALUES {', '.join([f"('{mid}')" for mid in all_mgs_merchant_ids[:500]])}) AS t(merchant_id_nk)
),
mgs_assignments AS (
    SELECT 
        CASE 
            WHEN seg.mgs = 'Low Jia Ying' THEN 'Low Jia Ying'
            WHEN seg.mgs = 'Teoh Jun Ling' THEN 'Teoh Jun Ling'
            WHEN seg.mgs = 'Hon Yi Ni' THEN 'Hon Yi Ni'
            WHEN seg.mgs = 'Lee Sook Chin' THEN 'Lee Sook Chin'
            ELSE 'Unknown'
        END as mgs_name,
        seg.merchant_id as merchant_id_nk
    FROM (VALUES {', '.join([f"('{mid}', '{segmentation_mapping[mid].get(\"mgs\", \"\")}')" for mid in all_mgs_merchant_ids[:500] if mid in segmentation_mapping])}) AS seg(merchant_id, mgs)
),
monthly_gmv_by_mgs AS (
    SELECT 
        CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER) as month_id,
        ma.mgs_name,
        COUNT(DISTINCT f.merchant_id) as unique_merchants,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END) as orders,
        COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.passenger_id END) as unique_eaters,
        SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.gross_merchandise_value ELSE 0 END) as gmv
    FROM ocd_adw.f_food_metrics f
    INNER JOIN mgs_assignments ma ON f.merchant_id = ma.merchant_id_nk
    WHERE f.city_id = 13
        AND f.country_id = 1
        AND f.date_id >= 20250501
        AND f.date_id < 20251101
        AND f.business_type = 0
    GROUP BY CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER), ma.mgs_name
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
    mg.mgs_name,
    mg.unique_merchants,
    mg.orders,
    mg.unique_eaters,
    mg.gmv,
    tp.total_penang_gmv,
    ROUND(mg.gmv * 100.0 / NULLIF(tp.total_penang_gmv, 0), 2) as gmv_pct_of_penang,
    ROUND(mg.gmv / NULLIF(mg.unique_merchants, 0), 2) as avg_gmv_per_merchant,
    ROUND(mg.gmv / NULLIF(mg.orders, 0), 2) as avg_gmv_per_order,
    ROUND(mg.gmv / NULLIF(mg.unique_eaters, 0), 2) as avg_gmv_per_eater
FROM monthly_gmv_by_mgs mg
INNER JOIN total_penang_gmv tp ON mg.month_id = tp.month_id
ORDER BY mg.month_id, mg.mgs_name;
"""
    
    with open('query_all_mgs_impact.sql', 'w', encoding='utf-8') as f:
        f.write(query)
    
    print(f"\n[OK] Generated query saved to: query_all_mgs_impact.sql")
    print(f"[WARNING] This query uses limited merchants from segmentation mapping")
    print(f"          To get full impact, we need all 494 merchant IDs from Main Tracker V2")

print("\n[INFO] Next Steps:")
print("   1. Read Main Tracker V2 sheet to get merchant IDs for all 494 MGS assignments")
print("   2. Update query with full merchant ID list")
print("   3. Execute query to get individual MGS impact metrics")


