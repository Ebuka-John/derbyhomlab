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

On `main`, Address/GeoServer **repository** code is taught inside the combined
service lessons (there is no separate “repositories only” page). Use those for
embedded walkthroughs; this lab’s next step ([07-services.md](./07-services.md))
is the matching business layer.

- Layered design: [00-backend-design.md (main)](https://github.com/Ebuka-John/derbyhomlab/blob/main/tutorial/backend/00-backend-design.md)
- Address repo + service walkthrough: [07-address-service.md (main)](https://github.com/Ebuka-John/derbyhomlab/blob/main/tutorial/backend/07-address-service.md)
- GeoServer repo + service walkthrough: [08-geoserver-service.md (main)](https://github.com/Ebuka-John/derbyhomlab/blob/main/tutorial/backend/08-geoserver-service.md)
- Design patterns (panel): [lfdocs/copilotdocs.md](../../lfdocs/copilotdocs.md) § Design patterns
- WFS / nearest-N notes (main): [docs/nearest-5-grit-bins.md](https://github.com/Ebuka-John/derbyhomlab/blob/main/docs/nearest-5-grit-bins.md)

---

| Previous | Next |
|:---------|-----:|
| ← [Models](./05-models.md) | [Services](./07-services.md) → |
