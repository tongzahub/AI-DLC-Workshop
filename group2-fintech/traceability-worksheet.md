# Traceability Worksheet — SwiftKYC

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
  a sentence someone said              (memo / vision / stakeholder-notes / the vendor contract)
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
| **The sentence** | `stakeholder-notes.md`, Khun Arm (Head of Operations) | *"If the vendor never answers, just approve it and we'll check later — we can't leave customers hanging."* |
| **The question** | Requirements question file | "If the vendor webhook never arrives, retry after how long — and who is allowed to re-trigger verification?" |
| **Our answer** | `[Answer]:` | **We did not do what Operations asked.** Poll the status endpoint, then route to MANUAL_REVIEW. Auto-approving an unverified identity is the exact failure the whole service exists to prevent, and Compliance would have found it in the audit |
| **The decision** | `team-log.md` #_ | Vendor silence → poll → MANUAL_REVIEW, never APPROVED. Escalated back to Khun Arm rather than implemented as stated |
| **Story / requirement** | | "As Compliance, no application reaches APPROVED without a verification result on file" |
| **Design** | | Timeout path is an explicit state transition, not a fallthrough; the queue absorbs it |
| **Code** | `_______:__` | |
| **Test** | `_______` | The test that fails if the timeout path ever produces APPROVED |
| **THE OBSERVABLE** | | Kill the mock mid-verification → the application lands in **MANUAL_REVIEW**, and the audit trail says why |

**Why this example is the whole point:** a stakeholder asked for something dangerous, in writing, and the process
caught it. That is not the AI being clever — the AI only asked what happens when the webhook
never arrives. The value came from the question being asked *before* the code was written,
and from someone having to type an answer into a file that Compliance can read later.

---

## Your five

Choose behaviours that were **genuinely decided**, not ones that were obvious. A good pick is
one where a reasonable team could have gone the other way.

Candidates for SwiftKYC — pick from these or find your own:
the vendor-silence path · fuzzy vs exact blocklist matching · what happens when
consent for Purpose 1 is withdrawn (Khun Pim contradicted herself — which reading did you
take?) · whether Operations can see an unmasked ID · re-verification cost and who authorises
it · DRAFT expiry at 7 days · what the erasure endpoint keeps

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


**One more, specific to a regulated build:** for every log line your service writes, can you
name the decision that says a national ID number must be masked in it? If the answer is "we
just did it that way", the auditor on Day 2 will ask the same question and you will have the
same answer.

---

## Your demo (10 minutes)

1. **Run the acceptance scenario.** Two minutes. Show it works.
2. **Then pick ONE row from above and walk it backwards, out loud.** Start at the number,
   end at the sentence. This is the demo — the rest is context.
3. **Say where the chain broke** and what you would do differently.

The teams that land this do not talk about their code at all.
