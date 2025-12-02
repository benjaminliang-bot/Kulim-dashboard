# GMV Data Validation - Island vs Mainland Comparison
**Date**: December 2025  
**Period**: January - November 2025 (11 months)

---

## 📊 DATA COMPARISON

### Your Raw Data (Jan-Nov 2025)

| Month | Island GMV | Mainland GMV | Total GMV |
|-------|------------|--------------|-----------|
| Jan 2025 | 26,209,573 | 15,765,354 | 41,974,927 |
| Feb 2025 | 24,550,268 | 14,480,920 | 39,031,188 |
| Mar 2025 | 23,883,727 | 13,508,554 | 37,392,281 |
| Apr 2025 | 25,143,627 | 15,234,570 | 40,378,197 |
| May 2025 | 28,348,515 | 16,925,739 | 45,274,254 |
| Jun 2025 | 27,631,709 | 16,158,243 | 43,789,952 |
| Jul 2025 | 29,192,804 | 17,023,344 | 46,216,148 |
| Aug 2025 | 29,048,046 | 17,687,058 | 46,735,104 |
| Sep 2025 | 28,019,009 | 17,250,853 | 45,269,862 |
| Oct 2025 | 28,900,813.64 | 18,224,772.08 | 47,125,585.72 |
| Nov 2025 | 29,308,622 | 18,184,372 | 47,492,994 |
| **TOTAL** | **290,237,213.64** | **188,443,777.08** | **478,680,990.72** |

---

### My Query Results (Using subcity_name = "Seberang Perai" for Mainland)

| Month | Island GMV | Mainland GMV | Total GMV |
|-------|------------|--------------|-----------|
| Jan 2025 | 27,130,252.90 | 12,994,941.27 | 40,125,194.17 |
| Feb 2025 | 25,272,198.84 | 11,914,335.73 | 37,186,534.57 |
| Mar 2025 | 24,408,587.40 | 11,215,942.99 | 35,624,530.39 |
| Apr 2025 | 26,166,098.21 | 12,477,517.08 | 38,643,615.29 |
| May 2025 | 29,283,361.56 | 13,964,736.86 | 43,248,098.42 |
| Jun 2025 | 29,010,511.58 | 13,431,403.43 | 42,441,915.01 |
| Jul 2025 | 30,816,065.65 | 14,364,247.46 | 45,180,313.11 |
| Aug 2025 | 30,960,289.42 | 14,838,601.55 | 45,798,890.97 |
| Sep 2025 | 29,883,918.10 | 14,484,844.59 | 44,368,762.69 |
| Oct 2025 | 30,868,425.15 | 15,275,678.00 | 46,144,103.15 |
| Nov 2025 | 31,232,038.24 | 15,350,184.09 | 46,582,222.33 |
| **TOTAL** | **315,031,747.05** | **150,312,433.05** | **465,344,180.10** |

---

## ⚠️ DISCREPANCIES IDENTIFIED

### Total GMV
- **Your Total**: 478,680,990.72 MYR
- **My Total**: 465,344,180.10 MYR
- **Difference**: -13,336,810.62 MYR (-2.8%)

### Island GMV
- **Your Island**: 290,237,213.64 MYR
- **My Island**: 315,031,747.05 MYR
- **Difference**: +24,794,533.41 MYR (+8.5% higher)

### Mainland GMV
- **Your Mainland**: 188,443,777.08 MYR
- **My Mainland**: 150,312,433.05 MYR
- **Difference**: -38,131,344.03 MYR (-20.2% lower)

---

## 🔍 ROOT CAUSE ANALYSIS

### Issue 1: Mainland Classification
**Problem**: My Mainland GMV is **20% lower** than your data.

**Possible Causes**:
1. **Area Classification Method**: I'm using `subcity_name LIKE '%Seberang Perai%'` to identify Mainland
   - Your method might use a different field or logic
   - Some areas might be classified differently

2. **Missing Areas**: Some Mainland areas might not have "Seberang Perai" in subcity_name
   - Or some areas I'm classifying as Island are actually Mainland

3. **Data Filters**: Your data might include/exclude certain order types
   - Different `booking_state_simple` filters?
   - Different `business_type` filters?

### Issue 2: Island Classification
**Problem**: My Island GMV is **8.5% higher** than your data.

**Possible Causes**:
1. **Over-classification**: Some Mainland areas might be incorrectly classified as Island
2. **Different area boundaries**: Area definitions might differ

### Issue 3: Total GMV
**Problem**: My total is **2.8% lower** than your data.

**Possible Causes**:
1. **Missing orders**: Some orders might not have `dropoff_area_id` populated
2. **Different date filters**: Edge cases in date boundaries
3. **Data completeness**: Your source might include additional data

---

## ❓ QUESTIONS TO RESOLVE

1. **How do you classify Island vs Mainland?**
   - Do you use `subcity_name` field?
   - Is there a specific field or mapping table?
   - Do you have a list of area_ids for Mainland?

2. **What filters do you apply?**
   - `booking_state_simple = 'COMPLETED'` only?
   - Any other filters on `business_type`, `is_completed`, etc.?
   - Do you exclude certain order types?

3. **Data source differences?**
   - Are you using the same `ocd_adw.f_food_metrics` table?
   - Any data transformations or aggregations?
   - Different date boundaries (start/end of month)?

---

## 🔧 RECOMMENDED FIX

**Option 1**: If you have a Mainland area mapping/list, I can use that directly.

**Option 2**: If you can share your classification logic, I'll update the queries.

**Option 3**: I can query all areas and their GMV, and you can tell me which ones should be Mainland.

---

## 📋 NEXT STEPS

1. **Share your Island/Mainland classification method** - I'll update queries accordingly
2. **Verify data filters** - Ensure we're using the same filters
3. **Re-run analysis** - Once classification is fixed, regenerate insights

---

**Status**: ⚠️ **DATA MISMATCH DETECTED** - Need to align classification method before proceeding with growth analysis.

