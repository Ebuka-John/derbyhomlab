# Approach

I treated the exercise as an **integration pipeline** with clearly separated stages:

```
validate params → geocode address → reproject to BNG → spatial query → rank → respond
```

```mermaid
flowchart LR
  V[Validate] --> G[Geocode]
  G --> R[Reproject BNG]
  R --> S[Spatial query]
  S --> K[Rank nearest]
  K --> J[JSON DTO]
```

## Layered backend

```mermaid
flowchart TB
  subgraph api ["api/"]
    RT[routers]
    DP[dependencies]
  end
  subgraph biz ["services/"]
    AS[address_service]
    GS[gritbin_service]
  end
  subgraph io ["repositories/"]
    AR[address_repository]
    GR[gritbin_repository]
  end
  RT --> DP --> AS --> AR
  DP --> GS --> GR
```

Design principles applied:

- **Thin HTTP layer** (`api/routers` + `app.py`): parameter validation, dependency
  wiring, and mapping domain errors to HTTP/JSON. No business logic.
- **Business rules in services** (`address_service.py`, `gritbin_service.py`): no
  FastAPI imports; orchestrate matching and DWITHIN fallback.
- **I/O isolated in repositories**: each external system has one client that knows
  its schema quirks and failure modes.
- **Pure helpers in utils** (`geospatial.py`): reprojection and distance math are
  side-effect free and unit-tested in isolation.
- **Domain vs DTO**: internal dataclasses in `models/domain/`; Pydantic wire models
  in `models/dto/`.
- **Config from environment only** (`core/settings.py`): all URLs, headers and
  tuning values come from `.env` via `pydantic-settings`; nothing is hard-coded.
- **WFS over WMS**: WMS renders map *images*; WFS returns *feature geometry and
  attributes*, which is what we need for distance calculation and titles.
- **Preferred server-side spatial filter, with a client-side fallback** so the
  service still works if the GeoServer instance disables CQL spatial predicates.
