# Request for Original SQL Query

The system needs access to the **original SQL query** you provided earlier for analyzing Kombo Jimat orders. 

## Current Status

I've created SQL query templates, but I need to know:

1. **What table did you use?** (e.g., `gt_aws_hive.ocd_adw.f_food_order`, `gt_aws_hive.ocd_adw.f_food_order_detail`, or another table?)
2. **What column identifies Kombo Jimat?** (e.g., `promo_name`, `promo_code`, `promo_id`, or another column?)
3. **How is Kombo Jimat identified in your query?** (e.g., specific promo codes, promo names, or other identifiers?)

## Why This Is Needed

To properly analyze the **distribution pattern** of Kombo Jimat orders across the last 4 days of each month, I need to:

1. Run the correct SQL query that matches your data structure
2. Analyze the actual distribution (which day typically has most orders)
3. Update the forecast to reflect this historical pattern (instead of assuming equal distribution)

## Next Steps

Please provide your **original SQL query** so I can:
- Execute it correctly
- Analyze the distribution pattern
- Update the daily GMV forecast for Penang 2026 with the correct distribution weights

Once I have your query, I'll:
1. Run it to get historical Kombo Jimat order distribution
2. Calculate distribution percentages across the 4 days
3. Update the forecast generation to use these percentages
4. Regenerate all CSV files with the corrected distribution


