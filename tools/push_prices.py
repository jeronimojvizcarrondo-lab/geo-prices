# vendored from Trading/bridge/push_prices.py 2026-10-18 - do not edit here; edit the Trading copy and re-copy (see bridge/README.md "Sync")
"""push_prices.py - compute the geo-watch price layer locally and publish it as prices.json.

    python bridge/push_prices.py             # compute, write to the geo-prices checkout, git commit + push
    python bridge/push_prices.py --dry-run   # compute, write bridge/prices.json, print a table, no git
    python bridge/push_prices.py --out DIR   # use DIR instead of the default checkout
    python bridge/push_prices.py --out . --no-git   # write DIR/prices.json only (GitHub Actions does the commit)

Reuses the maths in skills/geo-watch/watch.py (imported, not copied) and the v5 extra blocks in extras.py
(spreads, crack_321, gld_tonnes, hormuz_7d, eia_weekly, per-symbol max_range_60d). The same file runs from
geo-prices/tools/ (Actions cron, where watch.py and extras.py sit next to it). No token is read or stored:
git uses whatever credential helper / SSH key is already configured; EIA_KEY comes from the environment only.
Only prices.json is committed.
"""
import argparse
import datetime as dt
import json
import logging
import math
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "skills" / "geo-watch"))  # Trading checkout; absent in geo-prices (watch.py sits in HERE)
sys.path.insert(0, str(HERE))

import extras as X  # noqa: E402  (one source of truth for the v5 fields)
import watch as W  # noqa: E402  (module prints nothing on import; main() is guarded)

logging.getLogger("yfinance").setLevel(logging.CRITICAL)

SYMBOLS = ["BZ=F", "FRO", "HG=F", "ZC=F", "ZW=F", "GC=F", "SI=F", "NG=F", "EWZ", "SPY",
           "BNO", "SCO", "GLD", "CPER", "COPX", "CORN", "WEAT", "UNG", "SLV"]  # last nine = exec ETFs (added 16 Oct)
FRED = [("DFII10", "10y real yield (%)"), ("VIXCLS", "VIX"), ("OVXCLS", "OVX"),
        ("GVZCLS", "GVZ"), ("DTWEXBGS", "Broad dollar index")]
DEFAULT_DIR = Path(r"C:\CLAUDE CODE DESKTOP\geo-prices")
LOG = HERE / "push_log.txt"

SETUP = """geo-prices checkout not found (no .git in {d}).
One-time setup (run by hand, see bridge/README.md):
  1. github.com -> New repository -> name geo-prices -> PUBLIC, no README.
  2. winget install --id GitHub.cli -e
     gh auth login --web --git-protocol https
  3. mkdir "{d}"  &&  cd "{d}"
     git init -b main
     git remote add origin https://github.com/jeronimojvizcarrondo-lab/geo-prices.git
     git config user.name "<your name>"
     git config user.email "<your email>"
  4. python bridge/push_prices.py   (once, by hand)
  5. schtasks /Create /TN "geo-prices-bridge" /XML "{x}"
"""


def r(x, n):
    try:
        x = float(x)
    except Exception:
        return None
    return round(x, n) if math.isfinite(x) else None


def pdec(x):
    """price decimals: 4 below 10, else 2"""
    return 4 if x is not None and abs(x) < 10 else 2


def bars4h(h1):
    c = h1["Close"].dropna()
    return c.resample("4h", label="left", closed="left").last().dropna()


def one_symbol(sym, daily, h1, derr, herr):
    d = W.sub(daily, sym) if daily is not None else None
    if d is None or "Close" not in d or d["Close"].dropna().empty:
        raise ValueError(W.short(derr, 6) if derr else "no daily data")
    d = d.dropna(subset=["Close"])
    c = d["Close"]
    last = float(c.iloc[-1])
    dp = pdec(last)
    atr = W.atr14(d)
    out = {
        "last": r(last, dp),
        "prev_close": r(float(c.iloc[-2]), dp) if len(c) > 1 else None,
        "prev_bar_date": str(c.index[-2].date()) if len(c) > 1 else None,
        "pct_1d": r(W.pct(c, 1), 2),
        "pct_5d": r(W.pct(c, 5), 2),
        "atr14": r(atr, dp),
        "ema20": r(c.ewm(span=20, adjust=False).mean().iloc[-1], dp),
        "ema50": r(c.ewm(span=50, adjust=False).mean().iloc[-1], dp),
        "trend": W.trend_of(c),
        "ema20_4h": None, "ema50_4h": None, "dist4h": None, "dip_zone": False,
        "bar_date": str(c.index[-1].date()),
        "max_range_60d": X.max_range_60d(d),
        "why": None,
    }
    try:
        hd = W.sub(h1, sym) if h1 is not None else None
        if hd is None:
            raise ValueError(W.short(herr, 6) if herr else "no 1h data")
        e20 = W.ema20_4h(hd)          # watch.py's own function
        b = bars4h(hd)
        e50 = float(b.ewm(span=50, adjust=False).mean().iloc[-1]) if len(b) >= 50 else None
        out["ema20_4h"] = r(e20, dp)
        out["ema50_4h"] = r(e50, dp)
        dist = (last - e20) / atr
        out["dist4h"] = r(dist, 2)
        out["dip_zone"] = bool(out["trend"] in ("UP", "DOWN") and abs(dist) <= 0.5)
        if e50 is None:
            out["why"] = "under 50 4h bars: ema50_4h null"
    except Exception as e:
        out["why"] = "4h: " + W.short(e, 6)
    return out


