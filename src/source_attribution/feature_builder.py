"""
Feature engineering for the attribution model.

Canonical function:
    build_source_features()
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence

import numpy as np

from src.common.schemas import (
    CandidateSource,
    ContextRecord,
    PollutionEvent,
    PollutionRecord,
)
from src.source_attribution.pollutant_signatures import (
    calculate_pollutant_signature_evidence,
)


FEATURE_COLUMNS = [
    "pm25",
    "pm10",
    "no2",
    "so2",
    "co",
    "pm25_excess",
    "pm10_excess",
    "wind_speed",
    "traffic_index",
    "construction_activity",
    "industrial_activity",
    "fire_count_5km",
    "nearest_candidate_score",
    "nearest_upwind_score",
    "nearest_distance_km",
    "sig_traffic",
    "sig_road_dust",
    "sig_construction",
    "sig_industrial",
    "sig_waste_burning",
    "sig_biomass_burning",
]


def build_source_features(
    event: PollutionEvent,
    pollution: PollutionRecord,
    context: Optional[ContextRecord] = None,
    candidates: Optional[Sequence[CandidateSource]] = None,
) -> Dict[str, float]:
    """
    Build a flat feature dictionary suitable for the attribution classifier.
    """
    ctx = context
    cands = list(candidates or [])

    nearest = cands[0] if cands else None

    features: Dict[str, float] = {
        "pm25": float(pollution.pm25 or 0.0),
        "pm10": float(pollution.pm10 or 0.0),
        "no2": float(pollution.no2 or 0.0),
        "so2": float(pollution.so2 or 0.0),
        "co": float(pollution.co or 0.0),
        "pm25_excess": float((pollution.pm25 or 0.0) - event.baseline_value),
        "pm10_excess": float((pollution.pm10 or 0.0) - (event.baseline_value * 1.4)),
        "wind_speed": float(ctx.wind_speed) if ctx else 0.0,
        "traffic_index": float(ctx.traffic_index) if ctx else 0.0,
        "construction_activity": float(ctx.construction_activity) if ctx else 0.0,
        "industrial_activity": float(ctx.industrial_activity) if ctx else 0.0,
        "fire_count_5km": float(ctx.fire_count_5km) if ctx else 0.0,
        "nearest_candidate_score": nearest.candidate_score if nearest else 0.0,
        "nearest_upwind_score": nearest.upwind_score if nearest else 0.0,
        "nearest_distance_km": nearest.distance_km if nearest else 99.0,
        "sig_traffic": calculate_pollutant_signature_evidence(pollution, "traffic"),
        "sig_road_dust": calculate_pollutant_signature_evidence(pollution, "road_dust"),
        "sig_construction": calculate_pollutant_signature_evidence(
            pollution, "construction"
        ),
        "sig_industrial": calculate_pollutant_signature_evidence(
            pollution, "industrial"
        ),
        "sig_waste_burning": calculate_pollutant_signature_evidence(
            pollution, "waste_burning"
        ),
        "sig_biomass_burning": calculate_pollutant_signature_evidence(
            pollution, "biomass_burning"
        ),
    }
    return features


def features_to_vector(features: Dict[str, float]) -> np.ndarray:
    """Convert feature dict to a fixed-order numpy vector."""
    return np.array([features.get(c, 0.0) for c in FEATURE_COLUMNS], dtype=float)


def features_to_matrix(feature_list: List[Dict[str, float]]) -> np.ndarray:
    return np.vstack([features_to_vector(f) for f in feature_list])