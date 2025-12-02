import pandas as pd
import numpy as np

# Load merchant-level data from query result (use the latest/largest file)
import glob
import os
tool_files = glob.glob(r"C:\Users\benjamin.liang\.cursor\projects\c-Users-benjamin-liang-Documents-Python\agent-tools\*.txt")
# Get the largest file (most recent complete data)
merchant_data_path = max(tool_files, key=os.path.getsize)
print(f"Using data file: {merchant_data_path} ({os.path.getsize(merchant_data_path)/1024/1024:.1f} MB)")

# Load tracker for team assignments
tracker_path = r"C:\Users\benjamin.liang\Downloads\penang main tracker 2.xlsx"
df_tracker = pd.read_excel(tracker_path, sheet_name='Sheet1', header=1)
df_tracker.columns = [str(c) for c in df_tracker.columns]

# Create team assignment mapping
team_assignments = {}
for _, row in df_tracker.iterrows():
    merchant_id = row.get('Mex ID', '')
    if pd.notna(merchant_id):
        merchant_id = str(merchant_id)
        if pd.notna(row.get('MGS')):
            team_assignments[merchant_id] = 'EK'
        elif row.get('AMBD') == 'NMA':
            team_assignments[merchant_id] = 'XR'
        elif 'chiayee' in str(row.get('AM', '')).lower():
            team_assignments[merchant_id] = 'CY'
        elif 'darren' in str(row.get('AM', '')).lower():
            team_assignments[merchant_id] = 'Darren'
        elif 'suki' in str(row.get('AM', '')).lower():
            team_assignments[merchant_id] = 'Suki'

print(f"Team assignments created for {len(team_assignments)} merchants")

# Load merchant data (pipe-delimited from query result)
try:
    # Read file line by line and parse manually
    with open(merchant_data_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find header line (contains column names)
    header_line = None
    data_start = 0
    for i, line in enumerate(lines):
        if 'month_id' in line and 'merchant_id_nk' in line:
            header_line = i
            data_start = i + 2  # Skip header and separator line
            break
    
    if header_line is None:
        raise ValueError("Could not find header line")
    
    # Parse header
    header = [col.strip() for col in lines[header_line].split('|') if col.strip() and '---' not in col]
    print(f"Found columns: {header}")
    
    # Parse data rows
    data_rows = []
    for line in lines[data_start:]:
        if '---' in line or not line.strip():
            continue
        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 5 and parts[1]:  # Valid data row
            data_rows.append({
                'month_id': parts[1],
                'merchant_id_nk': parts[2],
                'merchant_gmv': parts[3],
                'merchant_commission_billing': parts[4],
                'total_penang_gmv': parts[5] if len(parts) > 5 else None
            })
    
    df_merchants = pd.DataFrame(data_rows)
    
    # Convert numeric columns
    numeric_cols = ['month_id', 'merchant_gmv', 'merchant_commission_billing', 'total_penang_gmv']
    for col in numeric_cols:
        if col in df_merchants.columns:
            df_merchants[col] = pd.to_numeric(df_merchants[col], errors='coerce')
    
    # Remove rows with missing data
    df_merchants = df_merchants.dropna(subset=['merchant_id_nk', 'month_id'])
    
    print(f"Loaded {len(df_merchants)} merchant records")
    
    # Assign team members
    df_merchants['owner'] = df_merchants['merchant_id_nk'].map(team_assignments)
    
    # Filter to only assigned team members (exclude Jamie and unassigned)
    df_team = df_merchants[df_merchants['owner'].isin(['EK', 'XR', 'CY', 'Darren', 'Suki'])].copy()
    
    # Aggregate by month and owner
    monthly_summary = df_team.groupby(['month_id', 'owner']).agg({
        'merchant_gmv': 'sum',
        'merchant_commission_billing': 'sum',
        'total_penang_gmv': 'first'  # Same for all rows in a month
    }).reset_index()
    
    # Calculate percentages and commission rates
    monthly_summary['gmv_pct_of_penang'] = (monthly_summary['merchant_gmv'] / monthly_summary['total_penang_gmv'] * 100).round(2)
    monthly_summary['commission_rate_pct'] = (monthly_summary['merchant_commission_billing'] / monthly_summary['merchant_gmv'] * 100).round(4)
    
    # Sort and display
    monthly_summary = monthly_summary.sort_values(['month_id', 'owner'])
    
    print("\nTEAM COMMISSION RATE ANALYSIS - YTD 2025")
    print("="*80)
    print(monthly_summary.to_string(index=False))
    
    # Calculate averages
    print("\nAVERAGE MONTHLY COMMISSION RATES:")
    avg_rates = monthly_summary.groupby('owner')['commission_rate_pct'].mean().sort_values(ascending=False)
    for owner, rate in avg_rates.items():
        print(f"{owner}: {rate:.4f}%")
    
    # Save to Excel
    output_path = r"C:\Users\benjamin.liang\Downloads\team_commission_analysis_ytd_2025.xlsx"
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        monthly_summary.to_excel(writer, sheet_name='Monthly_Summary', index=False)
        avg_rates.to_frame('Avg_Commission_Rate').to_excel(writer, sheet_name='Average_Rates', index=True)
    
    print(f"\nResults saved to: {output_path}")
    
except Exception as e:
    print(f"Error processing data: {e}")
    print("Trying alternative approach...")

