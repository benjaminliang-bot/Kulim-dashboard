#!/usr/bin/env python3
"""
Cursor Command Handler: update-kulim
Executes the update_kulim.py script to generate SQL query and update Kulim dashboard
"""

import os
import sys
import subprocess

def main():
    """Execute the update-kulim script"""
    # Get the workspace root directory
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Change to workspace directory
    os.chdir(workspace_root)
    
    # Path to the update script
    update_script = os.path.join(workspace_root, 'update_kulim.py')
    
    if not os.path.exists(update_script):
        print(f"ERROR: update_kulim.py not found at {update_script}")
        return 1
    
    try:
        # Execute the update script
        print("=" * 80)
        print("EXECUTING UPDATE-KULIM COMMAND")
        print("=" * 80)
        print()
        
        # Run the script
        result = subprocess.run(
            [sys.executable, update_script],
            cwd=workspace_root,
            capture_output=False,
            text=True
        )
        
        return result.returncode
        
    except Exception as e:
        print(f"ERROR: Failed to execute update_kulim.py: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())

