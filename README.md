# AI-DLC V1 Workshop Kit

A two-day, four-team workshop for running [AI-DLC](https://github.com/awslabs/aidlc-workflows)
— the AI-Driven Development Life Cycle — on realistic engagements.

Each team takes a different kind of work from business intent to tested, documented software:
one greenfield service, one greenfield regulated build, one brownfield change request, one
brownfield bug fix. Same methodology, four deliberately different shapes.

> Built and verified against AI-DLC Workflows **v1.0.1**.

## What the two days are designed to demonstrate

**1 · The workflow adapts to the work.** Nobody configures the difference. Four teams run the
same rules and produce four different execution plans, because Workflow Planning proposes a
path from the shape of the problem and the team defends or changes it at a gate. Day 2 puts
all four plans side by side; that comparison is the point of the workshop.

**2 · Every behaviour traces back to a sentence someone said.** The kit is built around 18
closed loops — a stakeholder quotation, the decision a team has to record, and a single number
in the running software you can point at. For example:

| Someone said | The software says |
|---|---|
| *"Today the POS rounds down per basket"* — Khun Beer, POS lead | **TX90007 posts 29 points**, not 27 |
| *"Just approve it and we'll check later"* — Khun Arm, Operations | **MANUAL_REVIEW** — the team refused the instruction |
| *"Our day closes at 20:00"* — Finance | **3 rows** in the 16 September COD summary |
| *"Your system should ignore the copies"* — the gateway vendor | **OEE 0.8167**, not the impossible 1.568 |

Teams reconstruct those chains themselves in `traceability-worksheet.md` and walk one of them,
backwards, in their demo. That worksheet — not a score — is what they take home.

## This is the participant half of a two-repository kit

Everything here is safe for participants to read. The material that would spoil the exercise —
the seeded defects, the model answers, the traceability answer sheet, the rubric and the
facilitator's own deck — lives in a **separate private repository**, `AIDLC-Workshop-Facilitator`.

If you are facilitating, clone the two side by side:

```
your-workspace/
  AIDLC-Workshop-Kit/          <- this repo
  AIDLC-Workshop-Facilitator/  <- private; its checks expect the kit as a sibling
```

Participants get **only their own group folder** plus `Participant-Setup-Guide.docx`, by USB or
zip. They run `git init` **inside their group folder** — they do not clone this repo, because
committing `aidlc-docs/` is one of their deliverables and belongs in their own history.

Nothing in this repository reveals the answers to another group's exercise. The answer-key CSVs
are deliberately included: reproducing a known-correct number is the exercise, and guessing what
the number should be is not.

## Everything here is fabricated

Every company, person, quotation, transaction, incident ticket, ID number and blocklist entry
is invented for teaching. Siam MegaMart, Metro Finance, Thunder Express and Apex Auto Parts do
not exist. The Thai national ID numbers are correctly formatted 13-digit values but **every one
of them deliberately fails the national-ID check digit**, so none can belong to a real person;
`blocklist.csv` is not derived from any real sanctions list. The API keys and webhook secrets
(`demo-key-123`, `demo-secret`, `whsec_*`) belong to mock servers that only listen on localhost.

## Layout

```
Participant-Setup-Guide.docx   how to install the rules, drive the workflow, what is expected

group1-retail/          PointHub    · retail loyalty points        · greenfield
group2-fintech/         SwiftKYC    · consumer-lending e-KYC       · greenfield, regulated
group3-logistics/       ParcelTrack · parcel tracking COD/webhooks · brownfield change request
group4-manufacturing/   LineMetrics · plant OEE service            · brownfield bug fix
```

Every group folder starts with its own `README.md` — a team can read that one file and be
running AI-DLC in half an hour. It carries the trigger phrase, the toolchain checks with their
expected output, the reading order, the ground rules and a troubleshooting table.

## The four groups

| | System | Engagement | Path it exercises | Extension | Stack |
|---|---|---|---|---|---|
| **1** | PointHub | Greenfield service | Full Inception → 2–3 units | declines all — *on record* | TypeScript 5.5 / Node 20 / Express / Postgres |
| **2** | SwiftKYC | Greenfield, regulated | Full path, security NFRs dominate design | **Security** OPT-IN | Python 3.12 / FastAPI / Postgres |
| **3** | ParcelTrack | Brownfield CR | Reverse Engineering → targeted stages, zero breaking changes | none | Python 3.12 / FastAPI / SQLite *(provided, running)* |
| **4** | LineMetrics | Brownfield bug fix | Minimal path — most stages SKIP | **PBT** OPT-IN | Python 3.12 / FastAPI / SQLite *(provided, with seeded bugs)* |

### What each group works in, runs, and is measured against

| | Works in | Runs | Ground truth |
|---|---|---|---|
| 1 | `starter-workspace/` — Node 20 + TS toolchain, no `src/` layout | — | `sample-data/expected-points.csv` — 40 sales + 3 refunds |
| 2 | `starter-workspace/` — Python 3.12 toolchain, no app layout | `python mock_verifyme.py` | the mock's scripted outcomes + `GET /_admin/billing` |
| 3 | `starter-code/` — the running service | `starter-code/seed_cod.py`, `webhook_receiver.py` | `expected-cod-summary.csv` — 2 settlement days |
| 4 | `starter-code/` — the running service | `starter-code/seed.py` | `expected-oee-l03.csv`, `expected-oee-all-lines.csv` |

The starter workspaces for groups 1 and 2 hold **toolchain only** — linters, test runners and
the prohibitions from their technical environment, but no application structure. Designing that
is what the workflow is for.

The answer keys are participant material on purpose: the exercise is building software that
reproduces a known-correct number, not guessing what the number should be. Every value in them
has been recomputed against the shipped data and reproduced against the shipped code.

Each group folder also carries `team-log.md` (decision log, gate record, retro) and
`traceability-worksheet.md`.

## Facilitating

Everything you need to run the two days is in the private `AIDLC-Workshop-Facilitator`
repository — the day-before pre-flight, the four in-room checkpoints, the answer sheet, the
rubric, the opening deck and the client report template. Start with its README.

The one thing to know here: **pin the rules version.** Re-check the newest release of
`awslabs/aidlc-workflows` and make sure `Participant-Setup-Guide.docx` agrees with what you hand
out. If stage names have moved, the workshop checkpoints will not line up.

## Maintaining the kit

Five files are **generated and coupled to an answer key**:

```
group1-retail/sample-data/transactions.csv     ─→ expected-points.csv, expected-points-by-line.csv
group3-logistics/sample-cod-day.csv            ─→ expected-cod-summary.csv
group4-manufacturing/sample-readings.jsonl     ─→ expected-oee-l03.csv, expected-oee-all-lines.csv
```

Editing the left-hand side by hand silently invalidates the right-hand side, and nobody finds
out until a team argues about a number on Day 2. After **any** change to this data, run the
verifier in the facilitator repository:

```
cd ../AIDLC-Workshop-Facilitator
python tools/verify_kit.py
```

It recomputes every answer key from the source data, checks the mock's identities against the
blocklist, confirms every Thai ID still fails the national-ID check digit, and reports anything
that references a missing file.

Changing a business rule (a campaign, a cutoff, a formula) means changing the data, the
technical environment document, the stakeholder note it came from, **and** the corresponding row
in the facilitator repo's `Traceability-Map.md`. Each loop only teaches something while all four
agree.

## Status

Last full verification: all answer keys recomputed from source data with 0 mismatches; every
observable quoted in the traceability map matched against the shipped files; both brownfield
services and both starter toolchains installed and run clean; the three seeded Group 4 incidents
and all three Group 2 blocklist paths reproduced live.
