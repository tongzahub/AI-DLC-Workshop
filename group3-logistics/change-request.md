# Change Request CR-2026-081 — COD Reconciliation & Merchant Webhooks

Requested by: Head of Operations · Priority: HIGH · Target: this quarter

## Trigger phrase for the workshop

> Using AI-DLC, implement change request CR-2026-081 for the existing ParcelTrack service in this workspace: add merchant status webhooks and daily COD reconciliation, per vision-document.md and technical-environment.md. This is a brownfield project — analyze the existing code first.

## Requirement details (from operations, verbatim)

1. Merchants keep hammering `GET /parcels/{id}` — give them webhooks. They register a URL and a secret with us; every time a parcel changes status we POST them an event within 30 seconds. If their endpoint is down, retry up to 5 times with increasing delay. We need to see a log of what was delivered.
2. Finance: every rider that carries COD parcels must have a daily summary — how much they *should* have collected vs what they *recorded* — flag differences over 50 baht or any missing collection. Cutoff 20:00, report ready by 20:30. Finance marks a rider's day as settled after counting cash.
3. Do NOT break the merchant API. Their integration teams take months to change anything.

## The settlement day (finance, in writing)

> "Our day closes at 20:00. Anything a rider records from 20:00 onwards is tomorrow's cash — it goes in tomorrow's count sheet, because tonight's sheet is already printed."

So **settlement day D = 20:00 on D−1 (inclusive) → 20:00 on D (exclusive), Asia/Bangkok**.
A delivery at exactly 20:00:00 belongs to the *next* day. `sample-cod-day.csv` contains rows on both sides of that boundary, including one at exactly 20:00:00.

Note that the running service stores timestamps as naive UTC strings ending in `Z`. 20:00 Bangkok is 13:00Z — a UTC calendar day will give you the wrong answer.

## Setting up the demo data

```
cd starter-code
python seed_cod.py ../sample-cod-day.csv     # 31 parcels + 30 COD collections, safe to re-run
```

The seeder writes into the *existing* tables only (`parcels`, `status_history`, `cod_collections`); it does not add columns or tables — that part is yours.
It exists because `POST /parcels` generates its own sequential id, so the `TEX-2026-0040xx` ids in the CSV cannot be created through the API.

The merchants to register are in `merchants.csv` (M-100 / M-113 / M-121, each with a callback URL and secret).
The test receiver is `webhook_receiver.py` — standard library only, no install:

```
python webhook_receiver.py                    # M-100 on :9410, verifies your HMAC signature
python webhook_receiver.py --fail             # always answers 500, for the retry demo
python webhook_receiver.py --port 9411 --merchant M-113 --secret whsec_m113_2b8c41
```

It answers **401** if the `X-Tex-Signature` HMAC does not verify (use `--no-verify` while wiring up).

## Acceptance snapshot (ops will demo exactly this)

- Register the webhook for merchant M-100 from `merchants.csv` → update a parcel's status → `webhook_receiver.py` shows a **signed** event (`sig OK`) within 30 s.
- Stop the receiver → update status → see 5 retries in the delivery log → start the receiver again → the next event delivers.
- Seed the COD day → `GET /cod/summary?date=2026-09-15` matches `expected-cod-summary.csv`:

| rider | parcels | expected | recorded | variance | flagged |
|---|---|---|---|---|---|
| R-005 | 8 | 6,090 | 6,090 | 0 | no |
| R-009 | 6 | 3,254 | 3,254 | 0 | no |
| R-017 | 5 | 1,829 | 1,709 | **−120** | **yes** |
| R-023 | 4 | 2,855 | 1,655 | **−1,200** | **yes** (1 collection never recorded) |
| R-031 | 5 | 3,260 | 3,260 | 0 | no |

- `GET /cod/summary?date=2026-09-16` returns exactly three rows (R-017 199, R-023 640, R-031 875, all clean) — this is what proves the 20:00 Bangkok cutoff was implemented, not a UTC day.
