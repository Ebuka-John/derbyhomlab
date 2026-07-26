# Frontend Step 9 — Run and test the UI

## What you will do

Start Next.js (with FastAPI already running) and test the full UI flow.

## Prerequisites

1. Backend running: http://127.0.0.1:8000/health → ok
2. You are in `frontend/` with dependencies installed

## Commands

**Terminal A (backend, project root):**

```powershell
.\.venv\Scripts\Activate.ps1
uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
```

**Terminal B (frontend):**

```powershell
cd frontend
npm run dev
```

## Checkpoints

1. Open http://127.0.0.1:3000 — you see **Gritfinder** and the form
2. Defaults should be `HILLBROW` / `DE55 5PB`
3. Click **Find nearest grit bin**
4. You see a result card with title + distance, or a clear error message

Proxy-only check:

```powershell
curl "http://127.0.0.1:3000/api/nearest-grit-bin?postcode=DE55%205PB&address=HILLBROW"
```

---

<!-- tutorial-nav -->

| Previous | Next |
|:---------|-----:|
| ← [Page](./08-page.md) | [Running fullstack](../05-running-fullstack.md) → |
