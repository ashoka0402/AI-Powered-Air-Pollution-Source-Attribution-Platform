#!/usr/bin/env python3
"""
End-to-end demo of Person 2 AI layer using sample data.

Run from project root:
    python demo_person2_pipeline.py
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from src.common.schemas import (
    ContextRecord,
    PollutionRecord,
    SourceRecord,
)
from src.common.utils import parse_iso
from src.common.pipeline_progress import PipelineProgress
from src.event_detection.baseline import build_pollution_baseline
from src.event_detection.event_detector import detect_pollution_event
from src.source_attribution.pipeline import generate_attribution_result
from src.forecasting.pollution_forecaster import PollutionForecaster


def load_json(name: str):
    with open(ROOT / "data" / "sample" / name) as f:
        return json.load(f)


def main():
    progress = PipelineProgress()
    progress.start("Person 2 · AI Pipeline  (demo)")

    # ── 1. Ingest ──────────────────────────────────────────────
    progress.step("ingest", "Loading sample data…")
    time.sleep(0.25)
    aq = load_json("sample_air_quality.json")
    wx = load_json("sample_weather.json")
    srcs = load_json("sample_sources.json")

    records = [
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
        )
        for r in aq
    ]
    contexts = {
        parse_iso(c["timestamp"]): ContextRecord(
            timestamp=parse_iso(c["timestamp"]),
            grid_id=c["grid_id"],
            wind_speed=c["wind_speed"],
            wind_direction=c["wind_direction"],
            temperature=c["temperature"],
            humidity=c["humidity"],
            traffic_index=c["traffic_index"],
            construction_activity=c["construction_activity"],
            industrial_activity=c["industrial_activity"],
            fire_count_5km=c["fire_count_5km"],
        )
        for c in wx
    }
    sources = [
        SourceRecord(
            source_id=s["source_id"],
            source_type=s["source_type"],
            latitude=s["latitude"],
            longitude=s["longitude"],
            active_flag=s["active_flag"],
            name=s.get("name"),
        )
        for s in srcs
    ]
    progress.done("ingest", f"{len(records)} records · {len(sources)} sources")

    # ── 2. Baseline ────────────────────────────────────────────
    progress.step("baseline", "Building time-of-day baseline…")
    time.sleep(0.2)
    baseline = build_pollution_baseline(records, pollutant="pm25")
    progress.done("baseline", f"{len(baseline.stats)} cells")

    # ── 3. Events ──────────────────────────────────────────────
    progress.step("events", "Scanning for anomalies…")
    time.sleep(0.2)
    events = detect_pollution_event(records, baseline, pollutant="pm25")
    progress.done("events", f"{len(events)} events")

    # ── 4–8. Attribution (strongest event) ─────────────────────
    result = None
    if events:
        event = max(events, key=lambda e: e.observed_value - e.baseline_value)
        pollution = min(
            records,
            key=lambda r: abs((r.timestamp - event.start_time).total_seconds()),
        )
        context = contexts.get(pollution.timestamp) or list(contexts.values())[0]

        progress.step("candidates", "Spatial + wind candidates…")
        time.sleep(0.15)
        progress.done("candidates", "upwind scoring done")

        progress.step("features", "Engineering feature vector…")
        time.sleep(0.15)
        progress.done("features", "22 features")

        progress.step("ml", "Source probabilities…")
        time.sleep(0.15)
        progress.done("ml", "uniform prior (no trained model)")

        progress.step("fusion", "Fusing ML + wind + signature…")
        time.sleep(0.2)
        result = generate_attribution_result(
            event=event,
            pollution=pollution,
            sources=sources,
            context=context,
            model=None,
        )
        progress.done("fusion", "5 evidence channels")

        progress.step("attribution", "Packaging result…")
        time.sleep(0.1)
        progress.done(
            "attribution",
            f"{result.primary_source_type}  conf={result.confidence:.2f}",
        )
    else:
        progress.skip("candidates")
        progress.skip("features")
        progress.skip("ml")
        progress.skip("fusion")
        progress.skip("attribution", "no events")

    # ── 9. Forecast ────────────────────────────────────────────
    progress.step("forecast", "24 h horizon…")
    time.sleep(0.2)
    forecaster = PollutionForecaster(pollutant="pm25")
    forecaster.fit(records)
    forecasts = forecaster.predict(records[-48:], horizon_hours=24)
    progress.done("forecast", f"{len(forecasts)} steps")

    progress.finish()

    # ── Summary (after the live bar) ───────────────────────────
    print()
    if events:
        print("Events detected:")
        for e in events[:5]:
            print(
                f"  • {e.event_id}  severity={e.severity}  "
                f"obs={e.observed_value:.1f}  base={e.baseline_value:.1f}"
            )
        if len(events) > 5:
            print(f"  … and {len(events) - 5} more")
    if result:
        print()
        print(f"Primary source : {result.primary_source_type}")
        print(f"Confidence     : {result.confidence}")
        print("Top contributions:")
        for s in result.sources[:4]:
            print(
                f"  {s.source_type:20s}  P={s.probability:.2f}  contrib={s.contribution:.2f}"
            )
        if result.evidence:
            print("Evidence:")
            for ev in result.evidence:
                print(f"  – {ev}")
    if forecasts:
        print()
        print("Forecast (every 6 h):")
        for f in forecasts[::6]:
            print(
                f"  +{f.forecast_horizon_hours:02d}h  "
                f"pred={f.predicted_value:6.1f}  "
                f"[{f.lower_bound:.1f} – {f.upper_bound:.1f}]"
            )


if __name__ == "__main__":
    main()
