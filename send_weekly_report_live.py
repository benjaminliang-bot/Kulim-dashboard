"""Send weekly report with live MCP data"""
import requests
import json

# Import functions directly
import importlib.util
spec = importlib.util.spec_from_file_location("mod", "process_and_send_weekly_report.py")
mod = importlib.util.module_from_spec(spec)

# Read and execute module code
with open("process_and_send_weekly_report.py", "r", encoding="utf-8") as f:
    code = f.read()
    exec(code, mod.__dict__)

# Get functions
process_oc_results = mod.process_oc_results
process_top_cities_results = mod.process_top_cities_results
format_slack_message = mod.format_slack_message
SLACK_WEBHOOK_URL = mod.SLACK_WEBHOOK_URL

# LIVE DATA from MCP queries (Nov 6, 2025)
oc_data = [{
    'this_week_orders': 1041314, 'same_week_last_month_orders': 1755791, 'ytd_avg_orders': 1497200,
    'this_week_completed_orders': 950674, 'same_week_last_month_completed_orders': 1607522, 'ytd_avg_completed_orders': 1395649,
    'this_week_completion_rate': 91.3, 'same_week_last_month_completion_rate': 91.6, 'ytd_avg_completion_rate': 93.2,
    'this_week_eaters': 553317, 'same_week_last_month_eaters': 801929, 'ytd_avg_eaters': 707469,
    'this_week_gmv': 33881372.67, 'same_week_last_month_gmv': 59976831.3, 'ytd_avg_gmv': 48996304.36,
    'this_week_basket': 31.50, 'same_week_last_month_basket': 32.95, 'ytd_avg_basket': 30.79,
    'this_week_promo_expense': 3165570.82, 'same_week_last_month_promo_expense': 5499394.48, 'ytd_avg_promo_expense': 3859246.53,
    'this_week_promo_orders': 486347, 'same_week_last_month_promo_orders': 831505, 'ytd_avg_promo_orders': 644186,
    'this_week_promo_penetration': 46.7, 'same_week_last_month_promo_penetration': 47.4, 'ytd_avg_promo_penetration': 43.0,
    'this_week_sessions': 933323, 'same_week_last_month_sessions': 1555288, 'ytd_avg_sessions': 1349107,
    'this_week_completed_sessions': 903825, 'same_week_last_month_completed_sessions': 1520034, 'ytd_avg_completed_sessions': 1327727,
    'this_week_orders_per_session': 1.1, 'same_week_last_month_orders_per_session': 1.1, 'ytd_avg_orders_per_session': 1.1,
    'this_week_cops': 1.1, 'same_week_last_month_cops': 1.1, 'ytd_avg_cops': 1.1,
    'this_week_new_pax': 18903, 'same_week_last_month_new_pax': 40926, 'ytd_avg_new_pax': 33926
}]

