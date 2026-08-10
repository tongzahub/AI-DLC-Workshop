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
| 1 · PointHub | Node.js **20 LTS** + npm | `node -v` → v20.x |
| 2 · SwiftKYC | Python **3.12** + pip | `python --version` → 3.12.x |
| 3 · ParcelTrack | Python **3.12** + pip | `python --version` → 3.12.x |
| 4 · LineMetrics | Python **3.12** + pip | `python --version` → 3.12.x |

Version note: the kits are tested against Python 3.12 and Node 20 exactly. A newer Python
(3.13+) should not be used for the venv; a newer Node usually works but 20 LTS is the baseline.

## Nice to have (saves time if the venue network is busy)

- [ ] A second laptop per team for reading documents while the driver types
- [ ] `npm install` (Group 1) or `pip download -r requirements.txt` (Groups 2–4) run once at
      home, so package caches are warm
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
