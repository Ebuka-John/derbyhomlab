# Frontend Step 2 — Environment

## What you will do

Create the frontend env files so the **server-side proxy** knows where FastAPI lives.

## File to create: `frontend/.env.example`

**Type this exactly:**

```text
# URL of the FastAPI backend (server-side only — used by the Next.js proxy route)
BACKEND_URL=http://127.0.0.1:8000
```

## File to create: `frontend/.env.local`

**What to do:**

1. Create a new file inside `frontend/` named exactly `.env.local`.
2. Type the same single line into it:

```text
BACKEND_URL=http://127.0.0.1:8000
```

Leave that value as-is for local development.

### Why `.env.local`

Next.js loads it automatically. Because the name is **not** `NEXT_PUBLIC_…`, the value stays on the server only (used by `route.ts`).

## Checkpoint

- `frontend/.env.local` exists
- Backend will be reachable at that URL when you start uvicorn

## Next

→ [03-types.md](./03-types.md)
