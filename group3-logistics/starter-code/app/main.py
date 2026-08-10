from datetime import datetime

import sqlalchemy as sa
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .db import cod_collections, engine, init_db, parcels, status_history

app = FastAPI(title="ParcelTrack", version="1.4.2")
init_db()


def now() -> str:
    return datetime.utcnow().isoformat() + "Z"


class ParcelIn(BaseModel):
    merchant_id: str
    recipient_name: str
    recipient_phone: str
    address: str
    district: str
    cod_amount: float = 0.0


class StatusIn(BaseModel):
    status: str
    note: str | None = None
    rider_id: str | None = None


class CodIn(BaseModel):
    rider_id: str
    amount: float


@app.post("/parcels", status_code=201)
def create_parcel(body: ParcelIn):
    with engine.begin() as conn:
        count = conn.execute(sa.select(sa.func.count()).select_from(parcels)).scalar_one()
        pid = f"TEX-2026-{count + 1:06d}"
        conn.execute(parcels.insert().values(
            id=pid, merchant_id=body.merchant_id, recipient_name=body.recipient_name,
            recipient_phone=body.recipient_phone, address=body.address, district=body.district,
            cod_amount=body.cod_amount, status="CREATED", rider_id=None,
            created_at=now(), updated_at=now(),
        ))
        conn.execute(status_history.insert().values(parcel_id=pid, status="CREATED", note=None, at=now()))
    return {"id": pid, "status": "CREATED"}


@app.get("/parcels/{parcel_id}")
def get_parcel(parcel_id: str):
    with engine.connect() as conn:
        row = conn.execute(sa.select(parcels).where(parcels.c.id == parcel_id)).mappings().first()
        if not row:
            raise HTTPException(404, "parcel not found")
        hist = conn.execute(
            sa.select(status_history).where(status_history.c.parcel_id == parcel_id).order_by(status_history.c.id)
        ).mappings().all()
    return {**dict(row), "history": [dict(h) for h in hist]}


@app.put("/parcels/{parcel_id}/status")
def update_status(parcel_id: str, body: StatusIn):
    # NOTE: accepts whatever status string the caller sends. The rider app team
    # said they validate on their side. (TODO from 2024, nobody remembers why.)
    with engine.begin() as conn:
        row = conn.execute(sa.select(parcels).where(parcels.c.id == parcel_id)).mappings().first()
        if not row:
            raise HTTPException(404, "parcel not found")
        values = {"status": body.status, "updated_at": now()}
        if body.rider_id:
            values["rider_id"] = body.rider_id
        conn.execute(parcels.update().where(parcels.c.id == parcel_id).values(**values))
        conn.execute(status_history.insert().values(parcel_id=parcel_id, status=body.status, note=body.note, at=now()))
    return {"id": parcel_id, "status": body.status}


@app.post("/parcels/{parcel_id}/cod", status_code=201)
def record_cod(parcel_id: str, body: CodIn):
    with engine.begin() as conn:
        row = conn.execute(sa.select(parcels).where(parcels.c.id == parcel_id)).mappings().first()
        if not row:
            raise HTTPException(404, "parcel not found")
        conn.execute(cod_collections.insert().values(
            parcel_id=parcel_id, rider_id=body.rider_id, amount=body.amount, collected_at=now(),
        ))
    return {"ok": True}


@app.get("/riders/{rider_id}/parcels")
def rider_parcels(rider_id: str):
    with engine.connect() as conn:
        rows = conn.execute(sa.select(parcels).where(parcels.c.rider_id == rider_id)).mappings().all()
    return [dict(r) for r in rows]
