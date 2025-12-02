"""
Execute all Mainland growth analysis queries and generate insights
"""

import json
from datetime import datetime

# Read the SQL file and extract queries
def extract_queries(sql_file):
    with open(sql_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by query markers
    queries = []
    query_sections = content.split('-- ============================================================================')
    
    query_names = [
        'QUERY 1: MERCHANT LIST',
        'QUERY 2: HOURLY ORDER DISTRIBUTION',
        'QUERY 3: BASKET SIZE DISTRIBUTION',
        'QUERY 4: OPERATIONAL FRICTION METRICS',
        'QUERY 5: CHURNED / INACTIVE MERCHANTS',
        'QUERY 6: DELIVERY DISTANCE ANALYSIS',
        'QUERY 7: FAILED SEARCHES'
    ]
    
    for i, section in enumerate(query_sections[1:], 1):  # Skip first empty section
        if i <= 7:  # We have 7 queries
            # Extract the SQL query (everything after the comment block)
            lines = section.split('\n')
            sql_start = False
            sql_lines = []
            
            for line in lines:
                # Skip comment lines at the start
                if line.strip().startswith('--') and not sql_start:
                    continue
                if line.strip() and not line.strip().startswith('--'):
                    sql_start = True
                if sql_start:
                    # Stop at next query marker or end
                    if 'QUERY' in line and 'QUERY' not in query_names[i-1] and i < 7:
                        break
                    sql_lines.append(line)
            
            query_sql = '\n'.join(sql_lines).strip()
            # Remove trailing comments
            if '/*' in query_sql:
                query_sql = query_sql.split('/*')[0].strip()
            
            if query_sql:
                queries.append({
                    'name': query_names[i-1] if i <= len(query_names) else f'Query {i}',
                    'sql': query_sql
                })
    
    return queries

if __name__ == '__main__':
    queries = extract_queries('penang_mainland_growth_analysis_queries.sql')
    print(f"Extracted {len(queries)} queries")
    for i, q in enumerate(queries, 1):
        print(f"\n{i}. {q['name']}")
        print(f"   SQL length: {len(q['sql'])} chars")
        print(f"   First 100 chars: {q['sql'][:100]}...")

