# How to return the nearest 5 grit bins

- Change `nearest_from_features` to **sort all in-radius candidates by distance** and
  return the first *N* (`matches[:5]`) instead of a single best.
- For the DWITHIN path, sort the returned `FeatureCollection` by computed distance; if
  fewer than 5 fall inside the radius, either widen the radius or issue a `BBOX`/k-NN
  query as a top-up.
- Expose it as `GET /nearest-grit-bins?limit=5&...` returning:

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
