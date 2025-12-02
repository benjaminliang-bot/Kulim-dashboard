"""
Analyze Ads Revenue Potential
Based on collected revenue breakdown data
"""

import json
import sys
import io

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Load results
with open('revenue_results_partial.json', 'r', encoding='utf-8') as f:
    results = json.load(f)

print("="*80)
print("ADS REVENUE POTENTIAL ANALYSIS")
print("="*80)

# Calculate ads revenue metrics
ads_analysis = {}

for person, data in results.items():
    months = data['months']
    
    # Calculate monthly ads revenue growth
    ads_revenue_trend = [m['ads'] for m in months]
    first_month_ads = ads_revenue_trend[0]
    last_month_ads = ads_revenue_trend[-1]
    ads_growth = ((last_month_ads - first_month_ads) / first_month_ads * 100) if first_month_ads > 0 else 0
    
    # Calculate ads revenue as % of GMV
    total_gmv = data['totals']['gmv']
    total_ads = data['totals']['ads']
    ads_as_pct_of_gmv = (total_ads / total_gmv * 100) if total_gmv > 0 else 0
    
    # Calculate commission as % of GMV (for comparison)
    total_commission = data['totals']['commission']
    commission_as_pct_of_gmv = (total_commission / total_gmv * 100) if total_gmv > 0 else 0
    
    # Calculate average ads revenue per merchant
    avg_merchants = sum(m['active_merchants'] for m in months) / len(months)
    ads_per_merchant = total_ads / avg_merchants if avg_merchants > 0 else 0
    
    # Calculate ads revenue per order
    total_orders = data['totals']['orders']
    ads_per_order = total_ads / total_orders if total_orders > 0 else 0
    
    ads_analysis[person] = {
        'total_ads': total_ads,
        'ads_pct_of_revenue': data['totals']['ads_pct'],
        'ads_pct_of_gmv': ads_as_pct_of_gmv,
        'commission_pct_of_gmv': commission_as_pct_of_gmv,
        'ads_growth_6m': ads_growth,
        'ads_per_merchant': ads_per_merchant,
        'ads_per_order': ads_per_order,
        'first_month_ads': first_month_ads,
        'last_month_ads': last_month_ads,
        'monthly_trend': ads_revenue_trend,
        'portfolio_size': data['portfolio']
    }

# Print analysis
print("\n1. CURRENT ADS REVENUE PERFORMANCE")
print("-" * 80)

print("\nTotal Ads Revenue (6 Months):")
for person, analysis in sorted(ads_analysis.items(), key=lambda x: x[1]['total_ads'], reverse=True):
    print(f"  {person:15s}: RM {analysis['total_ads']:>12,.2f} ({analysis['ads_pct_of_revenue']:>5.2f}% of total revenue)")

print("\nAds Revenue as % of GMV:")
for person, analysis in sorted(ads_analysis.items(), key=lambda x: x[1]['ads_pct_of_gmv'], reverse=True):
    print(f"  {person:15s}: {analysis['ads_pct_of_gmv']:>5.2f}% of GMV")

print("\n2. ADS REVENUE GROWTH TRENDS")
print("-" * 80)

for person, analysis in sorted(ads_analysis.items(), key=lambda x: x[1]['ads_growth_6m'], reverse=True):
    growth_icon = "📈" if analysis['ads_growth_6m'] > 0 else "📉" if analysis['ads_growth_6m'] < 0 else "➡️"
    print(f"\n{person}:")
    print(f"  {growth_icon} 6-Month Growth: {analysis['ads_growth_6m']:>6.2f}%")
    print(f"     First Month (May): RM {analysis['first_month_ads']:>10,.2f}")
    print(f"     Last Month (Oct):  RM {analysis['last_month_ads']:>10,.2f}")
    trend_str = ', '.join([f"{x:,.0f}" for x in analysis['monthly_trend']])
    print(f"     Monthly Trend: [{trend_str}]")

print("\n3. ADS REVENUE EFFICIENCY")
print("-" * 80)

print("\nAds Revenue per Merchant (6-month average):")
for person, analysis in sorted(ads_analysis.items(), key=lambda x: x[1]['ads_per_merchant'], reverse=True):
    print(f"  {person:15s}: RM {analysis['ads_per_merchant']:>10,.2f} per merchant")

print("\nAds Revenue per Order:")
for person, analysis in sorted(ads_analysis.items(), key=lambda x: x[1]['ads_per_order'], reverse=True):
    print(f"  {person:15s}: RM {analysis['ads_per_order']:>6.4f} per order")

