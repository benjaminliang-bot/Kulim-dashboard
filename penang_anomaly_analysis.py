"""
Penang Daily Trend Anomaly Detection & Causal Inference Analysis
Analyzes daily GMV & Orders trends, identifies anomalies, and suggests root causes
"""

import json
from datetime import datetime
from typing import Dict, List, Tuple

# Query results from MCP
data = [
    {'period': 'Same Week Last Year', 'date_id': 20241110, 'daily_orders': 37251, 'daily_completed_orders': 34860, 'daily_gmv': 1314059.39, 'daily_wtu': 29487, 'avg_basket_size': 33.22, 'daily_promo_expense': 121696.75, 'daily_promo_orders': 17163, 'daily_sessions': 33301, 'daily_active_merchants': 3597, 'promo_penetration_pct': 49.2, 'cops': 1.047},
    {'period': 'Same Week Last Year', 'date_id': 20241111, 'daily_orders': 32868, 'daily_completed_orders': 30748, 'daily_gmv': 1074368.2, 'daily_wtu': 26690, 'avg_basket_size': 30.76, 'daily_promo_expense': 106197.59, 'daily_promo_orders': 15043, 'daily_sessions': 29751, 'daily_active_merchants': 3561, 'promo_penetration_pct': 48.9, 'cops': 1.034},
    {'period': 'Same Week Last Year', 'date_id': 20241112, 'daily_orders': 33283, 'daily_completed_orders': 31298, 'daily_gmv': 1083183.14, 'daily_wtu': 27215, 'avg_basket_size': 30.55, 'daily_promo_expense': 102920.93, 'daily_promo_orders': 15131, 'daily_sessions': 30201, 'daily_active_merchants': 3649, 'promo_penetration_pct': 48.3, 'cops': 1.036},
    {'period': 'Same Week Last Year', 'date_id': 20241113, 'daily_orders': 33724, 'daily_completed_orders': 31707, 'daily_gmv': 1114516.59, 'daily_wtu': 27625, 'avg_basket_size': 31.05, 'daily_promo_expense': 100939.18, 'daily_promo_orders': 15218, 'daily_sessions': 30589, 'daily_active_merchants': 3734, 'promo_penetration_pct': 48.0, 'cops': 1.037},
    {'period': 'Same Week Last Year', 'date_id': 20241114, 'daily_orders': 34080, 'daily_completed_orders': 32067, 'daily_gmv': 1115995.5, 'daily_wtu': 27906, 'avg_basket_size': 30.72, 'daily_promo_expense': 102441.05, 'daily_promo_orders': 15377, 'daily_sessions': 30944, 'daily_active_merchants': 3793, 'promo_penetration_pct': 48.0, 'cops': 1.036},
    {'period': 'Same Week Last Year', 'date_id': 20241115, 'daily_orders': 35216, 'daily_completed_orders': 32966, 'daily_gmv': 1196276.36, 'daily_wtu': 28489, 'avg_basket_size': 31.96, 'daily_promo_expense': 108826.92, 'daily_promo_orders': 16161, 'daily_sessions': 31763, 'daily_active_merchants': 3818, 'promo_penetration_pct': 49.0, 'cops': 1.038},
    {'period': 'Same Week Last Year', 'date_id': 20241116, 'daily_orders': 36412, 'daily_completed_orders': 34099, 'daily_gmv': 1293600.1, 'daily_wtu': 29148, 'avg_basket_size': 33.45, 'daily_promo_expense': 114263.31, 'daily_promo_orders': 16599, 'daily_sessions': 32712, 'daily_active_merchants': 3766, 'promo_penetration_pct': 48.7, 'cops': 1.042},
    {'period': 'This Week', 'date_id': 20251110, 'daily_orders': 38007, 'daily_completed_orders': 35110, 'daily_gmv': 1295598.57, 'daily_wtu': 30457, 'avg_basket_size': 32.67, 'daily_promo_expense': 146607.38, 'daily_promo_orders': 19101, 'daily_sessions': 34093, 'daily_active_merchants': 4157, 'promo_penetration_pct': 54.4, 'cops': 1.03},
    {'period': 'This Week', 'date_id': 20251111, 'daily_orders': 38271, 'daily_completed_orders': 35656, 'daily_gmv': 1339028.44, 'daily_wtu': 30919, 'avg_basket_size': 33.27, 'daily_promo_expense': 149248.38, 'daily_promo_orders': 19540, 'daily_sessions': 34386, 'daily_active_merchants': 4119, 'promo_penetration_pct': 54.8, 'cops': 1.037},
    {'period': 'This Week', 'date_id': 20251112, 'daily_orders': 39849, 'daily_completed_orders': 37078, 'daily_gmv': 1384682.11, 'daily_wtu': 32063, 'avg_basket_size': 33.16, 'daily_promo_expense': 162990.28, 'daily_promo_orders': 20418, 'daily_sessions': 35743, 'daily_active_merchants': 4254, 'promo_penetration_pct': 55.1, 'cops': 1.037},
    {'period': 'This Week', 'date_id': 20251113, 'daily_orders': 40078, 'daily_completed_orders': 37478, 'daily_gmv': 1409446.23, 'daily_wtu': 32377, 'avg_basket_size': 33.45, 'daily_promo_expense': 167811.54, 'daily_promo_orders': 20899, 'daily_sessions': 36172, 'daily_active_merchants': 4358, 'promo_penetration_pct': 55.8, 'cops': 1.036},
    {'period': 'This Week', 'date_id': 20251114, 'daily_orders': 41215, 'daily_completed_orders': 38546, 'daily_gmv': 1485702.97, 'daily_wtu': 33226, 'avg_basket_size': 34.35, 'daily_promo_expense': 178227.38, 'daily_promo_orders': 21669, 'daily_sessions': 37086, 'daily_active_merchants': 4365, 'promo_penetration_pct': 56.2, 'cops': 1.039},
    {'period': 'This Week', 'date_id': 20251115, 'daily_orders': 43408, 'daily_completed_orders': 40543, 'daily_gmv': 1610033.44, 'daily_wtu': 34018, 'avg_basket_size': 35.40, 'daily_promo_expense': 186089.63, 'daily_promo_orders': 23283, 'daily_sessions': 38526, 'daily_active_merchants': 4325, 'promo_penetration_pct': 57.4, 'cops': 1.052},
    {'period': 'This Week', 'date_id': 20251116, 'daily_orders': 41946, 'daily_completed_orders': 38899, 'daily_gmv': 1537454.23, 'daily_wtu': 32831, 'avg_basket_size': 35.13, 'daily_promo_expense': 180642.03, 'daily_promo_orders': 22408, 'daily_sessions': 37319, 'daily_active_merchants': 4109, 'promo_penetration_pct': 57.6, 'cops': 1.042}
]

