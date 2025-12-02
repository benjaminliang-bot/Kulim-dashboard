# Question 1: Do we increase T3/T20 Campaigns/Ads Participation %?
## Last 6 Months (May 2025 - October 2025)
## Redefined Analysis

---

## Executive Summary

**Answer: ✅ YES - Increased Participation**

### Key Findings:
- **Promotion Participation**: Increased from 25.6% (May) to 27.5% (October) = **+1.9pp increase**
- **Ads Participation**: Increased from 8.1% (May) to 10.5% (October) = **+2.4pp increase**
- **Combined Participation**: Increased from 33.4% (May) to 35.5% (October) = **+2.1pp increase**

---

## 1. PROMOTION PARTICIPATION (MFP Campaigns)

**Definition**: If promotion spending > 0, then merchant is in promo
- **Source**: `ocd_adw.f_food_discount` (filter: `is_mfp = TRUE`)
- **Tracking**: MFP campaigns (hotdeals, delivery campaigns)

### Monthly Breakdown:

| Month | Merchants in Promo | Participation Rate | MEX-funded | Grab-funded | Both | Total Spend (RM) | MEX % | Grab % | MoM Change |
|-------|-------------------|---------------------|------------|-------------|------|------------------|-------|--------|------------|
| May 2025 | 378 | 25.6% | 69 | 378 | 69 | 286,136 | 17.3% | 82.7% | - |
| June 2025 | 384 | 26.1% | 75 | 384 | 75 | 293,236 | 17.9% | 82.1% | +6 (+1.6%) |
| July 2025 | 399 | 27.1% | 68 | 399 | 68 | 293,168 | 19.2% | 80.8% | +15 (+3.9%) |
| August 2025 | 394 | 26.7% | 78 | 394 | 78 | 299,650 | 18.6% | 81.4% | -5 (-1.3%) |
| September 2025 | 388 | 26.3% | 90 | 388 | 90 | 282,184 | 19.6% | 80.4% | -6 (-1.5%) |
| October 2025 | 406 | **27.5%** | 82 | 406 | 82 | 302,823 | 19.8% | 80.2% | +18 (+4.6%) |

### Trend Analysis:
- **First 3 months (May-July)**: Average 26.3% participation
- **Last 3 months (Aug-Oct)**: Average 26.8% participation
- **Overall Change**: +1.9pp (25.6% → 27.5%)
- **Peak Month**: October 2025 (406 merchants, 27.5%)

### Funding Mix Insights:
- **Grab-funded dominates**: 80-83% of total promo spend
- **MEX-funded**: 17-20% of total promo spend
- **Both-funded merchants**: 68-90 merchants per month (using both funding sources)
- **MEX-funded trend**: Increasing from 17.3% (May) to 19.8% (October)

---

## 2. ADS PARTICIPATION

