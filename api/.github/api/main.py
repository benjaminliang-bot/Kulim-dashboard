import os, io, re
import pandas as pd
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from google.oauth2 import service_account
from googleapiclient.discovery import build

FOLDER_ID = os.getenv("DRIVE_FOLDER_ID")  # the SKU_ELIGIBILITY folder id
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

# Auth to Drive
def drive_svc():
    creds_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
    if not creds_json:
        raise RuntimeError("Missing GOOGLE_APPLICATION_CREDENTIALS_JSON")
    creds = service_account.Credentials.from_service_account_info(
        eval(creds_json), scopes=SCOPES
    )
    return build("drive", "v3", credentials=creds)

app = FastAPI()

class Req(BaseModel):
    city: str
    q: str
    merchant: str | None = None
    am: str | None = None

def city_to_filename(city: str) -> str:
    slug = city.strip().lower().replace(" ", "_")
    return f"{slug}_eligibility.csv"

def load_city_csv(city: str) -> pd.DataFrame:
    filename = city_to_filename(city)
    svc = drive_svc()
    # find file by name in the folder
    q = f"name='{filename}' and '{FOLDER_ID}' in parents and trashed=false"
    res = svc.files().list(q=q, fields="files(id,name)").execute()
    files = res.get("files", [])
    if not files:
        raise HTTPException(404, f"No dataset for city: {city}")
    file_id = files[0]["id"]
    data = svc.files().get_media(fileId=file_id).execute()
    df = pd.read_csv(io.BytesIO(data))
    # normalize for safe matching
    for col in ["merchant_id","item_id","item_name","am_name","item_status"]:
        if col in df.columns:
            df[col] = df[col].astype(str)
    return df

def make_regex(query: str) -> str:
    if query.isdigit(): return None
    toks = [re.escape(t) for t in re.split(r"\s+", query.strip().lower()) if t]
    return "".join([f"(?=.*{t})" for t in toks]) + ".*"

@app.post("/skucheck")
def skucheck(r: Req):
    if not r.city or not r.q:
        raise HTTPException(400, "city and q required")
    if not (r.merchant or r.am):
        raise HTTPException(400, "merchant or am required")

    df = load_city_csv(r.city)

    # scope by merchant or AM
    if r.merchant:
        df = df[df["merchant_id"].str.lower() == r.merchant.strip().lower()]
    if r.am:
        df = df[df["am_name"].str.lower() == r.am.strip().lower()]

    # match by id or name tokens
    q = r.q.strip().lower()
    if q.isdigit():
        df = df[df["item_id"].str.lower() == q]
    else:
        pat = make_regex(q)
        df = df[df["item_name"].str.lower().str.contains(pat, regex=True, na=False)]

    # compute eligibility
    df["eligible_for_submission"] = (df["item_status"].str.upper()=="ACTIVE") & (~df["in_campaign"].astype(bool))
    df["reason"] = df.apply(
        lambda x: "Already in campaign" if bool(x["in_campaign"])
        else ("Item not ACTIVE on menu" if str(x["item_status"]).upper()!="ACTIVE"
              else "Eligible"),
        axis=1
    )

    cols = ["item_id","item_name","item_status","in_campaign","eligible_for_submission",
            "reason","am_name","merchant_id","city_id","lm_order_count","lm_pax_count","as_of_date"]
    out_cols = [c for c in cols if c in df.columns]
    out = df[out_cols].head(10)

    return {"count": len(out), "results": out.to_dict(orient="records")}
