# Interview pack (`lfdocs/`)

How to use these notes for the G11 Senior Developer (Integration) exercise.

## Documents

| File | Role |
|------|------|
| [interview.md](./interview.md) | **The brief** — requirements, investigation prompts, deliverables, follow-ups |
| [submission-notes.md](./submission-notes.md) | **Your short answers** — speak from this first (tools, issues, verify, deploy) |
| [copilotdocs.md](./copilotdocs.md) | **Depth** — architecture, WFS/`DWITHIN`, error model, follow-up designs |

Also useful:

- [interview-coverage.md](./interview-coverage.md) — checklist that every brief item is covered
- Repo root [README.md](../README.md) — how to run the solution (`docker compose`)

## How to prepare

1. Read **interview.md** — know what they mark you on (CORS, HILLBROW path, follow-ups).
2. Practise **submission-notes.md** out loud — approach, tried first, one issue, GB0199, deploy, nearest-5.
3. Keep **copilotdocs.md** open for probing questions (WFS vs WMS, spatial filters, batch/reuse).

## Panel flow

1. **Demo** the running app (see root README) — `HILLBROW` / `DE55 5PB` → Title **GB0199**.
2. **Talk** from submission-notes (investigation + deliverables).
3. **Go deeper** with copilotdocs if they ask about GeoServer queries or production design.

## Rule of thumb

- Brief = **interview.md**
- Default script = **submission-notes.md**
- Cheat sheet = **copilotdocs.md**
