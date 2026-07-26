# Backend Step 6 — Coordinates

## What you will do

1. Create the file below.
2. Type the code carefully (or type section by section).
3. Run the checkpoint before continuing.

## File to create: `src/utils/coordinates.py`

**Path:** `src/utils/coordinates.py`

### Purpose

Converts between WGS84 (lat/lon) and British National Grid (EPSG:27700), and computes planar distance in metres.

### Type this exactly

```python
"""Coordinate conversion and planar distance helpers.

UK local-authority geospatial layers (including Derbyshire GeoServer grit bins)
are published in British National Grid — EPSG:27700. Address APIs may return
either BNG easting/northing or WGS84 lat/lon (EPSG:4326).

We normalise everything to EPSG:27700 before spatial queries so that:
  - DWITHIN(... meters) is meaningful
  - Euclidean distance approximates true ground distance (planar projection)
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal

from pyproj import Transformer

from src.utils.errors import CoordinateConversionError

CrsCode = Literal["EPSG:27700", "EPSG:4326"]

# Lazily built transformers are expensive; cache module-level instances.
_to_bng = Transformer.from_crs("EPSG:4326", "EPSG:27700", always_xy=True)
_to_wgs84 = Transformer.from_crs("EPSG:27700", "EPSG:4326", always_xy=True)


@dataclass(frozen=True, slots=True)
class Point27700:
    """A point in British National Grid metres (easting, northing)."""

    easting: float
    northing: float


@dataclass(frozen=True, slots=True)
class Point4326:
    """A point in WGS84 degrees (longitude, latitude) — always_xy order."""

    longitude: float
    latitude: float


def lonlat_to_bng(longitude: float, latitude: float) -> Point27700:
    """Convert WGS84 lon/lat (EPSG:4326) → BNG easting/northing (EPSG:27700)."""
    try:
        easting, northing = _to_bng.transform(longitude, latitude)
    except Exception as exc:  # pragma: no cover - pyproj raises varied types
        raise CoordinateConversionError(str(exc)) from exc
    return Point27700(easting=float(easting), northing=float(northing))


def bng_to_lonlat(easting: float, northing: float) -> Point4326:
    """Convert BNG easting/northing (EPSG:27700) → WGS84 lon/lat (EPSG:4326)."""
    try:
        longitude, latitude = _to_wgs84.transform(easting, northing)
    except Exception as exc:  # pragma: no cover
        raise CoordinateConversionError(str(exc)) from exc
    return Point4326(longitude=float(longitude), latitude=float(latitude))


def ensure_bng(
    *,
    easting: float | None = None,
    northing: float | None = None,
    latitude: float | None = None,
    longitude: float | None = None,
) -> Point27700:
    """Return a BNG point from whichever coordinate pair is available.

    Preference order:
      1. Explicit easting/northing (already EPSG:27700)
      2. lat/lon converted via pyproj
    """
    if easting is not None and northing is not None:
        return Point27700(easting=float(easting), northing=float(northing))

    if latitude is not None and longitude is not None:
        return lonlat_to_bng(float(longitude), float(latitude))

    raise CoordinateConversionError(
        "Need either easting/northing or latitude/longitude."
    )


def euclidean_distance_meters(a: Point27700, b: Point27700) -> float:
    """Planar Euclidean distance in metres (valid for EPSG:27700)."""
    return math.hypot(a.easting - b.easting, a.northing - b.northing)


def detect_crs_from_values(
    x: float,
    y: float,
) -> CrsCode:
    """Heuristic CRS detection when the payload does not declare an SRS.

    BNG eastings are typically ~100_000–700_000 and northings ~0–1_300_000.
    WGS84 lon is roughly -8..2 and lat 49..61 for the UK.
    """
    # Lon/lat ranges for the British Isles (with a small margin)
    if -10.0 <= x <= 5.0 and 49.0 <= y <= 62.0:
        return "EPSG:4326"
    if 0.0 <= x <= 800_000 and -100_000 <= y <= 1_400_000:
        return "EPSG:27700"
    raise CoordinateConversionError(
        f"Unable to infer CRS for coordinates ({x}, {y})."
    )
```

### How the code works

#### Concepts in this file

| Concept | Where | Plain meaning |
|---------|-------|---------------|
| **`@dataclass`** | `Point27700`, `Point4326` | Auto-builds `__init__` so you don’t write boilerplate. Still a class/object. |
| **`frozen=True`** | dataclass option | Points are immutable — once created, easting/northing cannot change. Safer for coordinates. |
| **Named types vs tuples** | `Point27700` instead of `(x, y)` | Stops you mixing up order (“was x easting or lon?”). |
| **Module-level constants** | `_to_bng`, `_to_wgs84` | Created once when the file loads. Transformers are expensive; reuse them. |
| **`|` in types** | `float \| None` | Means “a float **or** None”. Older style was `Optional[float]`. |
| **Keyword-only args** | `ensure_bng(*, easting=…)` | Callers must name arguments, so you can’t swap lat/lon by accident. |
| **Pure functions** | `euclidean_distance_meters` | Take inputs, return a result, no hidden state. Easy to test. |

#### What the code is doing

1. UK map layers (grit bins) use **British National Grid** — metres east/north (EPSG:27700).
2. Some APIs return **lat/lon** degrees (EPSG:4326) instead.
3. `ensure_bng` normalises either flavour into a `Point27700`.
4. Distance is then simple Pythagoras (`math.hypot`) because BNG is already in metres.

> Why OOP here? A bare `(440000, 355000)` is easy to misuse. A `Point27700` object
> documents what the numbers mean. Primer: [00-python-fastapi-basics.md](./00-python-fastapi-basics.md) §4.

## Checkpoint

```powershell
python -c "from src.utils.coordinates import euclidean_distance_meters as d, Point27700 as P; print(d(P(0,0), P(3,4)))"
```
Expected: `5.0`

---

<!-- tutorial-nav -->

| Previous | Next |
|:---------|-----:|
| ← [Errors](./05-errors.md) | [Address service](./07-address-service.md) → |
