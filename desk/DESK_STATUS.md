# DESK STATUS — v6 Actions, code-rendered, no model

- v6 Actions 2026-10-28T13:57:03Z — status: DEGRADED: price file is stale (14.7 h old)
- Price file age: 14.7 hours (generated 2026-10-27T23:15:05Z, read from raw-url) — STALE: it predates the last scheduled update.
- API spend this month so far: $0.00 (hard limit $92, today $0.00).
- Source health: 188 ok / 38 missing / 38 swapped; 1 skipped (key not set).
- Book 1: n=0 open=0 · mean R n/a · mean twin_R n/a · diff n/a · bootstrap 90% lower bound of diff n/a (10,000 resamples, seed 7) · max drawdown 0.00R · logged-before-fill 0/0 · open marks Σ +0.00R  //  Book 2: n=0 open=3 · mean R n/a · mean twin_R n/a · diff n/a · bootstrap 90% lower bound of diff n/a (10,000 resamples, seed 7) · max drawdown 0.00R · logged-before-fill 0/3 · open marks Σ +3.15R

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
| BZ=F | 109.5 | -5.45 | UP | True | 2026-10-27 |
| FRO | 53.77 | -2.64 | UP | True | 2026-10-27 |
| HG=F | 6.6565 | 2.28 | UP | False | 2026-10-27 |
| ZC=F | 450.0 | -1.1 | DOWN | False | 2026-10-27 |
| ZW=F | 611.0 | -0.81 | DOWN | False | 2026-10-27 |
| GC=F | 4075.8 | 0.93 | DOWN | True | 2026-10-27 |
| SI=F | 54.53 | 0.79 | DOWN | True | 2026-10-27 |
| NG=F | 3.053 | 17.33 | FLAT | False | 2026-10-27 |
| EWZ | 34.3 | 0.44 | FLAT | False | 2026-10-27 |
| SPY | 769.66 | 0.56 | UP | True | 2026-10-27 |
| BNO | 69.67 | -0.57 | UP | False | 2026-10-27 |
| SCO | 16.25 | 0.81 | DOWN | False | 2026-10-27 |
| GLD | 372.28 | 1.21 | DOWN | True | 2026-10-27 |
| CPER | 40.05 | 1.68 | UP | False | 2026-10-27 |
| COPX | 76.68 | 3.89 | DOWN | True | 2026-10-27 |
| CORN | 17.44 | -1.08 | DOWN | False | 2026-10-27 |
| WEAT | 22.35 | -0.84 | DOWN | False | 2026-10-27 |
| UNG | 9.64 | 0.84 | DOWN | False | 2026-10-27 |
| SLV | 49.16 | 1.03 | DOWN | False | 2026-10-27 |

Real-yield data (FRED) newest date: 2026-10-19; stale: True.
Gate legs not evaluable: fed real-yield leg.
