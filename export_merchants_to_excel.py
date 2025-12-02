"""
Export Penang Mainland Merchants to Excel
Queries all active merchants from Mainland areas and exports to Excel format
"""

import pandas as pd
import json
from mcp_mcp_grab_data import run_presto_query

# SQL Query to get all Mainland merchants
query = """
WITH mainland_areas AS (
    -- Mainland areas based on QGIS classification
    SELECT DISTINCT area_id, area_name
    FROM ocd_adw.d_area
    WHERE city_id = 13  -- Penang
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
        a.area_id,
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
)
SELECT 
    merchant_id_nk,
    merchant_name,
    area_name,
    halal_status,
    primary_cuisine_id,
    segment,
    custom_segment,
    am_name,
    last_order_date,
    merchant_status
FROM (
    SELECT 
        merchant_id_nk,
        merchant_name,
        area_name,
        CASE 
            WHEN is_halal = TRUE THEN 'Halal'
            WHEN is_halal = FALSE THEN 'Non-Halal'
            ELSE 'Unknown'
        END as halal_status,
        CAST(primary_cuisine_id AS VARCHAR) as primary_cuisine_id,
        segment,
        custom_segment,
        am_name,
        last_order_date,
        CASE 
            WHEN last_order_date < CURRENT_DATE - INTERVAL '12' MONTH 
            THEN 'Churned'
            WHEN last_order_date IS NULL 
            THEN 'Never Ordered'
            ELSE 'Active'
        END as merchant_status
    FROM mainland_merchants
) t
ORDER BY area_name, halal_status, merchant_name
"""

def export_to_excel():
    """Execute query and export results to Excel"""
    print("Executing query to fetch merchants...")
    
    # Execute query using MCP tool
    result = run_presto_query(query=query)
    
    # Parse the result - it's a string with table format
    # Convert to DataFrame
    lines = result.strip().split('\n')
    
    # Find header row (starts with |)
    header_line = None
    data_start = None
    for i, line in enumerate(lines):
        if line.startswith('|') and 'merchant_id_nk' in line:
            header_line = i
            data_start = i + 2  # Skip header and separator line
            break
    
    if header_line is None:
        print("Error: Could not find header in results")
        return
    
    # Parse header
    headers = [h.strip() for h in lines[header_line].split('|')[1:-1]]
    
    # Parse data rows
    data_rows = []
    for line in lines[data_start:]:
        if line.startswith('|') and not line.startswith('|---'):
            if '*Execution time' in line:
                break
            cols = [c.strip() for c in line.split('|')[1:-1]]
            if len(cols) == len(headers):
                data_rows.append(cols)
    
    # Create DataFrame
    df = pd.DataFrame(data_rows, columns=headers)
    
    # Clean up data
    df['last_order_date'] = df['last_order_date'].replace('None', '')
    
    # Export to Excel
    output_file = 'penang_mainland_merchants.xlsx'
    df.to_excel(output_file, index=False, engine='openpyxl')
    
    print(f"\n✅ Successfully exported {len(df)} merchants to {output_file}")
    print(f"\nColumns: {', '.join(df.columns.tolist())}")
    print(f"\nSample data:")
    print(df.head(10).to_string())
    
    return df

if __name__ == "__main__":
    export_to_excel()

