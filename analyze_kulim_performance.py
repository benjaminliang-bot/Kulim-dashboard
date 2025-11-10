"""
Comprehensive analysis for Kulim, Penang performance
Supports findings from manual update document with quantitative data
"""

import json
import sys
import io
from typing import List, Dict, Any
from datetime import datetime

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Note: This script generates SQL queries to be executed via MCP tools
# The actual execution will be done through Hubble/Presto MCP

def generate_kulim_merchant_list_query() -> str:
    """Get list of all active merchants in Kulim using area_id from d_area"""
    return """
    WITH kulim_areas AS (
        SELECT DISTINCT area_id
        FROM ocd_adw.d_area
        WHERE city_id = 13 
            AND LOWER(area_name) LIKE '%kulim%'
    )
    SELECT 
        m.merchant_id,
        m.merchant_id_nk,
        m.merchant_name,
        m.district,
        a.area_name,
        a.subcity_name,
        m.segment,
        m.custom_segment,
        m.am_name,
        m.status,
        m.is_bd_account,
        m.is_bd_partner
    FROM ocd_adw.d_merchant m
    INNER JOIN ocd_adw.d_area a 
        ON m.city_id = a.city_id 
        AND m.geohash = a.geohash
    INNER JOIN kulim_areas ka ON a.area_id = ka.area_id
    WHERE m.city_id = 13 
        AND m.status = 'ACTIVE'
    ORDER BY m.merchant_name
    """

def generate_kulim_gmv_monthly_query() -> str:
    """Get monthly GMV for Kulim merchants (Sep, Oct, Nov 2025) using area_id from d_area"""
    return """
    WITH kulim_areas AS (
        SELECT DISTINCT area_id
        FROM ocd_adw.d_area
        WHERE city_id = 13 
            AND LOWER(area_name) LIKE '%kulim%'
    ),
    kulim_merchants AS (
        SELECT DISTINCT m.merchant_id_nk
        FROM ocd_adw.d_merchant m
        INNER JOIN ocd_adw.d_area a 
            ON m.city_id = a.city_id 
            AND m.geohash = a.geohash
        INNER JOIN kulim_areas ka ON a.area_id = ka.area_id
        WHERE m.city_id = 13 
            AND m.status = 'ACTIVE'
    ),
    monthly_gmv AS (
        SELECT 
            CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER) as month_id,
            COUNT(DISTINCT f.merchant_id) as active_merchants,
            COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.passenger_id END) as unique_passengers,
            COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END) as completed_orders,
            SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.gross_merchandise_value ELSE 0 END) as total_gmv,
            AVG(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.gross_merchandise_value END) as avg_order_value
        FROM ocd_adw.f_food_metrics f
        WHERE f.city_id = 13
            AND f.country_id = 1
            AND f.business_type = 0
            AND f.merchant_id IN (SELECT merchant_id_nk FROM kulim_merchants)
            AND CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER) IN (202509, 202510, 202511)
        GROUP BY CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER)
    )
    SELECT 
        month_id,
        active_merchants,
        unique_passengers,
        completed_orders,
        total_gmv,
        avg_order_value,
        CASE 
            WHEN LAG(total_gmv) OVER (ORDER BY month_id) > 0 
            THEN ((total_gmv - LAG(total_gmv) OVER (ORDER BY month_id)) / LAG(total_gmv) OVER (ORDER BY month_id)) * 100
            ELSE NULL
        END as mom_growth_pct
    FROM monthly_gmv
    ORDER BY month_id
    """

