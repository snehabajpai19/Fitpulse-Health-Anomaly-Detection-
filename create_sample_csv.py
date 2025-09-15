import os
from datetime import datetime, timedelta
from typing import Optional

import numpy as np
import pandas as pd


def _ensure_dir(path: str) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)


def create_heart_rate_csv(file_path: str, minutes: int = 180, seed: Optional[int] = 42) -> str:
    """Create a sample heart rate CSV with per-minute readings.

    Columns: timestamp, heart_rate_bpm
    """
    rng = np.random.default_rng(seed)
    start_time = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    timestamps = []
    heart_rates = []

    for i in range(minutes):
        ts = start_time + timedelta(minutes=i)
        # Baseline + mild sinusoidal variation + noise
        baseline = 72 + 8 * np.sin(i / 15)
        noise = rng.normal(0, 3)
        hr = int(max(48, min(180, baseline + noise)))
        timestamps.append(ts.strftime("%Y-%m-%d %H:%M:%S"))
        heart_rates.append(hr)

    df = pd.DataFrame({
        "timestamp": timestamps,
        "heart_rate_bpm": heart_rates,
    })

    _ensure_dir(file_path)
    df.to_csv(file_path, index=False)
    return file_path


def create_steps_csv(file_path: str, minutes: int = 180, seed: Optional[int] = 123) -> str:
    """Create a sample steps CSV with per-minute step count and cadence.

    Columns: timestamp, steps, cadence
    """
    rng = np.random.default_rng(seed)
    start_time = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    timestamps, steps, cadence = [], [], []

    for i in range(minutes):
        ts = start_time + timedelta(minutes=i)
        # Simulate activity bursts: more steps during daytime windows
        hour = ts.hour
        lam = 2
        if 8 <= hour < 10 or 12 <= hour < 14 or 17 <= hour < 19:
            lam = 20
        s = int(rng.poisson(lam))
        # Cadence in steps per minute; if no steps, cadence 0
        cad = s if s > 0 else 0
        timestamps.append(ts.strftime("%Y-%m-%d %H:%M:%S"))
        steps.append(s)
        cadence.append(cad)

    df = pd.DataFrame({
        "timestamp": timestamps,
        "steps": steps,
        "cadence": cadence,
    })

    _ensure_dir(file_path)
    df.to_csv(file_path, index=False)
    return file_path


def create_sleep_csv(
    file_path: str, duration_hours: int = 7, interval_minutes: int = 5, seed: Optional[int] = 7
) -> str:
    """Create a sample sleep-stage CSV across a single sleep session.

    Columns: timestamp, stage, duration_min
    Stages: awake, light, deep, REM
    """
    rng = np.random.default_rng(seed)
    # Sleep from previous day 23:00 to morning
    start_time = (datetime.now().replace(hour=23, minute=0, second=0, microsecond=0)
                  - timedelta(days=1))
    n = int((duration_hours * 60) / interval_minutes)

    stages = ["awake", "light", "deep", "REM"]
    probs = np.array([0.05, 0.55, 0.25, 0.15])

    timestamps, stage_vals, durations = [], [], []
    for i in range(n):
        ts = start_time + timedelta(minutes=i * interval_minutes)
        stage = rng.choice(stages, p=probs)
        timestamps.append(ts.strftime("%Y-%m-%d %H:%M:%S"))
        stage_vals.append(stage)
        durations.append(interval_minutes)

    df = pd.DataFrame({
        "timestamp": timestamps,
        "stage": stage_vals,
        "duration_min": durations,
    })

    _ensure_dir(file_path)
    df.to_csv(file_path, index=False)
    return file_path


def create_sample_csv(out_dir: str = ".") -> dict:
    """Create all three CSVs: heart rate, steps, sleep.

    Returns a dict with file paths.
    """
    paths = {
        "heart_rate": os.path.join(out_dir, "sample_heart_rate.csv"),
        "steps": os.path.join(out_dir, "sample_steps.csv"),
        "sleep": os.path.join(out_dir, "sample_sleep.csv"),
    }
    create_heart_rate_csv(paths["heart_rate"]) 
    create_steps_csv(paths["steps"]) 
    create_sleep_csv(paths["sleep"]) 
    return paths


if __name__ == "__main__":
    files = create_sample_csv()
    print("Created sample CSVs:")
    for k, v in files.items():
        print(f" - {k}: {v}")