def format_date(date_id: int) -> str:
    """Format YYYYMMDD to readable date"""
    date_str = str(date_id)
    return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"

def format_number(num: float) -> str:
    """Format large numbers"""
    if num >= 1000000:
        return f"{num/1000000:.2f}M"
    elif num >= 1000:
        return f"{num/1000:.1f}K"
    return f"{num:,.0f}"

def calculate_yoy_growth(this_week: Dict, last_year: Dict, metric: str) -> float:
    """Calculate YoY growth percentage"""
    this_val = this_week.get(metric, 0)
    last_val = last_year.get(metric, 0)
    if last_val == 0:
        return 0.0
    return ((this_val - last_val) / last_val) * 100

def identify_anomalies(this_week_data: List[Dict], last_year_data: List[Dict]) -> List[Dict]:
    """Identify anomalies by comparing day-by-day"""
    anomalies = []
    
    # Create lookup by day of week (0=Monday, 6=Sunday)
    last_year_by_dow = {}
    for row in last_year_data:
        date_obj = datetime.strptime(str(row['date_id']), '%Y%m%d')
        dow = date_obj.weekday()
        last_year_by_dow[dow] = row
    
    for this_row in this_week_data:
        date_obj = datetime.strptime(str(this_row['date_id']), '%Y%m%d')
        dow = date_obj.weekday()
        last_row = last_year_by_dow.get(dow)
        
        if not last_row:
            continue
        
        # Calculate YoY changes
        orders_yoy = calculate_yoy_growth(this_row, last_row, 'daily_completed_orders')
        gmv_yoy = calculate_yoy_growth(this_row, last_row, 'daily_gmv')
        basket_yoy = calculate_yoy_growth(this_row, last_row, 'avg_basket_size')
        sessions_yoy = calculate_yoy_growth(this_row, last_row, 'daily_sessions')
        wtu_yoy = calculate_yoy_growth(this_row, last_row, 'daily_wtu')
        merchants_yoy = calculate_yoy_growth(this_row, last_row, 'daily_active_merchants')
        promo_pen_yoy = this_row['promo_penetration_pct'] - last_row['promo_penetration_pct']
        
        # Flag anomalies
        is_anomaly = False
        anomaly_reasons = []
        
        # Significant deviation thresholds
        if abs(orders_yoy) > 20 or abs(gmv_yoy) > 20:
            is_anomaly = True
            if orders_yoy < -20:
                anomaly_reasons.append(f"Orders down {abs(orders_yoy):.1f}% YoY")
            elif orders_yoy > 20:
                anomaly_reasons.append(f"Orders up {orders_yoy:.1f}% YoY")
            if gmv_yoy < -20:
                anomaly_reasons.append(f"GMV down {abs(gmv_yoy):.1f}% YoY")
            elif gmv_yoy > 20:
                anomaly_reasons.append(f"GMV up {gmv_yoy:.1f}% YoY")
        
        # Basket size anomaly
        if abs(basket_yoy) > 10:
            is_anomaly = True
            if basket_yoy < -10:
                anomaly_reasons.append(f"Basket down {abs(basket_yoy):.1f}% YoY")
            elif basket_yoy > 10:
                anomaly_reasons.append(f"Basket up {basket_yoy:.1f}% YoY")
        
        # Sessions anomaly
        if abs(sessions_yoy) > 15:
            is_anomaly = True
            if sessions_yoy < -15:
                anomaly_reasons.append(f"Sessions down {abs(sessions_yoy):.1f}% YoY")
            elif sessions_yoy > 15:
                anomaly_reasons.append(f"Sessions up {sessions_yoy:.1f}% YoY")
        
        if is_anomaly:
            anomalies.append({
                'date': format_date(this_row['date_id']),
                'day_of_week': date_obj.strftime('%A'),
                'reasons': anomaly_reasons,
                'this_week': this_row,
                'last_year': last_row,
                'yoy_changes': {
                    'orders': orders_yoy,
                    'gmv': gmv_yoy,
                    'basket': basket_yoy,
                    'sessions': sessions_yoy,
                    'wtu': wtu_yoy,
                    'merchants': merchants_yoy,
                    'promo_penetration': promo_pen_yoy
                }
            })
    
    return anomalies

