"""
Create full CSV file from merchant query results
This script parses the complete query output and creates penang_mainland_merchants.csv
"""

import csv
import sys

def parse_table_output_to_csv(query_output_text, output_filename='penang_mainland_merchants.csv'):
    """
    Parse the table-formatted query output and create CSV file
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
    
    # Parse all data rows
    data_rows = []
    for line in lines[data_start_idx:]:
        # Stop at execution time line
        if '*Execution time' in line:
            break
        
        if line.strip() and line.startswith('|') and not line.startswith('|---'):
            cols = [c.strip() for c in line.split('|')[1:-1]]
            if len(cols) == len(headers):
                # Replace 'None' with empty string
                cols = ['' if c == 'None' else c for c in cols]
                data_rows.append(cols)
    
    # Write to CSV
    with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(headers)
        writer.writerows(data_rows)
    
    print(f"✅ Successfully created {output_filename}")
    print(f"   Total merchants: {len(data_rows)}")
    print(f"   Columns: {', '.join(headers)}")
    
    return output_filename, len(data_rows)

if __name__ == "__main__":
    # Read query output from stdin or file
    if len(sys.argv) > 1:
        # Read from file
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            query_output = f.read()
    else:
        # Read from stdin
        query_output = sys.stdin.read()
    
    parse_table_output_to_csv(query_output)

