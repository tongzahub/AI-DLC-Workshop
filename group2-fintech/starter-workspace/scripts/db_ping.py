#!/usr/bin/env python3
"""Prove the workshop database is reachable, before you build anything against it.

    python scripts/db_ping.py

This is toolchain, not application code — it makes no assumption about your
schema and creates nothing.
"""
import os
import re
import sys

URL = os.environ.get(
    "DATABASE_URL", "postgresql://swiftkyc:swiftkyc@localhost:5433/swiftkyc"
)
SAFE = re.sub(r":[^:@/]*@", ":****@", URL)


def main() -> int:
    try:
        import psycopg
    except ImportError:
        print("psycopg is not installed. Run:  pip install -r requirements.txt")
        return 1

    try:
        with psycopg.connect(URL, connect_timeout=5) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "select current_database(), version(), (now() at time zone 'UTC')"
                )
                row = cur.fetchone()
        if row is None:
            print(f"connected to {SAFE} but the server returned nothing — that is not normal")
            return 1
        db, version, utc_now = row
    except Exception as e:
        print(f"\ncannot reach the database at {SAFE}")
        print(f"  {e}\n")
        print("Start it first, from this folder:")
        print("    docker compose up -d")
        print('`docker compose ps` should show "healthy" before you retry.')
        print("If Docker Desktop itself is not running, start that first.")
        return 1

    print(f"  url      {SAFE}")
    print(f"  database {db}")
    print(f"  server   {version.split(',')[0]}")
    print(f"  utc now  {utc_now.isoformat()}")
    print("\ndatabase is up.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
