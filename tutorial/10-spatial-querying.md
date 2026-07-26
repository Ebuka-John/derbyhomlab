# 10. Spatial querying — the geospatial reasoning behind this project

This is the **unique part of the Derbyshire exercise**. Most candidates can wire
a form to an API; the differentiator is whether you can **reason about
geospatial data**: coordinate systems, spatial services, spatial filters, and
what to do when the smart path fails.

This page explains the five concepts the exercise tests, where each one lives in
the codebase, and where to study further. It assumes you have read
[09-sources-and-references.md](./09-sources-and-references.md) §1 (domain
background) but repeats the essentials so it stands alone.

The five concepts:

| # | Concept | One-line summary |
|---|---------|------------------|
| 1 | [EPSG:27700](#1-epsg27700--british-national-grid) | The metre-based UK grid everything is normalised to |
| 2 | [WFS vs WMS](#2-wfs-vs-wms--data-vs-pictures) | Ask for **data** (features), not **pictures** (tiles) |
| 3 | [CQL DWITHIN](#3-cql-dwithin--server-side-spatial-filtering) | Let GeoServer filter "within 100 m" for you |
| 4 | [Euclidean fallback](#4-manual-euclidean-distance-fallback) | Compute distance yourself when DWITHIN misbehaves |
| 5 | [SP_GEOMETRY extraction](#5-geometry-extraction-from-sp_geometry) | Pull easting/northing out of each GeoJSON feature |

---

## 1. EPSG:27700 — British National Grid

### What it is

A **coordinate reference system (CRS)** is a convention for turning positions on
the curved Earth into numbers. Two matter here:

| CRS | Name | Units | Axes | Used by |
|-----|------|-------|------|---------|
| **EPSG:27700** | British National Grid (BNG) | **metres** | easting, northing | UK council GIS layers, incl. `DCC:Gritbins` |
| **EPSG:4326** | WGS84 | **degrees** | longitude, latitude | GPS, Google Maps, most web APIs |

EPSG:27700 is a **projected** CRS: the UK is flattened onto a plane (a Transverse
Mercator projection tuned for Great Britain), and every point gets an
**easting** (metres east of a false origin) and a **northing** (metres north).
A grit bin near Alfreton might be roughly `easting=440000, northing=355000`.

### Why the exercise cares

The brief asks for grit bins "within ~100 **metres**". That question is only
natural in a metre-based CRS:

- In EPSG:27700, "100 metres" is literally 100 units on both axes — subtraction
  works.
- In EPSG:4326, 0.001° of longitude is a *different number of metres* depending
  on latitude. Naive degree arithmetic gives wrong distances, and mixing
  degrees with a metre-based layer gives nonsense.

So the rule in this project is: **normalise everything to EPSG:27700 before any
distance work**. The Address API may return either BNG easting/northing or
WGS84 lat/lon; `ensure_bng` in `src/utils/coordinates.py` accepts both and
converts lat/lon via **pyproj** (see
[backend/06-coordinates.md](./backend/06-coordinates.md)).

### Interview-ready sentence

> "The grit-bin layer is published in EPSG:27700 — British National Grid, in
> metres — so I reproject the address to the same CRS with pyproj, and then
> planar distance and metre-based radii are both valid."

### Study further

- EPSG registry entry for 27700: https://epsg.io/27700
- EPSG registry entry for 4326: https://epsg.io/4326
- Ordnance Survey — *A guide to coordinate systems in Great Britain*:
  https://www.ordnancesurvey.co.uk/documents/resources/guide-coordinate-systems-great-britain.pdf
- pyproj documentation (the conversion library used here):
  https://pyproj4.github.io/pyproj/stable/
- General intro to map projections and CRSs (QGIS docs, very readable):
  https://docs.qgis.org/latest/en/docs/gentle_gis_introduction/coordinate_reference_systems.html

---

## 2. WFS vs WMS — data vs pictures

### What they are

GeoServer (and any OGC-compliant map server) speaks several protocols. The two
you must be able to tell apart:

| Protocol | Stands for | Returns | Good for |
|----------|-----------|---------|----------|
| **WMS** | Web **Map** Service | Rendered map **images** (PNG/JPEG tiles) | Displaying a basemap in a UI |
| **WFS** | Web **Feature** Service | The **features themselves** — geometry + attributes, e.g. GeoJSON | Querying, filtering, computing with the data |

A WMS response is pixels — you cannot ask a PNG "which grit bin is closest?".
A WFS `GetFeature` response is structured data you can filter and iterate.

### The trap in this exercise

The Derbyshire host is literally named `wms.derbyshire.gov.uk` — but to find the
nearest grit bin you need **WFS**, because you need coordinates and titles, not
tiles. The hostname is a red herring (see
[`docs/issues-encountered.md`](../docs/issues-encountered.md)).

The request this project sends (built in `_base_params()` in
`src/services/geoserver_service.py`):

```text
{GEOSERVER_BASE_URL}/DCC/ows
  ?service=WFS
  &version=1.0.0
  &request=GetFeature
  &typeName=DCC:Gritbins
  &outputFormat=application/json
```

`request=GetFeature` + `outputFormat=application/json` → GeoJSON features.
To discover what a server offers in the first place, use
`request=GetCapabilities`.

### Interview-ready sentence

> "WMS returns rendered map images and WFS returns the underlying features. I
> need coordinates and attributes to compute a nearest match, so I use WFS
> GetFeature with a GeoJSON output format — even though the host is named
> `wms.`"

### Study further

- OGC WFS standard overview: https://www.ogc.org/standard/wfs/
- OGC WMS standard overview: https://www.ogc.org/standard/wms/
- GeoServer WFS reference (all operations, incl. GetFeature):
  https://docs.geoserver.org/latest/en/user/services/wfs/reference.html
- GeoServer WMS reference (for contrast):
  https://docs.geoserver.org/latest/en/user/services/wms/reference.html
- GeoJSON spec (the output format): https://datatracker.ietf.org/doc/html/rfc7946

---

## 3. CQL DWITHIN — server-side spatial filtering

### What it is

**CQL** (Common Query Language, extended by GeoServer as **ECQL**) is a
human-readable filter language you attach to a WFS request with the
`CQL_FILTER` parameter. It supports attribute filters (`Title = 'GB0199'`) and
**spatial predicates**, of which the exercise-relevant one is:

```text
DWITHIN(SP_GEOMETRY, POINT(440000 355000), 100, meters)
```

Read it as: *"return features whose `SP_GEOMETRY` lies within 100 metres of the
point easting=440000, northing=355000."*

Details that trip people up:

- `POINT(x y)` is **WKT** (Well-Known Text) and the order is **x y = easting
  northing** in the layer's CRS. In WGS84 contexts that would be lon/lat — a
  classic axis-order bug.
- The point must be expressed in the **layer's CRS** (EPSG:27700 here) — another
  reason to reproject the address first.
- The whole filter is URL-encoded into a query parameter.

This is `query_dwithin` in `src/services/geoserver_service.py`
(see [backend/08-geoserver-service.md](./backend/08-geoserver-service.md)).

### Why it is preferred

DWITHIN pushes the spatial work to the server: GeoServer uses its spatial index
and returns only matching features. The alternative — downloading the whole
layer — transfers every grit bin in Derbyshire on each request. For one county
layer that is tolerable; for a big layer it is not. Preferring the server-side
filter shows you think about **where computation should happen**.

### Interview-ready sentence

> "I filter server-side with a CQL DWITHIN predicate — point-in-layer-CRS, a
> 100-metre radius — so GeoServer's spatial index does the work and I only
> download candidate features."

### Study further

- GeoServer CQL/ECQL tutorial (start here):
  https://docs.geoserver.org/latest/en/user/tutorials/cql/cql_tutorial.html
- ECQL reference (full grammar, all spatial predicates — DWITHIN, INTERSECTS,
  WITHIN, BBOX…):
  https://docs.geoserver.org/latest/en/user/filter/ecql_reference.html
- GeoServer filtering overview:
  https://docs.geoserver.org/latest/en/user/filter/filter_reference.html
- WKT geometry notation (what `POINT(x y)` is):
  https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry

---

## 4. Manual Euclidean distance fallback

### What it is

If DWITHIN cannot be used, do the query client-side:

1. Fetch **all** features from the layer (unfiltered `GetFeature`).
2. For each feature, compute the planar distance to the address point.
3. Keep the closest one within the radius; if none qualifies, report "no grit
   bin nearby".

Because both points are in EPSG:27700 (metres on a flat grid), the distance is
plain Pythagoras:

\[
d = \sqrt{(e_1 - e_2)^2 + (n_1 - n_2)^2}
\]

In code that is one line — `math.hypot(a.easting - b.easting,
a.northing - b.northing)` in `euclidean_distance_meters`
([backend/06-coordinates.md](./backend/06-coordinates.md)) — and the
"best-so-far" loop is `nearest_from_features`
([backend/08-geoserver-service.md](./backend/08-geoserver-service.md)).

### Why a fallback exists at all

Live GeoServer installs are imperfect:

- Some disable or misconfigure spatial predicates, returning an **OGC
  ExceptionReport** (XML) instead of GeoJSON — sometimes with HTTP 200.
- A CRS mismatch can make DWITHIN silently return **zero** features even when a
  bin is 49 m away.

So `find_nearest` tries DWITHIN first and falls back to full-fetch + Euclidean
when the filter errors *or* comes back empty. Designing a plan B for an
external dependency is exactly the judgement the interviewer is probing.

### Why Euclidean and not Haversine?

**Haversine** computes great-circle distance from lat/lon on a sphere. It is
the right tool for raw WGS84 coordinates — but here everything is already
projected to a planar, metre-based grid, so Pythagoras is simpler and accurate
at this scale (BNG distortion is centimetres-per-hundred-metres territory).
Using Haversine on easting/northing values would be flat-out wrong; using it on
lat/lon while the layer is in BNG means you never needed to reproject —
defensible, but this project standardises on one CRS instead (see
[`docs/investigation-notes.md`](../docs/investigation-notes.md)).

### Interview-ready sentence

> "DWITHIN is the happy path, but live GeoServers can reject or silently drop
> spatial filters, so I fall back to fetching the layer and computing planar
> Euclidean distance — valid because both points are already in EPSG:27700
> metres, so I don't need Haversine."

### Study further

- Euclidean distance: https://en.wikipedia.org/wiki/Euclidean_distance
- Haversine formula (for contrast, and to explain *why not* here):
  https://en.wikipedia.org/wiki/Haversine_formula
- Python `math.hypot`: https://docs.python.org/3/library/math.html#math.hypot
- Movable Type's classic lat/lon distance write-up (great mental model for
  spherical vs planar): https://www.movable-type.co.uk/scripts/latlong.html
- OGC exception handling in GeoServer (why 200-with-XML happens):
  https://docs.geoserver.org/latest/en/user/services/wfs/vendor.html

---

## 5. Geometry extraction from SP_GEOMETRY

### What it is

`SP_GEOMETRY` is the name of the **geometry column** in the `DCC:Gritbins`
layer — the field that stores each bin's point. The name comes from the
council's underlying spatial database (many vendor GIS schemas use
`SP_GEOMETRY` / `GEOM` / `SHAPE` instead of the common default
`the_geom`). You use the name in two different places, in two different ways:

**In the CQL filter** you reference it by name, because DWITHIN needs to know
*which* column to test:

```text
DWITHIN(SP_GEOMETRY, POINT(440000 355000), 100, meters)
```

Using `the_geom` here — the default many tutorials show — fails on this layer.
Discovering the real column name (from `GetFeature` output or
`DescribeFeatureType`) is part of the exercise's investigation work.

**In the GeoJSON response** the geometry is *not* under a property called
`SP_GEOMETRY` — GeoServer maps the geometry column to the standard GeoJSON
`geometry` member:

```json
{
  "type": "Feature",
  "id": "Gritbins.123",
  "geometry": { "type": "Point", "coordinates": [440010.0, 355000.0] },
  "properties": { "Title": "GB0199", "...": "..." }
}
```

`coordinates` is `[easting, northing]` (x, y — in the layer CRS). The
extraction code is `_feature_point` in `src/services/geoserver_service.py`: it
defensively checks that `coordinates` is a list of at least two numbers before
building a `Point27700`, because live layers can contain malformed or empty
geometries.

### Interview-ready sentence

> "The layer's geometry column is `SP_GEOMETRY` — I reference it by name in the
> DWITHIN filter, but in the GeoJSON output it appears as the standard
> `geometry.coordinates` pair, which I parse as easting/northing with
> defensive type checks."

### Study further

- GeoJSON `geometry` / `Feature` structure (RFC 7946 §3):
  https://datatracker.ietf.org/doc/html/rfc7946#section-3
- WFS `DescribeFeatureType` (how to discover a layer's schema and geometry
  column name):
  https://docs.geoserver.org/latest/en/user/services/wfs/reference.html#describefeaturetype
- GeoServer GeoJSON output format:
  https://docs.geoserver.org/latest/en/user/services/wfs/outputformats.html
- This project's discovery trail:
  [`docs/investigation-notes.md`](../docs/investigation-notes.md) and
  [`docs/issues-encountered.md`](../docs/issues-encountered.md)

---

## How the five concepts fit together

One request through the system touches all five, in order:

```
postcode + address
   │
   ▼
Address API → coordinates (BNG or lat/lon)
   │
   ▼
[1] Normalise to EPSG:27700  (pyproj, ensure_bng)
   │
   ▼
[2] WFS GetFeature against DCC:Gritbins  (not WMS!)
   │
   ▼
[3] CQL_FILTER=DWITHIN(SP_GEOMETRY, POINT(e n), 100, meters)
   │
   ├─ works → candidate features
   └─ fails / empty
         │
         ▼
      [4] fetch all features → planar Euclidean distance loop
   │
   ▼
[5] extract geometry.coordinates from each feature → nearest GritBinMatch
```

Where each concept lives:

| Concept | Code | Lab step |
|---------|------|----------|
| EPSG:27700 + conversion | `src/utils/coordinates.py` | [backend/06-coordinates.md](./backend/06-coordinates.md) |
| WFS request params | `GeoServerService._base_params` | [backend/08-geoserver-service.md](./backend/08-geoserver-service.md) |
| CQL DWITHIN | `GeoServerService.query_dwithin` | [backend/08-geoserver-service.md](./backend/08-geoserver-service.md) |
| Euclidean fallback | `find_nearest` + `nearest_from_features` | [backend/08-geoserver-service.md](./backend/08-geoserver-service.md) |
| SP_GEOMETRY extraction | `_feature_point` | [backend/08-geoserver-service.md](./backend/08-geoserver-service.md) |

---

## Self-check before an interview

You are ready when you can answer these without notes:

1. Why is "within 100 metres" a meaningful question in EPSG:27700 but not in
   EPSG:4326?
2. You have a WMS endpoint and a WFS endpoint for the same layer. Which do you
   query to find the nearest feature, and why?
3. Write the CQL filter for "features within 250 m of easting 430500,
   northing 362200" from memory.
4. DWITHIN returns zero features but you know a bin is ~50 m away. Name two
   plausible causes and what your code should do next.
5. In the GeoJSON response, where do you find a grit bin's coordinates, and in
   what axis order?

(Answers are all on this page: §1, §2, §3, §4, §5 respectively.)

---

## Next

- Apply it: [07-derbyshire-exercise.md](./07-derbyshire-exercise.md)
- Full link library: [09-sources-and-references.md](./09-sources-and-references.md)
