import pandas as pd

# Commission data with merchant_id mapping
data = [
    {'merchant_id': 2227692, 'merchant_id_nk': '1-C2CZTRKGAKLCLT', 'merchant_name': 'Sin Nam Huat Roasted Chicken & Duck Rice - Island Glades [Non-Halal]', 'completed_orders': 20805, 'total_gmv_myr': 793393.77, 'total_commission_billing_myr': 148724.10, 'commission_rate_pct': 18.7453},
    {'merchant_id': 2232783, 'merchant_id_nk': '1-C2C2MBA2PE3JRE', 'merchant_name': 'Sin Nam Huat Roasted Chicken & Duck Rice - Jalan Burma [Non-Halal]', 'completed_orders': 8296, 'total_gmv_myr': 305062.28, 'total_commission_billing_myr': 60058.40, 'commission_rate_pct': 19.6873},
    {'merchant_id': 2421841, 'merchant_id_nk': '1-C2K3TYW3GNDJAN', 'merchant_name': 'Sin Nam Huat Roasted Chicken & Duck Rice - Persiaran Mahsuri [Non-Halal]', 'completed_orders': 9033, 'total_gmv_myr': 300948.39, 'total_commission_billing_myr': 58936.90, 'commission_rate_pct': 19.5837},
    {'merchant_id': 2206258, 'merchant_id_nk': '1-C2CKA6JYAKKCJX', 'merchant_name': 'Sin Nam Huat Roasted Chicken & Duck Rice - Jalan Macalister [Non-Halal]', 'completed_orders': 7466, 'total_gmv_myr': 281071.84, 'total_commission_billing_myr': 55573.68, 'commission_rate_pct': 19.7721},
    {'merchant_id': 2314950, 'merchant_id_nk': '1-C2EWE7WYRCKCGJ', 'merchant_name': 'Sin Nam Huat Roasted Chicken & Duck Rice - Ayer Itam [Non-Halal]', 'completed_orders': 7646, 'total_gmv_myr': 279393.70, 'total_commission_billing_myr': 53650.27, 'commission_rate_pct': 19.2024},
    {'merchant_id': 2233429, 'merchant_id_nk': '1-C2C2PFEJE76YVN', 'merchant_name': 'Sin Nam Huat Roasted Chicken & Duck Rice - Jalan Fettes [Non-Halal]', 'completed_orders': 7967, 'total_gmv_myr': 263487.17, 'total_commission_billing_myr': 52086.00, 'commission_rate_pct': 19.7679},
    {'merchant_id': 2464331, 'merchant_id_nk': '1-C2L1WFWBGX6FT6', 'merchant_name': 'Sin Nam Huat Roasted Chicken & Duck Rice - Solok Sungai Pinang [Non-Halal]', 'completed_orders': 7207, 'total_gmv_myr': 262557.44, 'total_commission_billing_myr': 51172.86, 'commission_rate_pct': 19.4902},
    {'merchant_id': 2956524, 'merchant_id_nk': '1-C25VVJLGJU2UCA', 'merchant_name': 'Sin Nam Huat Roasted Chicken & Duck Rice - Jalan Bagan Ajam [Non-Halal]', 'completed_orders': 5823, 'total_gmv_myr': 199692.97, 'total_commission_billing_myr': 38457.82, 'commission_rate_pct': 19.2585},
    {'merchant_id': 5144954, 'merchant_id_nk': '1-C7AUMF2ULXAJRJ', 'merchant_name': 'Sin Nam Huat Roasted Chicken & Duck Rice - Lintang Batu Maung 4 [Non-Halal]', 'completed_orders': 3571, 'total_gmv_myr': 140826.65, 'total_commission_billing_myr': 25825.73, 'commission_rate_pct': 18.3387},
    {'merchant_id': 3576332, 'merchant_id_nk': '1-C3VZLGBZLZJVNX', 'merchant_name': 'Sin Nam Huat Roasted Chicken & Duck Rice - Kedai Kopi Golden Lake [Non-Halal]', 'completed_orders': 2540, 'total_gmv_myr': 82534.52, 'total_commission_billing_myr': 15913.54, 'commission_rate_pct': 19.2811},
    {'merchant_id': 4108659, 'merchant_id_nk': '1-C4KVVLDZNJMBWA', 'merchant_name': '[INACTV: COCO] Sin Nam Huat Roasted Chicken & Duck Rice - Lintang Batu Maung 4 [Non-Halal]', 'completed_orders': 530, 'total_gmv_myr': 18393.18, 'total_commission_billing_myr': 3447.92, 'commission_rate_pct': 18.7456}
]

