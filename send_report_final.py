"""Send weekly report - minimal version"""
import sys
import os
import json
import requests

# Import processing functions only (avoid encoding wrapper)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import without triggering encoding wrapper
import importlib.util
spec = importlib.util.spec_from_file_location("process_module", "process_and_send_weekly_report.py")
process_module = importlib.util.module_from_spec(spec)

# Load module without executing main block
with open("process_and_send_weekly_report.py", "r", encoding="utf-8") as f:
    code = f.read()
    # Remove the encoding wrapper code
    code = code.replace("sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')", "# Encoding wrapper removed")
    exec(compile(code, "process_and_send_weekly_report.py", "exec"), process_module.__dict__)

# Get functions
process_oc_results = process_module.process_oc_results
process_top_cities_results = process_module.process_top_cities_results
format_slack_message = process_module.format_slack_message
SLACK_WEBHOOK_URL = process_module.SLACK_WEBHOOK_URL

# Live data from MCP queries
oc_data = [{
    'this_week_orders': 1017714, 'same_week_last_month_orders': 1755791, 'ytd_avg_orders': 1497200,
    'this_week_completed_orders': 933565, 'same_week_last_month_completed_orders': 1607522, 'ytd_avg_completed_orders': 1395649,
    'this_week_completion_rate': 91.7, 'same_week_last_month_completion_rate': 91.6, 'ytd_avg_completion_rate': 93.2,
    'this_week_eaters': 547033, 'same_week_last_month_eaters': 801929, 'ytd_avg_eaters': 707469,
    'this_week_gmv': 33248998.11, 'same_week_last_month_gmv': 59976831.3, 'ytd_avg_gmv': 48996304.36,
    'this_week_basket': 31.47, 'same_week_last_month_basket': 32.95, 'ytd_avg_basket': 30.79,
    'this_week_promo_expense': 3100064.85, 'same_week_last_month_promo_expense': 5499394.48, 'ytd_avg_promo_expense': 3859246.53,
    'this_week_promo_orders': 474177, 'same_week_last_month_promo_orders': 831505, 'ytd_avg_promo_orders': 644186,
    'this_week_promo_penetration': 46.6, 'same_week_last_month_promo_penetration': 47.4, 'ytd_avg_promo_penetration': 43.0,
    'this_week_sessions': 911901, 'same_week_last_month_sessions': 1555288, 'ytd_avg_sessions': 1349107,
    'this_week_completed_sessions': 887512, 'same_week_last_month_completed_sessions': 1520034, 'ytd_avg_completed_sessions': 1327727,
    'this_week_orders_per_session': 1.1, 'same_week_last_month_orders_per_session': 1.1, 'ytd_avg_orders_per_session': 1.1,
    'this_week_cops': 1.1, 'same_week_last_month_cops': 1.1, 'ytd_avg_cops': 1.1,
    'this_week_new_pax': 0, 'same_week_last_month_new_pax': 0, 'ytd_avg_new_pax': 0
}]

