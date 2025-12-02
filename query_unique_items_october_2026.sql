-- Query: Count unique item_ids successfully uploaded on October 25, 2025 from outer cities
-- Filter: Specific merchant_campaign_name values
-- Outer cities: city_id != 1 (exclude Klang Valley)
-- Result: 2,471 unique item_ids
--
-- ASSUMPTIONS:
-- 1. "Successfully uploaded" = items present in d_campaign_eligible_item (presence implies success)
-- 2. Upload date = campaign start_time (if upload_date exists in cei, use that instead)
-- 3. If cei has a status field, add: AND cei.status = 'ACTIVE' (or appropriate success status)

SELECT 
    COUNT(DISTINCT cei.eligible_item_id) as total_unique_item_ids
FROM 
    ocd_adw.d_campaign_eligible_item cei
INNER JOIN 
    ocd_adw.d_merchant_funded_campaign mfc 
    ON cei.campaign_id = mfc.campaign_id
WHERE 
    -- Outer cities filter (exclude Klang Valley)
    mfc.city_id != 1
    
    -- October 25, 2025 filter (using campaign start_time as proxy for upload date)
    -- If d_campaign_eligible_item has upload_date/created_at, use that instead:
    -- AND CAST(cei.upload_date AS DATE) = DATE '2025-10-25'
    AND CAST(mfc.start_time AS DATE) = DATE '2025-10-25'
    
    -- Merchant campaign name filter (exact match)
    AND mfc.merchant_campaign_name IN (
        '50% Off 2nd item',
        'Buy 1 Get 1 Free',
        '50% Off 2nd meal',
        'Buy 1 Free 1',
        'Buy 1, Free 1',
        'Buy One Free One'
    )
    
    -- Additional filters for data quality
    AND mfc.country_code = 'MY'
    AND mfc.author_type = 'Operations'
    
    -- Successfully uploaded: items that are in the campaign
    -- If d_campaign_eligible_item has a status field indicating success, add filter:
    -- AND (cei.status = 'ACTIVE' OR cei.status = 'APPROVED' OR cei.upload_status = 'SUCCESS')
    -- If there's a rejection/failure status, exclude it:
    -- AND cei.status != 'REJECTED'
    -- AND cei.status != 'FAILED'
;

