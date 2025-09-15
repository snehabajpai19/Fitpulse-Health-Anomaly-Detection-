import argparse
from typing import Dict, Literal, Any, List

try:
    import pandas as pd  # type: ignore
except Exception:
    pd = None  # type: ignore

from load_csv import load_all_csv
from load_json import load_fitness_json


Prefer = Literal["csv", "json", "both"]


def _is_dataframe(obj: Any) -> bool:
    return pd is not None and str(type(obj)).endswith("DataFrame'>")


def _is_empty(obj: Any) -> bool:
    if _is_dataframe(obj):
        return obj.empty
    return not obj


def _combine(csv_df: Any, json_df: Any) -> Any:
    """Combine two frames by union on rows and sort by timestamp.

    Assumes both frames already use aligned column names.
    Drops exact duplicate rows; if a 'timestamp' column exists, sorts by it.
    """
    # Handle empties and types
    if _is_dataframe(csv_df):
        csv_empty = csv_df.empty
    else:
        csv_empty = not csv_df
    if _is_dataframe(json_df):
        json_empty = json_df.empty
    else:
        json_empty = not json_df

    if csv_empty:
        if _is_dataframe(json_df):
            return json_df.copy()
        return list(json_df) if json_df else ([] if pd is None else pd.DataFrame())
    if json_empty:
        if _is_dataframe(csv_df):
            return csv_df.copy()
        return list(csv_df)

    # Both have data
    if _is_dataframe(csv_df) and _is_dataframe(json_df):
        common_cols = sorted(set(csv_df.columns).union(set(json_df.columns)))
        a = csv_df.reindex(columns=common_cols)
        b = json_df.reindex(columns=common_cols)
        out = pd.concat([a, b], ignore_index=True).drop_duplicates()
        if "timestamp" in out.columns:
            out = out.sort_values("timestamp").reset_index(drop=True)
        return out

    # List-of-dicts path
    merged: List[Dict[str, Any]] = list(csv_df) + list(json_df)
    # Drop exact duplicates
    seen = set()
    deduped: List[Dict[str, Any]] = []
    for item in merged:
        key = tuple(sorted(item.items()))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    # Sort by timestamp if present
    try:
        deduped.sort(key=lambda r: r.get("timestamp"))
    except Exception:
        pass
    return deduped


def load_pipeline(
    hr_csv: str | None = "sample_heart_rate.csv",
    steps_csv: str | None = "sample_steps.csv",
    sleep_csv: str | None = "sample_sleep.csv",
    json_path: str | None = "fitness_data.json",
    prefer: Prefer = "csv",
) -> Dict[str, Any]:
    """Load fitness data from CSVs and/or JSON, return standardized frames.

    - prefer="csv": use CSV data when present, otherwise fallback to JSON.
    - prefer="json": use JSON data when present, otherwise fallback to CSV.
    - prefer="both": union CSV and JSON rows for each dataset.
    """
    csv_data = load_all_csv(hr_csv, steps_csv, sleep_csv)
    empty = (pd.DataFrame() if pd is not None else [])
    json_data = load_fitness_json(json_path) if json_path else {"heart_rate": empty, "steps": empty, "sleep": empty}

    out: Dict[str, Any] = {}
    for key in ("heart_rate", "steps", "sleep"):
        cdf = csv_data.get(key, empty)
        jdf = json_data.get(key, empty)
        if prefer == "csv":
            out[key] = cdf if not _is_empty(cdf) else jdf
        elif prefer == "json":
            out[key] = jdf if not _is_empty(jdf) else cdf
        else:  # both
            out[key] = _combine(cdf, jdf)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Load fitness CSV/JSON data via pipeline")
    parser.add_argument("--hr_csv", default="sample_heart_rate.csv", help="Path to heart rate CSV")
    parser.add_argument("--steps_csv", default="sample_steps.csv", help="Path to steps CSV")
    parser.add_argument("--sleep_csv", default="sample_sleep.csv", help="Path to sleep CSV")
    parser.add_argument("--json", default="fitness_data.json", help="Path to fitness JSON")
    parser.add_argument("--prefer", choices=["csv", "json", "both"], default="csv", help="Prefer CSV, JSON, or union both")
    parser.add_argument("--show", action="store_true", help="Print head() and shapes")
    args = parser.parse_args()

    frames = load_pipeline(
        hr_csv=args.hr_csv,
        steps_csv=args.steps_csv,
        sleep_csv=args.sleep_csv,
        json_path=args.json,
        prefer=args.prefer,
    )

    if args.show:
        def show(name: str, obj: Any):
            print(f"\n{name}:")
            if _is_dataframe(obj):
                if obj.empty:
                    print("  (empty)")
                else:
                    print(obj.head())
                    print(f"shape={obj.shape}")
            else:
                if not obj:
                    print("  (empty)")
                else:
                    preview = obj[:5]
                    for row in preview:
                        print(row)
                    print(f"rows={len(obj)}")

        show("Heart Rate", frames["heart_rate"])
        show("Steps", frames["steps"]) 
        show("Sleep", frames["sleep"]) 


if __name__ == "__main__":
    main()
