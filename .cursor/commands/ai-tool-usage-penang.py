"""
Cursor command handler for ai-tool-usage-penang
This script queries AI tool usage for all Penang team members and displays dashboard
"""

import os
import sys

# Get the Python script directory (parent of .cursor/commands)
current_file = os.path.abspath(__file__)
commands_dir = os.path.dirname(current_file)  # .cursor/commands
cursor_dir = os.path.dirname(commands_dir)     # .cursor
script_dir = os.path.dirname(cursor_dir)       # Python/

# Change to script directory
os.chdir(script_dir)

# Add script directory to path for imports
sys.path.insert(0, script_dir)

if __name__ == '__main__':
    try:
        print("=" * 80)
        print("PENANG TEAM AI TOOLS USAGE CHECK")
        print("=" * 80)
        print()
        print("📊 Querying AI tool usage for all Penang team members...")
        print()
        
        # Import the query generator
        from generate_penang_team_ai_dashboard import generate_team_usage_query, PENANG_TEAM_EMAILS, TEAM_NAMES
        
        # Generate and display query
        query = generate_team_usage_query()
        
        print("✅ Query generated successfully!")
        print()
        print("📋 Team Members to Query:")
        for i, email in enumerate(PENANG_TEAM_EMAILS, 1):
            name = TEAM_NAMES.get(email, email.split('@')[0])
            print(f"   {i:2d}. {name} ({email})")
        print()
        print("=" * 80)
        print("SQL QUERY (Ready to Execute)")
        print("=" * 80)
        print()
        print(query)
        print()
        print("=" * 80)
        print()
        print("⚠️  Next Step: Execute this query using MCP tool")
        print("   Command: mcp_mcp-grab-data_run_presto_query")
        print()
        print("💡 The AI assistant will execute the query and generate the dashboard.")
        print()
        print("📄 Full dashboard will be saved to:")
        print("   PENANG_TEAM_AI_USAGE_DASHBOARD_COMPLETE.md")
        print()
        
    except ImportError as e:
        print(f"❌ Error: Could not import query module: {e}")
        print("   Make sure query_penang_team_ai_usage.py exists in the workspace")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

