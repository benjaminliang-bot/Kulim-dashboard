"""
Cursor command handler for update-kulim
This script is executed when user types /update-kulim in Cursor chat
"""

import os
import sys
import subprocess

# Get the Python script directory (parent of .cursor/commands)
# File structure: Python/.cursor/commands/update-kulim.py
# We need: Python/update_kulim.py
current_file = os.path.abspath(__file__)
commands_dir = os.path.dirname(current_file)  # .cursor/commands
cursor_dir = os.path.dirname(commands_dir)     # .cursor
script_dir = os.path.dirname(cursor_dir)       # Python/

# Change to script directory
os.chdir(script_dir)

# Import and run the main update script
if __name__ == '__main__':
    try:
        script_path = os.path.join(script_dir, "update_kulim.py")
        
        # Verify script exists
        if not os.path.exists(script_path):
            print(f"❌ Error: Script not found at {script_path}")
            sys.exit(1)
        
        # Execute the main update script
        result = subprocess.run(
            [sys.executable, script_path],
            cwd=script_dir,
            capture_output=False,
            text=True
        )
        sys.exit(result.returncode)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

