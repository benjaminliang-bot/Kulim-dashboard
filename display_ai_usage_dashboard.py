"""
Display AI Tools Usage Dashboard from query results
"""

from format_ai_usage_results import format_ai_usage_dashboard, format_usage_table

# Parse the query results into list of dicts
# Latest record (2025-11-26)
latest_record = {
    'as_of_date': '2025-11-26',
    'employee_id': '78272',
    'residing_region': 'Malaysia',
    'office_location_name': 'Petaling Jaya (First Avenue)-Selangor',
    'level_03_from_the_top': 'PCOO+ Office',
    'level_04_from_the_top': 'Operation - Malaysia',
    'level_05_from_the_top': 'MY - Outer Cities',
    'level_06_from_the_top': 'Non KV - Commercial',
    'level_07_from_the_top': 'Non KV – Borneo & NEC',
    'sup_org_name': 'Non KV – Borneo & NEC',
    'tech_nontech': 'Non-Tech',
    'seniority': '(2) Senior G4-6',
    'has_direct_report': 'Manager',
    'tenure_band': '(4) 2-3 years',
    'email_work': 'benjamin.liang@grabtaxi.com',
    'sow_as_of_date': '2025-11-24',
    'is_used_cursor': 1,
    'is_used_gpt': 0,
    'is_used_gpt_prompt': 0,
    'is_used_jarvis_superset': 0,
    'is_used_jarvis_slackbot': 0,
    'is_used_gemini': 1,
    'is_used_jarvis': 0,
    'is_used_any': 1,
    'is_used_cursor_wk_sow': 0,
    'is_used_gpt_wk_sow': 0,
    'is_used_gpt_prompt_wk_sow': 0,
    'is_used_jarvis_wk_sow': 0,
    'is_used_gemini_wk_sow': 0,
    'is_used_any_wk_sow': 0,
    'num_active_days_cursor_wk_sow': 0,
    'num_active_days_gpt_wk_sow': 0,
    'num_active_days_gpt_prompt_wk_sow': 0,
    'num_active_days_jarvis_wk_sow': 0,
    'num_active_days_gemini_wk_sow': 0,
    'num_active_days_any_wk_sow': 0,
    'num_working_days_wk_sow': 0,
    'num_streak_dau5': 0,
    'num_inactive_weeks_since_last_active': 0,
    'streak_percent_rank_dau5': 1.0,
    'streak_rank_dau5': 1,
    'is_dau5': 0,
    'is_dormant_users': 0
}

# Sample of recent records for trend analysis
sample_records = [
    latest_record,
    {
        'as_of_date': '2025-11-24',
        'is_used_cursor': 0,
        'is_used_gpt': 0,
        'is_used_gemini': 0,
        'is_used_any': 0,
        'sow_as_of_date': '2025-11-24',
        'num_active_days_any_wk_sow': 2,
        'num_working_days_wk_sow': 2,
        'num_streak_dau5': 1,
        'streak_percent_rank_dau5': 0.2844383373411199,
        'streak_rank_dau5': 23,
        'is_dau5': 1,
        'residing_region': 'Malaysia',
        'sup_org_name': 'Non KV – Borneo & NEC',
        'level_03_from_the_top': 'PCOO+ Office',
        'tech_nontech': 'Non-Tech',
        'seniority': '(2) Senior G4-6'
    },
    {
        'as_of_date': '2025-11-17',
        'is_used_cursor': 0,
        'is_used_gpt': 1,
        'is_used_gpt_prompt': 1,
        'is_used_gemini': 1,
        'is_used_any': 1,
        'sow_as_of_date': '2025-11-17',
        'num_active_days_any_wk_sow': 3,
        'num_active_days_gpt_wk_sow': 1,
        'num_active_days_gpt_prompt_wk_sow': 1,
        'num_active_days_gemini_wk_sow': 1,
        'num_working_days_wk_sow': 3,
        'num_streak_dau5': 0,
        'streak_percent_rank_dau5': 1.0,
        'streak_rank_dau5': 23,
        'is_dau5': 0,
        'residing_region': 'Malaysia',
        'sup_org_name': 'Non KV – Borneo & NEC',
        'level_03_from_the_top': 'PCOO+ Office',
        'tech_nontech': 'Non-Tech',
        'seniority': '(2) Senior G4-6'
    }
]

if __name__ == '__main__':
    # Generate dashboard
    dashboard = format_ai_usage_dashboard([latest_record], 'benjamin.liang@grabtaxi.com')
    print(dashboard)
    print("\n")
    print(format_usage_table(sample_records, max_rows=5))

