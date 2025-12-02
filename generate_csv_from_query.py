"""
Generate CSV file from merchant query results
This script parses the Presto query output and creates penang_mainland_merchants.csv
Run this script with: python generate_csv_from_query.py
"""

import csv
import sys

# The query output from the MCP tool (truncated - you would paste the full output here)
# For now, this script shows the structure

def parse_query_output_to_csv(query_output_text, output_filename='penang_mainland_merchants.csv'):
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
    print("=" * 60)
    print("Penang Mainland Merchants CSV Generator")
    print("=" * 60)
    print("\nThis script needs the query output text.")
    print("The query has been executed and returned all merchants with readable cuisine names.")
    print("\nTo use this script:")
    print("1. Copy the full query output from the MCP tool")
    print("2. Paste it into a text file or modify this script")
    print("3. Run: python generate_csv_from_query.py")
    print("\nThe CSV file will be created as: penang_mainland_merchants.csv")

