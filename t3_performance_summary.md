# T3 Performance Summary - Penang MEX

## Answers to Your Questions

### 1. Is segmentation mapped from "Main Tracker V2" Column J to all Penang MEX in d_merchant?

**Answer: NO - Partial Coverage Only**

- **Total Penang MEX in d_merchant**: 63,263 merchants
- **Merchants in Main Tracker V2**: 7,483 merchants (11.8% coverage)
- **T3 merchants in Main Tracker V2**: 197 merchants

**Conclusion**: Main Tracker V2 Column J segmentation covers only a subset of Penang MEX merchants, not all of them. This appears to be a tracking/management subset rather than the full merchant base.

### 2. T3 Performance: Last Month vs Same Month Last Year

**Query Setup:**
- **T3 Merchants**: 197 merchants (identified from Main Tracker V2 Column J)
- **Period 1**: October 2025 (2025-10-01 to 2025-10-31)
- **Period 2**: October 2024 (2024-10-01 to 2024-10-31)
- **Metrics**: GMV, Completed Orders, Growth %

**T3 Segmentation Distribution:**
- T20 (T3 - A1): 43 merchants
- T20 (T3 - A2): 37 merchants
- T20 (T3 - B2): 25 merchants
- T20 (T3 - B1): 22 merchants
- T20 (T3 - C2): 20 merchants
- T20 (T3 - C1): 18 merchants
- T20 (T3 - B3): 16 merchants
- T20 (T3 - C3): 12 merchants
- T20 (T3 - A3): 4 merchants

## Next Steps

To get the actual T3 performance data, we need to:
1. Query merchant_gross_merchandise_value metric via Midas
2. Filter by the 197 T3 merchant IDs
3. Aggregate for October 2025 vs October 2024
4. Calculate YoY growth metrics

The query structure is ready - execution via Midas/Hubble will provide the performance summary.


