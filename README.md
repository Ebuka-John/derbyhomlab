# Nearest Grit Bin

Resolves a UK postcode + address hint via Derbyshire’s Address Lookup API, then
returns the nearest grit bin (within 100 m by default) from GeoServer WFS.

Stack: **FastAPI** backend, **Next.js** frontend proxy UI, **Docker Compose**.

## Quick start (Docker)

1. Copy `.env.example` → `.env` and fill Address API credentials.
2. Run:

```bash
docker compose up --build
```

- UI: http://127.0.0.1:3000  
- API docs: http://127.0.0.1:8000/docs  
- Health: http://127.0.0.1:8000/api/v1/health  

## API

All endpoints live under `/api/v1`.

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/api/v1/addresses?postcode=&address=` | Address Lookup rows (easting/northing, …) |
| `GET` | `/api/v1/nearest-grit-bin?postcode=&address=` | Nearest grit bin within radius |
| `GET` | `/api/v1/nearest-grit-bins?postcode=&address=&limit=5` | Nearest N grit bins |
| `GET` | `/api/v1/grit-bins` | Full WFS grit-bin layer |
| `GET` | `/api/v1/health` | Liveness |

Example:

```bash
curl "http://127.0.0.1:8000/api/v1/nearest-grit-bin?postcode=AB12%203CD&address=Example%20Building"
```

### Errors

| HTTP | `error.code` |
|------|----------------|
| 400 | `missing_parameter`, `invalid_postcode` |
| 404 | `address_not_found`, `target_address_not_found`, `no_grit_bin_nearby` |
| 502 | `address_api_unreachable`, `geoserver_unreachable`, `unexpected_schema` |

## Local development (optional)

**Backend**

```bash
python -m venv .venv
# Windows: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt -r requirements-dev.txt
uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
pytest -q
```

**Frontend** (proxies to backend; never calls upstream APIs from the browser)

```bash
cd frontend
cp .env.example .env.local   # BACKEND_URL=http://127.0.0.1:8000
npm install
npm run dev
```

## Layout

```
src/           FastAPI app (routers → services → repositories)
frontend/      Next.js UI + /api/* proxy routes
tests/         Unit and API tests (upstream HTTP mocked)
Dockerfile     Backend image
frontend/Dockerfile
docker-compose.yml
```

## Config

See `.env.example`. Required: `ADDRESS_API_*`, `GEOSERVER_BASE_URL`, `GEOSERVER_LAYER`.
Optional: `NEAREST_SEARCH_RADIUS_METERS` (default `100`).