top_cities_data = [
    {'city_name': 'Johor Bahru', 'city_id': 2, 'this_week_orders': 257234, 'same_week_last_month_orders': 435599, 'ytd_avg_orders': 360596, 'this_week_completed_orders': 236184, 'same_week_last_month_completed_orders': 398192, 'ytd_avg_completed_orders': 336013, 'this_week_completion_rate': 91.8, 'same_week_last_month_completion_rate': 91.4, 'ytd_avg_completion_rate': 93.2, 'this_week_eaters': 134153, 'same_week_last_month_eaters': 194467, 'ytd_avg_eaters': 168739, 'this_week_gmv': 8708962.16, 'same_week_last_month_gmv': 15504095.56, 'ytd_avg_gmv': 12390829.88, 'this_week_basket': 32.66, 'same_week_last_month_basket': 34.45, 'ytd_avg_basket': 32.37, 'this_week_promo_expense': 727569.11, 'same_week_last_month_promo_expense': 1266319.47, 'ytd_avg_promo_expense': 836921.97, 'this_week_promo_orders': 117465, 'same_week_last_month_promo_orders': 198465, 'ytd_avg_promo_orders': 145898, 'this_week_promo_penetration': 45.7, 'same_week_last_month_promo_penetration': 45.6, 'ytd_avg_promo_penetration': 40.5, 'this_week_sessions': 229630, 'same_week_last_month_sessions': 384011, 'ytd_avg_sessions': 324358, 'this_week_completed_sessions': 224079, 'same_week_last_month_completed_sessions': 376185, 'ytd_avg_completed_sessions': 319552, 'this_week_orders_per_session': 1.1, 'same_week_last_month_orders_per_session': 1.1, 'ytd_avg_orders_per_session': 1.1, 'this_week_cops': 1.1, 'same_week_last_month_cops': 1.1, 'ytd_avg_cops': 1.1, 'this_week_new_pax': 0, 'same_week_last_month_new_pax': 0, 'ytd_avg_new_pax': 0},
    {'city_name': 'Penang', 'city_id': 13, 'this_week_orders': 161349, 'same_week_last_month_orders': 288415, 'ytd_avg_orders': 238104, 'this_week_completed_orders': 148298, 'same_week_last_month_completed_orders': 266563, 'ytd_avg_completed_orders': 224239, 'this_week_completion_rate': 91.9, 'same_week_last_month_completion_rate': 92.4, 'ytd_avg_completion_rate': 94.2, 'this_week_eaters': 86992, 'same_week_last_month_eaters': 132412, 'ytd_avg_eaters': 112614, 'this_week_gmv': 5524512.83, 'same_week_last_month_gmv': 10312838.74, 'ytd_avg_gmv': 8073138.57, 'this_week_basket': 33.03, 'same_week_last_month_basket': 34.30, 'ytd_avg_basket': 31.80, 'this_week_promo_expense': 638432.84, 'same_week_last_month_promo_expense': 1158916.33, 'ytd_avg_promo_expense': 776986.56, 'this_week_promo_orders': 88077, 'same_week_last_month_promo_orders': 156331, 'ytd_avg_promo_orders': 116401, 'this_week_promo_penetration': 54.6, 'same_week_last_month_promo_penetration': 54.2, 'ytd_avg_promo_penetration': 48.9, 'this_week_sessions': 144992, 'same_week_last_month_sessions': 256739, 'ytd_avg_sessions': 215347, 'this_week_completed_sessions': 141034, 'same_week_last_month_completed_sessions': 252110, 'ytd_avg_completed_sessions': 213085, 'this_week_orders_per_session': 1.1, 'same_week_last_month_orders_per_session': 1.1, 'ytd_avg_orders_per_session': 1.1, 'this_week_cops': 1.1, 'same_week_last_month_cops': 1.1, 'ytd_avg_cops': 1.1, 'this_week_new_pax': 0, 'same_week_last_month_new_pax': 0, 'ytd_avg_new_pax': 0},
    {'city_name': 'Kota Kinabalu', 'city_id': 19, 'this_week_orders': 83381, 'same_week_last_month_orders': 140120, 'ytd_avg_orders': 125733, 'this_week_completed_orders': 76284, 'same_week_last_month_completed_orders': 127741, 'ytd_avg_completed_orders': 117012, 'this_week_completion_rate': 91.5, 'same_week_last_month_completion_rate': 91.2, 'ytd_avg_completion_rate': 93.1, 'this_week_eaters': 43920, 'same_week_last_month_eaters': 62131, 'ytd_avg_eaters': 56975, 'this_week_gmv': 2901106.95, 'same_week_last_month_gmv': 5167379.41, 'ytd_avg_gmv': 4388214.96, 'this_week_basket': 33.73, 'same_week_last_month_basket': 35.82, 'ytd_avg_basket': 32.90, 'this_week_promo_expense': 302562.78, 'same_week_last_month_promo_expense': 532679.63, 'ytd_avg_promo_expense': 394988.25, 'this_week_promo_orders': 44820, 'same_week_last_month_promo_orders': 79413, 'ytd_avg_promo_orders': 62688, 'this_week_promo_penetration': 53.8, 'same_week_last_month_promo_penetration': 56.7, 'ytd_avg_promo_penetration': 49.9, 'this_week_sessions': 74459, 'same_week_last_month_sessions': 123163, 'ytd_avg_sessions': 112900, 'this_week_completed_sessions': 72438, 'same_week_last_month_completed_sessions': 120303, 'ytd_avg_completed_sessions': 111134, 'this_week_orders_per_session': 1.1, 'same_week_last_month_orders_per_session': 1.1, 'ytd_avg_orders_per_session': 1.1, 'this_week_cops': 1.1, 'same_week_last_month_cops': 1.1, 'ytd_avg_cops': 1.1, 'this_week_new_pax': 0, 'same_week_last_month_new_pax': 0, 'ytd_avg_new_pax': 0},
    {'city_name': 'Ipoh', 'city_id': 48, 'this_week_orders': 92829, 'same_week_last_month_orders': 168442, 'ytd_avg_orders': 142044, 'this_week_completed_orders': 85648, 'same_week_last_month_completed_orders': 153561, 'ytd_avg_completed_orders': 132585, 'this_week_completion_rate': 92.3, 'same_week_last_month_completion_rate': 91.2, 'ytd_avg_completion_rate': 93.3, 'this_week_eaters': 50896, 'same_week_last_month_eaters': 77411, 'ytd_avg_eaters': 68735, 'this_week_gmv': 2833265.39, 'same_week_last_month_gmv': 5257193.18, 'ytd_avg_gmv': 4344479.57, 'this_week_basket': 29.09, 'same_week_last_month_basket': 30.06, 'ytd_avg_basket': 28.53, 'this_week_promo_expense': 272498.39, 'same_week_last_month_promo_expense': 502038.95, 'ytd_avg_promo_expense': 365719.45, 'this_week_promo_orders': 41124, 'same_week_last_month_promo_orders': 75800, 'ytd_avg_promo_orders': 59381, 'this_week_promo_penetration': 44.3, 'same_week_last_month_promo_penetration': 45.0, 'ytd_avg_promo_penetration': 41.8, 'this_week_sessions': 83615, 'same_week_last_month_sessions': 150132, 'ytd_avg_sessions': 128663, 'this_week_completed_sessions': 81613, 'same_week_last_month_completed_sessions': 145864, 'ytd_avg_completed_sessions': 126544, 'this_week_orders_per_session': 1.1, 'same_week_last_month_orders_per_session': 1.1, 'ytd_avg_orders_per_session': 1.1, 'this_week_cops': 1.0, 'same_week_last_month_cops': 1.1, 'ytd_avg_cops': 1.0, 'this_week_new_pax': 0, 'same_week_last_month_new_pax': 0, 'ytd_avg_new_pax': 0},
    {'city_name': 'Kuching', 'city_id': 11, 'this_week_orders': 74921, 'same_week_last_month_orders': 125611, 'ytd_avg_orders': 118222, 'this_week_completed_orders': 68714, 'same_week_last_month_completed_orders': 115898, 'ytd_avg_completed_orders': 110511, 'this_week_completion_rate': 91.7, 'same_week_last_month_completion_rate': 92.3, 'ytd_avg_completion_rate': 93.5, 'this_week_eaters': 40253, 'same_week_last_month_eaters': 56398, 'ytd_avg_eaters': 54361, 'this_week_gmv': 2566605.16, 'same_week_last_month_gmv': 4503806.85, 'ytd_avg_gmv': 4043497.97, 'this_week_basket': 32.89, 'same_week_last_month_basket': 34.24, 'ytd_avg_basket': 32.01, 'this_week_promo_expense': 273695.12, 'same_week_last_month_promo_expense': 484455.75, 'ytd_avg_promo_expense': 392827.32, 'this_week_promo_orders': 40191, 'same_week_last_month_promo_orders': 71318, 'ytd_avg_promo_orders': 60326, 'this_week_promo_penetration': 53.6, 'same_week_last_month_promo_penetration': 56.8, 'ytd_avg_promo_penetration': 51.0, 'this_week_sessions': 66968, 'same_week_last_month_sessions': 110801, 'ytd_avg_sessions': 105416, 'this_week_completed_sessions': 64993, 'same_week_last_month_completed_sessions': 108741, 'ytd_avg_completed_sessions': 103979, 'this_week_orders_per_session': 1.1, 'same_week_last_month_orders_per_session': 1.1, 'ytd_avg_orders_per_session': 1.1, 'this_week_cops': 1.1, 'same_week_last_month_cops': 1.1, 'ytd_avg_cops': 1.1, 'this_week_new_pax': 0, 'same_week_last_month_new_pax': 0, 'ytd_avg_new_pax': 0}
]

if __name__ == '__main__':
    try:
        # Process results
        oc_report = process_oc_results(oc_data)
        top_cities = process_top_cities_results(top_cities_data)
        
        # Format message
        slack_message = format_slack_message(oc_report, top_cities, None)
        
        # Send directly to Slack
        payload = {
            "blocks": slack_message.get("blocks", []),
            "username": slack_message.get("username", "Weekly Report Bot")
        }
        
        response = requests.post(SLACK_WEBHOOK_URL, json=payload, headers={'Content-Type': 'application/json'}, timeout=10)
        
        if response.status_code == 200 and response.text.strip() == "ok":
            sys.stdout.write("SUCCESS: Weekly report sent to Slack!\n")
        else:
            sys.stdout.write(f"Response: {response.status_code} - {response.text[:100]}\n")
    except Exception as e:
        sys.stdout.write(f"ERROR: {str(e)}\n")
        import traceback
        traceback.print_exc()


