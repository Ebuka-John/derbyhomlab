# Backend 8 — Dependencies, routers, app

## Concept

- **Dependencies** — `Depends(...)` factories that pull `settings` + shared `httpx` client from `app.state` and build services.
- **Routers** — HTTP only: validate query params, call services, return DTOs.
  - `address.py` — `/health`, `/`
  - `gritbins.py` — `/nearest-grit-bin`, `/nearest-grit-bins`, `/grit-bins`
- **`app.py`** — lifespan (create/close HTTP client), register exception handler for `AppError`, include routers.
- **`main.py`** — optional `uvicorn` entrypoint.

## Type these files (one at a time)

| # | Create in lab | Type from reference |
|--:|---------------|---------------------|
| 1 | `src/api/dependencies/__init__.py` | `src/api/dependencies/__init__.py` |
| 2 | `src/api/routers/address.py` | `src/api/routers/address.py` |
| 3 | `src/api/routers/gritbins.py` | `src/api/routers/gritbins.py` |
| 4 | `src/app.py` | `src/app.py` |
| 5 | `src/main.py` | `src/main.py` |

## Checkpoint

```powershell
.\.venv\Scripts\Activate.ps1
python -c "from src.app import app; print(app.title)"
```

Should print `Nearest Grit Bin API`.

## Deeper reading

- `main`: `tutorial/backend/09-app.md`

---

| Previous | Next |
|:---------|-----:|
| ← [Services](./07-services.md) | [Run & test](./09-run.md) → |
