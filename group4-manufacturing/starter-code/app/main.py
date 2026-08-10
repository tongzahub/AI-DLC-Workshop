from datetime import datetime

import sqlalchemy as sa
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .db import engine, init_db, plan, readings
from .oee import compute_oee

app = FastAPI(title="LineMetrics", version="0.9.1")
init_db()


class ReadingIn(BaseModel):
    reading_id: str          # unique per cycle event, reused on gateway retry
    line_id: str             # L-01 .. L-08
    ts: str                  # ISO-8601 UTC, e.g. 2026-09-15T19:04:22Z
    cycle_count: int         # pieces produced in this report window
    reject_count: int        # rejected pieces out of cycle_count
    downtime_minutes: float = 0.0


@app.post("/readings", status_code=201)
def ingest(body: ReadingIn):
    # Gateways post every ~5 minutes per line.
    with engine.begin() as conn:
        conn.execute(readings.insert().values(
            reading_id=body.reading_id, line_id=body.line_id, ts=body.ts,
            cycle_count=body.cycle_count, reject_count=body.reject_count,
            downtime_minutes=body.downtime_minutes,
        ))
    return {"ok": True}


@app.get("/oee/{line_id}")
def oee_for_day(line_id: str, date: str):
    """OEE for a line on a given date (YYYY-MM-DD)."""
    with engine.connect() as conn:
        p = conn.execute(
            sa.select(plan).where(plan.c.line_id == line_id, plan.c.date == date)
        ).mappings().first()
        if not p:
            raise HTTPException(404, "no plan for that line/date")
        rows = conn.execute(
            sa.select(readings).where(
                readings.c.line_id == line_id,
                readings.c.ts >= f"{date}T00:00:00Z",
                readings.c.ts <= f"{date}T23:59:59Z",
            )
        ).mappings().all()

    total = sum(r["cycle_count"] for r in rows)
    rejects = sum(r["reject_count"] for r in rows)
    downtime = sum(r["downtime_minutes"] for r in rows)
    result = compute_oee(
        planned_minutes=p["planned_minutes"],
        downtime_minutes=downtime,
        ideal_cycle_time=p["ideal_cycle_time"],
        total_count=total,
        good_count=total - rejects,
    )
    return {"line_id": line_id, "date": date, "readings": len(rows), **result}


@app.get("/health")
def health():
    return {"status": "ok", "at": datetime.utcnow().isoformat() + "Z"}
