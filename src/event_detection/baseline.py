"""
Pollution baseline estimation.

Canonical functions:
    build_pollution_baseline()
    get_expected_concentration()

Class:
    PollutionBaseline
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from src.common.constants import (
    BASELINE_LOOKBACK_HOURS,
    BASELINE_TIME_OF_DAY_WINDOW_HOURS,
)
from src.common.exceptions import InsufficientDataError
from src.common.schemas import PollutionRecord
from src.common.utils import parse_iso


@dataclass
class BaselineStats:
    mean: float
    std: float
    median: float
    p25: float
    p75: float
    count: int


@dataclass
class PollutionBaseline:
    """Holds baseline statistics keyed by (grid_id, pollutant, hour_of_day)."""

    stats: Dict[Tuple[str, str, int], BaselineStats] = field(default_factory=dict)
    lookback_hours: int = BASELINE_LOOKBACK_HOURS
    built_at: Optional[datetime] = None

    def get(self, grid_id: str, pollutant: str, hour: int) -> Optional[BaselineStats]:
        return self.stats.get((grid_id, pollutant, hour))

    def expected(self, grid_id: str, pollutant: str, timestamp: datetime) -> float:
        return get_expected_concentration(self, grid_id, pollutant, timestamp)


def _hour_of_day(ts: datetime) -> int:
    return ts.hour


def build_pollution_baseline(
    records: Sequence[PollutionRecord],
    pollutant: str = "pm25",
    lookback_hours: int = BASELINE_LOOKBACK_HOURS,
    time_of_day_window_hours: int = BASELINE_TIME_OF_DAY_WINDOW_HOURS,
) -> PollutionBaseline:
    """
    Build a time-of-day aware baseline from historical PollutionRecords.

    For each (grid_id, pollutant, hour) we collect values whose hour falls
    inside ± time_of_day_window_hours and compute robust statistics.
    """
    if not records:
        raise InsufficientDataError("No records provided for baseline construction")

    # Group raw values: (grid_id, hour) -> list of pollutant values
    buckets: Dict[Tuple[str, int], List[float]] = {}
    cutoff = None
    if records:
        latest = max(r.timestamp for r in records)
        cutoff = latest - timedelta(hours=lookback_hours)

    for rec in records:
        if cutoff and rec.timestamp < cutoff:
            continue
        value = getattr(rec, pollutant, None)
        if value is None or (isinstance(value, float) and np.isnan(value)):
            continue
        hour = _hour_of_day(rec.timestamp)
        key = (rec.grid_id, hour)
        buckets.setdefault(key, []).append(float(value))

    baseline = PollutionBaseline(lookback_hours=lookback_hours, built_at=datetime.utcnow())

    for (grid_id, hour), values in buckets.items():
        if len(values) < 3:
            continue
        arr = np.asarray(values, dtype=float)
        stats = BaselineStats(
            mean=float(np.nanmean(arr)),
            std=float(np.nanstd(arr)) if len(arr) > 1 else 0.0,
            median=float(np.nanmedian(arr)),
            p25=float(np.nanpercentile(arr, 25)),
            p75=float(np.nanpercentile(arr, 75)),
            count=len(arr),
        )
        baseline.stats[(grid_id, pollutant, hour)] = stats

        # Also fill neighbouring hours within the window for smoother lookup
        for offset in range(1, time_of_day_window_hours + 1):
            for neighbour in ((hour - offset) % 24, (hour + offset) % 24):
                nkey = (grid_id, pollutant, neighbour)
                if nkey not in baseline.stats:
                    baseline.stats[nkey] = stats

    if not baseline.stats:
        raise InsufficientDataError(
            f"Could not build baseline for pollutant={pollutant}; need more data"
        )
    return baseline


def get_expected_concentration(
    baseline: PollutionBaseline,
    grid_id: str,
    pollutant: str,
    timestamp: datetime,
) -> float:
    """
    Return the expected (baseline) concentration for the given grid / pollutant / time.
    Falls back to global mean for that pollutant if the exact cell is missing.
    """
    hour = _hour_of_day(timestamp)
    stats = baseline.get(grid_id, pollutant, hour)
    if stats is not None:
        return stats.mean

    # Fallback: any hour for this grid
    for h in range(24):
        stats = baseline.get(grid_id, pollutant, h)
        if stats is not None:
            return stats.mean

    # Global fallback
    all_means = [
        s.mean
        for (g, p, _), s in baseline.stats.items()
        if p == pollutant
    ]
    if all_means:
        return float(np.mean(all_means))
    return 0.0


def baseline_zscore(
    baseline: PollutionBaseline,
    grid_id: str,
    pollutant: str,
    timestamp: datetime,
    observed: float,
) -> float:
    """Compute z-score of an observed value against the baseline."""
    hour = _hour_of_day(timestamp)
    stats = baseline.get(grid_id, pollutant, hour)
    if stats is None or stats.std < 1e-6:
        return 0.0
    return (observed - stats.mean) / stats.std