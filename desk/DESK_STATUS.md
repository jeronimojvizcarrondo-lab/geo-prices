# DESK STATUS — v6 Actions, code-rendered, no model

- v6 Actions 2026-11-18T23:08:40Z — status: OK
- Price file age: 3.5 hours (generated 2026-11-18T19:39:09Z, read from raw-url) — not stale.
- API spend this month so far: $0.00 (hard limit $92, today $0.00).
- Source health: 184 ok / 42 missing / 40 swapped; 1 skipped (key not set).
- Book 1: n=0 open=0 · mean R n/a · mean twin_R n/a · diff n/a · bootstrap 90% lower bound of diff n/a (10,000 resamples, seed 7) · max drawdown 0.00R · logged-before-fill 0/0 · open marks Σ +0.00R  //  Book 2: n=4 open=3 · mean R +0.36 · mean twin_R -0.56 · diff +0.92 · bootstrap 90% lower bound of diff +0.00 (10,000 resamples, seed 7) · max drawdown 2.04R · logged-before-fill 3/7 · open marks Σ +1.32R

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
  - (f) gate_inputs.json written 359 h ago (> 24 h)
  - (b) Hormuz war A: na
- oil short: (a) none in window
  - (f) gate_inputs.json written 359 h ago (> 24 h)
  - (b) Hormuz war B: na
- tankers long: (a) none in window
  - (f) gate_inputs.json written 359 h ago (> 24 h)
  - (b) Shadow-fleet sanctions B: na
- copper long: (a) none in window
  - (f) gate_inputs.json written 359 h ago (> 24 h)
  - (b) Chile copper labour B: na
- corn long: (a) none in window
  - (f) gate_inputs.json written 359 h ago (> 24 h)
  - (b) US harvest / grains B: fail
- wheat long: (a) none in window
  - (f) gate_inputs.json written 359 h ago (> 24 h)
  - (b) Black Sea / Ukraine B: fail
- gold long: (a) none in window
  - (f) gate_inputs.json written 359 h ago (> 24 h)
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
| oil short | Hormuz war B | BZ=F close <100 | BZ=F < 100 | 89.1 | true | BZ=F.last 89.1 bar 2026-11-18 |
| tankers long | Shadow-fleet sanctions B | = bridge FRO trend UP + DIP_ZONE | - | - | not evaluable | needs documents / counts / polls / other data the job cannot read |
| tankers long | Shadow-fleet sanctions B | a UKMTO warning number quoted by two outlets ≤72h — E7 ; today trend FLAT = not met | - | - | not evaluable | needs documents / counts / polls / other data the job cannot read |
| copper long | Chile copper labour B | = a company IR page or Sernageomin notice, dated after 16 Oct and ≤72h old, containing one mine name | - | - | not evaluable | needs documents / counts / polls / other data the job cannot read |
| copper long | Chile copper labour B | the word strike, huelga or paralización | - | - | not evaluable | needs documents / counts / polls / other data the job cannot read |
| copper long | Chile copper labour B | bridge HG=F DIP_ZONE with trend UP | - | - | not evaluable | needs documents / counts / polls / other data the job cannot read |
| corn long | US harvest / grains B | NASS Crop Progress corn harvested ≥5 pts behind the 5-yr average | - | - | not evaluable | needs documents / counts / polls / other data the job cannot read |
| corn long | US harvest / grains B | ZC=F close >500 | ZC=F > 500 | 448.25 | false | ZC=F.last 448.25 bar 2026-11-18 |
| wheat long | Black Sea / Ukraine B | port outage or Azov closure confirmed Tier 1 | - | - | not evaluable | needs documents / counts / polls / other data the job cannot read |
| wheat long | Black Sea / Ukraine B | ZW=F close >690 | ZW=F > 690 | 586.75 | false | ZW=F.last 586.75 bar 2026-11-18 |
| gold long | Fed / real yields A | = a treasury.gov/FRED DFII10 print ≤2.70 dated on or before 4 Nov | DFII10 ≤ 2.70 | 2.64 | not evaluable | DFII10 dated 2026-10-27: older than 7 days or missing |

## Bridge prices (asof = the bar date of the last price)

| symbol | last | 1d % | trend | dip_zone | asof |
|---|---|---|---|---|---|
| BZ=F | 89.1 | -4.34 | DOWN | False | 2026-11-18 |
| FRO | 44.44 | -1.95 | DOWN | False | 2026-11-18 |
| HG=F | 5.674 | -5.05 | DOWN | False | 2026-11-18 |
| ZC=F | 448.25 | 0.34 | DOWN | True | 2026-11-18 |
| ZW=F | 586.75 | -1.43 | DOWN | False | 2026-11-18 |
| GC=F | 3730.7 | -3.45 | DOWN | False | 2026-11-18 |
| SI=F | 44.94 | -4.97 | DOWN | False | 2026-11-18 |
| NG=F | 3.374 | 5.17 | UP | False | 2026-11-18 |
| EWZ | 30.1 | -2.97 | DOWN | False | 2026-11-18 |
| SPY | 729.89 | -0.35 | DOWN | False | 2026-11-18 |
| BNO | 58.3 | -1.12 | FLAT | False | 2026-11-18 |
| SCO | 21.22 | 3.09 | FLAT | False | 2026-11-18 |
| GLD | 341.0 | -3.26 | DOWN | False | 2026-11-18 |
| CPER | 34.07 | -5.33 | DOWN | False | 2026-11-18 |
| COPX | 60.88 | -6.79 | DOWN | False | 2026-11-18 |
| CORN | 16.9 | -2.04 | DOWN | False | 2026-11-18 |
| WEAT | 21.18 | -3.62 | DOWN | False | 2026-11-18 |
| UNG | 10.59 | 5.49 | FLAT | False | 2026-11-18 |
| SLV | 40.51 | -4.98 | DOWN | False | 2026-11-18 |

Real-yield data (FRED) newest date: 2026-10-27; stale: True.
Gate legs not evaluable: fed real-yield leg.
