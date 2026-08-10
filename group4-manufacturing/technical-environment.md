# Technical Environment: LineMetrics — Apex Auto Parts

> **Brownfield.** Existing stack is the baseline (see `starter-code/`). This is a fix-and-harden engagement, not a rewrite.

## Existing Stack (must be preserved)

| Layer | Technology | Notes |
|---|---|---|
| Language | Python 3.12 | |
| API framework | FastAPI + Pydantic v2 | |
| Database | SQLite via SQLAlchemy Core | keep it |
| Tests | pytest (2 exist and pass — keep them passing, note: they never caught the bugs, ask why) |
| PBT library | Hypothesis (in requirements, unused so far) | the PBT extension rules will put it to work |

## Hard Rules

- Gateway payload contract is frozen (vendor firmware): field names/types of `POST /readings` must not change.
- `GET /oee/{line_id}?date=` response may gain fields but must keep existing ones.
- Production day = 08:00 Asia/Bangkok → 08:00 next day. All day-bucketing must use this rule.
- Idempotency: same `reading_id` ingested any number of times must yield identical stored state and identical daily numbers. Decide (and document) behavior when the same `reading_id` arrives with a different payload.
- **Rounding: 4 decimal places, ROUND_HALF_UP** — the plant's Excel sheet has always rounded half-up and the ground-truth file was hand-calculated that way. Python's built-in `round()` uses banker's rounding and will give you `0.9062` where the shift log says `0.9063`; use `decimal.Decimal(...).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)`.
- **Round only at the edge.** Compute availability × performance × quality at full precision and round the result; do not multiply already-rounded factors (that gives 0.8228 instead of 0.8229 on 15 Sep).
- Every fix needs: a failing regression test first, the fix, and the test passing — plus property-based tests per the vision doc.

## Prohibited

| Prohibited | Use Instead |
|---|---|
| Rewriting to another framework/DB | fix in place |
| Fixing numbers by post-processing in the endpoint | fix the calculation/bucketing at the source |
| Deleting the existing tests | extend them; discuss why they missed the bugs (test-gap analysis is part of the workshop) |

## Provided Data

- `sample-readings.jsonl` + `starter-code/seed.py` — seeds the September plan & readings for L-01/L-03/L-05/L-07, including a gateway retry burst and readings that cross UTC midnight. Run from `starter-code/`: `python seed.py ../sample-readings.jsonl`
- `expected-oee-l03.csv` — hand-calculated ground truth for L-03 on 14/15/16 September; the fixed service must reproduce all three rows exactly
- `expected-oee-all-lines.csv` — the same ground truth for every seeded line/day, including L-01 (proves de-duplication is numerically correct, not just "no crash") and the L-05 maintenance day where all four values are undefined
- `bug-reports.md` — the three incident tickets (your actual requirements input)

Seeding is idempotent: `seed.py` clears `readings` and `plan` before loading, so running it twice must not change any reported number.
