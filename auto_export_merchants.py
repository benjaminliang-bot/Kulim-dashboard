"""
Auto-Export Penang Mainland Merchants to CSV
Automatically processes query output and creates penang_mainland_merchants.csv

This script will:
1. Look for query output in query_output.txt (if exists)
2. Or prompt you to paste the query output
3. Parse it and create the complete CSV file

Run with: python auto_export_merchants.py
"""

import csv
import sys
import os

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
    
    return output_filename, len(data_rows), headers


def main():
    """
    Main function to export merchants to CSV
    """
    print("=" * 70)
    print("Penang Mainland Merchants - Auto CSV Exporter")
    print("=" * 70)
    print()
    
    query_output = None
    
    # Try to read from file first
    if os.path.exists('query_output.txt'):
        print("✅ Found query_output.txt file")
        try:
            with open('query_output.txt', 'r', encoding='utf-8') as f:
                query_output = f.read()
                print("   Reading query output from file...")
        except Exception as e:
            print(f"   ❌ Error reading file: {e}")
    
    # If no file, try to get from stdin or prompt
    if not query_output or not query_output.strip():
        print()
        print("No query_output.txt file found.")
        print()
        print("To use this script automatically:")
        print("1. Copy the FULL query output from the MCP tool result")
        print("2. Save it to a file named 'query_output.txt' in this directory")
        print("3. Run this script again: python auto_export_merchants.py")
        print()
        print("Or paste the query output now (press Enter twice when done):")
        print("-" * 70)
        
        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            pass
        
        query_output = '\n'.join(lines)
        print("-" * 70)
    
    if not query_output or not query_output.strip():
        print("❌ No query output provided. Exiting.")
        return
    
    # Parse and create CSV
    try:
        print()
        print("Processing query output...")
        output_file, count, headers = parse_query_output_to_csv(query_output)
        
        print()
        print("=" * 70)
        print(f"✅ SUCCESS! CSV file created: {output_file}")
        print(f"   Total merchants exported: {count}")
        print(f"   Columns: {', '.join(headers)}")
        print("=" * 70)
        print()
        print(f"You can now open {output_file} in Excel!")
        
    except Exception as e:
        print()
        print("=" * 70)
        print(f"❌ ERROR: {e}")
        print("=" * 70)
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

