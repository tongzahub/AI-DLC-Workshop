# Traceability Worksheet — ParcelTrack

> Fill this in on Day 2, before your demo. It is the single most useful thing you will take
> home, and it is what your demo is built on.

## What this is for

Anyone can show working code. The question AI-DLC is actually answering is:

> **Why does the software behave this way, and who decided that?**

Pick a behaviour your system has. Walk it backwards until you reach a sentence a human said.
If you can do that for five behaviours, the process worked. If the chain breaks somewhere —
a number nobody can explain, a decision with no recorded why — that break is the most
valuable thing you will find today. Write it down honestly; it scores better than hiding it.

## The chain

```
  a sentence someone said              (vision / change-request / technical-environment / what Reverse Engineering found)
    └─ the question the AI asked       (aidlc-docs/.../*-questions.md)
        └─ the answer you typed        ([Answer]: ...)
            └─ the decision recorded   (team-log.md + audit.md)
                └─ requirement / story (aidlc-docs/)
                    └─ design element  (aidlc-docs/design/)
                        └─ code        (file:line)
                            └─ test    (the one that would fail if the decision flipped)
                                └─ THE OBSERVABLE   (a number you can point at)
```

---

## Worked example — do not reuse this one, it is here to show the shape

| Step | Where | What it says |
|---|---|---|
| **The sentence** | `change-request.md`, Finance | *"Our day closes at 20:00. Anything a rider records from 20:00 onwards is tomorrow's cash — it goes in tomorrow's count sheet, because tonight's sheet is already printed."* |
| **The question** | Requirements question file | "Which timestamps define the COD settlement day, and what happens to a collection recorded exactly at the cutoff?" |
| **Our answer** | `[Answer]:` | Settlement day D = 20:00 on D−1 inclusive → 20:00 on D exclusive, Asia/Bangkok. Exactly 20:00:00 belongs to the next day. The service stores naive UTC, so we convert before applying the rule |
| **The decision** | `team-log.md` #_ | Business day boundary is a business rule, not a storage detail. Chosen over the UTC calendar day, which is what the existing code would have led us to |
| **Story / requirement** | | "As Finance, my 20:30 report contains exactly the cash the riders handed in today" |
| **Design** | | Conversion at the query boundary; existing `collected_at` format untouched (merchant compatibility) |
| **Code** | `_______:__` | |
| **Test** | `_______` | The test that fails if someone bucket by `collected_at[:10]` |
| **THE OBSERVABLE** | `expected-cod-summary.csv` | **`GET /cod/summary?date=2026-09-16` returns exactly three rows.** A UTC calendar day gets the 15th roughly right and the 16th completely wrong |

**Why this example is the whole point:** the 15th looks correct under both implementations. Only the 16th separates
them. A team that never asked the question would have shipped something that passes its own
demo and quietly misreports cash every single evening after 20:00.

---

## Your five

Choose behaviours that were **genuinely decided**, not ones that were obvious. A good pick is
one where a reasonable team could have gone the other way.

Candidates for ParcelTrack — pick from these or find your own:
the settlement-day boundary · what to do about the float money columns you found
in RE · whether `PUT /status` keeps accepting any string · what the webhook event payload
contains (full object vs delta) · what happens when a rider records a different amount than
the parcel's COD value · how many retries and with what backoff · what you told merchants
about duplicate deliveries

### 1.

| Step | Where | What it says |
|---|---|---|
| The sentence | | |
| The question | | |
| Our answer | | |
| The decision | | |
| Story / requirement | | |
| Design | | |
| Code | | |
| Test | | |
| **THE OBSERVABLE** | | |

### 2.

| Step | Where | What it says |
|---|---|---|
| The sentence | | |
| The question | | |
| Our answer | | |
| The decision | | |
| Story / requirement | | |
| Design | | |
| Code | | |
| Test | | |
| **THE OBSERVABLE** | | |

### 3.

| Step | Where | What it says |
|---|---|---|
| The sentence | | |
| The question | | |
| Our answer | | |
| The decision | | |
| Story / requirement | | |
| Design | | |
| Code | | |
| Test | | |
| **THE OBSERVABLE** | | |

### 4.

| Step | Where | What it says |
|---|---|---|
| The sentence | | |
| The question | | |
| Our answer | | |
| The decision | | |
| Story / requirement | | |
| Design | | |
| Code | | |
| Test | | |
| **THE OBSERVABLE** | | |

### 5.

| Step | Where | What it says |
|---|---|---|
| The sentence | | |
| The question | | |
| Our answer | | |
| The decision | | |
| Story / requirement | | |
| Design | | |
| Code | | |
| Test | | |
| **THE OBSERVABLE** | | |

---

## Where the chain broke

Be honest. Every team has at least one. Naming it is worth more than pretending you do not.

| # | The behaviour | Where the chain stops | What we would have needed |
|---|---|---|---|
| 1 | | | |
| 2 | | | |

Common shapes: a number nobody can source · a design choice the AI made that we approved
without asking why · a requirement with no story · a story with no test · a decision that
only exists in someone's memory.


**Brownfield teams have a second kind of break:** things the code does that nobody ever
decided. The sequential parcel id, the naive UTC timestamps, the float money — those have no
sentence behind them at all. List the ones you found and what you did: fixed, contained, or
recorded and left alone. "We left it alone deliberately" is a complete answer. "We did not
notice" is the finding.

---

## Your demo (10 minutes)

1. **Run the acceptance scenario.** Two minutes. Show it works.
2. **Then pick ONE row from above and walk it backwards, out loud.** Start at the number,
   end at the sentence. This is the demo — the rest is context.
3. **Say where the chain broke** and what you would do differently.

The teams that land this do not talk about their code at all.
