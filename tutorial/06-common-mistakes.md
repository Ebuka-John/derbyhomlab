# 6. Common Mistakes

## Missing or misnamed `.env`

**Symptom:** Pydantic ValidationError on startup naming a missing variable.

**Fix:** From the project root in PowerShell:

```powershell
Copy-Item .env.example .env
# Open .env and fill ADDRESS_API_* values
Get-ChildItem -Force .env
```

Name it exactly `.env`, not `.env.txt`.

---

## CORS errors in the browser

**Symptom:** Browser console says request blocked by CORS.

**Fix:** Do **not** fetch `http://127.0.0.1:8000/...` from client code. Always call `/api/nearest-grit-bin` so Next.js proxies server-side.

---

## Wrong backend URL / backend unreachable

**Symptom:** `502` with `backend_unreachable`.

**Fix:**

```powershell
# Terminal A — project root
.\.venv\Scripts\Activate.ps1
uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
```

- Set `frontend/.env.local` → `BACKEND_URL=http://127.0.0.1:8000`
- In Docker Compose use `http://backend:8000` (the Compose **service name**), not `127.0.0.1`

Full Docker walkthrough: [docker/README.md](./docker/README.md).

---

## Incorrect fetch paths

**Symptom:** Next.js 404, or FastAPI never receives the call.

**Fix:**

| Layer | Correct path |
|-------|----------------|
| Browser → Next.js | `/api/nearest-grit-bin` |
| Next.js → FastAPI | `/nearest-grit-bin` |

Folder for the route must be `frontend/app/api/nearest-grit-bin/route.ts`.

---

## Postcode spaces

Use `%20` in URLs (`DE55%205PB`). The backend uses `quote(..., safe="")` for this.

---

## Absurd distances / no bin nearby

Coordinates must be EPSG:27700 before distance maths. Use `ensure_bng` — do not mix lat/lon degrees with BNG metres.

Quick reminder:

- **CRS** = what the numbers mean (EPSG:27700 metres vs EPSG:4326 degrees).
- **DWITHIN** = GeoServer filters “within N metres”.
- **Euclidean** = your app’s `sqrt(Δe² + Δn²)` on BNG points.

See [10-spatial-querying.md](./10-spatial-querying.md#beginner-faq--crs-bng-and-this-codebase).

---

<!-- tutorial-nav -->

| Previous | Next |
|:---------|-----:|
| ← [Docker run and test](./docker/06-run-and-test.md) | [Spatial querying](./10-spatial-querying.md) → |
