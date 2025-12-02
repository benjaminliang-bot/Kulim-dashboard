-- ============================================================================
-- PENANG COMMISSION RATE ANALYSIS
-- Calculate average commission rate = Gross Commission Billing / GMV
-- ============================================================================

WITH penang_metrics AS (
    SELECT 
        -- Total GMV (completed orders only)
        SUM(CASE 
            WHEN f.booking_state_simple = 'COMPLETED' 
            THEN COALESCE(f.gross_merchandise_value, 0) 
            ELSE 0 
        END) as total_gmv,
        
        -- Total Gross Commission Billing (completed orders only)
        SUM(CASE 
            WHEN f.booking_state_simple = 'COMPLETED' 
            THEN COALESCE(f.commission_from_merchant, 0) 
            ELSE 0 
        END) as total_commission_billing,
        
        -- Count of completed orders
        COUNT(DISTINCT CASE 
            WHEN f.booking_state_simple = 'COMPLETED' 
            THEN f.order_id 
        END) as completed_orders,
        
        -- Count of total orders
        COUNT(DISTINCT f.order_id) as total_orders,
        
        -- Date range info
        MIN(f.date_id) as min_date,
        MAX(f.date_id) as max_date
    FROM ocd_adw.f_food_metrics f
    WHERE f.city_id = 13  -- Penang city_id
        AND f.country_id = 1  -- Malaysia
        AND f.business_type = 0  -- Food delivery
        -- Adjust date range as needed (e.g., last 6 months, or specific period)
        AND f.date_id >= 20250401  -- April 2025 onwards
        AND f.date_id < 20251101   -- Before November 2025
)
SELECT 
    total_gmv,
    total_commission_billing,
    completed_orders,
    total_orders,
    -- Calculate commission rate
    ROUND(total_commission_billing * 100.0 / NULLIF(total_gmv, 0), 4) as commission_rate_pct,
    -- Additional metrics
    ROUND(total_commission_billing / NULLIF(completed_orders, 0), 2) as avg_commission_per_order,
    ROUND(total_gmv / NULLIF(completed_orders, 0), 2) as avg_gmv_per_order,
    -- Date range
    min_date,
    max_date
FROM penang_metrics;

-- ============================================================================
-- MONTHLY BREAKDOWN (Optional - to see trends)
-- ============================================================================

WITH monthly_metrics AS (
    SELECT 
        CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER) as month_id,
        SUM(CASE 
            WHEN f.booking_state_simple = 'COMPLETED' 
            THEN COALESCE(f.gross_merchandise_value, 0) 
            ELSE 0 
        END) as total_gmv,
        SUM(CASE 
            WHEN f.booking_state_simple = 'COMPLETED' 
            THEN COALESCE(f.commission_from_merchant, 0) 
            ELSE 0 
        END) as total_commission_billing
    FROM ocd_adw.f_food_metrics f
    WHERE f.city_id = 13
        AND f.country_id = 1
        AND f.business_type = 0
        AND f.date_id >= 20250401
        AND f.date_id < 20251101
    GROUP BY CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER)
)
SELECT 
    month_id,
    total_gmv,
    total_commission_billing,
    ROUND(total_commission_billing * 100.0 / NULLIF(total_gmv, 0), 4) as commission_rate_pct,
    -- MoM change
    LAG(ROUND(total_commission_billing * 100.0 / NULLIF(total_gmv, 0), 4)) 
        OVER (ORDER BY month_id) as prev_month_commission_rate,
    ROUND(
        (ROUND(total_commission_billing * 100.0 / NULLIF(total_gmv, 0), 4)) - 
        LAG(ROUND(total_commission_billing * 100.0 / NULLIF(total_gmv, 0), 4)) 
            OVER (ORDER BY month_id), 
        4
    ) as commission_rate_change
FROM monthly_metrics
ORDER BY month_id;
