# For a G11 Senior Developer (Integration) exercise

I'd present pseudocode at service level, integration level, and business flow level. The objective is to show architecture, separation of concerns, maintainability, error handling, and scalability.

Panel pack companions: [`submission-notes.md`](./submission-notes.md) (tools, issues, deploy, test) · [`interview.md`](./interview.md) (brief) · [`interview-coverage.md`](./interview-coverage.md) (checklist).

## Solution Architecture

```
FastAPI Router
       |
       v
AddressService + GritBinService
       |                  |
       v                  v
AddressRepository   GritBinRepository
       |                  |
       v                  v
Address API         GeoServer WFS
                          |
                          v
               geospatial helpers
               (Euclidean nearest)
                          |
                          v
               Return grit bin title
               + distance_meters
```

Layers:

- **routers** — HTTP only (query params → DTOs)
- **services** — business rules (no FastAPI imports)
- **repositories** — upstream HTTP
- **utils/geospatial** — CRS + planar distance

## Design patterns

### What I used

| Pattern | Where in this repo | Why |
|---------|-------------------|-----|
| **Layered architecture** | `api/` → `services/` → `repositories/` | One job per layer; change GeoServer without touching routers |
| **Repository** | `AddressRepository`, `GritBinRepository` | Encapsulate Address API / WFS HTTP; no matching or ranking here |
| **Service / application layer** | `AddressService`, `GritBinService` | Business rules; no FastAPI imports → easy unit tests |
| **DTO vs domain** | `models/dto` vs `models/domain` | Wire JSON ≠ internal value objects (`ResolvedAddress`, `Point27700`) |
| **Dependency injection** | FastAPI `Depends` + lifespan `httpx.AsyncClient` | Shared client/settings injected into services |
| **Centralised errors** | `AppError` hierarchy + handler in `app.py` | Stable `{ error: { code, message } }` for UI and tests |
| **Settings / 12-factor** | `pydantic-settings` + `.env` | Secrets and URLs outside source |
| **BFF / server proxy** | Next.js `app/api/*` → FastAPI | CORS + credentials stay server-side (brief requirement) |

```text
Browser → Next.js proxy → FastAPI router → service → repository → upstream
```

### Why not a single “god” module?

- Hard to mock Address API vs GeoServer independently
- HTTP status codes mixed into spatial logic
- Reuse for nearest-5 / other asset layers becomes copy-paste

### What I rejected (design-wise)

- **Fat controllers** — all logic in route handlers
- **Browser-direct upstream calls** — forbidden by brief; leaks tokens; CORS
- **Anemic “utils-only” dump** — no clear ownership of Address vs grit-bin rules

### Panel soundbite

> I used a layered FastAPI design: routers for HTTP, services for rules, repositories for Address API and GeoServer. DTOs sit at the edge; domain models stay internal. Next.js proxies so the browser never talks to Derbyshire. That makes each integration mockable and matches the CORS constraint.

Pocket card: [`G11_Interview_Rivision_Notes.md`](./G11_Interview_Rivision_Notes.md) · spoken script: [`submission-notes.md`](./submission-notes.md)

## Main Business Flow

```
FUNCTION FindNearestGritBin(postcode, address, searchRadius = 100)

    // Validate UK postcode format (invalid → 400 invalid_postcode)

    resolved =
        AddressService.ResolveAddress(
            postcode,
            address
        )
    // throws address_not_found / target_address_not_found / …

    features =
        GritBinService.CandidateFeatures(
            origin = resolved.point,   // EPSG:27700
            radius = searchRadius
        )
    // 1) WFS DWITHIN on SP_GEOMETRY
    // 2) if DWITHIN fails or is empty → fetch full layer (fallback)

    nearestBin =
        Geospatial.FindNearest(
            origin = resolved.point,
            features,
            radius = searchRadius
        )
    // throws no_grit_bin_nearby if none within radius

    RETURN
    {
        address: address,
        postcode: resolved.postcode,
        nearest_grit_bin_title: nearestBin.title,
        distance_meters: nearestBin.distance_meters
    }

END FUNCTION
```

Interview example (any pair works): `postcode=DE55 5PB`, `address=HILLBROW`.

## Address Service

### Responsibility

- Query Address API by postcode
- Match address hint (case-insensitive substring)
- Extract Easting/Northing (BNG), or convert lat/lon → EPSG:27700

