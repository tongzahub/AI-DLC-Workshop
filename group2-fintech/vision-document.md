# Vision: SwiftKYC — Digital Customer Onboarding API (Metro Finance)

> Workshop Group 2 · Greenfield project · Security extension expected: OPT IN · Suggested depth: Standard

## Executive Summary

SwiftKYC is the customer onboarding and e-KYC backend for Metro Finance (a fictional Thai consumer-lending company launching a digital personal-loan product). Today onboarding is a branch-only paper process taking 2 days; the new mobile app needs a fully digital flow — identity capture, verification through an external e-KYC vendor, PDPA consent, and risk screening — that completes in under 10 minutes. The expected outcome is 70% of new loan applications onboarded digitally within 6 months, with zero regulatory findings.

## Business Context

### Problem Statement
- Branch onboarding costs ~350 THB per applicant and loses ~40% of interested customers before completion.
- Compliance requires provable consent records and a complete audit trail per applicant; the paper process fails audits regularly.
- The mobile team (separate squad) is blocked waiting for backend APIs.

### Target Users and Stakeholders

| User Type | Description | Primary Need |
|-----------|-------------|--------------|
| Mobile app (system) | New lending app, separate team | Clean, well-documented onboarding API |
| Applicants | Consumers applying for a loan | Finish in <10 min, clear status feedback |
| Compliance team | 4 officers | Consent records, audit trail, PDPA data-subject requests |
| Operations (manual review) | 10 agents | Queue of flagged applications with evidence to approve/reject |
| External e-KYC vendor "VerifyMe" (system) | ID + face verification provider | Correct API usage incl. webhooks (contract provided) |

### Business Constraints
- PDPA compliance is non-negotiable: explicit versioned consent, purpose limitation, right-to-erasure workflow.
- Bank of Thailand–style guideline (workshop simplification): identity verification must reach IAL 2.3-equivalent — ID card OCR + face match ≥ 95% confidence, else manual review.
- National ID numbers and face images are sensitive personal data: encrypt at rest, mask in logs, restrict access by role.
- Vendor charges per verification call — avoid duplicate calls for the same application.

## Features In Scope (MVP)

- Application lifecycle API: create application → submit documents → verification → decision (states: DRAFT, PENDING_VERIFICATION, MANUAL_REVIEW, APPROVED, REJECTED, EXPIRED)
- PDPA consent capture: versioned consent text, per-purpose flags (credit check, marketing), timestamped, immutable
- Document intake: Thai national ID (front) + selfie — accept upload, validate format/size, store encrypted (in workshop: local encrypted storage is acceptable)
- Integration with VerifyMe (mock provided): submit ID + selfie, receive async webhook result (OCR fields, face-match score, liveness flag)
- Decision rules: score ≥ 0.95 and liveness pass → auto-approve identity; 0.80–0.95 → MANUAL_REVIEW queue; < 0.80 → reject
- Blocklist screening against a provided sanctions/blocklist CSV (exact ID match + fuzzy name match ≥ 0.9)
- Operations review API: list queue, view evidence, approve/reject with reason (role-restricted)
- **Operations review screen** — the 10 review agents cannot work from an API. They need the queue oldest-first with the score visible, the ID card and the selfie **side by side** on one page, and approve/reject with a reason. Role-restricted like the API behind it, and what an agent may and may not see on that page is a compliance question, not a layout question
- Full audit trail per application: every state change, who/what/when, immutable
- Data-subject erasure endpoint: on request, purge biometric artifacts, retain a legally required audit skeleton (7-year retention on audit fields)

## Features Explicitly Out of Scope (MVP)

- Credit scoring / loan decisioning (separate system — this service ends at identity decision)
- NDID integration (Phase 2 — VerifyMe mock only in MVP)
- Dip-chip / branch-assisted flow (Phase 2)
- The applicant-facing mobile app (a separate squad owns it). The internal operations screen above is ours
- AML transaction monitoring (separate system)

## Key Success Metrics

- End-to-end onboarding (happy path) < 10 minutes, API p95 < 300 ms (excluding vendor wait)
- 0 findings in the compliance team's audit-trail review (the workshop facilitator will play the auditor)
- Duplicate vendor verification calls per application: 0 — checked against the vendor's own `GET /_admin/billing`, where `double_billed` must be empty
- 100% of stored ID numbers encrypted and masked as `x-xxxx-xxxx-12-3` in every log line
- Blocklist screening stops all three seeded hits — including the one that only a fuzzy name match catches — even though all three pass face verification at 0.97

## Open Questions (expect the AI to ask)

- How long can an application stay in DRAFT before it expires? (Compliance suggests 7 days)
- If the vendor webhook never arrives, retry after how long — and who is allowed to re-trigger verification?
- Consent withdrawal mid-application: cancel the application or pause it?
- Can operations agents see the full ID number or a masked version? (Compliance: masked by default, unmask action is itself audited)
