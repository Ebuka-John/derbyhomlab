# How to batch-process addresses

- Add `POST /nearest-grit-bin/batch` accepting a JSON array of
  `{ "postcode": ..., "address": ... }`.
- **Bound concurrency** with an `asyncio.Semaphore` so the Address API and GeoServer are
  not flooded; reuse the shared `httpx.AsyncClient` connection pool.
- Return **per-item results** (success or typed error) so a single bad address doesn't
  fail the whole batch:

```json
{
  "results": [
    { "input": {"postcode": "AB12 3CD", "address": "Example Building"},
      "status": "ok", "nearest_grit_bin_title": "GBAV-424", "distance_meters": 12.3 },
    { "input": {"postcode": "XX0 0XX", "address": "NOWHERE"},
      "status": "error", "code": "address_not_found" }
  ]
}
```

- For large jobs, offload to a **task queue** (Celery/RQ/Cloud Tasks) and expose a
  job-status endpoint (`202 Accepted` → poll/callback) instead of a synchronous request.
