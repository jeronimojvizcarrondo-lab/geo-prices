# DESK STATUS — v6 Actions, code-rendered, no model

- v6 Actions 2026-11-22T23:33:53Z — status: OK
- Price file age: 46.6 hours (generated 2026-11-21T00:58:12Z, read from raw-url) — not stale.
- API spend this month so far: $0.00 (hard limit $92, today $0.00).
- Source health: 182 ok / 44 missing / 42 swapped; 1 skipped (key not set).
- Book 1: n=0 open=0 · mean R n/a · mean twin_R n/a · diff n/a · bootstrap 90% lower bound of diff n/a (10,000 resamples, seed 7) · max drawdown 0.00R · logged-before-fill 0/0 · open marks Σ +0.00R  //  Book 2: n=4 open=3 · mean R +0.36 · mean twin_R -0.56 · diff +0.92 · bootstrap 90% lower bound of diff +0.00 (10,000 resamples, seed 7) · max drawdown 2.04R · logged-before-fill 3/7 · open marks Σ +0.90R

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
  - (f) gate_inputs.json written 456 h ago (> 24 h)
  - (b) Hormuz war A: na
- oil short: (a) none in window
  - (f) gate_inputs.json written 456 h ago (> 24 h)
  - (b) Hormuz war B: na
- tankers long: (a) none in window
  - (f) gate_inputs.json written 456 h ago (> 24 h)
  - (b) Shadow-fleet sanctions B: na
- copper long: (a) none in window
  - (f) gate_inputs.json written 456 h ago (> 24 h)
  - (b) Chile copper labour B: na
- corn long: (a) none in window
  - (f) gate_inputs.json written 456 h ago (> 24 h)
  - (b) US harvest / grains B: fail
- wheat long: (a) none in window
  - (f) gate_inputs.json written 456 h ago (> 24 h)
  - (b) Black Sea / Ukraine B: fail
- gold long: (a) none in window
  - (f) gate_inputs.json written 456 h ago (> 24 h)
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
| oil short | Hormuz war B | BZ=F close <100 | BZ=F < 100 | 89.87 | true | BZ=F.last 89.87 bar 2026-11-20 |
| tankers long | Shadow-fleet sanctions B | = bridge FRO trend UP + DIP_ZONE | - | - | not evaluable | needs documents / counts / polls / other data the job cannot read |
| tankers long | Shadow-fleet sanctions B | a UKMTO warning number quoted by two outlets ≤72h — E7 ; today trend FLAT = not met | - | - | not evaluable | needs documents / counts / polls / other data the job cannot read |
| copper long | Chile copper labour B | = a company IR page or Sernageomin notice, dated after 16 Oct and ≤72h old, containing one mine name | - | - | not evaluable | needs documents / counts / polls / other data the job cannot read |
| copper long | Chile copper labour B | the word strike, huelga or paralización | - | - | not evaluable | needs documents / counts / polls / other data the job cannot read |
| copper long | Chile copper labour B | bridge HG=F DIP_ZONE with trend UP | - | - | not evaluable | needs documents / counts / polls / other data the job cannot read |
| corn long | US harvest / grains B | NASS Crop Progress corn harvested ≥5 pts behind the 5-yr average | - | - | not evaluable | needs documents / counts / polls / other data the job cannot read |
| corn long | US harvest / grains B | ZC=F close >500 | ZC=F > 500 | 448.75 | false | ZC=F.last 448.75 bar 2026-11-20 |
| wheat long | Black Sea / Ukraine B | port outage or Azov closure confirmed Tier 1 | - | - | not evaluable | needs documents / counts / polls / other data the job cannot read |
| wheat long | Black Sea / Ukraine B | ZW=F close >690 | ZW=F > 690 | 593.0 | false | ZW=F.last 593.0 bar 2026-11-20 |
| gold long | Fed / real yields A | = a treasury.gov/FRED DFII10 print ≤2.70 dated on or before 4 Nov | DFII10 ≤ 2.70 | 2.64 | not evaluable | DFII10 dated 2026-10-27: older than 7 days or missing |

## Bridge prices (asof = the bar date of the last price)

| symbol | last | 1d % | trend | dip_zone | asof |
|---|---|---|---|---|---|
| BZ=F | 89.87 | -2.29 | DOWN | True | 2026-11-20 |
| FRO | 45.21 | 1.03 | DOWN | True | 2026-11-20 |
| HG=F | 5.465 | -2.84 | DOWN | False | 2026-11-20 |
| ZC=F | 448.75 | 2.22 | DOWN | True | 2026-11-20 |
| ZW=F | 593.0 | 2.55 | DOWN | True | 2026-11-20 |
| GC=F | 3539.0 | -3.98 | DOWN | False | 2026-11-20 |
| SI=F | 41.08 | -7.31 | DOWN | False | 2026-11-20 |
| NG=F | 3.791 | 16.0 | UP | False | 2026-11-20 |
| EWZ | 28.54 | -3.29 | DOWN | False | 2026-11-20 |
| SPY | 689.81 | -3.64 | DOWN | False | 2026-11-20 |
| BNO | 59.02 | 0.31 | FLAT | False | 2026-11-20 |
| SCO | 20.54 | -0.44 | FLAT | False | 2026-11-20 |
| GLD | 322.87 | -3.67 | DOWN | False | 2026-11-20 |
| CPER | 32.92 | -2.49 | DOWN | False | 2026-11-20 |
| COPX | 56.33 | -4.98 | DOWN | False | 2026-11-20 |
| CORN | 16.9 | -1.0 | DOWN | False | 2026-11-20 |
| WEAT | 21.44 | -0.14 | DOWN | True | 2026-11-20 |
| UNG | 10.56 | 2.92 | FLAT | False | 2026-11-20 |
| SLV | 36.97 | -6.74 | DOWN | False | 2026-11-20 |

Real-yield data (FRED) newest date: 2026-10-27; stale: True.
Gate legs not evaluable: fed real-yield leg.
