# 2. Architecture Overview

## What you will do

Understand the data flow and the **backend layered design**. No coding yet.

## Responsibilities

### Backend (FastAPI)

- Accept `postcode` and `address` query params
- Call the Address Lookup API
- Match the address and normalise coordinates to **EPSG:27700** (British National Grid)
- Query GeoServer WFS for the nearest grit bin
- Return JSON success or a typed JSON error

### Frontend (Next.js)

- Render the search form
- Call its **own** `/api/nearest-grit-bin` route (same origin)
- That route (server-side) forwards to FastAPI
- Show the result or a friendly error

## Fullstack data flow

```mermaid
flowchart TD
  Browser["Browser (user)"]
  NextUI["Next.js UI<br/>page + SearchForm"]
  Proxy["Next.js proxy<br/>/api/nearest-grit-bin"]
  API["FastAPI :8000"]
  Addr["Address Lookup API"]
  Geo["GeoServer WFS"]

  Browser -->|"GET /api/nearest-grit-bin?postcode&address"| NextUI
  NextUI --> Proxy
  Proxy -->|"GET /nearest-grit-bin"| API
  API --> Addr
  API --> Geo
  Geo --> API
  Addr --> API
  API --> Proxy
  Proxy --> Browser
```

## Why the proxy exists

1. **Secrets stay on the server** (Address API token never reaches the browser)
2. **No CORS pain** — the browser only talks to Next.js on the same origin
3. **Clean separation** — UI talks to `/api/…`; FastAPI talks to Derbyshire systems

## Backend layered design

The backend is split so each layer has **one job**. Routers never call GeoServer
directly; services never import FastAPI; repositories own all upstream HTTP.

```mermaid
flowchart TB
  subgraph api_layer ["api/ — HTTP boundary"]
    R["routers/<br/>address.py, gritbins.py"]
    D["dependencies/<br/>DI: settings, httpx, services"]
  end

  subgraph svc_layer ["services/ — business rules"]
    AS["address_service.py"]
    GS["gritbin_service.py"]
  end

  subgraph repo_layer ["repositories/ — external I/O"]
    AR["address_repository.py"]
    GR["gritbin_repository.py"]
  end

  subgraph models_layer ["models/"]
    DTO["dto/ — Pydantic responses"]
    DOM["domain/ — Point27700, GritBinMatch…"]
  end

  subgraph core_utils ["core/ + utils/"]
    SET["core/settings.py"]
    GEO["utils/geospatial.py"]
    EX["utils/exceptions.py"]
  end

  R --> D
  D --> AS
  D --> GS
  AS --> AR
  GS --> GR
  AS --> DOM
  GS --> DOM
  R --> DTO
  AR --> SET
  GR --> SET
  AS --> GEO
  GS --> GEO
  AS --> EX
  GS --> EX
```

### Request path inside FastAPI

```mermaid
sequenceDiagram
  participant C as Client
  participant Router as gritbins router
  participant AddrSvc as AddressService
  participant AddrRepo as AddressRepository
  participant GritSvc as GritBinService
  participant GritRepo as GritBinRepository

  C->>Router: GET /nearest-grit-bin?postcode&address
  Router->>AddrSvc: resolve_address(...)
  AddrSvc->>AddrRepo: fetch_by_postcode(...)
  AddrRepo-->>AddrSvc: raw records
  AddrSvc-->>Router: ResolvedAddress (BNG point)
  Router->>GritSvc: find_nearest(point)
  GritSvc->>GritRepo: query_dwithin(...)
  alt DWITHIN ok
    GritRepo-->>GritSvc: candidate features
  else DWITHIN fails / empty
    GritSvc->>GritRepo: fetch_all()
    GritRepo-->>GritSvc: all features
    Note over GritSvc: Euclidean nearest in geospatial utils
  end
  GritSvc-->>Router: GritBinMatch
  Router-->>C: NearestGritBinResponse JSON
```

### Layer rules (memorise these)

| Layer | May do | Must not do |
|-------|--------|-------------|
| **Routers** | Parse query params, call services, return DTOs | Call GeoServer / Address API, do CRS maths |
| **Services** | Match addresses, orchestrate DWITHIN fallback | Import FastAPI, build HTTP responses |
| **Repositories** | httpx calls, parse upstream envelopes | Business ranking / “nearest” decisions |
| **Domain / utils** | Points, distance, exceptions | Know about HTTP status codes on routers |

Deep dive before you type the backend:

→ [backend/00-backend-design.md](./backend/00-backend-design.md)

---

<!-- tutorial-nav -->

| Previous | Next |
|:---------|-----:|
| ← [Sources and references](./09-sources-and-references.md) | [Folder structure](./03-folder-structure.md) → |