```
FUNCTION ResolveAddress(postcode, address)

    cleaned = RequireValidUkPostcode(postcode)

    url =
        ADDRESS_API + "/" + UrlEncode(cleaned)

    response =
        HttpGet(url, requiredHeaders)   // x-alias, x-auth-token, Accept: json

    // Map XML/JSON ResponseError → invalid_postcode / address_not_found
    // Empty list → address_not_found

    records = ParseAddressList(response)

    FOR EACH record IN records
        IF ToUpper(MatchableText(record)) CONTAINS ToUpper(address)
            RETURN ResolvedAddress(
                title,
                postcode = cleaned,
                point = Point27700(easting, northing)
            )
        END IF
    END FOR

    THROW target_address_not_found

END FUNCTION
```

## Grit Bin / GeoServer

### Why WFS?

Not WMS.

- **WMS:** Returns Images
- **WFS:** Returns Features

We need actual geometry and attributes.

### Where does `/DCC/ows` come from?

**Not in the assessment brief.** The brief asks you to identify the correct
GeoServer service; env gives the host root (`GEOSERVER_BASE_URL`) and we configure
the layer as `DCC:Gritbins`.

Discovery:

| Clue | Inference |
|------|-----------|
| `DCC:Gritbins` | Workspace `DCC`, layer `Gritbins` |
| GeoServer convention | Workspace OGC endpoint ≈ `{base}/{workspace}/ows` |
| Live probe | GetCapabilities / GetFeature on Derbyshire host returns grit-bin features |

Encoded in settings:

```text
geoserver_wfs_url = f"{GEOSERVER_BASE_URL}/DCC/ows"
```

`GEOSERVER_LAYER` is only the WFS `typeName` query param — not the path.

**References**

- GeoServer WFS GetFeature: https://docs.geoserver.org/maintain/en/user/services/wfs/reference.html
- GeoServer virtual / workspace services: https://docs.geoserver.org/maintain/en/user/services/virtual-services.html
- Live host: https://wms.derbyshire.gov.uk/geoserver  
  Smoke: `…/DCC/ows?service=WFS&version=1.0.0&request=GetCapabilities`
- Same `/DCC/ows` pattern in the wild: https://sourceforge.net/p/geoserver/mailman/message/58756516/
- Panel narrative: [`submission-notes.md`](./submission-notes.md) § “How `/DCC/ows` was found”

### GeoServer Query (as implemented)

```
FUNCTION QueryDWithin(origin, radius)

    parameters =
        service = WFS
        version = 1.0.0
        request = GetFeature
        typeName = DCC:Gritbins
        outputFormat = application/json
        CQL_FILTER =
            DWITHIN(
                SP_GEOMETRY,
                POINT(easting northing),
                radius,
                meters
            )

    RETURN ParseGeoJson(HttpGet(GEOSERVER/DCC/ows, parameters))

END FUNCTION
```

### Candidate features + fallback

```
FUNCTION CandidateFeatures(origin, radius)

    TRY
        features = QueryDWithin(origin, radius)
    CATCH GeoServer failure
        features = FetchAll()          // full GetFeature
    END TRY

    IF features IS EMPTY
        features = FetchAll()          // empty DWITHIN can be a CRS miss
    END IF

    RETURN features

END FUNCTION
```

## Spatial helpers

Although GeoServer can perform proximity filtering, distances are still calculated in-process to guarantee correctness and ranking.

```
FUNCTION FindNearest(origin, features, radius)

    shortestDistance = INFINITY
    nearestBin = NULL

    FOR EACH feature IN features
        point = FeaturePoint(feature)      // GeoJSON coords → BNG
        distance = CalculateDistance(
            origin.easting, origin.northing,
            point.easting, point.northing
        )
        IF distance <= radius AND distance < shortestDistance
            shortestDistance = distance
            nearestBin = feature
        END IF
    END FOR

    IF nearestBin IS NULL
        THROW no_grit_bin_nearby
    END IF

    RETURN { title, distance_meters: shortestDistance }

END FUNCTION
```

## Distance Formula

Because EPSG:27700 uses metres:

```
FUNCTION CalculateDistance(x1, y1, x2, y2)

    dx = x2 - x1
    dy = y2 - y1

    RETURN SQRT(dx² + dy²)

END FUNCTION
```

## FastAPI Endpoints (as implemented)

```
GET /api/v1/nearest-grit-bin?postcode=&address=
GET /api/v1/nearest-grit-bins?postcode=&address=&limit=5
GET /api/v1/grit-bins
GET /api/v1/health
```

