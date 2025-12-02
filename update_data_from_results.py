"""
Update hardcoded data in process_and_send_weekly_report.py with fresh MCP query results
"""

import os
import re
from datetime import datetime

# OC Results (from MCP query)
oc_results = {
    'this_week_orders': 2143143,
    'same_week_last_month_orders': 2006985,
    'ytd_avg_orders': 1741855,
    'this_week_completed_orders': 1970686,
    'same_week_last_month_completed_orders': 1829394,
    'ytd_avg_completed_orders': 1603564,
    'this_week_completion_rate': 92.0,
    'same_week_last_month_completion_rate': 91.2,
    'ytd_avg_completion_rate': 92.1,
    'this_week_eaters': 912478,
    'same_week_last_month_eaters': 876240,
    'ytd_avg_eaters': 774889,
    'this_week_gmv': 79554439.48999992,
    'same_week_last_month_gmv': 69591129.33000003,
    'ytd_avg_gmv': 59015480.83000003,
    'this_week_basket': 36.092717287279605,
    'same_week_last_month_basket': 33.64699013443793,
    'ytd_avg_basket': 32.37656637963912,
    'this_week_promo_expense': 14437132.699999824,
    'same_week_last_month_promo_expense': 6968462.339999984,
    'ytd_avg_promo_expense': 7236659.040000007,
    'this_week_promo_orders': 1162458,
    'same_week_last_month_promo_orders': 974848,
    'ytd_avg_promo_orders': 823739,
    'this_week_promo_penetration': 54.2,
    'same_week_last_month_promo_penetration': 48.6,
    'ytd_avg_promo_penetration': 47.3,
    'this_week_sessions': 3956367.0,
    'same_week_last_month_sessions': 5041833.0,
    'ytd_avg_sessions': 4483382.0,
    'this_week_completed_sessions': 3956367.0,
    'same_week_last_month_completed_sessions': 5041833.0,
    'ytd_avg_completed_sessions': 4483382.0,
    'this_week_orders_per_session': 0.54,
    'same_week_last_month_orders_per_session': 0.4,
    'ytd_avg_orders_per_session': 0.39,
    'this_week_cops': 0.43,
    'same_week_last_month_cops': 0.36,
    'ytd_avg_cops': 0.36,
    'this_week_new_pax': 41953,
    'same_week_last_month_new_pax': 43238,
    'ytd_avg_new_pax': 39568,
    'current_month_mtm': 49167,
    'last_month_mtm': 49240,
    'same_month_last_year_mtm': 46537,
    'current_month_earning_per_mex': 20.01,
    'last_month_earning_per_mex': 19.84,
    'same_month_last_year_earning_per_mex': 18.86
}

