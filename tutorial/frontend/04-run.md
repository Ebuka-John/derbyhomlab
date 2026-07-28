# Frontend 4 — Run full stack

## Concept

Two processes:

1. FastAPI on **8000**
2. Next.js on **3000** with `BACKEND_URL` pointing at FastAPI

Browser → Next → FastAPI → upstreams.

## Terminals (lab)

**Terminal A — backend**

```powershell
.\.venv\Scripts\Activate.ps1
uvicorn src.app:app --reload --host 127.0.0.1 --port 8000
```

**Terminal B — frontend**

```powershell
cd frontend
npm run dev
```

Open http://127.0.0.1:3000  

Try `DE55 5PB` / `HILLBROW` → expect **GB0199**.

## Checkpoint

Do **not** continue to the next lesson until this passes.


Form returns a grit-bin title and distance without browser network calls to
`derbyshire.gov.uk` (only calls to `:3000/api/...`).

Optional next: [Docker lab](../docker/README.md)

## Deeper reading

- `main`: `tutorial/frontend/09-run-and-test.md`, `tutorial/05-running-fullstack.md`
- This branch: root `README.md`

---

| Previous | Next |
|:---------|-----:|
| ← [UI](./03-ui.md) | [Docker](../docker/README.md) → |
