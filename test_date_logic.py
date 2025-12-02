"""Test the updated date logic"""
from generate_weekly_queries_with_new_pax import get_week_dates
from datetime import datetime, timedelta

dates = get_week_dates()
today = datetime.now()

print("=" * 60)
print("DATE LOGIC TEST")
print("=" * 60)
print(f"Today: {today.strftime('%Y-%m-%d %A')}")
print()
print("Period (current_date -1 to -8):")
print(f"  Start: {dates['this_week_start']} (8 days ago)")
print(f"  End:   {dates['this_week_end']} (yesterday)")
print()
print("MoM Comparison (same dates, previous month):")
print(f"  Start: {dates['same_week_last_month_start']}")
print(f"  End:   {dates['same_week_last_month_end']}")
print()
print("YoY Comparison (same dates, previous year):")
print(f"  Start: {dates['same_week_last_year_start']}")
print(f"  End:   {dates['same_week_last_year_end']}")
print()
print("=" * 60)


