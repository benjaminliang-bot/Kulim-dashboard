# T3/T20 Engagement Analysis - Complete Report
## Last 6 Months (May 2025 - October 2025)

---

## Executive Summary

**Merchant Base:**
- **T20 merchants**: 1,474
- **T3 merchants**: 197 (subset of T20)
- **Analysis Period**: May 2025 - October 2025

---

## Question 1: Do we increase T3/T20 Campaigns/Ads Participation %?

**Answer Tables Identified:**
1. **`ocd_adw.d_merchant_funded_campaign`** - Campaign creation/participation
2. **`ocd_adw.f_food_discount`** - Campaign usage/redemption (filter: `is_mfc = TRUE`)

### Sample Results (30 T20/T3 Merchants):

**Campaign Creation (d_merchant_funded_campaign):**
| Month | Participating Merchants | Total Campaigns | MoM Change |
|-------|------------------------|------------------|------------|
| May 2025 | 15 | 118 | - |
| June 2025 | 15 | 107 | 0 (0.0%) |
| July 2025 | 14 | 123 | -1 (-6.7%) |
| August 2025 | 16 | 186 | +2 (+14.3%) |
| September 2025 | 16 | 108 | 0 (0.0%) |
| October 2025 | 15 | 89 | -1 (-6.3%) |

**Campaign Usage (f_food_discount - is_mfc = TRUE):**
| Month | Merchants with Usage | Orders with Campaigns | Total Discount |
|-------|---------------------|----------------------|----------------|
| May 2025 | 17 | 2,341 | RM 40,482 |
| June 2025 | 16 | 2,439 | RM 39,096 |
| July 2025 | 11 | 1,659 | RM 32,688 |
| August 2025 | 15 | 3,597 | RM 53,121 |
| September 2025 | 17 | 3,280 | RM 68,724 |
| October 2025 | 13 | 3,383 | RM 74,288 |

### Key Findings (Sample):
- **Campaign Creation**: Relatively stable (14-16 merchants per month)
- **Campaign Usage**: Strong growth in discount value (+83.5% from May to October)
- **Peak Activity**: August-September show highest campaign usage

### Full Analysis Needed:
- Query all 1,474 T20/T3 merchants to get complete participation rates
- Calculate: (participating T20/T3 / total T20/T3) * 100
- Compare first 3 months vs last 3 months

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

### Recommendations:
1. **Immediate Priority**: Assign AMs to all T3 merchants (197)
2. **Short-term Goal**: Increase T20 engagement to 50% within 1 month
3. **Long-term Target**: Achieve 80%+ engagement rate for all T20/T3

---

## Summary & Action Items

### ✅ What's Working:
1. **DoD Participation**: Increased 16.6% over 6 months
2. **Campaign Usage Value**: Strong growth (+83.5% discount value May→Oct)

### ⚠️ Critical Issues:
1. **Low Engagement Rate**: Only 10.4% of T20/T3 have AM assignment
2. **Campaign Participation**: Need full analysis with all 1,474 merchants

### 🎯 Immediate Actions:
1. **Assign AMs** to 1,321 unassigned T20/T3 merchants (priority: T3 first)
2. **Complete campaign participation analysis** with all T20/T3 merchant IDs
3. **Set engagement targets**: 50% in 1 month, 80% in 3 months

---

**Data Sources:**
- ✅ `ocd_adw.d_merchant_funded_campaign` - Campaign creation
- ✅ `ocd_adw.f_food_discount` - Campaign usage (is_mfc = TRUE)
- ✅ `analytics_food.pre_purchased_deals_base` - DoD campaign setup
- ✅ `ocd_adw.f_food_prepurchased_deals` - DoD orders
- ✅ `ocd_adw.d_merchant` - Merchant tagging/engagement

**Files Created:**
- `query_campaign_participation_t3_t20.sql` - Complete SQL queries
- `t20_merchant_ids.json` - All T20 merchant IDs (1,474)
- `t3_merchant_ids.json` - All T3 merchant IDs (197)

**Report Date**: November 7, 2025


