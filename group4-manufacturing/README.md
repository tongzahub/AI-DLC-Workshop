# Group 4 · LineMetrics

**Production Incident Fixes for Apex Auto Parts** — a brownfield bug fix and hardening.

Three incidents are open on the service that computes the plant's OEE — the KPI its bonuses depend on. This is the smallest codebase of the four groups, deliberately. Your workshop is about precision: root-cause each ticket, prove it with a failing test first, fix it, then make the bug class unreachable.

> **Read this file first.** It gets you from an empty machine to a running AI-DLC workflow.
> Your full brief is `Group4-Project-Brief.docx` — open it once setup is done.

---

## 1 · Set up (30 minutes, before you type anything at the AI)

### 1.1 Install the AI-DLC rules

Follow §2 of the **Participant Setup Guide**. In short: drop `aws-aidlc-rules/` and
`aws-aidlc-rule-details/` into the folders your assistant expects — the table in that guide
lists the path for Kiro, Amazon Q, Cursor, Cline, Claude Code, Copilot and Codex.

Install them **into this folder** (the one holding this README). This folder is your workspace.

Use the rules version your facilitator names. Do not just grab "latest".

### 1.2 Check your toolchain

```
cd starter-code
pip install -r requirements.txt
python -m pytest                          # 2 passed - and they never caught any of the bugs
python seed.py ../sample-readings.jsonl   # seeded 6 plan rows and 97 readings
cd ..
```

Then reproduce all three incidents before you change a line — with the service running
(`uvicorn app.main:app --reload` from `starter-code/`):

| Call | What you should see |
|---|---|
| `GET /oee/L-05?date=2026-09-14` | HTTP 500, `ZeroDivisionError` — INC-1042 |
| `GET /oee/L-03?date=2026-09-15` | `oee: 0.9011` where the shift log says 0.8229 — INC-1043 |
| `GET /oee/L-01?date=2026-09-15` | `oee: 1.568` — an OEE above 100% — INC-1044 |

Python 3.12. If those three do not reproduce, the seed did not take.

If any of that is not green, call the facilitator **now**, not at 14:00.

### 1.3 Verify the rules took

Open a **fresh** session in this folder and paste your trigger phrase (below). You should get
the AI-DLC welcome message, and after the first stage an `aidlc-docs/` folder appears here with
`aidlc-state.md` and `audit.md` in it. If not, the rules are in the wrong place — call the
facilitator.

> **Where to open your assistant:** here, at the group folder. Not in `starter-code/`.
> Everything the workflow needs to answer its own questions — the vision, the incident tickets, the technical environment and the expected results — lives at this
> level. `starter-code/` is where the existing service lives — `pytest` and the seeder run from in there.

---

## 2 · Your trigger phrase

Paste this exactly, into a fresh session, in this folder:

```
Using AI-DLC, fix the production incidents described in bug-reports.md for the LineMetrics service in this workspace and harden it against recurrence, per vision-document.md and technical-environment.md. This is a brownfield project — analyze the existing code first.
```

Then let the workflow lead.

---

## 3 · What to read, in what order

| Order | File | Why |
|---|---|---|
| 1 | `Group4-Project-Brief.docx` | Your mission, the shape of the two days, the ground rules |
| 2 | `bug-reports.md` | The three incident tickets — **these are your requirements input**, with the exact numbers to reproduce |
| 3 | `Group4-Business-Project-Memo.docx` | Why wrong OEE is a labour-relations problem, not just a technical one |
| 4 | `vision-document.md` | Context, the 08:00→08:00 production-day rule, scope limits |
| 5 | `technical-environment.md` | Frozen gateway contract, the rounding rule, prohibited shortcuts |
| 6 | `starter-code/` | The service. Small enough to read completely — do that |
| 7 | `expected-oee-l03.csv` + `expected-oee-all-lines.csv` | The hand-calculated ground truth your fixes must reproduce |

Read them **before** the AI asks its first question. Almost every answer it wants is already
in these files — including the places where they contradict each other.

---

## 4 · How to work (the six rules)

1. **Answer in files, not in chat.** The AI writes questions into markdown files with lettered
   options and an `[Answer]:` tag. Open the file, type after the tag, save, tell the AI you are
   done. Answering in chat costs you points the second time the facilitator sees it.
2. **Read before you approve.** Every stage ends at a gate with two options — Continue, or
   Request Changes. Actually open the artifacts it points at. A gate you rubber-stamp is a gate
   you did not use.
3. **Never vibe code.** No editing files outside the workflow. If you do it anyway, tell the AI
   so the docs and state stay true. Undeclared hand edits are audit findings.
