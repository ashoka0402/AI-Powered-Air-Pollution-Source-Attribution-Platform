"""
Anomaly detection for pollution observations.

Canonical function:
    detect_pollution_anomaly()
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.common.constants import ANOMALY_ZSCORE_THRESHOLD
from src.common.schemas import PollutionRecord
from src.event_detection.baseline import PollutionBaseline, baseline_zscore


@dataclass
class AnomalyResult:
    is_anomaly: bool
    zscore: float
    observed: float
    expected: float
    pollutant: str
    grid_id: str
    timestamp: datetime
    severity_hint: str  # low / moderate / high / critical


def _severity_from_z(z: float) -> str:
    az = abs(z)
    if az < 2.0:
        return "low"
    if az < 3.0:
        return "moderate"
    if az < 4.5:
        return "high"
    return "critical"


def detect_pollution_anomaly(
    record: PollutionRecord,
    baseline: PollutionBaseline,
    pollutant: str = "pm25",
    zscore_threshold: float = ANOMALY_ZSCORE_THRESHOLD,
) -> AnomalyResult:
    """
    Decide whether a single PollutionRecord constitutes an anomaly
    relative to the time-of-day baseline.
    """
    observed = getattr(record, pollutant, None)
    if observed is None:
        return AnomalyResult(
            is_anomaly=False,
            zscore=0.0,
            observed=0.0,
            expected=0.0,
            pollutant=pollutant,
            grid_id=record.grid_id,
            timestamp=record.timestamp,
            severity_hint="low",
        )

    from src.event_detection.baseline import get_expected_concentration

    expected = get_expected_concentration(
        baseline, record.grid_id, pollutant, record.timestamp
    )
    z = baseline_zscore(
        baseline, record.grid_id, pollutant, record.timestamp, float(observed)
    )
    is_anom = z >= zscore_threshold  # only positive spikes for pollution events

    return AnomalyResult(
        is_anomaly=is_anom,
        zscore=float(z),
        observed=float(observed),
        expected=float(expected),
        pollutant=pollutant,
        grid_id=record.grid_id,
        timestamp=record.timestamp,
        severity_hint=_severity_from_z(z),
    )