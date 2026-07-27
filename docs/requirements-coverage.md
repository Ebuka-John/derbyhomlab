# Requirements coverage (exercise brief)

Maps each brief requirement to where it is implemented and documented.

## Functional requirements

| Requirement | Code | Docs |
|---|---|---|
| Use Address Lookup for `DE55 5PB` | `address_service.py` → `GET {base}/{postcode}` | [approach.md](approach.md), [investigation-notes.md](investigation-notes.md) |
| Identify HILLBROW record | Match on `BuildingName` / composed address text | [assumptions.md](assumptions.md), [issues-encountered.md](issues-encountered.md) |
| Use that record’s coordinates for GeoServer | `SpatialFeature.Eastings/Northings` → BNG point | [approach.md](approach.md), [investigation-notes.md](investigation-notes.md) |
| Nearest grit bin within ~100 m | WFS `DWITHIN` + Euclidean fallback; radius env default 100 | [approach.md](approach.md), README request flow |
| Return grit bin Title | `nearest_grit_bin_title` (live: **GB0199**) | README example + [investigation-notes.md](investigation-notes.md) |
| Address not found | `address_not_found` / `target_address_not_found` (404); `invalid_postcode` (400) | README error table, [assumptions.md](assumptions.md) |
| No grit bin nearby | `no_grit_bin_nearby` (404) | README error table, [assumptions.md](assumptions.md) |
| Clear error handling & assumptions | `utils/exceptions.py` + typed JSON errors | [assumptions.md](assumptions.md), README, [issues-encountered.md](issues-encountered.md) |

## What we are looking for (assessment criteria)

| Criterion | Evidence |
|---|---|
| Break the problem into parts | Pipeline in [approach.md](approach.md); modules under `src/` |
| Research unfamiliar APIs | [investigation-notes.md](investigation-notes.md) |
| Identify correct GeoServer service | WFS (not WMS) — [approach.md](approach.md), [issues-encountered.md](issues-encountered.md) |
| Work with different response schemas | Flexible Address parsing; live `BuildingName` fix — [issues-encountered.md](issues-encountered.md) |
| Coordinate systems & spatial queries | EPSG:27700, `DWITHIN`, Euclidean — [approach.md](approach.md), `utils/geospatial.py` |
| Work around CORS | Server-side FastAPI + Next.js proxy — [investigation-notes.md](investigation-notes.md), [available-to-other-solutions.md](available-to-other-solutions.md) |
| Explain reasoning | This `docs/` folder + README design decisions |
| Readable / maintainable code | Layered `app` / `services` / `utils`; tests under `tests/` |

## Investigation notes checklist

| Brief prompt | Covered in |
|---|---|
| What did you try first? | [investigation-notes.md](investigation-notes.md) → Tried first |
| Tools used? | → Tools used |
| Documentation / resources? | → Documentation / resources |
| Assumptions? | → Assumptions + [assumptions.md](assumptions.md) |
| Approaches rejected? | → Approaches rejected |
| How verified? | → How the result was verified (includes **GB0199**) |

## Deliverables

| Deliverable | Where |
|---|---|
| Solution running | `docker compose up --build` — UI `:3000`, API `:8000` (README) |
| Grit bin Title returned | **GB0199** — README + investigation notes |
| Approach | [approach.md](approach.md) |
| Assumptions | [assumptions.md](assumptions.md) |
| Issues encountered | [issues-encountered.md](issues-encountered.md) |
| How investigated | [investigation-notes.md](investigation-notes.md) |
| Improvements with more time | [improvements.md](improvements.md) |
| Deploy / reuse | [deploy.md](deploy.md) |

## Follow-up discussion

| Topic | File |
|---|---|
| Other asset types | [scale-multiple-asset-types.md](scale-multiple-asset-types.md) |
| Nearest five grit bins | [nearest-5-grit-bins.md](nearest-5-grit-bins.md) |
| Available to other Solutions | [available-to-other-solutions.md](available-to-other-solutions.md) |
| Large batch of addresses | [batch-process-addresses.md](batch-process-addresses.md) |
| Test & monitor in production | [test-and-monitor.md](test-and-monitor.md) |
