#!/usr/bin/env python3
"""Merchant webhook test receiver for CR-2026-081 (Group 3 — ParcelTrack).

Standard library only — no pip install needed.

    python webhook_receiver.py                       # listen on :9410 as merchant M-100
    python webhook_receiver.py --port 9411 --merchant M-113 --secret whsec_m113_2b8c41
    python webhook_receiver.py --fail                # always answer 500 (retry demo)
    python webhook_receiver.py --fail-first 3        # 500 for the first 3 deliveries, then 200
    python webhook_receiver.py --no-verify           # accept any signature (or none)

Secrets come from ../merchants.csv; the defaults below match M-100 in that file.

What it prints per delivery
---------------------------
    #1  20:14:07  POST /webhooks/parceltrack  ->  200   sig OK
        TEX-2026-004013  status=DELIVERED

Signature check: HMAC-SHA256 over the *raw* request body using the merchant
secret, read from the `X-Tex-Signature` header. Both `sha256=<hex>` and a bare
`<hex>` are accepted, so a prefix mismatch will not derail your demo; the value
actually received is printed so you can see what you sent. A missing or wrong
signature is answered with **401** (a real merchant would do the same, and your
retry logic should treat it as a failed delivery). Use `--no-verify` while you
are still wiring things up.

The acceptance demo (from change-request.md):
  1. start this receiver
  2. register the callback URL + secret for M-100 through your new API
  3. update a parcel's status  -> one signed delivery appears here within 30 s
  4. stop this receiver, update status again -> 5 retries in your delivery log
  5. start it again -> the next event is delivered
"""
import argparse
import hashlib
import hmac
import json
import sys
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

STATE = {"count": 0, "seen": {}, "fail_remaining": 0, "always_fail": False,
         "secret": b"", "merchant": "", "verify": True}


def check_signature(raw: bytes, header: str):
    """-> (ok, message)"""
    if not header:
        return False, "NO SIGNATURE HEADER"
    expected = hmac.new(STATE["secret"], raw, hashlib.sha256).hexdigest()
    got = header.split("=", 1)[1].strip() if header.lower().startswith("sha256=") else header.strip()
    if hmac.compare_digest(expected.lower(), got.lower()):
        return True, "sig OK"
    return False, f"SIG MISMATCH (expected {expected[:16]}..., got {got[:16]}...)"


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *_args):  # silence the default access log
        pass

    def do_POST(self):  # noqa: N802
        raw = self.rfile.read(int(self.headers.get("Content-Length") or 0))
        STATE["count"] += 1
        n = STATE["count"]
        sig_ok, sig = check_signature(raw, self.headers.get("X-Tex-Signature", ""))

        if STATE["always_fail"] or STATE["fail_remaining"] > 0:
            if STATE["fail_remaining"] > 0:
                STATE["fail_remaining"] -= 1
            code, note = 500, "  <- answering 500 on purpose"
        elif STATE["verify"] and not sig_ok:
            code, note = 401, "  <- rejected, run with --no-verify to accept anyway"
        else:
            code, note = 200, ""

        body = {200: b'{"received":true}',
                401: b'{"error":"invalid signature"}',
                500: b'{"error":"simulated outage"}'}[code]
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

        stamp = datetime.now().strftime("%H:%M:%S")
        print(f"#{n:<3} {stamp}  POST {self.path}  ->  {code}   {sig}{note}")
        try:
            event = json.loads(raw)
        except Exception:  # noqa: BLE001
            print(f"     raw body ({len(raw)} bytes): {raw[:200]!r}")
            sys.stdout.flush()
            return

        parcel = event.get("parcel_id") or event.get("parcelId") or event.get("id") or "?"
        status = event.get("status") or (event.get("data") or {}).get("status") or "?"
        event_id = event.get("event_id") or event.get("eventId")
        dup = ""
        if event_id:
            STATE["seen"][event_id] = STATE["seen"].get(event_id, 0) + 1
            if STATE["seen"][event_id] > 1:
                dup = f"   [duplicate delivery #{STATE['seen'][event_id]} of {event_id}]"
        print(f"     {parcel}  status={status}{dup}")
        print(f"     {json.dumps(event, ensure_ascii=False)[:300]}")
        sys.stdout.flush()

    def do_GET(self):  # noqa: N802
        body = json.dumps({"merchant": STATE["merchant"], "deliveries": STATE["count"]}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main():
    ap = argparse.ArgumentParser(description="ParcelTrack merchant webhook test receiver")
    ap.add_argument("--port", type=int, default=9410)
    ap.add_argument("--merchant", default="M-100")
    ap.add_argument("--secret", default="whsec_m100_7d3f9a")
    ap.add_argument("--fail", action="store_true", help="always answer 500")
    ap.add_argument("--fail-first", type=int, default=0, metavar="N",
                    help="answer 500 for the first N deliveries, then 200")
    ap.add_argument("--no-verify", action="store_true",
                    help="accept deliveries with a missing or wrong signature")
    a = ap.parse_args()

    # Python block-buffers stdout when it is not a terminal (a redirect, a pipe, or some IDE
    # consoles), which would hide every line below until the process exits.
    sys.stdout.reconfigure(line_buffering=True)

    STATE.update(secret=a.secret.encode(), merchant=a.merchant, verify=not a.no_verify,
                 always_fail=a.fail, fail_remaining=a.fail_first)

    mode = "ALWAYS 500" if a.fail else (f"500 for first {a.fail_first}" if a.fail_first else "200 OK")
    print(f"ParcelTrack webhook receiver - merchant {a.merchant}")
    print(f"  listening on  http://localhost:{a.port}/webhooks/parceltrack   (any path is accepted)")
    print(f"  secret        {a.secret}")
    print(f"  signature     {'REQUIRED - bad or missing gets 401' if STATE['verify'] else 'not checked (--no-verify)'}")
    print(f"  response mode {mode}")
    print(f"  GET http://localhost:{a.port}/ returns the delivery count")
    print("  Ctrl-C to stop (stopping it is how you demo the retry path)\n")
    try:
        ThreadingHTTPServer(("0.0.0.0", a.port), Handler).serve_forever()
    except KeyboardInterrupt:
        print(f"\nstopped after {STATE['count']} deliveries")


if __name__ == "__main__":
    main()
