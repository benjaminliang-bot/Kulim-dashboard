"""
Create complete CSV file from merchant query results
This script parses the full Presto query output and creates penang_mainland_merchants.csv

The query has been executed and returned all merchants with readable cuisine names.
This script will parse that output and create the complete CSV file.

Run with: python create_complete_csv.py
"""

import csv

# Paste the FULL query output here (from the MCP tool result)
# The query output starts with: | merchant_id_nk | merchant_name | ...
# and ends with: *Execution time: X.XXs

QUERY_OUTPUT = """
| merchant_id_nk | merchant_name | area_name | halal_status | cuisine_names | segment | custom_segment | am_name | last_order_date | merchant_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
[PASTE THE FULL QUERY OUTPUT HERE]
"""

def parse_query_output_to_csv(query_output_text, output_filename='penang_mainland_merchants.csv'):
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
    if "PASTE THE FULL QUERY OUTPUT HERE" in QUERY_OUTPUT:
        print("=" * 70)
        print("INSTRUCTIONS:")
        print("=" * 70)
        print("\n1. The query has been executed and returned all merchants")
        print("2. Copy the FULL query output from the MCP tool result")
        print("3. Paste it into the QUERY_OUTPUT variable in this script")
        print("4. Run: python create_complete_csv.py")
        print("\nThe CSV file will be created as: penang_mainland_merchants.csv")
        print("\nThe query output should start with:")
        print("  | merchant_id_nk | merchant_name | area_name | ...")
        print("And end with:")
        print("  *Execution time: X.XXs")
    else:
        parse_query_output_to_csv(QUERY_OUTPUT)

