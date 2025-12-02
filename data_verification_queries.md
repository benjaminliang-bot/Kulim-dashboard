# Data Verification - Query Details
## Current Query Logic

**Completion Rate Calculation:**
```sql
ROUND(100.0 * COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END) / 
      NULLIF(COUNT(DISTINCT f.order_id), 0), 2) as completion_rate
```

**Filters Applied:**
- `country_id = 1` (Malaysia)
- `city_id != 1` (exclude KL, for OC cities)
- `business_type = 0` (food delivery)
- `date_id` in range (Oct 1 - Nov 25, 2025)

---

## Verified Data Points

### Kota Bharu - Nov 23, 2025
- **Total Orders:** 4,661
- **Completed Orders:** 3,424
- **Completion Rate:** 73.5%
- **Query Result:** ✅ Matches

### Alor Setar - Oct 3, 2025
- **Total Orders:** 4,628
- **Completed Orders:** 3,723
- **Completion Rate:** 80.4%
- **Query Result:** ✅ Matches

### Penang - Oct 20, 2025
- **Total Orders:** 37,052
- **Completed Orders:** 32,357
- **Completion Rate:** 87.3%
- **Query Result:** ✅ Matches

### Ipoh - Oct 20, 2025
- **Total Orders:** 20,403
- **Completed Orders:** 17,425
- **Completion Rate:** 85.4%
- **Query Result:** ✅ Matches

---

## Potential Differences

### 1. Business Type Filter
- **Current:** `business_type = 0` only
- **Alternative:** Include `business_type = 1` as well?
- **Impact:** Nov 23 has 38 orders with business_type = 1 (minimal impact)

### 2. Completion Rate Definition
- **Current:** Completed / Total Orders
- **Alternative 1:** Completed / (Completed + Cancelled) - would give 95.8% for Kota Bharu Nov 23
- **Alternative 2:** Completed / Allocated Orders (exclude UNALLOCATED, ORDER_EXPIRED)

### 3. Date Range
- **Current:** Using date_id format (YYYYMMDD)
- **Verify:** Are dates correct? Nov 23 = 20251123

### 4. City Filter
- **Current:** Using city_id from d_city table
- **Verify:** City IDs are correct (verified: Penang=13, Ipoh=48, etc.)

---

## Questions for Dashboard Verification

1. **What specific numbers don't match?**
   - Which city/date combinations?
   - What does your dashboard show vs what I'm reporting?

2. **How is completion/fulfillment rate calculated in your dashboard?**
   - Same formula: Completed / Total Orders?
   - Or different denominator?

3. **What filters are applied in your dashboard?**
   - business_type filter?
   - Any order state exclusions?
   - Date range?

4. **What table/field does your dashboard use?**
   - Same table: `ocd_adw.f_food_metrics`?
   - Same field: `booking_state_simple`?

---

**Please provide specific examples of mismatches so I can adjust the queries accordingly.**

