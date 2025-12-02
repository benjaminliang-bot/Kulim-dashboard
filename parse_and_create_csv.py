"""
Parse merchant query results from table format and create CSV
"""

import csv
import re

# The query results are in markdown table format
# We need to parse them and create a CSV

# Read the query results (they're in the format returned by the MCP tool)
# For now, I'll create a script that processes the data structure

def create_csv_from_query_results():
    """Create CSV file from parsed query results"""
    
    # Headers from the query
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
    
    # The query has been executed and we have the results
    # We'll need to parse the table output
    print("CSV file creation script ready")
    print("Headers:", headers)
    
    # Note: The actual CSV creation will be done by processing the query results
    # which are already available from the MCP tool execution

if __name__ == "__main__":
    create_csv_from_query_results()

