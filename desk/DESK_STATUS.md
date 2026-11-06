# DESK STATUS — v6 Actions, code-rendered, no model

- v6 Actions 2026-11-06T14:54:23Z — status: OK
- Price file age: 14.3 hours (generated 2026-11-06T00:34:57Z, read from raw-url) — not stale.
- API spend this month so far: $0.00 (hard limit $92, today $0.00).
- Source health: 183 ok / 43 missing / 38 swapped; 1 skipped (key not set).
- Book 1: n=0 open=0 · mean R n/a · mean twin_R n/a · diff n/a · bootstrap 90% lower bound of diff n/a (10,000 resamples, seed 7) · max drawdown 0.00R · logged-before-fill 0/0 · open marks Σ +0.00R  //  Book 2: n=3 open=2 · mean R +0.82 · mean twin_R -0.47 · diff +1.29 · bootstrap 90% lower bound of diff +0.00 (10,000 resamples, seed 7) · max drawdown 1.03R · logged-before-fill 2/5 · open marks Σ +0.00R

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
  - (f) gate_inputs.json written 63 h ago (> 24 h)
  - (b) Hormuz war A: na
- oil short: (a) none in window
  - (f) gate_inputs.json written 63 h ago (> 24 h)
  - (b) Hormuz war B: na
- tankers long: (a) none in window
  - (f) gate_inputs.json written 63 h ago (> 24 h)
  - (b) Shadow-fleet sanctions B: na
- copper long: (a) none in window
  - (f) gate_inputs.json written 63 h ago (> 24 h)
  - (b) Chile copper labour B: na
- corn long: (a) none in window
  - (f) gate_inputs.json written 63 h ago (> 24 h)
  - (b) US harvest / grains B: fail
- wheat long: (a) none in window
  - (f) gate_inputs.json written 63 h ago (> 24 h)
  - (b) Black Sea / Ukraine B: fail
- gold long: (a) none in window
  - (f) gate_inputs.json written 63 h ago (> 24 h)
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
| oil short | Hormuz war B | BZ=F close <100 | BZ=F < 100 | 98.98 | true | BZ=F.last 98.98 bar 2026-11-05 |
| tankers long | Shadow-fleet sanctions B | = bridge FRO trend UP + DIP_ZONE | - | - | not evaluable | needs documents / counts / polls / other data the job cannot read |
| tankers long | Shadow-fleet sanctions B | a UKMTO warning number quoted by two outlets ≤72h — E7 ; today trend FLAT = not met | - | - | not evaluable | needs documents / counts / polls / other data the job cannot read |
| copper long | Chile copper labour B | = a company IR page or Sernageomin notice, dated after 16 Oct and ≤72h old, containing one mine name | - | - | not evaluable | needs documents / counts / polls / other data the job cannot read |
| copper long | Chile copper labour B | the word strike, huelga or paralización | - | - | not evaluable | needs documents / counts / polls / other data the job cannot read |
| copper long | Chile copper labour B | bridge HG=F DIP_ZONE with trend UP | - | - | not evaluable | needs documents / counts / polls / other data the job cannot read |
| corn long | US harvest / grains B | NASS Crop Progress corn harvested ≥5 pts behind the 5-yr average | - | - | not evaluable | needs documents / counts / polls / other data the job cannot read |
| corn long | US harvest / grains B | ZC=F close >500 | ZC=F > 500 | 440.75 | false | ZC=F.last 440.75 bar 2026-11-05 |
| wheat long | Black Sea / Ukraine B | port outage or Azov closure confirmed Tier 1 | - | - | not evaluable | needs documents / counts / polls / other data the job cannot read |
| wheat long | Black Sea / Ukraine B | ZW=F close >690 | ZW=F > 690 | 599.25 | false | ZW=F.last 599.25 bar 2026-11-05 |
| gold long | Fed / real yields A | = a treasury.gov/FRED DFII10 print ≤2.70 dated on or before 4 Nov | DFII10 ≤ 2.70 | 2.64 | not evaluable | DFII10 dated 2026-10-27: older than 7 days or missing |

## Bridge prices (asof = the bar date of the last price)

| symbol | last | 1d % | trend | dip_zone | asof |
|---|---|---|---|---|---|
| BZ=F | 98.98 | 4.61 | FLAT | False | 2026-11-05 |
| FRO | 44.7 | -7.8 | FLAT | False | 2026-11-05 |
| HG=F | 6.246 | -2.45 | DOWN | False | 2026-11-05 |
| ZC=F | 440.75 | -0.79 | DOWN | False | 2026-11-05 |
| ZW=F | 599.25 | 0.13 | DOWN | True | 2026-11-05 |
| GC=F | 4114.3 | 1.01 | FLAT | False | 2026-11-05 |
| SI=F | 52.06 | -0.11 | DOWN | True | 2026-11-05 |
| NG=F | 2.938 | -0.71 | FLAT | False | 2026-11-05 |
| EWZ | 31.76 | -1.52 | DOWN | False | 2026-11-05 |
| SPY | 733.0 | -4.41 | DOWN | False | 2026-11-05 |
| BNO | 62.53 | 3.53 | FLAT | False | 2026-11-05 |
| SCO | 19.19 | -0.05 | FLAT | False | 2026-11-05 |
| GLD | 375.49 | 0.81 | FLAT | False | 2026-11-05 |
| CPER | 37.36 | -3.19 | DOWN | False | 2026-11-05 |
| COPX | 70.23 | -5.81 | DOWN | False | 2026-11-05 |
| CORN | 17.15 | -1.44 | DOWN | False | 2026-11-05 |
| WEAT | 21.93 | -0.27 | DOWN | False | 2026-11-05 |
| UNG | 9.27 | 0.0 | DOWN | True | 2026-11-05 |
| SLV | 46.93 | -0.49 | DOWN | True | 2026-11-05 |

Real-yield data (FRED) newest date: 2026-10-27; stale: True.
Gate legs not evaluable: fed real-yield leg.
