# Issues encountered

- **`.env` format**: the original file held header/URL fragments as free text rather
  than `KEY=value` pairs. `python-dotenv` needs `KEY=value`, so it was normalised and
  a sanitised `.env.example` was added.
- **WMS vs WFS confusion risk**: the base URL is a `wms.` host, but the exercise
  requires feature data. Using the WMS `GetMap` would return an image, not attributes —
  the WFS `GetFeature` path (`/DCC/ows`) is the correct one.
- **GeoServer can return HTTP 200 with an XML `ServiceExceptionReport`** instead of a
  JSON error. A naive `.json()` parse would throw; the client detects XML/exception
  bodies and treats them as a failure that triggers the fallback.
- **Coordinate order in WKT**: `POINT(x y)` must be `POINT(easting northing)` in
  EPSG:27700 — swapping them silently returns wrong/empty results.
- **Live Address API schema** has no `Title` field: the property name is
  `BuildingName` (e.g. `HILLBROW`) and coordinates are nested under
  `SpatialFeature.Eastings` / `SpatialFeature.Northings`. Early matching against
  a `Title` key returned `target_address_not_found` even though the postcode
  lookup succeeded — fixed by composing/matching across Derbyshire address parts.

