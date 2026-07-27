# Test and monitor as a production service

How to harden testing and monitoring if this became a production integration service
(follow-up from the exercise brief).

## Testing

| Layer | What |
|---|---|
| **Unit** | Coordinate conversion, Title matching, nearest-bin selection, error mapping (`tests/`) |
| **Contract** | Recorded Address API / WFS fixtures (VCR) so upstream schema drift is caught in CI |
| **Integration** | Staging calls against real Address + GeoServer with non-prod credentials |
| **API / e2e** | Hit `/nearest-grit-bin` for known fixtures (e.g. Example Building / AB12 3CD) and assert Title + distance bounds |
| **Load** | Concurrent requests and batch jobs; protect upstreams with timeouts, semaphores, and rate limits |
| **Chaos / negative** | Simulate Address 5xx, GeoServer XML exceptions, empty DWITHIN — confirm typed errors and fallback |

CI should run `pytest` on every PR and block merges on failure. Image builds should be
scanned before promotion.

## Monitoring

- **Health probes**: `/health` for liveness/readiness (already in Docker `HEALTHCHECK`).
- **RED metrics**: request rate, error rate (by `error.code`), latency (p50/p95/p99) for
  `/nearest-grit-bin` and for each upstream call.
- **Dependency SLIs**: success rate and latency of Address API and GeoServer separately,
  so a council outage is obvious.
- **Logs**: structured JSON with correlation ID, postcode (careful with PII), upstream
  status, whether DWITHIN or Euclidean fallback was used.
- **Traces**: OpenTelemetry spans across Address → reproject → WFS.
- **Alerts**: spike in `502` / `address_api_unreachable` / `geoserver_unreachable`;
  sustained rise in `no_grit_bin_nearby` (data issue?); latency SLO burn.
- **Dashboards**: gateway + app + upstream health in one place (CloudWatch, Grafana, etc.).

## Production controls

- API-key / JWT auth via gateway; never expose Address/GeoServer tokens to callers.
- Timeouts, retries with backoff, and circuit breakers on upstreams.
- Config per environment (staging vs prod `.env` / secret manager).
- Runbooks for “Address API down” and “GeoServer empty/error” scenarios.