```
GET /api/v1/nearest-grit-bin

TRY
    result = FindNearestGritBin(postcode, address)
    RETURN 200 + result
CATCH missing_parameter | invalid_postcode
    RETURN 400 { error: { code, message } }
CATCH address_not_found | target_address_not_found | no_grit_bin_nearby
    RETURN 404 { error: { code, message } }
CATCH address_api_unreachable | geoserver_unreachable | unexpected_schema
    RETURN 502 { error: { code, message } }
END TRY
```

Frontend: Next.js UI proxies `/api/*` → FastAPI (browser never calls Address API or GeoServer).

## Error Handling (as implemented)

Stable body shape:

```json
{
  "error": {
    "code": "target_address_not_found",
    "message": "Address 'HILLBROW' was not found within postcode 'DE55 5PB'."
  }
}
```

| HTTP | code |
|------|------|
| 400 | `missing_parameter`, `invalid_postcode` |
| 404 | `address_not_found`, `target_address_not_found`, `no_grit_bin_nearby` |
| 502 | `address_api_unreachable`, `geoserver_unreachable`, `unexpected_schema` |

## Production Version (Reusable Design)

Built today:

```
FindNearestGritBin / FindNearestGritBins(limit)
GET /api/v1/nearest-grit-bin
GET /api/v1/nearest-grit-bins?limit=5
```

Future generalisation:

```
FindNearestAsset(assetType)
GET /assets/nearest?postcode=&address=&assetType=gritbin
```

### Asset mappings (future):

- gritbin -> DCC:Gritbins
- school -> DCC:Schools
- library -> DCC:Libraries
- hospital -> DCC:Hospitals
- defibrillator -> DCC:Defibrillators
- carpark -> DCC:CarParks
- busstop -> DCC:BusStops
- firehydrant -> DCC:FireHydrants
- recycling -> DCC:RecyclingCentres
- shelter -> DCC:EmergencyShelters
- firstaid -> DCC:FirstAidStations

## Investigation Notes (What I'd Present)

### What I tried first

- Investigated Address Lookup API.
- Determined postcode is the lookup key.
- Identified HILLBROW from returned postcode results.
- Investigated GeoServer capabilities.
- Determined WFS is more suitable than WMS.

### Why WFS

- WMS -> map image
- WFS -> spatial features

The solution requires geometry and attributes, therefore WFS is the appropriate service.

### Assumptions

- Address API returns Easting/Northing.
- Coordinates are EPSG:27700.
- SP_GEOMETRY contains point geometry.
- Grit bins contain a Title attribute.
- HILLBROW is returned within postcode results.

### Approaches Rejected

#### Client-side JavaScript

Rejected because exercise explicitly mentions CORS restrictions.

#### Download Entire Layer

Rejected as the **primary** path because:

- Poor performance
- Unnecessary network traffic
- Poor scalability

Instead:

- Spatial query against GeoServer (`DWITHIN`)

Fallback only:

- If DWITHIN fails or returns empty, fetch the layer and rank by Euclidean distance within the radius.

### Verification:

- Confirm HILLBROW coordinates.
- Execute WFS query.
- Verify returned grit bin location.
- Calculate distance independently.
- Check nearest returned bin.

## Follow-Up Discussion Answers

### Nearest 5 Grit Bins

```
GET /api/v1/nearest-grit-bins?postcode=&address=&limit=5
```

- Same address resolve as nearest-one
- Load candidates (full layer for unbounded nearest-N, or DWITHIN when a radius is set)
- Sort by Euclidean distance ascending, take `limit`
- Return `{ nearest_grit_bins: [{ title, distance_meters }, ...] }`

### Batch Processing

```
CSV
  ->
Queue
  ->
Worker
  ->
Address Lookup
  ->
GeoServer Query
  ->
Results File
```

### Shared Service For Other Teams

Expose:

- REST API
- OpenAPI / Swagger
- Versioned Endpoints
- SDK Generation

### Monitoring:

- Application Insights
- Structured Logging
- Health Checks
- Metrics
- Distributed Tracing
- Snapshot Debugger
- Alerting

---

This is the level of pseudocode and architectural reasoning I'd expect from a strong Senior Developer (Integration) submission.

## Determine the most appropriate way to query GeoServer

For this exercise, when they say:

"Determine the most appropriate way to query GeoServer"

they're really testing whether you understand spatial queries and when to use each one.

### Assuming:

- Layer: DCC:Gritbins
- Geometry Field: SP_GEOMETRY
- Projection: EPSG:27700

