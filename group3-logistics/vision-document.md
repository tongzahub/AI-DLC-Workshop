# Vision: ParcelTrack COD & Notification Upgrade (Thunder Express)

> Workshop Group 3 · **Brownfield** project — starter codebase provided in `starter-code/`
> Expect the AI to run **Reverse Engineering** first. Suggested depth: Standard.

## Executive Summary

Thunder Express is a fictional last-mile delivery company (300 riders, ~12,000 parcels/day, 60% cash-on-delivery). Its existing ParcelTrack service (provided) handles parcel intake and status updates, but COD money is reconciled on paper and customers get no proactive notifications — the call center answers ~900 "where is my parcel" calls/day. This project extends the existing service with COD reconciliation and customer webhooks, without breaking the API that 3 merchant integrations already depend on. Expected outcome: rider cash variance detected same-day instead of weekly, and WISMO ("where is my order") calls cut by half.

## Business Context

### Problem Statement
- COD: riders collect cash; finance reconciles from paper sheets a week later; variance ~0.4% of COD value is currently discovered too late to act.
- Merchants (3 integrated e-commerce platforms) poll the status endpoint aggressively (~20 req/s) because there is no push notification.
- The original developer left; there is **no documentation** — only the code. (This is why Reverse Engineering matters.)

### Target Users and Stakeholders

| User Type | Description | Primary Need |
|---|---|---|
| Merchants (systems) | 3 platforms already integrated | Status webhooks; unchanged existing API |
| Riders (mobile app, existing) | 300 riders | Record COD collection at doorstep (API already exists — verify in RE) |
| Finance | 5 staff | Daily COD summary per rider, variance report |
| Call center | 15 agents | Fewer WISMO calls |

### Business Constraints
- **Backward compatibility is absolute**: existing endpoints and response shapes must not change (merchants will not redeploy).
- Finance closes COD daily at 20:00 Asia/Bangkok. Settlement day D runs 20:00 on D−1 (inclusive) to 20:00 on D (exclusive); cash recorded from 20:00 onwards goes on tomorrow's count sheet.
- No message broker available yet — webhooks must be delivered from the service itself with retry (keep it simple; document the limitation).

## Features In Scope

1. **Status webhooks to merchants** — merchant registers a callback URL + secret; on every parcel status change, POST a signed event; retry with backoff (max 5 attempts); delivery log queryable.
2. **COD reconciliation** — daily summary per rider (expected vs recorded collections), variance flagging (> 50 THB or missing), finance endpoint `GET /cod/summary?date=` and rider detail; mark-settled action.
3. **Fix what you find** — RE will surface issues in the existing code. The team decides with the facilitator which are in scope; at minimum, money must not be floats in new code.

## Features Explicitly Out of Scope

- Rider mobile app changes (API-only)
- Route optimization, real-time GPS
- Message broker / queue infrastructure (Phase 2 — document the upgrade path)
- Multi-currency (THB only)

## Key Success Metrics

- 0 breaking changes to existing endpoints (merchant contract tests still pass)
- Webhook delivery success ≥ 99% with retries; duplicate deliveries tolerated by design (documented idempotency guidance for merchants)
- COD variance visible by 20:30 same day
- `GET /cod/summary?date=` reproduces `expected-cod-summary.csv` for **both** 15 and 16 September — the 16th is the row set that proves the 20:00 Bangkok cutoff was implemented rather than a UTC calendar day

## Open Questions (expect the AI to ask)

- Which status transitions are legal, and does the existing code actually enforce them? (Whatever RE finds here: bug to fix, or behavior to preserve?)
- Webhook event payload: full parcel object or minimal delta + fetch URL?
- If a rider records a COD amount different from the parcel's COD value, accept-and-flag or reject?
