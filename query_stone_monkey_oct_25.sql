-- Query: Count unique item_ids from "stone monkey" system
-- Filters:
--   - Campaign form: 1323
--   - Team tag: "OC"
--   - Campaign date: October 25, 2025
--   - Status: "Success"
--
-- NOTE: "Stone monkey" table not found in accessible schemas.
-- This query attempts to use d_campaign_eligible_item with d_merchant_funded_campaign
-- Adjust table/schema names based on actual "stone monkey" system location

SELECT 
    COUNT(DISTINCT cei.eligible_item_id) as total_unique_item_ids
FROM 
    ocd_adw.d_campaign_eligible_item cei
INNER JOIN 
    ocd_adw.d_merchant_funded_campaign mfc 
    ON cei.campaign_id = mfc.campaign_id
INNER JOIN 
    ocd_adw.d_merchant m 
    ON mfc.merchant_id = m.merchant_id_nk
WHERE 
    -- Campaign date: October 25, 2025
    CAST(mfc.start_time AS DATE) = DATE '2025-10-25'
    
    -- Campaign form 1323 (assuming this maps to author_type or a form field)
    -- If form is a separate field, adjust accordingly:
    -- AND mfc.form_id = 1323
    -- OR if it's author_type:
    -- AND mfc.author_type = '1323'
    
    -- Team tag "OC" (assuming this is in merchant table or campaign table)
    -- If team_tag is in merchant table:
    -- AND m.team_tag = 'OC'
    -- OR if it's in campaign meta/business_tag:
    -- AND mfc.business_tag = 'OC'
    
    -- Status: "Success" (assuming this maps to campaign_status or item status)
    -- AND mfc.campaign_status = 'Success'
    -- OR if item-level status:
    -- AND cei.status = 'Success'
    
    AND mfc.country_code = 'MY'
;





