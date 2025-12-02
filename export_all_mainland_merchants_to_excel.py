"""
Export All Penang Mainland Merchants to Excel
Queries all merchants (active and churned) from Mainland areas and exports to Excel format
"""

import pandas as pd
from mcp_mcp_grab_data_run_presto_query import run_presto_query

# SQL Query to get all Mainland merchants (active and churned)
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
            OR area_name LIKE 'Batu Kawan%' OR area_name = 'Batu Kawan'
            OR area_name LIKE 'Jawi%' OR area_name = 'Jawi'
            OR area_name LIKE 'Perai%' OR area_name = 'Perai'
        )
),
mainland_merchants AS (
    SELECT DISTINCT 
        m.merchant_id_nk,
        m.merchant_name,
        m.is_halal,
        m.primary_cuisine_id,
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
            WHEN status = 'ACTIVE' AND (last_order_date IS NULL OR last_order_date >= CURRENT_DATE - INTERVAL '12' MONTH)
            THEN 'Active'
            WHEN status = 'ACTIVE' AND last_order_date < CURRENT_DATE - INTERVAL '12' MONTH
            THEN 'Churned'
            WHEN status != 'ACTIVE'
            THEN 'Inactive'
            ELSE 'Unknown'
        END as merchant_status
    FROM mainland_merchants
) t
ORDER BY area_name, merchant_status, merchant_name;
"""

def export_merchants_to_excel():
    """Execute query and export results to Excel"""
    print("Querying Mainland merchants from Grab DataLake...")
    
    try:
        # Execute the query
        result = run_presto_query(query=query)
        
        # Convert result to DataFrame
        # The result should be a dictionary with query results
        if isinstance(result, dict):
            # Check if result contains data
            if 'data' in result or 'rows' in result:
                # Parse the result based on the actual structure
                # This may need adjustment based on the actual MCP response format
                df = pd.DataFrame(result.get('data', result.get('rows', [])))
            else:
                # If result is the data directly
                df = pd.DataFrame(result)
        else:
            df = pd.DataFrame(result)
        
        # If DataFrame is empty, try to parse from string response
        if df.empty and isinstance(result, str):
            print("Attempting to parse string response...")
            # This would need custom parsing based on actual response format
            return
        
        # Rename columns for better Excel readability
        column_mapping = {
            'merchant_id_nk': 'Merchant ID',
            'merchant_name': 'Merchant Name',
            'area_name': 'Area Name',
            'halal_status': 'Halal Status',
            'primary_cuisine_id': 'Primary Cuisine ID',
            'segment': 'Segment',
            'custom_segment': 'Custom Segment',
            'am_name': 'Account Manager',
            'last_order_date': 'Last Order Date',
            'merchant_status': 'Merchant Status'
        }
        df = df.rename(columns=column_mapping)
        
        # Export to Excel
        output_file = 'penang_mainland_merchants.xlsx'
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='All Merchants', index=False)
            
            # Auto-adjust column widths
            worksheet = writer.sheets['All Merchants']
            for idx, col in enumerate(df.columns):
                max_length = max(
                    df[col].astype(str).map(len).max(),
                    len(str(col))
                )
                worksheet.column_dimensions[chr(65 + idx)].width = min(max_length + 2, 50)
        
        print(f"✅ Successfully exported {len(df)} merchants to {output_file}")
        print(f"\nSummary:")
        print(f"  - Total Merchants: {len(df)}")
        print(f"  - Active: {len(df[df['Merchant Status'] == 'Active'])}")
        print(f"  - Churned: {len(df[df['Merchant Status'] == 'Churned'])}")
        print(f"  - Inactive: {len(df[df['Merchant Status'] == 'Inactive'])}")
        print(f"  - Areas: {df['Area Name'].nunique()}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    export_merchants_to_excel()



