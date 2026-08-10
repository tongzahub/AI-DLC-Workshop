# LineMetrics v0.9.1

OEE service for the Apex Auto Parts plant floor. Gateways POST /readings; dashboards call GET /oee/{line}?date=.

Run:  `pip install -r requirements.txt && uvicorn app.main:app --reload`
Test: `python -m pytest`

Seed the September plan + readings (run from this folder):

```
python seed.py ../sample-readings.jsonl
```

`seed.py` wipes and reloads the `plan` and `readings` tables, so it is safe to run repeatedly.
It seeds lines L-01, L-03, L-05 and L-07 for 14–16 September 2026.
