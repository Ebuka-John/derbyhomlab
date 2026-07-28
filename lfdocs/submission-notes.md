# Submission notes

Short answers for the deliverable / investigation prompts that sit alongside [`copilotdocs.md`](./copilotdocs.md) and the running app. Keep this file for the panel pack.

Brief: [`interview.md`](./interview.md). Coverage checklist: [`interview-coverage.md`](./interview-coverage.md).

---

## Approach (one paragraph)

Resolve any UK postcode + address hint via Derbyshire’s Address Lookup API, normalise to EPSG:27700, query GeoServer WFS with `DWITHIN` on `SP_GEOMETRY` (100 m default), then rank by planar Euclidean distance in-process. FastAPI owns integrations; Next.js proxies browser calls so upstream APIs and tokens never leave the server (CORS). Interview pair `HILLBROW` / `DE55 5PB` returns grit bin **GB0199** at ~49 m.

Broken into parts: **routers** (HTTP) → **services** (rules) → **repositories** (Address API / GeoServer) → **geospatial helpers** (CRS + distance). Typed errors map to stable `{ error: { code, message } }` JSON (400 / 404 / 502).

---

## What I tried first

- Read the brief: CORS constraint, Address Lookup for `DE55 5PB`, find `HILLBROW`, nearest grit bin ~100 m, return Title.
- Called the Address API with the supplied headers; confirmed postcode is the path key and inspected the JSON shape.
- Identified the `HILLBROW` row (`BuildingName` + `SpatialFeature` coords — not a single `Title` field).
- Probed Derbyshire GeoServer; confirmed **WFS** GetFeature on `DCC:Gritbins` (hostname says `wms.` but WMS is images only).
- Tried `DWITHIN` on `SP_GEOMETRY`, then ranked by Euclidean metres; verified Title **GB0199** ~49 m from HILLBROW.

---

## Tools used

- **PyCharm** — primary IDE for Python/FastAPI, debugging, and running tests
- **Copilot** — research aid (WFS vs WMS, CQL/`DWITHIN`, CRS concepts, pseudocode structuring); all integration decisions verified against live APIs and docs
- PowerShell / curl / `httpx` — probe Address API and WFS responses
- FastAPI `/docs` (Swagger) — exercise endpoints interactively
- pytest + respx — unit/API tests with mocked upstream HTTP
- Docker Compose — run backend + frontend together
- Browser UI (Gritfinder) — end-to-end smoke checks
- GeoServer WFS GetFeature / CQL in the browser or HTTP client — confirm layer, geometry field, filters

---

## Documentation and resources used

### From the exercise

- Technical exercise brief (problem, CORS, ~100 m, HILLBROW / DE55 5PB)
- Credentials / header file (`ADDRESS_API_BASE_URL`, `x-alias`, `x-auth-token`)
- Live Address API sample responses (field discovery — no public developer portal)

### Live systems probed

- Derbyshire GeoServer (public): https://wms.derbyshire.gov.uk/geoserver  
  (hostname says `wms.` — this solution uses **WFS** GetFeature, not WMS images)
- WFS entry: `{GEOSERVER_BASE_URL}/DCC/ows` — layer `DCC:Gritbins`, geometry `SP_GEOMETRY`

### Spatial / GIS references

- OGC WFS: https://www.ogc.org/standard/wfs/
- GeoServer docs: https://docs.geoserver.org/
- WFS GetFeature reference: https://docs.geoserver.org/latest/en/user/services/wfs/reference.html
- CQL / ECQL (incl. `DWITHIN`):  
  https://docs.geoserver.org/latest/en/user/tutorials/cql/cql_tutorial.html  
  https://docs.geoserver.org/latest/en/user/filter/ecql_reference.html
- GeoJSON: https://geojson.org/ · RFC 7946: https://datatracker.ietf.org/doc/html/rfc7946
- EPSG:27700 (BNG): https://epsg.io/27700 · EPSG:4326: https://epsg.io/4326
- EPSG registry: https://epsg.io/
- Ordnance Survey National Grid guide: https://www.ordnancesurvey.co.uk/documents/resources/guide-to-nationalgrid.pdf
- pyproj: https://pyproj4.github.io/pyproj/stable/ · PROJ: https://proj.org/

### UK address / postcode background

- Royal Mail find a postcode: https://www.royalmail.com/find-a-postcode
- UK postcodes (overview): https://en.wikipedia.org/wiki/Postcodes_in_the_United_Kingdom