4. **Source your answers.** From the documents in section 3. Where they conflict, the Product
   Owner decides and the Scribe records **why** in `team-log.md`.
5. **Record the why, not just the what.** "We chose b" is worth nothing. "We chose b because
   the shift supervisor said a cycle at 07:30 belongs to the previous day" is worth everything.
6. **Rotate the keyboard.** Driver, Product Owner, Reviewer, Scribe — swap at least once per
   half day. Track it in `team-log.md`.

> **Your extension decision:** you are expected to **opt IN to Property-Based Testing**.
> Three regression tests fix three bugs; property tests make the whole class unreachable.
>
> **Watch what Workflow Planning does with a bug-fix request.** It should SKIP most of the heavy
> stages. If it proposes a full greenfield plan — User Stories, Application Design, Units
> Generation — **push back at the gate**. That push-back *is* the exercise for this group.

---

## 5 · Expected shape of your two days

| When | You should be… |
|---|---|
| Day 1 morning | Reverse Engineering + root-cause analysis: all three tickets mapped to code with evidence; PBT extension OPT-IN recorded |
| Day 1 afternoon | Lean execution plan approved (most stages SKIPPED, with rationale); failing regression tests written for all three incidents |
| Day 2 morning | Fixes in: OEE composition, zero-division safety, Bangkok production-day bucketing, `reading_id` idempotency, half-up rounding |
| Day 2 afternoon | Property suite green over 1,000+ cases; L-03 matches ground truth; `RUNBOOK.md`; demo = live replay of each ticket |

---

## 6 · Definition of Done

- `GET /oee/L-03?date=` returns the values in `expected-oee-l03.csv` for **all three days** —
  on 15 Sep: availability 0.9063 / performance 0.9195 / quality 0.9875 / **OEE 0.8229**
  (round HALF-UP to 4 dp, and round the product — not already-rounded factors)
- Maintenance day (L-05, planned 0) returns a sane response, not a 500
- Seeding the retry burst twice changes nothing (idempotency proven by test), and **L-01 on
  15 Sep comes out at 0.8167 instead of 1.568**
- Property tests: every OEE factor and total always in [0,1]; every reading in exactly one
  production day
- The original 2 tests still pass, **plus your team's written answer to: why did they never
  catch these bugs?**
- `RUNBOOK.md` — one page ops can actually use

---

## 7 · What you hand in

- **`aidlc-docs/`** — state file, audit trail, requirements, stories, execution plan (with the
  Mermaid diagram), design, per-unit docs
- **Working code with passing tests**, in this folder
- **`team-log.md`** — decisions with the why, contradictions you found and how you resolved
  them, gate approvals, any hand edits, retro. Fill it in **as you go**; reconstructing it on
  Day 2 afternoon does not convince anyone
- **`traceability-worksheet.md`** — five behaviours of your system walked backwards to the
  sentence that caused each one, plus an honest note on where your chain broke
- **The Day-2 demo, 10 minutes** — run your acceptance scenario for two minutes, then pick ONE
  number your software produces and walk it backwards, out loud, to the sentence someone said
  that caused it. Then say where the chain broke

---

## 8 · When you are stuck

| Symptom | Do this |
|---|---|
| No welcome message / no `aidlc-docs/` | Rules are in the wrong folder for your assistant. Check the table in the Participant Setup Guide, then start a **fresh** session |
| The AI keeps asking the same thing | Your answer was vague. That follow-up clarification file is the system working — answer it more specifically |
| The AI proposes something your tech environment prohibits | Say so at the gate and point at the rule. Do not silently accept it, and do not switch the rule off |
| You cannot answer a question from the documents | Record an assumption, say it is an assumption, and move on. Timebox it — an honest recorded assumption scores better than twenty minutes of debate |
| Kiro suggests switching to Spec mode | Decline. Stay in Vibe mode; AI-DLC replaces that workflow |
| You get 0.9062 where the answer key says 0.9063 | Python's built-in `round()` is banker's rounding. The plant's Excel sheet rounds **half-up**, and so must you: `Decimal(x).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)` |
| You get 0.8228 instead of 0.8229 | You multiplied already-rounded factors. Round once, at the product |
| The numbers still look wrong after one fix | The bugs interact. INC-1044's day-bucketing changes the inputs INC-1043 is computed from — fix them in the order the evidence supports, not the order they are numbered |
| Tempted to correct the number in the endpoint | Prohibited. Fix the calculation and the bucketing at the source |

---

**Remember:** you are not judged on how much code you produce. You are judged on whether the
process would survive contact with a real project — gates honored, decisions recorded, nothing
vibe-coded — and on whether you can still explain, two days later, *why* your software does
what it does. Management stopped trusting these numbers once; the explanation is the product.
