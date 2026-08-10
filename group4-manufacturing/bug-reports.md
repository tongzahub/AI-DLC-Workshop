# Open Production Incidents — LineMetrics

> All numbers below were observed on the seeded September dataset
> (`python seed.py ../sample-readings.jsonl`, see `starter-code/README.md`).
> You should be able to reproduce every quoted value before you change any code.

## INC-1042 (P1) — Dashboard crashed during morning meeting

Reported by: Plant Manager, line L-05 · Tuesday 08:12

> Opened the OEE dashboard for Monday, got HTTP 500. Ops says the log shows `ZeroDivisionError` in the OEE endpoint. Monday was a planned maintenance day on L-05 (planned run time 0 minutes), so there were no cycles — but the dashboard for a maintenance day should show OEE "n/a" or 0, not crash the whole page for every line.

**Reproduce:** `GET /oee/L-05?date=2026-09-14` → 500 / `ZeroDivisionError`.

## INC-1043 (P2) — OEE total does not match manual calculation

Reported by: Production Engineer, line L-03

> I hand-calculated OEE for L-03 for three days from the shift logs and I get different numbers than the dashboard, always in the same direction (dashboard too high).
>
> Example, **15 Sep**: planned 480 min, downtime 45 min, ideal cycle time 0.5 min/piece, output 800 pieces (790 good).
> By hand: Availability = 435/480 = **0.9063**; Performance = (0.5×800)/435 = **0.9195**; Quality = 790/800 = **0.9875**; OEE = **0.8229**.
> The dashboard shows **OEE = 0.9011**.
>
> Here is the part I cannot explain: the dashboard's own displayed factors are availability 0.9062, performance 0.9126, quality 0.9874 — and **0.9126 × 0.9874 = 0.9011**, which is exactly the OEE it prints. It is as if one of the three factors never makes it into the total. Please find the root cause.
>
> (Separately, its performance factor is off from mine too — I think that is the night-shift problem in INC-1044, not this one. My worked numbers for **all three days** are in `expected-oee-l03.csv`; the dashboard must match them after the fix.)

**Reproduce:** `GET /oee/L-03?date=2026-09-15` → `{"availability": 0.9062, "performance": 0.9126, "quality": 0.9874, "oee": 0.9011}`.

## INC-1044 (P2) — Daily totals disagree with shift logs / phantom output

Reported by: Shift Supervisor, lines L-01 and L-07

> Two separate things, may or may not be related:
>
> **1. Wrong day.** Night-shift readings (after midnight, before 08:00) show up in the *wrong day's* report. Our production day runs 08:00 to 08:00 — a cycle at 07:30 on the 16th belongs to the 15th's production day. The report seems to cut at midnight — and I suspect not even midnight *our* time, because the numbers shift oddly around 07:00. On 15 Sep the shift log for L-03 says 800 pieces; the dashboard counted **794** — it dropped our last 41 pieces of the morning and picked up 35 pieces that belong to the 14th.
>
> **2. Phantom output.** On days with bad Wi-Fi on the shop floor, output counts are inflated — sometimes exactly double or triple for chunks of the day. On 15 Sep L-01 the dashboard reports **performance 1.6 and OEE 1.568**. An OEE above 100% is impossible; my shift log says 1,000 pieces, the dashboard counted 1,600. Vendor says the gateway retries POSTs but always with the same `reading_id`, so "your system should ignore the copies."

**Reproduce:** `GET /oee/L-01?date=2026-09-15` → `{"availability": 0.8333, "performance": 1.6, "quality": 0.98, "oee": 1.568}`.

---

Facilitator note to teams: reproduce each incident with a failing test first.
`sample-readings.jsonl` contains a gateway retry burst (L-01, L-07) and readings that cross the UTC midnight boundary on all three L-03 days.
`expected-oee-l03.csv` is the ground truth for L-03 after all fixes; `expected-oee-all-lines.csv` also covers L-01 (proves the de-duplication is numerically correct), L-07 and the L-05 maintenance day.
