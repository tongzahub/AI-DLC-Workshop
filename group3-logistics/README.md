# Group 3 · ParcelTrack

**COD Reconciliation & Merchant Webhooks for Thunder Express** — a brownfield change request.

The service in `starter-code/` is real, running and undocumented — the developer left, and three merchant platforms depend on its API exactly as it is. Your job is to extend it without breaking it, which starts with understanding it.

> **Read this file first.** It gets you from an empty machine to a running AI-DLC workflow.
> Your full brief is `Group3-Project-Brief.docx` — open it once setup is done.

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
python -m pytest                      # 3 passed - these must KEEP passing, unmodified
python seed_cod.py ../sample-cod-day.csv   # seeded 31 parcels and 30 COD collections
cd ..
```

Then start the merchant test receiver **in a second terminal** (standard library only, nothing
to install):

```
python webhook_receiver.py            # http://localhost:9410, merchant M-100
```

Python 3.12. The 3 existing tests must pass **before** you change anything — that is your
backward-compatibility baseline.

If any of that is not green, call the facilitator **now**, not at 14:00.

### 1.3 Verify the rules took

Open a **fresh** session in this folder and paste your trigger phrase (below). You should get
the AI-DLC welcome message, and after the first stage an `aidlc-docs/` folder appears here with
`aidlc-state.md` and `audit.md` in it. If not, the rules are in the wrong place — call the
facilitator.

> **Where to open your assistant:** here, at the group folder. Not in `starter-code/`.
> Everything the workflow needs to answer its own questions — the vision, the change request, the technical environment and the expected results — lives at this
> level. `starter-code/` is where the existing service lives — `pytest` and the seeders run from in there.

---

## 2 · Your trigger phrase

Paste this exactly, into a fresh session, in this folder:

```
Using AI-DLC, implement change request CR-2026-081 for the existing ParcelTrack service in this workspace: add merchant status webhooks and daily COD reconciliation, per vision-document.md and technical-environment.md. This is a brownfield project — analyze the existing code first.
```

Then let the workflow lead.

---

## 3 · What is in this folder

### Read these first, in this order

| # | File | Why |
|---|---|---|
| 1 | `Group3-Project-Brief.docx` | Your mission, the shape of the two days, the ground rules |
| 2 | `change-request.md` | **CR-2026-081, verbatim from Operations.** Your actual requirements input, including the acceptance demo they will ask you to run |
| 3 | `Group3-Business-Project-Memo.docx` | Why COD variance and WISMO calls matter enough to fund this |
| 4 | `Group3-Kickoff-Deck.pptx` | The same story as the memo, as the sponsor would present it |
| 5 | `vision-document.md` | Business context, scope, what is explicitly out |
| 6 | `technical-environment.md` | The brownfield boundary: what must not change, additive-only migrations, the webhook signature spec |

Read them **before** the AI asks its first question — but note what is *not* here: nobody can
tell you how the existing service works. That is what Reverse Engineering is for, and reviewing
what it produces is the first real work of the two days.

### The existing system

| | What it is |
|---|---|
| `starter-code/` | The running ParcelTrack service. `pip install -r requirements.txt`, then `uvicorn app.main:app`. It is undocumented on purpose |
| `starter-code/tests/` | Three tests that pass today. **They must still pass, unmodified, at every point** — that is your backward-compatibility baseline |
| `starter-code/seed_cod.py` | Loads a COD day into the existing tables: `python seed_cod.py ../sample-cod-day.csv`. Safe to re-run. It exists because `POST /parcels` generates its own ids, so the CSV's parcel ids cannot be created through the API |

### Data and tools you build against

| File | What it is |
|---|---|
| `sample-cod-day.csv` | 31 deliveries with Bangkok-local timestamps, including rows on both sides of the cutoff Finance described |
| `merchants.csv` | The three integrated merchants with their callback URL and webhook secret. Register these through your new API |
| `expected-cod-summary.csv` | **The answer key** — Finance's hand-worked figures for two settlement days |
| `webhook_receiver.py` | The merchant test receiver. Standard library only. Verifies your HMAC signature, and `--fail` makes it answer 500 so you can demo the retry path. `python webhook_receiver.py --help` |

### Files you fill in and hand back

| File | Who owns it |
|---|---|
| `team-log.md` | The Scribe, continuously — roles, decisions with the **why**, what Reverse Engineering found and what you decided to do about it, gate approvals, retro |
| `traceability-worksheet.md` | The whole team, Day 2 morning — five behaviours walked backwards to the sentence that caused them |
| `aidlc-docs/` | The workflow creates it, starting with the Reverse Engineering artifacts. Correct them where the AI guessed wrong — those corrections are scored |

See §7 for what "handing back" means.

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
   Finance explained how their day closes, over the reading the existing code implies" is worth everything.
6. **Rotate the keyboard.** Driver, Product Owner, Reviewer, Scribe — swap at least once per
   half day. Track it in `team-log.md`.

> **Your extension decision:** no extension is expected here — but record why, the same as
> any other decision.
>
> **The stage that matters most is the first one.** Let Reverse Engineering generate its
> artifacts before any feature work, then **review them critically**. At least two questionable
> patterns are in that code. Finding them is part of the exercise; so is deciding, on record,
> whether each one gets fixed, contained, or deliberately left alone.

---

## 5 · Expected shape of your two days

| When | You should be… |
|---|---|
| Day 1 morning | Reverse Engineering artifacts generated and **reviewed** — quirks found, decisions recorded; requirements from the CR |
| Day 1 afternoon | Execution plan approved — it should be leaner than a greenfield plan; challenge it if it is not. Design of webhooks + COD against the existing schema |
| Day 2 morning | Construction: webhook registration, signed delivery, retry with backoff, delivery log |
| Day 2 afternoon | COD summary endpoint; Build & Test; the acceptance demo from the CR — kill the receiver and watch the retries |

---

## 6 · Definition of Done

- The acceptance snapshot in `change-request.md` demos exactly as written — signed event within
  30 s, 5 retries visible after you stop the receiver, R-017 and R-023 flagged
- `GET /cod/summary?date=` matches `expected-cod-summary.csv` for **both 15 and 16 September**.
  Numeric columns and flags must match exactly; the `reason` column is explanatory text
- **All pre-existing tests pass unmodified**; existing endpoint responses byte-compatible
- New money fields are integer satang; any money-handling defect you find in the old code is at
  minimum documented with a remediation note
- Webhook events signed (HMAC-SHA256, `X-Tex-Signature`) and duplicate-tolerant by design
- **The finance screen works**: pick a date, see every rider's expected against recorded, the
  problem riders stand out without hunting, and a rider's day can be marked settled. It shows the
  same two days as `expected-cod-summary.csv`
- RE artifacts corrected by the team where the AI guessed wrong — corrections visible in `aidlc-docs/`

> **Build the screen last.** It sits on top of everything else, so a team that runs short still
> has a working, tested service to show. A team that starts with the screen has neither.

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
| The receiver answers 401 | Your HMAC does not verify. It accepts `sha256=<hex>` or a bare `<hex>`; the expected value is printed so you can compare. `--no-verify` disables the check while you wire up |
| You need to demo retries | `python webhook_receiver.py --fail` answers 500 every time, or just stop it with Ctrl-C |
| The seeded data disappeared | Re-run `python seed_cod.py ../sample-cod-day.csv` — it is safe to run repeatedly |
| You are tempted to rewrite something | Don't. The brief forbids it, and brownfield discipline is the lesson. Put that energy into the RE artifacts and the regression tests |

---

**Remember:** you are not judged on how much code you produce. You are judged on whether the
process would survive contact with a real project — gates honored, decisions recorded, nothing
vibe-coded — and on whether you can still explain, two days later, *why* your software does
what it does. Here that includes the things the previous developer never explained.
