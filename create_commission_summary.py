import pandas as pd

# Load the results
path = r"C:\Users\benjamin.liang\Downloads\team_commission_analysis_ytd_2025.xlsx"
df = pd.read_excel(path, sheet_name='Monthly_Summary')

# Create summary table
summary = df.groupby('owner').agg({
    'gmv_pct_of_penang': 'mean',
    'commission_rate_pct': 'mean'
}).reset_index()

summary.columns = ['Owner', 'Avg_GMV_Pct_of_Penang', 'Avg_Commission_Rate_Pct']
summary = summary.sort_values('Avg_GMV_Pct_of_Penang', ascending=False)

print('TEAM COMMISSION RATE & GMV CONTRIBUTION - YTD 2025 (Jan-Oct)')
print('='*70)
print('EXCLUDING JAMIE')
print('='*70)

print('\nSUMMARY - AVERAGE MONTHLY:')
print(summary.to_string(index=False))

# Monthly breakdown
print('\n\nMONTHLY BREAKDOWN - GMV % OF PENANG TOTAL:')
monthly_pivot = df.pivot_table(
    index='month_id', 
    columns='owner', 
    values='gmv_pct_of_penang', 
    aggfunc='first'
)
# Reorder columns
monthly_pivot = monthly_pivot[['EK', 'XR', 'CY', 'Darren', 'Suki']]
print(monthly_pivot.to_string())

print('\n\nMONTHLY BREAKDOWN - COMMISSION RATE %:')
commission_pivot = df.pivot_table(
    index='month_id', 
    columns='owner', 
    values='commission_rate_pct', 
    aggfunc='first'
)
commission_pivot = commission_pivot[['EK', 'XR', 'CY', 'Darren', 'Suki']]
print(commission_pivot.to_string())

# Save comprehensive summary
output_path = r"C:\Users\benjamin.liang\Downloads\team_commission_summary_final.xlsx"
with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    summary.to_excel(writer, sheet_name='Summary', index=False)
    monthly_pivot.to_excel(writer, sheet_name='Monthly_GMV_Pct', index=True)
    commission_pivot.to_excel(writer, sheet_name='Monthly_Commission_Rate', index=True)
    df.to_excel(writer, sheet_name='Detailed_Data', index=False)

print(f'\n\nComplete analysis saved to: {output_path}')

