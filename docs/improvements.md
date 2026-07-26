# Improvements with more time

- **Contract tests** against a recorded Address API response (VCR/cassette) once the
  real schema is frozen, replacing the flexible-alias parsing with strict Pydantic DTOs.
- **Caching** of the grit-bin layer (short TTL or ETag/conditional GET) to avoid the
  cost of the full-layer Euclidean fallback.
- **Observability**: structured JSON logging, request correlation IDs, and
  OpenTelemetry traces/metrics around each upstream call, with alerting on 502 spikes.
- **Input normalisation**: canonicalise postcodes (outward/inward spacing, case) and
  validate their format before calling the upstream API.
- **Resilience**: retries with exponential backoff + circuit breaker for the upstreams;
  per-caller rate limiting on this API.
- **Auth on this service**: API keys or JWT so it is safe to expose beyond a trusted
  network.
