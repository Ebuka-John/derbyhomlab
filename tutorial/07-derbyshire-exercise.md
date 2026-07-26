# 7. How this lab prepares you for the Derbyshire technical exercise

## What you will do

Use what you built as a springboard for interview-style changes.

## You can now modify the project confidently

| Change | Where to edit |
|--------|----------------|
| Custom search radius | Query param in `api/routers/gritbins.py` → pass to `GritBinService.find_nearest` → optional UI field + proxy |
| Different response fields | `models/dto/gritbin.py` **and** `frontend/lib/types.ts` together |
| New error case | Add subclass in `utils/exceptions.py` (handler in `app.py` already covers `AppError`) |

## Integrating real API calls

1. Put live credentials in root `.env`
2. Keep parsing tolerant (`_*_KEYS` in `address_service.py`)
3. Watch logs for DWITHIN vs Euclidean fallback in `gritbin_service.py`

## Adding spatial queries

- Template: `GritBinRepository.query_dwithin` CQL filter
- Nearest **N** bins: sort distances and return top N (see `docs/nearest-5-grit-bins.md`)
- Other asset types: change `GEOSERVER_LAYER` or add a new repository (see `docs/scale-multiple-asset-types.md`)

## Spatial querying is the differentiator

The geospatial reasoning — EPSG:27700, WFS vs WMS, CQL DWITHIN, the Euclidean
fallback, and `SP_GEOMETRY` extraction — is what the interviewers really probe.
Each concept is explained (with interview-ready answers and further-reading
links) in [10-spatial-querying.md](./10-spatial-querying.md).

---

<!-- tutorial-nav -->

| Previous | Next |
|:---------|-----:|
| ← [Spatial querying](./10-spatial-querying.md) | [Next steps](./08-next-steps.md) → |