### Framework / stack docs

| Area | Link |
|------|------|
| FastAPI | https://fastapi.tiangolo.com/ |
| Uvicorn | https://www.uvicorn.org/ |
| httpx | https://www.python-httpx.org/ |
| Pydantic / settings | https://docs.pydantic.dev/ |
| pytest | https://docs.pytest.org/ |
| respx | https://lundberg.github.io/respx/ |
| Next.js App Router | https://nextjs.org/docs/app |
| Next.js Route Handlers | https://nextjs.org/docs/app/building-your-application/routing/route-handlers |
| Docker | https://docs.docker.com/reference/dockerfile/ |

### Own write-ups

- [`copilotdocs.md`](./copilotdocs.md) — architecture, spatial query reasoning, follow-ups
- This file — tools, issues, deploy, test/monitor

---

## Assumptions

- Address API is keyed by postcode and returns one or more address records.
- `HILLBROW` appears in the returned set for `DE55 5PB` (BuildingName / composed text).
- Coordinates are (or can be converted to) EPSG:27700 easting/northing.
- Grit-bin layer is `DCC:Gritbins`; geometry field is `SP_GEOMETRY` (not `the_geom`).
- Grit bins expose a usable `Title` attribute.
- “Approximately 100 metres” is enforced as a configurable radius (default 100).

---

## Approaches rejected

- **Browser-direct calls to Address API / GeoServer** — brief forbids this (CORS); credentials would also leak.
- **WMS** — returns map images, not feature geometry/attributes needed for Title + distance.
- **Download the entire grit-bin layer as the primary path** — poor performance and scalability; prefer `DWITHIN`. For this exercise a full-layer fallback exists only to survive/validate DWITHIN gaps — not as a production strategy (see issue 5 and “improve with more time”).
- **Hard-coding HILLBROW / DE55 5PB in business logic** — interview pair is a fixture; the service accepts any postcode + address hint.
- **Matching only on a `Title` field** — live Address API uses `BuildingName` and related parts.

---

## Error handling (summary)

| HTTP | `error.code` | When |
|------|----------------|------|
| 400 | `missing_parameter`, `invalid_postcode` | Missing input or bad postcode |
| 404 | `address_not_found`, `target_address_not_found`, `no_grit_bin_nearby` | Postcode empty, hint miss, or no bin in radius |
| 502 | `address_api_unreachable`, `geoserver_unreachable`, `unexpected_schema` | Upstream down or unexpected body |

---

## Issues encountered and how investigated

### 1. Address schema has no single `Title`

- **Issue:** Matching on `Title` alone returned “not found” even when the postcode lookup succeeded.
- **Investigation:** Inspected live JSON; property name sits in `BuildingName`, coords under `SpatialFeature.Eastings` / `Northings`.
- **Fix:** Compose/match across Derbyshire address parts; tolerate alternate field aliases.

### 2. Invalid postcode returns HTTP 200 + XML

- **Issue:** Bad postcodes (e.g. `DE55 5PB4`) came back as XML with `ResponseError: Invalid postcode`, not a clean JSON 404.
- **Investigation:** Captured raw body/content-type; confirmed `Accept: application/json` is ignored for that error path.
- **Fix:** Detect XML/`ResponseError`; map to `invalid_postcode` (400). Also validate UK postcode format before calling upstream.

### 3. False “postcode not found” on good lookups

- **Issue:** Successful `DE55 5PB` responses were treated as failures.
- **Investigation:** Body-wide search for `ResponseError` hit nested Councillor objects (`"No results"`).
- **Fix:** Only treat top-level / XML error stubs as failures; ignore nested Councillor noise.

### 4. Geometry field name

- **Issue:** Default GeoServer examples use `the_geom`; this layer does not.
- **Investigation:** Inspected GetFeature / layer properties.
- **Fix:** Use `SP_GEOMETRY` in `DWITHIN`.

### 5. Empty DWITHIN is not always “no bins”

- **Issue:** Spatial filter can return empty (e.g. CRS/filter quirks) even when bins exist nearby.
- **Investigation:** Compared DWITHIN vs unfiltered GetFeature + local distance for the same origin.
- **Fix (exercise):** For this exercise, a full-layer fallback was used to validate DWITHIN results and still return a correct nearest bin within the radius.
- **Production preference:** I would not rely on downloading the whole layer if `DCC:Gritbins` grew large (e.g. hundreds of thousands of records). Prefer:
  - expanding-radius queries
  - nearest-neighbour GeoServer queries
  - spatial indexing
  - PostGIS-backed nearest searches

