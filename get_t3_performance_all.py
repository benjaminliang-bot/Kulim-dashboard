"""
Query T3 merchant performance for all 197 merchants
October 2025 vs October 2024
"""

import json
from datetime import datetime

# Load T3 merchant IDs
with open('t3_merchant_ids.json', 'r') as f:
    all_t3_ids = json.load(f)

print("="*80)
print("T3 PERFORMANCE QUERY - ALL 197 MERCHANTS")
print("="*80)
print(f"Total T3 merchants: {len(all_t3_ids)}")
print()

# Sample data from Midas queries (first 10 merchants)
oct_2025_sample = {
    '1-C25GT2E1KFTTDA': 90236.89,
    '1-C26CLN3TRNTHAA': 137053.35,
    '1-C6WWEPKBGEJCEN': 86397.47,
    '1-CZE3J8NERT63CT': 180946.57,
    '1-C3JAAVKVPGEYE6': 90404.94,
    '1-CYWCBE4HKBCXGA': 87895.81,
    '1-CYVTL4D3VTJZAN': 90774.69,
    '1-C6JYWF3UDB5ACT': 97672.16,
    '1-C4L2UA4VGJWDCJ': 87323.98,
    '1-CY5FNLDVJ2VKJE': 93564.22
}

oct_2024_sample = {
    '1-CZE3J8NERT63CT': 94446.74,
    '1-CYVTL4D3VTJZAN': 117629.53,
    '1-C3JAAVKVPGEYE6': 84679.29,
    '1-C26CLN3TRNTHAA': 61689.86,
    '1-C6WWEPKBGEJCEN': 14446.30,
    '1-C25GT2E1KFTTDA': 74885.50,
    '1-CY5FNLDVJ2VKJE': 47355.79,
    '1-CYWCBE4HKBCXGA': 47843.04,
    '1-C4L2UA4VGJWDCJ': 55915.35,
    '1-C6JYWF3UDB5ACT': 40830.31
}

# Calculate sample summary
sample_merchants = set(oct_2025_sample.keys()) & set(oct_2024_sample.keys())
gmv_2025 = sum(oct_2025_sample[m] for m in sample_merchants)
gmv_2024 = sum(oct_2024_sample[m] for m in sample_merchants)
growth_pct = ((gmv_2025 - gmv_2024) / gmv_2024 * 100) if gmv_2024 > 0 else 0

print("SAMPLE RESULTS (10 merchants):")
print(f"  October 2025 GMV: RM {gmv_2025:,.2f}")
print(f"  October 2024 GMV: RM {gmv_2024:,.2f}")
print(f"  YoY Growth: {growth_pct:+.2f}%")
print()

print("="*80)
print("FULL QUERY INSTRUCTIONS")
print("="*80)
print()
print("To get complete T3 performance for all 197 merchants:")
print()
print("1. Query October 2025:")
print("   - Metric: merchant_gross_merchandise_value")
print("   - Dimensions: ['city_name', 'merchant_id_nk']")
print("   - Date: 2025-10-01 to 2025-11-01")
print("   - Filter: city_name = 'Penang' AND merchant_id_nk IN (all 197 IDs)")
print()
print("2. Query October 2024:")
print("   - Same parameters, date: 2024-10-01 to 2024-11-01")
print()
print("3. Aggregate and calculate:")
print("   - Sum GMV for each period")
print("   - Calculate YoY growth %")
print("   - Count active merchants in each period")
print()
print("Note: Due to query limits, you may need to:")
print("  - Query in batches of 50-100 merchants")
print("  - Or use a SQL query via Hubble with all merchant IDs")
print()

# Save query structure
query_structure = {
    'total_t3_merchants': len(all_t3_ids),
    'sample_size': len(sample_merchants),
    'sample_gmv_2025': gmv_2025,
    'sample_gmv_2024': gmv_2024,
    'sample_growth_pct': growth_pct,
    'merchant_ids': all_t3_ids
}

with open('t3_performance_query_structure.json', 'w', encoding='utf-8') as f:
    json.dump(query_structure, f, indent=2)

print("Query structure saved to: t3_performance_query_structure.json")


