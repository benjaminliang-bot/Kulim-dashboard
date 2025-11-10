# Update Kulim Dashboard Command

## 🚀 Quick Start

### Windows:
```bash
update-kulim
```

### Linux/Mac:
```bash
chmod +x update-kulim.sh
./update-kulim.sh
```

---

## 📋 What It Does

The `update-kulim` command automates the process of updating the Kulim dashboard:

1. **Generates SQL Query** - Creates the query to fetch latest Kulim commercial metrics
2. **Shows Query** - Displays the query for manual execution via MCP tools
3. **Updates HTML** - Updates `kulim_penang_comprehensive_analysis.html` with new data
4. **Git Operations** - Commits and pushes changes to GitHub (optional)

---

## 🔧 Usage

### Method 1: Manual Update (Recommended)

1. **Run the command:**
   ```bash
   update-kulim
   ```

2. **Copy the SQL query** that's displayed

3. **Execute via Hubble/Presto MCP tools** to get the latest data

4. **Update the HTML manually** or run the script again with data

### Method 2: Automated Update (with data)

If you have the query results as JSON:

```bash
update-kulim '{"202510": {"total_gmv": 568189.00, "completed_orders": 17968, ...}}'
```

---

## 📊 Query Details

The script uses:
- **Table:** `ocd_adw.f_food_metrics`
- **Area Filter:** `area_name = 'Kulim'` (exact match)
- **Order Counting:** `COUNT(DISTINCT order_id)`
- **Date Range:** September, October, November 2025

---

## 📁 Files Created

- `update_kulim.py` - Main Python script
- `update-kulim.bat` - Windows batch file
- `update-kulim.sh` - Linux/Mac shell script

---

## 🔄 Workflow

```
1. Run: update-kulim
   ↓
2. Execute SQL query via MCP tools
   ↓
3. Get results (JSON format)
   ↓
4. Update HTML manually OR run with data
   ↓
5. Commit & push to GitHub (optional)
```

---

## 📝 Example Data Format

```json
{
  "202509": {
    "total_gmv": 499340.10,
    "completed_orders": 15915,
    "active_merchants": 139,
    "unique_passengers": 8207,
    "avg_order_value": 31.38
  },
  "202510": {
    "total_gmv": 568189.00,
    "completed_orders": 17968,
    "active_merchants": 143,
    "unique_passengers": 8983,
    "avg_order_value": 31.62
  },
  "202511": {
    "total_gmv": 168853.68,
    "completed_orders": 5423,
    "active_merchants": 132,
    "unique_passengers": 3873,
    "avg_order_value": 31.14
  }
}
```

---

## ✅ Features

- ✅ Automatic SQL query generation
- ✅ HTML file update with latest metrics
- ✅ Git commit and push automation
- ✅ Cross-platform support (Windows/Linux/Mac)
- ✅ Error handling and validation

---

## 🔗 GitHub Integration

The script automatically:
- Updates `kulim_penang_comprehensive_analysis.html`
- Copies to `index.html` (for GitHub Pages)
- Commits with descriptive message
- Pushes to: https://github.com/benjaminliang-bot/Kulim-dashboard

---

## 💡 Tips

1. **Always review the query** before executing
2. **Verify the numbers** match your dashboard
3. **Test locally** before pushing to GitHub
4. **Check GitHub Pages** after pushing (takes 1-2 minutes to update)

