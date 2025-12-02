import pandas as pd

print("SIN NAM HUAT COMMISSION ANALYSIS - ALL OUTLETS")
print("="*80)
print("Brand ID: 60_sin_nam_huat_roasted_chicken_and_duck_rice")
print("Period: Jan-Oct 2025 (YTD)")
print()

# Summary data from query
summary_data = {
    'merchant_id_nk': [
        '1-C2CZTRKGAKLCLT', '1-C2C2MBA2PE3JRE', '1-C2K3TYW3GNDJAN', 
        '1-C2CKA6JYAKKCJX', '1-C2EWE7WYRCKCGJ', '1-C2C2PFEJE76YVN',
        '1-C2L1WFWBGX6FT6', '1-C25VVJLGJU2UCA', '1-C7AUMF2ULXAJRJ',
        '1-C3VZLGBZLZJVNX', '1-C4KVVLDZNJMBWA'
    ],
    'merchant_name': [
        'Sin Nam Huat Roasted Chicken & Duck Rice - Island Glades [Non-Halal]',
        'Sin Nam Huat Roasted Chicken & Duck Rice - Jalan Burma [Non-Halal]',
        'Sin Nam Huat Roasted Chicken & Duck Rice - Persiaran Mahsuri [Non-Halal]',
        'Sin Nam Huat Roasted Chicken & Duck Rice - Jalan Macalister [Non-Halal]',
        'Sin Nam Huat Roasted Chicken & Duck Rice - Ayer Itam [Non-Halal]',
        'Sin Nam Huat Roasted Chicken & Duck Rice - Jalan Fettes [Non-Halal]',
        'Sin Nam Huat Roasted Chicken & Duck Rice - Solok Sungai Pinang [Non-Halal]',
        'Sin Nam Huat Roasted Chicken & Duck Rice - Jalan Bagan Ajam [Non-Halal]',
        'Sin Nam Huat Roasted Chicken & Duck Rice - Lintang Batu Maung 4 [Non-Halal]',
        'Sin Nam Huat Roasted Chicken & Duck Rice - Kedai Kopi Golden Lake [Non-Halal]',
        '[INACTV: COCO] Sin Nam Huat Roasted Chicken & Duck Rice - Lintang Batu Maung 4 [Non-Halal]'
    ],
    'completed_orders': [20805, 8296, 9033, 7466, 7646, 7967, 7207, 5823, 3571, 2540, 530],
    'total_gmv': [793393.77, 305062.28, 300948.39, 281071.84, 279393.70, 263487.17, 262557.44, 199692.97, 140826.65, 82534.52, 18393.18],
    'total_commission_billing': [148724.10, 60058.40, 58936.90, 55573.68, 53650.27, 52086.00, 51172.86, 38457.82, 25825.73, 15913.54, 3447.92],
    'commission_rate_pct': [18.7453, 19.6873, 19.5837, 19.7721, 19.2024, 19.7679, 19.4902, 19.2585, 18.3387, 19.2811, 18.7456]
}

df_summary = pd.DataFrame(summary_data)

# Calculate totals
total_orders = df_summary['completed_orders'].sum()
total_gmv = df_summary['total_gmv'].sum()
total_commission = df_summary['total_commission_billing'].sum()
avg_commission_rate = (total_commission / total_gmv * 100)

print("SUMMARY BY OUTLET (YTD Jan-Oct 2025):")
print("-"*80)
print(df_summary[['merchant_name', 'completed_orders', 'total_gmv', 'total_commission_billing', 'commission_rate_pct']].to_string(index=False))

print(f"\n\nBRAND TOTALS:")
print(f"Total Completed Orders: {total_orders:,}")
print(f"Total GMV: ${total_gmv:,.2f}")
print(f"Total Commission Billing: ${total_commission:,.2f}")
print(f"Average Commission Rate: {avg_commission_rate:.4f}%")

# Save to Excel
output_path = r"C:\Users\benjamin.liang\Downloads\sin_nam_huat_commission_analysis.xlsx"
df_summary.to_excel(output_path, sheet_name='Summary', index=False)
print(f"\n\nResults saved to: {output_path}")

