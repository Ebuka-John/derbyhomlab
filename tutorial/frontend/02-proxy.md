# Frontend 2 — Types & server proxy

## Concept

- **`lib/types.ts`** — TypeScript shapes matching FastAPI success/error JSON.
- **`lib/backend.ts`** — reads `BACKEND_URL` (server-only).
- **Route Handlers** under `app/api/*/route.ts` — validate query params, `fetch`
  FastAPI, return the same status/body to the browser.

The browser never sees Address API tokens or GeoServer URLs.

## Type these files (one at a time)

| # | Create in lab | Type from reference |
|--:|---------------|---------------------|
| 1 | `frontend/lib/types.ts` | `frontend/lib/types.ts` |
| 2 | `frontend/lib/backend.ts` | `frontend/lib/backend.ts` |
| 3 | `frontend/app/api/nearest-grit-bin/route.ts` | `frontend/app/api/nearest-grit-bin/route.ts` |
| 4 | `frontend/app/api/nearest-grit-bins/route.ts` | `frontend/app/api/nearest-grit-bins/route.ts` |
| 5 | `frontend/app/api/grit-bins/route.ts` | `frontend/app/api/grit-bins/route.ts` |

## Checkpoint

With backend running on :8000 and (optionally) frontend later on :3000, the proxy
files should exist and import without red squiggles in PyCharm once
`node_modules` is installed.

Quick syntax check:

```powershell
cd frontend
npx tsc --noEmit
cd ..
```

(May warn until UI files exist — that’s OK if errors are only missing `page.tsx`.)

## Deeper reading

- `main`: `tutorial/frontend/03-types.md`, `tutorial/frontend/04-api-route.md`

---

| Previous | Next |
|:---------|-----:|
| ← [Scaffold](./01-scaffold.md) | [UI](./03-ui.md) → |