df = pd.DataFrame(data)

# Reorder columns
df = df[['merchant_id', 'merchant_id_nk', 'merchant_name', 'completed_orders', 'total_gmv_myr', 'total_commission_billing_myr', 'commission_rate_pct']]

# Sort by commission descending
df = df.sort_values('total_commission_billing_myr', ascending=False)

print("SIN NAM HUAT COMMISSION ANALYSIS WITH MERCHANT_ID (MYR)")
print("="*80)
print("Brand ID: 60_sin_nam_huat_roasted_chicken_and_duck_rice")
print("Period: Jan-Oct 2025 (YTD)")
print("Currency: MYR (Malaysian Ringgit)")
print()

# Format for display
display_df = df.copy()
display_df['total_gmv_myr'] = display_df['total_gmv_myr'].apply(lambda x: f'MYR {x:,.2f}')
display_df['total_commission_billing_myr'] = display_df['total_commission_billing_myr'].apply(lambda x: f'MYR {x:,.2f}')
display_df['commission_rate_pct'] = display_df['commission_rate_pct'].apply(lambda x: f'{x:.2f}%')

print(display_df.to_string(index=False))

# Calculate totals
total_orders = df['completed_orders'].sum()
total_gmv = df['total_gmv_myr'].sum()
total_commission = df['total_commission_billing_myr'].sum()
avg_rate = (total_commission / total_gmv * 100)

print(f"\n\nBRAND TOTALS:")
print(f"Total Completed Orders: {total_orders:,}")
print(f"Total GMV: MYR {total_gmv:,.2f}")
print(f"Total Commission Billing: MYR {total_commission:,.2f}")
print(f"Average Commission Rate: {avg_rate:.4f}%")

# Save to Excel with MYR formatting
output_path = r"C:\Users\benjamin.liang\Downloads\sin_nam_huat_commission_with_merchant_id_myr.xlsx"
with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    # Write main data
    df.to_excel(writer, sheet_name='Commission_Summary', index=False)
    
    # Get the worksheet to format
    worksheet = writer.sheets['Commission_Summary']
    
    # Format currency columns
    from openpyxl.styles import Font, Alignment
    from openpyxl.utils import get_column_letter
    
    # Header formatting
    header_font = Font(bold=True)
    for cell in worksheet[1]:
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center')
    
    # Format GMV and Commission columns as currency (MYR)
    for row in range(2, len(df) + 2):
        # GMV column (E)
        cell = worksheet[f'E{row}']
        cell.number_format = 'MYR #,##0.00'
        # Commission column (F)
        cell = worksheet[f'F{row}']
        cell.number_format = 'MYR #,##0.00'
        # Commission rate column (G)
        cell = worksheet[f'G{row}']
        cell.number_format = '0.00"%"'
    
    # Add totals row
    totals_df = pd.DataFrame({
        'merchant_id': ['TOTAL'],
        'merchant_id_nk': ['ALL OUTLETS'],
        'merchant_name': [''],
        'completed_orders': [total_orders],
        'total_gmv_myr': [total_gmv],
        'total_commission_billing_myr': [total_commission],
        'commission_rate_pct': [avg_rate]
    })
    
    start_row = len(df) + 3
    totals_df.to_excel(writer, sheet_name='Commission_Summary', index=False, startrow=start_row, header=False)
    
    # Format totals row
    totals_font = Font(bold=True)
    for col in range(1, 8):
        cell = worksheet.cell(row=start_row+1, column=col)
        cell.font = totals_font
        if col == 5:  # GMV column
            cell.number_format = 'MYR #,##0.00'
        elif col == 6:  # Commission column
            cell.number_format = 'MYR #,##0.00'
        elif col == 7:  # Rate column
            cell.number_format = '0.00"%"'

print(f"\n\nResults saved to: {output_path}")