# Top Cities Results (from MCP query)
top_cities_results = [
    {'city_name': 'Johor Bahru', 'city_id': 2, 'this_week_orders': 533519, 'same_week_last_month_orders': 500267, 'ytd_avg_orders': 411288, 'this_week_completed_orders': 491467, 'same_week_last_month_completed_orders': 457515, 'ytd_avg_completed_orders': 375949, 'this_week_completion_rate': 92.1, 'same_week_last_month_completion_rate': 91.5, 'ytd_avg_completion_rate': 91.4, 'this_week_eaters': 220947, 'same_week_last_month_eaters': 212355, 'ytd_avg_eaters': 181231, 'this_week_gmv': 20133326.589999992, 'same_week_last_month_gmv': 18031735.30999999, 'ytd_avg_gmv': 14367406.07, 'this_week_basket': 36.633533726577724, 'same_week_last_month_basket': 34.96391836333232, 'ytd_avg_basket': 33.57999590369972, 'this_week_promo_expense': 3138900.0600000056, 'same_week_last_month_promo_expense': 1597168.4400000002, 'ytd_avg_promo_expense': 1473501.1100000013, 'this_week_promo_orders': 277537, 'same_week_last_month_promo_orders': 231930, 'ytd_avg_promo_orders': 184041, 'this_week_promo_penetration': 52.0, 'same_week_last_month_promo_penetration': 46.4, 'ytd_avg_promo_penetration': 44.7, 'this_week_sessions': 885466.0, 'same_week_last_month_sessions': 1105837.0, 'ytd_avg_sessions': 1007169.0, 'this_week_completed_sessions': 885466.0, 'same_week_last_month_completed_sessions': 1105837.0, 'ytd_avg_completed_sessions': 1007169.0, 'this_week_orders_per_session': 0.6, 'same_week_last_month_orders_per_session': 0.45, 'ytd_avg_orders_per_session': 0.41, 'this_week_cops': 0.48, 'same_week_last_month_cops': 0.41, 'ytd_avg_cops': 0.37, 'this_week_new_pax': 12122, 'same_week_last_month_new_pax': 12450, 'ytd_avg_new_pax': 10685, 'current_month_mtm': 8798, 'last_month_mtm': 8740, 'same_month_last_year_mtm': 8201, 'current_month_earning_per_mex': 20.53, 'last_month_earning_per_mex': 20.35, 'same_month_last_year_earning_per_mex': 19.48},
    {'city_name': 'Penang', 'city_id': 13, 'this_week_orders': 365476, 'same_week_last_month_orders': 313420, 'ytd_avg_orders': 291244, 'this_week_completed_orders': 338369, 'same_week_last_month_completed_orders': 282788, 'ytd_avg_completed_orders': 269477, 'this_week_completion_rate': 92.6, 'same_week_last_month_completion_rate': 90.2, 'ytd_avg_completion_rate': 92.5, 'this_week_eaters': 154131, 'same_week_last_month_eaters': 138090, 'ytd_avg_eaters': 129426, 'this_week_gmv': 15025753.250000013, 'same_week_last_month_gmv': 11185895.490000004, 'ytd_avg_gmv': 10337045.920000004, 'this_week_basket': 39.988133073656314, 'same_week_last_month_basket': 34.980503345262235, 'ytd_avg_basket': 33.99348827543734, 'this_week_promo_expense': 3677533.3100000103, 'same_week_last_month_promo_expense': 1381011.0100000007, 'ytd_avg_promo_expense': 1591061.3800000031, 'this_week_promo_orders': 231437, 'same_week_last_month_promo_orders': 174065, 'ytd_avg_promo_orders': 156538, 'this_week_promo_penetration': 63.3, 'same_week_last_month_promo_penetration': 55.5, 'ytd_avg_promo_penetration': 53.7, 'this_week_sessions': 694190.0, 'same_week_last_month_sessions': 862720.0, 'ytd_avg_sessions': 772384.0, 'this_week_completed_sessions': 694190.0, 'same_week_last_month_completed_sessions': 862720.0, 'ytd_avg_completed_sessions': 772384.0, 'this_week_orders_per_session': 0.53, 'same_week_last_month_orders_per_session': 0.36, 'ytd_avg_orders_per_session': 0.38, 'this_week_cops': 0.42, 'same_week_last_month_cops': 0.33, 'ytd_avg_cops': 0.35, 'this_week_new_pax': 10335, 'same_week_last_month_new_pax': 9890, 'ytd_avg_new_pax': 9910, 'current_month_mtm': 6452, 'last_month_mtm': 6490, 'same_month_last_year_mtm': 6231, 'current_month_earning_per_mex': 21.06, 'last_month_earning_per_mex': 20.75, 'same_month_last_year_earning_per_mex': 19.52},
    {'city_name': 'Ipoh', 'city_id': 48, 'this_week_orders': 197189, 'same_week_last_month_orders': 178355, 'ytd_avg_orders': 169353, 'this_week_completed_orders': 180350, 'same_week_last_month_completed_orders': 160449, 'ytd_avg_completed_orders': 157454, 'this_week_completion_rate': 91.5, 'same_week_last_month_completion_rate': 90.0, 'ytd_avg_completion_rate': 93.0, 'this_week_eaters': 86022, 'same_week_last_month_eaters': 80718, 'ytd_avg_eaters': 77247, 'this_week_gmv': 6776338.470000007, 'same_week_last_month_gmv': 5765281.9799999995, 'ytd_avg_gmv': 5414627.820000002, 'this_week_basket': 33.483040310507405, 'same_week_last_month_basket': 31.613974471639015, 'ytd_avg_basket': 30.156568204046945, 'this_week_promo_expense': 1293763.8099999996, 'same_week_last_month_promo_expense': 589298.63, 'ytd_avg_promo_expense': 734798.7099999987, 'this_week_promo_orders': 103468, 'same_week_last_month_promo_orders': 81272, 'ytd_avg_promo_orders': 79389, 'this_week_promo_penetration': 52.5, 'same_week_last_month_promo_penetration': 45.6, 'ytd_avg_promo_penetration': 46.9, 'this_week_sessions': 386982.0, 'same_week_last_month_sessions': 498210.0, 'ytd_avg_sessions': 444221.0, 'this_week_completed_sessions': 386982.0, 'same_week_last_month_completed_sessions': 498210.0, 'ytd_avg_completed_sessions': 444221.0, 'this_week_orders_per_session': 0.51, 'same_week_last_month_orders_per_session': 0.36, 'ytd_avg_orders_per_session': 0.38, 'this_week_cops': 0.4, 'same_week_last_month_cops': 0.32, 'ytd_avg_cops': 0.35, 'this_week_new_pax': 5543, 'same_week_last_month_new_pax': 6087, 'ytd_avg_new_pax': 5645, 'current_month_mtm': 5122, 'last_month_mtm': 5131, 'same_month_last_year_mtm': 4430, 'current_month_earning_per_mex': 18.83, 'last_month_earning_per_mex': 18.68, 'same_month_last_year_earning_per_mex': 17.79},
    {'city_name': 'Kota Kinabalu', 'city_id': 19, 'this_week_orders': 172157, 'same_week_last_month_orders': 163123, 'ytd_avg_orders': 150160, 'this_week_completed_orders': 158046, 'same_week_last_month_completed_orders': 149110, 'ytd_avg_completed_orders': 139965, 'this_week_completion_rate': 91.8, 'same_week_last_month_completion_rate': 91.4, 'ytd_avg_completion_rate': 93.2, 'this_week_eaters': 70304, 'same_week_last_month_eaters': 67894, 'ytd_avg_eaters': 62859, 'this_week_gmv': 6618803.4499999955, 'same_week_last_month_gmv': 6026494.179999999, 'ytd_avg_gmv': 5333602.179999999, 'this_week_basket': 37.47939372081555, 'same_week_last_month_basket': 35.93482911944211, 'ytd_avg_basket': 33.82117986639524, 'this_week_promo_expense': 1144352.0199999989, 'same_week_last_month_promo_expense': 697342.4999999998, 'ytd_avg_promo_expense': 645753.4799999999, 'this_week_promo_orders': 101463, 'same_week_last_month_promo_orders': 95487, 'ytd_avg_promo_orders': 78316, 'this_week_promo_penetration': 58.9, 'same_week_last_month_promo_penetration': 58.5, 'ytd_avg_promo_penetration': 52.2, 'this_week_sessions': 293797.0, 'same_week_last_month_sessions': 364214.0, 'ytd_avg_sessions': 339864.0, 'this_week_completed_sessions': 293797.0, 'same_week_last_month_completed_sessions': 364214.0, 'ytd_avg_completed_sessions': 339864.0, 'this_week_orders_per_session': 0.59, 'same_week_last_month_orders_per_session': 0.45, 'ytd_avg_orders_per_session': 0.44, 'this_week_cops': 0.47, 'same_week_last_month_cops': 0.41, 'ytd_avg_cops': 0.41, 'this_week_new_pax': 4361, 'same_week_last_month_new_pax': 4531, 'ytd_avg_new_pax': 3692, 'current_month_mtm': 3066, 'last_month_mtm': 3119, 'same_month_last_year_mtm': 3101, 'current_month_earning_per_mex': 21.17, 'last_month_earning_per_mex': 21.19, 'same_month_last_year_earning_per_mex': 20.01},
    {'city_name': 'Kuching', 'city_id': 11, 'this_week_orders': 160214, 'same_week_last_month_orders': 145291, 'ytd_avg_orders': 139005, 'this_week_completed_orders': 148767, 'same_week_last_month_completed_orders': 134257, 'ytd_avg_completed_orders': 129735, 'this_week_completion_rate': 92.9, 'same_week_last_month_completion_rate': 92.4, 'ytd_avg_completion_rate': 93.3, 'this_week_eaters': 65855, 'same_week_last_month_eaters': 62081, 'ytd_avg_eaters': 59120, 'this_week_gmv': 6315235.209999999, 'same_week_last_month_gmv': 5238716.719999998, 'ytd_avg_gmv': 5037249.069999999, 'this_week_basket': 37.861762084333236, 'same_week_last_month_basket': 34.3884203430734, 'ytd_avg_basket': 34.19717277527271, 'this_week_promo_expense': 1333729.0299999989, 'same_week_last_month_promo_expense': 638023.8999999996, 'ytd_avg_promo_expense': 797985.3999999993, 'this_week_promo_orders': 99180, 'same_week_last_month_promo_orders': 84933, 'ytd_avg_promo_orders': 76692, 'this_week_promo_penetration': 61.9, 'same_week_last_month_promo_penetration': 58.5, 'ytd_avg_promo_penetration': 55.2, 'this_week_sessions': 292888.0, 'same_week_last_month_sessions': 361923.0, 'ytd_avg_sessions': 337259.0, 'this_week_completed_sessions': 292888.0, 'same_week_last_month_completed_sessions': 361923.0, 'ytd_avg_completed_sessions': 337259.0, 'this_week_orders_per_session': 0.55, 'same_week_last_month_orders_per_session': 0.4, 'ytd_avg_orders_per_session': 0.41, 'this_week_cops': 0.44, 'same_week_last_month_cops': 0.37, 'ytd_avg_cops': 0.38, 'this_week_new_pax': 2768, 'same_week_last_month_new_pax': 3042, 'ytd_avg_new_pax': 2534, 'current_month_mtm': 3492, 'last_month_mtm': 3529, 'same_month_last_year_mtm': 3882, 'current_month_earning_per_mex': 21.11, 'last_month_earning_per_mex': 20.91, 'same_month_last_year_earning_per_mex': 19.96}
]

