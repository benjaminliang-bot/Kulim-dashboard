# Penang Mainland Growth Analysis - Data Extraction Guide

## Overview
This document provides SQL queries to extract granular operational data for developing a "Win the Mainland" growth strategy for GrabFood Penang. The queries are designed to identify hyper-growth opportunities across **Supply**, **Demand**, and **Operations** dimensions.

## File Structure
- **penang_mainland_growth_analysis_queries.sql**: Contains all 6 executable queries + 1 template query

## Query Summary

### ✅ Query 1: Merchant List with Cuisine & Halal Status
**Purpose**: Map current Mainland merchant coverage by cuisine type and Halal status  
**Output**: Merchant list with area, halal_status, cuisine_id, segment, and churn status  
**Key Insight**: Identifies cuisine gaps and Halal coverage by sub-area  
**Action**: Use this to build "Acquire Local Heroes" target list

**Columns Returned**:
- `merchant_id_nk`, `merchant_name`, `area_name`
- `halal_status` (Halal/Non-Halal/Unknown)
- `primary_cuisine_id` (numeric - join with d_cuisine for names)
- `segment`, `custom_segment`, `am_name`
- `merchant_status` (Active/Churned/Never Ordered)

---

### ✅ Query 2: Hourly Order Distribution (Island vs Mainland)
**Purpose**: Identify demand patterns by time of day  
**Output**: Orders, GMV, and basket size by hour (0-23) for both Island and Mainland  
**Key Insight**: 
- If Mainland shows 10 PM - 2 AM spike → "Supper Market" → Target late-night merchants
- If Mainland shows 6 PM - 9 PM spike → "Family Dinner Market" → Push family bundles

**Columns Returned**:
- `hour_of_day` (0-23)
- `mainland_orders`, `mainland_gmv`, `mainland_avg_basket_size`
- `island_orders`, `island_gmv`, `island_avg_basket_size`
- `mainland_vs_island_order_pct` (comparison ratio)

---

### ✅ Query 3: Basket Size Distribution
**Purpose**: Validate "Family Meal" strategy hypothesis  
**Output**: Order count and GMV by basket size buckets (0-15, 15-25, 25-40, 40-60, 60+)  
**Key Insight**: 
- If Mainland has higher % of 40+ baskets → Family Meal strategy validated
- If Mainland has higher % of 15-25 baskets → Single-pax strategy

**Columns Returned**:
- `basket_size_bucket` (0-15, 15-25, 25-40, 40-60, 60+)
- `mainland_orders`, `mainland_gmv`, `mainland_avg_basket_size`
- `island_orders`, `island_gmv`, `island_avg_basket_size`
- `mainland_pct_of_total`, `island_pct_of_total` (distribution %)

---

### ✅ Query 4: Operational Friction Metrics (Cancellation & No Driver Rates)
**Purpose**: Identify areas with driver shortages or operational issues  
**Output**: Cancellation rates, no-driver rates, and delivery metrics by Mainland sub-area  
**Key Insight**: 
- High cancellation rate in Alma Jaya → Don't market there until driver supply fixed
- High no-driver rate → Driver acquisition priority

**Columns Returned**:
- `area_name`, `total_orders`, `completed_orders`, `cancelled_orders`
- `cancellation_rate_pct`, `no_driver_rate_pct`, `unallocated_rate_pct`
- `avg_delivery_distance_km`, `avg_delivery_time_minutes`
- `total_gmv`, `active_merchants`, `avg_order_value`

---

### ✅ Query 5: Churned / Inactive Merchants
**Purpose**: Identify win-back opportunities (faster than new acquisition)  
**Output**: List of Mainland merchants who went inactive in last 12 months  
**Key Insight**: Why did they leave? Win-back is often faster than new acquisition

**Columns Returned**:
- `merchant_id_nk`, `merchant_name`, `area_name`, `halal_status`
- `current_status`, `last_order_date`, `last_completed_order_date`
- `churn_status` (Never Completed / Churned >12 months / Inactive 6-12 months / Active)
- `segment`, `am_name`

---

### ✅ Query 6: Delivery Distance Analysis
**Purpose**: Identify if delivery fees are a growth blocker  
**Output**: Average delivery distance, delivery fees, and long-distance order % by area  
**Key Insight**: 
- If avg distance > 10km → Delivery fees might be blocking growth
- If pct_orders_over_10km > 20% → Consider subsidizing long-distance delivery fees

**Columns Returned**:
- `area_name`, `completed_orders`
- `avg_delivery_distance_km`, `median_delivery_distance_km`
- `p75_delivery_distance_km`, `p90_delivery_distance_km`, `max_delivery_distance_km`
- `avg_delivery_fee`, `delivery_fee_per_km`
- `orders_over_10km`, `pct_orders_over_10km`

---

### ⚠️ Query 7: Failed Searches (Template - Requires Search Data)
**Purpose**: Identify cuisine gaps from user search behavior  
**Output**: Top 20 search queries with no results or no conversion  
**Key Insight**: Direct signal of unmet demand (e.g., "Vegetarian" in Kepala Batas)

