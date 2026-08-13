# Vision: LineMetrics Incident Fixes & Hardening (Apex Auto Parts)

> Workshop Group 4 · **Brownfield bug fix + hardening** — starter codebase provided in `starter-code/`
> Expected AI-DLC path: lightweight (several stages SKIPPED by Workflow Planning) · Property-Based Testing extension expected: **OPT IN**
> Trigger phrase: *"Using AI-DLC, fix the production incidents in bug-reports.md for the LineMetrics service in this workspace and harden it against recurrence. This is a brownfield project."*

## Executive Summary

Apex Auto Parts (fictional) runs 8 production lines; each line's PLC gateway posts machine-cycle readings to the LineMetrics service, which computes OEE (Overall Equipment Effectiveness) dashboards that plant managers use in the 08:00 morning meeting. Three production incidents are open: OEE numbers are wrong on some lines, daily reports disagree with shift logs, and last Tuesday the dashboard crashed during the morning meeting. Management has lost trust in the numbers. The goal is to fix all three incidents, prove the fixes with strong tests (the team should opt in to Property-Based Testing), and leave the service documented.

## Business Context

- OEE = Availability × Performance × Quality — the plant's core KPI; bonuses partially depend on it. Wrong numbers are a labor-relations problem, not just a technical one.
- Gateways retry aggressively on flaky Wi-Fi (up to 3 duplicate posts) — the vendor confirms retries reuse the same `reading_id`.
- The plant operates on Asia/Bangkok time; a production "day" is 08:00 → 08:00 (next calendar day), matching shift A start.
- The original developer left. Only the code and the failing dashboards remain.

## In Scope

1. Diagnose and fix the 3 incidents in `bug-reports.md` (root cause, fix, regression tests).
2. Add ingestion idempotency guaranteed at the service (dedupe by `reading_id`).
3. Correct OEE calculation, safe for edge cases (zero planned time, zero output, downtime > planned).
4. Correct day-boundary logic (08:00 Asia/Bangkok production day).
5. Property-based tests for: OEE bounds (each factor and OEE always within [0,1]), ingestion idempotency (posting a batch once vs. with duplicates yields identical daily numbers), and day-bucketing invariants (every reading lands in exactly one production day).
6. **The OEE dashboard itself.** INC-1042 is a report about a *page*, not an endpoint — "the dashboard for a maintenance day should show OEE n/a or 0, not crash the whole page for every line". That page was never in version control, so rebuilding it is part of closing the incident: one screen showing every line for a chosen production day, where a line with no data degrades on its own without taking the others down.
7. A one-page RUNBOOK.md for the ops team.

## Explicitly Out of Scope

- New endpoints or features beyond the three incidents. The dashboard is not a new feature — it is the thing INC-1042 is about
- Changing the gateway payload contract (vendor firmware is frozen)
- Performance work (volumes are small)

## Key Success Metrics

- All three incidents reproduced by a failing test **before** the fix, passing after
- The plant manager can open the dashboard on the morning of a maintenance day and still read every other line
- Recomputed daily OEE for line L-03 matches the hand-calculated values in `expected-oee-l03.csv` for **all three** production days (14, 15, 16 September)
- Every other seeded line/day matches `expected-oee-all-lines.csv` — in particular L-01 on 15 Sep, which today reports an impossible OEE of 1.568 and must come out at 0.8167
- Property-based test suite passes 1,000+ generated cases with no invariant violations

## Open Questions (expect the AI to ask)

- When downtime > planned minutes (data entry error), clamp availability to 0 or reject the record?
- Should duplicate `reading_id` with *different* payloads be dropped, versioned, or alarmed?
- Are historical (already-stored) duplicates to be cleaned up, or fix-forward only?
