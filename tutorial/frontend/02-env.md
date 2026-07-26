# Frontend Step 2 — Environment

## What you will do

Create the frontend env files with PowerShell so the **server-side proxy** knows
where FastAPI lives, then type the values yourself.

## File to create: `frontend/.env.example`

### Create it in PowerShell (project root)

```powershell
New-Item -ItemType File -Force -Path frontend\.env.example | Out-Null
```

Open `frontend/.env.example` and **type this exactly:**

```text
# URL of the FastAPI backend (server-side only — used by the Next.js proxy route)
BACKEND_URL=http://127.0.0.1:8000
```

## File to create: `frontend/.env.local`

### Create it in PowerShell (project root)

```powershell
Copy-Item frontend\.env.example frontend\.env.local
```

Open `frontend/.env.local` and confirm it contains:

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
