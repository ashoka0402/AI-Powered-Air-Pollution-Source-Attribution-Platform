#!/usr/bin/env python3
"""
Utility script that builds a pollution baseline from sample data
and optionally evaluates event detection on a held-out window.

Usage:
    python -m ml.training.train_event_detector
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.common.schemas import PollutionRecord
from src.common.utils import parse_iso
from src.event_detection.baseline import build_pollution_baseline
from src.event_detection.event_detector import detect_pollution_event


def load_records(path: Path):
    with open(path) as f:
        raw = json.load(f)
    records = []
    for r in raw:
        records.append(
            PollutionRecord(
                timestamp=parse_iso(r["timestamp"]),
                grid_id=r["grid_id"],
                latitude=r["latitude"],
                longitude=r["longitude"],
                pm25=r.get("pm25"),
                pm10=r.get("pm10"),
                no2=r.get("no2"),
                so2=r.get("so2"),
                co=r.get("co"),
                o3=r.get("o3"),
                aqi=r.get("aqi"),
                quality_flag=r.get("quality_flag", "valid"),
            )
        )
    return records


def main():
    sample = ROOT / "data/sample/sample_air_quality.json"
    if not sample.exists():
        print(f"Sample data missing: {sample}")
        print("Run the demo notebook / generate sample data first.")
        return

    records = load_records(sample)
    print(f"Loaded {len(records)} pollution records")

    baseline = build_pollution_baseline(records, pollutant="pm25")
    print(f"Baseline cells: {len(baseline.stats)}")

    events = detect_pollution_event(records, baseline, pollutant="pm25")
    print(f"Detected {len(events)} pollution events")
    for e in events[:5]:
        print(
            f"  {e.event_id}  grid={e.grid_id}  "
            f"obs={e.observed_value:.1f}  base={e.baseline_value:.1f}  "
            f"severity={e.severity}"
        )


if __name__ == "__main__":
    main()