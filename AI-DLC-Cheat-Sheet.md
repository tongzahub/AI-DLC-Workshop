# AI-DLC V1 — One-Page Cheat Sheet

> Keep this open all day. It is the map; your group README is the route.

## The golden rule

**The agent proposes, the human approves.** Never let the AI skip a gate, and never answer
its questions in chat — answers go into the question files, after the `[Answer]:` tags.

## The stage pipeline

Every stage ends at a **gate**: a completion message with explicit options
(**Request Changes / Continue**). Read the artifacts *before* you approve.
Workflow Planning decides, per stage, whether it will **EXECUTE** or **SKIP** — and you
defend or change that plan at its gate.

| # | Stage | What it produces | Typical for |
|---|---|---|---|
| 0 | Workspace Detection | recognises new vs existing code | all |
| 1 | Reverse Engineering | docs for existing code: architecture, APIs, quality | brownfield (G3, G4) — greenfield SKIPs |
| 2 | Requirements Analysis | requirements + **the extension question** (Security / Resiliency / PBT) | all |
| 3 | User Stories | stories with acceptance criteria | greenfield-heavy |
| 4 | Workflow Planning | the execution plan (Mermaid) — which stages run, in what order | all — **challenge it here** |
| 5 | Application Design | components, boundaries, NFRs | greenfield; brownfield = delta design |
| 6 | Units Generation | 2–3 Units of Work, each independently buildable | greenfield |
| 7 | Construction (per unit) | design → code → tests for one unit | all |
| 8 | Build and Test | full build, test run, verification | all |

Artifacts appear under `aidlc-docs/` — state (`aidlc-state.md`), audit trail (`audit.md`),
requirements, stories, plan, designs, per-unit docs. That folder is a deliverable: commit it.

## Question files, not chat

The AI writes questions into markdown files with lettered options and an `[Answer]:` tag.
Open the file → type your answer after the tag → save → tell the AI you are done.
A vague answer earns a follow-up clarification file — that is the system working.
Source answers from your scenario documents; where they conflict, the **Product Owner
decides** and the **Scribe records why** in `team-log.md`.

## Extensions (decided at Requirements Analysis — always record why)

| Extension | What it does | Who opts in |
|---|---|---|
| **Security baseline** | 15 rules become blocking checks at gates | Group 2 |
| **Resiliency** | failure-mode analysis in design | nobody (declines on record) |
| **Property-Based Testing** | generated-case test obligations | Group 4 |

Groups 1 and 3 decline all three — **on record**. An unrecorded "no" scores the same as
never having been asked.

## Mid-workflow changes

Allowed and logged: add a skipped stage, change depth, revisit a decision — ask explicitly;
AI-DLC supports 8 change types and writes them to the audit trail. Choose **Standard depth**
unless your brief says otherwise. Never edit code outside the workflow without telling the
AI afterwards (undeclared hand edits are audit findings).

## The four paths side by side (why Day 2 compares them)

| | G1 PointHub | G2 SwiftKYC | G3 ParcelTrack | G4 LineMetrics |
|---|---|---|---|---|
| Shape | greenfield | greenfield, regulated | brownfield CR | brownfield bug fix |
| RE stage | skip | skip | **first, and reviewed** | first, root-cause |
| Extensions | decline all | **Security IN** | decline all | **PBT IN** |
| Plan shape | fullest path | full + security gates | leaner — challenge it | most stages SKIP |
| Ground truth | `expected-points.csv` | mock outcomes + `/_admin/billing` | `expected-cod-summary.csv` | `expected-oee-*.csv` |

Same rules, four different execution plans — that comparison is the point of the workshop.

## Roles (rotate at least once per half-day)

**Driver** keyboard, never answers unilaterally · **Product Owner** owns the documents,
arbitrates conflicts, final say at gates · **Reviewer** reads every artifact before a gate ·
**Scribe** keeps `team-log.md` live.

## Scoring

Process quality **40%** · working software **30%** · decision quality at gates **20%** ·
demo & retro insight **10%**. You may ask to see the rubric at any time.
