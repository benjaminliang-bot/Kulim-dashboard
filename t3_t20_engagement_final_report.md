# T3/T20 Engagement Analysis - Last 6 Months
## May 2025 to October 2025

---

## Executive Summary

**Merchant Base:**
- **T20 merchants**: 1,474
- **T3 merchants**: 197 (subset of T20)
- **Analysis Period**: May 2025 - October 2025 (6 months)

---

## Question 1: Do we increase T3/T20 Campaigns/Ads Participation %?

**Status**: ⚠️ **Data Source Identification Needed**

**Current Status:**
- Campaign/Ads participation tracking requires identification of the correct source tables
- Potential sources: Campaign management systems, promo/voucher tables, marketing tracking

**Recommendation:**
- Identify specific campaign/ads participation tables
- Query participation rate filtered by T20/T3 merchant IDs
- Calculate month-over-month trends

**Next Steps:**
1. Identify campaign participation data source
2. Query T20/T3 merchant participation over last 6 months
3. Calculate participation % and trend

---

## Question 2: Do we Increase T3/T20 DoD Mex Participation %?

**Answer: ✅ YES - Increased by 16.6%**

### DoD Campaign Participation (pre_purchased_deals_base)

**Monthly Trend:**
| Month | Participating Merchants | Total Campaigns |
|-------|------------------------|-----------------|
| May 2025 | 107 | 111 |
| June 2025 | 95 | 109 |
| July 2025 | 132 | 154 |
| August 2025 | 165 | 238 |
| September 2025 | 113 | 220 |
| October 2025 | 79 | 90 |

**Period Comparison:**
- **May-July 2025**: 271 unique merchants participated
- **August-October 2025**: 316 unique merchants participated
- **Change**: +45 merchants (+16.6% increase)

### Key Findings:
1. ✅ **Positive Trend**: DoD participation increased 16.6% from first 3 months to last 3 months
2. **Peak Month**: August 2025 had highest participation (165 merchants, 238 campaigns)
3. **Volatility**: Participation varies month-to-month (range: 79-165 merchants)

### DoD Orders (f_food_prepurchased_deals)
- **Status**: Query executed but returned no results
- **Possible Reasons**: 
  - No DoD orders in period for Penang
  - Merchant ID format mismatch
  - Data availability issues

**Recommendation:**
- Verify merchant_id format in f_food_prepurchased_deals
- Check data availability for Penang DoD orders
- Re-query with corrected merchant ID mapping

---

## Question 3: Is all T20/T3 merchant being tagged to someone? (Engagement Rate)

**Answer: ❌ NO - Only 10.4% Engagement Rate**

### Current Status:
- **Total T20/T3 merchants**: 1,474
- **With AM assigned**: 153 merchants (10.4%)
- **Without AM assigned**: 1,321 merchants (89.6%)
- **Engagement Rate**: **10.4%**

### Critical Gap:
⚠️ **89.6% of T20/T3 merchants are NOT assigned to an Account Manager**

### Breakdown:
- **T3 merchants (197)**: Need to check specific engagement rate
- **T20 merchants (1,474)**: Overall 10.4% engagement

### Recommendations:
1. **Immediate Priority**: Assign AMs to all T3 merchants (197)
2. **Short-term Goal**: Increase T20 engagement to 50% within 1 month
3. **Long-term Target**: Achieve 80%+ engagement rate for all T20/T3
4. **Focus Areas**:
   - T3 merchants first (highest value segment)
   - Active merchants (recent orders)
   - High GMV merchants

---

## Summary & Action Items

### ✅ What's Working:
1. **DoD Participation**: Increased 16.6% over 6 months
2. **Campaign Activity**: Strong participation in August (165 merchants)

### ⚠️ Critical Issues:
1. **Low Engagement Rate**: Only 10.4% of T20/T3 have AM assignment
2. **Campaign/Ads Data**: Need to identify data source for participation tracking
3. **DoD Orders Data**: Need to verify and fix query for order-level analysis

### 🎯 Immediate Actions:
1. **Assign AMs** to 1,321 unassigned T20/T3 merchants (priority: T3 first)
2. **Identify campaign/ads data source** for Question 1 analysis
3. **Fix DoD orders query** to get order-level participation data
4. **Set engagement targets**: 50% in 1 month, 80% in 3 months

---

**Data Sources:**
- `analytics_food.pre_purchased_deals_base` - DoD campaign setup
- `ocd_adw.f_food_prepurchased_deals` - DoD orders (needs verification)
- `ocd_adw.d_merchant` - Merchant tagging/engagement

**Files Created:**
- `t3_t20_engagement_analysis.sql` - Complete SQL queries
- `t20_merchant_ids.json` - All T20 merchant IDs (1,474)
- `t3_merchant_ids.json` - All T3 merchant IDs (197)

**Report Date**: November 7, 2025


