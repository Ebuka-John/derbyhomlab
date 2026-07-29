# Backend 5 — Domain, DTO & geospatial

## Concept

- **Domain** — shapes used inside services (`ResolvedAddress`, `Point27700`, `GritBinMatch`).
- **DTO** — Pydantic models for OpenAPI / responses (`NearestGritBinResponse`, …).
- **Geospatial (`pyproj`)** — work in **EPSG:27700** (metres): convert CRS, planar
  distance, pick nearest GeoJSON feature(s).

GeoServer filters with `DWITHIN` on **`SP_GEOMETRY`** (not `the_geom`).

## Type these files (one at a time)

### Domain first

| # | Create in lab | Type from reference |
|--:|---------------|---------------------|
| 1 | `src/models/domain/geometry.py` | `src/models/domain/geometry.py` |
| 2 | `src/models/domain/address.py` | `src/models/domain/address.py` |
| 3 | `src/models/domain/gritbin.py` | `src/models/domain/gritbin.py` |

### Then geospatial (imports domain)

| # | Create in lab | Type from reference |
|--:|---------------|---------------------|
| 4 | `src/utils/geospatial.py` | `src/utils/geospatial.py` |

### DTOs

| # | Create in lab | Type from reference |
|--:|---------------|---------------------|
| 5 | `src/models/dto/address.py` | `src/models/dto/address.py` |
| 6 | `src/models/dto/gritbin.py` | `src/models/dto/gritbin.py` |

## Checkpoint

Do **not** continue to the next lesson until this passes.


```powershell
.\.venv\Scripts\Activate.ps1
python -c "from src.models.domain.geometry import Point27700; from src.utils.geospatial import euclidean_distance_meters; from src.models.dto.gritbin import NearestGritBinResponse; print('models ok')"
```

## Deeper reading

- [06-coordinates.md (main)](https://github.com/Ebuka-John/derbyhomlab/blob/main/tutorial/backend/06-coordinates.md)
- [10-spatial-querying.md (main)](https://github.com/Ebuka-John/derbyhomlab/blob/main/tutorial/10-spatial-querying.md)
- This branch: [lfdocs/copilotdocs.md](../../lfdocs/copilotdocs.md)

---

| Previous | Next |
|:---------|-----:|
| ← [Errors](./04-errors-utils.md) | [Repositories](./06-repositories.md) → |
