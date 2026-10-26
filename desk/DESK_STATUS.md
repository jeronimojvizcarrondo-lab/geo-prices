# DESK STATUS — v6 Actions, code-rendered, no model

- v6 Actions 2026-10-26T21:15:31Z — status: DEGRADED: price file is stale (3.6 h old)
- Price file age: 3.6 hours (generated 2026-10-26T17:40:36Z, read from raw-url) — STALE: it predates the last scheduled update.
- API spend this month so far: $0.00 (hard limit $92, today $0.00).
- Source health: 188 ok / 38 missing / 38 swapped; 1 skipped (key not set).
- Book 1: n=0 open=0 · mean R n/a · mean twin_R n/a · diff n/a · bootstrap 90% lower bound of diff n/a (10,000 resamples, seed 7) · max drawdown 0.00R · logged-before-fill 0/0 · open marks Σ +0.00R  //  Book 2: n=0 open=3 · mean R n/a · mean twin_R n/a · diff n/a · bootstrap 90% lower bound of diff n/a (10,000 resamples, seed 7) · max drawdown 0.00R · logged-before-fill 0/3 · open marks Σ +3.28R

## Gate verdict by market (conditions (a), (b), (f) are not supplied by the runner, so they default to FAIL)

| market | long | short |
|---|---|---|
| oil | QUIET | QUIET |
| tankers | QUIET | - |
| copper | QUIET | - |
| corn | QUIET | - |
| wheat | QUIET | - |
| gold | QUIET | - |

## Bridge prices (asof = the bar date of the last price)

| symbol | last | 1d % | trend | dip_zone | asof |
|---|---|---|---|---|---|
| BZ=F | 110.92 | -4.97 | UP | True | 2026-10-26 |
| FRO | 55.41 | 4.67 | UP | False | 2026-10-26 |
| HG=F | 6.556 | 1.24 | UP | False | 2026-10-26 |
| ZC=F | 455.25 | -0.16 | DOWN | True | 2026-10-26 |
| ZW=F | 616.0 | -1.44 | DOWN | False | 2026-10-26 |
| GC=F | 4037.5 | 0.74 | DOWN | True | 2026-10-26 |
| SI=F | 54.25 | 1.0 | DOWN | True | 2026-10-26 |
| NG=F | 3.04 | 15.15 | UP | True | 2026-10-26 |
| EWZ | 33.65 | -20.99 | FLAT | False | 2026-10-26 |
| SPY | 765.25 | 0.69 | FLAT | False | 2026-10-26 |
| BNO | 70.36 | -0.88 | UP | False | 2026-10-26 |
| SCO | 16.02 | 0.62 | DOWN | False | 2026-10-26 |
| GLD | 368.55 | 0.53 | DOWN | False | 2026-10-26 |
| CPER | 39.42 | 0.92 | DOWN | True | 2026-10-26 |
| COPX | 74.19 | 1.51 | DOWN | False | 2026-10-26 |
| CORN | 17.61 | -0.4 | DOWN | False | 2026-10-26 |
| WEAT | 22.52 | -1.36 | DOWN | False | 2026-10-26 |
| UNG | 9.55 | -0.31 | DOWN | False | 2026-10-26 |
| SLV | 48.87 | 0.31 | DOWN | False | 2026-10-26 |

Real-yield data (FRED) newest date: 2026-10-19; stale: True.
Gate legs not evaluable: fed real-yield leg.
