# 5. Running the Fullstack Project

## What you will do

Run backend + frontend together and verify the end-to-end path.

## Start FastAPI

Project root, venv active, `.env` present:

```powershell
uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
```

- Docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

## Start Next.js

Second terminal:

```powershell
cd frontend
npm run dev
```

- UI: http://127.0.0.1:3000

## Fullstack test plan

1. Open the UI
2. Submit `HILLBROW` + `DE55 5PB`
3. Confirm the browser network call is to `/api/nearest-grit-bin` (not `:8000`)
4. Confirm FastAPI logs show the upstream work
5. Compare:

```powershell
curl "http://127.0.0.1:8000/nearest-grit-bin?postcode=DE55%205PB&address=HILLBROW"
curl "http://127.0.0.1:3000/api/nearest-grit-bin?postcode=DE55%205PB&address=HILLBROW"
```

Both should return the same JSON shape.

## Optional: tests

```powershell
pip install -r requirements-dev.txt
pytest -v
```

---

<!-- tutorial-nav -->

| Previous | Next |
|:---------|-----:|
| ← [Frontend run and test](./frontend/09-run-and-test.md) | [Docker lab](./docker/README.md) → |
