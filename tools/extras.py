# vendored from Trading/bridge/extras.py 2026-10-18 - do not edit here; edit the Trading copy and re-copy (see bridge/README.md "Sync")
"""extras.py - the extra prices.json blocks (v5, 18 Oct 2026). ONE source of truth for the Task Scheduler
copy (Trading/bridge/) and the GitHub Actions copy (geo-prices/tools/, vendored from this file).

Every public block function takes the watch.py module `W` (for dl/sub/contract_codes) where it needs
yfinance, returns a dict with its own `asof` and `fetched_utc`, and NEVER raises: on any failure the
value fields are null and `why` says what happened. No key is ever written to a file or an error string.
"""
import datetime as dt
import io
import json
import math
import os
import urllib.parse
import urllib.request

import pandas as pd

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0 Safari/537.36"}
PORTWATCH = ("https://services9.arcgis.com/weJ1QsnbMYJlCHdG/arcgis/rest/services/Daily_Chokepoints_Data/"
             "FeatureServer/0/query?where=portname%3D%27Strait+of+Hormuz%27&outFields=date,n_total,n_tanker"
             "&orderByFields=date+DESC&resultRecordCount=14&f=json")
GLD_CSV = "https://www.spdrgoldshares.com/assets/dynamic/GLD/GLD_US_archive_EN.csv"
GLD_XLSX = "https://api.spdrgoldshares.com/api/v1/historical-archive?exchange=NYSE&product=GLD&lang=en&fileType=xlsx"
EIA_SERIES = {"crude_stocks": ("PET.WCESTUS1.W", "thousand barrels"),
              "natgas_storage": ("NG.NW2_EPG0_SWO_R48_BCF.W", "Bcf")}


def _utc():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _r(x, n=2):
    try:
        x = float(x)
    except Exception:
        return None
    return round(x, n) if math.isfinite(x) else None


def _why(e, n=14):
    s = (str(e) or type(e).__name__).strip().replace("\n", " ")
    key = os.environ.get("EIA_KEY")
    if key:
        s = s.replace(key, "***")
    return " ".join(s.split()[:n])


def _get(url, timeout=20):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def safe(fn):
    """Run a block; on any exception return {asof None, fetched_utc, why}. Never raises."""
    def wrap(*a, **k):
        try:
            return fn(*a, **k)
        except Exception as e:  # noqa: BLE001 - the contract is "never raise"
            return {"asof": None, "fetched_utc": _utc(), "why": f"{fn.__name__} failed: {_why(e)}"}
    wrap.__name__ = fn.__name__
    return wrap


# ------------------------------------------------------------------ per-symbol
def max_range_60d(d, n=60):
    """max(High-Low) over the last n sessions of daily frame d (gate.py gap-aware sizing). None on failure."""
    try:
        rng = (d["High"] - d["Low"]).dropna().tail(n)
        return _r(rng.max(), 4) if len(rng) else None
    except Exception:
        return None


# ------------------------------------------------------------------ yfinance-based blocks
def _contract_closes(W, prefix):
    """[(symbol, last_close, last_date)] for the monthly contracts of `prefix`, oldest month first,
    expired ones (bar older than the group's newest) dropped. Reuses watch.contract_codes/dl/sub."""
    codes = W.contract_codes(prefix)
    df = W.dl(codes, period="10d")
    got = []
    for t in codes:
        d = W.sub(df, t)
        if d is None:
            continue
        c = d["Close"].dropna()
        if len(c):
            got.append((t.replace(".NYM", ""), float(c.iloc[-1]), c.index[-1].date()))
    if not got:
        return []
    newest = max(g[2] for g in got)
    return [g for g in got if g[2] >= newest]


@safe
def spreads(W):
    out = {"asof": None, "fetched_utc": _utc(), "unit": "$/bbl", "why": None}
    whys = []
    dates = []
    for prefix, key in (("BZ", "brent"), ("CL", "wti")):
        try:
            got = _contract_closes(W, prefix)
            if len(got) < 2:
                raise ValueError(f"{len(got)} contracts priced")
            m1, m2 = got[0], got[1]
            blk = {"contracts": [g[0] for g in got[:3]], "closes": [_r(g[1], 2) for g in got[:3]],
                   "bar_date": str(m1[2]), "m1_m2": _r(m1[1] - m2[1], 2), "m1_m3": None}
            if len(got) >= 3:
                blk["m1_m3"] = _r(m1[1] - got[2][1], 2)
            blk["structure"] = "backwardation" if m1[1] > m2[1] else "contango"
            dates.append(m1[2])
            out[key] = blk
        except Exception as e:
            out[key] = {"contracts": None, "closes": None, "bar_date": None, "m1_m2": None, "m1_m3": None,
                        "structure": None}
            whys.append(f"{key}: {_why(e)}")
    out["asof"] = str(min(dates)) if dates else None
    out["why"] = "; ".join(whys) or None
    return out


@safe
def crack_321(W):
    """3-2-1 crack = (2*RB*42 + 1*HO*42 - 3*CL)/3 in $/bbl, RB/HO quoted $/gal."""
    out = {"asof": None, "fetched_utc": _utc(), "unit": "$/bbl", "value": None, "rb": None, "ho": None,
           "cl": None, "why": None}
    df = W.dl(["RB=F", "HO=F", "CL=F"], period="10d")
    cl = {s: W.sub(df, s)["Close"].dropna() if W.sub(df, s) is not None else None for s in ("RB=F", "HO=F", "CL=F")}
    miss = [s for s, v in cl.items() if v is None or v.empty]
    if miss:
        out["why"] = "no data: " + ",".join(miss)
        return out
    both = pd.concat(cl, axis=1).dropna()
    if both.empty:
        out["why"] = "no common session for RB=F, HO=F, CL=F"
        return out
    row = both.iloc[-1]
    rb, ho, c = float(row["RB=F"]), float(row["HO=F"]), float(row["CL=F"])
    out.update(asof=str(both.index[-1].date()), rb=_r(rb, 4), ho=_r(ho, 4), cl=_r(c, 2),
               value=_r((2 * rb * 42 + ho * 42 - 3 * c) / 3, 2))
    return out


