"""
AI Tool Adoption Tracker - Penang Team
Tracks and analyzes AI tool usage across team members
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from pathlib import Path

# Team structure
PENANG_TEAM = {
    'AM': ['Chia Yee', 'Darren', 'Suki'],
    'MGS': ['Teoh Jun Ling', 'Lee Sook Chin', 'Low Jia Ying', 'Hon Yi Ni']
}

# Common AI tools to track
AI_TOOLS = [
    'Cursor',
    'ChatGPT',
    'Claude (Anthropic)',
    'GitHub Copilot',
    'Microsoft Copilot',
    'Perplexity',
    'Notion AI',
    'Other'
]

# Usage frequency options
FREQUENCY_OPTIONS = {
    'Daily': 5,
    '3-4x per week': 3.5,
    '1-2x per week': 1.5,
    'Few times per month': 0.5,
    'Rarely/Never': 0
}

def create_tracking_template(output_path='ai_tool_usage_tracker.xlsx'):
    """Create Excel template for tracking AI tool usage"""
    
    # Create weekly tracking template
    weeks = []
    current_date = datetime.now()
    
    # Generate 4 weeks of tracking
    for i in range(4):
        week_start = current_date - timedelta(days=current_date.weekday() + (i * 7))
        week_end = week_start + timedelta(days=6)
        weeks.append({
            'Week': f"Week {i+1}",
            'Start Date': week_start.strftime('%Y-%m-%d'),
            'End Date': week_end.strftime('%Y-%m-%d')
        })
    
    # Create Excel writer
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        
        # Sheet 1: Weekly Usage Tracking
        weekly_data = []
        for week in weeks:
            for role, members in PENANG_TEAM.items():
                for member in members:
                    for tool in AI_TOOLS:
                        weekly_data.append({
                            'Week': week['Week'],
                            'Start Date': week['Start Date'],
                            'End Date': week['End Date'],
                            'Role': role,
                            'Team Member': member,
                            'AI Tool': tool,
                            'Usage Frequency': '',  # To be filled
                            'Primary Use Case': '',  # e.g., "Code generation", "Data analysis", "Writing"
                            'Time Saved (hours/week)': '',
                            'Notes': ''
                        })
        
        df_weekly = pd.DataFrame(weekly_data)
        df_weekly.to_excel(writer, sheet_name='Weekly Tracking', index=False)
        
        # Sheet 2: Team Member List
        team_list = []
        for role, members in PENANG_TEAM.items():
            for member in members:
                team_list.append({
                    'Name': member,
                    'Role': role,
                    'Email': '',  # To be filled
                    'Start Date': '',  # Optional
                    'Notes': ''
                })
        
        df_team = pd.DataFrame(team_list)
        df_team.to_excel(writer, sheet_name='Team Members', index=False)
        
        # Sheet 3: AI Tools Reference
        tools_ref = []
        for tool in AI_TOOLS:
            tools_ref.append({
                'Tool Name': tool,
                'Category': 'Code Assistant' if 'Cursor' in tool or 'Copilot' in tool else 'Chat/General',
                'Description': '',
                'Cost': '',
                'Notes': ''
            })
        
        df_tools = pd.DataFrame(tools_ref)
        df_tools.to_excel(writer, sheet_name='AI Tools Reference', index=False)
        
        # Sheet 4: Instructions
        instructions = [
            {'Section': 'How to Use', 'Content': '1. Fill in "Weekly Tracking" sheet with usage data'},
            {'Section': '', 'Content': '2. Update weekly (every Monday for previous week)'},
            {'Section': '', 'Content': '3. Usage Frequency options: Daily, 3-4x per week, 1-2x per week, Few times per month, Rarely/Never'},
            {'Section': '', 'Content': '4. Primary Use Case: Brief description (e.g., "SQL queries", "Report writing", "Code debugging")'},
            {'Section': '', 'Content': '5. Time Saved: Estimate hours saved per week using the tool'},
            {'Section': 'Analysis', 'Content': 'Run analyze_adoption() function to generate insights'},
            {'Section': 'Metrics Tracked', 'Content': '- Adoption rate (% of team using each tool)'},
            {'Section': '', 'Content': '- Usage frequency trends'},
            {'Section': '', 'Content': '- Time saved per tool'},
            {'Section': '', 'Content': '- Use case distribution'},
            {'Section': '', 'Content': '- Role-based adoption patterns'}
        ]
        
        df_instructions = pd.DataFrame(instructions)
        df_instructions.to_excel(writer, sheet_name='Instructions', index=False)
    
    print(f"✅ Tracking template created: {output_path}")
    print(f"   - {len(df_weekly)} tracking rows (4 weeks)")
    print(f"   - {len(df_team)} team members")
    print(f"   - {len(AI_TOOLS)} AI tools")
    return output_path


def load_tracking_data(file_path='ai_tool_usage_tracker.xlsx'):
    """Load tracking data from Excel file"""
    try:
        df = pd.read_excel(file_path, sheet_name='Weekly Tracking')
        df['Start Date'] = pd.to_datetime(df['Start Date'])
        df['End Date'] = pd.to_datetime(df['End Date'])
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None


def calculate_adoption_metrics(df):
    """Calculate adoption metrics from tracking data"""
    
    if df is None or df.empty:
        return None
    
    # Filter out empty rows
    df_active = df[df['Usage Frequency'].notna() & (df['Usage Frequency'] != '')].copy()
    
    if df_active.empty:
        return {
            'status': 'no_data',
            'message': 'No usage data found. Please fill in the tracking sheet.'
        }
    
    metrics = {}
    
    # 1. Overall Adoption Rate (by tool)
    tool_adoption = {}
    total_team_size = len(PENANG_TEAM['AM']) + len(PENANG_TEAM['MGS'])
    
    for tool in AI_TOOLS:
        tool_data = df_active[df_active['AI Tool'] == tool]
        if not tool_data.empty:
            unique_users = tool_data['Team Member'].nunique()
            adoption_rate = (unique_users / total_team_size) * 100
            tool_adoption[tool] = {
                'adoption_rate': adoption_rate,
                'users': unique_users,
                'total_team': total_team_size
            }
    
    metrics['tool_adoption'] = tool_adoption
    
    # 2. Usage Frequency Analysis
    frequency_mapping = {
        'Daily': 5,
        '3-4x per week': 3.5,
        '1-2x per week': 1.5,
        'Few times per month': 0.5,
        'Rarely/Never': 0
    }
    
    df_active['frequency_score'] = df_active['Usage Frequency'].map(frequency_mapping).fillna(0)
    
    avg_frequency_by_tool = df_active.groupby('AI Tool')['frequency_score'].mean().to_dict()
    metrics['avg_frequency'] = avg_frequency_by_tool
    
    # 3. Role-based Adoption
    role_adoption = {}
    for role in ['AM', 'MGS']:
        role_members = PENANG_TEAM[role]
        role_data = df_active[df_active['Role'] == role]
        if not role_data.empty:
            tools_used = role_data['AI Tool'].unique()
            role_adoption[role] = {
                'tools_used': len(tools_used),
                'total_tools': len(AI_TOOLS),
                'adoption_pct': (len(tools_used) / len(AI_TOOLS)) * 100,
                'unique_users': role_data['Team Member'].nunique(),
                'total_members': len(role_members)
            }
    
    metrics['role_adoption'] = role_adoption
    
    # 4. Time Saved Analysis
    df_active['time_saved'] = pd.to_numeric(df_active['Time Saved (hours/week)'], errors='coerce').fillna(0)
    time_saved_by_tool = df_active.groupby('AI Tool')['time_saved'].sum().to_dict()
    metrics['time_saved'] = time_saved_by_tool
    
    # 5. Use Case Distribution
    use_cases = df_active['Primary Use Case'].value_counts().to_dict()
    metrics['use_cases'] = use_cases
    
    # 6. Individual Adoption
    individual_adoption = {}
    for role, members in PENANG_TEAM.items():
        for member in members:
            member_data = df_active[df_active['Team Member'] == member]
            if not member_data.empty:
                tools_used = member_data['AI Tool'].nunique()
                total_time_saved = member_data['time_saved'].sum()
                individual_adoption[member] = {
                    'role': role,
                    'tools_used': tools_used,
                    'total_time_saved': total_time_saved,
                    'avg_frequency': member_data['frequency_score'].mean()
                }
    
    metrics['individual_adoption'] = individual_adoption
    
    # 7. Weekly Trends (if multiple weeks)
    if df_active['Week'].nunique() > 1:
        weekly_trends = {}
        for week in sorted(df_active['Week'].unique()):
            week_data = df_active[df_active['Week'] == week]
            weekly_trends[week] = {
                'active_users': week_data['Team Member'].nunique(),
                'tools_used': week_data['AI Tool'].nunique(),
                'total_time_saved': week_data['time_saved'].sum()
            }
        metrics['weekly_trends'] = weekly_trends
    
    return metrics


def generate_adoption_report(metrics, output_path='ai_tool_adoption_report.md'):
    """Generate markdown report with adoption insights"""
    
    if metrics is None or metrics.get('status') == 'no_data':
        report = f"""# AI Tool Adoption Report - Penang Team
