# Technical Environment: SwiftKYC — Metro Finance

## Stack (company standard — use this)

| Layer | Technology | Version | Notes |
|---|---|---|---|
| Language | Python | 3.12 | type hints required, mypy-clean |
| API framework | FastAPI | 0.11x | with Pydantic v2 models |
| Database | PostgreSQL | 15 | via SQLAlchemy Core or psycopg (no full ORM models with lazy loading) |
| Async jobs | none in MVP | — | webhook-driven; a simple retry poller script is acceptable |
| File storage | local `./secure-store/` in workshop | — | production would be S3 + KMS; in workshop use AES-256 (cryptography lib) with key from env var |
| Auth | OAuth2 client-credentials between systems; role claims in JWT | — | assume gateway-validated; trust `x-client-id`, `x-role` headers |
| Tests | pytest | 8.x | plus httpx TestClient |
| Lint | ruff + mypy | — | |

## Prohibited (with alternatives)

| Prohibited | Reason | Use Instead |
|---|---|---|
| Storing raw ID numbers or images unencrypted | PDPA / security baseline | AES-256-GCM envelope, key via env var |
| Logging PII (ID number, full name, images) | Security baseline / audit findings | masked formats, structured logging with an allowlist of fields |
| Calling VerifyMe synchronously and blocking the request | vendor is slow (2–20 s) | submit + webhook (mock provides both) |
| Django | company standard is FastAPI | FastAPI |
| Home-made crypto | obvious | `cryptography` library |

## Security Extension Note

This project is exactly the case the **AI-DLC Security baseline extension** exists for.
When Requirements Analysis asks about extensions, the team is expected to **opt IN to Security** (and may decline resiliency/PBT). Expect the security rules (encryption at rest/in transit, access logging, input validation, least privilege, fail-safe defaults…) to become blocking checks at stage gates.

## Integration Contract

See `verifyme-api-contract.md`. The mock vendor is `mock_verifyme.py` in this folder — run it with
`pip install fastapi uvicorn httpx && python mock_verifyme.py` (listens on `http://localhost:9310`).
Do not call any real service.

## Data Provided

- `mock_verifyme.py` — the VerifyMe mock vendor. The outcome *and the identity it returns* are driven by the last digit of your `reference`; three of those identities are on the blocklist. Also enforces the documented `402`, `429` and webhook-retry behaviour, and exposes `GET /_admin/billing` for the Day-2 audit
- `blocklist.csv` — 25 sanctions/blocklist entries (mix of exact-ID and name-only rows, incl. Thai names romanized inconsistently — your fuzzy match must handle them). All `idNumber` values are 13 digits like a real Thai national ID, but **every one of them fails the national-ID check digit on purpose** — they are fabricated test data and cannot belong to a real person. The names are invented too. Nothing in this file refers to any actual individual, sanction list, or investigation
- `sample-images/` — base64 ID-card and selfie payloads plus a ready-to-post `sample-submit.json`, so you are not blocked hunting for an image
- `consent-text-v1.md` — the legal consent text (versioned) to serve and record
- `stakeholder-notes.md` — raw interview notes from Compliance, Operations, the Vendor Manager, the mobile squad and Finance. They contain the answers to most of the AI's questions, two genuine contradictions, and **one instruction that must not be followed** — finding it is part of the exercise
- `starter-workspace/` — Python 3.12 toolchain only (FastAPI, pytest, ruff with the bandit rules on, strict mypy). No application layout: that is Application Design's job

### Blocklist screening must catch all three

| Submit a reference ending in | Vendor returns | Your screening must |
|---|---|---|
| `1` | `SOMSAK TESTASIRI` / `1103700111111`, face 0.97 | reject/flag on **exact ID** (BL-001) |
| `3` | `WICHAI SAETESTA` / clean ID, face 0.97 | reject/flag on **fuzzy name ≥ 0.9** — the list has `WICHAI SAE-TESTA` and `VICHAI SAETESTA`, neither spelled that way |
| `7` | `SOMPORN CHAROENTEST` / clean ID, face 0.97 | reject/flag on exact name (BL-008) |

All three pass face match. If your happy path auto-approves them, screening is not wired in.

## Non-Functional Expectations

- Every state transition writes an immutable audit event (actor, action, before→after, timestamp, requestId)
- Idempotent webhook handling (vendor retries on non-2xx; delivery may duplicate)
- Role checks: operations endpoints require `x-role: OPS_REVIEWER`; erasure requires `x-role: DPO`
- Timezone Asia/Bangkok for expiry business dates
