# T3/T20 Campaign/Ads Participation Analysis
## Last 6 Months (May 2025 - October 2025)

### Data Sources Identified

**Question 1: Do we increase T3/T20 Campaigns/Ads Participation %?**

**Answer Tables:**
1. **`ocd_adw.d_merchant_funded_campaign`** - Tracks merchant campaign creation/participation
   - Shows which merchants have created campaigns
   - Fields: `merchant_id`, `campaign_id`, `start_time`, `city_id`
   
2. **`ocd_adw.f_food_discount`** - Tracks actual campaign usage/redemption
   - Shows which merchants' campaigns are being used
   - Fields: `merchant_id`, `mfc_campaign_id`, `is_mfc`, `date_id`
   - Filter: `is_mfc = TRUE` for merchant-funded campaigns

### All Penang Merchants (Baseline)

**Campaign Participation (d_merchant_funded_campaign):**
| Month | Participating Merchants | Total Campaigns | MoM Change | MoM Change % |
|-------|------------------------|------------------|------------|--------------|
| May 2025 | 2,400 | 668,938 | - | - |
| June 2025 | 2,469 | 835,764 | +69 | +2.9% |
| July 2025 | 2,427 | 1135,671 | -42 | -1.7% |
| August 2025 | 2,797 | 751,414 | +370 | +15.2% |
| September 2025 | 2,850 | 932,102 | +53 | +1.9% |
| October 2025 | 3,110 | 887,178 | +260 | +9.1% |

**Campaign Usage (f_food_discount - is_mfc = TRUE):**
| Month | Merchants with Usage | Orders with Campaigns | Unique Campaigns Used | Total Discount |
|-------|---------------------|----------------------|----------------------|----------------|
| May 2025 | 2,374 | 198,057 | 17,717 | RM 2,530,150 |
| June 2025 | 2,237 | 181,717 | 17,349 | RM 2,309,331 |
| July 2025 | 2,193 | 188,330 | 17,845 | RM 2,527,413 |
| August 2025 | 2,450 | 191,750 | 21,408 | RM 2,641,174 |
| September 2025 | 2,358 | 175,824 | 20,405 | RM 2,788,422 |
| October 2025 | 2,682 | 177,677 | 17,965 | RM 2,792,137 |

### Key Findings (All Penang)

1. **Campaign Creation Trend**: 
   - Increased from 2,400 (May) to 3,110 (October)
   - **+710 merchants (+29.6% over 6 months)**
   - Strong growth in August (+15.2% MoM) and October (+9.1% MoM)

2. **Campaign Usage Trend**:
   - Merchants with usage: 2,374 (May) → 2,682 (October)
   - **+308 merchants (+13.0% over 6 months)**
   - Peak in August (2,450 merchants)

3. **Period Comparison**:
   - **May-July**: Avg 2,432 merchants creating campaigns
   - **August-October**: Avg 2,919 merchants creating campaigns
   - **Change**: +487 merchants (+20.0% increase)

### Next Steps

To get T3/T20-specific data:
1. Filter queries by T20/T3 merchant IDs (1,474 merchants)
2. Calculate participation rate: (participating T20/T3 / total T20/T3) * 100
3. Compare first 3 months vs last 3 months
4. Generate participation % trend

**SQL Queries Ready**: See `query_campaign_participation_t3_t20.sql`

---

**Tables Identified:**
- ✅ `ocd_adw.d_merchant_funded_campaign` - Campaign creation/participation
- ✅ `ocd_adw.f_food_discount` - Campaign usage/redemption (is_mfc = TRUE)


