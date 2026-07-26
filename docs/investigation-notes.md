# Investigation notes

How the problem was investigated (tools, trials, rejections, and verification).

## What I tried first

1. Confirmed the **Address Lookup** URL shape: postcode appended to the base path,
   with `x-alias` / `x-auth-token` from the provided credentials file.
2. Probed **GeoServer** capabilities — starting from the public WMS host — to find
   how `DCC:Gritbins` is exposed and which service returns *features* (not map tiles).
3. Sampled a small `GetFeature` response to learn the schema (`SP_GEOMETRY`, `Title`,
   EPSG:27700 coordinates).
4. Tested a **CQL `DWITHIN`** filter around a known BNG point before wiring it into
   the FastAPI service.

## Tools used

- **PowerShell / `Invoke-RestMethod` / `Invoke-WebRequest`** — live GeoServer WFS probes
- **`pyproj`** — EPSG:4326 ↔ EPSG:27700 conversion and round-trip checks
- **`httpx` + `respx` + `pytest`** — mocked unit/API tests without live credentials
- **Docker / Docker Compose** — reproducible server-side runtime (avoids CORS entirely)
- **FastAPI `/docs`** — interactive smoke-testing of the endpoint

## Documentation / resources

- GeoServer WFS / CQL filter documentation (GetFeature, `DWITHIN`, output formats)
- British National Grid / EPSG:27700 behaviour (planar metres → Euclidean distance OK)
- Derbyshire GeoServer layer metadata implied by live responses (`geometry_name`,
  property names)
- Address API: only the exercise brief + header file (limited docs by design)

## Assumptions made

See [assumptions.md](assumptions.md). In short: Title substring match, BNG layer CRS,
100 m radius as authoritative, first matching address wins.

## Approaches rejected

- **Browser / client-side JavaScript calling the APIs directly** — blocked by CORS
  (explicit constraint in the brief). A backend is required.
- **GeoServer WMS `GetMap`** — returns raster images, not grit-bin attributes/titles.
- **Haversine on lat/lon without reprojection** — layer is EPSG:27700; BNG planar
  distance (or server-side `DWITHIN` in metres) is the correct model.
- **Hard-coding HILLBROW / DE55 5PB** — the service must accept any postcode/address
  dynamically via query parameters.
- **Hard-coding API URLs / tokens in source** — credentials and base URLs belong in
  `.env` only.

## How the result was verified

- Live WFS: `DWITHIN(SP_GEOMETRY, POINT(...), 100, meters)` returned matching grit-bin
  features with a `Title` property.
- Unit tests cover address matching (including Derbyshire `BuildingName` /
  `SpatialFeature` schema), CRS conversion, DWITHIN success, Euclidean fallback, and
  typed errors (`pytest`).
- End-to-end path: `GET /nearest-grit-bin?postcode=DE55%205PB&address=HILLBROW`
  → Address API → BNG point → WFS → JSON result.
- **Live demonstrated result** (Docker Compose frontend proxy + backend):

```json
{
  "address": "HILLBROW",
  "postcode": "DE55 5PB",
  "nearest_grit_bin_title": "GB0199",
  "distance_meters": 48.99
}
```

  So the grit bin **Title** returned is **`GB0199`**, ~49 m from HILLBROW (within 100 m).
- Runtime: `docker compose up --build` — UI on `:3000`, API on `:8000`.

## Technical findings (evidence)

- **WFS endpoint**:
  `{GEOSERVER_BASE_URL}/DCC/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=DCC:Gritbins&outputFormat=application/json`
- **Feature schema**: Point in EPSG:27700; `geometry_name` = `SP_GEOMETRY`; properties
  include `Title` (e.g. `GBAV-424`), `Subtitle`, `Street_Name`, `Town_Name`, `USRN`.
- **CRS sanity**: Derbyshire BNG ≈ 440k E / 350k N; pyproj round-trips to sub-metre
  accuracy (`tests/test_coordinates.py`).
