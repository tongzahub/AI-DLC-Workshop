# SwiftKYC — starter workspace

**This is a toolchain, not a skeleton.** No `app/`, no module layout, no example endpoint:
deciding the structure is Application Design's job, and this is a regulated build where
that design has to answer to the Security extension.

## Set up (5 minutes, before the first exercise)

```
cd starter-workspace
python -m venv .venv
.venv\Scripts\activate          # Windows.  macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m pytest                 # 3 passed  (the toolchain smoke test)
ruff check .                     # All checks passed!
mypy .                           # Success: no issues found
```

All three must be green before you paste the trigger phrase. If any of them is not, call the
facilitator now rather than at 14:00.

`tests/test_toolchain.py` asserts nothing about SwiftKYC — it only proves Python 3.12, the
libraries, and AES-256-GCM are all working. Note that it is annotated `-> None`: `mypy` runs
strict here, and that includes your tests.

Then go back up one level. **Open your AI assistant at the group folder, not here** — that is
where `vision-document.md`, `technical-environment.md`, `stakeholder-notes.md`,
`verifyme-api-contract.md` and `blocklist.csv` live, and the workflow cannot answer its own
questions without them. `aidlc-docs/` appears up there too. This folder stays the Python
project root: `pytest`, `ruff` and `mypy` are run from here.

The VerifyMe mock also runs from the folder **above** this one, in its own terminal, and stays
running all day:

```
cd ..
python mock_verifyme.py          # http://localhost:9310
```

See `../README.md` for the full start-up sequence.

## What is already decided for you

| | |
|---|---|
| Python | 3.12 |
| API framework | FastAPI + Pydantic v2 |
| Database | SQLAlchemy Core or psycopg — no lazy-loading ORM models |
| Crypto | `cryptography` (AES-256-GCM, key from env) — never home-made |
| Tests | pytest + httpx TestClient, tests in `tests/` |
| Lint / types | `ruff check .` and `mypy .`, both configured strict |

`ruff` is set up with the **flake8-bandit (`S`) rules enabled**. Once you opt in to the
Security extension those stop being style nits and become gate findings — hardcoded
secrets, weak hashes, `subprocess` with shell, unvalidated input. Do not silence a rule to
get past a gate; fix the design and record the decision.

`mypy` runs in `strict` mode. Everything the vendor sends you is untrusted input arriving
as `Any` — making the types explicit at that boundary is the point.

## What is NOT here, on purpose

- No application layout or state machine — Application Design decides both
- No `secure-store/` and no encryption key — creating one is part of the security design;
  the key comes from an environment variable, never from a file in the repo
- No database schema or migrations
- No consent, blocklist or webhook code — those are the exercise

## The one thing to get right before you write any code

Every artifact you produce here can end up in front of the auditor on Day 2, including your
logs. Decide **before** the first log line what a masked ID number looks like
(`x-xxxx-xxxx-12-3`) and where that formatting lives, because retrofitting masking across a
codebase on Day 2 afternoon does not go well.