## Status: No Data Available

Please fill in the tracking sheet and run the analysis again.

**Next Steps:**
1. Open `ai_tool_usage_tracker.xlsx`
2. Fill in the "Weekly Tracking" sheet
3. Run `analyze_adoption()` function
"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        return
    
    report_lines = [
        "# AI Tool Adoption Report - Penang Team",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "---",
        "",
        "## Executive Summary",
        ""
    ]
    
    # Overall adoption summary
    tool_adoption = metrics.get('tool_adoption', {})
    if tool_adoption:
        total_tools_adopted = len([t for t, data in tool_adoption.items() if data['adoption_rate'] > 0])
        top_tool = max(tool_adoption.items(), key=lambda x: x[1]['adoption_rate']) if tool_adoption else None
        
        report_lines.extend([
            f"- **Tools in Use**: {total_tools_adopted} out of {len(AI_TOOLS)} tracked tools",
            f"- **Top Tool**: {top_tool[0]} ({top_tool[1]['adoption_rate']:.1f}% adoption)" if top_tool else "- **Top Tool**: N/A",
            ""
        ])
    
    # Role-based summary
    role_adoption = metrics.get('role_adoption', {})
    if role_adoption:
        report_lines.extend([
            "### Role-Based Adoption:",
            ""
        ])
        for role, data in role_adoption.items():
            report_lines.append(
                f"- **{role}**: {data['unique_users']}/{data['total_members']} members using AI tools "
                f"({data['adoption_pct']:.1f}% tool coverage)"
            )
        report_lines.append("")
    
    report_lines.extend([
        "---",
        "",
        "## Tool Adoption Rates",
        ""
    ])
    
    # Tool adoption table
    if tool_adoption:
        report_lines.extend([
            "| Tool | Adoption Rate | Users | Total Team |",
            "|------|---------------|-------|------------|"
        ])
        sorted_tools = sorted(tool_adoption.items(), key=lambda x: x[1]['adoption_rate'], reverse=True)
        for tool, data in sorted_tools:
            report_lines.append(
                f"| **{tool}** | {data['adoption_rate']:.1f}% | {data['users']} | {data['total_team']} |"
            )
        report_lines.append("")
    
    # Usage frequency
    report_lines.extend([
        "---",
        "",
        "## Usage Frequency Analysis",
        ""
    ])
    
    avg_frequency = metrics.get('avg_frequency', {})
    if avg_frequency:
        report_lines.extend([
            "| Tool | Avg Frequency Score* |",
            "|------|----------------------|"
        ])
        sorted_freq = sorted(avg_frequency.items(), key=lambda x: x[1], reverse=True)
        for tool, score in sorted_freq:
            freq_label = 'High' if score >= 3 else 'Medium' if score >= 1 else 'Low'
            report_lines.append(f"| **{tool}** | {score:.2f} ({freq_label}) |")
        report_lines.extend([
            "",
            "*Frequency Score: Daily=5, 3-4x/week=3.5, 1-2x/week=1.5, Few times/month=0.5, Rarely=0",
            ""
        ])
    
    # Time saved
    report_lines.extend([
        "---",
        "",
        "## Time Saved Analysis",
        ""
    ])
    
    time_saved = metrics.get('time_saved', {})
    if time_saved:
        total_time = sum(time_saved.values())
        report_lines.extend([
            f"**Total Time Saved**: {total_time:.1f} hours/week across all tools",
            "",
            "| Tool | Hours Saved/Week |",
            "|------|------------------|"
        ])
        sorted_time = sorted(time_saved.items(), key=lambda x: x[1], reverse=True)
        for tool, hours in sorted_time:
            if hours > 0:
                report_lines.append(f"| **{tool}** | {hours:.1f} |")
        report_lines.append("")
    
    # Individual adoption
    report_lines.extend([
        "---",
        "",
        "## Individual Adoption Status",
        ""
    ])
    
    individual = metrics.get('individual_adoption', {})
    if individual:
        report_lines.extend([
            "| Team Member | Role | Tools Used | Time Saved (hrs/week) | Avg Frequency |",
            "|-------------|------|------------|------------------------|---------------|"
        ])
        sorted_individual = sorted(individual.items(), key=lambda x: x[1]['tools_used'], reverse=True)
        for member, data in sorted_individual:
            report_lines.append(
                f"| **{member}** | {data['role']} | {data['tools_used']} | "
                f"{data['total_time_saved']:.1f} | {data['avg_frequency']:.2f} |"
            )
        report_lines.append("")
    
    # Use cases
    use_cases = metrics.get('use_cases', {})
    if use_cases:
        report_lines.extend([
            "---",
            "",
            "## Primary Use Cases",
            ""
        ])
        for use_case, count in use_cases.items():
            if pd.notna(use_case) and use_case.strip():
                report_lines.append(f"- **{use_case}**: {count} instances")
        report_lines.append("")
    
    # Weekly trends
    weekly_trends = metrics.get('weekly_trends', {})
    if weekly_trends and len(weekly_trends) > 1:
        report_lines.extend([
            "---",
            "",
            "## Weekly Trends",
            "",
            "| Week | Active Users | Tools Used | Total Time Saved (hrs) |",
            "|------|--------------|------------|------------------------|"
        ])
        for week, data in sorted(weekly_trends.items()):
            report_lines.append(
                f"| {week} | {data['active_users']} | {data['tools_used']} | {data['total_time_saved']:.1f} |"
            )
        report_lines.append("")
    
    # Recommendations
    report_lines.extend([
        "---",
        "",
        "## Recommendations",
        ""
    ])
    
    # Generate recommendations based on data
    if tool_adoption:
        low_adoption_tools = [t for t, d in tool_adoption.items() if d['adoption_rate'] < 30]
        if low_adoption_tools:
            report_lines.append("### Low Adoption Tools (<30%):")
            for tool in low_adoption_tools:
                report_lines.append(f"- **{tool}**: Consider training or showcasing use cases")
            report_lines.append("")
    
    if individual:
        non_users = [m for m in PENANG_TEAM['AM'] + PENANG_TEAM['MGS'] if m not in individual]
        if non_users:
            report_lines.append("### Team Members Not Using AI Tools:")
            for member in non_users:
                report_lines.append(f"- **{member}**: Consider 1-on-1 training or peer sharing")
            report_lines.append("")
    
    report_lines.extend([
        "### Next Steps:",
        "1. Share top use cases with low-adoption team members",
        "2. Schedule AI tool training sessions",
        "3. Create internal best practices documentation",
        "4. Track ROI: time saved vs. tool costs",
        ""
    ])
    
    # Write report
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print(f"✅ Adoption report generated: {output_path}")
    return output_path


