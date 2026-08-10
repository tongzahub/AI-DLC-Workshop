# Technical Environment: ParcelTrack — Thunder Express

> **Brownfield.** The existing stack is the baseline (see `starter-code/`). New code must follow existing patterns unless a pattern is explicitly identified as a defect during Reverse Engineering and the team approves changing it.

## Existing Stack (must be preserved)

| Layer | Technology | Notes |
|---|---|---|
| Language | Python 3.12 | |
| API framework | FastAPI + Pydantic v2 | |
| Database | SQLite via SQLAlchemy Core | fine for workshop; do not migrate to Postgres |
| Tests | pytest (a few exist — they must keep passing) | |
| Run | `uvicorn app.main:app` | |

## Hard Rules

- Existing endpoint paths, methods, and response shapes must not change (merchant compatibility).
- Additive DB migrations only (new tables / new columns with defaults).
- New money fields: **integer satang**, never float. If Reverse Engineering surfaces a pattern in the existing code that violates this, new code must not copy it — discuss remediation scope with the facilitator. The CSV is in whole THB; 560 THB = 56000 satang.
- Webhook signatures: HMAC-SHA256 over the raw body with the merchant's secret, header `X-Tex-Signature`. The test receiver accepts both `sha256=<hex>` and a bare `<hex>`, and answers 401 on a bad or missing signature.
- Timezone Asia/Bangkok for the 20:00 COD cutoff. **Settlement day D = 20:00 on D−1 (inclusive) → 20:00 on D (exclusive), Asia/Bangkok.** A collection recorded at exactly 20:00:00 belongs to day D+1.
- Existing timestamps are stored as **naive UTC strings ending in `Z`** (`datetime.utcnow().isoformat() + "Z"`). 20:00 Bangkok is 13:00Z, so a UTC calendar day produces the wrong settlement day. Keep writing the same format for new rows; convert when you apply the business rule.

## Prohibited

| Prohibited | Use Instead |
|---|---|
| Celery/Redis/queues | in-process background tasks + a retry table (document Phase-2 upgrade path) |
| ORM model rewrite | keep SQLAlchemy Core tables, add new ones alongside |
| New framework (Flask/Django) | FastAPI as-is |
| Changing existing JSON field names | add new endpoints/fields only |

## Data & Tooling Provided

| File | What it is |
|---|---|
| `sample-cod-day.csv` | 31 deliveries with Bangkok-local `deliveredAt` / `recordedAt`, including rows on both sides of the 20:00 cutoff and the two seeded discrepancies (R-017 short 120 THB, R-023 one collection never recorded) |
| `starter-code/seed_cod.py` | Loads that CSV into the existing tables. Run from `starter-code/`: `python seed_cod.py ../sample-cod-day.csv`. Idempotent — it deletes the CSV's parcel ids first. Needed because `POST /parcels` generates its own sequential id, so the `TEX-2026-0040xx` ids cannot be created through the API |
| `expected-cod-summary.csv` | Finance's hand-worked answer for 15 and 16 September — the ground truth your `/cod/summary` endpoint must reproduce |
| `merchants.csv` | The three integrated merchants with callback URL and webhook secret; register these through your new API |
| `webhook_receiver.py` | The merchant test receiver (standard library only). Verifies your HMAC signature, can be told to answer 500 so you can demo retries, and flags duplicate deliveries by `event_id`. `python webhook_receiver.py --help` |

`seed_cod.py` writes only to `parcels`, `status_history` and `cod_collections`. Any new table or column is yours to add — additively.

## What Reverse Engineering Should Produce First

Before any new feature work, the AI should generate its standard RE artifacts (business overview, architecture, code structure, API documentation, component inventory, technology stack, dependencies, code quality assessment). The team must **review and correct** them — at least 2 deliberate quirks exist in the codebase that the AI should flag — do not tell the AI in advance what to look for; review its artifacts critically and dispose of each finding on record.
