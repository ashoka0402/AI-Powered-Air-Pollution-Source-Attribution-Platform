"""Unit tests for pollution baseline."""

from datetime import datetime, timedelta

import pytest

from src.common.schemas import PollutionRecord
from src.event_detection.baseline import (
    build_pollution_baseline,
    get_expected_concentration,
)


def _make_records(n=48, base_pm25=60.0):
    start = datetime(2026, 8, 1, 0, 0)
    recs = []
    for i in range(n):
        ts = start + timedelta(hours=i)
        recs.append(
            PollutionRecord(
                timestamp=ts,
                grid_id="G001",
                latitude=28.6,
                longitude=77.2,
                pm25=base_pm25 + (10 if 8 <= ts.hour <= 10 else 0),
            )
        )
    return recs


def test_build_baseline():
    recs = _make_records()
    bl = build_pollution_baseline(recs, pollutant="pm25")
    assert len(bl.stats) > 0
    expected = get_expected_concentration(bl, "G001", "pm25", recs[9].timestamp)
    assert expected > 0


def test_expected_higher_in_peak_hours():
    recs = _make_records()
    bl = build_pollution_baseline(recs, pollutant="pm25")
    morning = get_expected_concentration(
        bl, "G001", "pm25", datetime(2026, 8, 1, 9, 0)
    )
    night = get_expected_concentration(
        bl, "G001", "pm25", datetime(2026, 8, 1, 2, 0)
    )
    assert morning >= night