"""Mock VerifyMe e-KYC server for Group 2 (SwiftKYC).

Run:  pip install fastapi uvicorn httpx && python mock_verifyme.py
Listens on http://localhost:9310 — behaviour per verifyme-api-contract.md.

Outcome is driven by the LAST DIGIT of the `reference` you submit:

  last digit  face_match_score  status      identity returned
  ----------  ----------------  ----------  ---------------------------------------------
  1           0.97              COMPLETED   SOMSAK TESTASIRI / 1103700111111  -> BL-001 exact ID hit
  3           0.97              COMPLETED   WICHAI SAETESTA                   -> BL-002/BL-004 fuzzy name hit
  7           0.97              COMPLETED   SOMPORN CHAROENTEST               -> BL-008 exact name hit
  5, 9        0.97              COMPLETED   clean identity, no blocklist hit
  0, 2        0.86              COMPLETED   clean identity  (MANUAL_REVIEW band)
  4           0.62              COMPLETED   clean identity  (reject band, liveness false)
  6           n/a               FAILED      no OCR, failure_reason = ID_EXPIRED
  8           0.97              COMPLETED   clean identity, webhook delivered TWICE

So 1, 3 and 7 all pass face match with 0.97 — the ONLY thing that stops them is
your blocklist screening. An implementation that matches ID exactly but not
names fuzzily will let reference-...3 through.

Also implemented (all documented in the contract):
  * 429 on POST /verifications above 5 requests/second
  * 429 on GET /verifications/{id} more often than once per 10 s
  * 402 QUOTA_EXCEEDED once the billing quota is used up   (--quota, default 60)
  * webhook retried up to 5 times with backoff while your endpoint answers non-2xx

Facilitator endpoints (not in the vendor contract — for the Day-2 audit):
  GET  /_admin/billing   per-reference call counts; any reference with count > 1
                         is a double-billed application
  POST /_admin/reset     clear the quota and the billing ledger
"""
import argparse
import asyncio
import hashlib
import hmac
import json
import time
import uuid
from collections import defaultdict, deque

import httpx
import uvicorn
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

SECRET = b"demo-secret"
API_KEY = "demo-key-123"

app = FastAPI(title="VerifyMe Mock", version="1.3")
store: dict = {}
billing: dict = defaultdict(int)
submit_times: deque = deque()
last_get: dict = {}
CFG = {"quota": 60, "rps": 5, "retries": [1, 2, 4, 8, 16], "delay": 3.0}

CLEAN = {"id_number": "1103700123456", "name_th": "สมชาย เทสต์ดี",
         "name_en": "SOMCHAI TESTDEE", "dob": "1994-02-14", "expiry_date": "2029-05-01"}
# identities that must trip blocklist screening (see blocklist.csv)
HIT_ID = {"id_number": "1103700111111", "name_th": "สมศักดิ์ เทสตะศิริ",
          "name_en": "SOMSAK TESTASIRI", "dob": "1988-07-30", "expiry_date": "2030-01-15"}
HIT_FUZZY = {"id_number": "3102000987654", "name_th": "วิชัย แซ่เทสต์",
             "name_en": "WICHAI SAETESTA", "dob": "1979-11-03", "expiry_date": "2028-09-22"}
HIT_NAME = {"id_number": "1450500246811", "name_th": "สมพร เจริญเทสต์",
            "name_en": "SOMPORN CHAROENTEST", "dob": "1991-04-18", "expiry_date": "2031-03-05"}
IDENTITY = {"1": HIT_ID, "3": HIT_FUZZY, "7": HIT_NAME}


class SubmitIn(BaseModel):
    reference: str
    id_card_image: str
    selfie_image: str
    callback_url: str


def outcome(reference: str) -> dict:
    last = reference.strip()[-1]
    ocr = IDENTITY.get(last, CLEAN)
    base = {"reference": reference, "status": "COMPLETED", "ocr": dict(ocr),
            "liveness_passed": True, "failure_reason": None}
    if last == "6":
        return {**base, "status": "FAILED", "face_match_score": None,
                "liveness_passed": False, "failure_reason": "ID_EXPIRED", "ocr": None}
    if last in "02":
        return {**base, "face_match_score": 0.86}
    if last == "4":
        return {**base, "face_match_score": 0.62, "liveness_passed": False}
    return {**base, "face_match_score": 0.97}  # 1,3,5,7,8,9