### 6. CORS / browser-direct calls

- **Issue:** Brief forbids client-side calls to upstream services.
- **Investigation:** Confirmed CORS would block browser → Address API / GeoServer with credentials.
- **Fix:** FastAPI backend + Next.js server-side proxy only.

---

## How the result was verified

- Resolved `HILLBROW` / `DE55 5PB` and recorded BNG coordinates (~443563, ~360212).
- Ran WFS `DWITHIN` / nearest path; confirmed returned Title **GB0199**.
- Independently computed Euclidean distance to GB0199 geometry (~49 m) — inside 100 m.
- Negative paths: missing params, invalid postcode, unknown address hint, no bin nearby.
- Automated: `pytest` with respx mocks for Address API and GeoServer.

---

## What I would improve with more time

- Recorded HTTP fixtures (VCR) for Address/WFS schema drift in CI
- Stronger observability: correlation IDs, structured logs, metrics on upstream latency/errors
- API versioning for a stable public contract (e.g. `/api/v1/nearest-grit-bin` rather than unversioned `/nearest-grit-bin`)
- Optional radius query param on nearest-N (UI + API) instead of unbounded full-layer when ranking N
- Generalise to `assetType` → layer mapping (schools, libraries, …) behind one endpoint
- Batch job: CSV/queue/worker with retries, dead-letter, and a results file
- AuthN/Z if exposing beyond an internal network
- Richer frontend: map pin for address vs grit bin, clearer empty/error states

### Spatial scalability

For this exercise GeoServer WFS queries are performed directly.

For high-volume production workloads I would consider loading GIS assets into a spatially indexed datastore such as PostGIS and performing nearest-neighbour searches using database spatial indexes rather than retrieving larger GeoServer result sets.

---

## Deploy and reuse

**Deploy (demonstrate running)**

- `docker compose up --build` → UI http://127.0.0.1:3000 · API http://127.0.0.1:8000/docs
- Or local: `uvicorn src.app:app` + `npm run dev` in `frontend/` (see `README.md`)
- Config via `.env` (Address API credentials, GeoServer base URL/layer, radius)
- Health: `GET /health`
- Demo check: `HILLBROW` + `DE55 5PB` → Title **GB0199**

**Reuse / follow-up discussion**

- **Other Solutions:** The API contract is self-documenting through FastAPI’s OpenAPI specification and Swagger UI (`/docs`). This allows other internal solutions to consume the service without requiring separate API documentation. Browser apps still use a server-side proxy (this Next.js BFF pattern or their own).
- **Versioned public API (design):** expose stable routes under `/api/v1/...` (e.g. `/api/v1/nearest-grit-bin`) when packaging for other teams.
- **Nearest five grit bins (built):** `GET /nearest-grit-bins?postcode=&address=&limit=5` (UI checkbox for custom limit).
- **Other asset types (design):** same pipeline with `assetType` → layer map (e.g. gritbin → `DCC:Gritbins`, school → `DCC:Schools`, …).
- **Large batch (design):**

```
CSV → Queue → Worker → Address Lookup → GeoServer query → Results file
```

  (retries, dead-letter, rate limits with more time)

---

## Resilience (upstream Address API / GeoServer)

Implemented today:

- HTTP timeout on upstream calls (`HTTP_TIMEOUT_SECONDS` / shared `httpx` client)

Production intent (more time):

- Retry transient failures (timeouts, 502/503)
- Circuit breaker for repeated upstream failures
- Clear typed errors when Address API or GeoServer is unavailable (`address_api_unreachable`, `geoserver_unreachable`)

---

## Test and monitor (production mindset)

**Test**

- Unit: address matching, postcode validation, Euclidean nearest, error mapping
- API: FastAPI TestClient + respx for upstream success/4xx/5xx/XML envelopes
- Smoke: live HILLBROW path + Docker stack after config is present

**Monitor**

- Health checks (`/health`)
- Structured logging (upstream failures, fallbacks)
- Metrics: request rate, latency, error codes (`invalid_postcode`, `no_grit_bin_nearby`, 502s)
- Alerts on Address API / GeoServer error rate
- Distributed tracing if the service sits in a wider platform (e.g. Application Insights)
