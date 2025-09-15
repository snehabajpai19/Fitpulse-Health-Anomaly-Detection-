from typing import Dict, Optional, List, Any
import csv
from datetime import datetime

try:
    import pandas as pd  # type: ignore
except Exception:  # pandas optional
    pd = None  # type: ignore


def load_heart_rate_csv(path: str):
    """Load heart rate CSV with column 'timestamp' and 'heart_rate_bpm'.

    Returns a pandas DataFrame if pandas is available, otherwise a list of dicts.
    """
    if pd is not None:
        try:
            df = pd.read_csv(path)
        except Exception:
            return pd.DataFrame()
        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        return df
    # Fallback: built-in csv
    rows: List[Dict[str, Any]] = []
    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                if "timestamp" in r and r["timestamp"]:
                    try:
                        r["timestamp"] = datetime.fromisoformat(r["timestamp"])
                    except Exception:
                        pass
                rows.append(r)
    except Exception:
        return []
    return rows


def load_steps_csv(path: str):
    """Load steps CSV with columns 'timestamp', 'steps', 'cadence'."""
    if pd is not None:
        try:
            df = pd.read_csv(path)
        except Exception:
            return pd.DataFrame()
        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        return df
    rows: List[Dict[str, Any]] = []
    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                if "timestamp" in r and r["timestamp"]:
                    try:
                        r["timestamp"] = datetime.fromisoformat(r["timestamp"])
                    except Exception:
                        pass
                rows.append(r)
    except Exception:
        return []
    return rows


def load_sleep_csv(path: str):
    """Load sleep CSV with columns 'timestamp', 'stage', 'duration_min'."""
    if pd is not None:
        try:
            df = pd.read_csv(path)
        except Exception:
            return pd.DataFrame()
        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        return df
    rows: List[Dict[str, Any]] = []
    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                if "timestamp" in r and r["timestamp"]:
                    try:
                        r["timestamp"] = datetime.fromisoformat(r["timestamp"])
                    except Exception:
                        pass
                rows.append(r)
    except Exception:
        return []
    return rows


def load_all_csv(
    heart_rate_path: Optional[str] = None,
    steps_path: Optional[str] = None,
    sleep_path: Optional[str] = None,
) -> Dict[str, Any]:
    """Load available CSVs and return a dict of DataFrames.

    Keys: 'heart_rate', 'steps', 'sleep'
    Missing files yield empty DataFrames.
    """
    empty = pd.DataFrame() if pd is not None else []
    data: Dict[str, Any] = {
        "heart_rate": empty,
        "steps": empty,
        "sleep": empty,
    }
    if heart_rate_path:
        data["heart_rate"] = load_heart_rate_csv(heart_rate_path)
    if steps_path:
        data["steps"] = load_steps_csv(steps_path)
    if sleep_path:
        data["sleep"] = load_sleep_csv(sleep_path)
    return data
