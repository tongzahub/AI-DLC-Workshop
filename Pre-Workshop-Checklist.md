# Pre-Workshop Checklist — send to every team 2–3 days before Day 1

> The single biggest risk to Day 1 morning is an AI assistant that cannot log in.
> Everything on this page must be **done and verified before you arrive**, on the laptop
> your team will actually use. Ten minutes now saves your team an hour on the day.

## Per team (one shared laptop — the driver rotates, the laptop does not)

- [ ] **AI coding assistant installed, licensed and logged in** — one of: Kiro, Amazon Q
      Developer, Cursor, Cline, Claude Code, GitHub Copilot, Codex
- [ ] **The assistant answers a test prompt** ("write a haiku about parcels") — this proves
      login, license *and* network in one shot. A spinner is not a pass
- [ ] **Git installed** — `git --version` prints a version
- [ ] Team knows **which group it is (1–4)** and which runtime that means (below)

## Runtime — install the one your group needs

| Group | Install | Verify |
|---|---|---|
| 1 · PointHub | Node.js **20 LTS** + npm · **Docker Desktop** | `node -v` → v20.x · `docker run --rm hello-world` prints a greeting |
| 2 · SwiftKYC | Python **3.12** + pip · **Docker Desktop** | `python --version` → 3.12.x · `docker run --rm hello-world` prints a greeting |
| 3 · ParcelTrack | Python **3.12** + pip | `python --version` → 3.12.x |
| 4 · LineMetrics | Python **3.12** + pip | `python --version` → 3.12.x |

Version note: the kits are tested against Python 3.12 and Node 20 exactly. A newer Python
(3.13+) should not be used for the venv; a newer Node usually works but 20 LTS is the baseline.

### Groups 1 and 2 — the database, and why Docker

Your service stores data in PostgreSQL 15. It runs **on your own laptop**, in a container that
the kit's `docker-compose.yml` starts for you — no cloud account, no server to configure, no
connection details to invent. Groups 3 and 4 use SQLite and need none of this.

**Pull the image at home**, so a room full of teams is not fetching it over the venue Wi-Fi
at 09:45:

```
docker pull postgres:15-alpine
```

- [ ] **Docker Desktop installed and actually starting.** On a corporate laptop this is the
      single most likely thing to be blocked — check it *now*, not on the morning. If your IT
      policy forbids Docker Desktop, tell the facilitator this week: there is a fallback, but
      it needs arranging in advance.
- [ ] `docker run --rm hello-world` prints its greeting
- [ ] `docker pull postgres:15-alpine` completes

## Nice to have (saves time if the venue network is busy)

- [ ] A second laptop per team for reading documents while the driver types
- [ ] `npm install` (Group 1) or `pip download -r requirements.txt` (Groups 2–4) run once at
      home, so package caches are warm
- [ ] Groups 1–2: `docker pull postgres:15-alpine` done at home (see above)
- [ ] A markdown-capable editor (VS Code is fine) for reading `.md` files and answering
      question files

## What you do NOT need to do in advance

- Do **not** download the AI-DLC rules bundle yet — the facilitator names the exact version
  on the morning (and carries it on USB as a fallback)
- Do **not** read ahead in another group's folder — each group's exercise only works unspoiled

## On the morning, before 09:00

Your group README, §1: install the rules, run the toolchain check, verify the trigger phrase
answers with the AI-DLC welcome message. If anything is not green, call the facilitator
**then** — not at 14:00.
