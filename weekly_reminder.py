"""
Weekly Reminder Script - Runs the report and shows a reminder
Can be run manually or added to startup/login scripts
"""

import os
import sys
from datetime import datetime, timedelta

# Add current directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

def should_run_report():
    """Check if it's Monday and time to run the report"""
    now = datetime.now()
    
    # Check if it's Monday
    is_monday = now.weekday() == 0  # Monday is 0
    
    # Check if it's around 9 AM (between 8:30 and 10:00)
    is_morning = 8 <= now.hour < 10
    
    return is_monday and is_morning

def show_reminder():
    """Show a reminder to run the weekly report"""
    print("=" * 60)
    print("📊 WEEKLY REPORT REMINDER")
    print("=" * 60)
    print("")
    print("It's Monday morning - time to run your weekly report!")
    print("")
    print("To run the report:")
    print("  1. Open Cursor")
    print("  2. Type: /weekly-update")
    print("")
    print("Or run manually:")
    print(f"  cd \"{script_dir}\"")
    print("  py process_and_send_weekly_report.py")
    print("")
    print("=" * 60)

if __name__ == '__main__':
    if should_run_report():
        show_reminder()
        print("\n🤔 Would you like to run the report now? (y/n): ", end='')
        try:
            response = input().strip().lower()
            if response == 'y':
                print("\n🚀 Running weekly report...\n")
                os.system(f'py "{os.path.join(script_dir, "process_and_send_weekly_report.py")}"')
            else:
                print("\n⏰ Reminder set. Run the report when ready!")
        except KeyboardInterrupt:
            print("\n\n⏸️  Cancelled.")
    else:
        print("ℹ️  Not the right time for weekly report.")
        print("   (Runs on Mondays between 8:30-10:00 AM)")

