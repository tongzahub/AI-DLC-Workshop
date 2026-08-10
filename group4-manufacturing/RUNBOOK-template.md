# RUNBOOK — LineMetrics (template)

> One page ops can actually use — that is the Definition of Done. Replace every
> *(prompt)* with your own content and delete this line. If a section would be empty,
> say why rather than deleting it.

## What this service is

*(Two sentences: what it computes, who reads it, when it matters — the 08:00 meeting.)*

## Start / stop / health

```
# start        *(exact command, from which folder)*
# stop         *(how, and what happens to in-flight requests)*
# health check *(the URL and what a good response looks like)*
```

## Seeding and re-seeding data

*(The seed command, whether it is idempotent, and how to verify the seed took —
which endpoint, which number should come back.)*

## Endpoints

| Endpoint | Who calls it | Normal response | Known edge case |
|---|---|---|---|
| `POST /readings` | plant gateways | | *(duplicate reading_id? different payload, same id?)* |
| `GET /oee/{line}?date=` | dashboards | | *(maintenance day? no readings? downtime > planned?)* |

## When the numbers look wrong — check in this order

1. *(The first thing to rule out, and the command that rules it out.)*
2. *(The second — e.g. how to tell a data problem from a calculation problem.)*
3. *(How to compare against the hand-calculation ground truth.)*

## Invariants that must always hold

*(The properties your PBT suite enforces — each factor and OEE in [0,1], one production
day per reading, idempotent ingestion. State them as sentences ops can check.)*

## Escalation

*(Who to call for: gateway/firmware issues · ground-truth disputes · code changes.
Remember: the vendor's firmware is frozen and Production Engineering owns the ground truth.)*
