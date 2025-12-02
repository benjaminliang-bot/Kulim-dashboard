"""
Analyze BD and KVAM GMV % Trends
Determine if contribution is reducing or not
"""

# BD GMV % data
bd_gmv_pct = {
    'May 2025': 29.01,
    'June 2025': 29.16,
    'July 2025': 29.78,
    'August 2025': 28.91,
    'September 2025': 29.67,
    'October 2025': 29.68
}

# KVAM GMV % data
kvam_gmv_pct = {
    'May 2025': 27.28,
    'June 2025': 27.54,
    'July 2025': 27.03,
    'August 2025': 28.09,
    'September 2025': 27.84,
    'October 2025': 27.31
}

print("="*80)
print("BD & KVAM GMV % TREND ANALYSIS")
print("="*80)

# Calculate first 3 months vs last 3 months
bd_first_3 = (bd_gmv_pct['May 2025'] + bd_gmv_pct['June 2025'] + bd_gmv_pct['July 2025']) / 3
bd_last_3 = (bd_gmv_pct['August 2025'] + bd_gmv_pct['September 2025'] + bd_gmv_pct['October 2025']) / 3
bd_change = bd_last_3 - bd_first_3

kvam_first_3 = (kvam_gmv_pct['May 2025'] + kvam_gmv_pct['June 2025'] + kvam_gmv_pct['July 2025']) / 3
kvam_last_3 = (kvam_gmv_pct['August 2025'] + kvam_gmv_pct['September 2025'] + kvam_gmv_pct['October 2025']) / 3
kvam_change = kvam_last_3 - kvam_first_3

# Calculate overall trend (start vs end)
bd_start_end = bd_gmv_pct['October 2025'] - bd_gmv_pct['May 2025']
kvam_start_end = kvam_gmv_pct['October 2025'] - kvam_gmv_pct['May 2025']

# Calculate linear trend (simple regression)
months = list(range(1, 7))  # May = 1, Oct = 6
bd_values = list(bd_gmv_pct.values())
kvam_values = list(kvam_gmv_pct.values())

# Simple linear regression: y = a + b*x
# b = (n*sum(xy) - sum(x)*sum(y)) / (n*sum(x^2) - (sum(x))^2)
n = len(months)
bd_sum_x = sum(months)
bd_sum_y = sum(bd_values)
bd_sum_xy = sum(x * y for x, y in zip(months, bd_values))
bd_sum_x2 = sum(x * x for x in months)
bd_slope = (n * bd_sum_xy - bd_sum_x * bd_sum_y) / (n * bd_sum_x2 - bd_sum_x * bd_sum_x)

kvam_sum_x = sum(months)
kvam_sum_y = sum(kvam_values)
kvam_sum_xy = sum(x * y for x, y in zip(months, kvam_values))
kvam_sum_x2 = sum(x * x for x in months)
kvam_slope = (n * kvam_sum_xy - kvam_sum_x * kvam_sum_y) / (n * kvam_sum_x2 - kvam_sum_x * kvam_sum_x)

print("\n1. BD GMV % TREND ANALYSIS")
print("-" * 80)
print(f"First 3 months average: {bd_first_3:.2f}%")
print(f"Last 3 months average: {bd_last_3:.2f}%")
print(f"Change: {bd_change:+.2f}pp")
print(f"\nStart (May): {bd_gmv_pct['May 2025']:.2f}%")
print(f"End (October): {bd_gmv_pct['October 2025']:.2f}%")
print(f"Overall change: {bd_start_end:+.2f}pp")
print(f"\nLinear trend slope: {bd_slope:+.4f}pp per month")
print(f"Projected annual change: {bd_slope * 12:+.2f}pp")

if bd_slope > 0:
    print("\n[CONCLUSION] BD GMV % is INCREASING in trend")
elif bd_slope < 0:
    print("\n[CONCLUSION] BD GMV % is DECREASING in trend")
else:
    print("\n[CONCLUSION] BD GMV % is STABLE (no trend)")

print("\n2. KVAM GMV % TREND ANALYSIS")
print("-" * 80)
print(f"First 3 months average: {kvam_first_3:.2f}%")
print(f"Last 3 months average: {kvam_last_3:.2f}%")
print(f"Change: {kvam_change:+.2f}pp")
print(f"\nStart (May): {kvam_gmv_pct['May 2025']:.2f}%")
print(f"End (October): {kvam_gmv_pct['October 2025']:.2f}%")
print(f"Overall change: {kvam_start_end:+.2f}pp")
print(f"\nLinear trend slope: {kvam_slope:+.4f}pp per month")
print(f"Projected annual change: {kvam_slope * 12:+.2f}pp")

if kvam_slope > 0:
    print("\n[CONCLUSION] KVAM GMV % is INCREASING in trend")
elif kvam_slope < 0:
    print("\n[CONCLUSION] KVAM GMV % is DECREASING in trend")
else:
    print("\n[CONCLUSION] KVAM GMV % is STABLE (no trend)")

print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print(f"BD GMV %: {'INCREASING' if bd_slope > 0 else 'DECREASING' if bd_slope < 0 else 'STABLE'} trend")
print(f"KVAM GMV %: {'INCREASING' if kvam_slope > 0 else 'DECREASING' if kvam_slope < 0 else 'STABLE'} trend")


