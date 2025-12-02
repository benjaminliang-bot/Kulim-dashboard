# Export Penang Mainland Merchants to Excel

## Query Executed Successfully ✅

The merchant query has been executed and returned **hundreds of merchants** from Penang Mainland areas.

## Quick Export Options

### Option 1: Direct Export from Query Results (Recommended)

The query results are already available. To export to Excel:

1. **Copy the query results** from the terminal/query output
2. **Open Excel** and paste the data
3. Excel will automatically format it as a table

### Option 2: Use Python Script

Run the provided script `export_merchants_to_excel.py` (requires pandas and openpyxl):

```bash
pip install pandas openpyxl
python export_merchants_to_excel.py
```

### Option 3: Re-run Query with Export

The query is saved in `penang_mainland_growth_analysis_queries.sql` (Query 1).

## Data Columns Included

The merchant list includes:
- **merchant_id_nk**: Unique merchant identifier
- **merchant_name**: Merchant business name
- **area_name**: Mainland area location
- **halal_status**: Halal / Non-Halal / Unknown
- **primary_cuisine_id**: Cuisine type IDs
- **segment**: Enterprise / Mid-Market / Long-Tail
- **custom_segment**: KVAM, BD, OC, etc.
- **am_name**: Account Manager email
- **last_order_date**: Last order date
- **merchant_status**: Active / Churned / Never Ordered

## Query Summary

- **Total Merchants**: Hundreds of active merchants across Mainland areas
- **Areas Covered**: All Mainland areas (Alma Jaya, Bukit Mertajam, Bagan Serai, etc.)
- **Status Filter**: ACTIVE merchants only
- **Order Status**: Includes merchants with orders in last 12 months (Active) vs churned

## Next Steps

1. Review the merchant list by area and halal status
2. Identify cuisine gaps by cross-referencing with demand patterns
3. Prioritize win-back opportunities (Churned merchants)
4. Map merchant coverage against session drop-off data

