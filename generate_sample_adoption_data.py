"""
Generate sample AI tool adoption data for testing/demonstration
"""

import pandas as pd
from datetime import datetime, timedelta
from ai_tool_adoption_tracker import PENANG_TEAM, AI_TOOLS, create_tracking_template

def generate_sample_data(output_path='ai_tool_usage_tracker.xlsx'):
    """Generate realistic sample data for demonstration"""
    
    # Create template first
    create_tracking_template(output_path)
    
    # Load the template
    df = pd.read_excel(output_path, sheet_name='Weekly Tracking')
    
    # Sample usage patterns (realistic scenarios)
    sample_patterns = {
        'Chia Yee': {
            'Cursor': {'freq': 'Daily', 'use_case': 'SQL queries, data analysis', 'time': 8},
            'ChatGPT': {'freq': '3-4x per week', 'use_case': 'Report writing, analysis', 'time': 3},
            'Perplexity': {'freq': '1-2x per week', 'use_case': 'Research, market insights', 'time': 1}
        },
        'Darren': {
            'Cursor': {'freq': 'Daily', 'use_case': 'Code generation, debugging', 'time': 6},
            'ChatGPT': {'freq': '3-4x per week', 'use_case': 'Documentation, emails', 'time': 2},
            'GitHub Copilot': {'freq': 'Daily', 'use_case': 'Code completion', 'time': 4}
        },
        'Suki': {
            'Cursor': {'freq': '3-4x per week', 'use_case': 'Data analysis scripts', 'time': 4},
            'ChatGPT': {'freq': '1-2x per week', 'use_case': 'Content creation', 'time': 1.5}
        },
        'Teoh Jun Ling': {
            'ChatGPT': {'freq': '1-2x per week', 'use_case': 'Merchant communications', 'time': 2},
            'Notion AI': {'freq': 'Few times per month', 'use_case': 'Note-taking, planning', 'time': 0.5}
        },
        'Lee Sook Chin': {
            'Cursor': {'freq': '3-4x per week', 'use_case': 'SQL queries for merchant analysis', 'time': 5},
            'ChatGPT': {'freq': '1-2x per week', 'use_case': 'Report summaries', 'time': 1}
        },
        'Low Jia Ying': {
            'ChatGPT': {'freq': '3-4x per week', 'use_case': 'Email drafting, analysis', 'time': 3},
            'Perplexity': {'freq': '1-2x per week', 'use_case': 'Market research', 'time': 1}
        },
        'Hon Yi Ni': {
            'ChatGPT': {'freq': 'Few times per month', 'use_case': 'General assistance', 'time': 0.5}
        }
    }
    
    # Fill in sample data for 2 weeks
    for idx, row in df.iterrows():
        member = row['Team Member']
        tool = row['AI Tool']
        week = row['Week']
        
        # Only fill Week 1 and Week 2
        if week in ['Week 1', 'Week 2']:
            if member in sample_patterns and tool in sample_patterns[member]:
                pattern = sample_patterns[member][tool]
                df.at[idx, 'Usage Frequency'] = pattern['freq']
                df.at[idx, 'Primary Use Case'] = pattern['use_case']
                df.at[idx, 'Time Saved (hours/week)'] = pattern['time']
                df.at[idx, 'Notes'] = 'Sample data'
    
    # Save updated data
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Weekly Tracking', index=False)
        
        # Keep other sheets
        df_team = pd.read_excel(output_path, sheet_name='Team Members')
        df_tools = pd.read_excel(output_path, sheet_name='AI Tools Reference')
        df_instructions = pd.read_excel(output_path, sheet_name='Instructions')
        
        df_team.to_excel(writer, sheet_name='Team Members', index=False)
        df_tools.to_excel(writer, sheet_name='AI Tools Reference', index=False)
        df_instructions.to_excel(writer, sheet_name='Instructions', index=False)
    
    print(f"✅ Sample data generated in {output_path}")
    print("   - Week 1 & Week 2 filled with realistic usage patterns")
    print("   - Ready for analysis demonstration")
    return output_path


if __name__ == '__main__':
    generate_sample_data()

