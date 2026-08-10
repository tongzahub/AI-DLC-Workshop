# Technical Environment: PointHub — Siam MegaMart

> Greenfield service, but it must fit the company's platform standards below.

## Stack (company standard — use this)

| Layer | Technology | Version | Notes |
|---|---|---|---|
| Language | TypeScript | 5.x | Strict mode |
| Runtime | Node.js | 20.x LTS | |
| API framework | Express | 4.x | Company standard for all services |
| Database | PostgreSQL | 15 | Runs locally from `starter-workspace/docker-compose.yml`. No ORM — raw SQL with typed query helpers |
| Cache | Redis | 7 | For balance reads if needed (optional, justify). Not provided — add a service to the compose file if your design earns it |
| Deployment | out of scope | — | Everything runs on your own machine. No cloud account, no containers to build, no IaC |
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
| Cron inside the API process | Ops standard | a separate job entrypoint the scheduler calls — in the workshop a CLI script you can run by hand is exactly right |

## Running Locally

Everything runs on the team's own laptop. The only moving part beyond Node is PostgreSQL,
which comes up from the compose file shipped in `starter-workspace/`:

```
cd starter-workspace
docker compose up -d      # or: npm run db:up
npm run db:ping           # must print "database is up."
```

| | |
|---|---|
| Connection | `postgres://pointhub:pointhub@localhost:5432/pointhub` |
| Override with | `DATABASE_URL` — read it from the environment, never hard-code it |
| Port already in use? | change the left-hand number in `docker-compose.yml` and set `DATABASE_URL` to match |
| Start clean | `docker compose down -v` throws the data away |

The database is left in **UTC on purpose.** Business dates here are Asia/Bangkok — expiry month
boundaries and day-of-week campaign rules — and converting them is the application's job. A
database that silently thinks in Bangkok time would hide that decision instead of forcing you
to make it.

## Integration Contracts (mock these in the workshop)

- **Member DB (read-only)**: `GET /members/{memberId}` → `{ memberId, tier: "SILVER"|"GOLD"|"PLATINUM", joinedAt }` — assume it exists; stub it from `sample-data/members.csv` (8 members).
- **POS**: calls PointHub synchronously at checkout. If PointHub is down, POS completes the sale and queues the earn request for retry — so **earn must be idempotent** (`transactionId` is the idempotency key).
- **POS refunds**: a refund arrives as its own transaction with `type = REFUND`, its own `transactionId`, an `originalTransactionId`, and negative line amounts. A refund may return **all** lines of the original or only **some** of them. It is idempotent on its own `transactionId` like any other earn call.

## Money and Points — the constraint, not the solution

Three requirements have to hold at the same time, and satisfying all three is a design problem
this document deliberately does not solve for you:

1. **No floating point** anywhere in money or points arithmetic (see Prohibited, above).
2. **Marketing runs fractional multipliers.** C3 is x2.5 and they will not drop it.
3. **A replay of the year must reproduce the same balances, exactly** — Finance and the external
   auditor both depend on it, and this was an audit finding last year.

The base earn rate, how campaigns combine, where rounding happens and how a refund is reversed
are **business decisions, not platform standards**. They are not written here on purpose. Ask
the business, and record what they tell you — `stakeholder-notes.md` has the interviews, and
in two places the stakeholders contradict each other.

## Non-Functional Expectations

- Earn/burn endpoints: p95 < 150 ms, 50 tx/sec peak
- Every balance change must be an immutable ledger entry (no UPDATE of balances — derive or maintain with ledger + snapshot)
- All manual adjustments require `reasonCode` and `agentId`; write to audit log
- Timezone: Asia/Bangkok for all business dates (expiry month boundaries, day-of-week rules)

## Data Provided

| File | What it is |
|---|---|
| `sample-data/transactions.csv` | 40 POS sales (81 line items) plus 3 refunds — 2 full and 1 partial. Columns: `transactionId, type, originalTransactionId, date, time, storeId, memberId, tier, lineNo, category, amountTHB`. Refund lines carry negative amounts |
| `sample-data/members.csv` | The 8 members with tier and join date — stub the Member DB from this |
| `sample-data/campaign-examples.md` | The 5 campaigns marketing wants to run, and the questions they raise. The answers are in the stakeholder interviews, not here |
| `sample-data/expected-points.csv` | **The answer key.** The points your earn API must post for every transaction |
| `sample-data/check-points.mjs` | Diff your posted points against the answer key. On a mismatch it shows the per-line breakdown so you can see where your calculation diverged |
| `starter-workspace/` | Node 20 + TypeScript 5.5 toolchain only — Express, `pg`, Jest, ESLint, Prettier, already configured to the standards on this page. No `src/` layout: that is Application Design's job |

Replaying the whole file in order (sales then refunds) must leave these balances — this is the finance-reproducibility check in one line:

| M1001 | M1002 | M1003 | M1004 | M1005 | M1006 | M1007 | M1008 |
|---|---|---|---|---|---|---|---|
| 383 | 254 | 374 | 156 | 567 | 452 | 624 | 78 |
