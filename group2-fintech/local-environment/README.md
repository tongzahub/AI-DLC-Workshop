# local-environment — a database, and nothing else

This folder is **not** your project. It exists so you have a PostgreSQL 15 running on your own
machine, and nothing more. There is no `pyproject.toml` here, no framework, no test runner, no
lint config — because choosing those is Application Design's job, and in a regulated build those
choices have to be defended at a gate rather than inherited from a starter kit.

## Use it

```
docker compose up -d      # PostgreSQL 15; the first run pulls the image, ~30 s
docker compose ps         # must say "healthy"
python check_db.py        # "database is up."
```

Then leave it running and go back up a level. Your project root is the **group folder**, not
this one. The VerifyMe mock also runs from up there, in its own terminal.

| | |
|---|---|
| Connection | `postgresql://swiftkyc:swiftkyc@localhost:5433/swiftkyc` |
| Read it from | `DATABASE_URL` in the environment — never hard-code it |
| Port | 5433, so it does not collide with a Postgres you may already run |
| Stop it | `docker compose down` (keeps the data) |
| Start over | `docker compose down -v` (throws the data away) |

`check_db.py` uses the Python standard library only. It confirms something is listening on the
port — it deliberately does not pick a database driver for you.

## Your project

Create it in the group folder, one level up. Python 3.12 and PostgreSQL 15 are the platform
standards (`../technical-environment.md`); everything else — framework, layout, test runner, how
you reach the database — is yours to choose and to justify.

Two things worth settling before your first line of code, because retrofitting them on Day 2
afternoon does not go well:

- **where secrets come from.** The compose password is a local development value and the
  encryption key belongs in an environment variable. `.env`, `*.key` and `secure-store/` are
  already git-ignored.
- **what a masked ID number looks like**, and where that formatting lives. The auditor will
  grep your logs.

Nothing is deployed. The workshop ends at working, tested code running on this laptop.
