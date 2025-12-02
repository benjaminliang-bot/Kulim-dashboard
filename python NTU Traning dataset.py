# ============================================
# NTU Uplift Focus — Merchant ranking by promo-driven NEW users
# Works with or without PyTorch (falls back to scikit-learn)
# Input:
#   C:\Users\benjamin.liang\Downloads\_NTU_training_dataset_weekly_merchant_window_Penang_COMPLETED_on_202509121144.csv
# Outputs:
#   C:\Users\benjamin.liang\Downloads\mex_ntu_focus_rows.csv
#   C:\Users\benjamin.liang\Downloads\mex_ntu_focus_merchants.csv
# ============================================

import os, sys, warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd

# ---------- TRY TORCH, else fallback ----------
USE_TORCH = True
try:
    import torch
    import torch.nn as nn
    from torch.utils.data import Dataset, DataLoader
except Exception:
    USE_TORCH = False
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor

# ---------- CONFIG ----------
DIR   = r"C:\Users\benjamin.liang\Downloads"
FNAME = r"_NTU_training_dataset_weekly_merchant_window_Penang_COMPLETED_on_202509171306"
CSV   = os.path.join(DIR, FNAME if FNAME.lower().endswith(".csv") else FNAME + ".csv")
OUT_ROWS = os.path.join(DIR, "mex_ntu_focus_rows.csv")
OUT_MEX  = os.path.join(DIR, "mex_ntu_focus_merchants.csv")

TARGET_NTU    = "ntu_next_week"
TARGET_ORDERS = "orders_next_week"
TOPN_PER_WINDOW = 20

NUM_COLS = [
    "orders","gmv","promo_expense","subsidy",
    "avg_order_value","avg_basket_size",
    "avg_prep_time","p95_prep_time",
    "group_order_share",
    "orders_l4w","gmv_l4w","promo_spend_l4w",
    "new_user_share_l4w","ntu_l4w",
    "days_since_last_promo"
]

# ---------- LOAD ----------
if not os.path.exists(CSV):
    raise FileNotFoundError(f"File not found: {CSV}")

df = pd.read_csv(
    CSV,
    na_values=["NULL","[NULL]","na","NA","None",""],
    keep_default_na=True,
    thousands=","
)

req = {"merchant_id","week_start","window","action",TARGET_ORDERS}
missing = req - set(df.columns)
if missing:
    raise ValueError(f"Missing columns: {missing}")

has_true_ntu = (TARGET_NTU in df.columns)

df["week_start"] = pd.to_datetime(df["week_start"], errors="coerce")
df = df[df["week_start"].notna()].copy()
df["window"] = df["window"].astype(str).str.upper()
df = df[df["window"].isin(["LUNCH","DINNER"])].copy()
df["action"] = pd.to_numeric(df["action"], errors="coerce").fillna(0).astype(int)
df = df[df["action"].isin([0,1])].copy()

for c in (set(NUM_COLS) | {TARGET_ORDERS, TARGET_NTU}):
    if c not in df.columns:
        df[c] = 0.0
    df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0.0)

# ---------- TIME SPLIT ----------
weeks = sorted(df["week_start"].unique())
if len(weeks) < 6:
    c1 = max(int(len(weeks)*0.7), 1)
    c2 = max(int(len(weeks)*0.85), min(len(weeks)-1, c1+1))
    train_weeks, val_weeks, test_weeks = weeks[:c1], weeks[c1:c2], weeks[c2:] or weeks[-1:]
else:
    train_weeks, val_weeks, test_weeks = weeks[:-4], weeks[-4:-1], weeks[-1:]

def take(d, wk): return d[d["week_start"].isin(wk)].copy()
train, val, test = take(df, train_weeks), take(df, val_weeks), take(df, test_weeks)
if test.empty: test = take(df, [weeks[-1]])

