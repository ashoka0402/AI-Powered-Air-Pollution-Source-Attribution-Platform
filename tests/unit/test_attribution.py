"""Unit tests for source attribution helpers."""

from datetime import datetime

from src.common.schemas import (
    CandidateSource,
    ContextRecord,
    PollutionEvent,
    PollutionRecord,
    SourceRecord,
)
from src.source_attribution.candidate_sources import generate_candidate_sources
from src.source_attribution.pollutant_signatures import (
    calculate_pollutant_signature_evidence,
)
from src.source_attribution.pipeline import generate_attribution_result


def test_candidate_generation():
    event = PollutionEvent(
        event_id="EVT-1",
        grid_id="G042",
        start_time=datetime(2026, 8, 23, 10, 0),
        pollutant="pm25",
        observed_value=150,
        baseline_value=60,
        latitude=28.6139,
        longitude=77.2090,
    )
    sources = [
        SourceRecord(
            source_id="C1",
            source_type="construction",
            latitude=28.618,
            longitude=77.215,
            active_flag=True,
        ),
        SourceRecord(
            source_id="FAR",
            source_type="industrial",
            latitude=29.0,
            longitude=78.0,
            active_flag=True,
        ),
    ]
    ctx = ContextRecord(
        timestamp=event.start_time,
        grid_id="G042",
        wind_speed=3.0,
        wind_direction=45.0,
    )
    cands = generate_candidate_sources(event, sources, ctx)
    assert len(cands) >= 1
    assert all(c.distance_km <= 15 for c in cands)


def test_signature_evidence():
    rec = PollutionRecord(
        timestamp=datetime(2026, 8, 23, 10, 0),
        grid_id="G042",
        latitude=28.6,
        longitude=77.2,
        pm25=80,
        pm10=180,
        no2=20,
        so2=10,
        co=0.5,
    )
    score = calculate_pollutant_signature_evidence(rec, "construction")
    assert 0.0 <= score <= 1.0


def test_full_pipeline():
    event = PollutionEvent(
        event_id="EVT-TEST",
        grid_id="G042",
        start_time=datetime(2026, 8, 23, 10, 0),
        pollutant="pm25",
        observed_value=160,
        baseline_value=70,
        latitude=28.6139,
        longitude=77.2090,
        severity="high",
    )
    pollution = PollutionRecord(
        timestamp=event.start_time,
        grid_id="G042",
        latitude=28.6139,
        longitude=77.2090,
        pm25=160,
        pm10=240,
        no2=45,
        so2=12,
        co=1.1,
    )
    sources = [
        SourceRecord(
            source_id="C1",
            source_type="construction",
            latitude=28.618,
            longitude=77.215,
            active_flag=True,
        )
    ]
    ctx = ContextRecord(
        timestamp=event.start_time,
        grid_id="G042",
        wind_speed=2.5,
        wind_direction=30,
        construction_activity=1.0,
        traffic_index=0.4,
    )
    result = generate_attribution_result(event, pollution, sources, ctx, model=None)
    assert result.event_id == "EVT-TEST"
    assert result.primary_source_type in (
        "construction",
        "road_dust",
        "traffic",
        "unknown",
        "background",
    )
    assert 0.15 <= result.confidence <= 0.98
    assert len(result.sources) > 0