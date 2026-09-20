"""
Pollution event detection.

Canonical function:
    detect_pollution_event()

Class:
    PollutionEventDetector
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Sequence

from src.common.constants import (
    EVENT_MERGE_WINDOW_MINUTES,
    EVENT_MIN_DURATION_MINUTES,
)
from src.common.enums import EventSeverity, EventStatus
from src.common.schemas import PollutionEvent, PollutionRecord
from src.common.utils import generate_event_id
from src.event_detection.anomaly_detector import AnomalyResult, detect_pollution_anomaly
from src.event_detection.baseline import PollutionBaseline


@dataclass
class PollutionEventDetector:
    """Stateful detector that can track open events across successive records."""

    baseline: PollutionBaseline
    pollutant: str = "pm25"
    min_duration_minutes: int = EVENT_MIN_DURATION_MINUTES
    merge_window_minutes: int = EVENT_MERGE_WINDOW_MINUTES
    open_events: Dict[str, PollutionEvent] = field(default_factory=dict)

    def process(self, record: PollutionRecord) -> Optional[PollutionEvent]:
        """Process one record; returns a closed event when an open event ends."""
        anomaly = detect_pollution_anomaly(record, self.baseline, self.pollutant)
        key = record.grid_id

        if anomaly.is_anomaly:
            if key in self.open_events:
                # Extend existing event
                evt = self.open_events[key]
                evt.observed_value = max(evt.observed_value, anomaly.observed)
                if anomaly.severity_hint == "critical":
                    evt.severity = EventSeverity.CRITICAL.value
                elif (
                    anomaly.severity_hint == "high"
                    and evt.severity != EventSeverity.CRITICAL.value
                ):
                    evt.severity = EventSeverity.HIGH.value
                return None
            else:
                # Start new event
                event_id = generate_event_id(record.grid_id, record.timestamp)
                evt = PollutionEvent(
                    event_id=event_id,
                    grid_id=record.grid_id,
                    start_time=record.timestamp,
                    pollutant=self.pollutant,
                    observed_value=anomaly.observed,
                    baseline_value=anomaly.expected,
                    severity=anomaly.severity_hint,
                    status=EventStatus.ACTIVE.value,
                    latitude=record.latitude,
                    longitude=record.longitude,
                )
                self.open_events[key] = evt
                return None
        else:
            # No anomaly – close any open event if it has lasted long enough
            if key in self.open_events:
                evt = self.open_events[key]
                duration = (record.timestamp - evt.start_time).total_seconds() / 60.0
                if duration >= self.min_duration_minutes:
                    evt.end_time = record.timestamp
                    evt.status = EventStatus.RESOLVED.value
                    closed = evt
                    del self.open_events[key]
                    return closed
                else:
                    # Too short – discard as noise
                    del self.open_events[key]
            return None

    def flush(self, as_of: Optional[datetime] = None) -> List[PollutionEvent]:
        """Force-close all remaining open events (e.g. at end of batch)."""
        closed = []
        as_of = as_of or datetime.utcnow()
        for key, evt in list(self.open_events.items()):
            evt.end_time = as_of
            evt.status = EventStatus.RESOLVED.value
            closed.append(evt)
            del self.open_events[key]
        return closed


def detect_pollution_event(
    records: Sequence[PollutionRecord],
    baseline: PollutionBaseline,
    pollutant: str = "pm25",
) -> List[PollutionEvent]:
    """
    Batch helper: run the detector over a time-ordered sequence of records
    and return all completed PollutionEvent objects.
    """
    if not records:
        return []

    ordered = sorted(records, key=lambda r: r.timestamp)
    detector = PollutionEventDetector(baseline=baseline, pollutant=pollutant)
    events: List[PollutionEvent] = []

    for rec in ordered:
        closed = detector.process(rec)
        if closed is not None:
            events.append(closed)

    # Flush remaining open events
    events.extend(detector.flush(as_of=ordered[-1].timestamp if ordered else None))
    return events