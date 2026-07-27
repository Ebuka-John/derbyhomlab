# 5. Running the Fullstack Project

## What you will do

Run backend + frontend together and verify the end-to-end path.

**Preferred way:** Docker Compose (same stack you ship and demo).  
**Optional:** local uvicorn + `npm run dev` for fast edit–reload while typing code
(hours 2–6). If you are only validating the finished app, skip straight to Docker.

All commands below are PowerShell — run them yourself.

---

## Preferred: Docker Compose

From the **project root** (Docker Desktop running, root `.env` filled in):

```powershell
docker compose up --build
```

| Check | URL / action |
|-------|----------------|
| Backend health | http://127.0.0.1:8000/health |
| API docs | http://127.0.0.1:8000/docs |
| UI | http://127.0.0.1:3000 |

Full Docker walkthrough (Dockerfiles, Compose, troubleshooting):
[docker/06-run-and-test.md](./docker/06-run-and-test.md).

### Fullstack test plan (Docker)

1. Open the UI at http://127.0.0.1:3000
2. Submit `HILLBROW` + `DE55 5PB`
3. Confirm the browser network call is to `/api/nearest-grit-bin` (not `:8000`)
4. Confirm Compose logs show upstream Address / GeoServer work
5. Compare in another PowerShell window:

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/nearest-grit-bin?postcode=DE55%205PB&address=HILLBROW" |
  ConvertTo-Json -Depth 5

Invoke-RestMethod "http://127.0.0.1:3000/api/nearest-grit-bin?postcode=DE55%205PB&address=HILLBROW" |
  ConvertTo-Json -Depth 5
```

Both should return the same JSON shape.

After code changes, rebuild so containers pick them up:

```powershell
docker compose up --build
```

---

## Optional: local servers (type-along / debugging)

Use this only when you are mid-tutorial and want `--reload` without rebuilding
images. You still need a venv, Node, and `.env`.

**Terminal A** — project root:

```powershell
.\.venv\Scripts\Activate.ps1
uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
```

**Terminal B:**

```powershell
Set-Location frontend
npm run dev
```

- Docs: http://127.0.0.1:8000/docs  
- UI: http://127.0.0.1:3000  

Stop local servers before `docker compose up` if ports 8000/3000 are already taken.

### Optional: tests (local venv)

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
