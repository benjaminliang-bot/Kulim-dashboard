"""Test date display formatting"""
from generate_weekly_queries_with_new_pax import get_week_dates
from datetime import datetime

dates = get_week_dates()

def parse_date(date_str):
    """Parse YYYYMMDD string to datetime"""
    return datetime.strptime(str(date_str), '%Y%m%d')

period_start = parse_date(dates['this_week_start'])
period_end = parse_date(dates['this_week_end'])
mom_start = parse_date(dates['same_week_last_month_start'])
mom_end = parse_date(dates['same_week_last_month_end'])
yoy_start = parse_date(dates['same_week_last_year_start'])
yoy_end = parse_date(dates['same_week_last_year_end'])

this_week_display = f"{period_start.strftime('%b %d')} - {period_end.strftime('%b %d')}"
same_week_last_month_display = f"{mom_start.strftime('%b %d')} - {mom_end.strftime('%b %d')}"
same_week_last_year_display = f"{yoy_start.strftime('%b %d')} - {yoy_end.strftime('%b %d')}"

print("=" * 60)
print("SLACK MESSAGE DATE DISPLAY")
print("=" * 60)
print(f"Period: {this_week_display}")
print(f"MoM: {same_week_last_month_display}")
print(f"YoY: {same_week_last_year_display}")
print()
print("Full context text:")
print(f"*Period:* {this_week_display} | *Comparisons:* MoM ({same_week_last_month_display}) & YoY ({same_week_last_year_display}) | *Generated:* {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 60)


