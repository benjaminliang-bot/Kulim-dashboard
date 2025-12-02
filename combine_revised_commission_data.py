import pandas as pd
import numpy as np

print("COMBINING REVISED DATA WITH EK & XR")
print("="*70)

# Load the revised data for Darren, CY, Suki (from monthly mapping)
# This data is from the query result above
revised_data = {
    '202501': {'CY': {'gmv': 4622180.82, 'commission': 1006075.24, 'pct': 11.11, 'rate': 21.77},
               'Darren': {'gmv': 3797357.11, 'commission': 871400.50, 'pct': 9.13, 'rate': 22.95}},
    '202502': {'CY': {'gmv': 4411228.14, 'commission': 973491.39, 'pct': 11.41, 'rate': 22.07},
               'Darren': {'gmv': 3493956.82, 'commission': 797747.57, 'pct': 9.03, 'rate': 22.83}},
    '202503': {'CY': {'gmv': 4571175.17, 'commission': 1010725.86, 'pct': 12.35, 'rate': 22.11},
               'Darren': {'gmv': 3258518.53, 'commission': 731202.88, 'pct': 8.80, 'rate': 22.44}},
    '202504': {'CY': {'gmv': 4803774.61, 'commission': 1051541.95, 'pct': 12.01, 'rate': 21.89},
               'Darren': {'gmv': 3861105.80, 'commission': 865007.54, 'pct': 9.65, 'rate': 22.40}},
    '202505': {'CY': {'gmv': 5203139.57, 'commission': 1142892.72, 'pct': 11.61, 'rate': 21.97},
               'Darren': {'gmv': 4281293.52, 'commission': 961370.92, 'pct': 9.56, 'rate': 22.46}},
    '202506': {'CY': {'gmv': 5126747.98, 'commission': 1141806.01, 'pct': 11.82, 'rate': 22.27},
               'Darren': {'gmv': 5492028.33, 'commission': 1245152.31, 'pct': 12.67, 'rate': 22.67},
               'Suki': {'gmv': 2783032.94, 'commission': 641469.11, 'pct': 6.42, 'rate': 23.05}},
    '202507': {'CY': {'gmv': 5442254.98, 'commission': 1220118.75, 'pct': 11.82, 'rate': 22.42},
               'Darren': {'gmv': 3972196.09, 'commission': 882854.38, 'pct': 8.62, 'rate': 22.23},
               'Suki': {'gmv': 3323268.41, 'commission': 777756.66, 'pct': 7.22, 'rate': 23.40}},
    '202508': {'CY': {'gmv': 5284802.86, 'commission': 1174835.61, 'pct': 11.31, 'rate': 22.23},
               'Darren': {'gmv': 4317883.35, 'commission': 964158.67, 'pct': 9.24, 'rate': 22.33},
               'Suki': {'gmv': 3455495.31, 'commission': 811135.90, 'pct': 7.39, 'rate': 23.47}},
    '202509': {'CY': {'gmv': 5168707.60, 'commission': 1153179.55, 'pct': 11.42, 'rate': 22.31},
               'Darren': {'gmv': 4071390.15, 'commission': 919084.43, 'pct': 8.99, 'rate': 22.57},
               'Suki': {'gmv': 3306129.89, 'commission': 778216.30, 'pct': 7.30, 'rate': 23.54}},
    '202510': {'CY': {'gmv': 5152701.15, 'commission': 1140759.83, 'pct': 10.93, 'rate': 22.14},
               'Darren': {'gmv': 4244822.18, 'commission': 950781.59, 'pct': 9.01, 'rate': 22.40},
               'Suki': {'gmv': 3475061.18, 'commission': 815770.23, 'pct': 7.37, 'rate': 23.48}}
}

# Load EK and XR from previous analysis
previous_path = r"C:\Users\benjamin.liang\Downloads\team_commission_analysis_ytd_2025.xlsx"
df_previous = pd.read_excel(previous_path, sheet_name='Monthly_Summary')

# Get EK and XR data
ek_xr_data = df_previous[df_previous['owner'].isin(['EK', 'XR'])].copy()

