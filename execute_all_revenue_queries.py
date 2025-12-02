"""
Execute all revenue breakdown queries and compile results
"""

import re
import sys
import io
import json

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def extract_queries_from_sql_file(filename):
    """Extract individual queries from SQL file"""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by query markers
    query_pattern = r'-- ============================================================================\n-- QUERY \d+: (.+?)\n-- ============================================================================\n\n(.*?)(?=\n\n-- ============================================================================\n-- QUERY|\Z)'
    matches = re.findall(query_pattern, content, re.DOTALL)
    
    queries = []
    for match in matches:
        query_name = match[0].strip()
        query_sql = match[1].strip()
        if query_sql and not query_sql.startswith('--'):
            queries.append((query_name, query_sql))
    
    return queries

# Extract queries
print("Extracting queries from SQL file...")
queries = extract_queries_from_sql_file('query_revenue_breakdown_executable.sql')

print(f"\nFound {len(queries)} queries:")
for i, (name, _) in enumerate(queries, 1):
    print(f"  {i}. {name}")

# Save queries to individual files for execution
print("\nSaving individual query files...")
for i, (name, query) in enumerate(queries, 1):
    safe_name = name.replace(':', '').replace(' ', '_').replace('/', '_')
    filename = f'query_revenue_{i}_{safe_name}.sql'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(query)
    print(f"  Saved: {filename}")

print("\n[INFO] Queries extracted and saved.")
print("[INFO] Ready to execute via Presto/Hubble MCP")
print("\n[NOTE] Due to query complexity, execute each query individually via:")
print("       mcp_mcp-grab-data_run_presto_query")