def generate_kulim_merchant_performance_query() -> str:
    """Get top performing merchants in Kulim using area_id from d_area"""
    return """
    WITH kulim_areas AS (
        SELECT DISTINCT area_id
        FROM ocd_adw.d_area
        WHERE city_id = 13 
            AND LOWER(area_name) LIKE '%kulim%'
    ),
    kulim_merchants AS (
        SELECT DISTINCT m.merchant_id_nk, m.merchant_name, m.segment, m.custom_segment, m.am_name
        FROM ocd_adw.d_merchant m
        INNER JOIN ocd_adw.d_area a 
            ON m.city_id = a.city_id 
            AND m.geohash = a.geohash
        INNER JOIN kulim_areas ka ON a.area_id = ka.area_id
        WHERE m.city_id = 13 
            AND m.status = 'ACTIVE'
    ),
    merchant_gmv AS (
        SELECT 
            f.merchant_id,
            COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.passenger_id END) as unique_passengers,
            COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END) as completed_orders,
            SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.gross_merchandise_value ELSE 0 END) as total_gmv,
            AVG(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.gross_merchandise_value END) as avg_order_value
        FROM ocd_adw.f_food_metrics f
        WHERE f.city_id = 13
            AND f.country_id = 1
            AND f.business_type = 0
            AND f.merchant_id IN (SELECT merchant_id_nk FROM kulim_merchants)
            AND CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER) IN (202509, 202510, 202511)
        GROUP BY f.merchant_id
    )
    SELECT 
        m.merchant_id_nk,
        m.merchant_name,
        m.segment,
        m.custom_segment,
        m.am_name,
        COALESCE(g.total_gmv, 0) as total_gmv,
        COALESCE(g.completed_orders, 0) as completed_orders,
        COALESCE(g.unique_passengers, 0) as unique_passengers,
        COALESCE(g.avg_order_value, 0) as avg_order_value,
        CASE 
            WHEN COALESCE(g.total_gmv, 0) > 0 THEN 'Active'
            ELSE 'Inactive'
        END as performance_status
    FROM kulim_merchants m
    LEFT JOIN merchant_gmv g ON m.merchant_id_nk = g.merchant_id
    ORDER BY g.total_gmv DESC NULLS LAST
    LIMIT 50
    """

def generate_kulim_campaign_participation_query() -> str:
    """Get campaign participation for Kulim merchants using area_id from d_area"""
    return """
    WITH kulim_areas AS (
        SELECT DISTINCT area_id
        FROM ocd_adw.d_area
        WHERE city_id = 13 
            AND LOWER(area_name) LIKE '%kulim%'
    ),
    kulim_merchants AS (
        SELECT DISTINCT m.merchant_id_nk
        FROM ocd_adw.d_merchant m
        INNER JOIN ocd_adw.d_area a 
            ON m.city_id = a.city_id 
            AND m.geohash = a.geohash
        INNER JOIN kulim_areas ka ON a.area_id = ka.area_id
        WHERE m.city_id = 13 
            AND m.status = 'ACTIVE'
    ),
    campaign_data AS (
        SELECT 
            f.merchant_id,
            CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER) as month_id,
            COUNT(DISTINCT CASE 
                WHEN f.booking_state_simple = 'COMPLETED' 
                AND f.promo_code IS NOT NULL 
                AND f.promo_code != ''
                THEN f.promo_code 
            END) as unique_campaigns,
            COUNT(DISTINCT CASE 
                WHEN f.booking_state_simple = 'COMPLETED' 
                AND f.promo_code IS NOT NULL 
                AND f.promo_code != ''
                THEN f.order_id 
            END) as campaign_orders,
            SUM(CASE 
                WHEN f.booking_state_simple = 'COMPLETED' 
                AND f.promo_code IS NOT NULL 
                AND f.promo_code != ''
                THEN f.gross_merchandise_value 
                ELSE 0 
            END) as campaign_gmv,
            COUNT(DISTINCT CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.order_id END) as total_orders,
            SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.gross_merchandise_value ELSE 0 END) as total_gmv
        FROM ocd_adw.f_food_metrics f
        WHERE f.city_id = 13
            AND f.country_id = 1
            AND f.business_type = 0
            AND f.merchant_id IN (SELECT merchant_id_nk FROM kulim_merchants)
            AND CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER) IN (202509, 202510, 202511)
        GROUP BY f.merchant_id, CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER)
    )
    SELECT 
        month_id,
        COUNT(DISTINCT merchant_id) as merchants_with_campaigns,
        SUM(unique_campaigns) as total_unique_campaigns,
        SUM(campaign_orders) as total_campaign_orders,
        SUM(campaign_gmv) as total_campaign_gmv,
        SUM(total_orders) as total_orders,
        SUM(total_gmv) as total_gmv,
        CASE 
            WHEN SUM(total_orders) > 0 
            THEN (SUM(campaign_orders) * 100.0 / SUM(total_orders))
            ELSE 0
        END as campaign_participation_rate,
        CASE 
            WHEN SUM(total_gmv) > 0 
            THEN (SUM(campaign_gmv) * 100.0 / SUM(total_gmv))
            ELSE 0
        END as campaign_gmv_share
    FROM campaign_data
    GROUP BY month_id
    ORDER BY month_id
    """

