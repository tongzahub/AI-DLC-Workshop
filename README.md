# AI-DLC V1 Workshop Kit

A two-day workshop for running [AI-DLC](https://github.com/awslabs/aidlc-workflows) — the
AI-Driven Development Life Cycle — with four teams working four different kinds of engagement
at the same time.

Everything a team needs is in its own folder: the business documents, the seeded data, and an
answer key their software has to reproduce. Each team ships a working service **and one screen
on top of it**, so what they built is something you can look at rather than a `curl` transcript.
Everything runs on their own laptop.

> Built and verified against AI-DLC Workflows **v1.0.1**.

## The four groups

| | System | Engagement | What it exercises | Extension | Runs on |
|---|---|---|---|---|---|
| **1** | **PointHub** · retail loyalty points | Greenfield | The full path — richest Inception, 2–3 units of work | declines all, *on record* | Node 20 + Postgres in Docker |
| **2** | **SwiftKYC** · consumer-lending e-KYC | Greenfield, regulated | The full path with security as a blocking gate check | **Security** | Python 3.12 + Postgres in Docker |
| **3** | **ParcelTrack** · parcel tracking, COD & webhooks | Brownfield change request | Reverse Engineering first, then a lean plan, zero breaking changes | none | Python 3.12 + the running service provided |
| **4** | **LineMetrics** · plant OEE service | Brownfield bug fix | Most stages **skipped** — pushing back on an over-sized plan is the exercise | **PBT** | Python 3.12 + the running service provided |

The point of running all four at once: nobody configures the difference. Same rules, four
execution plans, because Workflow Planning proposes a path from the shape of the problem. Day 2
puts the four plans side by side.

### What each group is measured against

| | Answer key | Checked with | The screen it ships with |
|---|---|---|---|
| 1 | `sample-data/expected-points.csv` — 40 sales + 3 refunds | `node sample-data/check-points.mjs your-output.csv` | customer-service lookup: balance, tier, history with the reason for each entry |
| 2 | the vendor mock's scripted outcomes | `GET localhost:9310/_admin/billing` | operations review queue, plus the compliance view the Day-2 auditor is walked through |
| 3 | `expected-cod-summary.csv` — two settlement days | `GET /cod/summary?date=` | finance reconciliation: per-rider expected vs recorded, problems flagged, mark settled |
| 4 | `expected-oee-l03.csv`, `expected-oee-all-lines.csv` | `GET /oee/{line}?date=` | the OEE dashboard INC-1042 is about — one bad line must not take the page down |

Every one of those screens was asked for by a stakeholder in that group's own documents. The
number the screen displays is the number in the answer key, which is what makes the Day-2 demo
something to look at instead of something to read out.

The answer keys ship **with** the teams on purpose. Building software that reproduces a
known-correct number is the exercise; guessing what the number should be is not.

## Using it

**As a participant** — read your group's `README.md`. One file gets you from an empty machine to
a running workflow: the trigger phrase, the setup commands with their expected output, what to
read in what order, and a troubleshooting table.

**As a facilitator** — hand each team **only its own group folder**, plus
`Participant-Setup-Guide.docx`, `AI-DLC-Cheat-Sheet.md` and `Workshop-Agenda.md`. Send
`Pre-Workshop-Checklist.md` two or three days ahead. Teams run `git init` **inside their group
folder**; they do not clone this repo, because committing `aidlc-docs/` is one of their
deliverables and belongs in their own history.

Everything needed to *run* the two days — the pre-flight, the in-room checkpoints, the answer
sheet, the rubric, the opening deck and the client report — is in a separate **private**
repository, `AIDLC-Workshop-Facilitator`. It holds the material that would spoil the exercise,
so nothing from it should ever reach a participant.

Groups 1 and 2 need **Docker Desktop** for their database. Groups 3 and 4 need nothing beyond
Python. No cloud account, no deployment, no infrastructure.

## What is deliberately missing

**Groups 1 and 2 get no starter project** — not even a `package.json`. Their
`local-environment/` folder holds a compose file that gives them an empty PostgreSQL, and
nothing else. Framework, project layout, test runner and database access are decisions their
Application Design has to produce and defend at a gate — which is what the tech half of the room
is there to do. Their technical environment names three platform standards and two prohibitions,
and is otherwise silent.

**No document settles a business rule.** How campaigns combine, where rounding happens, what a
refund reverses, when a settlement day starts — none of it is written down as fact anywhere. The
answers live in stakeholder interviews, incident tickets and change requests, in the words of
people who sometimes contradict each other and once ask for something the team should refuse.

That is what makes the second half of Day 2 work. A team picks one number its software
produces and walks it backwards, out loud:

```
a number you can point at
  └─ the test that would fail if the decision flipped
      └─ the design, the requirement, the recorded decision
          └─ the answer someone typed into a question file
              └─ the sentence a stakeholder actually said
```

There are eighteen of those chains in the kit. What they are is not written anywhere a team can
read — finding them is the exercise. Teams reconstruct their own in
`traceability-worksheet.md`, and that worksheet, not a score, is what they take home.

## Everything here is fabricated

Every company, person, quotation, transaction, incident ticket, ID number and blocklist entry is
invented for teaching. Siam MegaMart, Metro Finance, Thunder Express and Apex Auto Parts do not
exist. The Thai national ID numbers are correctly formatted 13-digit values, but **every one of
them deliberately fails the national-ID check digit**, so none can belong to a real person, and
`blocklist.csv` is not derived from any real sanctions list. The API keys and webhook secrets
(`demo-key-123`, `demo-secret`, `whsec_*`) belong to mock servers that only listen on localhost.

## Layout

```
Participant-Setup-Guide.docx   installing the rules, driving the workflow, what is expected
AI-DLC-Cheat-Sheet.md          one-page map of stages, gates and extensions
Workshop-Agenda.md             the two-day timetable
Pre-Workshop-Checklist.md      goes out 2–3 days before Day 1

group1-retail/          PointHub      greenfield
group2-fintech/         SwiftKYC      greenfield, regulated
group3-logistics/       ParcelTrack   brownfield change request
group4-manufacturing/   LineMetrics   brownfield bug fix
```

Each group folder also carries `team-log.md` (decisions, gates, retro) and
`traceability-worksheet.md`.

## Changing the kit

Three files are generated, and each one is coupled to an answer key:

```
group1-retail/sample-data/transactions.csv   ─→ expected-points.csv (+ the per-line breakdown)
group3-logistics/sample-cod-day.csv          ─→ expected-cod-summary.csv
group4-manufacturing/sample-readings.jsonl   ─→ expected-oee-*.csv
```

Hand-editing the left-hand side silently invalidates the right, and nobody notices until a team
argues about a number on Day 2. Regenerate, then run `tools/verify_kit.py` from the facilitator
repository — it recomputes every answer key from source, re-checks the mock's identities and the
ID check digits, and exits non-zero on drift.

Changing a business rule means changing four things together: the data, the technical
environment, the stakeholder note or ticket it came from, and the matching row in the
facilitator repo's traceability map. Each chain only teaches something while all four agree.
