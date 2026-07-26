# Docker lab

Type these files **in order**. Do this **after** the backend and frontend labs work
locally (you have already typed the app code).

Docker packages the same FastAPI + Next.js app into containers so anyone can run
the stack with one command — without installing Python or Node on their machine.

## What you will build

| Piece | File | Role |
|-------|------|------|
| Backend image | `Dockerfile` (project root) | Runs uvicorn on port 8000 |
| Backend ignore list | `.dockerignore` | Keeps secrets and junk out of the image |
| Frontend image | `frontend/Dockerfile` | Multi-stage Next.js production build |
| Frontend ignore list | `frontend/.dockerignore` | Skips `node_modules` / `.next` |
| Orchestration | `docker-compose.yml` | Starts both services and wires networking |

## TYPE THESE FILES IN ORDER

| Step | Lesson file | You create |
|-----:|-------------|------------|
| 1 | [01-backend-dockerfile.md](./01-backend-dockerfile.md) | `Dockerfile` |
| 2 | [02-backend-dockerignore.md](./02-backend-dockerignore.md) | `.dockerignore` |
| 3 | [03-frontend-dockerfile.md](./03-frontend-dockerfile.md) | `frontend/Dockerfile` |
| 4 | [04-frontend-dockerignore.md](./04-frontend-dockerignore.md) | `frontend/.dockerignore` |
| 5 | [05-compose.md](./05-compose.md) | `docker-compose.yml` |
| 6 | [06-run-and-test.md](./06-run-and-test.md) | Build and run the stack |

## Prerequisites

- Docker Desktop (or Docker Engine + Compose plugin) installed and running
- Root `.env` already filled with real Address API credentials (from the backend lab)
- Frontend has been built at least once locally so `package-lock.json` exists:

```powershell
Set-Location frontend
npm install
Set-Location ..
Test-Path frontend\package-lock.json
```

(`npm ci` in the frontend Dockerfile needs that lockfile.)

## Before you start

Stop any local servers so ports **8000** and **3000** are free (`Ctrl+C` in their
PowerShell windows).

Then open **[01-backend-dockerfile.md](./01-backend-dockerfile.md)** — create each
file with PowerShell `New-Item`, then type the contents yourself.

---

<!-- tutorial-nav -->

| Previous | Next |
|:---------|-----:|
| ← [Running fullstack](../05-running-fullstack.md) | [Backend Dockerfile](./01-backend-dockerfile.md) → |
