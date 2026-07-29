G11 Senior Developer (Integration) Interview Revision Notes
Quick Facts
Property: HILLBROW, DE55 5PB  
Nearest Grit Bin: GB0199  
Distance: ~49 metres  
Projection: EPSG:27700 (British National Grid)  
Layer: DCC:Gritbins  
Geometry Field: SP_GEOMETRY  
GeoServer Service: WFS (not WMS)  
WFS URL: `{GEOSERVER_BASE_URL}/DCC/ows`  
  (not in the brief — discovered by probing live GeoServer; see below)
---
30-Second Summary
Search Address Lookup API using postcode DE55 5PB.
Find the address record for HILLBROW.
Extract Easting/Northing (already EPSG:27700 — not a CRS convert).
Query GeoServer WFS using DWITHIN on SP_GEOMETRY.
Find grit bins within 100 metres.
Calculate distance and return the nearest grit bin.
Result: GB0199 at approximately 49 metres.
---
Architecture
```text
Browser
   |
   v
Next.js
   |
   v
FastAPI
   |
   +-------------------+
   |                   |
   v                   v
Address API      GeoServer WFS
                 …/DCC/ows
```
Backend Layers:
```text
Router
  ↓
Service
  ↓
Repository
  ↓
External APIs
```
---
Design Patterns (if asked)
Main pattern: layered architecture
Also: Repository, Service, DTO vs domain, DI, BFF proxy

```text
Router → Service → Repository → External APIs
```

| Pattern | Why here |
|---------|----------|
| Layered | Separate HTTP, rules, and upstream I/O |
| Repository | Address API / GeoServer HTTP only |
| Service | Match address, nearest bin — no FastAPI |
| DTO vs domain | JSON wire shape ≠ BNG value objects |
| DI (Depends) | Shared httpx client + settings |
| AppError mapping | Stable error.code for UI/tests |
| Next.js proxy | CORS + secrets stay server-side |

Panel line:
I used layered FastAPI with Repository and Service layers,
DTOs at the edge, and a Next.js server proxy so the browser
never calls Derbyshire APIs — testable and CORS-safe.

