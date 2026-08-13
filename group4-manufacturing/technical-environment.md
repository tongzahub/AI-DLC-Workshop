# Technical Environment: LineMetrics — Apex Auto Parts

> **Brownfield.** Existing stack is the baseline (see `starter-code/`). This is a fix-and-harden engagement, not a rewrite.

## The existing stack

Whatever `starter-code/` is running on. The developer who wrote it left, and the only
documentation is the code and three failing dashboards. **Reverse Engineering is how you find
out** — read what it produces before you trust it.

What the plant can tell you is the boundary: **fix it in place.** Same language, same framework,
same database. This is an incident response, not a rewrite. Hypothesis is already in
`requirements.txt`, unused — the PBT extension will put it to work.


## Hard Rules

- Gateway payload contract is frozen (vendor firmware): field names/types of `POST /readings` must not change.
- `GET /oee/{line_id}?date=` response may gain fields but must keep existing ones.
- Idempotency: same `reading_id` ingested any number of times must yield identical stored state and identical daily numbers. Decide (and document) behavior when the same `reading_id` arrives with a different payload.
- **Reported values carry 4 decimal places, and they must match the plant's own hand calculations exactly** — the engineers check the dashboard against figures they worked out themselves, and `expected-oee-l03.csv` is those figures. If your fourth decimal is off by one, the difference is real and worth understanding before you paper over it.
- Every fix needs: a failing regression test first, the fix, and the test passing — plus property-based tests per the vision doc.

## The screen

One user interface is in scope (see the vision document). The platform team has exactly two
rules about it, and no opinion on anything else:

- **It is served by your own service and runs in a browser on this laptop.** No separate
  frontend server, no deployment, no build pipeline required.
- **Nothing is fetched from the internet at runtime.** No CDN for a framework, a font or an
  icon set — the venue Wi-Fi is not part of your architecture, and the demo has to work when it
  is not there.

Framework or no framework, one page or several, a build step or plain files served as-is —
that is a design decision like any other. Make it, record why, and be ready to defend it at a
gate. A single page your API serves is a completely respectable answer for two days of work.

The dashboard is what INC-1042 is about. `GET /oee/{line_id}?date=` may gain fields but must
keep the ones it already returns — the page is a new consumer of that endpoint, not a reason to
change it.

The page shows every line for one production day; that endpoint answers for one line. Calling it
once per line is fine at this scale. Adding an endpoint that answers for all lines is also fine —
it is additive and breaks nothing — but it is a decision, so record why you made it.


## Prohibited

| Prohibited | Use Instead |
|---|---|
| Rewriting to another framework/DB | fix in place |
| Fixing numbers by post-processing in the endpoint | fix the calculation/bucketing at the source |
| Deleting the existing tests | extend them — and account for what they were and were not asserting |

## Provided Data

- `sample-readings.jsonl` + `starter-code/seed.py` — seeds the September plan & readings for L-01/L-03/L-05/L-07, including a gateway retry burst and readings that cross UTC midnight. Run from `starter-code/`: `python seed.py ../sample-readings.jsonl`
- `expected-oee-l03.csv` — hand-calculated ground truth for L-03 on 14/15/16 September; the fixed service must reproduce all three rows exactly
- `expected-oee-all-lines.csv` — the same ground truth for every seeded line/day, including L-01 (proves de-duplication is numerically correct, not just "no crash") and the L-05 maintenance day where all four values are undefined
- `bug-reports.md` — the three incident tickets (your actual requirements input)

Seeding is idempotent: `seed.py` clears `readings` and `plan` before loading, so running it twice must not change any reported number.
