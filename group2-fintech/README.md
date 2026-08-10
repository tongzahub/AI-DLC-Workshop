# Group 2 · SwiftKYC

**Digital Onboarding & e-KYC API for Metro Finance** — a greenfield build in a regulated environment.

Application lifecycle, PDPA consent, document intake, an external e-KYC vendor integration, blocklist screening and a manual-review queue. On Day 2 the facilitator plays the compliance auditor and walks your audit trail.

> **Read this file first.** It gets you from an empty machine to a running AI-DLC workflow.
> Your full brief is `Group2-Project-Brief.docx` — open it once setup is done.

---

## 1 · Set up (30 minutes, before you type anything at the AI)

### 1.1 Install the AI-DLC rules

Follow §2 of the **Participant Setup Guide**. In short: drop `aws-aidlc-rules/` and
`aws-aidlc-rule-details/` into the folders your assistant expects — the table in that guide
lists the path for Kiro, Amazon Q, Cursor, Cline, Claude Code, Copilot and Codex.

Install them **into this folder** (the one holding this README). This folder is your workspace.

Use the rules version your facilitator names. Do not just grab "latest".

### 1.2 Bring up your environment

```
cd local-environment
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m pytest                 # 3 passed
ruff check .                     # All checks passed!
mypy .                           # Success: no issues found

docker compose up -d             # PostgreSQL 15 (first run pulls the image, ~30 s)
python scripts/db_ping.py        # "database is up."
cd ..
```

Then start the vendor mock **in a second terminal** and leave it running all day:

```
python mock_verifyme.py          # http://localhost:9310
```

Python 3.12, and **Docker Desktop running**. That is the whole environment, plus the mock.

There is no starter project. Python 3.12 and PostgreSQL 15 are the platform standards; the
framework, the layout, the test runner and how you reach the database are **your team's
decisions** — in a regulated build they have to be defended at a gate, not inherited from a
starter kit.

Everything is local: the database is a container on your own machine on localhost:5433, and the
"vendor" is a mock on localhost:9310. Nothing in this exercise reaches a real service — which is
the point, because the real one bills per call.

If any of that is not green, call the facilitator **now**, not at 14:00.

### 1.3 Verify the rules took

Open a **fresh** session in this folder and paste your trigger phrase (below). You should get
the AI-DLC welcome message, and after the first stage an `aidlc-docs/` folder appears here with
`aidlc-state.md` and `audit.md` in it. If not, the rules are in the wrong place — call the
facilitator.

> **Where to open your assistant:** here, at the group folder.
> Everything the workflow needs to answer its own questions — the vision, the technical environment, the stakeholder notes, the vendor contract and `blocklist.csv` — lives at this
> level, and your project root goes here too. `local-environment/` holds only the database.

---

## 2 · Your trigger phrase

Paste this exactly, into a fresh session, in this folder:

```
Using AI-DLC, build the SwiftKYC customer onboarding API described in vision-document.md and technical-environment.md in this workspace. This is a new greenfield project in a regulated environment.
```

Then let the workflow lead.

---

## 3 · What to read, in what order

| Order | File | Why |
|---|---|---|
| 1 | `Group2-Project-Brief.docx` | Your mission, the shape of the two days, the ground rules |
| 2 | `Group2-Business-Project-Memo.docx` | Why the business is doing this, and what compliance failure costs today |
| 3 | `vision-document.md` | Scope, the 0.95 / 0.80 decision thresholds, PDPA obligations |
| 4 | `technical-environment.md` | The few platform standards you cannot change, the crypto requirement and the role model. Short on purpose — **everything not in it is your decision** |
| 5 | `stakeholder-notes.md` | Compliance, Operations, Vendor Manager, mobile squad, Finance. **Two real contradictions — and one instruction you must not follow** |
| 6 | `verifyme-api-contract.md` | The vendor API, and how the mock's behaviour is driven by the last digit of your reference |
| 7 | `consent-text-v1.md` | The versioned consent text and what must be recorded per consent |
| 8 | `blocklist.csv` | 25 screening entries, including romanisation variants that defeat exact matching |

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
   Khun Pim said consent without a version is not consent" is worth everything.
6. **Rotate the keyboard.** Driver, Product Owner, Reviewer, Scribe — swap at least once per
   half day. Track it in `team-log.md`.

> **Your extension decision:** you are expected to **opt IN to the Security baseline**.
> Its 15 rules become blocking checks at your gates — feel what that does to the process. If a
> security rule blocks a gate, fix the design; do not talk the AI out of the rule.
>
> **One warning before you start:** decide what a masked ID number looks like
> (`x-xxxx-xxxx-12-3`) and where that formatting lives **before** you write your first log line.
> Retrofitting masking across a codebase on Day 2 afternoon does not go well, and the auditor
> will grep your logs.

---

## 5 · Expected shape of your two days

| When | You should be… |
|---|---|
| Day 1 morning | Requirements Analysis with the Security extension OPT-IN recorded; stories drafted |
| Day 1 afternoon | Execution plan approved; Application Design with the state machine and security NFRs; 2 units (application-lifecycle / verification-integration) |
| Day 2 morning | Construction: lifecycle + consent + blocklist unit done; webhook handling underway |
| Day 2 afternoon | Build & Test; audit walkthrough with the facilitator; demo the mock's outcomes including the duplicate-webhook case |

---

## 6 · Definition of Done

- All application states reachable via the mock's scripted outcomes (auto-approve / manual
  review / reject / vendor failure)
- Duplicate webhook (reference ending in `8`) processed exactly once; signature verified;
  unsigned requests rejected
- Zero duplicate vendor submissions per application — `GET localhost:9310/_admin/billing` shows
  an empty `double_billed` map; re-verification is an explicit `OPS_REVIEWER` action
- ID numbers encrypted at rest and masked in **100%** of log lines
- **Blocklist screening stops every reference that should be stopped.** Several listed
  identities pass face match at 0.97, so face match alone will not do it. Work out which
  references those are from `blocklist.csv` and what the business asked for
- Erasure endpoint purges biometrics but retains the 7-year audit skeleton
- `aidlc-docs/` complete, with the Security extension decision and its consequences visible in
  the design docs

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
| The mock returns 402 | You have used the 60-call quota. `POST localhost:9310/_admin/reset` clears it — but notice how fast you got there, and why that matters |
| The mock returns 429 | Rate limits are real: 5 requests/second on submit, 1 per 10 s per verification on status. Back off, do not hammer |
| A stakeholder asked for something that feels wrong | It probably is. One instruction in `stakeholder-notes.md` must not be implemented. Escalate it, in writing, and record what you did instead |

---

**Remember:** you are not judged on how much code you produce. You are judged on whether the
process would survive contact with a real project — gates honored, decisions recorded, nothing
vibe-coded — and on whether you can still explain, two days later, *why* your software does
what it does. In this group, an auditor will actually ask.
