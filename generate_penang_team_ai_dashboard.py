"""
Generate Penang Team AI Tools Usage Dashboard
Queries all team members and generates comprehensive dashboard report
"""

import sys
import io
from datetime import datetime
from typing import List, Dict, Any

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Penang Team Email List (12 members)
PENANG_TEAM_EMAILS = [
    'benjamin.liang@grabtaxi.com',
    'darren.ng@grabtaxi.com',
    'suki.teoh@grabtaxi.com',
    'chiayee.leong@grabtaxi.com',
    'earnest.koe@grabtaxi.com',
    'xinrong.chong@grabtaxi.com',
    'xinyu.lin@grabtaxi.com',
    'ext.junling.teoh@grabtaxi.com',
    'sookchin.lee@grabtaxi.com',
    'jiaying.voon@grabtaxi.com',
    'yingjia.liu@grabtaxi.com',
    'hsintsi.lim@grabtaxi.com',
    'meiyan.chui@grabtaxi.com'
]

# Team member name mapping
TEAM_NAMES = {
    'benjamin.liang@grabtaxi.com': 'Benjamin Liang',
    'darren.ng@grabtaxi.com': 'Darren',
    'suki.teoh@grabtaxi.com': 'Suki',
    'chiayee.leong@grabtaxi.com': 'Chia Yee',
    'earnest.koe@grabtaxi.com': 'Earnest Koe',
    'xinrong.chong@grabtaxi.com': 'Xin Rong Chong',
    'xinyu.lin@grabtaxi.com': 'Xin Yu Lin (Jamie)',
    'ext.junling.teoh@grabtaxi.com': 'Teoh Jun Ling',
    'sookchin.lee@grabtaxi.com': 'Lee Sook Chin',
    'jiaying.voon@grabtaxi.com': 'Low Jia Ying',
    'yingjia.liu@grabtaxi.com': 'Hon Yi Ni',
    'hsintsi.lim@grabtaxi.com': 'Jess (Hsin Tsi Lim)',
    'meiyan.chui@grabtaxi.com': 'Maggie (Mei Yan Chui)'
}

def generate_team_usage_query():
    """Generate SQL query for all Penang team members"""
    
    email_list = "', '".join(PENANG_TEAM_EMAILS)
    
    query = f"""
SELECT 
    email_work,
    MAX(as_of_date) as latest_date,
    MAX(CASE WHEN as_of_date = (SELECT MAX(as_of_date) FROM ai_tooling_usage.grabbers_ai_usage_summary WHERE email_work = u.email_work) THEN is_used_cursor ELSE NULL END) as is_used_cursor,
    MAX(CASE WHEN as_of_date = (SELECT MAX(as_of_date) FROM ai_tooling_usage.grabbers_ai_usage_summary WHERE email_work = u.email_work) THEN is_used_gpt ELSE NULL END) as is_used_gpt,
    MAX(CASE WHEN as_of_date = (SELECT MAX(as_of_date) FROM ai_tooling_usage.grabbers_ai_usage_summary WHERE email_work = u.email_work) THEN is_used_gpt_prompt ELSE NULL END) as is_used_gpt_prompt,
    MAX(CASE WHEN as_of_date = (SELECT MAX(as_of_date) FROM ai_tooling_usage.grabbers_ai_usage_summary WHERE email_work = u.email_work) THEN is_used_gemini ELSE NULL END) as is_used_gemini,
    MAX(CASE WHEN as_of_date = (SELECT MAX(as_of_date) FROM ai_tooling_usage.grabbers_ai_usage_summary WHERE email_work = u.email_work) THEN is_used_jarvis ELSE NULL END) as is_used_jarvis,
    MAX(CASE WHEN as_of_date = (SELECT MAX(as_of_date) FROM ai_tooling_usage.grabbers_ai_usage_summary WHERE email_work = u.email_work) THEN is_used_any ELSE NULL END) as is_used_any,
    MAX(CASE WHEN as_of_date = (SELECT MAX(as_of_date) FROM ai_tooling_usage.grabbers_ai_usage_summary WHERE email_work = u.email_work) THEN num_active_days_any_wk_sow ELSE NULL END) as num_active_days_any_wk_sow,
    MAX(CASE WHEN as_of_date = (SELECT MAX(as_of_date) FROM ai_tooling_usage.grabbers_ai_usage_summary WHERE email_work = u.email_work) THEN num_streak_dau5 ELSE NULL END) as num_streak_dau5,
    MAX(CASE WHEN as_of_date = (SELECT MAX(as_of_date) FROM ai_tooling_usage.grabbers_ai_usage_summary WHERE email_work = u.email_work) THEN is_dau5 ELSE NULL END) as is_dau5,
    MAX(CASE WHEN as_of_date = (SELECT MAX(as_of_date) FROM ai_tooling_usage.grabbers_ai_usage_summary WHERE email_work = u.email_work) THEN streak_percent_rank_dau5 ELSE NULL END) as streak_percent_rank_dau5
FROM ai_tooling_usage.grabbers_ai_usage_summary u
WHERE email_work IN ('{email_list}')
GROUP BY email_work
ORDER BY email_work
"""
    return query.strip()

def main():
    """Main function"""
    print("=" * 80)
    print("PENANG TEAM AI TOOLS USAGE DASHBOARD GENERATOR")
    print("=" * 80)
    print()
    print(f"📊 Team Members: {len(PENANG_TEAM_EMAILS)} (12 total)")
    print()
    print("Generated SQL Query:")
    print("-" * 80)
    query = generate_team_usage_query()
    print(query)
    print("-" * 80)
    print()
    print("⚠️  Execute this query using MCP tool:")
    print("   mcp_mcp-grab-data_run_presto_query")
    print()
    print("=" * 80)
    print()
    print("💡 The AI assistant will execute the query and generate the dashboard.")
    print("   Dashboard will be saved to: PENANG_TEAM_AI_USAGE_DASHBOARD_COMPLETE.md")
    print()

if __name__ == '__main__':
    main()

