# Kulim Commercial Metrics Preview (Using area_id from d_area)

## 📊 Preview Numbers - Review Before Publishing

### **September 2025:**
- **Active Merchants:** 298
- **Unique Passengers:** 17,449
- **Completed Orders:** 47,049
- **Total GMV:** RM 1,606,330.41
- **Average Order Value:** RM 34.14

### **October 2025:**
- **Active Merchants:** 308 (+10 vs Sep)
- **Unique Passengers:** 18,338 (+5.1% vs Sep)
- **Completed Orders:** 51,309 (+9.1% vs Sep)
- **Total GMV:** RM 1,734,436.13 (+8.0% MoM)
- **Average Order Value:** RM 33.80

### **November 2025 (Partial - through Nov 10):**
- **Active Merchants:** 283
- **Unique Passengers:** 8,699
- **Completed Orders:** 15,338
- **Total GMV:** RM 510,252.69
- **Average Order Value:** RM 33.27

---

## 📈 Summary Totals (Sep + Oct + Nov Partial):
- **Total GMV:** RM 3,851,019.23
- **Total Orders:** 113,696
- **Max Active Merchants:** 308
- **Max Unique Passengers:** 18,338
- **Average AOV:** RM 33.88

---

## 🔍 Comparison with Previous Numbers

### Previous (district-based):
- September: 372 merchants, 19,427 passengers, 56,490 orders, RM 1,892,587.28
- October: 382 merchants, 20,252 passengers, 60,669 orders, RM 2,018,636.08
- November: 348 merchants, 9,795 passengers, 18,026 orders, RM 588,553.94

### New (area_id-based):
- September: 298 merchants, 17,449 passengers, 47,049 orders, RM 1,606,330.41
- October: 308 merchants, 18,338 passengers, 51,309 orders, RM 1,734,436.13
- November: 283 merchants, 8,699 passengers, 15,338 orders, RM 510,252.69

### Difference:
- **Merchants:** ~20% fewer (more accurate area classification)
- **GMV:** ~15% lower (more precise Kulim area definition)
- **Orders:** ~15% lower (aligned with merchant count)

---

## ✅ Method Used

Using geohash prefix matching (first 6 characters) to join `d_merchant` with `d_area`:
- Identifies 774 merchants matching Kulim area geohashes
- More accurate than district-based classification
- Aligns with official area mapping from Geo team

---

## ⚠️ Action Required

**Please review these numbers before updating the HTML dashboard.**

If these numbers look correct, I'll update the HTML file. If you want adjustments, let me know!