# ---------- ENCODING / SCALING ----------
def fit_indexer(series):
    cats = sorted(pd.Series(series.dropna().unique()).tolist())
    return {c:i for i,c in enumerate(cats)} or {}

win2id = fit_indexer(train["window"]) or {"LUNCH":0,"DINNER":1}
mid2id = fit_indexer(train["merchant_id"]) or {m:i for i,m in enumerate(sorted(df["merchant_id"].unique()))}

def map_cat(s, m): return s.map(m).fillna(-1).astype(int)
for d in (train, val, test):
    d["win_id"] = map_cat(d["window"], win2id)
    d["mid_id"] = map_cat(d["merchant_id"], mid2id)

scaler = StandardScaler().fit(train[NUM_COLS]) if len(train)>0 else StandardScaler().fit(df[NUM_COLS])
for d in (train, val, test):
    d[NUM_COLS] = scaler.transform(d[NUM_COLS])

# ---------- MODELING ----------
def _predict_sklearn(model, Xn, Xc):
    X = np.hstack([Xn, Xc])
    return model.predict(X)

if USE_TORCH:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    class TabDS(Dataset):
        def __init__(self, df_, target_col):
            self.Xn = torch.tensor(df_[NUM_COLS].values, dtype=torch.float32)
            self.Xc = torch.tensor(df_[["win_id","mid_id"]].values, dtype=torch.long)
            self.y  = torch.tensor(df_[target_col].values, dtype=torch.float32)
        def __len__(self): return len(self.y)
        def __getitem__(self, i): return self.Xn[i], self.Xc[i], self.y[i]
    class MLP(nn.Module):
        def __init__(self, cat_cardinals, n_num, hidden=(128,64)):
            super().__init__()
            self.embs, dims = nn.ModuleList(), []
            for c in cat_cardinals:
                dim = 1 if c <= 1 else min(50, (c+1)//2)
                self.embs.append(nn.Embedding(max(c,1), dim)); dims.append(dim)
            self.mlp = nn.Sequential(
                nn.Linear(n_num + sum(dims), hidden[0]), nn.ReLU(),
                nn.BatchNorm1d(hidden[0]),
                nn.Linear(hidden[0], hidden[1]), nn.ReLU(),
                nn.Linear(hidden[1], 1)
            )
        def forward(self, xn, xc):
            es = []
            for i, emb in enumerate(self.embs):
                idx = torch.clamp(xc[:,i], min=0)
                es.append(emb(idx))
            ecat = torch.cat(es, dim=1) if es else torch.zeros((xn.size(0),0), device=xn.device)
            x = torch.cat([xn, ecat], dim=1)
            return self.mlp(x).squeeze(1)
    def train_regressor_torch(tr_df, va_df, target_col, epochs=40, patience=6, lr=1e-3, bs_tr=256, bs_va=512):
        tr, va = TabDS(tr_df, target_col), TabDS(va_df, target_col)
        dl_tr = DataLoader(tr, batch_size=bs_tr, shuffle=True)
        dl_va = DataLoader(va, batch_size=bs_va, shuffle=False)
        model = MLP([len(win2id), len(mid2id)], n_num=len(NUM_COLS)).to(device)
        opt = torch.optim.Adam(model.parameters(), lr=lr)
        crit = nn.SmoothL1Loss(beta=1.0)
        best, best_state, pat = 1e30, None, patience
        for _ in range(epochs):
            model.train()
            for xn, xc, y in dl_tr:
                xn, xc, y = xn.to(device), xc.to(device), y.to(device)
                opt.zero_grad(); loss = crit(model(xn, xc), y); loss.backward(); opt.step()
            model.eval()
            vlosses = []
            with torch.no_grad():
                for xn, xc, y in dl_va:
                    xn, xc, y = xn.to(device), xc.to(device), y.to(device)
                    vlosses.append(crit(model(xn, xc), y).item())
            v = float(np.mean(vlosses)) if vlosses else best
            if v < best:
                best, best_state, pat = v, {k: p.detach().cpu().clone() for k,p in model.state_dict().items()}, patience
            else:
                pat -= 1
                if pat <= 0: break
        if best_state is not None: model.load_state_dict(best_state)
        return model
    def predict_torch(model, df_):
        Xn = torch.tensor(df_[NUM_COLS].values, dtype=torch.float32).to(device)
        Xc = torch.tensor(df_[["win_id","mid_id"]].values, dtype=torch.long).to(device)
        model.eval(); out = []
        with torch.no_grad():
            for i in range(0, len(df_), 512):
                out.append(model(Xn[i:i+512], Xc[i:i+512]).detach().cpu().numpy())
        return np.concatenate(out) if out else np.array([])

def train_T_learner(train_df, val_df, action_val, target_col):
    sub_tr = train_df[train_df["action"]==action_val].copy()
    sub_va = val_df[val_df["action"]==action_val].copy()
    if len(sub_tr) == 0:
        return None
    if USE_TORCH:
        return train_regressor_torch(sub_tr, sub_va, target_col)
    else:
        Xtr = np.hstack([sub_tr[NUM_COLS].values, sub_tr[["win_id","mid_id"]].values])
        ytr = sub_tr[target_col].values
        model = RandomForestRegressor(n_estimators=400, max_depth=None, random_state=42, n_jobs=-1)
        model.fit(Xtr, ytr)
        return model

def predict_any(model, df_):
    if model is None or len(df_)==0:
        return np.zeros(len(df_), dtype=float)
    if USE_TORCH:
        return predict_torch(model, df_)
    else:
        return _predict_sklearn(model, df_[NUM_COLS].values, df_[["win_id","mid_id"]].values)

# ---------- TRAIN ----------
if has_true_ntu:
    f0_ntu = train_T_learner(train, val, 0, TARGET_NTU)
    f1_ntu = train_T_learner(train, val, 1, TARGET_NTU)
else:
    f0_ntu = f1_ntu = None
f0_ord = train_T_learner(train, val, 0, TARGET_ORDERS)
f1_ord = train_T_learner(train, val, 1, TARGET_ORDERS)

# ---------- INFERENCE (latest week) ----------
latest_week = test["week_start"].max()
cand = test[test["week_start"]==latest_week].copy()
if cand.empty:
    latest_week = df["week_start"].max()
    cand = df[df["week_start"]==latest_week].copy()
cand = cand.reset_index(drop=True)

y0o = predict_any(f0_ord, cand)
y1o = predict_any(f1_ord, cand)
orders_uplift = np.maximum(0.0, y1o - y0o)

if has_true_ntu and (f0_ntu is not None) and (f1_ntu is not None):
    y0n = predict_any(f0_ntu, cand)
    y1n = predict_any(f1_ntu, cand)
    ntu_uplift_model = y1n - y0n
else:
    ntu_uplift_model = np.zeros(len(cand), dtype=float)

nus = cand["new_user_share_l4w"].values
nus = np.where(np.isfinite(nus) & (nus>0), nus, 0.20)
ntu_uplift_fallback = orders_uplift * nus

ntu_uplift = np.where(ntu_uplift_model > ntu_uplift_fallback, ntu_uplift_model, ntu_uplift_fallback)
ntu_uplift = np.where(ntu_uplift > 0, ntu_uplift, 0.0)

ppo = (cand["promo_spend_l4w"].values / np.maximum(cand["orders_l4w"].values, 1.0))
ppo = np.clip(ppo, 0.0, np.nanpercentile(ppo, 95) if len(ppo)>0 else 100.0)
expected_promo_spend = np.maximum(1.0, ppo * np.maximum(orders_uplift, 1.0))

ntu_per_rm = np.where(expected_promo_spend>0, ntu_uplift/expected_promo_spend, 0.0)

cand["ntu_uplift"] = ntu_uplift
cand["expected_incremental_orders"] = orders_uplift
cand["expected_promo_spend"] = expected_promo_spend
cand["ntu_per_rm"] = ntu_per_rm

cand["focus"] = "N"
for w in cand["window"].unique():
    take = cand[cand["window"]==w]
    k = min(TOPN_PER_WINDOW, len(take))
    if k > 0:
        idx = take.nlargest(k, "ntu_per_rm").index
        cand.loc[idx, "focus"] = "Y"

eff_med  = np.nanmedian(cand["ntu_per_rm"]) if len(cand)>0 else 0
prep_p70 = np.nanpercentile(cand["p95_prep_time"], 70) if len(cand)>0 else 0
dsp_med  = np.nanmedian(cand["days_since_last_promo"]) if len(cand)>0 else 0
promo_p70= np.nanpercentile(cand["promo_spend_l4w"], 70) if len(cand)>0 else 0

def build_why(r):
    bits = []
    if r["ntu_uplift"] > 0: bits.append("positive NTU uplift")
    if r["ntu_per_rm"] >= eff_med: bits.append("NTU/RM ≥ median")
    if r["days_since_last_promo"] >= dsp_med: bits.append("cool-off elapsed")
    if r["promo_spend_l4w"] > promo_p70: bits.append("recent promo saturation")
    if r["p95_prep_time"] > prep_p70: bits.append("ops risk: high prep time")
    if not bits: bits.append("weak NTU uplift / efficiency")
    out, seen = [], set()
    for b in bits:
        if b not in seen: out.append(b); seen.add(b)
    return "; ".join(out)

cand["why"] = cand.apply(build_why, axis=1)
cand["rank_in_window"] = cand.groupby("window")["ntu_per_rm"].rank(ascending=False, method="first")

row_cols = [
    "focus","why","merchant_id","week_start","window",
    "ntu_uplift","ntu_per_rm",
    "expected_incremental_orders","expected_promo_spend",
    "orders","orders_l4w","promo_spend_l4w","new_user_share_l4w","days_since_last_promo","p95_prep_time",
    "rank_in_window"
]
for c in row_cols:
    if c not in cand.columns: cand[c] = np.nan
rows_out = cand.sort_values(["window","focus","ntu_per_rm"], ascending=[True, False, False])[row_cols].reset_index(drop=True)
rows_out.to_csv(OUT_ROWS, index=False, encoding="utf-8-sig")

def pick_best(g):
    g = g.sort_values("ntu_per_rm", ascending=False)
    top = g.iloc[0]
    return pd.Series({
        "best_window": top["window"],
        "best_week": top["week_start"],
        "ntu_per_rm": top["ntu_per_rm"],
        "ntu_uplift": top["ntu_uplift"],
        "expected_promo_spend": top["expected_promo_spend"],
        "expected_incremental_orders": top["expected_incremental_orders"],
        "focus_any": "Y" if (g["focus"]=="Y").any() else "N",
        "why": top["why"]
    })

mex = cand.groupby("merchant_id", as_index=False).apply(pick_best)
mex = mex.sort_values("ntu_per_rm", ascending=False).reset_index(drop=True)
mex["rank_overall"] = np.arange(1, len(mex)+1)
mex_cols = ["rank_overall","merchant_id","best_window","best_week","ntu_per_rm","ntu_uplift","expected_incremental_orders","expected_promo_spend","focus_any","why"]
mex[mex_cols].to_csv(OUT_MEX, index=False, encoding="utf-8-sig")

print("\n=== NTU FOCUS — latest week:", pd.to_datetime(latest_week).date() if pd.notna(latest_week) else latest_week, "===")
print("\nTop 15 merchants by NTU per RM:")
print(mex[mex_cols].head(15).to_string(index=False))
print(f"\nSaved rows → {OUT_ROWS}")
print(f"Saved merchants → {OUT_MEX}\n")
