"""
Query AI Tools Usage for Penang Team
Queries all team members and generates dashboard report
"""

import sys
import io
from datetime import datetime

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
    """Main function to generate query"""
    print("=" * 80)
    print("PENANG TEAM AI TOOLS USAGE QUERY")
    print("=" * 80)
    print()
    print(f"Team Members: {len(PENANG_TEAM_EMAILS)}")
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
    print("📊 After executing the query, the results will be used to generate")
    print("   the team dashboard report.")
    print()
    print("💡 Tip: Use the /ai-tool-usage-penang command in Cursor chat to")
    print("   automatically query and display the dashboard.")

if __name__ == '__main__':
    main()

