# Docker lab (optional)

Package both services with Compose. Type each file from this branch into the lab.

## Concept

- **Backend image** — install Python deps, copy `src/`, run uvicorn as non-root.
- **Frontend image** — multi-stage build; `standalone` output; `BACKEND_URL=http://backend:8000`
  (Compose DNS name, not `localhost`).
- **`.dockerignore`** — keep secrets and junk out of the build context.

## Type these files (one at a time)

| # | Create in lab | Type from reference |
|--:|---------------|---------------------|
| 1 | `Dockerfile` | `Dockerfile` |
| 2 | `.dockerignore` | `.dockerignore` |
| 3 | `frontend/Dockerfile` | `frontend/Dockerfile` |
| 4 | `frontend/.dockerignore` | `frontend/.dockerignore` |
| 5 | `docker-compose.yml` | `docker-compose.yml` |

Ensure lab root `.env` has Address API credentials (Compose `env_file: .env`).

## Run

```powershell
docker compose up --build
```

- UI: http://127.0.0.1:3000  
- API docs: http://127.0.0.1:8000/docs  

## Checkpoint

Do **not** continue to the next lesson until this passes.


Same HILLBROW lookup works through Compose.

## Deeper reading

- `main`: `tutorial/docker/` (split lessons + run notes)
- This branch: root `README.md`, `docs/deploy.md`

---

| Previous | Next |
|:---------|-----:|
| ← [Frontend run](../frontend/04-run.md) | [Lab README](../README.md) → |