Rejected: fat controllers, browser-direct calls, one mega module.
Depth: copilotdocs.md § Design patterns
---
Key Decisions
Why WFS instead of WMS?
WMS:
Returns images
Used for map rendering
WFS:
Returns feature data
Returns geometry
Returns attributes
Supports spatial queries
Needed geometry and Title therefore WFS was chosen.
Why DWITHIN?
Spatial filtering happens on GeoServer
Reduces returned data
Suitable for "find assets within 100m"
Why EPSG:27700?
Native coordinate system of DCC:Gritbins
Uses metres
Makes distance calculations simple
Why FastAPI?
Separation of concerns
OpenAPI / Swagger support
Easy integration testing
Why Server Side?
Exercise forbids browser calls
Avoids CORS issues
Protects credentials
Where does /DCC/ows come from?
Not written in the assessment doc.
Env gives host root: https://wms.derbyshire.gov.uk/geoserver
Layer id DCC:Gritbins → workspace DCC
GeoServer convention: {base}/{workspace}/ows
Confirmed with live GetCapabilities / GetFeature
Settings builds: f"{GEOSERVER_BASE_URL}/DCC/ows"
GEOSERVER_LAYER only sets typeName=DCC:Gritbins
---
Investigation Process
Reviewed exercise requirements.
Called Address Lookup API (Postman + HTTP clients).
Confirmed postcode is the lookup key (URL path only).
Found HILLBROW record via BuildingName (no single Title field).
Composed postal line from NLPG parts + SpatialFeature coords.
Investigated GeoServer (research task from the brief).
Determined WFS was required (not WMS).
Discovered WFS path /DCC/ows (brief silent on this path).
Identified:
Layer: DCC:Gritbins
Geometry: SP_GEOMETRY
Projection: EPSG:27700
Implemented DWITHIN query.
Verified returned grit bin independently (upstream vs downstream in Postman).
---
Address API → postal line (quick)
Lookup key: postcode in URL (…/Address/DE55%205PB).
Property id: UPRN.
No FullAddress — join BuildingName / OrganisationName / street /
locality / town / PostCode.
Hillbrow → HILLBROW, ALFRETON ROAD, TIBSHELF, ALFRETON, DE55 5PB
Hint HILLBROW matches BuildingName (case-insensitive).
Coords: SpatialFeature.Eastings / Northings (already EPSG:27700).
Also present: Longitude / Latitude (EPSG:4326) — prefer BNG; convert only if BNG missing.
---
Postman (upstream vs downstream)
Upstream: Derbyshire Address API (raw JSON for DE55 5PB).
Downstream: Health, /addresses, nearest-grit-bin, nearest-grit-bins.
Compare BuildingName:HILLBROW row with our cleaned API / GB0199 result.
---
Assumptions
Address API returns valid address data.
HILLBROW exists in DE55 5PB results.
Eastings/Northings under SpatialFeature are already EPSG:27700 (lon/lat fallback only).
Grit bins expose a Title attribute.
Default search radius is 100 metres.
WFS lives at workspace OWS path /DCC/ows on the Derbyshire host.
---
Approaches Rejected
Browser Direct Integration
Rejected because:
Exercise prohibits it
CORS restrictions
Credential exposure
WMS
Rejected because it returns images rather than feature data.
Download Entire Layer
Rejected as primary approach because:
Excessive data transfer
Poor scalability
Unnecessary processing
Preferred approach:
DWITHIN
Spatial filtering
Smaller result sets
---
Interview Questions to Expect
What design pattern did you use?
Layered architecture with Repository + Service, DTO vs domain,
FastAPI Depends for DI, and a Next.js BFF-style proxy.
Why not put everything in the router?
Harder to test; mixes HTTP with spatial/business rules;
harder to reuse for nearest-5 or other asset types.
Why WFS instead of WMS?
Because WFS returns geometry and attributes. WMS returns images.
Where did you get /DCC/ows? It is not in the brief.
From GeoServer workspace URL conventions + live probing of
https://wms.derbyshire.gov.uk/geoserver — layer DCC:Gritbins implies workspace DCC.
What is EPSG:27700?
British National Grid coordinate system used by the layer.
Why “convert” Eastings if Lon/Lat are also returned?
Eastings/Northings already are EPSG:27700 — we extract/wrap them as a BNG point.
Lon/Lat are EPSG:4326 degrees; wrong units for metre DWITHIN / Euclidean.
ensure_bng prefers Eastings/Northings; pyproj lon/lat→BNG only if BNG missing.
Why use DWITHIN?
To allow GeoServer to perform spatial filtering.
What is SP_GEOMETRY?
The geometry field containing grit bin locations.
Why calculate distance locally?
To independently verify and rank returned candidates.
Why not call GeoServer from JavaScript?
CORS restrictions and credential security.
How would you return the nearest 5 grit bins?
Sort by distance and return top 5.
How would you support other assets?
Introduce assetType → layer mapping.
How would you process 100,000 addresses?
CSV → Queue → Worker → Results.
---
Issues Encountered
Address API Has No Single Title Field
Found:
BuildingName
SpatialFeature.Eastings / Northings (EPSG:27700 — use these)
SpatialFeature.Longitude / Latitude (EPSG:4326 — present but not preferred)
Solution:
Match across address components; wrap Eastings/Northings as Point27700 (no CRS convert).
Invalid Postcodes Return HTTP 200 + XML
Solution:
Validate postcode first.
Detect XML error responses.
WFS Path Not Documented In Brief
Found via:
Workspace from DCC:Gritbins
GeoServer /{workspace}/ows pattern
Live GetFeature probe
Solution:
Hard-code /DCC/ows onto GEOSERVER_BASE_URL in settings.
Geometry Field Is Not the_geom
Solution:
Use SP_GEOMETRY.
DWITHIN Validation
Observed:
Empty results in some scenarios.
Exercise fallback:
Validate against wider dataset.
Production preference:
Expanding-radius searches
Nearest-neighbour queries
Spatial indexing
PostGIS
---
Verification
Verified by:
Resolving HILLBROW from Address API.
Extracting coordinates.
Executing GeoServer query on …/DCC/ows.
Confirming GB0199.
Calculating distance independently.
Result:
```text
Property: HILLBROW
Postcode: DE55 5PB
Nearest Grit Bin: GB0199
Distance: ~49 metres
```
---
References (GeoServer path)
GeoServer WFS: https://docs.geoserver.org/maintain/en/user/services/wfs/reference.html
Virtual / workspace services: https://docs.geoserver.org/maintain/en/user/services/virtual-services.html
Live host: https://wms.derbyshire.gov.uk/geoserver
GetCapabilities smoke:
https://wms.derbyshire.gov.uk/geoserver/DCC/ows?service=WFS&version=1.0.0&request=GetCapabilities
Public example of Derbyshire /DCC/ows WFS:
https://sourceforge.net/p/geoserver/mailman/message/58756516/
Full narrative: submission-notes.md · depth: copilotdocs.md
---
Improvements With More Time
Technical
API versioning
Correlation IDs
Better telemetry
Structured logging
Cached responses
Functional
Asset type support
Map visualisation
Nearest-N searches
Batch processing
Scalability
Redis caching
Spatial indexing
PostGIS
Nearest-neighbour database queries
---
Monitoring and Resilience
Current:
Health endpoint
Timeouts
Automated tests
Future:
Retries
Circuit breakers
Application Insights
Distributed tracing
Alerting
---
Follow-Up Discussion Answers
Other Asset Types
Schools
Libraries
Hospitals
Defibrillators
Car Parks
Bus Stops
Fire Hydrants
Recycling Centres
Large Batch Processing
```text
CSV
  ↓
Queue
  ↓
Worker
  ↓
Address Lookup
  ↓
GeoServer Query
  ↓
Results File
```
Making It Available To Other Teams
REST API
OpenAPI
Swagger
Versioned endpoints
---
Final Talking Point
The exercise was not just about finding a grit bin. It was about demonstrating investigation, integration, spatial reasoning, GeoServer research (including discovering /DCC/ows when the brief omitted it), error handling, architecture decisions, and the ability to build a reusable GIS asset lookup service.
