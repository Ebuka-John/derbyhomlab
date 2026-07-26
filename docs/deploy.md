# How to deploy (container + API gateway)

1. **Container** — the included `Dockerfile` uses a slim Python 3.12 base, installs only
   runtime dependencies, runs as a **non-root** user, and defines a `HEALTHCHECK` hitting
   `/health`. Secrets are injected at runtime via `--env-file` / orchestrator secrets and
   are **never baked into image layers** (`.dockerignore` excludes `.env`).
2. **Local orchestration** — `docker compose up --build` starts **backend** (`:8000`)
   and **frontend** (`:3000`). The Next.js container proxies to
   `http://backend:8000` on the Compose network; `.env` is loaded by the API only.
3. **Cloud runtime** — deploy to Kubernetes (`Deployment` + `Service`, liveness/readiness
   probes on `/health`) or a managed runtime like Cloud Run / ECS Fargate with a warm
   minimum instance count.
4. **API gateway** — front the service with AWS API Gateway / Azure APIM / Kong for TLS
   termination, API-key or JWT auth, rate limiting, quotas, and request logging. The
   gateway owns public auth so the app stays focused on business logic.
5. **Config & secrets** — per-environment values from a parameter store / secret manager
   (`ADDRESS_API_*` and `GEOSERVER_*` differ across staging and prod).
6. **CI/CD** — run `pytest` on every push, build and scan the image, then promote through
   environments; roll out with health-gated deploys.
