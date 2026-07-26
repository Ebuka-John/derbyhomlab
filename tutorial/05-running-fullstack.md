# 5. Running the Fullstack Project

## What you will do

Run backend + frontend together and verify the end-to-end path. All commands are
PowerShell — run them yourself in two terminals.

## Start FastAPI

**Terminal A** — project root:

```powershell
.\.venv\Scripts\Activate.ps1
uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
```

- Docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

## Start Next.js

**Terminal B:**

```powershell
Set-Location frontend
npm run dev
```

- UI: http://127.0.0.1:3000

## Fullstack test plan

1. Open the UI
2. Submit `HILLBROW` + `DE55 5PB`
3. Confirm the browser network call is to `/api/nearest-grit-bin` (not `:8000`)
4. Confirm FastAPI logs show the upstream work
5. Compare in a third PowerShell window:

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/nearest-grit-bin?postcode=DE55%205PB&address=HILLBROW" |
  ConvertTo-Json -Depth 5

Invoke-RestMethod "http://127.0.0.1:3000/api/nearest-grit-bin?postcode=DE55%205PB&address=HILLBROW" |
  ConvertTo-Json -Depth 5
```

Both should return the same JSON shape.

## Optional: tests

**Terminal** at project root (venv active):

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
pytest -v
```

---

<!-- tutorial-nav -->

| Previous | Next |
|:---------|-----:|
| ← [Frontend run and test](./frontend/09-run-and-test.md) | [Docker lab](./docker/README.md) → |
