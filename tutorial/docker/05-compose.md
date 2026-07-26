# Docker Step 5 — docker-compose.yml

## What you will do

Create the Compose file that builds both images, starts them together, shares a
private network, and injects configuration.

## File to create: `docker-compose.yml`

**Path:** `docker-compose.yml` (project root)

### Purpose

One file to run the full stack. Compose:

1. Builds the backend and frontend images
2. Maps ports `8000` and `3000` to your machine
3. Loads `.env` into the backend only
4. Sets `BACKEND_URL=http://backend:8000` for the frontend proxy
5. Waits until the backend healthcheck passes before starting the frontend

### Type this exactly

```yaml
services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile
    image: nearest-grit-bin-backend:latest
    ports:
      - "8000:8000"
    env_file:
      - .env
    restart: unless-stopped
    healthcheck:
      test:
        [
          "CMD",
          "python",
          "-c",
          "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')",
        ]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    image: nearest-grit-bin-frontend:latest
    ports:
      - "3000:3000"
    environment:
      # Server-side proxy target (Docker Compose DNS name for the API service)
      BACKEND_URL: http://backend:8000
    depends_on:
      backend:
        condition: service_healthy
    restart: unless-stopped
    healthcheck:
      test:
        [
          "CMD",
          "wget",
          "-qO-",
          "http://127.0.0.1:3000/",
        ]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 20s
```

### How the code works

#### Concepts in this file

| Concept | Plain meaning |
|---------|---------------|
| **Image** | A packaged snapshot of your app + runtime (built from a Dockerfile). |
| **Container** | A running instance of an image (like a lightweight process with its own filesystem). |
| **Compose service** | A named container role (`backend`, `frontend`) with build/ports/env rules. |
| **Service DNS name** | Inside Compose, `backend` resolves to the API container — use that in `BACKEND_URL`, not `127.0.0.1`. |
| **Healthcheck** | Periodic probe; other services can wait until it passes. |
| **`env_file` vs `environment`** | Backend secrets from `.env`; frontend gets `BACKEND_URL` from Compose itself. |

**Backend service**
- `build.context: .` — uses the root Dockerfile
- `ports: "8000:8000"` — host:container port mapping
- `env_file: .env` — injects Address API + GeoServer secrets at runtime
- `healthcheck` — same idea as the Dockerfile HEALTHCHECK

**Frontend service**
- `build.context: ./frontend` — uses the frontend Dockerfile
- `BACKEND_URL: http://backend:8000` — **critical**
  - Inside Compose, services reach each other by **service name**, not `127.0.0.1`
  - `backend` is the DNS name Compose gives the API container
  - The Next.js proxy (server-side) uses this URL
- `depends_on` + `condition: service_healthy` — frontend starts only after `/health` is OK

```
Browser → http://127.0.0.1:3000
              │
              ▼
         frontend container
              │  BACKEND_URL=http://backend:8000
              ▼
         backend container  → Address API / GeoServer
```

## Checkpoint

Confirm `docker-compose.yml` is at the project root next to `.env` and `Dockerfile`.

---

<!-- tutorial-nav -->

| Previous | Next |
|:---------|-----:|
| ← [Frontend dockerignore](./04-frontend-dockerignore.md) | [Docker run and test](./06-run-and-test.md) → |
