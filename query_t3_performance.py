"""
Query T3 merchant performance for October 2025 vs October 2024
Using all 197 T3 merchant IDs from Main Tracker V2
"""

import json
from datetime import datetime

# Load T3 merchant IDs
with open('t3_merchant_ids.json', 'r') as f:
    t3_merchant_ids = json.load(f)

print("="*80)
print("T3 PERFORMANCE QUERY SETUP")
print("="*80)
print(f"Total T3 merchants: {len(t3_merchant_ids)}")
print(f"Sample IDs: {t3_merchant_ids[:5]}")
print()
print("Query Parameters:")
print("  - Metric: merchant_gross_merchandise_value")
print("  - City: Penang (city_id = 13)")
print("  - Period 1: October 2025 (2025-10-01 to 2025-10-31)")
print("  - Period 2: October 2024 (2024-10-01 to 2024-10-31)")
print("  - Filter: merchant_id_nk IN (197 T3 merchant IDs)")
print()
print("Note: This query needs to be executed via Midas/Hubble with merchant filters")
print("Due to the large number of merchant IDs, we may need to:")
print("  1. Query in batches, or")
print("  2. Use a subquery/join approach, or")
print("  3. Filter by a segmentation field if T3 is stored in d_merchant")


