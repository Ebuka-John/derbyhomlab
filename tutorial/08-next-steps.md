# 8. Next Steps

## Suggested improvements

- Return the nearest **5** grit bins
- Cache postcode lookups
- Retries / backoff for upstream HTTP
- Request IDs in logs
- Map view in the UI

## Containerise

If you have not done the Docker lab yet, type the files here:

→ [docker/README.md](./docker/README.md)

You will create `Dockerfile`, `.dockerignore`, `frontend/Dockerfile`,
`frontend/.dockerignore`, and `docker-compose.yml`, then run:

```powershell
docker compose up --build
```

More deployment context (API gateway, cloud runtimes, CI/CD) lives in
[`docs/deploy.md`](../docs/deploy.md).

## Add authentication

- Protect FastAPI with an API key or JWT (`Depends`)
- Store the expected secret in `config.py`
- Attach the token in the Next.js proxy (`route.ts`) so the browser never sees it

## Scale the architecture

- Run multiple backend replicas behind a load balancer (stateless)
- Add Redis for caching
- Split `app.py` into FastAPI routers when the API grows
- Add metrics and health monitoring (see `docs/test-and-monitor.md`)

---

## You finished the lab

You typed a real FastAPI + Next.js system (and optionally its Docker packaging)
and understand the request path from click → proxy → Address API / GeoServer →
JSON → UI.

Keep experimenting — that is how it sticks.

---

<!-- tutorial-nav -->

| Previous | Next |
|:---------|-----:|
| ← [Derbyshire exercise](./07-derbyshire-exercise.md) | *End of lab* → |
