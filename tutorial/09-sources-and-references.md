# Sources, references, and domain background

This page is for learners who have **never** worked with Derbyshire County Council
systems, UK postcodes, grit bins, or spatial APIs. It also lists the **real
documentation and websites** you would open while building this project yourself.

Nothing here assumes secret knowledge. The Address Lookup API in the exercise is
credential-gated (brief + header file only). The map layer is public GeoServer —
you can probe it yourself.

---

## 1. Domain background (what is this about?)

### Derbyshire County Council (not “Derby City” only)

**Derbyshire** is a county in England. **Derbyshire County Council (DCC)** runs
many county-wide services (roads, winter maintenance, some mapping). The grit-bin
layer in this project is labelled `DCC:…`, which means it lives in the DCC
GeoServer **workspace**.

Public map / GIS host used in this project:

- https://wms.derbyshire.gov.uk/geoserver

(You may also see Derby *City* Council elsewhere on the web — different
organisation. This exercise uses **county** GeoServer / Address APIs.)

### What is a grit bin?

In the UK, a **grit bin** (sometimes “salt bin”) is a roadside container of grit
or rock salt. Councils place them so residents or crews can treat icy paths and
roads in winter. Finding the **nearest** bin to an address is a practical winter
ops / public-info problem.

You do not need a council job to understand the software: address → coordinates →
nearby mapped asset.

### UK postcodes (why `DE55 5PB`?)

UK addresses are commonly looked up by **postcode**. A full postcode looks like
`DE55 5PB`:

| Part | Example | Role |
|------|---------|------|
| Outward code | `DE55` | Area + district (rough geography) |
| Inward code | `5PB` | Sector + unit (narrows to a small set of addresses) |

Rules of thumb for this project:

- Spaces matter in human form (`DE55 5PB`); in URLs the space becomes `%20`
- Matching is usually case-insensitive
- One postcode can return **many** address records — that is why the exercise also
  asks for an address hint like `HILLBROW`

Royal Mail / Ordnance Survey style background (optional reading):

- https://www.royalmail.com/find-a-postcode  
- https://en.wikipedia.org/wiki/Postcodes_in_the_United_Kingdom  

### British National Grid (why not just lat/lon?)

UK local-authority GIS layers often use **British National Grid (BNG)**,
coordinate reference system **EPSG:27700**. Coordinates are **easting** and
**northing** in **metres**. That makes “within 100 metres” a natural question.

WGS84 lat/lon is **EPSG:4326** (degrees). Mixing degrees with metre-based map
layers without converting gives nonsense distances.

Registry entry:

- https://epsg.io/27700  
- https://epsg.io/4326  

Ordnance Survey overview of the National Grid:

- https://www.ordnancesurvey.co.uk/documents/resources/guide-to-nationalgrid.pdf  
  (or search “Ordnance Survey guide to the National Grid”)

---

## 2. What you get from the exercise itself

These are **primary** sources for the Derbyshire technical exercise. Without them
you cannot call the Address API.

| Source | What it gives you |
|--------|-------------------|
| **Technical exercise brief** | Problem statement, example `HILLBROW` / `DE55 5PB`, ~100 m rule, CORS constraint (no browser-direct calls to upstream APIs) |
| **Credentials / header file** | `ADDRESS_API_BASE_URL`, `x-alias`, `x-auth-token` (or equivalent) |
| **Live trial calls** | Actual JSON shape for addresses (this project found `BuildingName` + `SpatialFeature.Eastings/Northings`, not a single `Title` field) |

The Address Lookup API in this exercise is **not** a fully public, well-documented
product site. In practice you reverse-engineer the contract from:

1. The brief  
2. The credential file  
3. Sample HTTP responses (PowerShell, curl, or httpx)

That limitation is called out in [`docs/investigation-notes.md`](../docs/investigation-notes.md).

---

## 3. Live systems you probe yourself

### Derbyshire GeoServer (public)

Base URL used in `.env.example`:

```text
https://wms.derbyshire.gov.uk/geoserver
```