top_cities_data = [
    {'city_name': 'Johor Bahru', 'city_id': 2, 'this_week_orders': 263017, 'same_week_last_month_orders': 435599, 'ytd_avg_orders': 360596, 'this_week_completed_orders': 240361, 'same_week_last_month_completed_orders': 398192, 'ytd_avg_completed_orders': 336013, 'this_week_completion_rate': 91.4, 'same_week_last_month_completion_rate': 91.4, 'ytd_avg_completion_rate': 93.2, 'this_week_eaters': 135579, 'same_week_last_month_eaters': 194467, 'ytd_avg_eaters': 168739, 'this_week_gmv': 8868208.29, 'same_week_last_month_gmv': 15504095.56, 'ytd_avg_gmv': 12390829.88, 'this_week_basket': 32.69, 'same_week_last_month_basket': 34.45, 'ytd_avg_basket': 32.37, 'this_week_promo_expense': 742453.16, 'same_week_last_month_promo_expense': 1266319.47, 'ytd_avg_promo_expense': 836921.97, 'this_week_promo_orders': 120380, 'same_week_last_month_promo_orders': 198465, 'ytd_avg_promo_orders': 145898, 'this_week_promo_penetration': 45.8, 'same_week_last_month_promo_penetration': 45.6, 'ytd_avg_promo_penetration': 40.5, 'this_week_sessions': 234898, 'same_week_last_month_sessions': 384011, 'ytd_avg_sessions': 324358, 'this_week_completed_sessions': 228059, 'same_week_last_month_completed_sessions': 376185, 'ytd_avg_completed_sessions': 319552, 'this_week_orders_per_session': 1.1, 'same_week_last_month_orders_per_session': 1.1, 'ytd_avg_orders_per_session': 1.1, 'this_week_cops': 1.1, 'same_week_last_month_cops': 1.1, 'ytd_avg_cops': 1.1, 'this_week_new_pax': 5201, 'same_week_last_month_new_pax': 11152, 'ytd_avg_new_pax': 9503},
    {'city_name': 'Penang', 'city_id': 13, 'this_week_orders': 165415, 'same_week_last_month_orders': 288415, 'ytd_avg_orders': 238104, 'this_week_completed_orders': 150881, 'same_week_last_month_completed_orders': 266563, 'ytd_avg_completed_orders': 224239, 'this_week_completion_rate': 91.2, 'same_week_last_month_completion_rate': 92.4, 'ytd_avg_completion_rate': 94.2, 'this_week_eaters': 87931, 'same_week_last_month_eaters': 132412, 'ytd_avg_eaters': 112614, 'this_week_gmv': 5629266.48, 'same_week_last_month_gmv': 10312838.74, 'ytd_avg_gmv': 8073138.57, 'this_week_basket': 33.09, 'same_week_last_month_basket': 34.30, 'ytd_avg_basket': 31.80, 'this_week_promo_expense': 652093.89, 'same_week_last_month_promo_expense': 1158916.33, 'ytd_avg_promo_expense': 776986.56, 'this_week_promo_orders': 90565, 'same_week_last_month_promo_orders': 156331, 'ytd_avg_promo_orders': 116401, 'this_week_promo_penetration': 54.8, 'same_week_last_month_promo_penetration': 54.2, 'ytd_avg_promo_penetration': 48.9, 'this_week_sessions': 148710, 'same_week_last_month_sessions': 256739, 'ytd_avg_sessions': 215347, 'this_week_completed_sessions': 143524, 'same_week_last_month_completed_sessions': 252110, 'ytd_avg_completed_sessions': 213085, 'this_week_orders_per_session': 1.1, 'same_week_last_month_orders_per_session': 1.1, 'ytd_avg_orders_per_session': 1.1, 'this_week_cops': 1.1, 'same_week_last_month_cops': 1.1, 'ytd_avg_cops': 1.1, 'this_week_new_pax': 4161, 'same_week_last_month_new_pax': 9780, 'ytd_avg_new_pax': 7722},
    {'city_name': 'Kota Kinabalu', 'city_id': 19, 'this_week_orders': 85782, 'same_week_last_month_orders': 140120, 'ytd_avg_orders': 125733, 'this_week_completed_orders': 77940, 'same_week_last_month_completed_orders': 127741, 'ytd_avg_completed_orders': 117012, 'this_week_completion_rate': 90.9, 'same_week_last_month_completion_rate': 91.2, 'ytd_avg_completion_rate': 93.1, 'this_week_eaters': 44484, 'same_week_last_month_eaters': 62131, 'ytd_avg_eaters': 56975, 'this_week_gmv': 2963263.89, 'same_week_last_month_gmv': 5167379.41, 'ytd_avg_gmv': 4388214.96, 'this_week_basket': 33.73, 'same_week_last_month_basket': 35.82, 'ytd_avg_basket': 32.90, 'this_week_promo_expense': 309371.97, 'same_week_last_month_promo_expense': 532679.63, 'ytd_avg_promo_expense': 394988.25, 'this_week_promo_orders': 46144, 'same_week_last_month_promo_orders': 79413, 'ytd_avg_promo_orders': 62688, 'this_week_promo_penetration': 53.8, 'same_week_last_month_promo_penetration': 56.7, 'ytd_avg_promo_penetration': 49.9, 'this_week_sessions': 76615, 'same_week_last_month_sessions': 123163, 'ytd_avg_sessions': 112900, 'this_week_completed_sessions': 74012, 'same_week_last_month_completed_sessions': 120303, 'ytd_avg_completed_sessions': 111134, 'this_week_orders_per_session': 1.1, 'same_week_last_month_orders_per_session': 1.1, 'ytd_avg_orders_per_session': 1.1, 'this_week_cops': 1.1, 'same_week_last_month_cops': 1.1, 'ytd_avg_cops': 1.1, 'this_week_new_pax': 2121, 'same_week_last_month_new_pax': 5879, 'ytd_avg_new_pax': 3153},
    {'city_name': 'Ipoh', 'city_id': 48, 'this_week_orders': 94593, 'same_week_last_month_orders': 168442, 'ytd_avg_orders': 142044, 'this_week_completed_orders': 87044, 'same_week_last_month_completed_orders': 153561, 'ytd_avg_completed_orders': 132585, 'this_week_completion_rate': 92.0, 'same_week_last_month_completion_rate': 91.2, 'ytd_avg_completion_rate': 93.3, 'this_week_eaters': 51501, 'same_week_last_month_eaters': 77411, 'ytd_avg_eaters': 68735, 'this_week_gmv': 2881809.71, 'same_week_last_month_gmv': 5257193.18, 'ytd_avg_gmv': 4344479.57, 'this_week_basket': 29.12, 'same_week_last_month_basket': 30.06, 'ytd_avg_basket': 28.53, 'this_week_promo_expense': 277435.68, 'same_week_last_month_promo_expense': 502038.95, 'ytd_avg_promo_expense': 365719.45, 'this_week_promo_orders': 42001, 'same_week_last_month_promo_orders': 75800, 'ytd_avg_promo_orders': 59381, 'this_week_promo_penetration': 44.4, 'same_week_last_month_promo_penetration': 45.0, 'ytd_avg_promo_penetration': 41.8, 'this_week_sessions': 85190, 'same_week_last_month_sessions': 150132, 'ytd_avg_sessions': 128663, 'this_week_completed_sessions': 82930, 'same_week_last_month_completed_sessions': 145864, 'ytd_avg_completed_sessions': 126544, 'this_week_orders_per_session': 1.1, 'same_week_last_month_orders_per_session': 1.1, 'ytd_avg_orders_per_session': 1.1, 'this_week_cops': 1.0, 'same_week_last_month_cops': 1.1, 'ytd_avg_cops': 1.0, 'this_week_new_pax': 2443, 'same_week_last_month_new_pax': 5015, 'ytd_avg_new_pax': 4700},
    {'city_name': 'Kuching', 'city_id': 11, 'this_week_orders': 76986, 'same_week_last_month_orders': 125611, 'ytd_avg_orders': 118222, 'this_week_completed_orders': 70434, 'same_week_last_month_completed_orders': 115898, 'ytd_avg_completed_orders': 110511, 'this_week_completion_rate': 91.5, 'same_week_last_month_completion_rate': 92.3, 'ytd_avg_completion_rate': 93.5, 'this_week_eaters': 40859, 'same_week_last_month_eaters': 56398, 'ytd_avg_eaters': 54361, 'this_week_gmv': 2631424.48, 'same_week_last_month_gmv': 4503806.85, 'ytd_avg_gmv': 4043497.97, 'this_week_basket': 32.91, 'same_week_last_month_basket': 34.24, 'ytd_avg_basket': 32.01, 'this_week_promo_expense': 281117.49, 'same_week_last_month_promo_expense': 484455.75, 'ytd_avg_promo_expense': 392827.32, 'this_week_promo_orders': 41354, 'same_week_last_month_promo_orders': 71318, 'ytd_avg_promo_orders': 60326, 'this_week_promo_penetration': 53.7, 'same_week_last_month_promo_penetration': 56.8, 'ytd_avg_promo_penetration': 51.0, 'this_week_sessions': 68841, 'same_week_last_month_sessions': 110801, 'ytd_avg_sessions': 105416, 'this_week_completed_sessions': 66611, 'same_week_last_month_completed_sessions': 108741, 'ytd_avg_completed_sessions': 103979, 'this_week_orders_per_session': 1.1, 'same_week_last_month_orders_per_session': 1.1, 'ytd_avg_orders_per_session': 1.1, 'this_week_cops': 1.1, 'same_week_last_month_cops': 1.1, 'ytd_avg_cops': 1.1, 'this_week_new_pax': 1473, 'same_week_last_month_new_pax': 2653, 'ytd_avg_new_pax': 2405}
]

if __name__ == '__main__':
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
    
    # Check result
    success = (response.status_code == 200 and response.text.strip() == "ok")
    
    # Write result to file
    with open("report_send_result.txt", "w") as f:
        if success:
            f.write("SUCCESS: Weekly report sent to Slack with LIVE New Pax data!\n")
            f.write(f"OC New Pax: {oc_data[0]['this_week_new_pax']}\n")
            f.write("Top Cities New Pax:\n")
            for city in top_cities_data:
                f.write(f"  {city['city_name']}: {city['this_week_new_pax']}\n")
        else:
            f.write(f"Response: {response.status_code} - {response.text[:200]}\n")
    
    # Try to output
    try:
        if success:
            print("SUCCESS: Weekly report sent to Slack with LIVE New Pax data!")
            print(f"OC New Pax: {oc_data[0]['this_week_new_pax']}")
            print("Top Cities New Pax:")
            for city in top_cities_data:
                print(f"  {city['city_name']}: {city['this_week_new_pax']}")
        else:
            print(f"Response: {response.status_code} - {response.text[:200]}")
    except:
        pass


