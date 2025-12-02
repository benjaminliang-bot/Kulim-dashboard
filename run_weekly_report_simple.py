"""
Simple Python script to run weekly report - can be triggered manually or via Cursor
No admin rights required!
"""

import subprocess
import sys
import os
import io

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Change to script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Run the main report script
print("🚀 Running weekly report...")
print(f"📁 Working directory: {script_dir}")
print("")

try:
    # Run the main script
    result = subprocess.run(
        [sys.executable, "process_and_send_weekly_report.py"],
        cwd=script_dir,
        capture_output=False,
        text=True
    )
    
    if result.returncode == 0:
        print("\n✅ Weekly report completed successfully!")
    else:
        print(f"\n❌ Weekly report failed with exit code {result.returncode}")
        sys.exit(1)
        
except Exception as e:
    print(f"\n❌ Error running weekly report: {e}")
    sys.exit(1)

