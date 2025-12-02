# Kulim Area Classification Update

## ✅ Changes Completed

All queries have been updated to use `area_id` from `d_area` table instead of `district` from `d_merchant` table for classifying Kulim merchants.

---

## 📋 Updated Files

### 1. `analyze_kulim_performance.py`
All 6 query functions updated:
- ✅ `generate_kulim_merchant_list_query()`
- ✅ `generate_kulim_gmv_monthly_query()`
- ✅ `generate_kulim_merchant_performance_query()`
- ✅ `generate_kulim_campaign_participation_query()`
- ✅ `generate_kulim_segmentation_analysis_query()`
- ✅ `generate_kulim_t20_analysis_query()`

### 2. `populate_kulim_commercial_metrics.py`
- ✅ `generate_metrics_query()` updated

---

## 🔄 Query Pattern Change

### **Before (Using district):**
```sql
WHERE city_id = 13 
    AND LOWER(district) LIKE '%kulim%'
    AND is_active = true
```

### **After (Using area_id from d_area):**
```sql
WITH kulim_areas AS (
    SELECT DISTINCT area_id
    FROM ocd_adw.d_area
    WHERE city_id = 13 
        AND LOWER(area_name) LIKE '%kulim%'
),
kulim_merchants AS (
    SELECT DISTINCT m.merchant_id_nk
    FROM ocd_adw.d_merchant m
    INNER JOIN ocd_adw.d_area a 
        ON m.city_id = a.city_id 
        AND m.geohash = a.geohash
    INNER JOIN kulim_areas ka ON a.area_id = ka.area_id
    WHERE m.city_id = 13 
        AND m.status = 'ACTIVE'
)
```

---

## 🎯 Benefits

1. **More Accurate Classification**: Uses official area mapping from `d_area` table
2. **Consistent with Geo Team Data**: Aligns with geohash.area_map managed by Geo team
3. **Better Coverage**: Captures all merchants in Kulim area regardless of district field variations
4. **Standardized Approach**: Uses the same area classification system across all queries

---

## 📊 Kulim Area IDs Found

Query identified multiple `area_id` values for Kulim:
- Area Name: `Ayer Puteh_Kulim`
- Subcity Name: `Kedah-Kulim-Kulim`
- Multiple area_ids (e.g., 1451515, 800498, 1451488, etc.)

All merchants matching these area_ids are now included in the analysis.

---

## ✅ Status

All queries have been successfully updated and are ready to use. The new approach will:
- Join `d_merchant` with `d_area` using `city_id` and `geohash`
- Filter for Kulim area_ids from `d_area`
- Use `status = 'ACTIVE'` instead of `is_active = true`

---

## 🔍 Verification

To verify the changes work correctly, run any of the updated queries and compare merchant counts with the previous district-based approach.


