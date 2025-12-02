"""
Format AI Tools Usage Results - Create executive dashboard from query results
"""

from datetime import datetime
from typing import List, Dict, Any

def format_ai_usage_dashboard(data: List[Dict], email: str) -> str:
    """Format AI tools usage data as executive dashboard"""
    
    if not data:
        return f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    AI TOOLS USAGE DASHBOARD                                  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ Email: {email:<66} ║
║ Status: ❌ No usage data found                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    
    # Get latest record (most recent date)
    latest = max(data, key=lambda x: x.get('as_of_date', ''))
    
    # Calculate metrics
    total_records = len(data)
    date_range = {
        'earliest': min(row.get('as_of_date', '') for row in data),
        'latest': max(row.get('as_of_date', '') for row in data)
    }
    
    # Tool usage flags (from latest record)
    tools_used = []
    if latest.get('is_used_cursor', 0) == 1:
        tools_used.append('Cursor')
    if latest.get('is_used_gpt', 0) == 1:
        tools_used.append('GPT')
    if latest.get('is_used_gpt_prompt', 0) == 1:
        tools_used.append('GPT Prompt')
    if latest.get('is_used_jarvis', 0) == 1:
        tools_used.append('Jarvis')
    if latest.get('is_used_gemini', 0) == 1:
        tools_used.append('Gemini')
    if latest.get('is_used_jarvis_superset', 0) == 1:
        tools_used.append('Jarvis Superset')
    if latest.get('is_used_jarvis_slackbot', 0) == 1:
        tools_used.append('Jarvis Slackbot')
    
    # Weekly usage (from latest)
    weekly_usage = {
        'cursor': latest.get('num_active_days_cursor_wk_sow', 0),
        'gpt': latest.get('num_active_days_gpt_wk_sow', 0),
        'gpt_prompt': latest.get('num_active_days_gpt_prompt_wk_sow', 0),
        'jarvis': latest.get('num_active_days_jarvis_wk_sow', 0),
        'gemini': latest.get('num_active_days_gemini_wk_sow', 0),
        'any': latest.get('num_active_days_any_wk_sow', 0)
    }
    
    working_days = latest.get('num_working_days_wk_sow', 0)
    
    # Adoption metrics
    adoption_rate = (latest.get('is_used_any', 0) * 100) if latest.get('is_used_any') is not None else 0
    dau5_status = "✅ Active" if latest.get('is_dau5', 0) == 1 else "❌ Inactive"
    streak_days = latest.get('num_streak_dau5', 0)
    streak_rank = latest.get('streak_rank_dau5', 0)
    streak_percentile = latest.get('streak_percent_rank_dau5', 0)
    
    # Organizational info
    org_info = {
        'region': latest.get('residing_region', 'N/A'),
        'org': latest.get('sup_org_name', 'N/A'),
        'level_03': latest.get('level_03_from_the_top', 'N/A'),
        'tech_nontech': latest.get('tech_nontech', 'N/A'),
        'seniority': latest.get('seniority', 'N/A')
    }
    
    # Build dashboard
    dashboard = []
    dashboard.append("╔══════════════════════════════════════════════════════════════════════════════╗")
    dashboard.append("║                    AI TOOLS USAGE DASHBOARD                                  ║")
    dashboard.append("╠══════════════════════════════════════════════════════════════════════════════╣")
    dashboard.append(f"║ Email: {email:<66} ║")
    dashboard.append(f"║ Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S'):<58} ║")
    dashboard.append("╠══════════════════════════════════════════════════════════════════════════════╣")
    
    # Summary Statistics
    dashboard.append("║ 📊 SUMMARY STATISTICS                                                         ║")
    dashboard.append("╠══════════════════════════════════════════════════════════════════════════════╣")
    dashboard.append(f"║ Total Records: {total_records:<60} ║")
    dashboard.append(f"║ Date Range: {date_range['earliest']} to {date_range['latest']:<40} ║")
    dashboard.append(f"║ Latest Record: {latest.get('as_of_date', 'N/A'):<58} ║")
    dashboard.append("╠══════════════════════════════════════════════════════════════════════════════╣")
    
    # Tool Adoption
    dashboard.append("║ 🛠️  TOOL ADOPTION (Latest Record)                                            ║")
    dashboard.append("╠══════════════════════════════════════════════════════════════════════════════╣")
    if tools_used:
        dashboard.append(f"║ Active Tools: {', '.join(tools_used):<60} ║")
    else:
        dashboard.append("║ Active Tools: None (No AI tools in use)                                    ║")
    dashboard.append(f"║ Any Tool Usage: {'✅ Yes' if latest.get('is_used_any', 0) == 1 else '❌ No':<60} ║")
    dashboard.append(f"║ DAU5 Status: {dau5_status:<60} ║")
    dashboard.append("╠══════════════════════════════════════════════════════════════════════════════╣")
    
    # Weekly Activity
    dashboard.append("║ 📅 WEEKLY ACTIVITY (Week Starting: {})                            ║".format(latest.get('sow_as_of_date', 'N/A')))
    dashboard.append("╠══════════════════════════════════════════════════════════════════════════════╣")
    dashboard.append(f"║ Working Days: {working_days:<60} ║")
    if weekly_usage['any'] > 0:
        dashboard.append(f"║ Active Days (Any Tool): {weekly_usage['any']}/{working_days} ({weekly_usage['any']/working_days*100:.1f}%){' '*(60-len(f'Active Days (Any Tool): {weekly_usage['any']}/{working_days} ({weekly_usage['any']/working_days*100:.1f}%)'))} ║")
    else:
        dashboard.append("║ Active Days (Any Tool): 0 (No activity this week)                          ║")
    
    if weekly_usage['cursor'] > 0:
        dashboard.append(f"║   • Cursor: {weekly_usage['cursor']} days{' '*(60-len(f'  • Cursor: {weekly_usage['cursor']} days'))} ║")
    if weekly_usage['gpt'] > 0:
        dashboard.append(f"║   • GPT: {weekly_usage['gpt']} days{' '*(60-len(f'  • GPT: {weekly_usage['gpt']} days'))} ║")
    if weekly_usage['gpt_prompt'] > 0:
        dashboard.append(f"║   • GPT Prompt: {weekly_usage['gpt_prompt']} days{' '*(60-len(f'  • GPT Prompt: {weekly_usage['gpt_prompt']} days'))} ║")
    if weekly_usage['jarvis'] > 0:
        dashboard.append(f"║   • Jarvis: {weekly_usage['jarvis']} days{' '*(60-len(f'  • Jarvis: {weekly_usage['jarvis']} days'))} ║")
    if weekly_usage['gemini'] > 0:
        dashboard.append(f"║   • Gemini: {weekly_usage['gemini']} days{' '*(60-len(f'  • Gemini: {weekly_usage['gemini']} days'))} ║")
    dashboard.append("╠══════════════════════════════════════════════════════════════════════════════╣")
    
    # Streak Metrics
    dashboard.append("║ 🔥 STREAK METRICS                                                              ║")
    dashboard.append("╠══════════════════════════════════════════════════════════════════════════════╣")
    dashboard.append(f"║ Current Streak: {streak_days} days{' '*(60-len(f'Current Streak: {streak_days} days'))} ║")
    if streak_percentile is not None:
        dashboard.append(f"║ Streak Percentile: {streak_percentile*100:.1f}% (Rank: {streak_rank}){' '*(60-len(f'Streak Percentile: {streak_percentile*100:.1f}% (Rank: {streak_rank})'))} ║")
    inactive_weeks = latest.get('num_inactive_weeks_since_last_active', 0)
    if inactive_weeks > 0:
        dashboard.append(f"║ Inactive Weeks: {inactive_weeks} weeks since last active{' '*(60-len(f'Inactive Weeks: {inactive_weeks} weeks since last active'))} ║")
    dashboard.append("╠══════════════════════════════════════════════════════════════════════════════╣")
    
    # Organizational Context
    dashboard.append("║ 🏢 ORGANIZATIONAL CONTEXT                                                      ║")
    dashboard.append("╠══════════════════════════════════════════════════════════════════════════════╣")
    dashboard.append(f"║ Region: {org_info['region']:<62} ║")
    dashboard.append(f"║ Organization: {org_info['org'][:62]:<62} ║")
    dashboard.append(f"║ Level 03: {org_info['level_03'][:62]:<62} ║")
    dashboard.append(f"║ Tech/Non-Tech: {org_info['tech_nontech']:<58} ║")
    dashboard.append(f"║ Seniority: {org_info['seniority']:<60} ║")
    dashboard.append("╚══════════════════════════════════════════════════════════════════════════════╝")
    
    return "\n".join(dashboard)


def format_usage_table(data: List[Dict], max_rows: int = 10) -> str:
    """Format usage data as ASCII table (for detailed view)"""
    if not data:
        return "No data available"
    
    # Get relevant columns
    key_columns = [
        'as_of_date', 'is_used_cursor', 'is_used_gpt', 'is_used_jarvis', 
        'is_used_gemini', 'is_used_any', 'num_active_days_any_wk_sow',
        'num_streak_dau5', 'is_dau5'
    ]
    
    # Filter to available columns
    available_cols = [col for col in key_columns if col in data[0].keys()]
    
    # Build table
    lines = []
    lines.append("=" * 100)
    lines.append("DETAILED USAGE HISTORY (Last {} records)".format(min(len(data), max_rows)))
    lines.append("=" * 100)
    
    # Header
    header = " | ".join(col.replace('_', ' ').title()[:15].ljust(15) for col in available_cols)
    lines.append(header)
    lines.append("-" * len(header))
    
    # Rows (most recent first)
    for row in data[:max_rows]:
        row_str = " | ".join(
            str(row.get(col, 'N/A'))[:15].ljust(15) for col in available_cols
        )
        lines.append(row_str)
    
    lines.append("=" * 100)
    
    return "\n".join(lines)