def causal_inference_analysis(anomalies: List[Dict]) -> List[Dict]:
    """Perform causal inference analysis to suggest root causes"""
    causal_insights = []
    
    for anomaly in anomalies:
        this_week = anomaly['this_week']
        last_year = anomaly['last_year']
        yoy = anomaly['yoy_changes']
        
        insights = []
        confidence = []
        
        # Causal Factor 1: Promo Penetration Impact
        if yoy['promo_penetration'] > 5:
            # Higher promo penetration
            if yoy['orders'] > 10 and yoy['gmv'] > 5:
                insights.append("HIGH PROMO PENETRATION driving volume growth")
                confidence.append("HIGH")
            elif yoy['orders'] < -5:
                insights.append("High promo penetration but orders declining - promo effectiveness issue")
                confidence.append("MEDIUM")
        
        # Causal Factor 2: Sessions vs Orders Mismatch
        if yoy['sessions'] > 10 and yoy['orders'] < 5:
            insights.append("Sessions up but orders flat - conversion issue (COPS declining)")
            confidence.append("HIGH")
        elif yoy['sessions'] < -10 and yoy['orders'] < -10:
            insights.append("Sessions decline driving order decline - traffic acquisition issue")
            confidence.append("HIGH")
        
        # Causal Factor 3: Basket Size Impact
        if yoy['basket'] > 10 and yoy['gmv'] > yoy['orders']:
            insights.append("Basket expansion driving GMV growth beyond order growth")
            confidence.append("HIGH")
        elif yoy['basket'] < -10 and yoy['gmv'] < yoy['orders']:
            insights.append("Basket compression amplifying GMV decline")
            confidence.append("HIGH")
        
        # Causal Factor 4: Merchant Base Impact
        if yoy['merchants'] > 10 and yoy['orders'] > 10:
            insights.append("Merchant base expansion contributing to order growth")
            confidence.append("MEDIUM")
        elif yoy['merchants'] < -5 and yoy['orders'] < -5:
            insights.append("Merchant base contraction contributing to order decline")
            confidence.append("MEDIUM")
        
        # Causal Factor 5: WTU vs Orders Relationship
        if yoy['wtu'] > yoy['orders']:
            insights.append("WTU growth exceeding order growth - frequency decline")
            confidence.append("MEDIUM")
        elif yoy['wtu'] < yoy['orders']:
            insights.append("Order growth exceeding WTU growth - frequency increase")
            confidence.append("MEDIUM")
        
        # Causal Factor 6: Promo Expense Efficiency
        promo_expense_yoy = calculate_yoy_growth(this_week, last_year, 'daily_promo_expense')
        if promo_expense_yoy > 30 and yoy['orders'] < 10:
            insights.append("Promo expense up significantly but orders not responding - ROI issue")
            confidence.append("HIGH")
        
        if insights:
            causal_insights.append({
                'date': anomaly['date'],
                'day_of_week': anomaly['day_of_week'],
                'insights': insights,
                'confidence_levels': confidence,
                'key_metrics': {
                    'orders_yoy': yoy['orders'],
                    'gmv_yoy': yoy['gmv'],
                    'sessions_yoy': yoy['sessions'],
                    'basket_yoy': yoy['basket'],
                    'promo_pen_yoy': yoy['promo_penetration']
                }
            })
    
    return causal_insights

