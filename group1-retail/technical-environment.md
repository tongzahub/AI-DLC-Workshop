# Technical Environment: PointHub — Siam MegaMart

> Greenfield service, but it must fit the company's platform standards below.

## Stack (company standard — use this)

| Layer | Technology | Version | Notes |
|---|---|---|---|
| Language | TypeScript | 5.x | Strict mode |
| Runtime | Node.js | 20.x LTS | |
| API framework | Express | 4.x | Company standard for all services |
| Database | PostgreSQL | 15 | No ORM — raw SQL with typed query helpers |
| Cache | Redis | 7 | For balance reads if needed (optional, justify) |
| Infrastructure | AWS ECS Fargate + RDS | — | Assume containers; IaC not required in workshop |
| Auth | API key per calling system + JWT for member-facing endpoints | — | Assume validated upstream at API Gateway; trust `x-member-id` / `x-system-id` headers |
| Tests | Jest | 29.x | ts-jest, tests in `__tests__/` |
| Lint | ESLint + Prettier | — | |

## Prohibited (with alternatives)

| Prohibited | Reason | Use Instead |
|---|---|---|
| ORMs (Prisma, TypeORM, Sequelize) | Company uses raw SQL with typed helpers | node-postgres typed query functions |
| Axios | Node 20 has fetch | native fetch |
| Vitest / Mocha | Standard is Jest | Jest |
| Floating-point money/points math | Audit reproducibility | integer satang / integer points, explicit rounding functions |
| Cron inside the API process | Ops standard | separate job entrypoint (can be a script triggered by EventBridge; in workshop a CLI script is fine) |

## Integration Contracts (mock these in the workshop)

- **Member DB (read-only)**: `GET /members/{memberId}` → `{ memberId, tier: "SILVER"|"GOLD"|"PLATINUM", joinedAt }` — assume it exists; stub it from `sample-data/members.csv` (8 members).
- **POS**: calls PointHub synchronously at checkout. If PointHub is down, POS completes the sale and queues the earn request for retry — so **earn must be idempotent** (`transactionId` is the idempotency key).
- **POS refunds**: a refund arrives as its own transaction with `type = REFUND`, its own `transactionId`, an `originalTransactionId`, and negative line amounts. A refund may return **all** lines of the original or only **some** of them. It is idempotent on its own `transactionId` like any other earn call.

## Points Arithmetic (no floats — this is how you keep audit reproducibility)

| Quantity | Representation |
|---|---|
| Base rate | 25 THB = 1 point |
| Campaign multiplier | integer scaled by 1000 — `x2.5` is stored as `2500`, never as `2.5` |
| Line value | `milli_points = amountTHB * (mult_x1000 / 25)` — the divisor is exact for every allowed multiplier (40, 80, 100, 120, 200) |
| Basket value | sum of the line milli-points |
| Posted points | `basket_milli // 1000` — floor, **once**, at basket level, never per line |

Campaign selection is **best single multiplier per line item** given (category, tier, date) — never stacked, never summed. When two campaigns tie on multiplier, the tie-break must be deterministic and the chosen campaign recorded on the ledger entry, or the replay is not reproducible.

**Clawback on refund**: recompute the original basket without the returned lines, floor it, and reverse the difference. For a full refund that reduces to "reverse exactly what the original earned". Reversing each returned line independently gives a different (wrong) answer — see `RF90003` in the answer key.

## Redemption Parameters (from Finance, fixed for MVP)

| Parameter | Value |
|---|---|
| Point value on redemption | 1 point = 0.25 THB (25 satang — integer satang everywhere) |
| Minimum redemption | 100 points per transaction |
| Redemption granularity | multiples of 100 points |
| Maximum per basket | 50% of the basket total, rounded **down** to the nearest allowed multiple |
| Redeeming on discounted items | allowed — no exclusions in MVP |
| Earning on the redeemed portion | no — points are earned on the amount actually paid after the point discount |

## Non-Functional Expectations

- Earn/burn endpoints: p95 < 150 ms, 50 tx/sec peak
- Every balance change must be an immutable ledger entry (no UPDATE of balances — derive or maintain with ledger + snapshot)
- All manual adjustments require `reasonCode` and `agentId`; write to audit log
- Timezone: Asia/Bangkok for all business dates (expiry month boundaries, day-of-week rules)

## Data Provided

| File | What it is |
|---|---|
| `sample-data/transactions.csv` | 40 POS sales (86 line items) plus 3 refunds — 2 full and 1 partial. Columns: `transactionId, type, originalTransactionId, date, time, storeId, memberId, tier, lineNo, category, amountTHB`. Refund lines carry negative amounts |
| `sample-data/members.csv` | The 8 members with tier and join date — stub the Member DB from this |
| `sample-data/campaign-examples.md` | The 5 campaigns marketing wants to run, the overlap questions, and how to keep x2.5 out of floating point |
| `sample-data/expected-points.csv` | **The answer key.** Points your earn API must post for every transaction, with the reasoning for the twelve deliberately tricky ones |
| `sample-data/expected-points-by-line.csv` | The same answer broken down per line item: winning campaign, multiplier, milli-points |
| `starter-workspace/` | Node 20 + TypeScript 5.5 toolchain only — Express, `pg`, Jest, ESLint, Prettier, already configured to the standards on this page. No `src/` layout: that is Application Design's job |

Replaying the whole file in order (sales then refunds) must leave these balances — this is the finance-reproducibility check in one line:

| M1001 | M1002 | M1003 | M1004 | M1005 | M1006 | M1007 | M1008 |
|---|---|---|---|---|---|---|---|
| 383 | 254 | 374 | 156 | 567 | 452 | 624 | 78 |
