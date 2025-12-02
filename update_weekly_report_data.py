"""
Update hardcoded data in process_and_send_weekly_report.py with fresh MCP query results
This script executes queries via MCP and updates the hardcoded data
"""

import os
import sys
import re
from datetime import datetime

# Import query generation
from generate_weekly_queries_with_new_pax import (
    get_week_dates,
    generate_oc_query_with_new_pax,
    generate_top_cities_query_with_new_pax
)

def execute_query_via_mcp(query):
    """Execute query via MCP - this will be called from Cursor chat context"""
    # This function will be called by the AI in Cursor chat
    # The actual execution happens via mcp_mcp-grab-data_run_presto_query
    pass

def update_hardcoded_data(oc_results, top_cities_results):
    """Update hardcoded data in process_and_send_weekly_report.py"""
    script_path = 'process_and_send_weekly_report.py'
    
    if not os.path.exists(script_path):
        print(f"Error: {script_path} not found")
        return False
    
    # Read the script
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse OC results
    if oc_results and len(oc_results) > 0:
        oc_row = oc_results[0] if isinstance(oc_results[0], dict) else dict(oc_results[0])
        
        # Update OC data section
        oc_data_pattern = r'(# Query results from MCP tools.*?oc_data = \[)(.*?)(\])'
        
        # Format new OC data
        today_str = datetime.now().strftime('%b %d, %Y')
        new_oc_data = f"""# Query results from MCP tools (Updated: {today_str} - LIVE DATA with updated COPS and Sessions)
oc_data = [{{
    'this_week_orders': {int(oc_row.get('this_week_orders', 0))},
    'same_week_last_month_orders': {int(oc_row.get('same_week_last_month_orders', 0))},
    'ytd_avg_orders': {int(oc_row.get('ytd_avg_orders', 0))},
    'this_week_completed_orders': {int(oc_row.get('this_week_completed_orders', 0))},
    'same_week_last_month_completed_orders': {int(oc_row.get('same_week_last_month_completed_orders', 0))},
    'ytd_avg_completed_orders': {int(oc_row.get('ytd_avg_completed_orders', 0))},
    'this_week_completion_rate': {round(oc_row.get('this_week_completion_rate', 0), 1)},
    'same_week_last_month_completion_rate': {round(oc_row.get('same_week_last_month_completion_rate', 0), 1)},
    'ytd_avg_completion_rate': {round(oc_row.get('ytd_avg_completion_rate', 0), 1)},
    'this_week_eaters': {int(oc_row.get('this_week_eaters', 0))},
    'same_week_last_month_eaters': {int(oc_row.get('same_week_last_month_eaters', 0))},
    'ytd_avg_eaters': {int(oc_row.get('ytd_avg_eaters', 0))},
    'this_week_gmv': {oc_row.get('this_week_gmv', 0)},
    'same_week_last_month_gmv': {oc_row.get('same_week_last_month_gmv', 0)},
    'ytd_avg_gmv': {oc_row.get('ytd_avg_gmv', 0)},
    'this_week_basket': {round(oc_row.get('this_week_basket', 0), 2)},
    'same_week_last_month_basket': {round(oc_row.get('same_week_last_month_basket', 0), 2)},
    'ytd_avg_basket': {round(oc_row.get('ytd_avg_basket', 0), 2)},
    'this_week_promo_expense': {oc_row.get('this_week_promo_expense', 0)},
    'same_week_last_month_promo_expense': {oc_row.get('same_week_last_month_promo_expense', 0)},
    'ytd_avg_promo_expense': {oc_row.get('ytd_avg_promo_expense', 0)},
    'this_week_promo_orders': {int(oc_row.get('this_week_promo_orders', 0))},
    'same_week_last_month_promo_orders': {int(oc_row.get('same_week_last_month_promo_orders', 0))},
    'ytd_avg_promo_orders': {int(oc_row.get('ytd_avg_promo_orders', 0))},
    'this_week_promo_penetration': {round(oc_row.get('this_week_promo_penetration', 0), 1)},
    'same_week_last_month_promo_penetration': {round(oc_row.get('same_week_last_month_promo_penetration', 0), 1)},
    'ytd_avg_promo_penetration': {round(oc_row.get('ytd_avg_promo_penetration', 0), 1)},
    'this_week_sessions': {oc_row.get('this_week_sessions', 0)},
    'same_week_last_month_sessions': {oc_row.get('same_week_last_month_sessions', 0)},
    'ytd_avg_sessions': {oc_row.get('ytd_avg_sessions', 0)},
    'this_week_completed_sessions': {oc_row.get('this_week_completed_sessions', 0)},
    'same_week_last_month_completed_sessions': {oc_row.get('same_week_last_month_completed_sessions', 0)},
    'ytd_avg_completed_sessions': {oc_row.get('ytd_avg_completed_sessions', 0)},
    'this_week_orders_per_session': {round(oc_row.get('this_week_orders_per_session', 0), 2)},
    'same_week_last_month_orders_per_session': {round(oc_row.get('same_week_last_month_orders_per_session', 0), 2)},
    'ytd_avg_orders_per_session': {round(oc_row.get('ytd_avg_orders_per_session', 0), 2)},
    'this_week_cops': {round(oc_row.get('this_week_cops', 0), 2)},
    'same_week_last_month_cops': {round(oc_row.get('same_week_last_month_cops', 0), 2)},
    'ytd_avg_cops': {round(oc_row.get('ytd_avg_cops', 0), 2)},
    'this_week_new_pax': {int(oc_row.get('this_week_new_pax', 0))},
    'same_week_last_month_new_pax': {int(oc_row.get('same_week_last_month_new_pax', 0))},
    'ytd_avg_new_pax': {int(oc_row.get('ytd_avg_new_pax', 0))},
    'current_month_mtm': {int(oc_row.get('current_month_mtm', 0))},
    'last_month_mtm': {int(oc_row.get('last_month_mtm', 0))},
    'same_month_last_year_mtm': {int(oc_row.get('same_month_last_year_mtm', 0))},
    'current_month_earning_per_mex': {round(oc_row.get('current_month_earning_per_mex', 0), 2)},
    'last_month_earning_per_mex': {round(oc_row.get('last_month_earning_per_mex', 0), 2)},
    'same_month_last_year_earning_per_mex': {round(oc_row.get('same_month_last_year_earning_per_mex', 0), 2)}
}}]"""
        
        # Replace OC data section
        content = re.sub(
            r'# Query results from MCP tools.*?oc_data = \[.*?\n\]',
            new_oc_data,
            content,
            flags=re.DOTALL
        )
    
    # Parse Top Cities results
    if top_cities_results and len(top_cities_results) > 0:
        # Format new top cities data
        today_str = datetime.now().strftime('%b %d, %Y')
        new_top_cities_data = f"# LIVE DATA from MCP queries (Updated: {today_str} - with updated Sessions and COPS from agg_food_cops_metrics)\ntop_cities_data = [\n"
        
        for city_row in top_cities_results:
            city_dict = city_row if isinstance(city_row, dict) else dict(city_row)
            city_data = f"    {{'city_name': '{city_dict.get('city_name', '')}', 'city_id': {city_dict.get('city_id', 0)}, "
            city_data += f"'this_week_orders': {int(city_dict.get('this_week_orders', 0))}, "
            city_data += f"'same_week_last_month_orders': {int(city_dict.get('same_week_last_month_orders', 0))}, "
            city_data += f"'ytd_avg_orders': {int(city_dict.get('ytd_avg_orders', 0))}, "
            city_data += f"'this_week_completed_orders': {int(city_dict.get('this_week_completed_orders', 0))}, "
            city_data += f"'same_week_last_month_completed_orders': {int(city_dict.get('same_week_last_month_completed_orders', 0))}, "
            city_data += f"'ytd_avg_completed_orders': {int(city_dict.get('ytd_avg_completed_orders', 0))}, "
            city_data += f"'this_week_completion_rate': {round(city_dict.get('this_week_completion_rate', 0), 1)}, "
            city_data += f"'same_week_last_month_completion_rate': {round(city_dict.get('same_week_last_month_completion_rate', 0), 1)}, "
            city_data += f"'ytd_avg_completion_rate': {round(city_dict.get('ytd_avg_completion_rate', 0), 1)}, "
            city_data += f"'this_week_eaters': {int(city_dict.get('this_week_eaters', 0))}, "
            city_data += f"'same_week_last_month_eaters': {int(city_dict.get('same_week_last_month_eaters', 0))}, "
            city_data += f"'ytd_avg_eaters': {int(city_dict.get('ytd_avg_eaters', 0))}, "
            city_data += f"'this_week_gmv': {city_dict.get('this_week_gmv', 0)}, "
            city_data += f"'same_week_last_month_gmv': {city_dict.get('same_week_last_month_gmv', 0)}, "
            city_data += f"'ytd_avg_gmv': {city_dict.get('ytd_avg_gmv', 0)}, "
            city_data += f"'this_week_basket': {round(city_dict.get('this_week_basket', 0), 2)}, "
            city_data += f"'same_week_last_month_basket': {round(city_dict.get('same_week_last_month_basket', 0), 2)}, "
            city_data += f"'ytd_avg_basket': {round(city_dict.get('ytd_avg_basket', 0), 2)}, "
            city_data += f"'this_week_promo_expense': {city_dict.get('this_week_promo_expense', 0)}, "
            city_data += f"'same_week_last_month_promo_expense': {city_dict.get('same_week_last_month_promo_expense', 0)}, "
            city_data += f"'ytd_avg_promo_expense': {city_dict.get('ytd_avg_promo_expense', 0)}, "
            city_data += f"'this_week_promo_orders': {int(city_dict.get('this_week_promo_orders', 0))}, "
            city_data += f"'same_week_last_month_promo_orders': {int(city_dict.get('same_week_last_month_promo_orders', 0))}, "
            city_data += f"'ytd_avg_promo_orders': {int(city_dict.get('ytd_avg_promo_orders', 0))}, "
            city_data += f"'this_week_promo_penetration': {round(city_dict.get('this_week_promo_penetration', 0), 1)}, "
            city_data += f"'same_week_last_month_promo_penetration': {round(city_dict.get('same_week_last_month_promo_penetration', 0), 1)}, "
            city_data += f"'ytd_avg_promo_penetration': {round(city_dict.get('ytd_avg_promo_penetration', 0), 1)}, "
            city_data += f"'this_week_sessions': {city_dict.get('this_week_sessions', 0)}, "
            city_data += f"'same_week_last_month_sessions': {city_dict.get('same_week_last_month_sessions', 0)}, "
            city_data += f"'ytd_avg_sessions': {city_dict.get('ytd_avg_sessions', 0)}, "
            city_data += f"'this_week_completed_sessions': {city_dict.get('this_week_completed_sessions', 0)}, "
            city_data += f"'same_week_last_month_completed_sessions': {city_dict.get('same_week_last_month_completed_sessions', 0)}, "
            city_data += f"'ytd_avg_completed_sessions': {city_dict.get('ytd_avg_completed_sessions', 0)}, "
            city_data += f"'this_week_orders_per_session': {round(city_dict.get('this_week_orders_per_session', 0), 2)}, "
            city_data += f"'same_week_last_month_orders_per_session': {round(city_dict.get('same_week_last_month_orders_per_session', 0), 2)}, "
            city_data += f"'ytd_avg_orders_per_session': {round(city_dict.get('ytd_avg_orders_per_session', 0), 2)}, "
            city_data += f"'this_week_cops': {round(city_dict.get('this_week_cops', 0), 2)}, "
            city_data += f"'same_week_last_month_cops': {round(city_dict.get('same_week_last_month_cops', 0), 2)}, "
            city_data += f"'ytd_avg_cops': {round(city_dict.get('ytd_avg_cops', 0), 2)}, "
            city_data += f"'this_week_new_pax': {int(city_dict.get('this_week_new_pax', 0))}, "
            city_data += f"'same_week_last_month_new_pax': {int(city_dict.get('same_week_last_month_new_pax', 0))}, "
            city_data += f"'ytd_avg_new_pax': {int(city_dict.get('ytd_avg_new_pax', 0))}, "
            city_data += f"'current_month_mtm': {int(city_dict.get('current_month_mtm', 0))}, "
            city_data += f"'last_month_mtm': {int(city_dict.get('last_month_mtm', 0))}, "
            city_data += f"'same_month_last_year_mtm': {int(city_dict.get('same_month_last_year_mtm', 0))}, "
            city_data += f"'current_month_earning_per_mex': {round(city_dict.get('current_month_earning_per_mex', 0), 2)}, "
            city_data += f"'last_month_earning_per_mex': {round(city_dict.get('last_month_earning_per_mex', 0), 2)}, "
            city_data += f"'same_month_last_year_earning_per_mex': {round(city_dict.get('same_month_last_year_earning_per_mex', 0), 2)}}},\n"
            new_top_cities_data += city_data
        
        new_top_cities_data = new_top_cities_data.rstrip(',\n') + '\n]'
        
        # Replace top cities data section
        content = re.sub(
            r'# LIVE DATA from MCP queries.*?top_cities_data = \[.*?\n\]',
            new_top_cities_data,
            content,
            flags=re.DOTALL
        )
    
    # Write updated content
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

if __name__ == '__main__':
    print("This script should be called from Cursor chat to execute queries via MCP")
    print("The AI will execute queries and call update_hardcoded_data() with results")