def generate_report():
    """Generate comprehensive analysis report"""
    this_week_data = [d for d in data if d['period'] == 'This Week']
    last_year_data = [d for d in data if d['period'] == 'Same Week Last Year']
    
    # Calculate weekly totals
    this_week_total = {
        'orders': sum(d['daily_completed_orders'] for d in this_week_data),
        'gmv': sum(d['daily_gmv'] for d in this_week_data),
        'wtu': sum(d['daily_wtu'] for d in this_week_data),
        'sessions': sum(d['daily_sessions'] for d in this_week_data)
    }
    
    last_year_total = {
        'orders': sum(d['daily_completed_orders'] for d in last_year_data),
        'gmv': sum(d['daily_gmv'] for d in last_year_data),
        'wtu': sum(d['daily_wtu'] for d in last_year_data),
        'sessions': sum(d['daily_sessions'] for d in last_year_data)
    }
    
    # Weekly YoY
    weekly_orders_yoy = ((this_week_total['orders'] - last_year_total['orders']) / last_year_total['orders']) * 100
    weekly_gmv_yoy = ((this_week_total['gmv'] - last_year_total['gmv']) / last_year_total['gmv']) * 100
    
    print("=" * 100)
    print("PENANG DAILY GMV & ORDERS TREND ANALYSIS")
    print("Last Completed Week vs Same Week Last Year")
    print("=" * 100)
    print()
    
    print("WEEKLY SUMMARY")
    print("-" * 100)
    print(f"This Week (Nov 10-16, 2025):")
    print(f"  Orders: {format_number(this_week_total['orders'])} | GMV: {format_number(this_week_total['gmv'])}")
    print(f"  WTU: {format_number(this_week_total['wtu'])} | Sessions: {format_number(this_week_total['sessions'])}")
    print()
    print(f"Same Week Last Year (Nov 10-16, 2024):")
    print(f"  Orders: {format_number(last_year_total['orders'])} | GMV: {format_number(last_year_total['gmv'])}")
    print(f"  WTU: {format_number(last_year_total['wtu'])} | Sessions: {format_number(last_year_total['sessions'])}")
    print()
    print(f"Weekly YoY Growth:")
    print(f"  Orders: {weekly_orders_yoy:+.1f}% | GMV: {weekly_gmv_yoy:+.1f}%")
    print()
    
    print("=" * 100)
    print("DAILY BREAKDOWN")
    print("=" * 100)
    print()
    
    # Day-by-day comparison
    for i, this_row in enumerate(this_week_data):
        last_row = last_year_data[i] if i < len(last_year_data) else None
        if not last_row:
            continue
        
        date_obj = datetime.strptime(str(this_row['date_id']), '%Y%m%d')
        orders_yoy = calculate_yoy_growth(this_row, last_row, 'daily_completed_orders')
        gmv_yoy = calculate_yoy_growth(this_row, last_row, 'daily_gmv')
        basket_yoy = calculate_yoy_growth(this_row, last_row, 'avg_basket_size')
        sessions_yoy = calculate_yoy_growth(this_row, last_row, 'daily_sessions')
        
        print(f"{date_obj.strftime('%A, %b %d')} ({format_date(this_row['date_id'])})")
        print(f"  This Week: Orders={format_number(this_row['daily_completed_orders'])}, GMV={format_number(this_row['daily_gmv'])}, Basket={this_row['avg_basket_size']:.2f}")
        print(f"  Last Year: Orders={format_number(last_row['daily_completed_orders'])}, GMV={format_number(last_row['daily_gmv'])}, Basket={last_row['avg_basket_size']:.2f}")
        print(f"  YoY: Orders={orders_yoy:+.1f}%, GMV={gmv_yoy:+.1f}%, Basket={basket_yoy:+.1f}%, Sessions={sessions_yoy:+.1f}%")
        print(f"  Promo Pen: {this_row['promo_penetration_pct']:.1f}% (vs {last_row['promo_penetration_pct']:.1f}% last year, {this_row['promo_penetration_pct'] - last_row['promo_penetration_pct']:+.1f}pp)")
        print()
    
    # Identify anomalies
    print("=" * 100)
    print("ANOMALY DETECTION")
    print("=" * 100)
    print()
    
    anomalies = identify_anomalies(this_week_data, last_year_data)
    
    if anomalies:
        print(f"Found {len(anomalies)} day(s) with significant anomalies:")
        print()
        for anomaly in anomalies:
            print(f"[ANOMALY] {anomaly['date']} ({anomaly['day_of_week']})")
            for reason in anomaly['reasons']:
                print(f"   - {reason}")
            print()
    else:
        print("No significant anomalies detected. Performance is within expected ranges.")
        print()
    
    # Causal inference analysis
    print("=" * 100)
    print("CAUSAL INFERENCE ANALYSIS")
    print("=" * 100)
    print()
    
    causal_insights = causal_inference_analysis(anomalies if anomalies else [])
    
    # Calculate averages for overall analysis (used in recommendations)
    avg_orders_yoy = sum(calculate_yoy_growth(tw, ly, 'daily_completed_orders') 
                        for tw, ly in zip(this_week_data, last_year_data)) / len(this_week_data)
    avg_gmv_yoy = sum(calculate_yoy_growth(tw, ly, 'daily_gmv') 
                     for tw, ly in zip(this_week_data, last_year_data)) / len(this_week_data)
    avg_basket_yoy = sum(calculate_yoy_growth(tw, ly, 'avg_basket_size') 
                        for tw, ly in zip(this_week_data, last_year_data)) / len(this_week_data)
    avg_sessions_yoy = sum(calculate_yoy_growth(tw, ly, 'daily_sessions') 
                          for tw, ly in zip(this_week_data, last_year_data)) / len(this_week_data)
    avg_promo_pen_diff = sum(tw['promo_penetration_pct'] - ly['promo_penetration_pct'] 
                             for tw, ly in zip(this_week_data, last_year_data)) / len(this_week_data)
    
    if causal_insights:
        for insight in causal_insights:
            print(f"[ANALYSIS] {insight['date']} ({insight['day_of_week']})")
            print(f"   Key Metrics: Orders {insight['key_metrics']['orders_yoy']:+.1f}% YoY, GMV {insight['key_metrics']['gmv_yoy']:+.1f}% YoY")
            print(f"   Sessions: {insight['key_metrics']['sessions_yoy']:+.1f}% YoY, Basket: {insight['key_metrics']['basket_yoy']:+.1f}% YoY")
            print()
            print("   Root Cause Analysis:")
            for i, (ins, conf) in enumerate(zip(insight['insights'], insight['confidence_levels'])):
                print(f"   {i+1}. [{conf}] {ins}")
            print()
    else:
        # Overall causal analysis
        print("OVERALL ROOT CAUSE ANALYSIS:")
        print()
        
        print(f"Average Weekly Performance:")
        print(f"  Orders: {avg_orders_yoy:+.1f}% YoY | GMV: {avg_gmv_yoy:+.1f}% YoY")
        print(f"  Basket: {avg_basket_yoy:+.1f}% YoY | Sessions: {avg_sessions_yoy:+.1f}% YoY")
        print(f"  Promo Penetration: {avg_promo_pen_diff:+.1f}pp vs last year")
        print()
        
        print("Key Insights:")
        if avg_orders_yoy > 10 and avg_gmv_yoy > 10:
            print("  [STRONG GROWTH] Driven by:")
            if avg_sessions_yoy > 5:
                print("     - Session growth (traffic acquisition working)")
            if avg_basket_yoy > 5:
                print("     - Basket expansion (upselling/price increases)")
            if avg_promo_pen_diff > 5:
                print("     - Higher promo penetration (promotional activity)")
        elif avg_orders_yoy < -5:
            print("  [VOLUME DECLINE] Driven by:")
            if avg_sessions_yoy < -5:
                print("     - Session decline (traffic acquisition issue)")
            if avg_basket_yoy < -5:
                print("     - Basket compression (price sensitivity)")
            if avg_promo_pen_diff < -5:
                print("     - Lower promo penetration (promo pullback)")
        print()
    
    print("=" * 100)
    print("RECOMMENDATIONS")
    print("=" * 100)
    print()
    
    # Generate recommendations based on analysis
    recommendations = []
    
    if weekly_orders_yoy > 15:
        recommendations.append("[ACTION] Maintain current promo intensity - strong growth trajectory")
    elif weekly_orders_yoy < -10:
        recommendations.append("[URGENT] Review promo calendar and campaign effectiveness")
    
    if avg_sessions_yoy < -10:
        recommendations.append("[ACTION] Focus on traffic acquisition - sessions declining")
    elif avg_sessions_yoy > 10:
        recommendations.append("[ACTION] Traffic acquisition strong - optimize conversion (COPS)")
    
    if avg_basket_yoy < -5:
        recommendations.append("[ACTION] Review pricing strategy - basket compression detected")
    elif avg_basket_yoy > 10:
        recommendations.append("[ACTION] Basket expansion working - continue upselling initiatives")
    
    if avg_promo_pen_diff > 10:
        recommendations.append("[ACTION] Monitor promo ROI - high penetration may impact margins")
    
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec}")
    else:
        print("Performance is stable. Continue monitoring key metrics.")
    
    print()

if __name__ == '__main__':
    generate_report()

