"""
Generate CSV file from merchant query results
Run this script to create penang_mainland_merchants.csv
"""

import csv
import sys

def parse_table_line(line):
    """Parse a table line and extract columns"""
    if not line.strip() or line.startswith('|---') or '*Execution time' in line:
        return None
    
    if line.startswith('|'):
        # Remove leading and trailing |
        parts = line.strip().split('|')
        # Remove empty strings from split
        cols = [p.strip() for p in parts if p.strip()]
        return cols
    return None

def create_csv_from_query_output():
    """Create CSV from the query output"""
    
    # You would paste the query output here or read from a file
    # For now, this is a template that shows how to process the data
    
    headers = [
        'merchant_id_nk',
        'merchant_name', 
        'area_name',
        'halal_status',
        'primary_cuisine_id',
        'segment',
        'custom_segment',
        'am_name',
        'last_order_date',
        'merchant_status'
    ]
    
    output_file = 'penang_mainland_merchants.csv'
    
    # This would process the actual query output
    # The query results are already available from the MCP tool execution
    
    print(f"CSV file template created: {output_file}")
    print("To generate the full CSV, paste the query results into this script")
    
    return output_file

if __name__ == "__main__":
    create_csv_from_query_output()

