"""Load plan rows and a readings JSONL file into the local DB.

Usage:  python seed.py [path/to/sample-readings.jsonl]
Default path is ../sample-readings.jsonl (the file shipped one level up).
"""
import json
import os
import sys

import sqlalchemy as sa

from app.db import engine, init_db, plan, readings

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_READINGS = os.path.join(HERE, os.pardir, "sample-readings.jsonl")

PLAN = [
    # line, production date, planned_minutes, ideal_cycle_time (min/piece)
    ("L-03", "2026-09-14", 480, 0.5),
    ("L-03", "2026-09-15", 480, 0.5),
    ("L-03", "2026-09-16", 480, 0.5),
    ("L-05", "2026-09-14", 0, 0.5),      # planned maintenance day (INC-1042)
    ("L-01", "2026-09-15", 480, 0.4),
    ("L-07", "2026-09-15", 480, 0.6),
]

path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_READINGS
if not os.path.exists(path):
    sys.exit(f"readings file not found: {path}\n"
             f"run this from starter-code/ as:  python seed.py ../sample-readings.jsonl")

init_db()
with engine.begin() as conn:
    conn.execute(sa.delete(readings))
    conn.execute(sa.delete(plan))
    for line, date, mins, ict in PLAN:
        conn.execute(plan.insert().values(line_id=line, date=date,
                                          planned_minutes=mins, ideal_cycle_time=ict))
    n = 0
    with open(path, encoding="utf-8") as f:
        for ln in f:
            if not ln.strip():
                continue
            conn.execute(readings.insert().values(**json.loads(ln)))
            n += 1
print(f"seeded {len(PLAN)} plan rows and {n} readings from {os.path.relpath(path, HERE)}")
