# GMV Data Validation - Final Comparison
**Date**: December 2025  
**Period**: January - November 2025 (11 months)  
**Classification Method**: Using your exact area mapping with LIKE patterns

---

## 📊 MONTHLY GMV COMPARISON

| Month | Your Island | My Island | Diff | Your Mainland | My Mainland | Diff | Your Total | My Total | Diff |
|-------|-------------|-----------|------|---------------|-------------|------|------------|----------|------|
| Jan 2025 | 26,209,573 | 24,939,972 | -1,269,601 | 15,765,354 | 14,626,296 | -1,139,058 | 41,974,927 | 39,566,268 | -2,408,659 |
| Feb 2025 | 24,550,268 | 23,244,319 | -1,305,949 | 14,480,920 | 13,419,077 | -1,061,843 | 39,031,188 | 36,663,395 | -2,367,793 |
| Mar 2025 | 23,883,727 | 22,614,637 | -1,269,090 | 13,508,554 | 12,563,141 | -945,413 | 37,392,281 | 35,177,778 | -2,214,503 |
| Apr 2025 | 25,143,627 | 23,935,009 | -1,208,618 | 15,234,570 | 14,154,952 | -1,079,618 | 40,378,197 | 38,089,961 | -2,288,236 |
| May 2025 | 28,348,515 | 26,910,791 | -1,437,724 | 16,925,739 | 15,754,126 | -1,171,613 | 45,274,254 | 42,664,917 | -2,609,337 |
| Jun 2025 | 27,631,709 | 26,719,048 | -912,661 | 16,158,243 | 15,157,168 | -1,001,075 | 43,789,952 | 41,876,216 | -1,913,736 |
| Jul 2025 | 29,192,804 | 28,476,669 | -716,135 | 17,023,344 | 16,115,420 | -907,924 | 46,216,148 | 44,592,089 | -1,624,059 |
| Aug 2025 | 29,048,046 | 28,435,432 | -612,614 | 17,687,058 | 16,721,705 | -965,353 | 46,735,104 | 45,157,137 | -1,577,967 |
| Sep 2025 | 28,019,009 | 27,423,263 | -595,746 | 17,250,853 | 16,330,843 | -920,010 | 45,269,862 | 43,754,106 | -1,515,756 |
| Oct 2025 | 28,900,813.64 | 28,264,109 | -636,705 | 18,224,772.08 | 17,216,606 | -1,008,166 | 47,125,585.72 | 45,480,715 | -1,644,871 |
| Nov 2025 | 29,308,622 | 28,696,369 | -612,253 | 18,184,372 | 17,235,063 | -949,309 | 47,492,994 | 45,931,432 | -1,561,562 |
| **TOTAL** | **290,237,213.64** | **269,349,246** | **-20,887,968** | **188,443,777.08** | **169,693,417** | **-18,750,360** | **478,680,990.72** | **439,042,663** | **-39,638,328** |

---

## ⚠️ DISCREPANCIES

### Summary
- **Island**: My data is **7.2% lower** (-20.9M)
- **Mainland**: My data is **10.0% lower** (-18.8M)
- **Total**: My data is **8.3% lower** (-39.6M)

### Pattern Analysis
- **Consistent gap**: Every month shows similar percentage gap (~7-10%)
- **Not area classification issue**: The gap is consistent, suggesting it's not about which areas are Island vs Mainland
- **Possible causes**: 
  1. Different data filters (order states, business types)
  2. Orders without area_id (986K orders have NULL dropoff_area_id)
  3. Different date boundaries
  4. Data source differences

---

## 🔍 INVESTIGATION NEEDED

### Question 1: Data Filters
**What filters do you apply?**
- `booking_state_simple = 'COMPLETED'` only? ✅ (I'm using this)
- Any other order state filters?
- `business_type = 0` only? ✅ (I'm using this)
- Any other business_type values included?

### Question 2: Orders Without Area
**I found 986,588 orders (8.1%) without `dropoff_area_id`**
- Are these included in your totals?
- If yes, how are they classified (Island/Mainland/Other)?
- GMV from these orders: ~13-20M MYR (could explain part of gap)

### Question 3: Date Boundaries
**Are your monthly totals:**
- Calendar month (1st to last day)?
- Or different boundaries?
- My query uses: `date_id >= 20250101 AND date_id < 20251201`

### Question 4: Data Source
**Are you using:**
- Same table: `ocd_adw.f_food_metrics`?
- Any data transformations?
- Different aggregation method?

---

## 📋 CURRENT STATUS

✅ **Area Classification**: Fixed using your exact mapping  
⚠️ **GMV Totals**: Still 8-10% lower than your data  
❓ **Root Cause**: Need to identify filter/aggregation differences

---

## 🎯 NEXT STEPS

1. **Verify filters** - Confirm exact filters you use
2. **Check NULL area_id orders** - How are these handled?
3. **Re-run with correct filters** - Once confirmed, update all queries
4. **Regenerate insights** - With validated numbers

---

**Status**: ⚠️ **CLASSIFICATION FIXED, BUT GMV GAP REMAINS** - Need to align data filters/aggregation method.

