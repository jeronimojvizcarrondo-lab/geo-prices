# vendored from Trading/skills/geo-watch/watch.py 2026-10-18 - do not edit here; edit the Trading copy and re-copy (see bridge/README.md "Sync")
"""geo-watch: one-shot commodities/geo desk snapshot. Standalone (stdlib + yfinance + pandas).

    python watch.py

Columns: last = latest daily close (may be intraday); 1d%/5d% = change vs 1/5 sessions ago.
trend = daily EMA20/EMA50 (adjust=False): px>EMA20>EMA50 UP, px<EMA20<EMA50 DOWN, else FLAT.
ATR14 = Wilder 14-day ATR on daily OHLC ($ units). dist4h = (last - 4h EMA20)/ATR14, signed
(+ = above); 4h bars are resampled from 1h data (yfinance has no 4h). DIP_ZONE: printed when
trend is UP or DOWN and |dist4h| <= 0.5 ATR (price has pulled back to the 4h EMA20 inside a
trend); otherwise "-". vol = today's volume / mean of prior 20 sessions (n/a if zero/NaN).
vol/20d skips zero-volume bars, needs >=15 sessions (else n/a (thin)), shows '?' if >5x, and is
partial intraday until the session closes.
VIX row: last close and 5d change in points (regime tells 16/20/30). SPY is a regime gauge only and is never traded. Macro block: Brent (else WTI) and natgas
curve spreads, 10y real yield, dollar, OVX, GVZ. Every failed fetch prints "unavailable (why)".
FRED is tried first (works in cloud, times out on some local machines); sources are printed.
"""

import datetime as dt
import io
import logging
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd
import yfinance as yf

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
logging.getLogger("yfinance").setLevel(logging.CRITICAL)

T0 = time.time()
DASH = "—"

SYMBOLS = [
    ("BZ=F", "oil"), ("FRO", "tankers"), ("HG=F", "copper"), ("ZC=F", "corn"),
    ("ZW=F", "wheat"), ("GC=F", "gold"), ("SI=F", "silver"), ("NG=F", "natgas"),
    ("EWZ", "brazil"), ("SPY", "(gauge)"),
]
MACRO_YF = ["DX-Y.NYB", "^OVX", "^GVZ", "^VIX"]
MONTH_CODES = "FGHJKMNQUVXZ"
UA = {"User-Agent": "Mozilla/5.0 (geo-watch)"}


def short(e, n=8):
    s = (str(e) or type(e).__name__).strip().replace("\n", " ")
    if not s or "Timeout" in type(e).__name__ or "timed out" in s:
        s = "timeout" if "imed" in (s + type(e).__name__) else s
    return " ".join(s.split()[:n])


def unavailable(why):
    return f"unavailable ({short(why) if isinstance(why, Exception) else why})"


# ------------------------------------------------------------------ time
def uk_now(utc):
    try:
        from zoneinfo import ZoneInfo
        return utc.astimezone(ZoneInfo("Europe/London")).strftime("%Y-%m-%d %H:%M %Z")
    except Exception:
        # BST = last Sunday of March 01:00 UTC .. last Sunday of Oct 01:00 UTC
        def last_sun(y, m):
            d = dt.datetime(y, m + 1, 1, 1, tzinfo=dt.timezone.utc) if m < 12 else dt.datetime(y + 1, 1, 1, 1, tzinfo=dt.timezone.utc)
            d -= dt.timedelta(days=1)
            return d - dt.timedelta(days=(d.weekday() + 1) % 7)
        bst = last_sun(utc.year, 3) <= utc < last_sun(utc.year, 10)
        return (utc + dt.timedelta(hours=1 if bst else 0)).strftime("%Y-%m-%d %H:%M ") + ("BST" if bst else "GMT")


# ------------------------------------------------------------------ http (FRED / treasury)
def http_csv(url, timeout=10):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return pd.read_csv(io.BytesIO(r.read()))