def generate_kulim_segmentation_analysis_query() -> str:
    """Analyze merchants by segmentation using area_id from d_area"""
    return """
    WITH kulim_areas AS (
        SELECT DISTINCT area_id
        FROM ocd_adw.d_area
        WHERE city_id = 13 
            AND LOWER(area_name) LIKE '%kulim%'
    ),
    kulim_merchants AS (
        SELECT 
            m.merchant_id_nk,
            m.merchant_name,
            m.segment,
            m.custom_segment,
            m.am_name,
            m.is_bd_account,
            m.is_bd_partner
        FROM ocd_adw.d_merchant m
        INNER JOIN ocd_adw.d_area a 
            ON m.city_id = a.city_id 
            AND m.geohash = a.geohash
        INNER JOIN kulim_areas ka ON a.area_id = ka.area_id
        WHERE m.city_id = 13 
            AND m.status = 'ACTIVE'
    ),
    merchant_gmv AS (
        SELECT 
            f.merchant_id,
            SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.gross_merchandise_value ELSE 0 END) as total_gmv,
            COUNT(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN 1 END) as completed_orders
        FROM ocd_adw.f_food_metrics f
        WHERE f.city_id = 13
            AND f.country_id = 1
            AND f.business_type = 0
            AND f.merchant_id IN (SELECT merchant_id_nk FROM kulim_merchants)
            AND CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER) IN (202509, 202510, 202511)
        GROUP BY f.merchant_id
    )
    SELECT 
        m.segment,
        m.custom_segment,
        COUNT(DISTINCT m.merchant_id_nk) as merchant_count,
        COUNT(DISTINCT CASE WHEN g.total_gmv > 0 THEN m.merchant_id_nk END) as active_merchants,
        SUM(COALESCE(g.total_gmv, 0)) as total_gmv,
        SUM(COALESCE(g.completed_orders, 0)) as total_orders,
        AVG(COALESCE(g.total_gmv, 0)) as avg_merchant_gmv,
        CASE 
            WHEN COUNT(DISTINCT m.merchant_id_nk) > 0 
            THEN (COUNT(DISTINCT CASE WHEN g.total_gmv > 0 THEN m.merchant_id_nk END) * 100.0 / COUNT(DISTINCT m.merchant_id_nk))
            ELSE 0
        END as activation_rate
    FROM kulim_merchants m
    LEFT JOIN merchant_gmv g ON m.merchant_id_nk = g.merchant_id
    GROUP BY m.segment, m.custom_segment
    ORDER BY total_gmv DESC
    """

