# Assumptions

- The Address Lookup API returns a JSON **list** of address records for a postcode.
  On the live Derbyshire API there is **no** single `Title` field — the property name
  sits in `BuildingName` (e.g. `HILLBROW`), with street/locality parts alongside, and
  coordinates under `SpatialFeature.Eastings` / `SpatialFeature.Northings` (EPSG:27700),
  plus optional WGS84 lat/lon.
- The `address` query parameter is a **case-insensitive substring** of the composed
  address text (BuildingName and related parts), e.g. `HILLBROW` matches the
  HILLBROW record for `DE55 5PB`.
- The GeoServer layer `DCC:Gritbins` publishes geometry in **EPSG:27700** under the
  attribute `SP_GEOMETRY` (confirmed against the live WFS endpoint). The grit bin
  display name is the feature property `Title` (e.g. `GB0199`).
- The **100 m** radius is authoritative: a bin outside the radius is not returned even
  if it is the globally nearest one. The radius is configurable via
  `NEAREST_SEARCH_RADIUS_METERS`.
- The first matching address record is the intended property (the interview example is
  unambiguous). Multiple-match disambiguation is out of scope.
- Missing / unmatched address and “no bin within 100 m” are **client-visible errors**
  (`target_address_not_found`, `address_not_found`, `no_grit_bin_nearby`), not empty
  200 responses.
- This service is internal/trusted for the exercise; it does not yet authenticate its
  own callers.
- Upstream Address / GeoServer calls are made **server-side only** (FastAPI / Next.js
  proxy) because browser CORS blocks direct client calls.
