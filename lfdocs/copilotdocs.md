# For a G11 Senior Developer (Integration) exercise

I'd present pseudocode at service level, integration level, and business flow level. The objective is to show architecture, separation of concerns, maintainability, error handling, and scalability.

## Solution Architecture

```
FastAPI Endpoint
       |
       v
Nearest Asset Service
       |
       +------------------+
       |                  |
       v                  v
Address API         GeoServer WFS
       |                  |
       +--------+---------+
                |
                v
      Spatial Distance Logic
                |
                v
         Return Grit Bin Title
```

## Main Business Flow

```
FUNCTION FindNearestGritBin()

    postcode = "DE55 5PB"
    propertyName = "HILLBROW"
    searchRadius = 100

    addressRecord =
        AddressService.GetAddress(
            postcode,
            propertyName
        )

    IF addressRecord IS NULL THEN

        RETURN
        {
            success: false,
            error: "Address not found"
        }

    END IF

    gritBins =
        GeoServerService.FindNearbyAssets(
            layer = "DCC:Gritbins",
            geometryField = "SP_GEOMETRY",
            easting = addressRecord.easting,
            northing = addressRecord.northing,
            radius = searchRadius
        )

    IF gritBins IS EMPTY THEN

        RETURN
        {
            success: false,
            error: "No grit bins found within 100 metres"
        }

    END IF

    nearestBin =
        SpatialService.FindNearest(
            addressRecord,
            gritBins
        )

    RETURN
    {
        success: true,
        title: nearestBin.Title,
        distance: nearestBin.Distance
    }

END FUNCTION
```

## Address Service

### Responsibility

- Query Address API
- Find HILLBROW record
- Extract Easting/Northing

```
FUNCTION GetAddress(
    postcode,
    propertyName
)

    url =
    ADDRESS_API +
    UrlEncode(postcode)

    response =
    HttpGet(
        url,
        requiredHeaders
    )

    IF response.status != 200 THEN

        THROW
        AddressApiException

    END IF

    addresses =
    ParseJson(response)

    FOR EACH address IN addresses

        IF
        ToUpper(address.description)
        CONTAINS
        ToUpper(propertyName)

            RETURN
            {
                easting : address.Easting,
                northing : address.Northing,
                description : address.description
            }

        END IF

    END FOR

    RETURN NULL

END FUNCTION
```

## GeoServer Service

### Why WFS?

Not WMS.

- **WMS:** Returns Images
- **WFS:** Returns Features

We need actual geometry and attributes.

### GeoServer Query

```
FUNCTION FindNearbyAssets(
    layer,
    geometryField,
    easting,
    northing,
    radius
)

    build WFS query

    GeoServerUrl =
    "/geoserver/wfs"

    parameters =

        service = WFS
        version = 2.0.0
        request = GetFeature
        typeNames = DCC:Gritbins
        outputFormat = application/json

        cql_filter =

            DWITHIN(
                SP_GEOMETRY,
                POINT(easting northing),
                radius,
                meters
            )

    response =
        HttpGet(
            GeoServerUrl,
            parameters
        )

    IF response.status != 200 THEN

        THROW GeoServerException

    END IF

    RETURN ParseGeoJson(response)

END FUNCTION
```

## Spatial Service

Although GeoServer can perform some proximity filtering, I would still calculate distances in the service to guarantee correctness.

```
FUNCTION FindNearest(
    address,
    gritBins
)

    shortestDistance =
        INFINITY

    nearestBin =
        NULL

    FOR EACH gritBin IN gritBins

        binX =
            gritBin.SP_GEOMETRY.X

        binY =
            gritBin.SP_GEOMETRY.Y

        distance =
            CalculateDistance(
                address.easting,
                address.northing,
                binX,
                binY
            )

        IF distance < shortestDistance

            shortestDistance =
                distance

            nearestBin =
                gritBin

        END IF

    END FOR

    nearestBin.Distance =
        shortestDistance

    RETURN nearestBin

END FUNCTION
```

## Distance Formula

Because EPSG:27700 uses metres:

```
FUNCTION CalculateDistance(
    x1,
    y1,
    x2,
    y2
)

    dx = x2 - x1
    dy = y2 - y1

    RETURN
        SQRT(
            dx² + dy²
        )

END FUNCTION
```

## FastAPI Endpoint Pseudocode

```
GET /api/v1/gritbins/nearest

TRY

    result =
        FindNearestGritBin()

    RETURN 200

CATCH AddressNotFoundException

    RETURN 404

    {
        error:
        "Address not found"
    }

CATCH NoGritBinsFoundException

    RETURN 404

    {
        error:
        "No grit bins found"
    }

CATCH GeoServerException

    RETURN 503

    {
        error:
        "GeoServer unavailable"
    }

CATCH Exception

    LogError()

    RETURN 500

END TRY
```

## Production Version (Reusable Design)

Instead of:

```
FindNearestGritBin()
```

I'd create:

```
FindNearestAsset()
```

```
GET /api/v1/assets/nearest
?postcode=DE55 5PB
&property=HILLBROW
&assetType=gritbin
```

### Asset mappings:

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

## Error Handling

### Address API Failure

```json
{
  "success": false,
  "error": "Address lookup service unavailable"
}
```

### HILLBROW Not Found

```json
{
  "success": false,
  "error": "Property HILLBROW not found in postcode DE55 5PB"
}
```

### Missing Coordinates

```json
{
  "success": false,
  "error": "Address record contains no coordinates"
}
```

### No Nearby Grit Bin

```json
{
  "success": false,
  "error": "No grit bin found within 100 metres"
}
```

### GeoServer Failure

```json
{
  "success": false,
  "error": "Unable to query GeoServer"
}
```

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

Rejected because:

- Poor performance
- Unnecessary network traffic
- Poor scalability

Instead:

- Spatial query against GeoServer

### Verification:

- Confirm HILLBROW coordinates.
- Execute WFS query.
- Verify returned grit bin location.
- Calculate distance independently.
- Check nearest returned bin.

## Follow-Up Discussion Answers

### Nearest 5 Grit Bins

### Follow-Up Discussion Answers

### Nearest 5 Grit Bins

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
