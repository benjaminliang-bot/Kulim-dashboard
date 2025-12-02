"""
Compile MGS Individual Impact Analysis
Using results from executed queries
"""

# Results from executed queries
mgs_results = {
    'Teoh Jun Ling': [
        {'month_id': 202505, 'unique_merchants': 522, 'orders': 85527, 'unique_eaters': 49907, 'gmv': 3217887.46, 'total_penang_gmv': 44803729.06, 'gmv_pct_of_penang': 7.18, 'avg_gmv_per_merchant': 6164.54, 'avg_gmv_per_order': 37.62, 'avg_gmv_per_eater': 64.48},
        {'month_id': 202506, 'unique_merchants': 520, 'orders': 83413, 'unique_eaters': 49403, 'gmv': 3092592.22, 'total_penang_gmv': 43356803.19, 'gmv_pct_of_penang': 7.13, 'avg_gmv_per_merchant': 5947.29, 'avg_gmv_per_order': 37.08, 'avg_gmv_per_eater': 62.6},
        {'month_id': 202507, 'unique_merchants': 519, 'orders': 86593, 'unique_eaters': 49862, 'gmv': 3149536.15, 'total_penang_gmv': 46058006.24, 'gmv_pct_of_penang': 6.84, 'avg_gmv_per_merchant': 6068.47, 'avg_gmv_per_order': 36.37, 'avg_gmv_per_eater': 63.17},
        {'month_id': 202508, 'unique_merchants': 521, 'orders': 83315, 'unique_eaters': 48540, 'gmv': 3090355.18, 'total_penang_gmv': 46740658.95, 'gmv_pct_of_penang': 6.61, 'avg_gmv_per_merchant': 5931.58, 'avg_gmv_per_order': 37.09, 'avg_gmv_per_eater': 63.67},
        {'month_id': 202509, 'unique_merchants': 525, 'orders': 78494, 'unique_eaters': 47085, 'gmv': 2926927.08, 'total_penang_gmv': 45276009.59, 'gmv_pct_of_penang': 6.46, 'avg_gmv_per_merchant': 5575.1, 'avg_gmv_per_order': 37.29, 'avg_gmv_per_eater': 62.16},
        {'month_id': 202510, 'unique_merchants': 520, 'orders': 80099, 'unique_eaters': 47860, 'gmv': 2988747.94, 'total_penang_gmv': 47130906.33, 'gmv_pct_of_penang': 6.34, 'avg_gmv_per_merchant': 5747.59, 'avg_gmv_per_order': 37.31, 'avg_gmv_per_eater': 62.45}
    ],
    'Lee Sook Chin': [
        {'month_id': 202505, 'unique_merchants': 287, 'orders': 26810, 'unique_eaters': 10813, 'gmv': 709525.75, 'total_penang_gmv': 44803729.06, 'gmv_pct_of_penang': 1.58, 'avg_gmv_per_merchant': 2472.22, 'avg_gmv_per_order': 26.46, 'avg_gmv_per_eater': 65.62},
        {'month_id': 202506, 'unique_merchants': 282, 'orders': 24616, 'unique_eaters': 10315, 'gmv': 660961.92, 'total_penang_gmv': 43356803.19, 'gmv_pct_of_penang': 1.52, 'avg_gmv_per_merchant': 2343.84, 'avg_gmv_per_order': 26.85, 'avg_gmv_per_eater': 64.08},
        {'month_id': 202507, 'unique_merchants': 283, 'orders': 25808, 'unique_eaters': 10070, 'gmv': 679654.92, 'total_penang_gmv': 46058006.24, 'gmv_pct_of_penang': 1.48, 'avg_gmv_per_merchant': 2401.61, 'avg_gmv_per_order': 26.34, 'avg_gmv_per_eater': 67.49},
        {'month_id': 202508, 'unique_merchants': 285, 'orders': 27101, 'unique_eaters': 10899, 'gmv': 734287.68, 'total_penang_gmv': 46740658.95, 'gmv_pct_of_penang': 1.57, 'avg_gmv_per_merchant': 2576.45, 'avg_gmv_per_order': 27.09, 'avg_gmv_per_eater': 67.37},
        {'month_id': 202509, 'unique_merchants': 291, 'orders': 25566, 'unique_eaters': 10645, 'gmv': 683108.33, 'total_penang_gmv': 45276009.59, 'gmv_pct_of_penang': 1.51, 'avg_gmv_per_merchant': 2347.45, 'avg_gmv_per_order': 26.72, 'avg_gmv_per_eater': 64.17},
        {'month_id': 202510, 'unique_merchants': 284, 'orders': 28042, 'unique_eaters': 11444, 'gmv': 755734.86, 'total_penang_gmv': 47130906.33, 'gmv_pct_of_penang': 1.6, 'avg_gmv_per_merchant': 2661.04, 'avg_gmv_per_order': 26.95, 'avg_gmv_per_eater': 66.04}
    ]
}

# Calculate 6-month totals and averages
print("="*80)
print("MGS INDIVIDUAL IMPACT ANALYSIS - PENANG")
print("Last 6 Months (May 2025 - October 2025)")
print("="*80)

for mgs_name, monthly_data in mgs_results.items():
    total_gmv = sum(m['gmv'] for m in monthly_data)
    total_orders = sum(m['orders'] for m in monthly_data)
    total_eaters = sum(m['unique_eaters'] for m in monthly_data)
    avg_merchants = sum(m['unique_merchants'] for m in monthly_data) / len(monthly_data)
    avg_gmv_pct = sum(m['gmv_pct_of_penang'] for m in monthly_data) / len(monthly_data)
    
    first_3m_gmv = sum(m['gmv'] for m in monthly_data[:3])
    last_3m_gmv = sum(m['gmv'] for m in monthly_data[3:])
    growth_rate = ((last_3m_gmv - first_3m_gmv) / first_3m_gmv * 100) if first_3m_gmv > 0 else 0
    
    print(f"\n{mgs_name}:")
    print(f"  Total GMV (6 months): RM {total_gmv:,.2f}")
    print(f"  Avg % of Penang GMV: {avg_gmv_pct:.2f}%")
    print(f"  Avg Unique Merchants: {avg_merchants:.0f}")
    print(f"  Total Orders: {total_orders:,}")
    print(f"  Total Unique Eaters: {total_eaters:,}")
    print(f"  Avg GMV per Merchant: RM {total_gmv / avg_merchants / 6:,.2f}")
    print(f"  Avg GMV per Order: RM {total_gmv / total_orders:,.2f}")
    print(f"  Avg GMV per Eater: RM {total_gmv / total_eaters:,.2f}")
    print(f"  Growth Rate (Last 3m vs First 3m): {growth_rate:+.2f}%")

print("\n[INFO] Note: Low Jia Ying and Hon Yi Ni queries need to be executed")
print("       Once executed, full analysis will be compiled")

