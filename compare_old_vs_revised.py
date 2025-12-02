import pandas as pd

# Load old data
old_path = r"C:\Users\benjamin.liang\Downloads\team_commission_analysis_ytd_2025.xlsx"
df_old = pd.read_excel(old_path, sheet_name='Monthly_Summary')

# Load revised data
revised_path = r"C:\Users\benjamin.liang\Downloads\team_commission_revised_monthly_mapping.xlsx"
df_revised = pd.read_excel(revised_path, sheet_name='Detailed_Data')

print("COMPARISON: OLD vs REVISED CALCULATION")
print("="*80)
print("OLD: Based on static tracker file")
print("REVISED: Using monthly AM mapping for Darren, CY, and Suki")
print()

# Filter to only Darren, CY, Suki for comparison
df_old_filtered = df_old[df_old['owner'].isin(['CY', 'Darren', 'Suki'])].copy()
df_revised_filtered = df_revised[df_revised['owner'].isin(['CY', 'Darren', 'Suki'])].copy()

# Merge for comparison
df_compare = df_old_filtered.merge(
    df_revised_filtered,
    on=['month_id', 'owner'],
    suffixes=('_old', '_revised'),
    how='outer'
)

# Calculate differences
df_compare['gmv_pct_diff'] = df_compare['gmv_pct_of_penang_revised'] - df_compare['gmv_pct_of_penang_old']
df_compare['commission_rate_diff'] = df_compare['commission_rate_pct_revised'] - df_compare['commission_rate_pct_old']
df_compare['gmv_diff'] = df_compare['merchant_gmv_revised'] - df_compare['merchant_gmv_old']

print("MONTHLY COMPARISON - GMV % OF PENANG:")
print("-"*80)
comparison_pct = df_compare.pivot_table(
    index='month_id',
    columns='owner',
    values='gmv_pct_diff',
    aggfunc='first'
)
comparison_pct = comparison_pct[['CY', 'Darren', 'Suki']]
print(comparison_pct.to_string())

print("\n\nMONTHLY COMPARISON - COMMISSION RATE %:")
print("-"*80)
comparison_rate = df_compare.pivot_table(
    index='month_id',
    columns='owner',
    values='commission_rate_diff',
    aggfunc='first'
)
comparison_rate = comparison_rate[['CY', 'Darren', 'Suki']]
print(comparison_rate.to_string())

# Summary of changes
print("\n\nSUMMARY OF CHANGES:")
print("-"*80)
summary_old = df_old_filtered.groupby('owner').agg({
    'gmv_pct_of_penang': 'mean',
    'commission_rate_pct': 'mean'
}).reset_index()
summary_old.columns = ['Owner', 'Avg_GMV_Pct_Old', 'Avg_Commission_Rate_Old']

summary_revised = df_revised_filtered.groupby('owner').agg({
    'gmv_pct_of_penang': 'mean',
    'commission_rate_pct': 'mean'
}).reset_index()
summary_revised.columns = ['Owner', 'Avg_GMV_Pct_Revised', 'Avg_Commission_Rate_Revised']

summary_merge = summary_old.merge(summary_revised, on='Owner')
summary_merge['GMV_Pct_Change'] = summary_merge['Avg_GMV_Pct_Revised'] - summary_merge['Avg_GMV_Pct_Old']
summary_merge['Commission_Rate_Change'] = summary_merge['Avg_Commission_Rate_Revised'] - summary_merge['Avg_Commission_Rate_Old']

print(summary_merge.to_string(index=False))

# Save comparison
output_path = r"C:\Users\benjamin.liang\Downloads\team_commission_comparison_old_vs_revised.xlsx"
with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    summary_merge.to_excel(writer, sheet_name='Summary_Comparison', index=False)
    comparison_pct.to_excel(writer, sheet_name='GMV_Pct_Diff', index=True)
    comparison_rate.to_excel(writer, sheet_name='Commission_Rate_Diff', index=True)
    df_compare.to_excel(writer, sheet_name='Detailed_Comparison', index=False)

print(f"\n\nComparison saved to: {output_path}")