and your property is:

```
POINT(Easting Northing)
```

### 1. DWITHIN (Most Appropriate)

Find features within a distance from a point.

```
Find grit bins within 100 metres of HILLBROW
```

Conceptually:

```
DWITHIN(
  SP_GEOMETRY,
  POINT(438123 356789),
  100,
  metres
)
```

Returns:

- Grit Bin A 25m
- Grit Bin B 67m
- Grit Bin C 94m

#### Use Cases

- Nearest grit bins
- Nearest schools
- Nearest libraries
- Nearest defibrillators

For this exercise, this would be my first choice.

### 2. WITHIN

Find assets completely inside a boundary.

```
Is this grit bin inside Derbyshire?
```

Conceptually:

```
WITHIN(
   SP_GEOMETRY,
   DerbyshireBoundary
)
```

#### Use Cases

- Assets within a district
- Assets within a ward
- Schools within a catchment area
- Libraries within a borough

### 3. INTERSECTS

Find geometries that touch or overlap.

Conceptually:

```
INTERSECTS(
    SP_GEOMETRY,
    SearchArea
)
```

#### Use Cases

- Roads crossing flood areas
- Schools within flood zones
- Properties touching planning zones
- Grit bins located on treated routes

### 4. CONTAINS

Find features completely contained within another feature.

Conceptually:

```
CONTAINS(
   SchoolBoundary,
   Playground
)
```

#### Use Cases

- School contains building
- Ward contains address
- Hospital campus contains car park

### 5. CROSSES

Find geometries that cross each other.

Conceptually:

```
CROSSES(
    Road,
    River
)
```

#### Use Cases

- Road crossings
- Utility network crossings
- Cycleway crossing railway

### 6. TOUCHES

Find features sharing a boundary.

Conceptually:

```
TOUCHES(
    WardA,
    WardB
)
```

#### Use Cases

- Neighbouring wards
- Adjacent land parcels
- Adjacent council regions

### 7. OVERLAPS

Find features partially occupying the same space.

Conceptually:

```
OVERLAPS(
    FloodZone,
    HousingArea
)
```

#### Use Cases

- Flood risk analysis
- Planning permissions
- Conservation areas

### 8. DISJOINT

Find geometries that do not touch.

Conceptually:

```
DISJOINT(
   School,
   FloodZone
)
```

#### Use Cases

- Schools outside flood areas
- Assets not impacted by roadworks

### 9. EQUALS

Find exact geometric matches.

Conceptually:

```
EQUALS(
   GeometryA,
   GeometryB
)
```

#### Use Cases

- Data quality validation
- Duplicate detection

### 10. BBOX (Bounding Box)

Very common in GeoServer.

Search within a rectangular area.

Conceptually:

```
BBOX(
   SP_GEOMETRY,
   minX,
   minY,
   maxX,
   maxY
)
```

#### Use Cases

- Map viewport searches
- Faster preliminary filtering
- Reducing result sets

### 11. Nearest Neighbour Search

GeoServer can support nearest-neighbour style searches.

Conceptually:

```
ORDER BY Distance
LIMIT 1
```

or

```
Sort by geometry distance
```

#### Use Cases

- Nearest grit bin
- Nearest hospital
- Nearest defibrillator

This is likely what the interviewers hope you'll discover.

### 12. Distance Calculation

Not technically a filter, but commonly used.

```
Distance(
   HILLBROW,
   GritBin
)
```

Produces:

- 23 metres
- 51 metres
- 125 metres

Then:

```
Select Minimum Distance
```

### 13. Buffer Search

Create a search circle around a location.

```
BUFFER(
   POINT(438123 356789),
   100
)
```

Then:

```
INTERSECTS(
    SP_GEOMETRY,
    BUFFER(...)
)
```

#### Use Cases

- Find nearby assets
- Emergency response zones
- Walking-distance searches

## If I Were Answering the Interview

I'd say:

For this requirement, the most appropriate spatial query is a WFS GetFeature request using a DWITHIN filter on SP_GEOMETRY with a 100-metre radius around the HILLBROW coordinates. This minimizes the result set, leverages GeoServer spatial indexing, and avoids retrieving unnecessary features. I would then calculate exact distances and return the grit bin with the shortest distance. For future reuse, the same pattern could support hospitals, schools, libraries, defibrillators, fire hydrants, bus stops, recycling centres, emergency shelters, pharmacies, EV charging points, and the nearest five assets by simply changing the layer and result limit.
