# Backend 3 — Config & logging

## Concept

- **`Settings`** (`pydantic_settings`) reads env vars once, validates required keys,
  builds Address API headers and the WFS URL (`…/DCC/ows`).
- **`get_settings()`** is `@lru_cache` — one settings object per process.
- **`config.py`** re-exports settings so callers can `from src.config import get_settings`.
- **`logging.py`** configures a simple console logger for the app.

## Type these files (one at a time)

| # | Create in lab | Type from reference | Why |
|--:|---------------|---------------------|-----|
| 1 | `src/core/settings.py` | `src/core/settings.py` | Env → typed config |
| 2 | `src/core/logging.py` | `src/core/logging.py` | Log format / level |
| 3 | `src/config.py` | `src/config.py` | Thin re-export |

After each file, save (`Ctrl+S`). Do not skip settings — everything else depends on it.

## Checkpoint

Do **not** continue to the next lesson until this passes.


```powershell
.\.venv\Scripts\Activate.ps1
python -c "from src.config import get_settings; s=get_settings(); print(s.geoserver_layer)"
```

Should print `DCC:Gritbins` (or whatever you set in `.env`). If ValidationError —
fix missing keys in `.env`.

## Deeper reading

- `main`: `tutorial/backend/04-config.md`

---

| Previous | Next |
|:---------|-----:|
| ← [Packages](./02-packages.md) | [Errors & utils](./04-errors-utils.md) → |
