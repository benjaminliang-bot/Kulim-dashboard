A README is the front-page of your repo. It tells anyone (including future-you) **what this project is, how to run it, and where the important bits are**. For your SKU Checker, here’s a ready-to-use README you can paste into GitHub.

---

# SKU Checker

Fast lookup to validate if a SKU is **eligible for campaign** before submission. AMs query by `item_id` or name fragment, scoped by **city + merchant/AM**. Output shows `item_status`, `in_campaign`, and an **eligibility verdict** with reason.

## Why this exists

* Sheets or ad-hoc SQL with 800k rows is painful.
* This repo keeps one source of truth (SQL + scripts) and lets us automate refresh and expose a Slack `/skucheck` command.

## How it works (high level)

1. **Warehouse job** builds a skinny table `tools.item_eligibility` (daily/hourly).
2. Table stores: `city_id, merchant_id_v, item_id_v, item_name, am_name, item_status, in_campaign, last_seen_date_id, as_of_date`.
3. **Checker** (Sheet or Slack) queries this table with tight filters and returns ≤10–25 matches + eligibility reasons.

## Repo layout

```
sql/
  00_create_item_eligibility_trino.sql   # one-time CTAS to create the table
  10_refresh_item_eligibility_trino.sql  # daily INSERT/REFRESH
api/                                     # (optional) Slack checker service
  main.py
  requirements.txt
  Dockerfile
.github/workflows/                       # (optional) automations
  refresh.yml                            # nightly refresh via Trino CLI
  deploy-api.yml                         # deploy API (e.g., Cloud Run)
ops/
  trino.properties.example               # connection template
  slack.env.example                      # Slack/API env examples
README.md
```

## Prerequisites

* Access to Trino/Presto (catalog: `hive`) and schemas `ocd_adw`, `tools`.
* Tables: `f_food_order_detail`, `d_merchant`, `d_menu_item`, `d_campaign_eligible_item`, `d_date`.
* DBeaver installed (for manual runs).
* Optional: GitHub Actions runner that can reach Trino; Slack workspace for slash command.

## Quick start (manual, simplest)

1. Open **DBeaver** → connect to Trino (`hive` catalog).
2. Run `sql/00_create_item_eligibility_trino.sql` once.
3. Daily: run `sql/10_refresh_item_eligibility_trino.sql` to refresh the latest data.
4. Point your **Google Sheet checker** or **Slack command** at `tools.item_eligibility`.

## Using the Google Sheet checker (no server needed)

* Build a “Checker” sheet with inputs: `city_id`, `merchant_id` or `am_name`, and query `q`.
* Use the single-cell formula I gave earlier (LET+FILTER) or the Apps Script `=CHECK_SKU(...)` if you want BigQuery backing.
* Result shows: `item_id, item_name, item_status, in_campaign, eligible_for_submission, reason`.

## Optional: Slack `/skucheck`

* Tiny FastAPI service in `api/` that reads from the skinny table (or BigQuery mirror).
* Slash command syntax:

  ```
  /skucheck city=4 merchant=123 q=987654321
  /skucheck city=4 am="Alice Tan" q="spicy chicken"
  ```
* Returns top 10 matches with a clear badge: ✅ Eligible or ⚠️ Reason.

## Automation (optional but nice)

* `.github/workflows/refresh.yml` runs the daily refresh automatically.
* Add secrets in GitHub → Settings → Actions: `TRINO_HOST`, `TRINO_PORT`, `TRINO_USER`, `TRINO_PASSWORD`.
* If Trino is private, use a **self-hosted runner** inside your network; otherwise keep doing DBeaver manual refresh.

## Data rules (so results are trustworthy)

* **Scope campaign** by **(merchant_id, item_id)**, not item alone.
* Normalize all IDs to **text** (`*_v` columns) to avoid type mismatches.
* Prefer **menu status** as truth for “ACTIVE”; only fall back to order-seen status if menu is missing.
* Require **city + merchant/AM** in queries to avoid noisy name matches.

## Troubleshooting

* **Query slow?** Ensure your skinny table is partitioned by `city_id, as_of_date`. Query only latest `as_of_date`.
* **Wrong answers?** Check that campaign join includes **merchant_id** and that IDs are consistently text.
* **Sheet laggy?** Force inputs (city + merchant/AM) and cap results to ≤25.

## Roadmap

* Add Redis cache for hottest lookups.
* Add reason codes beyond ACTIVE/campaign (e.g., price-test missing, policy block).
* Add `/skucheck help` in Slack and a small audit log (top queries, miss rate).

## Glossary

* **Repo**: this project folder on GitHub with version history.
* **CTAS**: “Create Table As Select” — one-time build of the skinny table.
* **Refresh**: daily insert/update to keep data current.
* **Eligibility**: `item_status='ACTIVE'` AND not already in campaign.

