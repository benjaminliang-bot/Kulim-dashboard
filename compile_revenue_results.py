"""
Compile revenue breakdown results and generate final report
"""

import json
import sys
import io

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Results collected so far
results = {
    'Darren': {
        'role': 'AM',
        'portfolio': 189,
        'months': [
            {'month': 'May 2025', 'month_id': 202505, 'commission': 822619.14, 'ads': 63722.72, 'mex_campaign': 145961.72, 'total': 886341.86, 'gmv': 3818126.89, 'orders': 93891, 'active_merchants': 167, 'commission_pct': 92.81, 'ads_pct': 7.19},
            {'month': 'Jun 2025', 'month_id': 202506, 'commission': 838588.93, 'ads': 70659.32, 'mex_campaign': 157718.31, 'total': 909248.25, 'gmv': 3782022.57, 'orders': 92125, 'active_merchants': 168, 'commission_pct': 92.23, 'ads_pct': 7.77},
            {'month': 'Jul 2025', 'month_id': 202507, 'commission': 885758.69, 'ads': 70994.26, 'mex_campaign': 193760.53, 'total': 956752.95, 'gmv': 3983335.69, 'orders': 97568, 'active_merchants': 168, 'commission_pct': 92.58, 'ads_pct': 7.42},
            {'month': 'Aug 2025', 'month_id': 202508, 'commission': 964158.67, 'ads': 79982.54, 'mex_campaign': 217404.85, 'total': 1044141.21, 'gmv': 4317883.35, 'orders': 102763, 'active_merchants': 168, 'commission_pct': 92.34, 'ads_pct': 7.66},
            {'month': 'Sep 2025', 'month_id': 202509, 'commission': 919084.43, 'ads': 88457.65, 'mex_campaign': 201575.27, 'total': 1007542.08, 'gmv': 4071390.15, 'orders': 97308, 'active_merchants': 168, 'commission_pct': 91.22, 'ads_pct': 8.78},
            {'month': 'Oct 2025', 'month_id': 202510, 'commission': 950781.59, 'ads': 70516.11, 'mex_campaign': 211302.45, 'total': 1021297.70, 'gmv': 4244822.18, 'orders': 100770, 'active_merchants': 167, 'commission_pct': 93.10, 'ads_pct': 6.90},
        ]
    },
    'Suki': {
        'role': 'AM',
        'portfolio': 162,
        'months': [
            {'month': 'May 2025', 'month_id': 202505, 'commission': 762131.82, 'ads': 38303.62, 'mex_campaign': 116682.74, 'total': 800435.44, 'gmv': 3278345.18, 'orders': 87043, 'active_merchants': 156, 'commission_pct': 95.21, 'ads_pct': 4.79},
            {'month': 'Jun 2025', 'month_id': 202506, 'commission': 744595.46, 'ads': 38695.02, 'mex_campaign': 119062.85, 'total': 783290.48, 'gmv': 3195794.08, 'orders': 83095, 'active_merchants': 156, 'commission_pct': 95.06, 'ads_pct': 4.94},
            {'month': 'Jul 2025', 'month_id': 202507, 'commission': 764516.98, 'ads': 34865.93, 'mex_campaign': 127694.82, 'total': 799382.91, 'gmv': 3261915.32, 'orders': 86962, 'active_merchants': 156, 'commission_pct': 95.64, 'ads_pct': 4.36},
            {'month': 'Aug 2025', 'month_id': 202508, 'commission': 827088.38, 'ads': 47826.60, 'mex_campaign': 142986.97, 'total': 874914.98, 'gmv': 3518282.08, 'orders': 90463, 'active_merchants': 158, 'commission_pct': 94.53, 'ads_pct': 5.47},
            {'month': 'Sep 2025', 'month_id': 202509, 'commission': 789817.63, 'ads': 48565.61, 'mex_campaign': 146670.56, 'total': 838383.24, 'gmv': 3352969.58, 'orders': 85830, 'active_merchants': 158, 'commission_pct': 94.21, 'ads_pct': 5.79},
            {'month': 'Oct 2025', 'month_id': 202510, 'commission': 815770.23, 'ads': 48173.70, 'mex_campaign': 160268.54, 'total': 863943.93, 'gmv': 3475061.18, 'orders': 88896, 'active_merchants': 157, 'commission_pct': 94.42, 'ads_pct': 5.58},
        ]
    },
    'Chia Yee': {
        'role': 'AM',
        'portfolio': 186,
        'months': [
            {'month': 'May 2025', 'month_id': 202505, 'commission': 1126782.20, 'ads': 61999.90, 'mex_campaign': 252082.98, 'total': 1188782.10, 'gmv': 5127841.41, 'orders': 109284, 'active_merchants': 167, 'commission_pct': 94.78, 'ads_pct': 5.22},
            {'month': 'Jun 2025', 'month_id': 202506, 'commission': 1111240.93, 'ads': 53233.36, 'mex_campaign': 252225.16, 'total': 1164474.29, 'gmv': 4960653.34, 'orders': 104835, 'active_merchants': 168, 'commission_pct': 95.43, 'ads_pct': 4.57},
            {'month': 'Jul 2025', 'month_id': 202507, 'commission': 1159485.23, 'ads': 50024.11, 'mex_campaign': 301151.90, 'total': 1209509.34, 'gmv': 5203546.94, 'orders': 108892, 'active_merchants': 173, 'commission_pct': 95.86, 'ads_pct': 4.14},
            {'month': 'Aug 2025', 'month_id': 202508, 'commission': 1178772.24, 'ads': 60630.99, 'mex_campaign': 279301.49, 'total': 1239403.23, 'gmv': 5291476.35, 'orders': 108824, 'active_merchants': 173, 'commission_pct': 95.11, 'ads_pct': 4.89},
            {'month': 'Sep 2025', 'month_id': 202509, 'commission': 1156427.07, 'ads': 60477.49, 'mex_campaign': 269147.85, 'total': 1216904.56, 'gmv': 5182328.31, 'orders': 105981, 'active_merchants': 174, 'commission_pct': 95.03, 'ads_pct': 4.97},
            {'month': 'Oct 2025', 'month_id': 202510, 'commission': 1140759.83, 'ads': 59248.30, 'mex_campaign': 268458.11, 'total': 1200008.13, 'gmv': 5152701.15, 'orders': 107498, 'active_merchants': 174, 'commission_pct': 95.06, 'ads_pct': 4.94},
        ]
    }
}

