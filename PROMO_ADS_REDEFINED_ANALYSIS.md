# T3/T20 Promotion and Ads Participation - Redefined Analysis
## Last 6 Months (May 2025 - October 2025)

---

## Redefinition Summary

### 1. **Promotion Participation**
**Definition**: If promotion spending > 0, then merchant is in promo

**Tracking**:
- MFP campaigns (hotdeals, delivery campaigns)
- Filter: `is_mfp = TRUE` in `ocd_adw.f_food_discount`

**Funding Breakdown**:
- **MEX-funded**: `total_mex_promo_spend > 0`
- **Grab-funded**: `total_grab_promo_spend > 0`
- **Both**: Merchants with both MEX and Grab funding

**Data Source**: `ocd_adw.f_food_discount`
- Fields: `total_mex_promo_spend`, `total_grab_promo_spend`, `is_mfp`, `mfc_campaign_id`, `eater_app_campaign_name`

---

### 2. **Ads Participation**
**Definition**: If ads revenue > 0, then merchant is in ads

**Revenue Definition**:
- Ads revenue = `accrued_amount_before_tax_local` (amount Grab earns from ads)
- This represents the actual revenue generated from merchant advertising

**Funding Breakdown**:
- **MEX-funded**: `mex_prorated_billable_ad_spend_local > 0` (merchants paying for ads)
- **Grab-funded**: Ads where Grab funds the advertising (house ads, promotional ads)

**Data Source**: `ocd_adw.agg_ads_merchant`
- Fields: `accrued_amount_before_tax_local`, `mex_prorated_billable_ad_spend_local`, `billable_ad_spend_local`

---

## Key Insights Provided

### Promotion Participation Insights

1. **Participation Rate Trend**
   - Monthly count of T20/T3 merchants with promo spending > 0
   - Month-over-month change and percentage change
   - Participation rate: (merchants in promo / total T20/T3) * 100

2. **Funding Mix Analysis**
   - **MEX-funded merchants**: Count and percentage of total promo spend
   - **Grab-funded merchants**: Count and percentage of total promo spend
   - **Both-funded merchants**: Merchants using both funding sources
   - **Funding split**: MEX vs Grab percentage of total promo spend

3. **Campaign Type Breakdown**
   - **MFP campaigns**: Total count of MFP campaigns (hotdeals, delivery campaigns)
   - **Hotdeal/Delivery campaigns**: Specific count of hotdeal and delivery campaigns
   - **MFC campaigns**: Count of merchant-funded campaigns (for comparison)

4. **Performance Metrics**
   - Total promo spend (MEX + Grab)
   - Total promo orders
   - Average promo spend per merchant

---

### Ads Participation Insights

1. **Participation Rate Trend**
   - Monthly count of T20/T3 merchants with ads revenue > 0
   - Month-over-month change and percentage change
   - Participation rate: (merchants in ads / total T20/T3) * 100

2. **Funding Mix Analysis**
   - **MEX-funded ads**: Count of merchants paying for ads and total spend
   - **Grab-funded ads**: Count of merchants with Grab-funded ads
   - **Funding split**: MEX vs Grab percentage of total ads spend

3. **Performance Metrics**
   - Total ads revenue (Grab's revenue from ads)
   - Total ads spend (merchant spend on ads)
   - Attributed orders (orders attributed to ads)
   - Attributed GMV (GMV attributed to ads)
   - Clicks and impressions

---

### Combined Insights

1. **Overall Participation**
   - Merchants in promo only
   - Merchants in ads only
   - Merchants in both promo and ads
   - Merchants in either promo or ads
   - Combined participation rate

2. **Cross-Participation Analysis**
   - Overlap between promo and ads participation
   - Merchants using both channels vs single channel
   - Revenue contribution from each channel

---

## SQL Queries

**File**: `query_promo_ads_redefined_complete.sql`

**Contains**:
1. **Part 1**: Promotion Participation (MFP campaigns with Grab/MEX funding breakdown)
2. **Part 2**: Ads Revenue Participation (with Grab/MEX funding breakdown)
3. **Part 3**: Combined Promo + Ads Participation
4. **Part 4**: Campaign Type Breakdown (to identify hotdeals, delivery campaigns)

---

## Implementation Notes

### Merchant ID List
- **Total T20/T3 merchants**: 1,474
- **Source**: `t20_merchant_ids.json` and `t3_merchant_ids.json`
- **Note**: Replace the LIMIT clause in queries with actual merchant_id_nk list for full analysis

### Date Range
- **Period**: May 2025 - October 2025 (6 months)
- **Date format**: `date_id >= 20250501 AND date_id < 20251101`

### City Filter
- **City ID**: 13 (Penang)
- Applied to all queries

---

## Expected Output Format

### Promotion Participation
```
Month | Merchants in Promo | MEX-funded | Grab-funded | Both | Total Spend | MEX % | Grab % | Participation Rate
```

### Ads Participation
```
Month | Merchants in Ads | MEX-funded | Grab-funded | Total Revenue | MEX % | Grab % | Participation Rate
```

### Combined
```
Month | Promo Only | Ads Only | Both | Either | Combined Rate | Both Rate
```

---

## Next Steps

1. **Execute Queries**: Run `query_promo_ads_redefined_complete.sql` with full T20/T3 merchant list
2. **Campaign Type Identification**: Review Part 4 results to identify hotdeal and delivery campaign types
3. **Trend Analysis**: Compare first 3 months (May-July) vs last 3 months (Aug-Oct)
4. **Insights Generation**: 
   - Are we increasing participation?
   - What's the funding mix trend (MEX vs Grab)?
   - Which channel (promo vs ads) is growing faster?
   - What's the overlap between channels?

---

**Generated**: November 7, 2025


