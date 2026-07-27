# Frontend Step 2 — Environment

## What you will do

Create the frontend env files in your editor so the **server-side proxy** knows
where FastAPI lives, then type the values yourself.

## File to create: `frontend/.env.example`

### Create this file in the editor

Create `frontend/.env.example` in your editor (from the project root), then type the contents below yourself.

```text
# URL of the FastAPI backend (server-side only — used by the Next.js proxy route)
BACKEND_URL=http://127.0.0.1:8000
```

## File to create: `frontend/.env.local`

### Create this file in the editor

Create `frontend/.env.local` in your editor (from the project root) by copying `frontend/.env.example` to `frontend/.env.local` (or duplicate it in the editor), then edit as needed.

```text
BACKEND_URL=http://127.0.0.1:8000
```

Leave that value as-is for local development.

Confirm:

```powershell
Get-ChildItem -Force frontend\.env.example, frontend\.env.local
```

### Why `.env.local`

Next.js loads it automatically. Because the name is **not** `NEXT_PUBLIC_…`, the value stays on the server only (used by `route.ts`).

## Checkpoint

```powershell
Test-Path frontend\.env.local
Get-Content frontend\.env.local
```

- `frontend/.env.local` exists
- Backend will be reachable at that URL when you start uvicorn

---

<!-- tutorial-nav -->

| Previous | Next |
|:---------|-----:|
| ← [Scaffold](./01-scaffold.md) | [Types](./03-types.md) → |