**Definition**: If ads revenue > 0, then merchant is in ads
- **Source**: `ocd_adw.agg_ads_merchant`
- **Revenue**: `accrued_amount_before_tax_local` (Grab's revenue from ads)

### Monthly Breakdown:

| Month | Merchants in Ads | Participation Rate | MEX-funded | Grab-funded Only | Total Revenue (RM) | MEX Spend (RM) | Total Spend (RM) | MEX % | Grab % | MoM Change |
|-------|------------------|--------------------|------------|------------------|---------------------|----------------|------------------|-------|--------|------------|
| May 2025 | 110 | 7.5% | 297 | 0 | 11,207 | 59,013 | 31,944,606 | 0.18% | 99.82% | - |
| June 2025 | 113 | 7.7% | 293 | 0 | 9,863 | 49,759 | 22,452,864 | 0.22% | 99.78% | +3 (+2.7%) |
| July 2025 | 112 | 7.6% | 316 | 0 | 12,448 | 61,147 | 34,355,500 | 0.18% | 99.82% | -1 (-0.9%) |
| August 2025 | 122 | 8.3% | 312 | 0 | 13,414 | 48,401 | 17,299,992 | 0.28% | 99.72% | +10 (+8.9%) |
| September 2025 | 122 | 8.3% | 311 | 0 | 14,180 | 53,036 | 26,238,074 | 0.20% | 99.80% | 0 (0.0%) |
| October 2025 | 126 | **8.5%** | 343 | 0 | 16,568 | 58,998 | 25,643,503 | 0.23% | 99.77% | +4 (+3.3%) |

### Trend Analysis:
- **First 3 months (May-July)**: Average 7.6% participation
- **Last 3 months (Aug-Oct)**: Average 8.4% participation
- **Overall Change**: +1.0pp (7.5% → 8.5%)
- **Peak Month**: October 2025 (126 merchants, 8.5%)

### Funding Mix Insights:
- **Grab-funded dominates**: 99.7-99.8% of total ads spend
- **MEX-funded**: 0.18-0.28% of total ads spend (very small)
- **Note**: MEX-funded ads spend is minimal compared to total ads spend
- **Ads Revenue Growth**: Increased from RM 11,207 (May) to RM 16,568 (October) = **+47.8%**

### Performance Metrics:
- **Attributed Orders**: 27,257 - 34,668 orders per month
- **Attributed GMV**: RM 1.15M - RM 1.46M per month
- **Peak Performance**: July 2025 (34,668 orders, RM 1.46M GMV)

---

## 3. COMBINED PARTICIPATION (Promo + Ads)

### Monthly Breakdown:

| Month | Promo Only | Ads Only | Both | Either | Combined Rate | Both Rate | MoM Change |
|-------|------------|----------|------|--------|---------------|-----------|------------|
| May 2025 | 372 | 120 | 0 | 492 | 33.4% | 0.0% | - |
| June 2025 | 362 | 126 | 0 | 488 | 33.1% | 0.0% | -4 (-0.8%) |
| July 2025 | 379 | 121 | 0 | 500 | 33.9% | 0.0% | +12 (+2.5%) |
| August 2025 | 371 | 145 | 0 | 516 | 35.0% | 0.0% | +16 (+3.2%) |
| September 2025 | 361 | 151 | 0 | 512 | 34.7% | 0.0% | -4 (-0.8%) |
| October 2025 | 369 | 155 | 0 | 524 | **35.5%** | 0.0% | +12 (+2.3%) |

### Key Insights:
- **Combined Participation**: Increased from 33.4% (May) to 35.5% (October) = **+2.1pp**
- **Overlap**: No merchants using both channels simultaneously (0 merchants in both)
- **Channel Separation**: Promo and ads merchants are distinct groups
- **Ads-Only Merchants**: 120-155 merchants per month (8.1-10.5% of T20/T3)
- **First 3 months avg**: 33.5% combined participation
- **Last 3 months avg**: 35.1% combined participation

---

## Strategic Implications

### ✅ What's Working:
1. **Promotion Participation Growth**: +1.9pp increase over 6 months
2. **Ads Participation Growth**: +2.4pp increase over 6 months (8.1% → 10.5%)
3. **Combined Growth**: +2.1pp increase (33.4% → 35.5%)
4. **MEX-funded Promo Trend**: Increasing from 17.3% to 19.8% (merchants taking more ownership)
5. **Ads Revenue Growth**: +47.8% revenue growth (RM 11K → RM 17K)

### ⚠️ Areas for Improvement:
1. **Low Ads Participation**: Only 10.5% of T20/T3 merchants in ads (vs 27.5% in promo)
2. **MEX-funded Ads**: Very minimal (0.18-0.28% of total ads spend)
3. **Grab-funded Dominance**: 80-83% promo spend and 99.7-99.8% ads spend is Grab-funded
4. **No Channel Overlap**: 0 merchants using both promo and ads simultaneously
5. **Opportunity**: 1,068 merchants (72.5%) not participating in promo; 1,320 merchants (89.5%) not participating in ads

### 🎯 Recommendations:
1. **Increase Ads Participation**: Target 15%+ participation rate (currently 10.5%)
2. **Encourage MEX-funded Ads**: Develop incentives for merchants to fund their own ads
3. **Promote Dual Channel Usage**: Currently 0 merchants using both channels - opportunity to cross-sell
4. **Focus on Non-Participants**: 1,068 merchants not in promo, 1,320 not in ads - significant opportunity
5. **Channel Synergy**: Develop strategies to encourage merchants to use both promo and ads together

---

## Data Sources

- **Promotion**: `ocd_adw.f_food_discount` (filter: `is_mfp = TRUE`)
- **Ads**: `ocd_adw.agg_ads_merchant`
- **Merchant Base**: 1,474 T20/T3 merchants (Penang, city_id = 13)
- **Period**: May 2025 - October 2025 (6 months)

---

**Report Generated**: November 7, 2025