def fred_series(sid):
    df = http_csv(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}", 10)
    s = pd.to_numeric(df[sid], errors="coerce")
    s.index = pd.to_datetime(df.iloc[:, 0])
    s = s.dropna()
    if len(s) < 6:
        raise ValueError("too few observations")
    return s


def treasury_real10():
    y = dt.datetime.now().year
    url = ("https://home.treasury.gov/resource-center/data-chart-center/interest-rates/"
           f"daily-treasury-rates.csv/{y}/all?type=daily_treasury_real_yield_curve"
           f"&field_tdr_date_value={y}&page&_format=csv")
    df = http_csv(url, 10)
    s = pd.to_numeric(df["10 YR"], errors="coerce")
    s.index = pd.to_datetime(df["Date"])
    s = s.dropna().sort_index()
    if len(s) < 6:
        raise ValueError("too few observations")
    return s


def dfii10_job():
    try:
        return fred_series("DFII10"), "FRED"
    except Exception as e1:
        try:
            return treasury_real10(), f"treasury.gov (FRED failed: {short(e1, 3)})"
        except Exception as e2:
            raise RuntimeError(f"FRED+treasury failed: {short(e2, 4)}")


# ------------------------------------------------------------------ yfinance helpers
def sub(df, sym):
    try:
        d = df[sym].dropna(how="all")
    except Exception:
        return None
    return d if len(d) else None


def dl(tickers, **kw):
    return yf.download(tickers, group_by="ticker", threads=True, auto_adjust=False,
                       progress=False, **kw)


# copied from research/quant/read_chart.py (cloud has no data/ store)
def trend_of(close):
    px = float(close.iloc[-1])
    e20 = float(close.ewm(span=20, adjust=False).mean().iloc[-1])
    e50 = float(close.ewm(span=50, adjust=False).mean().iloc[-1])
    return "UP" if px > e20 > e50 else "DOWN" if px < e20 < e50 else "FLAT"


# copied from research/quant/read_chart.py (cloud has no data/ store)
def vol_ratio(vol):
    """Returns (ratio|None, flag). Prior 20 non-zero, non-NaN sessions; <15 -> thin."""
    v = pd.to_numeric(vol, errors="coerce")
    today = v.iloc[-1]
    if not np.isfinite(today) or today <= 0:
        return None, "n/a"
    prior = v.iloc[:-1]
    prior = prior[prior.notna() & (prior > 0)].iloc[-20:]
    if len(prior) < 15:
        return None, "n/a (thin)"
    avg = prior.mean()
    if not avg or not np.isfinite(avg):
        return None, "n/a"
    r = float(today / avg)
    return r, (f"{r:.2f}?" if r > 5.0 else f"{r:.2f}")


def atr14(d):
    h, l, c = d["High"], d["Low"], d["Close"]
    pc = c.shift(1)
    tr = pd.concat([h - l, (h - pc).abs(), (l - pc).abs()], axis=1).max(axis=1)
    return float(tr.ewm(alpha=1 / 14, adjust=False).mean().iloc[-1])


def ema20_4h(h1):
    c = h1["Close"].dropna()
    if c.empty:
        raise ValueError("no 1h data")
    bars = c.resample("4h", label="left", closed="left").last().dropna()
    if len(bars) < 20:
        raise ValueError("under 20 4h bars")
    return float(bars.ewm(span=20, adjust=False).mean().iloc[-1])


def pct(c, n):
    return (c.iloc[-1] / c.iloc[-1 - n] - 1) * 100 if len(c) > n else float("nan")


def f(x, fmt):
    return fmt.format(x) if x is not None and np.isfinite(x) else "n/a"


# ------------------------------------------------------------------ curve
def contract_codes(prefix, n=14):
    now = dt.datetime.now()
    out = []
    for i in range(n):
        m = now.month - 1 + i
        y, mi = now.year + m // 12, m % 12
        out.append(f"{prefix}{MONTH_CODES[mi]}{y % 100:02d}.NYM")
    return out


