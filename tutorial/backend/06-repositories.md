# Backend 6 — Repositories

## Concept

Repositories own **HTTP only**:

| Module | Upstream | Responsibility |
|--------|----------|----------------|
| `address_repository.py` | Address Lookup API | GET by postcode, unwrap JSON/XML errors → typed `AppError` |
| `gritbin_repository.py` | GeoServer WFS | `GetFeature` JSON; `DWITHIN(SP_GEOMETRY, …)` or full layer |

No address matching and no “pick nearest” here — that is the service layer.

Key GeoServer detail: geometry property is **`SP_GEOMETRY`**. Wrong name → empty or ExceptionReport.

## Type these files (one at a time)

| # | Create in lab | Type from reference |
|--:|---------------|---------------------|
| 1 | `src/repositories/address_repository.py` | `src/repositories/address_repository.py` |
| 2 | `src/repositories/gritbin_repository.py` | `src/repositories/gritbin_repository.py` |

## Checkpoint

Do **not** continue to the next lesson until this passes.


```powershell
.\.venv\Scripts\Activate.ps1
python -c "from src.repositories.address_repository import AddressRepository; from src.repositories.gritbin_repository import GritBinRepository, GEOMETRY_FIELD; print(GEOMETRY_FIELD)"
```

Should print `SP_GEOMETRY`.

## Deeper reading

- `main`: `tutorial/backend/07-address-service.md` (repo section), `tutorial/backend/08-geoserver-service.md`
- This branch: `docs/nearest-5-grit-bins.md`, `lfdocs/copilotdocs.md`

---

| Previous | Next |
|:---------|-----:|
| ← [Models](./05-models.md) | [Services](./07-services.md) → |
