# Frontend lab (Next.js) — type-along

Still use **two windows**: reference = this branch’s `frontend/`; lab = your new
project’s `frontend/` folder.

**Rule:** after each lesson, run the **Checkpoint** before opening the next
file list. Do not scaffold + proxy + UI in one go and only run `npm` at the end.

PyCharm can edit TypeScript fine; for Node tooling use the **lab Terminal**.
(WebStorm is optional — not required.)

## Order

| Step | Lesson | You create |
|-----:|--------|------------|
| 1 | [01-scaffold.md](./01-scaffold.md) | `frontend/` config + folders |
| 2 | [02-proxy.md](./02-proxy.md) | types, backend helper, `/api/*` routes |
| 3 | [03-ui.md](./03-ui.md) | SearchForm, layout, page, CSS |
| 4 | [04-run.md](./04-run.md) | `npm run dev` + full-stack check |

## Why a proxy

The exercise forbids browser → Derbyshire calls. The UI fetches `/api/nearest-grit-bins`
on the same origin; the Route Handler forwards to FastAPI using `BACKEND_URL`.

## Deeper reading (`main`)

- `tutorial/frontend/` (full numbered lessons with embedded code on `main`)
- Code you type: this branch’s `frontend/`

Start → [01-scaffold.md](./01-scaffold.md)

---

| Previous | Next |
|:---------|-----:|
| ← [Backend run](../backend/09-run.md) | [Scaffold](./01-scaffold.md) → |
