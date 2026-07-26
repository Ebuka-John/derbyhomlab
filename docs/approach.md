# Approach

I treated the exercise as an **integration pipeline** with clearly separated stages:

```
validate params → geocode address → reproject to BNG → spatial query → rank → respond
```

Design principles applied:

- **Thin transport layer** (`src/app.py`): parameter validation, dependency wiring,
  and mapping domain errors to HTTP/JSON. No business logic.
- **I/O isolated in services** (`address_service.py`, `geoserver_service.py`): each
  external system has one client that knows its schema quirks and failure modes.
- **Pure functions in utils** (`coordinates.py`): reprojection and distance math are
  side-effect free and unit-tested in isolation.
- **Config from environment only** (`config.py`): all URLs, headers and tuning values
  come from `.env` via `pydantic-settings`; nothing is hard-coded.
- **WFS over WMS**: WMS renders map *images*; WFS returns *feature geometry and
  attributes*, which is what we need for distance calculation and titles.
- **Preferred server-side spatial filter, with a client-side fallback** so the service
  still works if the GeoServer instance disables CQL spatial predicates.
