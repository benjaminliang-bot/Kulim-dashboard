import pandas as pd

# Commission data with merchant_id
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
df = df.sort_values('total_commission_billing_myr', ascending=False)

print("="*100)
print("SIN NAM HUAT COMMISSION ANALYSIS - ALL OUTLETS WITH MERCHANT_ID")
print("="*100)
print("Brand ID: 60_sin_nam_huat_roasted_chicken_and_duck_rice")
print("Period: Jan-Oct 2025 (YTD)")
print("Currency: MYR (Malaysian Ringgit)")
print("="*100)
print()

# Display with merchant_id first
for idx, row in df.iterrows():
    print(f"Merchant ID: {row['merchant_id']}")
    print(f"Merchant ID NK: {row['merchant_id_nk']}")
    print(f"Outlet: {row['merchant_name']}")
    print(f"  - Completed Orders: {row['completed_orders']:,}")
    print(f"  - Total GMV: MYR {row['total_gmv_myr']:,.2f}")
    print(f"  - Commission Billing: MYR {row['total_commission_billing_myr']:,.2f}")
    print(f"  - Commission Rate: {row['commission_rate_pct']:.2f}%")
    print("-" * 100)

# Summary table
print("\n\nSUMMARY TABLE:")
print("="*100)
summary_cols = ['merchant_id', 'merchant_id_nk', 'merchant_name', 'total_commission_billing_myr']
summary_df = df[summary_cols].copy()
summary_df['total_commission_billing_myr'] = summary_df['total_commission_billing_myr'].apply(lambda x: f'MYR {x:,.2f}')
print(summary_df.to_string(index=False))

# Totals
print(f"\n\nTOTALS:")
print(f"Total Outlets: {len(df)}")
print(f"Total Completed Orders: {df['completed_orders'].sum():,}")
print(f"Total GMV: MYR {df['total_gmv_myr'].sum():,.2f}")
print(f"Total Commission Billing: MYR {df['total_commission_billing_myr'].sum():,.2f}")
print(f"Average Commission Rate: {(df['total_commission_billing_myr'].sum() / df['total_gmv_myr'].sum() * 100):.2f}%")

