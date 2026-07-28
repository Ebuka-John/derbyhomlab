# Frontend 1 — Scaffold

## Concept

Next.js App Router: `app/` holds pages and Route Handlers. Config files
(`package.json`, `tsconfig.json`, `next.config.ts`) define the toolchain.
`output: "standalone"` later helps the Docker image.

## Create folders (lab)

Under the **lab project root**:

```text
frontend/
  app/
    api/
      nearest-grit-bin/
      nearest-grit-bins/
      grit-bins/
  components/
  lib/
  public/
```

In PyCharm: right-click → `New → Directory`. Folder names with hyphens matter —
they become URL segments.

## Type these files (one at a time)

| # | Create in lab | Type from reference |
|--:|---------------|---------------------|
| 1 | `frontend/package.json` | `frontend/package.json` |
| 2 | `frontend/package-lock.json` | `frontend/package-lock.json` *(or run `npm install` after package.json only)* |
| 3 | `frontend/tsconfig.json` | `frontend/tsconfig.json` |
| 4 | `frontend/next.config.ts` | `frontend/next.config.ts` |
| 5 | `frontend/next-env.d.ts` | `frontend/next-env.d.ts` |
| 6 | `frontend/css.d.ts` | `frontend/css.d.ts` |
| 7 | `frontend/.gitignore` | `frontend/.gitignore` |
| 8 | `frontend/.env.example` | `frontend/.env.example` |
| 9 | `frontend/.env.local` | Copy example → set `BACKEND_URL=http://127.0.0.1:8000` |
| 10 | `frontend/public/.gitkeep` | `frontend/public/.gitkeep` |

> Prefer typing `package.json` then `npm install` so the lockfile is generated,
> unless you want an exact lockfile match — then type `package-lock.json` too.

## Install

```powershell
cd frontend
npm install
cd ..
```

## Checkpoint

Do **not** continue to the next lesson until this passes.


```powershell
Test-Path frontend\node_modules\next
```

Should be `True`.

## Deeper reading

- `main`: `tutorial/frontend/01-scaffold.md`, `tutorial/frontend/02-env.md`

---

| Previous | Next |
|:---------|-----:|
| ← [Frontend README](./README.md) | [Proxy](./02-proxy.md) → |
