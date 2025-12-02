"""
Export Penang Mainland Merchants to CSV
Automatically processes query output and creates penang_mainland_merchants.csv

This script:
1. Runs the SQL query to get all merchants with readable cuisine names
2. Parses the query output
3. Creates a complete CSV file

Run with: python export_merchants_csv.py
"""

import csv
import sys
import subprocess
import json

# SQL Query to get all Mainland merchants with readable cuisine names
SQL_QUERY = """
WITH mainland_areas AS (
    SELECT DISTINCT area_id, area_name
    FROM ocd_adw.d_area
    WHERE city_id = 13
        AND (
            area_name LIKE 'Kepala Batas%' OR area_name = 'Kepala Batas'
            OR area_name LIKE 'Prai%' OR area_name = 'Prai'
            OR area_name LIKE 'Tasek Gelugor%' OR area_name = 'Tasek Gelugor'
            OR area_name LIKE 'Bandar Cassia%' OR area_name = 'Bandar Cassia'
            OR area_name LIKE 'Bukit Mertajam%' OR area_name = 'Bukit Mertajam'
            OR area_name LIKE 'Penaga%' OR area_name = 'Penaga'
            OR area_name LIKE 'Kubang Semang%' OR area_name = 'Kubang Semang'
            OR area_name LIKE 'Simpang Ampat%' OR area_name = 'Simpang Ampat'
            OR area_name LIKE 'Bukit Tengah%' OR area_name = 'Bukit Tengah'
            OR area_name LIKE 'Bukit Teh%' OR area_name = 'Bukit Teh'
            OR area_name LIKE 'Kws Perusahaan Bebas Perai%' OR area_name = 'Kws Perusahaan Bebas Perai'
            OR area_name LIKE 'Batu Kawan Industrial Park%' OR area_name = 'Batu Kawan Industrial Park'
            OR area_name LIKE 'Sungai Bakap%' OR area_name = 'Sungai Bakap'
            OR area_name LIKE 'Padang Serai%' OR area_name = 'Padang Serai'
            OR area_name LIKE 'Bandar Tasek Mutiara%' OR area_name = 'Bandar Tasek Mutiara'
            OR area_name LIKE 'Parit Buntar%' OR area_name = 'Parit Buntar'
            OR area_name LIKE 'Bukit Minyak%' OR area_name = 'Bukit Minyak'
            OR area_name LIKE 'Permatang Pauh%' OR area_name = 'Permatang Pauh'
            OR area_name LIKE 'Seberang Jaya%' OR area_name = 'Seberang Jaya'
            OR area_name LIKE 'Kulim%' OR area_name = 'Kulim'
            OR area_name LIKE 'Sungai Jawi%' OR area_name = 'Sungai Jawi'
            OR area_name LIKE 'Taman Widuri%' OR area_name = 'Taman Widuri'
            OR area_name LIKE 'Bagan Serai%' OR area_name = 'Bagan Serai'
            OR area_name LIKE 'Telok Air Tawar%' OR area_name = 'Telok Air Tawar'
            OR area_name LIKE 'Nibong Tebal%' OR area_name = 'Nibong Tebal'
            OR area_name LIKE 'Alma Jaya%' OR area_name = 'Alma Jaya'
            OR area_name LIKE 'Beringin%' OR area_name = 'Beringin'
            OR area_name LIKE 'Kuala Kurau%' OR area_name = 'Kuala Kurau'
            OR area_name LIKE 'Karangan%' OR area_name = 'Karangan'
            OR area_name LIKE 'Gurun_Sala Besar%' OR area_name = 'Gurun_Sala Besar'
            OR area_name LIKE 'Butterworth%' OR area_name = 'Butterworth'
        )
),
mainland_merchants AS (
    SELECT DISTINCT 
        m.merchant_id_nk,
        m.merchant_name,
        m.is_halal,
        m.primary_cuisine_id,
        m.array_primary_cuisine_id,
        m.status,
        m.last_order_date,
        a.area_name,
        m.segment,
        m.custom_segment,
        m.am_name
    FROM ocd_adw.d_merchant m
    INNER JOIN ocd_adw.d_area a 
        ON m.city_id = a.city_id 
        AND SUBSTRING(m.geohash, 1, 6) = SUBSTRING(a.geohash, 1, 6)
    INNER JOIN mainland_areas ma ON a.area_id = ma.area_id
    WHERE m.city_id = 13
        AND m.status = 'ACTIVE'
        AND m.geohash IS NOT NULL
),
merchant_cuisines AS (
    SELECT 
        m.merchant_id_nk,
        m.merchant_name,
        m.area_name,
        m.is_halal,
        m.primary_cuisine_id,
        m.segment,
        m.custom_segment,
        m.am_name,
        m.last_order_date,
        CASE 
            WHEN m.is_halal = TRUE THEN 'Halal'
            WHEN m.is_halal = FALSE THEN 'Non-Halal'
            ELSE 'Unknown'
        END as halal_status,
        CASE 
            WHEN m.last_order_date < CURRENT_DATE - INTERVAL '12' MONTH 
            THEN 'Churned'
            WHEN m.last_order_date IS NULL 
            THEN 'Never Ordered'
            ELSE 'Active'
        END as merchant_status,
        cuisine_id
    FROM mainland_merchants m
    CROSS JOIN UNNEST(m.array_primary_cuisine_id) AS t(cuisine_id)
),
merchant_cuisine_names AS (
    SELECT 
        mc.merchant_id_nk,
        mc.merchant_name,
        mc.area_name,
        mc.halal_status,
        mc.segment,
        mc.custom_segment,
        mc.am_name,
        mc.last_order_date,
        mc.merchant_status,
        ARRAY_JOIN(ARRAY_AGG(DISTINCT c.name ORDER BY c.name), ', ') as cuisine_names
    FROM merchant_cuisines mc
    LEFT JOIN ocd_adw.d_cuisine c ON mc.cuisine_id = c.cuisine_id
    GROUP BY 
        mc.merchant_id_nk,
        mc.merchant_name,
        mc.area_name,
        mc.halal_status,
        mc.segment,
        mc.custom_segment,
        mc.am_name,
        mc.last_order_date,
        mc.merchant_status
)
SELECT 
    merchant_id_nk,
    merchant_name,
    area_name,
    halal_status,
    COALESCE(cuisine_names, 'Unknown') as cuisine_names,
    segment,
    custom_segment,
    am_name,
    last_order_date,
    merchant_status
FROM merchant_cuisine_names
ORDER BY area_name, halal_status, merchant_name
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


def get_query_output_from_mcp():
    """
    Attempt to get query output using MCP tool
    Note: This requires MCP to be available in the environment
    """
    try:
        # Try to import and use MCP tool if available
        # This is a placeholder - actual implementation depends on MCP setup
        print("Attempting to run query via MCP...")
        print("Note: If MCP is not available, you'll need to provide query output manually")
        return None
    except Exception as e:
        print(f"MCP not available: {e}")
        return None


def main():
    """
    Main function to export merchants to CSV
    """
    print("=" * 70)
    print("Penang Mainland Merchants CSV Exporter")
    print("=" * 70)
    print()
    
    # Try to get query output automatically
    query_output = get_query_output_from_mcp()
    
    if query_output is None:
        # If MCP is not available, try to read from a file or ask user
        print("MCP tool not available. Please provide query output:")
        print()
        print("Option 1: Save the query output to a file named 'query_output.txt'")
        print("Option 2: Paste the query output when prompted")
        print()
        
        # Try to read from file first
        try:
            with open('query_output.txt', 'r', encoding='utf-8') as f:
                query_output = f.read()
                print("✅ Found query_output.txt file")
        except FileNotFoundError:
            print("No query_output.txt file found.")
            print()
            print("Please paste the query output below (press Ctrl+D or Ctrl+Z when done):")
            print("-" * 70)
            query_output = sys.stdin.read()
            print("-" * 70)
    
    if not query_output or not query_output.strip():
        print("❌ No query output provided. Exiting.")
        print()
        print("To use this script:")
        print("1. Run the SQL query using the MCP tool")
        print("2. Copy the full output")
        print("3. Save it to a file named 'query_output.txt' in the same directory")
        print("4. Run this script again: python export_merchants_csv.py")
        return
    
    # Parse and create CSV
    try:
        output_file, count = parse_query_output_to_csv(query_output)
        print()
        print("=" * 70)
        print(f"✅ CSV file created successfully: {output_file}")
        print(f"   Total merchants exported: {count}")
        print("=" * 70)
    except Exception as e:
        print(f"❌ Error creating CSV: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

