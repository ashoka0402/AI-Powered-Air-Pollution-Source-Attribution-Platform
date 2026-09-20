"""Canonical Pydantic-style data schemas used across the platform.

These schemas are the integration contract between Person 1 (data),
Person 2 (AI), and Person 3 (app).
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any, Dict, List, Optional

from .enums import (
    EventSeverity,
    EventStatus,
    Pollutant,
    QualityFlag,
    SourceType,
)


@dataclass
class PollutionRecord:
    timestamp: datetime
    grid_id: str
    latitude: float
    longitude: float
    pm25: Optional[float] = None
    pm10: Optional[float] = None
    no2: Optional[float] = None
    so2: Optional[float] = None
    co: Optional[float] = None
    o3: Optional[float] = None
    aqi: Optional[int] = None
    quality_flag: str = QualityFlag.VALID.value

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["timestamp"] = self.timestamp.isoformat()
        return d


@dataclass
class ContextRecord:
    timestamp: datetime
    grid_id: str
    wind_speed: float = 0.0
    wind_direction: float = 0.0  # degrees, meteorological convention
    temperature: float = 25.0
    humidity: float = 50.0
    traffic_index: float = 0.0  # 0.0 – 1.0
    construction_activity: float = 0.0
    industrial_activity: float = 0.0
    fire_count_5km: int = 0
    fire_count_10km: int = 0
    precipitation: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["timestamp"] = self.timestamp.isoformat()
        return d


@dataclass
class SourceRecord:
    source_id: str
    source_type: str
    latitude: float
    longitude: float
    active_flag: bool = True
    name: Optional[str] = None
    distance_km: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PollutionEvent:
    event_id: str
    grid_id: str
    start_time: datetime
    pollutant: str
    observed_value: float
    baseline_value: float
    severity: str = EventSeverity.MODERATE.value
    status: str = EventStatus.ACTIVE.value
    end_time: Optional[datetime] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["start_time"] = self.start_time.isoformat()
        if self.end_time:
            d["end_time"] = self.end_time.isoformat()
        return d


@dataclass
class CandidateSource:
    event_id: str
    source_id: str
    source_type: str
    distance_km: float
    upwind_score: float
    candidate_score: float
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SourceContribution:
    source_type: str
    probability: float
    contribution: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AttributionResult:
    event_id: str
    grid_id: str
    timestamp: datetime
    primary_source_type: str
    confidence: float
    model_version: str
    sources: List[SourceContribution] = field(default_factory=list)
    evidence: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "grid_id": self.grid_id,
            "timestamp": self.timestamp.isoformat(),
            "primary_source_type": self.primary_source_type,
            "confidence": self.confidence,
            "model_version": self.model_version,
            "sources": [s.to_dict() for s in self.sources],
            "evidence": self.evidence,
        }


@dataclass
class ForecastResult:
    grid_id: str
    pollutant: str
    forecast_horizon_hours: int
    predicted_value: float
    lower_bound: float
    upper_bound: float
    model_version: str
    timestamp: datetime

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["timestamp"] = self.timestamp.isoformat()
        return d