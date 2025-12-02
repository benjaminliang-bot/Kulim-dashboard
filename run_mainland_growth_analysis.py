"""
Penang Mainland Growth Analysis - Execute All Queries and Generate Insights

This script:
1. Extracts all queries from penang_mainland_growth_analysis_queries.sql
2. Executes each query via MCP tool
3. Generates actionable insights for Mainland growth strategy
"""

import re
import json
from typing import List, Dict, Any, Optional
from datetime import datetime

# Query extraction function
def extract_queries_from_sql_file(filename: str) -> List[Dict[str, str]]:
    """
    Extract individual queries from SQL file.
    Returns list of dicts with 'name', 'description', and 'query' keys.
    """
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    queries = []
    
    # Split by query separators
    query_sections = re.split(r'-- =+.*?QUERY \d+:', content)
    
    for section in query_sections[1:]:  # Skip header
        # Extract query name and description
        lines = section.split('\n')
        name_line = None
        desc_lines = []
        query_start = None
        
        for i, line in enumerate(lines):
            if 'QUERY' in line and ':' in line:
                name_line = line.split(':', 1)[1].strip()
            elif line.strip().startswith('--') and 'Data Point' in line:
                desc_lines.append(line.replace('--', '').strip())
            elif line.strip().startswith('--') and 'Insight' in line:
                desc_lines.append(line.replace('--', '').strip())
            elif not line.strip().startswith('--') and line.strip() and query_start is None:
                query_start = i
                break
        
        if query_start is not None:
            query_text = '\n'.join(lines[query_start:]).strip()
            # Remove trailing comments
            query_text = re.sub(r'--.*$', '', query_text, flags=re.MULTILINE)
            query_text = query_text.strip()
            
            if query_text and query_text != '':
                queries.append({
                    'name': name_line or 'Unknown Query',
                    'description': ' | '.join(desc_lines) if desc_lines else '',
                    'query': query_text
                })
    
    return queries

# Alternative: Extract queries by pattern matching
def extract_queries_alternative(filename: str) -> List[Dict[str, str]]:
    """Extract queries using pattern matching for the specific SQL file structure."""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    queries = []
    
    # Define query patterns
    query_patterns = [
        {
            'name': 'Query 1: Merchant List with Cuisine & Halal Status',
            'start': '-- ============================================================================\n-- QUERY 1: MERCHANT LIST',
            'end': '-- ============================================================================\n-- QUERY 2:'
        },
        {
            'name': 'Query 2: Hourly Order Distribution',
            'start': '-- ============================================================================\n-- QUERY 2: HOURLY ORDER DISTRIBUTION',
            'end': '-- ============================================================================\n-- QUERY 3:'
        },
        {
            'name': 'Query 3: Basket Size Distribution',
            'start': '-- ============================================================================\n-- QUERY 3: BASKET SIZE DISTRIBUTION',
            'end': '-- ============================================================================\n-- QUERY 4:'
        },
        {
            'name': 'Query 4: Operational Friction Metrics',
            'start': '-- ============================================================================\n-- QUERY 4: OPERATIONAL FRICTION METRICS',
            'end': '-- ============================================================================\n-- QUERY 5:'
        },
        {
            'name': 'Query 5: Churned / Inactive Merchants',
            'start': '-- ============================================================================\n-- QUERY 5: CHURNED / INACTIVE MERCHANTS',
            'end': '-- ============================================================================\n-- QUERY 6:'
        },
        {
            'name': 'Query 6: Delivery Distance Analysis',
            'start': '-- ============================================================================\n-- QUERY 6: DELIVERY DISTANCE ANALYSIS',
            'end': '-- ============================================================================\n-- QUERY 7:'
        },
        {
            'name': 'Query 7: Failed Searches / Sessions',
            'start': '-- ============================================================================\n-- QUERY 7: FAILED SEARCHES / SESSIONS',
            'end': '-- ============================================================================\n-- NOTES & LIMITATIONS'
        }
    ]
    
    for i, pattern in enumerate(query_patterns):
        start_idx = content.find(pattern['start'])
        end_idx = content.find(pattern['end'])
        
        if start_idx != -1:
            query_section = content[start_idx:end_idx] if end_idx != -1 else content[start_idx:]
            
            # Extract the actual SQL query (remove comments)
            lines = query_section.split('\n')
            query_lines = []
            in_query = False
            
            for line in lines:
                stripped = line.strip()
                if stripped and not stripped.startswith('--'):
                    in_query = True
                    query_lines.append(line)
                elif in_query and stripped.startswith('--'):
                    # End of query, start of next comment block
                    break
            
            query_text = '\n'.join(query_lines).strip()
            
            # Clean up query
            query_text = re.sub(r'--.*$', '', query_text, flags=re.MULTILINE)
            query_text = re.sub(r'/\*.*?\*/', '', query_text, flags=re.DOTALL)
            query_text = query_text.strip()
            
            if query_text:
                queries.append({
                    'name': pattern['name'],
                    'description': '',
                    'query': query_text
                })
    
    return queries

def print_query_summary(queries: List[Dict[str, str]]):
    """Print summary of extracted queries."""
    print("=" * 80)
    print("PENANG MAINLAND GROWTH ANALYSIS - QUERY EXTRACTION")
    print("=" * 80)
    print(f"\nExtracted {len(queries)} queries:\n")
    
    for i, q in enumerate(queries, 1):
        print(f"{i}. {q['name']}")
        if q['description']:
            print(f"   {q['description']}")
        print(f"   Query length: {len(q['query'])} characters")
        print()

def save_queries_to_file(queries: List[Dict[str, str]], filename: str = 'mainland_growth_queries_extracted.json'):
    """Save extracted queries to JSON file."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(queries, f, indent=2, ensure_ascii=False)
    print(f"✅ Queries saved to {filename}")

def main():
    """Main function to extract queries."""
    sql_file = 'penang_mainland_growth_analysis_queries.sql'
    
    print("Extracting queries from SQL file...")
    queries = extract_queries_alternative(sql_file)
    
    if not queries:
        print("⚠️  No queries extracted. Trying alternative method...")
        queries = extract_queries_from_sql_file(sql_file)
    
    if queries:
        print_query_summary(queries)
        save_queries_to_file(queries)
        print("\n" + "=" * 80)
        print("✅ Query extraction complete!")
        print("\nNext steps:")
        print("1. Review extracted queries in mainland_growth_queries_extracted.json")
        print("2. Execute queries via MCP tool: mcp_mcp-grab-data_run_presto_query")
        print("3. Generate insights from results")
        print("=" * 80)
    else:
        print("❌ Failed to extract queries. Please check SQL file format.")

if __name__ == '__main__':
    main()