def priced_contracts(prefixes):
    """Download all candidate contracts in one call; keep ones with a recent close."""
    cand = {p: contract_codes(p) for p in prefixes}
    allt = [t for v in cand.values() for t in v]
    df = dl(allt, period="10d")
    res = {}
    cutoff = pd.Timestamp.now().normalize() - pd.Timedelta(days=7)
    for p, tl in cand.items():
        got = []
        for t in tl:
            d = sub(df, t)
            if d is None:
                continue
            c = d["Close"].dropna()
            if len(c) and c.index[-1].tz_localize(None) >= cutoff:
                got.append((t.replace(".NYM", ""), float(c.iloc[-1]), c.index[-1].date()))
        if got:  # drop expired contracts that only return a stale last print
            newest = max(g[2] for g in got)
            got = [g[:2] for g in got if g[2] >= newest]
        res[p] = got
    return res


def spread_lines(label, got, want6=True):
    if len(got) < 2:
        return [f"{label}: unavailable ({len(got)} contracts priced)"]
    (n1, p1), (n2, p2) = got[0], got[1]
    state = "backwardation" if p1 > p2 else "contango"
    line = f"{label}: M1-M2 {p1 - p2:+.2f} ({n1} {p1:.2f} - {n2} {p2:.2f}) {state}"
    if want6:
        if len(got) >= 6:
            n6, p6 = got[5]
            line += f" | M1-M6 {p1 - p6:+.2f} ({n1}-{n6} {p6:.2f})"
        else:
            line += f" | M1-M6 unavailable (only {len(got)} contracts)"
    return [line]


def curve_block():
    out = []
    try:
        res = priced_contracts(["BZ", "NG"])
    except Exception as e:
        return [f"Brent curve: {unavailable(e)}", f"Natgas curve: {unavailable(e)}"]
    if len(res["BZ"]) >= 2:
        out += spread_lines("Brent curve", res["BZ"])
    else:
        try:
            wti = priced_contracts(["CL"])["CL"]
            out += [l.replace("Brent curve:", "Brent unavailable -> WTI curve (CL):", 1)
                    for l in spread_lines("Brent curve", wti)]
        except Exception as e:
            out.append(f"Brent/WTI curve: {unavailable(e)}")
    out += spread_lines("Natgas curve", res["NG"], want6=False)
    return out


