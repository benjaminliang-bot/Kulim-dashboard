"""
Create full CSV file from merchant query results
This script parses the complete query output and creates penang_mainland_merchants.csv
"""

import csv
import re

def parse_table_output_to_csv(query_output_text, output_filename='penang_mainland_merchants.csv'):
    """
    Parse the table-formatted query output and create CSV file
    
    Args:
        query_output_text: The full text output from the Presto query
        output_filename: Name of the CSV file to create
    """
    lines = query_output_text.strip().split('\n')
    
    # Find header row
    header_line_idx = None
    for i, line in enumerate(lines):
        if 'merchant_id_nk' in line and 'merchant_name' in line:
            header_line_idx = i
            break
    
    if header_line_idx is None:
        raise ValueError("Could not find header row in query output")
    
    # Parse headers
    header_line = lines[header_line_idx]
    headers = [h.strip() for h in header_line.split('|')[1:-1]]
    
    # Find data start (skip separator line)
    data_start_idx = header_line_idx + 2
    
    # Parse data rows
    data_rows = []
    for line in lines[data_start_idx:]:
        # Skip separator lines and execution time lines
        if line.startswith('|---') or '*Execution time' in line or not line.strip():
            continue
        
        if line.startswith('|'):
            # Parse the row
            cols = [c.strip() for c in line.split('|')[1:-1]]
            if len(cols) == len(headers):
                data_rows.append(cols)
    
    # Write to CSV
    with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(data_rows)
    
    print(f"✅ Successfully created {output_filename} with {len(data_rows)} merchants")
    return len(data_rows)

if __name__ == "__main__":
    # Read the query output from a file or paste it here
    # For now, this is a template - you would paste the query output here
    print("This script needs the query output text to be provided")
    print("Please paste the query output when running this script")

