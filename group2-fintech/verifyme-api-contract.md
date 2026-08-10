# VerifyMe e-KYC Vendor — API Contract (v1.3, mock)

Base URL (mock): `http://localhost:9310`
Auth: header `X-Api-Key: <key>` (mock accepts `demo-key-123`)
Billing: **every** POST /verifications call is billed — duplicate submissions for the same application cost real money.

Run the mock (from your group folder): `pip install fastapi uvicorn httpx && python mock_verifyme.py`
`python mock_verifyme.py --help` shows the quota / rate-limit / webhook-delay switches.

## 1. Submit verification

`POST /verifications`

```json
{
  "reference": "APP-2026-000123",        // your application id — used to correlate the webhook
  "id_card_image": "<base64>",
  "selfie_image": "<base64>",
  "callback_url": "https://your-service/webhooks/verifyme"
}
```

Response `202 Accepted`:

```json
{ "verification_id": "vm_7f3a1c", "status": "PROCESSING", "estimated_seconds": 15 }
```

Errors: `400 INVALID_IMAGE` (unreadable/too small), `402 QUOTA_EXCEEDED` (contracted volume used up), `429` (rate limit 5 rps — back off and retry).
Ready-made request bodies and base64 images are in `sample-images/`.

## 2. Webhook (VerifyMe → you)

`POST {callback_url}` — retried up to 5 times on non-2xx with increasing delay, and **may deliver duplicates**. Signature header `X-Vm-Signature: sha256=<hmac-hex>` using shared secret (`demo-secret`) over the raw body; you MUST verify it.

```json
{
  "verification_id": "vm_7f3a1c",
  "reference": "APP-2026-000123",
  "status": "COMPLETED",                  // or FAILED
  "ocr": {
    "id_number": "1103700123456",
    "name_th": "สมชาย เทสต์ดี",
    "name_en": "SOMCHAI TESTDEE",
    "dob": "1994-02-14",
    "expiry_date": "2029-05-01"
  },
  "face_match_score": 0.973,              // 0.0 – 1.0
  "liveness_passed": true,
  "failure_reason": null                  // e.g. "ID_EXPIRED", "FACE_NOT_FOUND", "BLURRY_IMAGE"
}
```

## 3. Query status (fallback if webhook lost)

`GET /verifications/{verification_id}` → same body as the webhook. Rate limit: 1 request / 10 s per verification (`429` if you poll faster).

## Mock server behaviour (for the workshop)

The outcome is chosen by the **last digit of `reference`**. Face-match score and the identity returned by OCR vary independently — an application can pass face match and still have to be stopped by blocklist screening.

| last digit | score | status | OCR identity returned | what it exercises |
|---|---|---|---|---|
| `1` | 0.97 | COMPLETED | `SOMSAK TESTASIRI` / `1103700111111` | **blocklist hit by exact ID** (BL-001) |
| `3` | 0.97 | COMPLETED | `WICHAI SAETESTA` / `3102000987654` | **blocklist hit by fuzzy name only** — the list holds `WICHAI SAE-TESTA` (BL-002) and `VICHAI SAETESTA` (BL-004); exact matching misses this |
| `7` | 0.97 | COMPLETED | `SOMPORN CHAROENTEST` / `1450500246811` | blocklist hit by exact name (BL-008) |
| `5`, `9` | 0.97 | COMPLETED | `SOMCHAI TESTDEE` / `1103700123456` | clean auto-approve |
| `0`, `2` | 0.86 | COMPLETED | clean | MANUAL_REVIEW band |
| `4` | 0.62 | COMPLETED, liveness false | clean | reject band |
| `6` | — | FAILED, `ID_EXPIRED` | none (`ocr: null`) | vendor failure path |
| `8` | 0.97 | COMPLETED | clean | **webhook delivered TWICE** (duplicate handling) |

Note that `1`, `3` and `7` all sail through face match at 0.97. The only thing that stops them is your screening — and only a fuzzy name match stops `3`.

## Facilitator / audit endpoints (not part of the vendor contract)

- `GET /_admin/billing` → `{ total_credits, quota, by_reference, double_billed }`. Any reference with a count above 1 means that application was submitted twice and billed twice — this is how the Day-2 auditor checks the "0 duplicate vendor calls" metric.
- `POST /_admin/reset` → clears the quota and the billing ledger between runs.
