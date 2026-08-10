"""Load a COD day (sample-cod-day.csv) into the local ParcelTrack database.

Usage:  python seed_cod.py [path/to/sample-cod-day.csv]
Default path is ../sample-cod-day.csv (the file shipped one level up).

Why this script exists
----------------------
`POST /parcels` generates its own sequential parcel id, so the ids in the CSV
(TEX-2026-004001 ...) cannot be created through the API. This seeder writes the
day straight into the existing tables so the CR acceptance demo has data to run
against. It does NOT change the schema — new tables/columns are the team's job.

Timestamps
----------
The CSV carries Asia/Bangkok local times because that is how operations reads
them. The running service stores naive UTC strings ending in "Z", so this
seeder converts on the way in — exactly like the live system would have. The
20:00 Bangkok cutoff therefore has to be applied by converting back.

Re-running is safe: rows for the parcel ids in the CSV are deleted first.
"""
import csv
import os
import sys
from datetime import datetime, timedelta, timezone

import sqlalchemy as sa

from app.db import cod_collections, engine, init_db, parcels, status_history

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CSV = os.path.join(HERE, os.pardir, "sample-cod-day.csv")
BKK = timezone(timedelta(hours=7))

DISTRICTS = ["Bang Rak", "Huai Khwang", "Chatuchak", "Watthana", "Din Daeng",
             "Phaya Thai", "Lat Phrao", "Bang Na"]
NAMES = ["Somchai P.", "Pranee S.", "Nattapong K.", "Suda W.", "Anucha T.",
         "Malee C.", "Kittipong R.", "Orawan M."]


def z(dt_bkk: datetime) -> str:
    """Bangkok-aware datetime -> the naive-UTC + 'Z' string the service writes."""
    return dt_bkk.astimezone(timezone.utc).replace(tzinfo=None).isoformat() + "Z"


path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CSV
if not os.path.exists(path):
    sys.exit(f"csv not found: {path}\n"
             f"run this from starter-code/ as:  python seed_cod.py ../sample-cod-day.csv")

with open(path, encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

init_db()
ids = [r["parcelId"] for r in rows]
n_parcels = n_collections = 0

with engine.begin() as conn:
    conn.execute(cod_collections.delete().where(cod_collections.c.parcel_id.in_(ids)))
    conn.execute(status_history.delete().where(status_history.c.parcel_id.in_(ids)))
    conn.execute(parcels.delete().where(parcels.c.id.in_(ids)))

    for i, r in enumerate(rows):
        delivered = datetime.fromisoformat(r["deliveredAt"])
        created = delivered - timedelta(days=1, hours=2)
        picked = delivered - timedelta(hours=3)
        out = delivered - timedelta(minutes=40)

        conn.execute(parcels.insert().values(
            id=r["parcelId"],
            merchant_id=r["merchantId"],
            recipient_name=NAMES[i % len(NAMES)],
            recipient_phone=f"08{10000000 + i * 137:08d}"[:10],
            address=f"{100 + i} Sukhumvit Rd",
            district=DISTRICTS[i % len(DISTRICTS)],
            cod_amount=float(r["codAmountTHB"]),
            status="DELIVERED",
            rider_id=r["riderId"],
            created_at=z(created),
            updated_at=z(delivered),
        ))
        n_parcels += 1

        for status, at in (("CREATED", created), ("PICKED_UP", picked),
                           ("OUT_FOR_DELIVERY", out), ("DELIVERED", delivered)):
            conn.execute(status_history.insert().values(
                parcel_id=r["parcelId"], status=status, note=None, at=z(at)))

        if r["recordedAmountTHB"].strip():
            conn.execute(cod_collections.insert().values(
                parcel_id=r["parcelId"],
                rider_id=r["riderId"],
                amount=float(r["recordedAmountTHB"]),
                collected_at=z(datetime.fromisoformat(r["recordedAt"])),
            ))
            n_collections += 1

print(f"seeded {n_parcels} parcels and {n_collections} COD collections "
      f"from {os.path.relpath(path, HERE)}")
print(f"  {n_parcels - n_collections} delivered parcel(s) have no collection recorded")
