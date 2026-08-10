# Campaign Examples from Marketing (validate your rules design against all 5)

| # | Campaign | Rule | Period | Notes |
|---|---|---|---|---|
| C1 | Fresh Weekend | x3 points on category FRESH, Sat–Sun only | 1 Sep – 30 Sep | all tiers |
| C2 | Gold Boost | x2 points on everything for GOLD | 1 Sep – 15 Sep | GOLD only |
| C3 | Platinum Everyday | x2.5 points on everything for PLATINUM | always-on | no end date |
| C4 | Payday Splurge | x5 points storewide | 25 Sep – 28 Sep | all tiers; marketing expects this to be "the best deal" and override others |
| C5 | Home & Living Push | x2 on category HOME | 10 Sep – 10 Oct | overlaps C1/C2/C4 on some days |

Test questions for the team (the AI should surface these):
- On Sat 27 Sep, a GOLD member buys FRESH items. C1 (x3), C2 has ended, C4 (x5) both could apply → which wins? (Marketing: best single multiplier → x5)
- Does C3 (always-on) stack with C4? (No — best single)
- What happens to points earned under a campaign that is later deactivated retroactively? (Earned points stand; deactivation is forward-only)
- **What if two campaigns tie?** On Sat 12 Sep a GOLD member buys HOME: C2 (x2) and C5 (x2) both apply at the same multiplier. The points are the same either way, but the ledger has to say *which* campaign was credited — pick a deterministic tie-break rule (lowest campaign id is fine) and record it, or your replay will not be reproducible.

## C3 is x2.5 — and money math may not use floats

The technical environment prohibits floating point for points math, but marketing wants a
x2.5 multiplier. Store multipliers **scaled by 1000** and work in *milli-points*:

```
mult_x1000     BASE 1000 · C1 3000 · C2 2000 · C3 2500 · C4 5000 · C5 2000
milli(line)  = amountTHB * (mult_x1000 / 25)      # 40, 120, 80, 100, 200 — all exact integers
basket       = sum of milli(line) over the line items
posted       = basket // 1000                     # floor, ONCE, per basket
```

Every value stays an integer, and the result is bit-for-bit reproducible for audit.

## Where the answers are

`expected-points.csv` is the ground truth for all 40 sales and 3 refunds — the points your
earn API must post, per transaction. `expected-points-by-line.csv` breaks it down to the
winning campaign and milli-points per line item, so when a number is off you can see which
line disagrees.

Five of those rows exist purely to catch a wrong design:

| Transaction | Catches |
|---|---|
| TX90007 | flooring per **line** (27 points) instead of per **basket** (29 points) |
| TX90006 | not flooring at all — 749 THB × x2 = 59.92 points must post as 59 |
| TX90004 | mishandling the x2.5 multiplier |
| TX90002 | a non-deterministic tie-break between C2 and C5 |
| RF90003 | a partial refund clawed back per line (16) instead of by recomputing the basket (17) |
