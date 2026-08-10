# Traceability Worksheet — LineMetrics

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
  a sentence someone said              (vision / bug-reports / technical-environment / what Reverse Engineering found)
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
| **The sentence** | `bug-reports.md`, INC-1044, Shift Supervisor | *"Our production day runs 08:00 to 08:00 — a cycle at 07:30 on the 16th belongs to the 15th's production day."* |
| **The question** | Requirements question file | "What defines a production day, and which timezone is authoritative for bucketing readings?" |
| **Our answer** | `[Answer]:` | 08:00 → 08:00 Asia/Bangkok, i.e. 01:00Z → 01:00Z. Gateways post ISO-8601 UTC and the contract is frozen, so the conversion happens on our side at bucketing time |
| **The decision** | `team-log.md` #_ | Fix the bucketing at the source, not by post-processing in the endpoint (technical-environment.md forbids the latter) |
| **Story / requirement** | | "As a plant manager, every reading appears in exactly one production day, the one the shift log agrees with" |
| **Design** | | Single `production_day(ts)` function; every query goes through it; PBT asserts the partition is total and disjoint |
| **Code** | `_______:__` | |
| **Test** | `_______` | Regression test written **before** the fix, plus the property test over 1,000 generated timestamps |
| **THE OBSERVABLE** | `expected-oee-l03.csv` | **L-03 on 15 Sep counts 800 pieces, not 794.** The old filter dropped the 41 pieces made at 07:30 on the 16th and stole 35 that belonged to the 14th |

**Why this example is the whole point:** the supervisor did not report "a timezone bug". He reported that his numbers
were wrong and that they "shift oddly around 07:00". Turning that sentence into 01:00Z is the
work — and the 794 → 800 is the proof it was done, not guessed.

---

## Your five

Choose behaviours that were **genuinely decided**, not ones that were obvious. A good pick is
one where a reasonable team could have gone the other way.

Candidates for LineMetrics — pick from these or find your own:
the production-day boundary · what happens when the same `reading_id` arrives with
a different payload · whether historical duplicates get cleaned up or fixed forward · what a
maintenance day (planned 0) should return · clamping when downtime exceeds planned minutes ·
which invariants you chose for the property tests, and why those · why the two existing tests
never caught any of this

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


**Your fifth row is prescribed:** trace the *test gap* itself. The two original tests passed
throughout, and every one of these bugs was live. Walk backwards from "the dashboard was
wrong for months" to what those tests asserted, and what they did not. That chain ends at an
absence rather than a sentence — which is exactly why the PBT extension exists.

---

## Your demo (10 minutes)

1. **Run the acceptance scenario.** Two minutes. Show it works.
2. **Then pick ONE row from above and walk it backwards, out loud.** Start at the number,
   end at the sentence. This is the demo — the rest is context.
3. **Say where the chain broke** and what you would do differently.

The teams that land this do not talk about their code at all.
