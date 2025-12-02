# T3/T20 Engagement Analysis - Last 6 Months
## May 2025 to October 2025

### Executive Summary

**Merchant Base:**
- **T20 merchants**: 1,474
- **T3 merchants**: 197 (subset of T20)
- **Total T20/T3**: 1,474 unique merchants

---

## Question 1: Do we increase T3/T20 Campaigns/Ads Participation %?

**Status**: ⚠️ **Data Source Needed**

Campaign/Ads participation data requires identification of the correct source tables. Potential sources:
- Campaign management systems
- Promo/voucher tables
- Marketing campaign tracking tables

**Next Steps:**
- Identify campaign participation tracking tables
- Query participation rate over last 6 months
- Compare month-over-month trends

---

## Question 2: Do we Increase T3/T20 DoD Mex Participation %?

**Data Sources:**
1. `analytics_food.pre_purchased_deals_base` - Campaign setup/configuration
2. `ocd_adw.f_food_prepurchased_deals` - Actual DoD orders

### Analysis Structure:

**From pre_purchased_deals_base:**
- Tracks DoD campaigns created/uploaded
- Shows merchant participation in campaign setup
- Monthly trend: Count of participating merchants and campaigns

**From f_food_prepurchased_deals:**
- Tracks actual DoD orders completed
- Shows real merchant participation in DoD sales
- Monthly trend: Participating merchants, orders, GMV

**Query Results**: See SQL queries in `t3_t20_engagement_analysis.sql`

---

## Question 3: Is all T20/T3 merchant being tagged to someone? (Engagement Rate)

**Current Status:**
- **Total T20/T3 merchants**: 1,474
- **With AM assigned**: 153 (10.4%)
- **Without AM assigned**: 1,321 (89.6%)
- **Engagement Rate**: **10.4%**

### Key Finding:
⚠️ **Low Engagement Rate**: Only 10.4% of T20/T3 merchants have an assigned Account Manager (AM).

### Recommendations:
1. **Immediate Action**: Assign AMs to remaining 1,321 merchants
2. **Target**: Increase engagement rate to 80%+ within next quarter
3. **Priority**: Focus on T3 merchants (197) first, then expand to full T20

---

## Next Steps

1. **Execute full queries** with all 1,474 T20/T3 merchant IDs
2. **Calculate participation trends** month-over-month
3. **Identify campaign/ads data source** for Question 1
4. **Generate actionable insights** for improving engagement

---

**Files Created:**
- `t3_t20_engagement_analysis.sql` - Complete SQL queries
- `t20_merchant_ids.json` - All T20 merchant IDs (1,474)
- `t3_merchant_ids.json` - All T3 merchant IDs (197)