async def deliver(vid: str, url: str, times: int):
    """Deliver the webhook `times` times; each delivery retries on non-2xx."""
    await asyncio.sleep(CFG["delay"])  # simulated processing
    body = json.dumps({"verification_id": vid, **store[vid]["result"]}).encode()
    sig = "sha256=" + hmac.new(SECRET, body, hashlib.sha256).hexdigest()
    headers = {"Content-Type": "application/json", "X-Vm-Signature": sig}
    async with httpx.AsyncClient(timeout=10) as client:
        for n in range(times):
            for attempt, backoff in enumerate([0] + CFG["retries"], start=1):
                if backoff:
                    await asyncio.sleep(backoff)
                try:
                    r = await client.post(url, content=body, headers=headers)
                except Exception as e:  # noqa: BLE001
                    print(f"[webhook] {vid} delivery {n + 1} attempt {attempt} FAILED: {e}")
                    continue
                print(f"[webhook] {vid} delivery {n + 1} attempt {attempt} -> HTTP {r.status_code}")
                if 200 <= r.status_code < 300:
                    break
            else:
                print(f"[webhook] {vid} delivery {n + 1} GAVE UP after "
                      f"{len(CFG['retries']) + 1} attempts")


@app.post("/verifications", status_code=202)
async def submit(body: SubmitIn, x_api_key: str = Header(default="")):
    if x_api_key != API_KEY:
        raise HTTPException(401, "bad api key")

    now = time.monotonic()
    while submit_times and now - submit_times[0] > 1.0:
        submit_times.popleft()
    if len(submit_times) >= CFG["rps"]:
        return JSONResponse(status_code=429, content={"error": "RATE_LIMITED",
                                                      "detail": f"max {CFG['rps']} requests/second"},
                            headers={"Retry-After": "1"})
    submit_times.append(now)

    if len(body.id_card_image) < 10 or len(body.selfie_image) < 10:
        raise HTTPException(400, "INVALID_IMAGE")

    if sum(billing.values()) >= CFG["quota"]:
        return JSONResponse(status_code=402, content={"error": "QUOTA_EXCEEDED",
                                                      "detail": f"quota of {CFG['quota']} verifications used"})

    vid = "vm_" + uuid.uuid4().hex[:6]
    store[vid] = {"result": outcome(body.reference), "reference": body.reference}
    billing[body.reference] += 1
    times = 2 if body.reference.strip().endswith("8") else 1
    asyncio.create_task(deliver(vid, body.callback_url, times))

    n = billing[body.reference]
    flag = "  <-- DUPLICATE, this application has now been billed twice" if n > 1 else ""
    print(f"[billing] {vid} for {body.reference} - 1 credit charged "
          f"(call #{n} for this reference, {sum(billing.values())}/{CFG['quota']} used){flag}")
    return {"verification_id": vid, "status": "PROCESSING", "estimated_seconds": 15}


@app.get("/verifications/{vid}")
async def query(vid: str, x_api_key: str = Header(default="")):
    if x_api_key != API_KEY:
        raise HTTPException(401, "bad api key")
    if vid not in store:
        raise HTTPException(404, "unknown verification")
    now = time.monotonic()
    if now - last_get.get(vid, -999) < 10.0:
        return JSONResponse(status_code=429, content={"error": "RATE_LIMITED",
                                                      "detail": "1 request per 10 s per verification"},
                            headers={"Retry-After": "10"})
    last_get[vid] = now
    return {"verification_id": vid, **store[vid]["result"]}


@app.get("/_admin/billing")
async def admin_billing():
    dupes = {ref: n for ref, n in billing.items() if n > 1}
    return {"total_credits": sum(billing.values()), "quota": CFG["quota"],
            "by_reference": dict(billing), "double_billed": dupes}


@app.post("/_admin/reset")
async def admin_reset():
    billing.clear()
    store.clear()
    last_get.clear()
    return {"ok": True}


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="VerifyMe e-KYC mock vendor")
    ap.add_argument("--port", type=int, default=9310)
    ap.add_argument("--quota", type=int, default=60, help="billed calls before 402 QUOTA_EXCEEDED")
    ap.add_argument("--rps", type=int, default=5, help="POST /verifications rate limit")
    ap.add_argument("--delay", type=float, default=3.0, help="seconds before the webhook fires")
    a = ap.parse_args()
    CFG.update(quota=a.quota, rps=a.rps, delay=a.delay)
    print(f"VerifyMe mock on http://localhost:{a.port}  "
          f"api-key={API_KEY}  secret={SECRET.decode()}  quota={a.quota}  rps={a.rps}",
          flush=True)
    uvicorn.run(app, host="0.0.0.0", port=a.port)
