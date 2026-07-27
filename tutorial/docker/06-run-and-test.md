# Docker Step 6 — Build, run, and test

## What you will do

Build both images, start the stack, and verify the fullstack flow through Docker.

## Before you run

1. Docker Desktop (or the Docker daemon) is running
2. Ports **8000** and **3000** are free — in PowerShell, stop local servers
   (`Ctrl+C` in their terminals), or check:

```powershell
Get-NetTCPConnection -LocalPort 8000,3000 -ErrorAction SilentlyContinue |
  Select-Object LocalPort, State, OwningProcess
```

3. Root `.env` has real `ADDRESS_API_*` values
4. `frontend/package-lock.json` exists (`npm install` from the frontend scaffold step)

## Build and start

From the **project root**:

```powershell
docker compose up --build
```

First run downloads base images and can take several minutes. Leave this terminal
open — logs stream here.

To run in the background instead:

```powershell
docker compose up --build -d
```

## Checkpoints

| Check | How |
|-------|-----|
| Backend health | Open http://127.0.0.1:8000/health → `{"status":"ok"}` |
| API docs | Open http://127.0.0.1:8000/docs |
| Frontend UI | Open http://127.0.0.1:3000 |
| Full lookup | Submit a real Derbyshire postcode + address hint in the UI |
| Proxy path | Browser Network tab shows `/api/nearest-grit-bin` (not a call to `:8000`) |

Direct API check:

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/nearest-grit-bin?postcode=AB12%203CD&address=Example%20Building" |
  ConvertTo-Json -Depth 5
```

Through the frontend proxy:

```powershell
Invoke-RestMethod "http://127.0.0.1:3000/api/nearest-grit-bin?postcode=AB12%203CD&address=Example%20Building" |
  ConvertTo-Json -Depth 5
```

Both should return the same JSON shape.

## Useful commands

```powershell
# Status
docker compose ps

# Follow logs
docker compose logs -f

# Stop and remove containers
docker compose down

# Rebuild after Dockerfile or code changes
docker compose up --build
```

## Common Docker mistakes

| Problem | Fix |
|---------|-----|
| `backend_unreachable` from the UI | `BACKEND_URL` must be `http://backend:8000` in Compose — not `127.0.0.1` |
| Port already allocated | Stop local servers, or `docker compose down` then retry |
| Frontend build fails on `npm ci` | Ensure `frontend/package-lock.json` exists (`npm install` once) |
| Backend fails on missing env | Root `.env` must exist; Compose does not bake it into the image |
| Stale code after edits | Rebuild with `docker compose up --build` |

## Backend only (optional)

```powershell
docker compose up --build backend
```

Or without Compose:

```powershell
docker build -t nearest-grit-bin-backend .
docker run --rm -p 8000:8000 --env-file .env nearest-grit-bin-backend
```

---

<!-- tutorial-nav -->

| Previous | Next |
|:---------|-----:|
| ← [Compose](./05-compose.md) | [Common mistakes](../06-common-mistakes.md) → |
