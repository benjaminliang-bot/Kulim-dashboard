-- Query: Count unique item_ids from stone_monkey table
-- Filters:
--   - Campaign form: 1323
--   - Team tag: "OC"
--   - Campaign date: October 25, 2025
--   - Status: "Success"

-- Query: Count unique item_ids from stone_monkey.my_campaign_creation
-- Filters:
--   - Team tag: "OC AM" (OC team)
--   - Campaign date: October 25, 2025
--   - Status: "Success"
-- Note: Form 1323 column not found in table structure.
--       If all records in my_campaign_creation are from form 1323, no form filter needed.
--       Otherwise, form filter needs to be added once form column location is identified.

SELECT 
    COUNT(DISTINCT c_item_id) as total_unique_item_ids
FROM 
    stone_monkey.my_campaign_creation
WHERE 
    -- Team tag filter (OC AM for Outer Cities)
    c_team_tag = 'OC AM'
    
    -- Campaign date: October 25, 2025
    AND CAST(c_applicable_to_month AS DATE) = DATE '2025-10-25'
    
    -- Status: Success
    AND c_status = 'Success'
    
    -- Form 1323 filter (if form column exists, uncomment and adjust):
    -- AND form = 1323
    -- OR if form is in a related table, add join
;

