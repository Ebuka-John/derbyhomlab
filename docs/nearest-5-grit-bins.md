# How to return the nearest 5 grit bins

Implemented as `GET /nearest-grit-bins?postcode=...&address=...&limit=5`.

## Approach

- Rank with `nearest_n_from_features`: compute Euclidean distance in EPSG:27700,
  **sort ascending**, return the first *N* (`matches[:limit]`).
- `GritBinService.find_nearest_n` fetches the **full WFS layer** by default so
  the result is not capped by the exercise 100 m window (that window often only
  contains one bin near HILLBROW). Pass `radius_meters` only when you want a
  constrained search.
- The single-bin exercise endpoint `/nearest-grit-bin` still uses the 100 m
  DWITHIN / Euclidean path.

## Example response

```json
{
  "address": "HILLBROW",
  "postcode": "DE55 5PB",
  "nearest_grit_bins": [
    { "title": "GBAV-424", "distance_meters": 12.3 },
    { "title": "GB1078",   "distance_meters": 47.9 }
  ]
}
```

## Related: list every grit bin

`GET /grit-bins` returns the unfiltered WFS layer (title + BNG easting/northing)
via `GritBinService.list_all` → `GritBinRepository.fetch_all`.
