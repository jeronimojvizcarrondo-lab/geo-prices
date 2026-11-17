# DESK STATUS — v6 Actions, code-rendered, no model

- v6 Actions 2026-11-17T23:43:14Z — status: OK
- Price file age: 3.6 hours (generated 2026-11-17T20:05:29Z, read from raw-url) — not stale.
- API spend this month so far: $0.00 (hard limit $92, today $0.00).
- Source health: 186 ok / 40 missing / 37 swapped; 1 skipped (key not set).
- Book 1: n=0 open=0 · mean R n/a · mean twin_R n/a · diff n/a · bootstrap 90% lower bound of diff n/a (10,000 resamples, seed 7) · max drawdown 0.00R · logged-before-fill 0/0 · open marks Σ +0.00R  //  Book 2: n=4 open=3 · mean R +0.36 · mean twin_R -0.50 · diff +0.85 · bootstrap 90% lower bound of diff -0.13 (10,000 resamples, seed 7) · max drawdown 2.04R · logged-before-fill 3/7 · open marks Σ +0.37R

## Gate verdict by market

Legs (a) verified driver, (b) trigger, (f) desk-written opposing case are supplied by the runner (desk/numbers.py). `not evaluable` means the runner could not evaluate the leg; it is not a FAIL.

| market | dir | a | b | f | verdict |
|---|---|---|---|---|---|
| oil | long | fail | not evaluable | not evaluable | QUIET |
| oil | short | fail | not evaluable | not evaluable | QUIET |
| tankers | long | fail | not evaluable | not evaluable | QUIET |
| copper | long | fail | not evaluable | not evaluable | QUIET |
| corn | long | fail | fail | not evaluable | QUIET |
| wheat | long | fail | fail | not evaluable | QUIET |
| gold | long | fail | not evaluable | not evaluable | QUIET |

## Gate evidence

- oil long: (a) none in window
  - (f) gate_inputs.json written 336 h ago (> 24 h)
  - (b) Hormuz war A: na
- oil short: (a) none in window
  - (f) gate_inputs.json written 336 h ago (> 24 h)
  - (b) Hormuz war B: na
- tankers long: (a) none in window
  - (f) gate_inputs.json written 336 h ago (> 24 h)
  - (b) Shadow-fleet sanctions B: na
- copper long: (a) none in window
  - (f) gate_inputs.json written 336 h ago (> 24 h)
  - (b) Chile copper labour B: na
- corn long: (a) none in window
  - (f) gate_inputs.json written 336 h ago (> 24 h)
  - (b) US harvest / grains B: fail
- wheat long: (a) none in window
  - (f) gate_inputs.json written 336 h ago (> 24 h)
  - (b) Black Sea / Ukraine B: fail
- gold long: (a) none in window
  - (f) gate_inputs.json written 336 h ago (> 24 h)
  - (b) Fed / real yields A: na

## Gate (b) clauses

Clauses extracted from the claude/THREADS.md trigger of the ticket for each market/direction, split on AND. Any numeric clause false makes (b) fail; any non-numeric or unreadable clause makes it not evaluable.

