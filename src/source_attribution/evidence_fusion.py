"""
Evidence fusion combining wind, distance, pollutant signatures and ML scores.

Canonical function:
    fuse_source_evidence()

Class:
    EvidenceFusionEngine
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence

import numpy as np

from src.common.constants import ATTRIBUTION_SOURCE_TYPES
from src.common.schemas import CandidateSource, ContextRecord, PollutionRecord
from src.common.utils import clamp
from src.source_attribution.pollutant_signatures import (
    calculate_pollutant_signature_evidence,
)


@dataclass
class EvidenceFusionEngine:
    """
    Weighted fusion of independent evidence channels into final source probabilities.

    Channels
    --------
    - ml_probs          : output of the attribution classifier
    - wind_evidence     : aggregated upwind scores per source type
    - distance_evidence : inverse-distance scores per source type
    - signature_evidence: chemical signature similarity per source type
    - activity_evidence : contextual activity indicators (traffic, construction…)
    """

    w_ml: float = 0.40
    w_wind: float = 0.20
    w_distance: float = 0.15
    w_signature: float = 0.15
    w_activity: float = 0.10

    def fuse(
        self,
        ml_probs: Dict[str, float],
        candidates: Sequence[CandidateSource],
        pollution: PollutionRecord,
        context: Optional[ContextRecord] = None,
    ) -> Dict[str, float]:
        return fuse_source_evidence(
            ml_probs=ml_probs,
            candidates=candidates,
            pollution=pollution,
            context=context,
            weights={
                "ml": self.w_ml,
                "wind": self.w_wind,
                "distance": self.w_distance,
                "signature": self.w_signature,
                "activity": self.w_activity,
            },
        )


def _aggregate_candidate_scores(
    candidates: Sequence[CandidateSource],
    score_attr: str,
) -> Dict[str, float]:
    """Sum / max scores by source_type and normalise to [0,1]."""
    scores: Dict[str, float] = {t: 0.0 for t in ATTRIBUTION_SOURCE_TYPES}
    for c in candidates:
        val = getattr(c, score_attr, 0.0)
        scores[c.source_type] = max(scores.get(c.source_type, 0.0), val)
    total = sum(scores.values())
    if total > 1e-9:
        scores = {k: v / total for k, v in scores.items()}
    return scores


def calculate_wind_evidence(candidates: Sequence[CandidateSource]) -> Dict[str, float]:
    return _aggregate_candidate_scores(candidates, "upwind_score")


def calculate_distance_evidence(
    candidates: Sequence[CandidateSource],
) -> Dict[str, float]:
    # Use candidate_score which already encodes proximity
    return _aggregate_candidate_scores(candidates, "candidate_score")


def _activity_evidence(context: Optional[ContextRecord]) -> Dict[str, float]:
    scores = {t: 0.05 for t in ATTRIBUTION_SOURCE_TYPES}  # small prior
    if context is None:
        return scores
    scores["traffic"] += context.traffic_index * 0.8
    scores["road_dust"] += context.traffic_index * 0.4
    scores["construction"] += context.construction_activity * 0.9
    scores["industrial"] += context.industrial_activity * 0.9
    if context.fire_count_5km > 0:
        scores["waste_burning"] += min(1.0, context.fire_count_5km * 0.3)
        scores["biomass_burning"] += min(1.0, context.fire_count_5km * 0.3)
    total = sum(scores.values())
    if total > 1e-9:
        scores = {k: v / total for k, v in scores.items()}
    return scores


def fuse_source_evidence(
    ml_probs: Dict[str, float],
    candidates: Sequence[CandidateSource],
    pollution: PollutionRecord,
    context: Optional[ContextRecord] = None,
    weights: Optional[Dict[str, float]] = None,
) -> Dict[str, float]:
    """
    Linear opinion pool of evidence channels → calibrated probability vector.
    """
    w = weights or {
        "ml": 0.40,
        "wind": 0.20,
        "distance": 0.15,
        "signature": 0.15,
        "activity": 0.10,
    }
    # Normalise weights
    wsum = sum(w.values())
    w = {k: v / wsum for k, v in w.items()}

    wind_ev = calculate_wind_evidence(candidates)
    dist_ev = calculate_distance_evidence(candidates)
    sig_ev = {
        t: calculate_pollutant_signature_evidence(pollution, t)
        for t in ATTRIBUTION_SOURCE_TYPES
    }
    # Normalise signature evidence
    sig_total = sum(sig_ev.values())
    if sig_total > 1e-9:
        sig_ev = {k: v / sig_total for k, v in sig_ev.items()}
    act_ev = _activity_evidence(context)

    fused: Dict[str, float] = {}
    for t in ATTRIBUTION_SOURCE_TYPES:
        fused[t] = (
            w["ml"] * ml_probs.get(t, 0.0)
            + w["wind"] * wind_ev.get(t, 0.0)
            + w["distance"] * dist_ev.get(t, 0.0)
            + w["signature"] * sig_ev.get(t, 0.0)
            + w["activity"] * act_ev.get(t, 0.0)
        )

    # Renormalise
    total = sum(fused.values())
    if total < 1e-12:
        # Uniform fallback
        n = len(ATTRIBUTION_SOURCE_TYPES)
        return {t: 1.0 / n for t in ATTRIBUTION_SOURCE_TYPES}
    return {k: clamp(v / total, 0.0, 1.0) for k, v in fused.items()}