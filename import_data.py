import argparse
import json
from typing import Dict, Tuple

import pandas as pd


def read_heart_rate_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


def read_steps_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


def read_sleep_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


def read_json(path: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    with open(path, "r", encoding="utf-8") as f:
        blob: Dict = json.load(f)

    hr = pd.DataFrame(blob.get("heart_rate_data", []))
    steps = pd.DataFrame(blob.get("step_data", []))
    sleep = pd.DataFrame(blob.get("sleep_data", []))

    for df in (hr, steps, sleep):
        if not df.empty and "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"])    
    return hr, steps, sleep


def main() -> None:
    parser = argparse.ArgumentParser(description="Import fitness CSV/JSON data")
    parser.add_argument("--hr_csv", help="Path to heart rate CSV", default="sample_heart_rate.csv")
    parser.add_argument("--steps_csv", help="Path to steps CSV", default="sample_steps.csv")
    parser.add_argument("--sleep_csv", help="Path to sleep CSV", default="sample_sleep.csv")
    parser.add_argument("--json", help="Path to JSON file", default="sample_data.json")
    parser.add_argument("--show", action="store_true", help="Print first rows of each dataset")
    args = parser.parse_args()

    # Load CSVs (if present)
    try:
        hr_csv_df = read_heart_rate_csv(args.hr_csv)
    except Exception:
        hr_csv_df = pd.DataFrame()
    try:
        steps_csv_df = read_steps_csv(args.steps_csv)
    except Exception:
        steps_csv_df = pd.DataFrame()
    try:
        sleep_csv_df = read_sleep_csv(args.sleep_csv)
    except Exception:
        sleep_csv_df = pd.DataFrame()

    # Load JSON (if present)
    try:
        hr_json_df, steps_json_df, sleep_json_df = read_json(args.json)
    except Exception:
        hr_json_df, steps_json_df, sleep_json_df = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    if args.show:
        def show(name: str, df: pd.DataFrame):
            print(f"\n{name}:")
            if df.empty:
                print("  (empty or not found)")
            else:
                print(df.head())

        show("CSV Heart Rate", hr_csv_df)
        show("CSV Steps", steps_csv_df)
        show("CSV Sleep", sleep_csv_df)
        show("JSON Heart Rate", hr_json_df)
        show("JSON Steps", steps_json_df)
        show("JSON Sleep", sleep_json_df)


if __name__ == "__main__":
    main()