def update_hardcoded_data():
    """Update hardcoded data in process_and_send_weekly_report.py"""
    script_path = 'process_and_send_weekly_report.py'
    
    if not os.path.exists(script_path):
        print(f"Error: {script_path} not found")
        return False
    
    # Read the script
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update OC data section
    today_str = datetime.now().strftime('%b %d, %Y')
    oc_row = oc_results
    
    new_oc_data = f"""# Query results from MCP tools (Updated: {today_str} - LIVE DATA with updated COPS and Sessions)
oc_data = [{{
    'this_week_orders': {int(oc_row['this_week_orders'])},
    'same_week_last_month_orders': {int(oc_row['same_week_last_month_orders'])},
    'ytd_avg_orders': {int(oc_row['ytd_avg_orders'])},
    'this_week_completed_orders': {int(oc_row['this_week_completed_orders'])},
    'same_week_last_month_completed_orders': {int(oc_row['same_week_last_month_completed_orders'])},
    'ytd_avg_completed_orders': {int(oc_row['ytd_avg_completed_orders'])},
    'this_week_completion_rate': {round(oc_row['this_week_completion_rate'], 1)},
    'same_week_last_month_completion_rate': {round(oc_row['same_week_last_month_completion_rate'], 1)},
    'ytd_avg_completion_rate': {round(oc_row['ytd_avg_completion_rate'], 1)},
    'this_week_eaters': {int(oc_row['this_week_eaters'])},
    'same_week_last_month_eaters': {int(oc_row['same_week_last_month_eaters'])},
    'ytd_avg_eaters': {int(oc_row['ytd_avg_eaters'])},
    'this_week_gmv': {oc_row['this_week_gmv']},
    'same_week_last_month_gmv': {oc_row['same_week_last_month_gmv']},
    'ytd_avg_gmv': {oc_row['ytd_avg_gmv']},
    'this_week_basket': {round(oc_row['this_week_basket'], 2)},
    'same_week_last_month_basket': {round(oc_row['same_week_last_month_basket'], 2)},
    'ytd_avg_basket': {round(oc_row['ytd_avg_basket'], 2)},
    'this_week_promo_expense': {oc_row['this_week_promo_expense']},
    'same_week_last_month_promo_expense': {oc_row['same_week_last_month_promo_expense']},
    'ytd_avg_promo_expense': {oc_row['ytd_avg_promo_expense']},
    'this_week_promo_orders': {int(oc_row['this_week_promo_orders'])},
    'same_week_last_month_promo_orders': {int(oc_row['same_week_last_month_promo_orders'])},
    'ytd_avg_promo_orders': {int(oc_row['ytd_avg_promo_orders'])},
    'this_week_promo_penetration': {round(oc_row['this_week_promo_penetration'], 1)},
    'same_week_last_month_promo_penetration': {round(oc_row['same_week_last_month_promo_penetration'], 1)},
    'ytd_avg_promo_penetration': {round(oc_row['ytd_avg_promo_penetration'], 1)},
    'this_week_sessions': {oc_row['this_week_sessions']},
    'same_week_last_month_sessions': {oc_row['same_week_last_month_sessions']},
    'ytd_avg_sessions': {oc_row['ytd_avg_sessions']},
    'this_week_completed_sessions': {oc_row['this_week_completed_sessions']},
    'same_week_last_month_completed_sessions': {oc_row['same_week_last_month_completed_sessions']},
    'ytd_avg_completed_sessions': {oc_row['ytd_avg_completed_sessions']},
    'this_week_orders_per_session': {round(oc_row['this_week_orders_per_session'], 2)},
    'same_week_last_month_orders_per_session': {round(oc_row['same_week_last_month_orders_per_session'], 2)},
    'ytd_avg_orders_per_session': {round(oc_row['ytd_avg_orders_per_session'], 2)},
    'this_week_cops': {round(oc_row['this_week_cops'], 2)},
    'same_week_last_month_cops': {round(oc_row['same_week_last_month_cops'], 2)},
    'ytd_avg_cops': {round(oc_row['ytd_avg_cops'], 2)},
    'this_week_new_pax': {int(oc_row['this_week_new_pax'])},
    'same_week_last_month_new_pax': {int(oc_row['same_week_last_month_new_pax'])},
    'ytd_avg_new_pax': {int(oc_row['ytd_avg_new_pax'])},
    'current_month_mtm': {int(oc_row['current_month_mtm'])},
    'last_month_mtm': {int(oc_row['last_month_mtm'])},
    'same_month_last_year_mtm': {int(oc_row['same_month_last_year_mtm'])},
    'current_month_earning_per_mex': {round(oc_row['current_month_earning_per_mex'], 2)},
    'last_month_earning_per_mex': {round(oc_row['last_month_earning_per_mex'], 2)},
    'same_month_last_year_earning_per_mex': {round(oc_row['same_month_last_year_earning_per_mex'], 2)}
}}]"""
    
    # Replace OC data section
    pattern = r'(# Query results from MCP tools.*?oc_data = \[)(.*?)(\])'
    content = re.sub(pattern, new_oc_data, content, flags=re.DOTALL)
    
    # Update Top Cities data section
    new_top_cities_data = f"# LIVE DATA from MCP queries (Updated: {today_str} - with updated Sessions and COPS from agg_food_cops_metrics)\ntop_cities_data = [\n"
    
    for city_dict in top_cities_results:
        city_name = city_dict['city_name'].replace("'", "\\'")
        city_data = f"    {{'city_name': '{city_name}', 'city_id': {city_dict['city_id']}, "
        city_data += f"'this_week_orders': {int(city_dict['this_week_orders'])}, "
        city_data += f"'same_week_last_month_orders': {int(city_dict['same_week_last_month_orders'])}, "
        city_data += f"'ytd_avg_orders': {int(city_dict['ytd_avg_orders'])}, "
        city_data += f"'this_week_completed_orders': {int(city_dict['this_week_completed_orders'])}, "
        city_data += f"'same_week_last_month_completed_orders': {int(city_dict['same_week_last_month_completed_orders'])}, "
        city_data += f"'ytd_avg_completed_orders': {int(city_dict['ytd_avg_completed_orders'])}, "
        city_data += f"'this_week_completion_rate': {round(city_dict['this_week_completion_rate'], 1)}, "
        city_data += f"'same_week_last_month_completion_rate': {round(city_dict['same_week_last_month_completion_rate'], 1)}, "
        city_data += f"'ytd_avg_completion_rate': {round(city_dict['ytd_avg_completion_rate'], 1)}, "
        city_data += f"'this_week_eaters': {int(city_dict['this_week_eaters'])}, "
        city_data += f"'same_week_last_month_eaters': {int(city_dict['same_week_last_month_eaters'])}, "
        city_data += f"'ytd_avg_eaters': {int(city_dict['ytd_avg_eaters'])}, "
        city_data += f"'this_week_gmv': {city_dict['this_week_gmv']}, "
        city_data += f"'same_week_last_month_gmv': {city_dict['same_week_last_month_gmv']}, "
        city_data += f"'ytd_avg_gmv': {city_dict['ytd_avg_gmv']}, "
        city_data += f"'this_week_basket': {round(city_dict['this_week_basket'], 2)}, "
        city_data += f"'same_week_last_month_basket': {round(city_dict['same_week_last_month_basket'], 2)}, "
        city_data += f"'ytd_avg_basket': {round(city_dict['ytd_avg_basket'], 2)}, "
        city_data += f"'this_week_promo_expense': {city_dict['this_week_promo_expense']}, "
        city_data += f"'same_week_last_month_promo_expense': {city_dict['same_week_last_month_promo_expense']}, "
        city_data += f"'ytd_avg_promo_expense': {city_dict['ytd_avg_promo_expense']}, "
        city_data += f"'this_week_promo_orders': {int(city_dict['this_week_promo_orders'])}, "
        city_data += f"'same_week_last_month_promo_orders': {int(city_dict['same_week_last_month_promo_orders'])}, "
        city_data += f"'ytd_avg_promo_orders': {int(city_dict['ytd_avg_promo_orders'])}, "
        city_data += f"'this_week_promo_penetration': {round(city_dict['this_week_promo_penetration'], 1)}, "
        city_data += f"'same_week_last_month_promo_penetration': {round(city_dict['same_week_last_month_promo_penetration'], 1)}, "
        city_data += f"'ytd_avg_promo_penetration': {round(city_dict['ytd_avg_promo_penetration'], 1)}, "
        city_data += f"'this_week_sessions': {city_dict['this_week_sessions']}, "
        city_data += f"'same_week_last_month_sessions': {city_dict['same_week_last_month_sessions']}, "
        city_data += f"'ytd_avg_sessions': {city_dict['ytd_avg_sessions']}, "
        city_data += f"'this_week_completed_sessions': {city_dict['this_week_completed_sessions']}, "
        city_data += f"'same_week_last_month_completed_sessions': {city_dict['same_week_last_month_completed_sessions']}, "
        city_data += f"'ytd_avg_completed_sessions': {city_dict['ytd_avg_completed_sessions']}, "
        city_data += f"'this_week_orders_per_session': {round(city_dict['this_week_orders_per_session'], 2)}, "
        city_data += f"'same_week_last_month_orders_per_session': {round(city_dict['same_week_last_month_orders_per_session'], 2)}, "
        city_data += f"'ytd_avg_orders_per_session': {round(city_dict['ytd_avg_orders_per_session'], 2)}, "
        city_data += f"'this_week_cops': {round(city_dict['this_week_cops'], 2)}, "
        city_data += f"'same_week_last_month_cops': {round(city_dict['same_week_last_month_cops'], 2)}, "
        city_data += f"'ytd_avg_cops': {round(city_dict['ytd_avg_cops'], 2)}, "
        city_data += f"'this_week_new_pax': {int(city_dict['this_week_new_pax'])}, "
        city_data += f"'same_week_last_month_new_pax': {int(city_dict['same_week_last_month_new_pax'])}, "
        city_data += f"'ytd_avg_new_pax': {int(city_dict['ytd_avg_new_pax'])}, "
        city_data += f"'current_month_mtm': {int(city_dict['current_month_mtm'])}, "
        city_data += f"'last_month_mtm': {int(city_dict['last_month_mtm'])}, "
        city_data += f"'same_month_last_year_mtm': {int(city_dict['same_month_last_year_mtm'])}, "
        city_data += f"'current_month_earning_per_mex': {round(city_dict['current_month_earning_per_mex'], 2)}, "
        city_data += f"'last_month_earning_per_mex': {round(city_dict['last_month_earning_per_mex'], 2)}, "
        city_data += f"'same_month_last_year_earning_per_mex': {round(city_dict['same_month_last_year_earning_per_mex'], 2)}}},\n"
        new_top_cities_data += city_data
    
    new_top_cities_data = new_top_cities_data.rstrip(',\n') + '\n]'
    
    # Replace top cities data section
    pattern = r'(# LIVE DATA from MCP queries.*?top_cities_data = \[)(.*?)(\])'
    content = re.sub(pattern, new_top_cities_data, content, flags=re.DOTALL)
    
    # Write updated content
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated hardcoded data in {script_path}")
    print(f"   OC data updated with {len(oc_results)} fields")
    print(f"   Top cities data updated with {len(top_cities_results)} cities")
    return True

if __name__ == '__main__':
    update_hardcoded_data()

