export type NearestGritBinSuccess = {
  address: string;
  postcode: string;
  nearest_grit_bin_title: string;
  distance_meters: number;
};

export type GritBinDistanceItem = {
  title: string;
  distance_meters: number;
};

export type NearestGritBinsSuccess = {
  address: string;
  postcode: string;
  nearest_grit_bins: GritBinDistanceItem[];
};

export type GritBinItem = {
  title: string;
  easting: number;
  northing: number;
};

export type GritBinsSuccess = {
  count: number;
  grit_bins: GritBinItem[];
};

export type ApiErrorBody = {
  error: {
    code: string;
    message: string;
  };
};

export type LookupResult<T> =
  | { ok: true; data: T }
  | { ok: false; status: number; error: ApiErrorBody["error"] };