# Calculate 6-month totals
for person, data in results.items():
    total_commission = sum(m['commission'] for m in data['months'])
    total_ads = sum(m['ads'] for m in data['months'])
    total_revenue = total_commission + total_ads
    total_mex_campaign = sum(m['mex_campaign'] for m in data['months'])
    total_gmv = sum(m['gmv'] for m in data['months'])
    total_orders = sum(m['orders'] for m in data['months'])
    
    data['totals'] = {
        'commission': total_commission,
        'ads': total_ads,
        'total_revenue': total_revenue,
        'mex_campaign': total_mex_campaign,
        'gmv': total_gmv,
        'orders': total_orders,
        'commission_pct': round(total_commission * 100.0 / total_revenue, 2) if total_revenue > 0 else 0,
        'ads_pct': round(total_ads * 100.0 / total_revenue, 2) if total_revenue > 0 else 0
    }

# Save results
with open('revenue_results_partial.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("="*80)
print("REVENUE BREAKDOWN RESULTS (Partial - AMs Only)")
print("="*80)

for person, data in results.items():
    print(f"\n{person} ({data['role']}) - Portfolio: {data['portfolio']} merchants")
    print(f"  6-Month Total Revenue: RM {data['totals']['total_revenue']:,.2f}")
    print(f"    Commission: RM {data['totals']['commission']:,.2f} ({data['totals']['commission_pct']}%)")
    print(f"    Ads: RM {data['totals']['ads']:,.2f} ({data['totals']['ads_pct']}%)")
    print(f"  MEX Campaign Spend: RM {data['totals']['mex_campaign']:,.2f}")
    print(f"  Total GMV: RM {data['totals']['gmv']:,.2f}")
    print(f"  Total Orders: {data['totals']['orders']:,}")

print("\n[INFO] MGS queries still need to be executed")
print("[INFO] Results saved to: revenue_results_partial.json")





