import json
from datetime import datetime, timedelta
from typing import Optional

import numpy as np


def create_sample_json_data(minutes: int = 60, seed: Optional[int] = 2024) -> dict:
    """Create in-memory sample fitness data for heart rate, steps, and sleep.

    Structure:
    {
      "heart_rate_data": [ {timestamp, bpm, confidence}, ... ],
      "step_data": [ {timestamp, steps, cadence}, ... ],
      "sleep_data": [ {timestamp, stage, duration_min}, ... ]
    }
    """
    rng = np.random.default_rng(seed)
    data = {"heart_rate_data": [], "step_data": [], "sleep_data": []}

    # Start of the day at 08:00 for HR and Steps
    start_time = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)

    # Heart rate data (per minute)
    for i in range(minutes):
        ts = start_time + timedelta(minutes=i)
        baseline = 70 + 6 * np.sin(i / 12)
        noise = rng.normal(0, 4)
        hr = int(max(48, min(180, baseline + noise)))
        data["heart_rate_data"].append({
            "timestamp": ts.isoformat(),
            "bpm": hr,
            "confidence": float(rng.uniform(0.8, 1.0)),
        })

    # Step data (per minute)
    for i in range(minutes):
        ts = start_time + timedelta(minutes=i)
        hour = ts.hour
        lam = 2
        if 8 <= hour < 10 or 12 <= hour < 14 or 17 <= hour < 19:
            lam = 18
        steps = int(rng.poisson(lam))
        data["step_data"].append({
            "timestamp": ts.isoformat(),
            "steps": steps,
            "cadence": steps if steps > 0 else 0,
        })

    # Sleep data (5-minute intervals over ~7 hours)
    sleep_start = (datetime.now().replace(hour=23, minute=0, second=0, microsecond=0)
                   - timedelta(days=1))
    interval = 5
    n = int((7 * 60) / interval)
    stages = ["awake", "light", "deep", "REM"]
    probs = np.array([0.06, 0.54, 0.25, 0.15])
    for i in range(n):
        ts = sleep_start + timedelta(minutes=i * interval)
        stage = rng.choice(stages, p=probs)
        data["sleep_data"].append({
            "timestamp": ts.isoformat(),
            "stage": str(stage),
            "duration_min": interval,
        })

    return data


def write_sample_json(file_path: str = "sample_data.json", minutes: int = 60) -> str:
    data = create_sample_json_data(minutes=minutes)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return file_path


if __name__ == "__main__":
    path = write_sample_json()
    print(f"Created sample JSON at: {path}")

