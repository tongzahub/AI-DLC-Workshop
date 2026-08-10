#!/usr/bin/env python3
"""Is the workshop database reachable from this machine?

    python check_db.py

Standard library only, on purpose: at this point you have not chosen a database
driver yet, and this script must not choose one for you. It checks that something
is listening on the port the compose file publishes — which is all you need to know
before you start. Your own connection test comes later, once your design has picked
a driver.
"""
import os
import socket
import sys

HOST = os.environ.get("PGHOST", "127.0.0.1")
PORT = int(os.environ.get("PGPORT", "5433"))


def main() -> int:
    try:
        with socket.create_connection((HOST, PORT), timeout=4):
            pass
    except OSError as e:
        print(f"\nnothing is listening on {HOST}:{PORT}")
        print(f"  {e}\n")
        print("Start it, from this folder:")
        print("    docker compose up -d")
        print('`docker compose ps` should show "healthy" before you retry.')
        print("If Docker Desktop itself is not running, start that first.")
        return 1

    print(f"  postgres is accepting connections on {HOST}:{PORT}")
    print(f"  connection string: postgresql://swiftkyc:swiftkyc@{HOST}:{PORT}/swiftkyc")
    print("\ndatabase is up.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
