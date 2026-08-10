# Workshop Agenda — two days, four teams

> Clock times are the default plan; the facilitator may shift them on the day.
> The four in-room checkpoints are when the facilitator visits every team — be ready to
> show your `aidlc-docs/` and `team-log.md` as they are, not as you wish they were.

## Day 1 — from business intent to an approved plan

| Time | What | Notes |
|---|---|---|
| 08:30 – 09:00 | Arrival · toolchain check | §1.2 of your group README. Everything green **before** 09:00 |
| 09:00 – 09:30 | Opening briefing | Kickoff decks; how the two days are scored |
| 09:30 – 10:00 | Team reading, role split | PO: stakeholder notes + vision · Reviewer: tech-env + contracts · Driver: rules install · Scribe: opens `team-log.md`, assigns roles |
| 10:00 | **Trigger phrase** | Fresh session, group folder, pasted exactly |
| 10:00 – 12:00 | G1/G2: Requirements Analysis (extension decision **on record**) → User Stories · G3/G4: Reverse Engineering, reviewed critically | Answer in question files, never in chat |
| 11:45 | **Checkpoint 1** | Extension decision recorded? RE artifacts reviewed, not rubber-stamped? |
| 12:00 – 13:00 | Lunch | |
| 13:00 – 16:30 | G1: Workflow Planning → Application Design → Units · G2: plan → state machine + security NFRs → 2 units · G3: leaner plan (challenge it if it is not) → delta design · G4: lean plan (SKIPs justified) → failing regression tests ×3 | |
| 16:30 – 17:00 | **Checkpoint 2** · stand-down | Execution plan approved at a real gate? Scribe's decision log current? |

## Day 2 — from plan to proven software

| Time | What | Notes |
|---|---|---|
| 09:00 – 12:00 | Construction | G1: points-engine unit, then #2 · G2: lifecycle + consent + blocklist, webhooks underway · G3: webhook registration, signed delivery, retries · G4: the four fixes, tests red→green |
| 11:45 | **Checkpoint 3** | First unit complete? Ground truth partially reproducing? |
| 12:00 – 13:00 | Lunch | |
| 13:00 – 14:30 | Build & Test · match the ground truth | G1: replay vs `expected-points.csv` · G2: audit walkthrough prep, `/_admin/billing` clean · G3: CR acceptance snapshot · G4: property suite 1,000+ cases |
| 14:30 – 15:00 | **Checkpoint 4** · `traceability-worksheet.md` + retro notes | The worksheet is what your demo is built on — finish it **before** demoing |
| 15:00 – 16:20 | **Demos** — 4 teams × (10 min + 5 min Q&A) | 2 min acceptance scenario, then walk ONE number backwards to the sentence that caused it, then say where the chain broke |
| 16:20 – 16:50 | The comparison | All four execution plans side by side — same rules, four shapes. This is the point of the workshop |
| 16:50 – 17:00 | Retro share-out · close | 3 things AI-DLC did well · 3 frictions · 1 change before a real project |

## The four checkpoints in one line each

1. **Decisions started on record** — extension choice + first contradictions found
2. **A plan you actually argued with** — the gate was used, not clicked
3. **Software converging on ground truth** — at least one number already matches
4. **The chain is walkable** — worksheet done before the demo, honest breaks included