# ------------------------------------------------------------------ plain-HTTP blocks
@safe
def gld_tonnes():
    out = {"asof": None, "fetched_utc": _utc(), "tonnes": None, "chg_1d": None, "source": None, "why": None}
    df, src = None, None
    try:  # 1) the documented CSV (answered a PDF on 18 Oct 2026, so verify it really is text)
        raw = _get(GLD_CSV)
        if raw[:4] == b"%PDF" or b"," not in raw[:2000]:
            raise ValueError("CSV url returned non-CSV (" + ("PDF" if raw[:4] == b"%PDF" else "no commas") + ")")
        df, src = pd.read_csv(io.BytesIO(raw), header=None, on_bad_lines="skip", engine="python"), "csv"
    except Exception as e1:
        try:  # 2) the xlsx the SPDR site itself links to
            df, src = pd.read_excel(io.BytesIO(_get(GLD_XLSX, 40)), sheet_name=-1, header=None), "xlsx"
        except Exception as e2:
            out["why"] = f"csv: {_why(e1, 8)}; xlsx: {_why(e2, 8)}"
            return out
    hdr = None
    for i in range(min(len(df), 30)):
        if any(str(v).strip().lower().startswith("tonnes of gold") for v in df.iloc[i].values):
            hdr = i
            break
    if hdr is None:
        out["why"] = f"{src}: no 'Tonnes of Gold' header row"
        return out
    cols = [str(v).strip().lower() for v in df.iloc[hdr].values]
    ti = next(i for i, c in enumerate(cols) if c.startswith("tonnes of gold"))
    body = df.iloc[hdr + 1:, [0, ti]].copy()
    body.columns = ["d", "t"]
    body["d"] = pd.to_datetime(body["d"], errors="coerce", format="mixed")
    body["t"] = pd.to_numeric(body["t"], errors="coerce")
    body = body.dropna()
    if body.empty:
        out["why"] = f"{src}: no parsable data rows"
        return out
    out.update(asof=str(body["d"].iloc[-1].date()), tonnes=_r(body["t"].iloc[-1], 2), source=src)
    if len(body) > 1:
        out["chg_1d"] = _r(body["t"].iloc[-1] - body["t"].iloc[-2], 2)
    return out


@safe
def hormuz_7d():
    out = {"asof": None, "fetched_utc": _utc(), "n_total": None, "n_tanker": None, "mean_7d": None,
           "mean_14d": None, "n_rows": 0, "why": None}
    j = json.loads(_get(PORTWATCH))
    feats = j.get("features") or []
    rows = []
    for f in feats:
        a = f.get("attributes", {})
        d = a.get("date")
        if isinstance(d, (int, float)):
            d = dt.datetime.fromtimestamp(d / 1000, dt.timezone.utc).strftime("%Y-%m-%d")
        if d is not None and a.get("n_total") is not None:
            rows.append((str(d)[:10], float(a["n_total"]), a.get("n_tanker")))
    if not rows:
        out["why"] = "PortWatch returned 0 rows: " + _why(j.get("error", "empty"), 10)
        return out
    rows.sort(reverse=True)
    out.update(asof=rows[0][0], n_total=int(rows[0][1]), n_rows=len(rows),
               n_tanker=None if rows[0][2] is None else int(rows[0][2]),
               mean_7d=_r(sum(r[1] for r in rows[:7]) / len(rows[:7]), 2) if len(rows) >= 7 else None,
               mean_14d=_r(sum(r[1] for r in rows[:14]) / 14, 2) if len(rows) >= 14 else None)
    if len(rows) < 14:
        out["why"] = f"only {len(rows)} rows: mean_14d null"
    return out


@safe
def eia_weekly():
    key = os.environ.get("EIA_KEY", "").strip()
    out = {"asof": None, "fetched_utc": _utc(), "crude_stocks": None, "natgas_storage": None, "why": None}
    if not key:
        out["why"] = "EIA_KEY not set"
        return out
    whys, dates = [], []
    for name, (sid, unit) in EIA_SERIES.items():
        try:
            url = ("https://api.eia.gov/v2/seriesid/" + sid + "?" +
                   urllib.parse.urlencode({"api_key": key, "length": 2, "sort[0][column]": "period",
                                           "sort[0][direction]": "desc"}))
            data = json.loads(_get(url, 25))["response"]["data"]
            if not data:
                raise ValueError("0 rows")
            v0 = float(data[0]["value"])
            v1 = float(data[1]["value"]) if len(data) > 1 else None
            out[name] = {"series": sid, "unit": unit, "period": data[0]["period"], "value": _r(v0, 1),
                         "prior": _r(v1, 1), "change": _r(v0 - v1, 1) if v1 is not None else None}
            dates.append(data[0]["period"])
        except Exception as e:
            whys.append(f"{name}: {_why(e, 10)}")
    out["asof"] = min(dates) if dates else None
    out["why"] = "; ".join(whys) or None
    return out


def all_blocks(W):
    """Run every extra block. yfinance-based ones run sequentially (yf.download shares state across threads);
    each returns its own dict. Keys are the top-level prices.json keys."""
    return {"spreads": spreads(W), "crack_321": crack_321(W), "gld_tonnes": gld_tonnes(),
            "hormuz_7d": hormuz_7d(), "eia_weekly": eia_weekly()}
