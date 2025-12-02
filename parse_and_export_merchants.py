"""
Parse merchant query results and export to Excel
"""

import pandas as pd
import re

# The query result text (from the MCP tool call)
result_text = """| merchant_id_nk | merchant_name | area_name | halal_status | primary_cuisine_id | segment | custom_segment | am_name | last_order_date | merchant_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1-CZEJRAMXLU6JAT | Auntie Anne's - AEON Bukit Mertajam | Alma Jaya | Halal | [519,79,81,24,62] | Enterprise | None |  | 2023-04-12 | Churned |"""

def parse_table_output(text):
    """Parse the table-formatted output from Presto query"""
    lines = text.strip().split('\n')
    
    # Find header
    header_line = None
    for i, line in enumerate(lines):
        if 'merchant_id_nk' in line and 'merchant_name' in line:
            header_line = i
            break
    
    if header_line is None:
        raise ValueError("Could not find header row")
    
    # Parse headers
    header_row = lines[header_line]
    headers = [h.strip() for h in header_row.split('|')[1:-1]]
    
    # Find data start (skip separator line)
    data_start = header_line + 2
    
    # Parse data rows
    data_rows = []
    for line in lines[data_start:]:
        # Stop at execution time line
        if '*Execution time' in line:
            break
        if line.strip() and line.startswith('|') and not line.startswith('|---'):
            cols = [c.strip() for c in line.split('|')[1:-1]]
            if len(cols) == len(headers):
                # Replace 'None' with empty string
                cols = ['' if c == 'None' else c for c in cols]
                data_rows.append(cols)
    
    return pd.DataFrame(data_rows, columns=headers)

# Read the full query result from a file or use the MCP result directly
# For now, we'll create a script that can be run with the actual results

if __name__ == "__main__":
    print("This script needs to be updated with the actual query results.")
    print("Please run the query first and paste the results.")

