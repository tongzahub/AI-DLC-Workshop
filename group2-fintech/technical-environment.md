# Technical Environment: SwiftKYC — Metro Finance

> From the CIO office, not from the business. These are the few things the platform team and the
> security baseline will not let you change. **Everything not listed here is yours to decide** —
> and in a regulated build, to defend at a gate.

## Platform standards

| | Standard | Why it is not negotiable |
|---|---|---|
| Language & runtime | Python 3.12 | every service the platform team operates runs on it |
| Database | PostgreSQL 15 | the only datastore ops will run in production |
| Business timezone | Asia/Bangkok | application expiry is counted in business days by people in Bangkok |
| Cryptography | the `cryptography` library | home-made crypto has never survived an audit and never will |

Framework, project layout, test runner, linting, how you talk to the database, how you model the
application lifecycle — none of that is standardised here. Choose, and record why.

## Prohibited

| Prohibited | Reason |
|---|---|
| Storing national ID numbers or biometric images unencrypted | PDPA, and the security baseline |
| Logging PII — ID numbers, full names, images | every unmasked ID in a log line is an audit finding |
| Blocking a request while waiting for the e-KYC vendor | the vendor takes 2–20 seconds and is not reliable |

## Integration Contracts

- **VerifyMe, the e-KYC vendor** — `verifyme-api-contract.md`. The mock is `mock_verifyme.py` in this folder; run it with `pip install fastapi uvicorn httpx && python mock_verifyme.py`. **Do not call any real service.**
- **Authentication**: OAuth2 client-credentials between systems, role claims in the JWT. Assume the gateway has already validated it — trust the `x-client-id` and `x-role` headers.
- **Roles**: operations endpoints require `x-role: OPS_REVIEWER`; data-subject erasure requires `x-role: DPO`.

## The screen

One user interface is in scope (see the vision document). The platform team has exactly two
rules about it, and no opinion on anything else:

- **It is served by your own service and runs in a browser on this laptop.** No separate
  frontend server, no deployment, no build pipeline required.
- **Nothing is fetched from the internet at runtime.** No CDN for a framework, a font or an
  icon set — the venue Wi-Fi is not part of your architecture, and the demo has to work when it
  is not there.

Framework or no framework, one page or several, a build step or plain files served as-is —
that is a design decision like any other. Make it, record why, and be ready to defend it at a
gate. A single page your API serves is a completely respectable answer for two days of work.


## Environment

You need Python 3.12 and a PostgreSQL 15 you can reach. `local-environment/` has a compose file
that gives you one on your own machine — see `../README.md` §1.2. Document storage is a folder
on your own disk; there is no object store and no managed key service, and the encryption key
comes from an environment variable. Nothing here runs in a cloud, and nothing is deployed.

`secure-store/`, `.env` and `*.key` are already git-ignored. Keep it that way.

## Data Provided

- `mock_verifyme.py` — the VerifyMe mock vendor. The outcome *and the identity it returns* are driven by the last digit of your `reference`. It also enforces the documented `402`, `429` and webhook-retry behaviour, and exposes `GET /_admin/billing`
- `blocklist.csv` — 25 screening entries: some carry a national ID, some are name-only, and the romanisation is not consistent. All `idNumber` values are 13 digits like a real Thai national ID, but **every one of them fails the national-ID check digit on purpose** — they are fabricated and cannot belong to a real person. The names are invented too. Nothing in this file refers to any actual individual, sanction list, or investigation
- `sample-images/` — base64 ID-card and selfie payloads plus a ready-to-post `sample-submit.json`
- `consent-text-v1.md` — the versioned consent text and what must be recorded per consent
- `stakeholder-notes.md` — raw interview notes from Compliance, Operations, the Vendor Manager, the mobile squad and Finance. They hold the answers to most of the AI's questions, two genuine contradictions, and **one instruction that must not be followed** — finding it is part of the exercise
