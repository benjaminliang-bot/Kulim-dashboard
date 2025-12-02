# Search Data Discovery Guide for Query 7

## Problem
Query 7 needs to identify "failed searches" - search queries that resulted in no results or no conversion. However, direct search query data may not be available in standard `ocd_adw` tables.

## Solution Approach

### ✅ **Option 1: Use Session Data (IMPLEMENTED)**
**Status**: Ready to use - Query 7 now uses this approach

**Method**: Identify sessions with no completed orders as a proxy for failed searches
- **Logic**: If a user has a `scribe_session_id` but no completed orders, they likely:
  1. Searched but found no results
  2. Found results but didn't like them
  3. Encountered friction (high fees, long delivery time)

**Query**: See Query 7 in `penang_mainland_growth_analysis_queries.sql`

**Output**:
- Sessions with no orders by area and hour
- Session drop-off rate (failed sessions / total sessions)
- Unique users who didn't convert

**Limitations**:
- Doesn't show actual search queries
- Can't distinguish between "no results" vs "didn't like results"
- May include users who just browsed without searching

---

### 🔍 **Option 2: Find Search Analytics Tables (DISCOVERY NEEDED)**

**Step 1**: Run discovery queries to find search tables

```sql
-- Run this in Presto/Trino
SELECT 
    table_schema,
    table_name
FROM information_schema.tables
WHERE table_schema = 'ocd_adw'
    AND (
        table_name LIKE '%search%' 
        OR table_name LIKE '%query%'
        OR table_name LIKE '%session%'
        OR table_name LIKE '%scribe%'
    )
ORDER BY table_name;
```

**Step 2**: If tables found, check their schema:

```sql
SELECT 
    column_name,
    data_type
FROM information_schema.columns
WHERE table_schema = 'ocd_adw' 
    AND table_name = '[FOUND_TABLE_NAME]'
ORDER BY ordinal_position;
```

**Step 3**: Update Query 7 template with actual table and column names

**Common Table Names to Look For**:
- `f_food_search_log`
- `d_scribe_session` (dimension table with session details)
- `f_user_search_events`
- `f_search_analytics`
- `d_search_query`

---

### 🔍 **Option 3: Check track_events_v2 (IF AVAILABLE)**

**Table**: `grab_x.track_events_v2`

**Requirements**:
- Requires `scope` filter (e.g., `scope = 'grab_food'`)
- May contain search events in `event_name` and `event_properties`

**Discovery Query**:
```sql
SELECT DISTINCT
    event_name,
    event_properties
FROM grab_x.track_events_v2
WHERE scope = 'grab_food'  -- ADJUST SCOPE AS NEEDED
    AND event_name LIKE '%search%'
    AND ingestion_date >= CURRENT_DATE - INTERVAL '7' DAY
LIMIT 100;
```

**If search events exist**, they might have:
- `event_properties['search_query']` - The actual search term
- `event_properties['has_results']` - Whether results were returned
- `event_properties['result_count']` - Number of results

**Note**: See commented section in Query 7 for template using track_events_v2

---

### 🔍 **Option 4: Contact Data Team**

**Questions to Ask**:
1. Where is user search query data stored?
2. Is there a search analytics table in `ocd_adw` or another schema?
3. Can we access search events from `track_events_v2`?
4. Is there a `d_scribe_session` dimension table with search details?

**Information to Provide**:
- Need: Search queries that resulted in no results or no conversion
- Location: Penang Mainland areas
- Time period: Last 3 months
- Purpose: Identify cuisine gaps for merchant acquisition

---

## Recommended Action Plan

### Immediate (Use Now):
1. ✅ **Use Query 7 as implemented** (Option 1 - Session Data)
   - Provides proxy metric for unmet demand
   - Shows areas/hours with high session drop-off
   - Actionable for identifying operational issues

### Short-term (This Week):
2. 🔍 **Run discovery queries** (Option 2)
   - Execute `find_search_data_tables.sql`
   - Check if search tables exist
   - If found, update Query 7 with actual table structure

3. 🔍 **Check track_events_v2** (Option 3)
   - Run discovery query above
   - If search events exist, use commented template in Query 7

### Long-term (If Needed):
4. 📧 **Contact data team** (Option 4)
   - If no search tables found
   - Request access or data export
   - May need to set up new data pipeline

---

## What Query 7 Currently Provides (Session-Based Approach)

### Metrics:
- **Sessions with no orders**: Users who browsed but didn't order
- **Session drop-off rate**: % of sessions that didn't convert
- **By area and hour**: Identifies where/when demand is lost

### Insights:
- **High drop-off in specific area** → Potential supply gap or operational issue
- **High drop-off at specific hours** → Demand exists but not met
- **High attempted orders but all cancelled** → Operational friction (driver shortage, fees)

### Action Items:
- Areas with >30% session drop-off → Investigate supply gaps
- Hours with high drop-off → Target merchant acquisition for those times
- High cancellation rate → Fix operational issues first

---

## Next Steps

1. **Execute Query 7** (session-based) to get initial insights
2. **Run discovery queries** to find search tables
3. **If search tables found**, update Query 7 with actual search query data
4. **If not found**, use session-based approach as proxy metric

---

## Files Created

1. **`find_search_data_tables.sql`**: Discovery queries to find search tables
2. **`penang_mainland_growth_analysis_queries.sql`**: Updated Query 7 with working session-based approach
3. **`search_data_discovery_guide.md`**: This guide