def macro_block():
    res = {}
    with ThreadPoolExecutor(max_workers=5) as ex:
        futs = {sid: ex.submit(W.fred_series, sid) for sid, _ in FRED}  # 10 s timeout inside
        for sid, nm in FRED:
            try:
                s = futs[sid].result(timeout=20)
                res[sid] = {"name": nm, "value": r(s.iloc[-1], 3), "date": str(s.index[-1].date()),
                            "chg_5d": r(s.iloc[-1] - s.iloc[-6], 3), "why": None}
            except Exception as e:
                res[sid] = {"name": nm, "value": None, "date": None, "chg_5d": None,
                            "why": "FRED unavailable: " + W.short(e, 6)}
    return res


def log(ok, why):
    try:
        with open(LOG, "a", encoding="utf-8") as fh:
            fh.write(f"{dt.datetime.now(dt.timezone.utc):%Y-%m-%d %H:%M:%S}Z {'ok' if ok else 'fail'} {why}\n")
    except Exception:
        pass


def git(cwd, *args):
    p = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, timeout=120)
    return p.returncode, (p.stdout + p.stderr).strip()


def build():
    utc = dt.datetime.now(dt.timezone.utc)
    errors = []
    ex = ThreadPoolExecutor(max_workers=2)
    mfut = ex.submit(macro_block)
    daily = h1 = derr = herr = None
    try:
        daily = W.dl(SYMBOLS, period="1y")
    except Exception as e:
        derr = e
        errors.append("daily download: " + W.short(e, 8))
    try:
        h1 = W.dl(SYMBOLS, period="60d", interval="1h")
    except Exception as e:
        herr = e
        errors.append("1h download: " + W.short(e, 8))
    syms = {}
    for s in SYMBOLS:
        try:
            syms[s] = one_symbol(s, daily, h1, derr, herr)
            if syms[s]["why"]:
                errors.append(f"{s}: {syms[s]['why']}")
        except Exception as e:
            syms[s] = None
            errors.append(f"{s}: {W.short(e, 8)}")
    extra = X.all_blocks(W)  # never raises; each block carries its own asof / fetched_utc / why
    for k, blk in extra.items():
        if blk.get("why"):
            errors.append(f"{k}: {blk['why']}")
    try:
        macro = mfut.result(timeout=60)
    except Exception as e:
        macro = {sid: {"name": nm, "value": None, "date": None, "chg_5d": None,
                       "why": "macro block failed: " + W.short(e, 6)} for sid, nm in FRED}
    ex.shutdown(wait=False, cancel_futures=True)
    for sid, m in macro.items():
        if m["why"]:
            errors.append(f"{sid}: {m['why']}")
    return {
        "generated_utc": utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "generated_uk": W.uk_now(utc),
        "source": ("tools/push_prices.py (GitHub Actions, yfinance)" if os.environ.get("GITHUB_ACTIONS")
                   else "bridge push_prices.py (yfinance local)"),
        "symbols": syms, "macro": macro, **extra, "errors": errors,
    }


