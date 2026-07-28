# Backend 7 — Services

## Concept

Services implement **business rules** and call repositories. Still **no FastAPI**.

| Service | Does |
|---------|------|
| `AddressService` | Validate postcode → fetch records → substring-match address → BNG point |
| `GritBinService` | `DWITHIN` candidates → Euclidean nearest; fallback to full layer if needed |

Shared `httpx.AsyncClient` is injected (from app lifespan later) so connections are pooled.

## Type these files (one at a time)

| # | Create in lab | Type from reference |
|--:|---------------|---------------------|
| 1 | `src/services/address_service.py` | `src/services/address_service.py` |
| 2 | `src/services/gritbin_service.py` | `src/services/gritbin_service.py` |

## Checkpoint

```powershell
.\.venv\Scripts\Activate.ps1
python -c "from src.services.address_service import AddressService; from src.services.gritbin_service import GritBinService; print('services ok')"
```

## Deeper reading

- `main`: `tutorial/backend/07-address-service.md`, `tutorial/backend/08-geoserver-service.md`

---

| Previous | Next |
|:---------|-----:|
| ← [Repositories](./06-repositories.md) | [API & app](./08-api-app.md) → |
