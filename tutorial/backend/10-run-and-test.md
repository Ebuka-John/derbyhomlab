# Backend Step 10 — Run and test the API

## What you will do

Start FastAPI and verify the endpoint works — every command in PowerShell, run by you.

## Commands

From the **project root**, in a new PowerShell window:

```powershell
.\.venv\Scripts\Activate.ps1
# If blocked:
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
# .\.venv\Scripts\Activate.ps1

uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
```

Leave that window running.

## Checkpoints

1. Open http://127.0.0.1:8000/health → `{"status":"ok"}`
2. Open http://127.0.0.1:8000/docs → Swagger UI appears
3. In a **second** PowerShell window, try the interview example:

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/nearest-grit-bin?postcode=DE55%205PB&address=HILLBROW" |
  ConvertTo-Json -Depth 5
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
- Import errors → confirm you are in the project root and venv is active (`.\.venv\Scripts\Activate.ps1`)
- Upstream 502 → check Address API credentials / network

---

<!-- tutorial-nav -->

| Previous | Next |
|:---------|-----:|
| ← [FastAPI app](./09-app.md) | [Frontend lab](../frontend/README.md) → |
