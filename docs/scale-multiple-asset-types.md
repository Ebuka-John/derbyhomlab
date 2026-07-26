# How to scale to multiple asset types

Grit bins are just one GeoServer layer; the pattern generalises:

- **Config-driven layer map**, e.g. `ASSET_LAYERS={"grit-bin": "DCC:Gritbins",
  "gulley": "DCC:Gullies", ...}`, resolved from the environment.
- **Generalise the endpoint** to `GET /nearest-asset?type=grit-bin&postcode=...&address=...`
  and have `GeoServerService.find_nearest(layer, geometry_field, origin, radius)` accept
  the layer/geometry-field as arguments (they are already the only asset-specific parts).
- **Keep response DTOs thin** and asset-agnostic (`title`, `distance_meters`, plus an
  optional `properties` bag).
- **Fan out** with `asyncio.gather` when a caller wants the nearest asset across several
  asset classes at once.
