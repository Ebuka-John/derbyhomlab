# Backend 4 — Errors & postcode

## Concept

**Typed errors (`AppError`)** carry `code` + `status_code`. The FastAPI app maps
them to JSON `{"error": {"code", "message"}}` so the UI and tests stay stable.

**Postcode helper** — normalise / reject bad UK postcodes before calling upstream.

Geospatial helpers come **after** domain models (next two steps), because they
import `Point27700` / `GritBinMatch`.

## Type these files (one at a time)

| # | Create in lab | Type from reference |
|--:|---------------|---------------------|
| 1 | `src/utils/exceptions.py` | `src/utils/exceptions.py` |
| 2 | `src/utils/postcode.py` | `src/utils/postcode.py` |

## Checkpoint

Do **not** continue to the next lesson until this passes.


```powershell
.\.venv\Scripts\Activate.ps1
python -c "from src.utils.exceptions import AppError, NoGritBinNearbyError; from src.utils.postcode import require_valid_uk_postcode; print('errors ok')"
```

## Deeper reading

- `main`: `tutorial/backend/05-errors.md`

---

| Previous | Next |
|:---------|-----:|
| ← [Config](./03-config.md) | [Models](./05-models.md) → |