Useful entry points (open in a browser or curl):

| What | Why |
|------|-----|
| GeoServer web UI / welcome | Confirm the host is alive |
| WFS `GetCapabilities` for the DCC workspace | Discover layers and operations |
| WFS `GetFeature` for `DCC:Gritbins` | See real geometry + properties (`Title`, `SP_GEOMETRY`, …) |

Example GetFeature pattern (from this project’s investigation):

```text
{GEOSERVER_BASE_URL}/DCC/ows
  ?service=WFS
  &version=1.0.0
  &request=GetFeature
  &typeName=DCC:Gritbins
  &outputFormat=application/json
```

Optional spatial filter (what the code prefers):

```text
&CQL_FILTER=DWITHIN(SP_GEOMETRY,POINT(easting northing),100,meters)
```

**Important discovery from this project:** the hostname says `wms.` but you need
**WFS** (features), not **WMS** (map images). See
[`docs/issues-encountered.md`](../docs/issues-encountered.md).

### Address Lookup API (credentialed)

Shape used by this codebase:

```text
GET {ADDRESS_API_BASE_URL}/{postcode}
Headers: x-alias, x-auth-token, Accept: application/json
```

There is no separate public “developer portal” referenced in-repo for this API —
the brief + headers + live responses are the documentation.

---

## 4. Standards and vendor docs (spatial stack)

These are the references that make GeoServer / WFS / CQL understandable if you are
new to GIS. For a guided explanation of how this project uses them (EPSG:27700,
WFS vs WMS, DWITHIN, the Euclidean fallback, `SP_GEOMETRY`), see
[10-spatial-querying.md](./10-spatial-querying.md).

### OGC / WFS (what “GetFeature” means)

- OGC WFS overview: https://www.ogc.org/standard/wfs/  
- Idea to take away: **WFS returns feature data** (points + attributes); **WMS
  returns pictures of maps**.

### GeoServer documentation

Official docs (search within for the topic you need):

- https://docs.geoserver.org/  
- WFS reference / GetFeature:  
  https://docs.geoserver.org/latest/en/user/services/wfs/reference.html  
- CQL filters (including spatial predicates like `DWITHIN`):  
  https://docs.geoserver.org/latest/en/user/tutorials/cql/cql_tutorial.html  
  https://docs.geoserver.org/latest/en/user/filter/ecql_reference.html  

### GeoJSON (what the JSON features look like)

- https://geojson.org/  
- RFC 7946: https://datatracker.ietf.org/doc/html/rfc7946  

### Coordinate conversion library used here

- pyproj docs: https://pyproj4.github.io/pyproj/stable/  
- PROJ (underlying library): https://proj.org/  

### EPSG registry

- https://epsg.io/  
- https://spatialreference.org/ref/epsg/27700/  

---

## 5. Framework and library docs (how the app is built)

### Backend

| Topic | Link |
|-------|------|
| FastAPI | https://fastapi.tiangolo.com/ |
| FastAPI first steps | https://fastapi.tiangolo.com/tutorial/first-steps/ |
| Query parameters | https://fastapi.tiangolo.com/tutorial/query-params/ |
| Handling errors | https://fastapi.tiangolo.com/tutorial/handling-errors/ |
| Lifespan / startup | https://fastapi.tiangolo.com/advanced/events/ |
| Uvicorn | https://www.uvicorn.org/ |
| httpx (async HTTP client) | https://www.python-httpx.org/ |
| Pydantic | https://docs.pydantic.dev/ |
| pydantic-settings | https://docs.pydantic.dev/latest/concepts/pydantic_settings/ |
| python-dotenv | https://saurabh-kumar.com/python-dotenv/ |
| pytest | https://docs.pytest.org/ |
| respx (mock httpx) | https://lundberg.github.io/respx/ |

### Frontend

