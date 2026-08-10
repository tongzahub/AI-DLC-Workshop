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
| **The sentence** | `stakeholder-notes.md`, Khun Golf (Vendor Manager) | *"Every call. Even the ones that come back FAILED. Even the ones you sent twice by accident — especially those."* |
| **The question** | Requirements question file | "Who may trigger a repeat verification for the same application, and what prevents an accidental duplicate submission?" |
| **Our answer** | `[Answer]:` | The service never re-submits on its own. Re-verification is an explicit `OPS_REVIEWER` action behind a cost warning, and every submission is guarded by a per-application check |
| **The decision** | `team-log.md` #_ | One billed vendor call per application unless a human deliberately orders another. Chosen over automatic re-submission, which spends the company's money without anyone deciding to |
| **Story / requirement** | | "As Finance, every vendor charge on the invoice maps to one deliberate action I can find in the audit trail" |
| **Design** | | Submission goes through a single guarded path; the re-verify endpoint is role-gated, audited, and reuses the stored images |
| **Code** | `_______:__` | |
| **Test** | `_______` | The test that fails if two submissions for one application can ever reach the vendor client |
| **THE OBSERVABLE** | `GET localhost:9310/_admin/billing` | **`double_billed` is an empty map** after the full Day-2 demo — the vendor's own ledger says no application was ever charged twice |

**Why this example is the whole point:** the observable is not in your code at all — it is on the *vendor's* side,
the same place the invoice comes from. A sentence about money, said in a taxi, became a guard
in the design, and the proof is a ledger your team does not control. That is what "defensible"
means in this project.

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
