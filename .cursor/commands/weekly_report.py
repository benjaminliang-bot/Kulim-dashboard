"""
Cursor command handler for weekly_report
This script is executed when user types /weekly_report in Cursor chat
It will execute queries via MCP, update hardcoded data, then run the main script
"""

import os
import sys
import subprocess
import io

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Get the Python script directory (parent of .cursor/commands)
# File structure: Python/.cursor/commands/weekly_report.py
# We need: Python/process_and_send_weekly_report.py
current_file = os.path.abspath(__file__)
commands_dir = os.path.dirname(current_file)  # .cursor/commands
cursor_dir = os.path.dirname(commands_dir)     # .cursor
script_dir = os.path.dirname(cursor_dir)       # Python/

# Change to script directory
os.chdir(script_dir)

# Import and run the main report script
if __name__ == '__main__':
    try:
        script_path = os.path.join(script_dir, "process_and_send_weekly_report.py")
        
        # Verify script exists
        if not os.path.exists(script_path):
            print(f"❌ Error: Script not found at {script_path}")
            sys.exit(1)
        
        print("Running weekly report...")
        print(f"Working directory: {script_dir}")
        print("")
        print("Note: Queries will be executed via MCP and data will be updated")
        print("   The AI assistant will execute queries and update hardcoded data")
        print("")
        
        # Execute the main report script
        result = subprocess.run(
            [sys.executable, script_path],
            cwd=script_dir,
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            print("\n✅ Weekly report completed successfully!")
        else:
            print(f"\n❌ Weekly report failed with exit code {result.returncode}")
        
        sys.exit(result.returncode)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

