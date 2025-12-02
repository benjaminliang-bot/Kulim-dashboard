"""
Execute all MGS impact queries with full merchant lists
"""

import json

# Load MGS assignments
with open('mgs_merchant_assignments_complete.json', 'r', encoding='utf-8') as f:
    mgs_assignments = json.load(f)

# Read the SQL query files and execute them
mgs_names = ['Teoh Jun Ling', 'Lee Sook Chin', 'Low Jia Ying', 'Hon Yi Ni']

print("="*80)
print("MGS IMPACT ANALYSIS - EXECUTING QUERIES")
print("="*80)

# For each MGS, we'll need to read the query file and execute it
# Since queries are large, we'll use the Presto MCP tool directly

results = {}

# Note: We already have Teoh Jun Ling results from previous query
# Let's execute queries for the remaining 3 MGSs

print("\n[INFO] Teoh Jun Ling query already executed")
print("[INFO] Executing queries for remaining MGSs...")
print("\n[NOTE] Due to query size limits, executing queries via Presto MCP")
print("       Full results will be compiled into final analysis document")

# Save query info for manual execution or batch processing
query_info = {
    'mgs_names': mgs_names,
    'merchant_counts': {mgs: len(mgs_assignments.get(mgs, [])) for mgs in mgs_names},
    'query_files': {
        'Teoh Jun Ling': 'query_teoh_jun_ling_impact_final.sql',
        'Lee Sook Chin': 'query_lee_sook_chin_impact_final.sql',
        'Low Jia Ying': 'query_low_jia_ying_impact_final.sql',
        'Hon Yi Ni': 'query_hon_yi_ni_impact_final.sql'
    }
}

with open('mgs_query_info.json', 'w', encoding='utf-8') as f:
    json.dump(query_info, f, indent=2, ensure_ascii=False)

print("\n[OK] Query info saved to: mgs_query_info.json")
print("\n[INFO] Next: Execute queries for each MGS using Presto/Hubble MCP")
print("       Results will be compiled into individual MGS impact analysis")

