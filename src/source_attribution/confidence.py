"""
Attribution confidence scoring.

Canonical function:
    calculate_attribution_confidence()

Class:
    ConfidenceEstimator
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence

from src.common.constants import MAX_CONFIDENCE, MIN_CONFIDENCE
from src.common.schemas import CandidateSource, ContextRecord
from src.common.utils import clamp


@dataclass
class ConfidenceEstimator:
    def calculate(
        self,
        probabilities: Dict[str, float],
        candidates: Sequence[CandidateSource],
        context: Optional[ContextRecord] = None,
        evidence_items: Optional[List[str]] = None,
    ) -> float:
        return calculate_attribution_confidence(
            probabilities, candidates, context, evidence_items
        )


def calculate_attribution_confidence(
    probabilities: Dict[str, float],
    candidates: Sequence[CandidateSource],
    context: Optional[ContextRecord] = None,
    evidence_items: Optional[List[str]] = None,
) -> float:
    """
    Heuristic confidence score in [MIN_CONFIDENCE, MAX_CONFIDENCE].

    Factors considered:
    - Peak probability (how decisive the distribution is)
    - Number of supporting candidates
    - Strength of top upwind score
    - Availability of wind / activity context
    - Number of independent evidence statements
    """
    if not probabilities:
        return MIN_CONFIDENCE

    probs = sorted(probabilities.values(), reverse=True)
    top = probs[0]
    second = probs[1] if len(probs) > 1 else 0.0
    margin = top - second

    # Base from peak + margin
    base = 0.35 * top + 0.25 * margin

    # Candidate support
    n_cand = len(candidates)
    cand_factor = min(1.0, n_cand / 5.0) * 0.15
    top_upwind = max((c.upwind_score for c in candidates), default=0.0)
    upwind_factor = top_upwind * 0.15

    # Context availability
    ctx_factor = 0.0
    if context is not None:
        ctx_factor += 0.05
        if context.wind_speed > 0.5:
            ctx_factor += 0.05
        if context.traffic_index > 0 or context.construction_activity > 0:
            ctx_factor += 0.05

    # Evidence count
    n_ev = len(evidence_items or [])
    evidence_factor = min(0.10, n_ev * 0.025)

    confidence = base + cand_factor + upwind_factor + ctx_factor + evidence_factor
    return round(clamp(confidence, MIN_CONFIDENCE, MAX_CONFIDENCE), 3)