def generate_kulim_t20_analysis_query() -> str:
    """Analyze T20 merchants in Kulim using area_id from d_area"""
    return """
    WITH kulim_areas AS (
        SELECT DISTINCT area_id
        FROM ocd_adw.d_area
        WHERE city_id = 13 
            AND LOWER(area_name) LIKE '%kulim%'
    ),
    kulim_merchants AS (
        SELECT DISTINCT m.merchant_id_nk, m.merchant_name, m.segment, m.custom_segment, m.am_name
        FROM ocd_adw.d_merchant m
        INNER JOIN ocd_adw.d_area a 
            ON m.city_id = a.city_id 
            AND m.geohash = a.geohash
        INNER JOIN kulim_areas ka ON a.area_id = ka.area_id
        WHERE m.city_id = 13 
            AND m.status = 'ACTIVE'
    ),
    merchant_gmv AS (
        SELECT 
            f.merchant_id,
            SUM(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN f.gross_merchandise_value ELSE 0 END) as total_gmv,
            COUNT(CASE WHEN f.booking_state_simple = 'COMPLETED' THEN 1 END) as completed_orders
        FROM ocd_adw.f_food_metrics f
        WHERE f.city_id = 13
            AND f.country_id = 1
            AND f.business_type = 0
            AND f.merchant_id IN (SELECT merchant_id_nk FROM kulim_merchants)
            AND CAST(SUBSTRING(CAST(f.date_id AS VARCHAR), 1, 6) AS INTEGER) IN (202509, 202510, 202511)
        GROUP BY f.merchant_id
    ),
    ranked_merchants AS (
        SELECT 
            m.merchant_id_nk,
            m.merchant_name,
            m.segment,
            m.custom_segment,
            m.am_name,
            COALESCE(g.total_gmv, 0) as total_gmv,
            COALESCE(g.completed_orders, 0) as completed_orders,
            PERCENT_RANK() OVER (ORDER BY COALESCE(g.total_gmv, 0) DESC) as gmv_percentile
        FROM kulim_merchants m
        LEFT JOIN merchant_gmv g ON m.merchant_id_nk = g.merchant_id
    )
    SELECT 
        merchant_id_nk,
        merchant_name,
        segment,
        custom_segment,
        am_name,
        total_gmv,
        completed_orders,
        CASE 
            WHEN gmv_percentile <= 0.20 THEN 'T20'
            WHEN gmv_percentile <= 0.30 THEN 'T3'
            ELSE 'Other'
        END as tier
    FROM ranked_merchants
    WHERE gmv_percentile <= 0.30
    ORDER BY total_gmv DESC
    """

def generate_analysis_summary() -> str:
    """Generate summary of all queries"""
    queries = {
        "kulim_merchant_list": generate_kulim_merchant_list_query(),
        "kulim_gmv_monthly": generate_kulim_gmv_monthly_query(),
        "kulim_merchant_performance": generate_kulim_merchant_performance_query(),
        "kulim_campaign_participation": generate_kulim_campaign_participation_query(),
        "kulim_segmentation_analysis": generate_kulim_segmentation_analysis_query(),
        "kulim_t20_analysis": generate_kulim_t20_analysis_query()
    }
    
    return json.dumps(queries, indent=2)

def main():
    print("="*80)
    print("KULIM, PENANG PERFORMANCE ANALYSIS QUERIES")
    print("="*80)
    print()
    print("This script generates SQL queries to analyze Kulim performance.")
    print("Queries should be executed via Hubble/Presto MCP tools.")
    print()
    print("="*80)
    print("QUERY SUMMARY")
    print("="*80)
    print()
    print("1. kulim_merchant_list: Get all active merchants in Kulim")
    print("2. kulim_gmv_monthly: Monthly GMV trends (Sep, Oct, Nov 2025)")
    print("3. kulim_merchant_performance: Top performing merchants")
    print("4. kulim_campaign_participation: Campaign participation analysis")
    print("5. kulim_segmentation_analysis: Segmentation breakdown")
    print("6. kulim_t20_analysis: T20 merchant identification and analysis")
    print()
    print("="*80)
    print("QUERIES GENERATED")
    print("="*80)
    print()
    
    # Save queries to file
    queries = {
        "kulim_merchant_list": generate_kulim_merchant_list_query(),
        "kulim_gmv_monthly": generate_kulim_gmv_monthly_query(),
        "kulim_merchant_performance": generate_kulim_merchant_performance_query(),
        "kulim_campaign_participation": generate_kulim_campaign_participation_query(),
        "kulim_segmentation_analysis": generate_kulim_segmentation_analysis_query(),
        "kulim_t20_analysis": generate_kulim_t20_analysis_query()
    }
    
    with open('kulim_analysis_queries.json', 'w', encoding='utf-8') as f:
        json.dump(queries, f, indent=2, ensure_ascii=False)
    
    print("Queries saved to: kulim_analysis_queries.json")
    print()
    print("="*80)
    print("NEXT STEPS")
    print("="*80)
    print()
    print("1. Review queries in kulim_analysis_queries.json")
    print("2. Execute queries via Hubble/Presto MCP tools")
    print("3. Analyze results to support findings in manual update document")
    print("4. Generate insights and recommendations based on data")

if __name__ == '__main__':
    main()