# Build comprehensive dataset
rows = []
for month_id in ['202501', '202502', '202503', '202504', '202505', '202506', '202507', '202508', '202509', '202510']:
    month_int = int(month_id)
    
    # Get EK and XR from previous data
    ek_data = ek_xr_data[(ek_xr_data['month_id'] == month_int) & (ek_xr_data['owner'] == 'EK')]
    xr_data = ek_xr_data[(ek_xr_data['month_id'] == month_int) & (ek_xr_data['owner'] == 'XR')]
    
    total_penang = ek_data['total_penang_gmv'].values[0] if len(ek_data) > 0 else None
    
    # Add EK
    if len(ek_data) > 0:
        rows.append({
            'month_id': month_int,
            'owner': 'EK',
            'merchant_gmv': ek_data['merchant_gmv'].values[0],
            'merchant_commission_billing': ek_data['merchant_commission_billing'].values[0],
            'total_penang_gmv': total_penang,
            'gmv_pct_of_penang': ek_data['gmv_pct_of_penang'].values[0],
            'commission_rate_pct': ek_data['commission_rate_pct'].values[0]
        })
    
    # Add XR
    if len(xr_data) > 0:
        rows.append({
            'month_id': month_int,
            'owner': 'XR',
            'merchant_gmv': xr_data['merchant_gmv'].values[0],
            'merchant_commission_billing': xr_data['merchant_commission_billing'].values[0],
            'total_penang_gmv': total_penang,
            'gmv_pct_of_penang': xr_data['gmv_pct_of_penang'].values[0],
            'commission_rate_pct': xr_data['commission_rate_pct'].values[0]
        })
    
    # Add revised CY, Darren, Suki
    if month_id in revised_data:
        for owner in ['CY', 'Darren', 'Suki']:
            if owner in revised_data[month_id]:
                data = revised_data[month_id][owner]
                rows.append({
                    'month_id': month_int,
                    'owner': owner,
                    'merchant_gmv': data['gmv'],
                    'merchant_commission_billing': data['commission'],
                    'total_penang_gmv': total_penang,
                    'gmv_pct_of_penang': data['pct'],
                    'commission_rate_pct': data['rate']
                })

df_revised = pd.DataFrame(rows)
df_revised = df_revised.sort_values(['month_id', 'owner'])

print("\nREVISED TEAM COMMISSION ANALYSIS - YTD 2025 (Jan-Oct)")
print("="*70)
print("Using monthly AM mapping for Darren, CY, and Suki")
print("EK and XR based on tracker file (MGS and NMA)")
print()

# Summary
summary = df_revised.groupby('owner').agg({
    'gmv_pct_of_penang': 'mean',
    'commission_rate_pct': 'mean'
}).reset_index()
summary.columns = ['Owner', 'Avg_GMV_Pct_of_Penang', 'Avg_Commission_Rate_Pct']
summary = summary.sort_values('Avg_GMV_Pct_of_Penang', ascending=False)

print("SUMMARY - AVERAGE MONTHLY:")
print(summary.to_string(index=False))

# Monthly breakdown
print("\n\nMONTHLY BREAKDOWN - GMV % OF PENANG TOTAL:")
monthly_pivot = df_revised.pivot_table(
    index='month_id', 
    columns='owner', 
    values='gmv_pct_of_penang', 
    aggfunc='first'
)
monthly_pivot = monthly_pivot[['EK', 'XR', 'CY', 'Darren', 'Suki']]
print(monthly_pivot.to_string())

print("\n\nMONTHLY BREAKDOWN - COMMISSION RATE %:")
commission_pivot = df_revised.pivot_table(
    index='month_id', 
    columns='owner', 
    values='commission_rate_pct', 
    aggfunc='first'
)
commission_pivot = commission_pivot[['EK', 'XR', 'CY', 'Darren', 'Suki']]
print(commission_pivot.to_string())

# Save
output_path = r"C:\Users\benjamin.liang\Downloads\team_commission_revised_monthly_mapping.xlsx"
with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    summary.to_excel(writer, sheet_name='Summary', index=False)
    monthly_pivot.to_excel(writer, sheet_name='Monthly_GMV_Pct', index=True)
    commission_pivot.to_excel(writer, sheet_name='Monthly_Commission_Rate', index=True)
    df_revised.to_excel(writer, sheet_name='Detailed_Data', index=False)

print(f"\n\nComplete revised analysis saved to: {output_path}")

