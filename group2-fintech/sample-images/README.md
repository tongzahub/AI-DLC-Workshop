# Sample images for VerifyMe submissions

The mock never looks at pixels — it only checks that each base64 string is at least
10 characters (`400 INVALID_IMAGE` below that). These files exist so you have
something real to post while building, without hunting for a photo.

| File | What it stands for |
|---|---|
| `id-card.b64.txt` | Thai national ID card front (base64 PNG, 196 chars) |
| `selfie.b64.txt` | Applicant selfie (base64 PNG, 168 chars) |
| `blurry.b64.txt` | Small/unreadable image — still over the 10-char floor, so use it as your own "too small to accept" fixture if you add client-side validation |
| `sample-submit.json` | A ready-to-post `POST /verifications` body, reference `APP-2026-000001` |

Quick check that the mock is up (from this folder):

```
python -c "import json,urllib.request as u; b=open('sample-submit.json','rb').read(); \
  print(u.urlopen(u.Request('http://localhost:9310/verifications', b, \
  {'Content-Type':'application/json','X-Api-Key':'demo-key-123'})).read())"
```

Reference `APP-2026-000001` ends in `1`, so it comes back with face match 0.97 **and**
the identity `SOMSAK TESTASIRI / 1103700111111`, which is `BL-001` on the blocklist.
Change the last digit of the reference to steer the outcome — the full map is at the
top of `mock_verifyme.py` and in `verifyme-api-contract.md`.

These are real PNG files. To view one:

```
python -c "import base64; open('id-card.png','wb').write(base64.b64decode(open('id-card.b64.txt').read()))"
```