def analyze_adoption(tracker_file='ai_tool_usage_tracker.xlsx', 
                     report_file='ai_tool_adoption_report.md'):
    """Main function to analyze adoption and generate report"""
    
    print("="*80)
    print("AI TOOL ADOPTION ANALYSIS - PENANG TEAM")
    print("="*80)
    print()
    
    # Load data
    print("Loading tracking data...")
    df = load_tracking_data(tracker_file)
    
    if df is None:
        print(f"❌ Could not load data from {tracker_file}")
        print("   Please ensure the file exists and is properly formatted.")
        return None
    
    # Calculate metrics
    print("Calculating adoption metrics...")
    metrics = calculate_adoption_metrics(df)
    
    if metrics is None or metrics.get('status') == 'no_data':
        print("⚠️  No usage data found in tracking sheet.")
        print("   Please fill in the 'Weekly Tracking' sheet first.")
        # Still generate report with instructions
        generate_adoption_report(metrics, report_file)
        return metrics
    
    # Generate report
    print("Generating adoption report...")
    generate_adoption_report(metrics, report_file)
    
    # Print summary
    print()
    print("="*80)
    print("SUMMARY")
    print("="*80)
    
    tool_adoption = metrics.get('tool_adoption', {})
    if tool_adoption:
        top_tool = max(tool_adoption.items(), key=lambda x: x[1]['adoption_rate'])
        print(f"Top Tool: {top_tool[0]} ({top_tool[1]['adoption_rate']:.1f}% adoption)")
    
    individual = metrics.get('individual_adoption', {})
    if individual:
        print(f"Active Users: {len(individual)}/{len(PENANG_TEAM['AM']) + len(PENANG_TEAM['MGS'])}")
    
    time_saved = metrics.get('time_saved', {})
    if time_saved:
        total_time = sum(time_saved.values())
        print(f"Total Time Saved: {total_time:.1f} hours/week")
    
    print()
    print(f"📊 Full report saved to: {report_file}")
    print()
    
    return metrics


if __name__ == '__main__':
    # Create template if it doesn't exist
    template_path = 'ai_tool_usage_tracker.xlsx'
    if not os.path.exists(template_path):
        print("Creating tracking template...")
        create_tracking_template(template_path)
        print()
        print("✅ Template created! Please fill in the tracking data, then run analyze_adoption()")
    else:
        # Analyze existing data
        analyze_adoption()

