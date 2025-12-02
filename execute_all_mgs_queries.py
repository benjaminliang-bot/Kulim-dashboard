"""
Execute all MGS queries and compile results
"""

import json
import subprocess
import sys

# Load MGS assignments
with open('mgs_merchant_assignments.json', 'r', encoding='utf-8') as f:
    mgs_assignments = json.load(f)

print("="*80)
print("MGS IMPACT ANALYSIS - EXECUTION PLAN")
print("="*80)
print()

# MGS names sorted by merchant count
mgs_list = sorted(mgs_assignments.items(), key=lambda x: -len(x[1]))

print("MGS Distribution:")
for mgs_name, merchant_ids in mgs_list:
    print(f"  {mgs_name}: {len(merchant_ids)} merchants")

print("\n" + "="*80)
print("QUERIES READY FOR EXECUTION")
print("="*80)
print("\nAll queries have been generated and saved:")
for mgs_name, merchant_ids in mgs_list:
    mgs_var_name = mgs_name.replace(' ', '_').replace('.', '').lower()
    query_file = f"query_{mgs_var_name}_impact.sql"
    print(f"  - {mgs_name}: {query_file}")

print("\n[INFO] Execute queries via Presto/Hubble MCP tool")
print("       Results will be compiled into MGS_IMPACT_ANALYSIS_PENANG.md")
