import json
from typing import Dict, Any, List
from datetime import datetime

try:
    import pandas as pd  # type: ignore
except Exception:
    pd = None  # type: ignore


def load_fitness_json(path: str) -> Dict[str, Any]:
    """Load fitness JSON into standardized DataFrames.

    Input JSON structure (keys optional):
    - heart_rate_data: [{timestamp, bpm, confidence?}]
    - step_data: [{timestamp, steps, cadence?}]
    - sleep_data: [{timestamp, stage, duration_min}]

    Returns DataFrames with columns aligned to CSVs:
    - heart_rate: timestamp, heart_rate_bpm, confidence?
    - steps: timestamp, steps, cadence?
    - sleep: timestamp, stage, duration_min
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            blob = json.load(f)
    except Exception:
        empty = pd.DataFrame() if pd is not None else []
        return {"heart_rate": empty, "steps": empty, "sleep": empty}

    hr_list: List[Dict[str, Any]] = list(blob.get("heart_rate_data", []))
    steps_list: List[Dict[str, Any]] = list(blob.get("step_data", []))
    sleep_list: List[Dict[str, Any]] = list(blob.get("sleep_data", []))

    # Standardize columns and types
    for r in hr_list:
        if "bpm" in r and "heart_rate_bpm" not in r:
            r["heart_rate_bpm"] = r.pop("bpm")
        ts = r.get("timestamp")
        if ts:
            try:
                r["timestamp"] = datetime.fromisoformat(ts)
            except Exception:
                pass
    for r in steps_list:
        ts = r.get("timestamp")
        if ts:
            try:
                r["timestamp"] = datetime.fromisoformat(ts)
            except Exception:
                pass
    for r in sleep_list:
        ts = r.get("timestamp")
        if ts:
            try:
                r["timestamp"] = datetime.fromisoformat(ts)
            except Exception:
                pass

    if pd is None:
        return {"heart_rate": hr_list, "steps": steps_list, "sleep": sleep_list}

    hr = pd.DataFrame(hr_list)
    steps = pd.DataFrame(steps_list)
    sleep = pd.DataFrame(sleep_list)

    for df in (hr, steps, sleep):
        if not df.empty and "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    return {"heart_rate": hr, "steps": steps, "sleep": sleep}
