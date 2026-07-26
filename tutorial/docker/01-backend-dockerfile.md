# Docker Step 1 — Backend Dockerfile

## What you will do

Create the backend image recipe at the project root with PowerShell (`New-Item`),
then type the Dockerfile contents yourself. This tells Docker how to package the
FastAPI app.

## File to create: `Dockerfile`

**Path:** `Dockerfile` (project root — same folder as `requirements.txt` and `src/`)

### Create it in PowerShell (project root)

```powershell
New-Item -ItemType File -Force -Path Dockerfile | Out-Null
```

Open `Dockerfile` in your editor and type the contents below yourself.

### Purpose

Builds a small Python image that installs dependencies, copies only `src/`, runs
as a non-root user, and starts uvicorn on port 8000.

### Type this exactly

```dockerfile
# syntax=docker/dockerfile:1

FROM python:3.12-slim AS base

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Non-root user for runtime
RUN groupadd --system app && useradd --system --gid app --home /app --shell /usr/sbin/nologin app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src

USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')"

# Secrets come from --env-file / Compose / orchestrator — never bake .env into the image
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### How the code works

| Line / block | Meaning |
|--------------|---------|
| `FROM python:3.12-slim` | Official slim Python base (smaller than the full image) |
| `WORKDIR /app` | All later paths are relative to `/app` inside the container |
| `ENV …` | Avoid `.pyc` clutter, flush logs immediately, skip pip cache |
| `groupadd` / `useradd` | Create a non-root user named `app` (safer than running as root) |
| `COPY requirements.txt` then `pip install` | Install deps **before** copying source so Docker can cache this layer when only code changes |
| `COPY src ./src` | Copy only the application package — not tests, docs, or secrets |
| `USER app` | Drop privileges before the process starts |
| `EXPOSE 8000` | Documents the port (Compose still maps it) |
| `HEALTHCHECK` | Hits `/health` so Compose knows when the API is ready |
| `CMD […]` | Default process: uvicorn, listening on all interfaces (`0.0.0.0`) |

**Important:** `.env` is **not** copied into the image. Secrets are injected at
**runtime** by Compose (`env_file: .env`).

## Checkpoint

Confirm the file exists at the project root and is named exactly `Dockerfile`
(no extension).

Optional smoke build (can wait until the end if you prefer):

```powershell
docker build -t nearest-grit-bin-backend:latest .
```

---

<!-- tutorial-nav -->

| Previous | Next |
|:---------|-----:|
| ← [Docker lab](./README.md) | [Backend dockerignore](./02-backend-dockerignore.md) → |
