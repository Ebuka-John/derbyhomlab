# Frontend Step 9 — Run and test the UI

## What you will do

Start Next.js (with FastAPI already running) and test the full UI flow. You run
every command yourself in PowerShell.

## Prerequisites

1. Backend running: http://127.0.0.1:8000/health → ok
2. Dependencies installed (`frontend\node_modules` exists from step 1)

## Commands

**Terminal A (backend, project root):**

```powershell
.\.venv\Scripts\Activate.ps1
uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
```

**Terminal B (frontend):**

```powershell
Set-Location frontend
npm run dev
```

## Checkpoints

1. Open http://127.0.0.1:3000 — you see **Gritfinder** and the form
2. Placeholders should be `Example Building` / `AB12 3CD` (fields start empty)
3. Enter a real Derbyshire postcode + address hint, then click **Find nearest grit bin**
4. You see a result card with title + distance, or a clear error message

Proxy-only check (third PowerShell window, or stop nothing — just run):

```powershell
Invoke-RestMethod "http://127.0.0.1:3000/api/nearest-grit-bin?postcode=AB12%203CD&address=Example%20Building" |
  ConvertTo-Json -Depth 5
```

---

<!-- tutorial-nav -->

| Previous | Next |
|:---------|-----:|
| ← [Page](./08-page.md) | [Running fullstack](../05-running-fullstack.md) → |
