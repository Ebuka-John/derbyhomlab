# Interview pack (`lfdocs/`)

How to use these notes for the G11 Senior Developer (Integration) exercise.

## Documents

| File | Role |
|------|------|
| [interview.md](./interview.md) | **The brief** — requirements, investigation prompts, deliverables, follow-ups |
| [submission-notes.md](./submission-notes.md) | **Your short answers** — speak from this first (tools, issues, verify, deploy) |
| [G11_Interview_Rivision_Notes.md](./G11_Interview_Rivision_Notes.md) | **One-page revision sheet** — quick facts, Q&A, talking points |
| [copilotdocs.md](./copilotdocs.md) | **Depth** — architecture, design patterns, WFS/`DWITHIN`, `/DCC/ows`, follow-ups |

Also useful:

- Repo root [README.md](../README.md) — how to run the solution (`docker compose`)
- [tutorial/](../tutorial/) — PyCharm type-along (optional rebuild practice)

## How to prepare

1. Read **interview.md** — know what they mark you on (CORS, HILLBROW path, follow-ups).
2. Practise **submission-notes.md** out loud — approach, tried first, one issue, GB0199, deploy, nearest-5.
3. Skim **G11_Interview_Rivision_Notes.md** the morning of — especially `/DCC/ows` and **Design Patterns**.
4. Keep **copilotdocs.md** open for probing questions (design patterns, WFS vs WMS, spatial filters, batch/reuse).

## Panel flow

1. **Demo** the running app (see root README) — `HILLBROW` / `DE55 5PB` → Title **GB0199**.
2. **Talk** from submission-notes (investigation + deliverables).
3. **Go deeper** with revision notes / copilotdocs if they ask about GeoServer URLs or production design.

## Rule of thumb

- Brief = **interview.md**
- Default script = **submission-notes.md**
- Pocket card = **G11_Interview_Rivision_Notes.md**
- Cheat sheet = **copilotdocs.md**

## Panel soundbite: design patterns

> Layered FastAPI: routers → services → repositories; DTOs at the edge;
> Next.js server proxy for CORS. Integrations stay mockable and secrets stay server-side.

Full table: [copilotdocs.md](./copilotdocs.md) § Design patterns · pocket card: [G11_Interview_Rivision_Notes.md](./G11_Interview_Rivision_Notes.md)

## Panel soundbite: `/DCC/ows`

The assessment never names `/DCC/ows`. Env gives the GeoServer **root**;
`DCC:Gritbins` implies workspace **DCC**; GeoServer’s usual workspace OGC path is
`/{workspace}/ows`. Confirmed with live GetCapabilities / GetFeature on
https://wms.derbyshire.gov.uk/geoserver. Full write-up:
[submission-notes.md](./submission-notes.md) § “How `/DCC/ows` was found”.
