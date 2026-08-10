# Technical Environment: SwiftKYC — Metro Finance

## Stack (company standard — use this)

| Layer | Technology | Version | Notes |
|---|---|---|---|
| Language | Python | 3.12 | type hints required, mypy-clean |
| API framework | FastAPI | 0.11x | with Pydantic v2 models |
| Database | PostgreSQL | 15 | Runs locally from `starter-workspace/docker-compose.yml`. Use SQLAlchemy Core or psycopg (no full ORM models with lazy loading) |
| Async jobs | none in MVP | — | webhook-driven; a simple retry poller script is acceptable |
| File storage | local `./secure-store/` | — | a folder on your own disk, encrypted with AES-256-GCM (`cryptography` lib), key from an env var. It is git-ignored — never commit it |
| Deployment | out of scope | — | Everything runs on your own machine. No cloud account, no object storage, no managed key service |
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

## Running Locally

Everything runs on the team's own laptop. The only moving part beyond Python is PostgreSQL,
which comes up from the compose file shipped in `starter-workspace/`:

```
cd starter-workspace
docker compose up -d              # first run pulls the image, ~30 s
python scripts/db_ping.py         # must print "database is up."
```

| | |
|---|---|
| Connection | `postgresql://swiftkyc:swiftkyc@localhost:5433/swiftkyc` |
| Override with | `DATABASE_URL` — read it from the environment, never hard-code it |
| Port | 5433, so it does not collide with a Postgres you may already run |
| Start clean | `docker compose down -v` throws the data away |

The database is left in **UTC on purpose** — expiry business dates are Asia/Bangkok and
converting them is the application's job.

**Two things the security extension will ask you about, and the answer is the same for both:**
the encryption key and the database password are configuration, not code. The key comes from an
environment variable and the compose file's password is a local development value. Neither
belongs in the repository, and `secure-store/`, `.env` and `*.key` are already git-ignored.

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

### Blocklist screening

The vendor returns an identity; deciding what to do with it is yours. Compliance and Operations
both had something to say about how that matching should behave, and they are not saying quite
the same thing — `stakeholder-notes.md` has both, and `vision-document.md` has the threshold
Compliance settled on.

What you can rely on: the mock returns a **different identity depending on the last digit of
your `reference`**, and some of those identities are on `blocklist.csv`. Face match will not
stop them — several of the listed identities score 0.97, the same as a clean applicant. If your
happy path approves everyone who passes face match, screening is not wired in.

Work out which references should be stopped, and why, before you look at the Definition of Done.

## Non-Functional Expectations

- Every state transition writes an immutable audit event (actor, action, before→after, timestamp, requestId)
- Idempotent webhook handling (vendor retries on non-2xx; delivery may duplicate)
- Role checks: operations endpoints require `x-role: OPS_REVIEWER`; erasure requires `x-role: DPO`
- Timezone Asia/Bangkok for expiry business dates
