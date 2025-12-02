# Export Penang Mainland Merchants to CSV

This guide explains how to automatically export all Penang Mainland merchants to a CSV file with readable cuisine names.

## Quick Start

The query has already been executed and returned all merchants with readable cuisine names (e.g., "Beverages, Fast Food, Halal" instead of IDs).

### Option 1: Automatic (Recommended)

1. **Save the query output:**
   - Copy the FULL query output from the MCP tool result (starts with `| merchant_id_nk | merchant_name | ...`)
   - Run: `python save_query_output.py`
   - Paste the query output when prompted
   - Press Enter twice when done

2. **Generate CSV automatically:**
   - Run: `python auto_export_merchants.py`
   - The script will automatically read `query_output.txt` and create `penang_mainland_merchants.csv`

### Option 2: One-Step Process

1. Run: `python auto_export_merchants.py`
2. When prompted, paste the query output
3. Press Enter twice when done
4. The CSV will be created automatically

## Files Created

- `penang_mainland_merchants.csv` - Complete list of all merchants with:
  - Merchant ID and name
  - Area name
  - Halal status
  - **Readable cuisine names** (comma-separated)
  - Segment, custom segment, AM name
  - Last order date
  - Merchant status (Active/Churned/Never Ordered)

## What's Included

The CSV includes **all active merchants** from Penang Mainland areas with:
- ✅ Full merchant list (hundreds of merchants)
- ✅ Human-readable cuisine names (not IDs)
- ✅ All relevant merchant information
- ✅ Properly formatted for Excel

## Notes

- The query output should include the header row and all data rows
- The output should end with `*Execution time: X.XXs`
- The script automatically handles parsing and CSV creation
- The CSV file is UTF-8 encoded and ready for Excel