def table(data):
    print(f"{'symbol':<7}{'last':>10}{'ATR14':>9}{'4hEMA20':>10}{'4hEMA50':>10}{'dist4h':>8}  {'trend':<5} DIP_ZONE  bar")
    print("-" * 82)
    for s, v in data["symbols"].items():
        if not v:
            print(f"{s:<7} unavailable")
            continue

        def g(k):
            return "n/a" if v[k] is None else f"{v[k]:.2f}"

        dist = "n/a" if v["dist4h"] is None else format(v["dist4h"], "+.2f")
        print(f"{s:<7}{g('last'):>10}{g('atr14'):>9}{g('ema20_4h'):>10}{g('ema50_4h'):>10}"
              f"{dist:>8}  {v['trend']:<5} {'DIP_ZONE' if v['dip_zone'] else '-':<9} {v['bar_date']}")
    print("-" * 82)
    for sid, m in data["macro"].items():
        if m["value"] is not None:
            print(f"{sid:<9} {m['value']} ({m['date']}) 5d {m['chg_5d']:+}")
        else:
            print(f"{sid:<9} null - {m['why']}")
    print("-" * 82)
    sp, ck, gl, hz, ei = (data.get(k, {}) for k in ("spreads", "crack_321", "gld_tonnes", "hormuz_7d", "eia_weekly"))
    for key in ("brent", "wti"):
        b = sp.get(key) or {}
        print(f"spread {key:<6} M1-M2 {b.get('m1_m2')}  M1-M3 {b.get('m1_m3')}  {b.get('contracts')}  ({sp.get('asof')}) "
              f"{'' if b.get('m1_m2') is not None else sp.get('why')}")
    print(f"crack_321  {ck.get('value')} $/bbl  (RB {ck.get('rb')} HO {ck.get('ho')} CL {ck.get('cl')}, {ck.get('asof')}) {ck.get('why') or ''}")
    print(f"gld_tonnes {gl.get('tonnes')} t chg {gl.get('chg_1d')} ({gl.get('asof')}) {gl.get('why') or ''}")
    print(f"hormuz_7d  newest {hz.get('n_total')} ({hz.get('asof')}) 7d {hz.get('mean_7d')} 14d {hz.get('mean_14d')} {hz.get('why') or ''}")
    print(f"eia_weekly crude {ei.get('crude_stocks')} gas {ei.get('natgas_storage')} {ei.get('why') or ''}")
    if data["errors"]:
        print("errors:", "; ".join(data["errors"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--out", help=f"geo-prices checkout dir (default {DEFAULT_DIR})")
    ap.add_argument("--no-git", action="store_true", help="write DIR/prices.json only; no git (Actions commits)")
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    out_dir = Path(a.out) if a.out else DEFAULT_DIR
    if not a.dry_run and not a.no_git and not (out_dir / ".git").exists():
        print(SETUP.format(d=out_dir, x=HERE / "geo-prices-bridge.xml"))
        log(False, f"no git checkout at {out_dir}")
        return 2

    try:
        data = build()
    except Exception as e:
        log(False, "compute failed: " + W.short(e, 10))
        print("push_prices: compute failed:", W.short(e, 10))
        return 1
    n_ok = sum(1 for v in data["symbols"].values() if v)
    if n_ok == 0:
        log(False, "no symbol priced; not publishing")
        print("push_prices: no symbol priced, nothing published")
        return 1
    text = json.dumps(data, indent=1, ensure_ascii=False)

    if a.dry_run:
        (HERE / "prices.json").write_text(text, encoding="utf-8")
        table(data)
        print(f"dry-run: wrote {HERE / 'prices.json'} ({n_ok}/{len(SYMBOLS)} symbols, {len(data['errors'])} errors)")
        log(True, f"dry-run {n_ok}/{len(SYMBOLS)} symbols")
        return 0

    (out_dir / "prices.json").write_text(text, encoding="utf-8")
    stamp = data["generated_utc"]
    if a.no_git:
        log(True, f"no-git wrote {n_ok}/{len(SYMBOLS)} symbols")
        print(f"push_prices ok (no-git) {stamp}: {n_ok}/{len(SYMBOLS)} symbols, macro "
              f"{sum(1 for m in data['macro'].values() if m['value'] is not None)}/{len(FRED)}, {len(data['errors'])} errors")
        return 0
    try:
        rc, o = git(out_dir, "add", "prices.json")
        if rc:
            raise RuntimeError("git add: " + o)
        rc, o = git(out_dir, "diff", "--cached", "--quiet")
        if rc == 0:
            log(True, "no change")
            print("push_prices: prices.json unchanged, nothing to commit")
            return 0
        rc, o = git(out_dir, "commit", "-m", f"prices {stamp}")
        if rc:
            raise RuntimeError("git commit: " + o)
        rc, o = git(out_dir, "push", "-u", "origin", "main")
        if rc:
            raise RuntimeError("git push: " + o)
    except Exception as e:
        log(False, W.short(e, 25))
        print("push_prices FAILED:", e)
        return 1
    log(True, f"pushed {n_ok}/{len(SYMBOLS)} symbols, {len(data['errors'])} errors")
    print(f"push_prices ok {stamp}: {n_ok}/{len(SYMBOLS)} symbols, macro "
          f"{sum(1 for m in data['macro'].values() if m['value'] is not None)}/{len(FRED)}, {len(data['errors'])} errors")
    return 0


if __name__ == "__main__":
    sys.exit(main())
