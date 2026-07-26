# Making functionality available to other Solutions

How this nearest-grit-bin capability can be reused by other Derbyshire solutions
(follow-up from the exercise brief).

## Prefer a shared backend API (not client-side calls)

The brief forbids calling Address Lookup / GeoServer from browser JavaScript (CORS).
Other Solutions should therefore call **this service** (or a shared integration layer),
not the upstreams directly.

## Integration options

1. **HTTP API (already)** — `GET /nearest-grit-bin?postcode=...&address=...`
   - Other apps (web, mobile backends, batch jobs) consume JSON over HTTPS.
   - Contract stays stable; upstream schema quirks stay behind this boundary.
2. **API gateway / developer portal** — publish the route with API keys, quotas, and
   OpenAPI (`/docs` / `/openapi.json`) so other teams can discover and subscribe.
3. **Internal library / SDK** — thin client wrappers (Python/C#) around the same HTTP
   contract for Solutions that prefer typed SDKs.
4. **Event / batch interface** — for bulk consumers, expose
   `POST /nearest-grit-bin/batch` or a queue-based job API (see
   [batch-process-addresses.md](batch-process-addresses.md)).
5. **Parameterised asset lookup** — generalise to `/nearest-asset?type=...` so gulley,
   grit-bin, and other layers share one integration surface (see
   [scale-multiple-asset-types.md](scale-multiple-asset-types.md)).

## Operational expectations for consumers

- Document error codes (`missing_parameter`, `target_address_not_found`,
  `no_grit_bin_nearby`, upstream `502`s) so callers can handle failures consistently.
- Version the API (`/v1/...`) before breaking response shape changes.
- Do not share Address API / GeoServer credentials with every Solution — keep them
  in this service’s secret store only.
