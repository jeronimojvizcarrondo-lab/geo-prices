# DESK STATUS — v6 Actions, code-rendered, no model

- v6 Actions 2026-11-11T23:02:19Z — status: OK
- Price file age: 4.1 hours (generated 2026-11-11T18:53:53Z, read from raw-url) — not stale.
- API spend this month so far: $0.00 (hard limit $92, today $0.00).
- Source health: 185 ok / 41 missing / 40 swapped; 1 skipped (key not set).
- Book 1: n=0 open=0 · mean R n/a · mean twin_R n/a · diff n/a · bootstrap 90% lower bound of diff n/a (10,000 resamples, seed 7) · max drawdown 0.00R · logged-before-fill 0/0 · open marks Σ +0.00R  //  Book 2: n=3 open=4 · mean R +0.82 · mean twin_R -0.51 · diff +1.33 · bootstrap 90% lower bound of diff +0.00 (10,000 resamples, seed 7) · max drawdown 1.03R · logged-before-fill 3/7 · open marks Σ -0.57R

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
  - (f) gate_inputs.json written 191 h ago (> 24 h)
  - (b) Hormuz war A: na
- oil short: (a) none in window
  - (f) gate_inputs.json written 191 h ago (> 24 h)
  - (b) Hormuz war B: na
- tankers long: (a) none in window
  - (f) gate_inputs.json written 191 h ago (> 24 h)
  - (b) Shadow-fleet sanctions B: na
- copper long: (a) none in window
  - (f) gate_inputs.json written 191 h ago (> 24 h)
  - (b) Chile copper labour B: na
- corn long: (a) none in window
  - (f) gate_inputs.json written 191 h ago (> 24 h)
  - (b) US harvest / grains B: fail
- wheat long: (a) none in window
  - (f) gate_inputs.json written 191 h ago (> 24 h)
  - (b) Black Sea / Ukraine B: fail
- gold long: (a) none in window
  - (f) gate_inputs.json written 191 h ago (> 24 h)
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
| oil short | Hormuz war B | BZ=F close <100 | BZ=F < 100 | 93.06 | true | BZ=F.last 93.06 bar 2026-11-11 |
| tankers long | Shadow-fleet sanctions B | = bridge FRO trend UP + DIP_ZONE | - | - | not evaluable | needs documents / counts / polls / other data the job cannot read |
| tankers long | Shadow-fleet sanctions B | a UKMTO warning number quoted by two outlets ≤72h — E7 ; today trend FLAT = not met | - | - | not evaluable | needs documents / counts / polls / other data the job cannot read |
| copper long | Chile copper labour B | = a company IR page or Sernageomin notice, dated after 16 Oct and ≤72h old, containing one mine name | - | - | not evaluable | needs documents / counts / polls / other data the job cannot read |
| copper long | Chile copper labour B | the word strike, huelga or paralización | - | - | not evaluable | needs documents / counts / polls / other data the job cannot read |
| copper long | Chile copper labour B | bridge HG=F DIP_ZONE with trend UP | - | - | not evaluable | needs documents / counts / polls / other data the job cannot read |
| corn long | US harvest / grains B | NASS Crop Progress corn harvested ≥5 pts behind the 5-yr average | - | - | not evaluable | needs documents / counts / polls / other data the job cannot read |
| corn long | US harvest / grains B | ZC=F close >500 | ZC=F > 500 | 447.0 | false | ZC=F.last 447.0 bar 2026-11-11 |
| wheat long | Black Sea / Ukraine B | port outage or Azov closure confirmed Tier 1 | - | - | not evaluable | needs documents / counts / polls / other data the job cannot read |
| wheat long | Black Sea / Ukraine B | ZW=F close >690 | ZW=F > 690 | 599.25 | false | ZW=F.last 599.25 bar 2026-11-11 |
| gold long | Fed / real yields A | = a treasury.gov/FRED DFII10 print ≤2.70 dated on or before 4 Nov | DFII10 ≤ 2.70 | 2.64 | not evaluable | DFII10 dated 2026-10-27: older than 7 days or missing |

## Bridge prices (asof = the bar date of the last price)

| symbol | last | 1d % | trend | dip_zone | asof |
|---|---|---|---|---|---|
| BZ=F | 93.06 | 1.72 | FLAT | False | 2026-11-11 |
| FRO | 45.61 | 3.97 | FLAT | False | 2026-11-11 |
| HG=F | 6.2815 | 1.0 | DOWN | True | 2026-11-11 |
| ZC=F | 447.0 | -0.45 | DOWN | True | 2026-11-11 |
| ZW=F | 599.25 | 1.1 | DOWN | True | 2026-11-11 |
| GC=F | 3997.7 | -0.81 | DOWN | False | 2026-11-11 |
| SI=F | 51.95 | 1.66 | DOWN | True | 2026-11-11 |
| NG=F | 3.231 | -1.97 | UP | True | 2026-11-11 |
| EWZ | 32.38 | 0.73 | DOWN | True | 2026-11-11 |
| SPY | 762.39 | 1.66 | FLAT | False | 2026-11-11 |
| BNO | 59.37 | 1.73 | FLAT | False | 2026-11-11 |
| SCO | 19.66 | -2.64 | FLAT | False | 2026-11-11 |
| GLD | 365.4 | -1.07 | DOWN | False | 2026-11-11 |
| CPER | 37.83 | 0.25 | DOWN | True | 2026-11-11 |
| COPX | 73.49 | 0.85 | DOWN | True | 2026-11-11 |
| CORN | 17.3 | -0.28 | DOWN | True | 2026-11-11 |
| WEAT | 22.12 | 1.75 | DOWN | True | 2026-11-11 |
| UNG | 10.2 | -2.06 | FLAT | False | 2026-11-11 |
| SLV | 46.83 | 0.74 | DOWN | True | 2026-11-11 |

Real-yield data (FRED) newest date: 2026-10-27; stale: True.
Gate legs not evaluable: fed real-yield leg.