# ------------------------------------------------------------------ main
def main():
    utc = dt.datetime.now(dt.timezone.utc)
    ex = ThreadPoolExecutor(max_workers=6)
    jobs = {"DFII10": ex.submit(dfii10_job)}
    for sid in ("DTWEXBGS", "OVXCLS", "GVZCLS", "VIXCLS"):
        jobs[sid] = ex.submit(fred_series, sid)
    curve_fut = ex.submit(curve_block)

    syms = [s for s, _ in SYMBOLS]
    daily = h1 = None
    derr = herr = None
    try:
        daily = dl(syms + MACRO_YF, period="1y")
    except Exception as e:
        derr = e
    try:
        h1 = dl(syms, period="60d", interval="1h")
    except Exception as e:
        herr = e

    print(f"GEO-WATCH  run {utc:%Y-%m-%d %H:%M} UTC / {uk_now(utc)} UK")
    print(f"{'symbol':<14}{'last':>9}{'1d%':>7}{'5d%':>7}  {'trend':<5}{'ATR14':>8}{'d4h/ATR':>9}  {'DIP_ZONE':<9}{'vol/20d':>11}")
    print("-" * 80)
    spy_trend = None
    for sym, name in SYMBOLS:
        label = f"{sym} {name}"
        d = sub(daily, sym) if daily is not None else None
        if d is None or "Close" not in d or d["Close"].dropna().empty:
            print(f"{label:<14} {unavailable(derr or 'no daily data')}")
            continue
        try:
            d = d.dropna(subset=["Close"])
            c = d["Close"]
            last = float(c.iloc[-1])
            tr = trend_of(c)
            atr = atr14(d)
            vr = vol_ratio(d["Volume"]) if "Volume" in d else (None, "n/a")
            if sym == "SPY":
                spy_trend = (tr, pct(c, 1))
        except Exception as e:
            print(f"{label:<14} {unavailable(e)}")
            continue
        dist = None
        why = None
        try:
            hd = sub(h1, sym) if h1 is not None else None
            if hd is None:
                raise ValueError(short(herr, 5) if herr else "no 1h data")
            dist = (last - ema20_4h(hd)) / atr
        except Exception as e:
            why = short(e, 5)
        dip = DASH if dist is None else ("DIP_ZONE" if tr in ("UP", "DOWN") and abs(dist) <= 0.5 else DASH)
        dcell = f"{dist:+.2f}" if dist is not None else "unavail"
        print(f"{label:<14}{last:>9.2f}{f(pct(c, 1), '{:+.1f}'):>7}{f(pct(c, 5), '{:+.1f}'):>7}  {tr:<5}"
              f"{atr:>8.2f}{dcell:>9}  {dip:<9}{vr[1]:>11}")
        if why:
            print(f"   note: {sym} 4h dist {unavailable(why)}")
    print("(SPY = regime gauge only, never traded)")

    # ---- macro
    print("-" * 80)
    for line in (curve_fut.result(timeout=45) if True else []):
        print(line)

    def getjob(k):
        try:
            return jobs[k].result(timeout=25), None
        except Exception as e:
            return None, e

    def yf_series(t):
        d = sub(daily, t) if daily is not None else None
        if d is None or d["Close"].dropna().size < 6:
            raise ValueError("no yfinance data")
        return d["Close"].dropna()

    # DFII10
    try:
        r, e = getjob("DFII10")
        if e:
            raise e
        s, src = r
        print(f"DFII10 10y real yield: {s.iloc[-1]:.2f}% ({s.index[-1]:%Y-%m-%d}), 5d chg "
              f"{(s.iloc[-1] - s.iloc[-6]) * 100:+.0f}bp [src: {src}]")
    except Exception as e:
        print(f"DFII10 10y real yield: {unavailable(e)}")

    # DXY, OVX, GVZ: FRED first then yfinance
    for fid, yt, nm, nm_yf, kind in (
            ("DTWEXBGS", "DX-Y.NYB", "Broad dollar (DTWEXBGS, not DXY)", "DXY", "pct"),
            ("OVXCLS", "^OVX", "OVX", "OVX", "abs"),
            ("GVZCLS", "^GVZ", "GVZ", "GVZ", "abs"),
            ("VIXCLS", "^VIX", "VIX", "VIX", "abs")):
        s, src, ferr = None, None, None
        s, ferr = getjob(fid)
        if s is not None:
            src = f"FRED {fid}"
        else:
            try:
                s = yf_series(yt)
                src = f"yfinance {yt} (FRED failed: {short(ferr, 3)})"
                nm = nm_yf
            except Exception as e:
                print(f"{nm}: {unavailable(e)}")
                continue
        try:
            chg = f"{pct(s, 5):+.2f}%" if kind == "pct" else f"{s.iloc[-1] - s.iloc[-6]:+.2f} pts"
            print(f"{nm}: {s.iloc[-1]:.2f}, 5d {chg} [src: {src}]")
        except Exception as e:
            print(f"{nm}: {unavailable(e)}")

    if spy_trend:
        print(f"SPY trend: {spy_trend[0]}, 1d {spy_trend[1]:+.2f}% (regime gauge only {DASH} never traded)")
    else:
        print(f"SPY trend: {unavailable('no daily data')}")

    print("-" * 80)
    print(f"runtime {time.time() - T0:.1f}s")
    ex.shutdown(wait=False, cancel_futures=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # never crash
        print(f"geo-watch aborted: {unavailable(exc)}")
        print(f"runtime {time.time() - T0:.1f}s")
