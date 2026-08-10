# PointHub — starter workspace

**This is a toolchain, not a skeleton.** There is deliberately no `src/`, no folder layout
and no example module: deciding the structure is Application Design's job, and pre-empting
it would hand you an answer the workflow is supposed to produce.

What is here is only the plumbing you would otherwise burn the first hour on, already
configured to the company standards in `../technical-environment.md`.

## Set up (5 minutes, before the first exercise)

```
cd starter-workspace
npm install           # ~470 packages, about 30 s
npm run typecheck     # silent = clean
npm test              # 1 suite, 3 tests passed  (the toolchain smoke test)
npm run lint          # silent = clean

npm run db:up         # starts PostgreSQL 15 in Docker (first run pulls, ~30 s)
npm run db:ping       # "database is up."
```

All six must be green before you paste the trigger phrase. If any of them is not, call the
facilitator now rather than at 14:00.

Docker Desktop has to be running for the last two. Everything is local — the image is pulled
once and nothing talks to a cloud after that.

`__tests__/toolchain.test.ts` asserts nothing about PointHub — it only proves Node, strict
TypeScript and Jest are working. Delete it or keep it, whichever you prefer.

Then go back up one level. **Open your AI assistant at the group folder, not here** — that is
where `vision-document.md`, `technical-environment.md`, `stakeholder-notes.md` and
`sample-data/` live, and the workflow cannot answer its own questions without them.
`aidlc-docs/` appears up there too. This folder stays the Node project root: `npm test` and
`npm run lint` are run from here.

See `../README.md` for the full start-up sequence.

## What is already decided for you

| | |
|---|---|
| Node | 20.x (`engines` pins it — `npm install` warns if you are on 18 or 22) |
| TypeScript | 5.5, `strict` **plus** `noUncheckedIndexedAccess` and `exactOptionalPropertyTypes` |
| API framework | Express 4 |
| Database | PostgreSQL 15 in Docker, on localhost:5432. `docker-compose.yml` is here |
| Database driver | `pg` (node-postgres) — no ORM, raw SQL with typed helpers |
| Connection string | `DATABASE_URL`, defaulting to `postgres://pointhub:pointhub@localhost:5432/pointhub` |
| Tests | Jest 29 + ts-jest, tests in `__tests__/`, files named `*.test.ts` |
| Lint / format | ESLint + Prettier, `npm run lint`, `npm run format` |

Database commands: `npm run db:up` · `npm run db:ping` · `npm run db:down`
(`docker compose down -v` if you want to wipe the data and start clean).

Two lint rules exist to catch the prohibitions in the technical environment before a
reviewer has to:

- importing `prisma`, `typeorm`, `sequelize` or `axios` is an **error**
- `parseFloat` is an **error** — points and money are integers here (see the milli-points
  scheme in `../sample-data/campaign-examples.md`)

If the workflow proposes a design that needs one of those, that is a conversation to have
at the gate and record — not a rule to switch off quietly.

## What is NOT here, on purpose

- No `src/` layout, no module boundaries, no example service — Application Design decides
- No database schema or migrations — an empty database is running; what goes in it comes out
  of the design
- No Dockerfile for the service itself, no IaC, no deployment — everything runs from your own
  machine and stops when you close the laptop
- No member-DB stub — build it from `../sample-data/members.csv` when the design calls for it
