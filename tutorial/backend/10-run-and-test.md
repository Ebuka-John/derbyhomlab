# Backend Step 10 — Run and test the API

## What you will do

Start FastAPI and verify the endpoint works.

## Commands

From the **project root**, with `.venv` activated and `.env` present:

```powershell
uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
```

## Checkpoints

1. Open http://127.0.0.1:8000/health → `{"status":"ok"}`
2. Open http://127.0.0.1:8000/docs → Swagger UI appears
3. Try the interview example:

```powershell
curl "http://127.0.0.1:8000/nearest-grit-bin?postcode=DE55%205PB&address=HILLBROW"
```

Success looks like:

```json
{
  "address": "HILLBROW",
  "postcode": "DE55 5PB",
  "nearest_grit_bin_title": "GB0199",
  "distance_meters": 48.99
}
```

(Exact title/distance depend on live data.)

## If something fails

- Missing env → fix `.env` (see [02-env.md](./02-env.md))
- Import errors → confirm you are in the project root and venv is active
- Upstream 502 → check Address API credentials / network

## Next

Backend done. Go to the frontend lab:

→ [../frontend/README.md](../frontend/README.md)
