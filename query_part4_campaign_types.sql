CAMPAIGN TYPE BREAKDOWN (Hotdeals, Delivery Campaigns)
SELECT DISTINCT
    campaign_type,
    COUNT(*) as campaign_count,
    COUNT(DISTINCT merchant_id) as merchant_count,
    COUNT(DISTINCT CASE WHEN mexfunded_ratio > 0 THEN merchant_id END) as mex_funded_merchants,
    COUNT(DISTINCT CASE WHEN mexfunded_ratio = 0 OR mexfunded_ratio IS NULL THEN merchant_id END) as grab_funded_merchants
FROM ocd_adw.d_merchant_funded_campaign
WHERE city_id = 13
    AND CAST(start_time AS DATE) >= DATE '2025-05-01'
    AND CAST(start_time AS DATE) < DATE '2025-11-01'
GROUP BY campaign_type
ORDER BY campaign_count DESC
LIMIT 20;