| market dir | ticket | clause | evaluated | value | result | source |
|---|---|---|---|---|---|---|
| oil long | Hormuz war A | = sources.md row : 7d mean of the newest 7 n_total rows ≤ /day | - | - | not evaluable | needs documents / counts / polls / other data the job cannot read |
| oil long | Hormuz war A | a new UKMTO warning number quoted by two outlets ≤48h | - | - | not evaluable | needs documents / counts / polls / other data the job cannot read |
| oil long | Hormuz war A | bridge BZ=F DIP_ZONE with trend UP | - | - | not evaluable | needs documents / counts / polls / other data the job cannot read |
| oil short | Hormuz war B | PortWatch Hormuz 7d mean of n_total ≥ /day | - | - | not evaluable | needs documents / counts / polls / other data the job cannot read |
| oil short | Hormuz war B | no new UKMTO warning number for 7 days | - | - | not evaluable | needs documents / counts / polls / other data the job cannot read |
| oil short | Hormuz war B | BZ=F close <100 | BZ=F < 100 | 92.64 | true | BZ=F.last 92.64 bar 2026-11-17 |
| tankers long | Shadow-fleet sanctions B | = bridge FRO trend UP + DIP_ZONE | - | - | not evaluable | needs documents / counts / polls / other data the job cannot read |
| tankers long | Shadow-fleet sanctions B | a UKMTO warning number quoted by two outlets ≤72h — E7 ; today trend FLAT = not met | - | - | not evaluable | needs documents / counts / polls / other data the job cannot read |
| copper long | Chile copper labour B | = a company IR page or Sernageomin notice, dated after 16 Oct and ≤72h old, containing one mine name | - | - | not evaluable | needs documents / counts / polls / other data the job cannot read |
| copper long | Chile copper labour B | the word strike, huelga or paralización | - | - | not evaluable | needs documents / counts / polls / other data the job cannot read |
| copper long | Chile copper labour B | bridge HG=F DIP_ZONE with trend UP | - | - | not evaluable | needs documents / counts / polls / other data the job cannot read |
| corn long | US harvest / grains B | NASS Crop Progress corn harvested ≥5 pts behind the 5-yr average | - | - | not evaluable | needs documents / counts / polls / other data the job cannot read |
| corn long | US harvest / grains B | ZC=F close >500 | ZC=F > 500 | 446.75 | false | ZC=F.last 446.75 bar 2026-11-17 |
| wheat long | Black Sea / Ukraine B | port outage or Azov closure confirmed Tier 1 | - | - | not evaluable | needs documents / counts / polls / other data the job cannot read |
| wheat long | Black Sea / Ukraine B | ZW=F close >690 | ZW=F > 690 | 610.25 | false | ZW=F.last 610.25 bar 2026-11-17 |
| gold long | Fed / real yields A | = a treasury.gov/FRED DFII10 print ≤2.70 dated on or before 4 Nov | DFII10 ≤ 2.70 | 2.64 | not evaluable | DFII10 dated 2026-10-27: older than 7 days or missing |

## Bridge prices (asof = the bar date of the last price)

| symbol | last | 1d % | trend | dip_zone | asof |
|---|---|---|---|---|---|
| BZ=F | 92.64 | 0.22 | DOWN | True | 2026-11-17 |
| FRO | 45.62 | 0.39 | DOWN | True | 2026-11-17 |
| HG=F | 5.9795 | -0.3 | DOWN | False | 2026-11-17 |
| ZC=F | 446.75 | -0.45 | DOWN | True | 2026-11-17 |
| ZW=F | 610.25 | 3.96 | FLAT | False | 2026-11-17 |
| GC=F | 3851.3 | -0.04 | DOWN | True | 2026-11-17 |
| SI=F | 47.17 | 0.81 | DOWN | False | 2026-11-17 |
| NG=F | 3.184 | 1.99 | UP | True | 2026-11-17 |
| EWZ | 30.91 | -0.05 | DOWN | False | 2026-11-17 |
| SPY | 728.93 | -1.49 | DOWN | False | 2026-11-17 |
| BNO | 58.78 | 0.2 | FLAT | False | 2026-11-17 |
| SCO | 20.67 | 1.25 | FLAT | False | 2026-11-17 |
| GLD | 352.36 | -0.16 | DOWN | False | 2026-11-17 |
| CPER | 35.97 | -0.18 | DOWN | False | 2026-11-17 |
| COPX | 64.97 | -0.83 | DOWN | False | 2026-11-17 |
| CORN | 17.26 | 0.38 | DOWN | True | 2026-11-17 |
| WEAT | 21.95 | 1.54 | DOWN | True | 2026-11-17 |
| UNG | 10.04 | 2.2 | FLAT | False | 2026-11-17 |
| SLV | 42.55 | 0.38 | DOWN | False | 2026-11-17 |

Real-yield data (FRED) newest date: 2026-10-27; stale: True.
Gate legs not evaluable: fed real-yield leg.
