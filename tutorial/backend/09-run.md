# Backend 9 — Run & smoke-test

## Concept

`uvicorn` loads the ASGI app `src.app:app`. Swagger UI at `/docs` is the fastest
manual check. Live nearest-bin calls need a valid `.env`.

## Run (lab Terminal)

```powershell
.\.venv\Scripts\Activate.ps1
uvicorn src.app:app --reload --host 127.0.0.1 --port 8000
```

**PyCharm run configuration (optional):**

1. `Run → Edit Configurations… → + → Python`
2. Module name: `uvicorn`
3. Parameters: `src.app:app --reload --host 127.0.0.1 --port 8000`
4. Working directory: lab project root
5. Prefer the project `.venv` interpreter

## Smoke checks

Browser: http://127.0.0.1:8000/docs  

Or:

```powershell
curl http://127.0.0.1:8000/health
```

Live (replace with your fixture when ready):

```powershell
curl "http://127.0.0.1:8000/nearest-grit-bin?postcode=DE55%205PB&address=HILLBROW"
```

Expect nearest title **GB0199** and distance around **49** metres when credentials and upstream are healthy.

## Optional: unit tests

If you also want tests, type from reference `tests/` (same one-file-at-a-time habit), then:

```powershell
pytest -q
```

(Tests mock upstream HTTP — see `tests/conftest.py` on this branch.)

## Checkpoint

`/health` returns `{"status":"ok"}` and `/docs` loads.

Backend done → [Frontend lab](../frontend/README.md)

## Deeper reading

- `main`: `tutorial/backend/10-run-and-test.md`, `tutorial/05-running-fullstack.md`
- This branch: root `README.md`

---

| Previous | Next |
|:---------|-----:|
| ← [API & app](./08-api-app.md) | [Frontend](../frontend/README.md) → |
