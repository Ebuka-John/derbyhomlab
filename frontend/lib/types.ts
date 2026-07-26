export type NearestGritBinSuccess = {
  address: string;
  postcode: string;
  nearest_grit_bin_title: string;
  distance_meters: number;
};

export type ApiErrorBody = {
  error: {
    code: string;
    message: string;
  };
};

export type LookupResult =
  | { ok: true; data: NearestGritBinSuccess }
  | { ok: false; status: number; error: ApiErrorBody["error"] };