| Topic | Link |
|-------|------|
| Next.js App Router | https://nextjs.org/docs/app |
| Route Handlers (API routes) | https://nextjs.org/docs/app/building-your-application/routing/route-handlers |
| Environment variables | https://nextjs.org/docs/app/building-your-application/configuring/environment-variables |
| React (`useState`, forms) | https://react.dev/learn |
| TypeScript handbook | https://www.typescriptlang.org/docs/handbook/intro.html |

### Docker

| Topic | Link |
|-------|------|
| Dockerfile reference | https://docs.docker.com/reference/dockerfile/ |
| Compose file | https://docs.docker.com/compose/compose-file/ |
| Multi-stage builds | https://docs.docker.com/build/building/multi-stage/ |

---

## 6. How this project was actually investigated (honest trail)

Aligned with [`docs/investigation-notes.md`](../docs/investigation-notes.md) — the
practical order someone building this would follow:

1. **Read the brief** — postcode + address → nearest grit bin within ~100 m; no
   browser CORS to upstream APIs.
2. **Load credentials into `.env`** — never hard-code tokens.
3. **Call the Address API** with `DE55 5PB` — inspect JSON; discover real field
   names (`BuildingName`, `SpatialFeature`, …).
4. **Open Derbyshire GeoServer** — confirm `DCC:Gritbins` via WFS, not WMS tiles.
5. **Sample GetFeature JSON** — learn `SP_GEOMETRY`, `Title`, EPSG:27700.
6. **Read GeoServer CQL docs** — try `DWITHIN(... meters)` against a known BNG point.
7. **Read EPSG / OS National Grid notes** — decide to normalise everything to
   EPSG:27700 and use planar metres (or server-side `DWITHIN`).
8. **Reject Haversine-on-lat/lon** without reprojection — wrong CRS model for this
   layer.
9. **Implement FastAPI** using FastAPI + httpx + pydantic-settings docs.
10. **Add Euclidean fallback** when DWITHIN fails or returns empty (live GeoServer
    quirks — see issues notes).
11. **Add Next.js proxy** because the brief forbids browser-direct upstream calls.
12. **Verify** with the interview example → grit bin title `GB0199` ≈ 49 m away.

Tools that helped (same notes):

- PowerShell `Invoke-RestMethod` / `Invoke-WebRequest` (or curl) for live probes  
- `pyproj` for CRS round-trips  
- `httpx` + `respx` + `pytest` for offline tests  
- FastAPI `/docs` for manual endpoint checks  
- Docker Compose for a reproducible full stack  

---

## 7. In-repo notes worth reading next

These capture decisions and traps specific to **this** codebase:

| Doc | Why read it |
|-----|-------------|
| [`docs/investigation-notes.md`](../docs/investigation-notes.md) | What was tried, rejected, and verified |
| [`docs/assumptions.md`](../docs/assumptions.md) | Matching rules, CRS, 100 m radius |
| [`docs/issues-encountered.md`](../docs/issues-encountered.md) | WMS vs WFS, XML exceptions, live Address schema |
| [`docs/approach.md`](../docs/approach.md) | Pipeline design (validate → geocode → reproject → query) |
| [`docs/deploy.md`](../docs/deploy.md) | Container + gateway thinking |
| Root [`README.md`](../README.md) | Runbook, env table, error codes |

---

## 8. Suggested reading order if you are completely new

1. This page — §§1–2 (domain + exercise materials)  
2. Probe GeoServer GetFeature in a browser (§3)  
3. Skim GeoServer WFS + CQL tutorial links (§4)  
4. Skim EPSG:27700 on epsg.io (§1 / §4)  
5. FastAPI first-steps tutorial (§5)  
6. [`backend/00-python-fastapi-basics.md`](./backend/00-python-fastapi-basics.md)  
7. Then start typing the lab at [`backend/README.md`](./backend/README.md)  

You do not need to memorise GIS theory. You need enough to answer:

> “Where is this address in metres on the same grid as the grit bins, and which
> bin is within 100 m?”


---

<!-- tutorial-nav -->

| Previous | Next |
|:---------|-----:|
| ← [Introduction](./01-introduction.md) | [Architecture](./02-architecture.md) → |
