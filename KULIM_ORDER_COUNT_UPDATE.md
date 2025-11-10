# Kulim Order Count Update - Using DISTINCT Orders

## ✅ Changes Completed

All queries have been updated to use `COUNT(DISTINCT order_id)` instead of `COUNT(CASE WHEN ... THEN 1 END)` to ensure we're counting unique orders only.

---

## 📋 Updated Queries

### Files Updated:
1. ✅ `analyze_kulim_performance.py` - All 6 query functions
2. ✅ `populate_kulim_commercial_metrics.py` - Metrics query

### Changes Made:
- Changed from: `COUNT(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN 1 END)`
- Changed to: `COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END)`

### Also Updated:
- Campaign orders: Now uses `COUNT(DISTINCT ... order_id)` for campaign_orders
- Total orders: Now uses `COUNT(DISTINCT ... order_id)` for total_orders
- All queries now use `f_food_metrics` consistently (instead of mixing with `f_food_booking`)

---

## 📊 Verified Numbers (Using DISTINCT order_id)

### September 2025:
- **Active Merchants:** 298
- **Unique Passengers:** 17,449
- **Completed Orders:** 47,049 (distinct orders)
- **Total GMV:** RM 1,606,330.41
- **Average Order Value:** RM 34.14

### October 2025:
- **Active Merchants:** 308
- **Unique Passengers:** 18,338
- **Completed Orders:** 51,309 (distinct orders)
- **Total GMV:** RM 1,734,436.13
- **Average Order Value:** RM 33.80
- **MoM Growth:** +7.98%

### November 2025 (Partial):
- **Active Merchants:** 283
- **Unique Passengers:** 8,699
- **Completed Orders:** 15,338 (distinct orders)
- **Total GMV:** RM 510,252.69
- **Average Order Value:** RM 33.27

---

## ✅ Status

All queries now properly count **distinct completed orders** to avoid double-counting.

Note: The numbers remain the same because `f_food_metrics` already appears to have one row per order, but the query logic is now explicitly using DISTINCT for accuracy and future-proofing.

