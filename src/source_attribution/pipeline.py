"""
End-to-end attribution pipeline.

Canonical function:
    generate_attribution_result()
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Sequence

from src.common.constants import MODEL_VERSION
from src.common.schemas import (
    AttributionResult,
    CandidateSource,
    ContextRecord,
    PollutionEvent,
    PollutionRecord,
    SourceRecord,
)
from src.source_attribution.attribution_model import (
    AttributionModel,
    predict_source_probabilities,
)
from src.source_attribution.candidate_sources import generate_candidate_sources
from src.source_attribution.confidence import calculate_attribution_confidence
from src.source_attribution.contribution_estimator import estimate_source_contributions
from src.source_attribution.evidence_fusion import fuse_source_evidence
from src.source_attribution.feature_builder import build_source_features


def _build_evidence_statements(
    candidates: Sequence[CandidateSource],
    primary: str,
    context: Optional[ContextRecord],
) -> List[str]:
    evidence: List[str] = []
    if candidates:
        top = candidates[0]
        if top.upwind_score > 0.5:
            evidence.append(
                f"upwind {top.source_type} source ({top.distance_km:.1f} km)"
            )
        if top.candidate_score > 0.4:
            evidence.append(f"high spatial candidate score for {top.source_type}")
    if context:
        if context.construction_activity > 0.5 and primary == "construction":
            evidence.append("active construction activity nearby")
        if context.traffic_index > 0.6 and primary in ("traffic", "road_dust"):
            evidence.append("elevated traffic index")
        if context.fire_count_5km > 0 and primary in (
            "waste_burning",
            "biomass_burning",
        ):
            evidence.append(f"{context.fire_count_5km} fire hotspot(s) within 5 km")
        if context.wind_speed < 1.0:
            evidence.append("low wind speed (accumulation conditions)")
    return evidence


def generate_attribution_result(
    event: PollutionEvent,
    pollution: PollutionRecord,
    sources: Sequence[SourceRecord],
    context: Optional[ContextRecord] = None,
    model: Optional[AttributionModel] = None,
) -> AttributionResult:
    """
    Full attribution pipeline for a single pollution event.

    Steps
    -----
    1. Generate candidate sources (spatial + wind)
    2. Build feature vector
    3. ML source probabilities (or uniform prior if no model)
    4. Fuse with physics / signature / activity evidence
    5. Estimate contributions
    6. Compute confidence
    7. Package AttributionResult
    """
    candidates = generate_candidate_sources(event, sources, context)

    features = build_source_features(event, pollution, context, candidates)

    if model is not None and model.trained:
        ml_probs = predict_source_probabilities(model, features)
    else:
        # Uniform prior when model is unavailable (demo / cold-start)
        from src.common.constants import ATTRIBUTION_SOURCE_TYPES

        n = len(ATTRIBUTION_SOURCE_TYPES)
        ml_probs = {t: 1.0 / n for t in ATTRIBUTION_SOURCE_TYPES}

    fused = fuse_source_evidence(ml_probs, candidates, pollution, context)

    contributions = estimate_source_contributions(
        fused, event.observed_value, event.baseline_value
    )

    primary = max(fused.items(), key=lambda x: x[1])[0]
    evidence = _build_evidence_statements(candidates, primary, context)
    confidence = calculate_attribution_confidence(
        fused, candidates, context, evidence
    )

    return AttributionResult(
        event_id=event.event_id,
        grid_id=event.grid_id,
        timestamp=event.start_time,
        primary_source_type=primary,
        confidence=confidence,
        model_version=model.model_version if model else MODEL_VERSION,
        sources=contributions,
        evidence=evidence,
    )