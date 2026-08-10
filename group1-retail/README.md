# Group 1 · PointHub

**Loyalty Points & Rewards Service for Siam MegaMart** — a greenfield build.

One central points service behind an API, replacing three systems that disagree with each other. Yours is the richest Inception of the four groups: you start from nothing but business intent and four stakeholders who do not fully agree.

> **Read this file first.** It gets you from an empty machine to a running AI-DLC workflow.
> Your full brief is `Group1-Project-Brief.docx` — open it once setup is done.

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
cd starter-workspace
npm install           # ~470 packages, about 30 s
npm run typecheck     # silent = clean
npm test              # 1 suite, 3 tests passed
npm run lint          # silent = clean
cd ..
```

Node 20 or newer. All four commands must be green.

If any of that is not green, call the facilitator **now**, not at 14:00.

### 1.3 Verify the rules took

Open a **fresh** session in this folder and paste your trigger phrase (below). You should get
the AI-DLC welcome message, and after the first stage an `aidlc-docs/` folder appears here with
`aidlc-state.md` and `audit.md` in it. If not, the rules are in the wrong place — call the
facilitator.

> **Where to open your assistant:** here, at the group folder. Not in `starter-workspace/`.
> Everything the workflow needs to answer its own questions — the vision, the technical environment, the stakeholder notes and `sample-data/` — lives at this
> level. `starter-workspace/` is where the Node project lives — `npm test` and `npm run lint` run from in there.

---

## 2 · Your trigger phrase

Paste this exactly, into a fresh session, in this folder:

```
Using AI-DLC, build the PointHub loyalty points service described in vision-document.md and technical-environment.md in this workspace. This is a new greenfield project.
```

Then let the workflow lead.

---

## 3 · What to read, in what order

| Order | File | Why |
|---|---|---|
| 1 | `Group1-Project-Brief.docx` | Your mission, the shape of the two days, the ground rules |
| 2 | `Group1-Business-Project-Memo.docx` | Why the business is doing this, signed by the CCO. The success metrics come from here |
| 3 | `vision-document.md` | Scope, out-of-scope, success metrics — the primary input |
| 4 | `technical-environment.md` | Company stack, prohibited libraries, the points arithmetic, redemption parameters |
| 5 | `stakeholder-notes.md` | Raw interview notes from four stakeholders. **Contains the contradictions you must resolve** |
| 6 | `sample-data/campaign-examples.md` | The 5 campaigns your rules engine must handle, and the overlap traps |
| 7 | `sample-data/expected-points.csv` | The answer key. Your earn API must reproduce every row |

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
   Khun Nok said 'we'd go broke if they stack'" is worth everything.
6. **Rotate the keyboard.** Driver, Product Owner, Reviewer, Scribe — swap at least once per
   half day. Track it in `team-log.md`.

> **Your extension decision:** you are expected to **decline all three** extensions
> (Security, Resiliency, Property-Based Testing) — and to record *why* each one does not apply
> here. An unrecorded "no" scores the same as never having been asked.

---

## 5 · Expected shape of your two days

| When | You should be… |
|---|---|
| Day 1 morning | Through Requirements Analysis (extensions declined, on record) and into User Stories |
| Day 1 afternoon | Workflow Planning approved; Application Design and Units Generation done — expect 2–3 units, e.g. points-engine / campaign-management / reporting |
| Day 2 morning | Construction: points-engine unit complete (earn / burn / ledger with idempotency), second unit underway |
| Day 2 afternoon | Build & Test; demo — replay `transactions.csv` against your API and match `expected-points.csv` |

---

## 6 · Definition of Done

- Earn API reproduces **every row** of `sample-data/expected-points.csv` — best single
  multiplier, x2.5 held as the integer 2500, floor once per basket (**TX90007 is 29 points, not 27**)
- Refund clawback works for full **and** partial refunds (RF90001–3); negative balances allowed;
  every change is a ledger entry
- Earn is idempotent by `transactionId` — show the test that proves the POS retry is safe
- Point liability summary endpoint returns totals by tier, and replaying the whole file gives
  the eight member balances in `technical-environment.md`
- `aidlc-docs/` complete: requirements, stories, Mermaid execution plan, design, unit docs, audit trail

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
| Your points are off by one or two | You floored in the wrong place. Check `expected-points-by-line.csv` — it shows the milli-points per line so you can see which line disagrees |

---

**Remember:** you are not judged on how much code you produce. You are judged on whether the
process would survive contact with a real project — gates honored, decisions recorded, nothing
vibe-coded — and on whether you can still explain, two days later, *why* your software does
what it does.