print("\n4. COMPARISON: COMMISSION vs ADS REVENUE")
print("-" * 80)

for person, analysis in ads_analysis.items():
    commission_pct = results[person]['totals']['commission_pct']
    ads_pct = analysis['ads_pct_of_revenue']
    ratio = commission_pct / ads_pct if ads_pct > 0 else 0
    print(f"\n{person}:")
    print(f"  Commission: {commission_pct:>5.2f}% of revenue (RM {results[person]['totals']['commission']:>12,.2f})")
    print(f"  Ads:         {ads_pct:>5.2f}% of revenue (RM {analysis['total_ads']:>12,.2f})")
    print(f"  Ratio:       {ratio:>5.1f}:1 (Commission:Ads)")

print("\n5. POTENTIAL OPPORTUNITIES")
print("-" * 80)

# Find highest and lowest ads revenue performers
highest_ads = max(ads_analysis.items(), key=lambda x: x[1]['ads_pct_of_revenue'])
lowest_ads = min(ads_analysis.items(), key=lambda x: x[1]['ads_pct_of_revenue'])
highest_growth = max(ads_analysis.items(), key=lambda x: x[1]['ads_growth_6m'])

print(f"\n📊 Key Insights:")
print(f"  • Highest Ads Revenue %: {highest_ads[0]} ({highest_ads[1]['ads_pct_of_revenue']:.2f}%)")
print(f"  • Lowest Ads Revenue %:  {lowest_ads[0]} ({lowest_ads[1]['ads_pct_of_revenue']:.2f}%)")
print(f"  • Highest Growth:        {highest_growth[0]} ({highest_growth[1]['ads_growth_6m']:+.2f}%)")

# Calculate potential if all reach highest performer's level
highest_pct = highest_ads[1]['ads_pct_of_revenue']
total_current_ads = sum(a['total_ads'] for a in ads_analysis.values())
total_current_revenue = sum(results[p]['totals']['total_revenue'] for p in results.keys())

potential_ads_if_all_match = total_current_revenue * (highest_pct / 100)
additional_potential = potential_ads_if_all_match - total_current_ads

print(f"\n💡 Potential Analysis:")
print(f"  • Current Total Ads Revenue: RM {total_current_ads:,.2f}")
print(f"  • If all reach {highest_ads[0]}'s level ({highest_pct:.2f}%): RM {potential_ads_if_all_match:,.2f}")
print(f"  • Additional Potential:       RM {additional_potential:,.2f} ({additional_potential/total_current_ads*100:.1f}% increase)")

# Calculate average ads revenue % across all
avg_ads_pct = sum(a['ads_pct_of_revenue'] for a in ads_analysis.values()) / len(ads_analysis)
print(f"  • Average Ads Revenue %:     {avg_ads_pct:.2f}%")
print(f"  • Range:                     {lowest_ads[1]['ads_pct_of_revenue']:.2f}% - {highest_ads[1]['ads_pct_of_revenue']:.2f}%")

print("\n6. RECOMMENDATIONS")
print("-" * 80)

print(f"\n✅ For {lowest_ads[0]} (Lowest Ads Revenue %):")
print(f"   • Current: {lowest_ads[1]['ads_pct_of_revenue']:.2f}% of revenue")
print(f"   • Opportunity: Increase to {highest_ads[1]['ads_pct_of_revenue']:.2f}% = +RM {results[lowest_ads[0]]['totals']['total_revenue'] * (highest_ads[1]['ads_pct_of_revenue'] - lowest_ads[1]['ads_pct_of_revenue']) / 100:,.2f} potential")

print(f"\n✅ For {highest_growth[0]} (Highest Growth):")
print(f"   • Growth: {highest_growth[1]['ads_growth_6m']:+.2f}%")
print(f"   • Replicate strategies to other individuals")

print(f"\n✅ Overall Strategy:")
print(f"   • Current ads revenue is {avg_ads_pct:.2f}% of total revenue")
print(f"   • Commission revenue dominates at ~{100-avg_ads_pct:.2f}%")
print(f"   • Significant opportunity to grow ads revenue by {additional_potential/total_current_ads*100:.1f}%")

# Save analysis
with open('ads_revenue_potential_analysis.json', 'w', encoding='utf-8') as f:
    json.dump(ads_analysis, f, indent=2, ensure_ascii=False)

print("\n[OK] Analysis saved to: ads_revenue_potential_analysis.json")

