# DESK STATUS — v6 Actions, code-rendered, no model

- v6 Actions 2026-10-27T13:06:30Z — status: DEGRADED: price file is stale (13.7 h old)
- Price file age: 13.7 hours (generated 2026-10-26T23:24:03Z, read from raw-url) — STALE: it predates the last scheduled update.
- API spend this month so far: $0.00 (hard limit $92, today $0.00).
- Source health: 186 ok / 40 missing / 39 swapped; 1 skipped (key not set).
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
| BZ=F | 110.15 | -5.63 | UP | True | 2026-10-26 |
| FRO | 55.23 | 4.33 | UP | False | 2026-10-26 |
| HG=F | 6.544 | 1.05 | FLAT | False | 2026-10-26 |
| ZC=F | 455.0 | -0.22 | DOWN | True | 2026-10-26 |
| ZW=F | 615.5 | -1.52 | DOWN | False | 2026-10-26 |
| GC=F | 4024.7 | 0.42 | DOWN | True | 2026-10-26 |
| SI=F | 53.94 | 0.44 | DOWN | False | 2026-10-26 |
| NG=F | 3.043 | 15.27 | UP | True | 2026-10-26 |
| EWZ | 34.15 | -19.82 | FLAT | False | 2026-10-26 |
| SPY | 765.37 | 0.71 | FLAT | False | 2026-10-26 |
| BNO | 70.07 | -1.3 | UP | False | 2026-10-26 |
| SCO | 16.12 | 1.26 | DOWN | False | 2026-10-26 |
| GLD | 367.82 | 0.33 | DOWN | False | 2026-10-26 |
| CPER | 39.39 | 0.84 | DOWN | True | 2026-10-26 |
| COPX | 73.81 | 0.99 | DOWN | False | 2026-10-26 |
| CORN | 17.63 | -0.28 | DOWN | False | 2026-10-26 |
| WEAT | 22.54 | -1.27 | DOWN | False | 2026-10-26 |
| UNG | 9.56 | -0.21 | DOWN | False | 2026-10-26 |
| SLV | 48.66 | -0.12 | DOWN | False | 2026-10-26 |

Real-yield data (FRED) newest date: 2026-10-19; stale: True.
Gate legs not evaluable: fed real-yield leg.
