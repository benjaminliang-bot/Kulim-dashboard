# Quick Update Guide - update-kulim Command

## 🚀 Quick Command

### Windows:
```bash
update-kulim
```

### Linux/Mac:
```bash
./update-kulim.sh
```

---

## 📋 What It Does

1. **Shows SQL Query** - Displays the query to execute via MCP tools
2. **Updates HTML** - Updates dashboard with new metrics (if data provided)
3. **Git Push** - Commits and pushes to GitHub (optional)

---

## 🔄 Typical Workflow

### Step 1: Run the command
```bash
update-kulim
```

### Step 2: Copy the SQL query shown

### Step 3: Execute via Hubble/Presto MCP
- Use the `mcp_mcp-hubble_run_presto_query` tool
- Or execute in your Presto/Hubble environment

### Step 4: Update HTML with results
- Option A: Manually update `kulim_penang_comprehensive_analysis.html`
- Option B: Run script with JSON data (see below)

### Step 5: Push to GitHub (optional)
```bash
git add kulim_penang_comprehensive_analysis.html index.html
git commit -m "Update Kulim dashboard"
git push
```

---

## 📊 Query Details

- **Area:** `area_name = 'Kulim'` (exact match)
- **Order Counting:** `COUNT(DISTINCT order_id)`
- **Table:** `ocd_adw.f_food_metrics`
- **Months:** September, October, November 2025

---

## ✅ Files

- `update_kulim.py` - Main script
- `update-kulim.bat` - Windows command
- `update-kulim.sh` - Linux/Mac command

---

## 💡 Tips

- Run `update-kulim` anytime to get the latest query
- The query uses the correct area definition and DISTINCT counting
- Always verify numbers match your dashboard before pushing

