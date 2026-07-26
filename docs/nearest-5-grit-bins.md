# How to return the nearest 5 grit bins

Implemented as `GET /nearest-grit-bins?postcode=...&address=...&limit=5`.

## Approach

- Rank candidates with `nearest_n_from_features`: compute Euclidean distance in
  EPSG:27700, keep bins inside the search radius, **sort ascending**, return the
  first *N* (`matches[:limit]`).
- Reuse the same DWITHIN → full-fetch fallback as the single nearest endpoint
  (`GritBinService.find_nearest_n`).
- If fewer than `limit` bins fall inside the radius, return whatever is available
  (at least one). Zero in-radius candidates still yields `404 no_grit_bin_nearby`.

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
