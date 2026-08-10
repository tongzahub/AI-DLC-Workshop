# Stakeholder Interview Notes — SwiftKYC Kickoff (excerpts)

> Raw meeting notes, as you would receive them in real life.
> They contain useful details, some contradictions, and some noise.
> Use them to answer the AI's clarification questions. Where notes conflict, the team must
> decide and record the decision — in a regulated build, an undocumented decision is a finding.

## From: Khun Pim — Head of Compliance / DPO (60 min, she brought a printout)

- "Consent is not a checkbox, it is a record. Version, purposes, timestamp, channel, application id. If you cannot show me the exact text the customer agreed to, we have no consent."
- Purpose 1 (identity + credit) is required; Purpose 2 (marketing) is optional and **must not** be pre-ticked.
- Withdrawal: "Purpose 2 they can withdraw any time and nothing happens to the loan. Purpose 1 — if they withdraw, the application is over."
- Asked what "over" means: *"Terminated. Not paused."* Then, later in the same meeting: *"Well — if they withdraw and then change their mind the same day, obviously we do not make them start again."* **(Contradiction. Decide: terminate immediately, or a short grace window? Record which and why.)**
- DRAFT applications: "Seven days and it is stale. Delete it." Asked whether that means delete the record or expire the state: *"…that is your problem, not mine. Just do not keep the photos."*
- Erasure requests: "By law we have thirty days. In practice do it same day. But you cannot delete what we are required to keep for seven years." **(retain the audit skeleton, purge biometrics)**
- On unmasking: "Ops can unmask if they need to. But I want to know every single time they did, and who."

## From: Khun Arm — Head of Operations, manual review queue (40 min)

- 10 agents. Queue depth today is invisible; they want oldest-first with the score visible.
- "My agents need to see the face photo and the ID photo side by side. Otherwise what are they reviewing?" — asked about the ID number specifically: *"Honestly they don't need the number. They need the face."*
- Re-verification: "Sometimes the photo is genuinely bad and the customer sends a better one. We need to be able to run it again." Told it costs money per call: *"Then put a big warning on the button. But don't take it away."*
- **"If the vendor never answers, just approve it and we'll check later — we can't leave customers hanging."**
- Blocklist hits: "If someone is on the sanctions list, that is not a review, that is a stop. Do not put those in my queue." Then: "…but the name matching had better be good, I am not explaining to a customer that they share a surname with someone."

## From: Khun Golf — Vendor Manager (short call, he was in a taxi)

- VerifyMe bills per `POST /verifications`. "Every call. Even the ones that come back FAILED. Even the ones you sent twice by accident — *especially* those."
- Current contracted volume is 60 calls in the workshop sandbox; production is different. When the quota is gone you get 402 and nothing works.
- "Their webhook is not reliable. It retries, it duplicates, and about once a week it just never turns up. Their support answer is 'poll the status endpoint'."
- Polling limit is 1 request per 10 seconds per verification. "Do not hammer it, they will rate limit you and then you have neither."
- On the signature: "Verify it. I know nobody does. Verify it."

## From: Khun Ice — Mobile squad lead (Slack thread, pasted)

> "we just need the API contract early, we're blocked
> also can the app poll a status endpoint? we don't want to do websockets for v1
> and please don't make us upload the image twice if verification fails, our users are on 4G in a rice field"

- **(A real design input from the mobile squad — decide how re-verification interacts with the stored images, and remember the vendor bills per call either way.)**

## From: Khun Tan — Finance (one line, forwarded email)

> "Whatever you build, I need to know at month end how many verifications we were billed for and how many of those produced an approved customer."

## Noise / parking lot (do not build)

- Khun Arm asked about a supervisor dashboard with agent productivity stats — sponsor deferred to Phase 2.
- Khun Ice floated NDID integration "since we're doing identity anyway" — explicitly Phase 2 in the vision document.
- Someone mentioned liveness could be replaced with a video selfie next year. Vendor firmware, not ours.