**Status**: Template provided - requires access to search analytics tables  
**Next Steps**: 
1. Identify search data table (e.g., `scribe_session`, `search_log`, `user_search_events`)
2. Adjust table name and column names in template
3. Execute to get failed search list

---

## How to Execute

### Option 1: Via MCP Tool (Recommended)
```python
# In Cursor chat, use MCP tool:
mcp_mcp-grab-data_run_presto_query(query="[paste query here]")
```

### Option 2: Via Presto/Trino CLI
1. Connect to Grab DataLake Presto/Trino instance
2. Copy individual query from SQL file
3. Execute query
4. Export results to CSV/Excel

### Option 3: Via Python Script
```python
from mcp_mcp_grab_data import run_presto_query

# Read query from file
with open('penang_mainland_growth_analysis_queries.sql', 'r') as f:
    queries = f.read().split('-- ============================================================================')

# Execute Query 1 (Merchant List)
query1 = queries[1]  # Adjust index based on query position
results = run_presto_query(query=query1)
```

---

## Data Limitations & Next Steps

### 1. **Cuisine Names**
- Current: `primary_cuisine_id` returns numeric IDs
- **Action**: Join with `d_cuisine` table to get cuisine names
- **If d_cuisine exists**, add to Query 1:
  ```sql
  LEFT JOIN ocd_adw.d_cuisine c ON m.primary_cuisine_id = c.cuisine_id
  ```

### 2. **Search Data**
- Current: Template query provided (Query 7)
- **Action**: 
  1. Identify search analytics table name
  2. Verify column names (search_query, has_results, converted, session_id)
  3. Update template and execute

### 3. **Mainland Area Definition**
- Current: Hardcoded list of area names
- **Action**: 
  1. Run this to verify Mainland areas:
     ```sql
     SELECT DISTINCT area_name 
     FROM ocd_adw.d_area 
     WHERE city_id = 13 
     ORDER BY area_name;
     ```
  2. Update `mainland_areas` CTE in all queries with verified list

### 4. **Date Range**
- Current: Last 12 months
- **Action**: Adjust `date_id` filters if you need different time periods:
   ```sql
   -- Last 6 months:
   AND f.date_id >= CAST(DATE_FORMAT(DATE_ADD('month', -6, CURRENT_DATE), '%Y%m%d') AS INTEGER)
   
   -- Specific month (e.g., October 2025):
   AND f.date_id >= 20251001 AND f.date_id < 20251101
   ```

---

## Recommended Execution Order

1. **Start with Query 1** (Merchant List) - Builds foundation for all other analysis
2. **Then Query 2** (Hourly Distribution) - Quick win to identify demand patterns
3. **Then Query 3** (Basket Size) - Validates Family Meal hypothesis
4. **Then Query 4** (Operational Friction) - Identifies blockers before marketing
5. **Then Query 5** (Churned Merchants) - Win-back opportunities
6. **Then Query 6** (Delivery Distance) - Fee optimization opportunities
7. **Finally Query 7** (Failed Searches) - After identifying search data table

---

## Expected Output Sizes

| Query | Expected Rows | Key Metrics |
|-------|--------------|-------------|
| Query 1 | ~6,500 (Mainland merchants) | Merchant coverage |
| Query 2 | 24 (hours 0-23) | Demand patterns |
| Query 3 | 5 (basket buckets) | Basket distribution |
| Query 4 | ~12 (Mainland areas) | Operational health |
| Query 5 | ~500-2,000 (churned merchants) | Win-back list |
| Query 6 | ~12 (Mainland areas) | Distance/fee analysis |
| Query 7 | 20 (top failed searches) | Cuisine gaps |

---

## Integration with Growth Plan

### Supply Gaps (What are we missing?)
- **Query 1**: Current merchant coverage by cuisine & Halal
- **Query 5**: Churned merchants (win-back targets)
- **Query 7**: Failed searches (unmet demand)

### Demand Patterns (When and How do they eat?)
- **Query 2**: Hourly order distribution (Supper vs Dinner market)
- **Query 3**: Basket size distribution (Family vs Single-pax)

### Operational Friction (Why are we losing orders?)
- **Query 4**: Cancellation & no-driver rates by zone
- **Query 6**: Delivery distance & fee analysis

---

## Questions or Issues?

If queries fail or return unexpected results:
1. **Verify area names**: Run area lookup query first
2. **Check date ranges**: Ensure date_id format is correct (YYYYMMDD integer)
3. **Verify table schemas**: Use `get_table_definition` MCP tool
4. **Check data availability**: Some metrics may not exist for all time periods

---

## Next Steps After Data Extraction

1. **Load data into Excel/Python** for analysis
2. **Create visualizations**:
   - Heatmap: Hourly order distribution (Query 2)
   - Histogram: Basket size distribution (Query 3)
   - Bar chart: Cancellation rates by area (Query 4)
3. **Build growth plan** using insights from all queries
4. **Prioritize actions**:
   - High cancellation areas → Fix ops first
   - High failed searches → Acquire merchants
   - Large basket areas → Push family bundles

