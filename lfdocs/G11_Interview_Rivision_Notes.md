G11 Senior Developer (Integration) Interview Revision Notes
Quick Facts
Property: HILLBROW, DE55 5PB  
Nearest Grit Bin: GB0199  
Distance: ~49 metres  
Projection: EPSG:27700 (British National Grid)  
Layer: DCC:Gritbins  
Geometry Field: SP_GEOMETRY  
GeoServer Service: WFS (not WMS)
---
30-Second Summary
Search Address Lookup API using postcode DE55 5PB.
Find the address record for HILLBROW.
Extract Easting/Northing coordinates.
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
---
Investigation Process
Reviewed exercise requirements.
Called Address Lookup API.
Confirmed postcode is the lookup key.
Found HILLBROW record.
Investigated GeoServer.
Determined WFS was required.
Identified:
Layer: DCC:Gritbins
Geometry: SP_GEOMETRY
Projection: EPSG:27700
Implemented DWITHIN query.
Verified returned grit bin independently.
---
Assumptions
Address API returns valid address data.
HILLBROW exists in DE55 5PB results.
Coordinates are available or convertible to EPSG:27700.
Grit bins expose a Title attribute.
Default search radius is 100 metres.
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
Why WFS instead of WMS?
Because WFS returns geometry and attributes. WMS returns images.
What is EPSG:27700?
British National Grid coordinate system used by the layer.
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
SpatialFeature.Eastings
SpatialFeature.Northings
Solution:
Match across address components.
Invalid Postcodes Return HTTP 200 + XML
Solution:
Validate postcode first.
Detect XML error responses.
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
Executing GeoServer query.
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
The exercise was not just about finding a grit bin. It was about demonstrating investigation, integration, spatial reasoning, GeoServer research, error handling, architecture decisions, and the ability to build a reusable GIS asset lookup service.