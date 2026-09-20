"""
Candidate source generation.

Canonical function:
    generate_candidate_sources()

Class:
    CandidateSourceEngine
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Sequence

from src.common.constants import MAX_CANDIDATE_DISTANCE_KM, UPWIND_ANGLE_TOLERANCE_DEG
from src.common.schemas import CandidateSource, ContextRecord, PollutionEvent, SourceRecord
from src.common.utils import haversine_km, bearing_degrees, wind_alignment_score


@dataclass
class CandidateSourceEngine:
    max_distance_km: float = MAX_CANDIDATE_DISTANCE_KM
    upwind_tolerance_deg: float = UPWIND_ANGLE_TOLERANCE_DEG

    def generate(
        self,
        event: PollutionEvent,
        sources: Sequence[SourceRecord],
        context: Optional[ContextRecord] = None,
    ) -> List[CandidateSource]:
        return generate_candidate_sources(
            event=event,
            sources=sources,
            context=context,
            max_distance_km=self.max_distance_km,
            upwind_tolerance_deg=self.upwind_tolerance_deg,
        )


def generate_candidate_sources(
    event: PollutionEvent,
    sources: Sequence[SourceRecord],
    context: Optional[ContextRecord] = None,
    max_distance_km: float = MAX_CANDIDATE_DISTANCE_KM,
    upwind_tolerance_deg: float = UPWIND_ANGLE_TOLERANCE_DEG,
) -> List[CandidateSource]:
    """
    Produce a ranked list of CandidateSource objects for a pollution event.

    Ranking combines inverse-distance and wind-alignment (upwind) scores.
    """
    if event.latitude is None or event.longitude is None:
        # Cannot compute spatial candidates without receptor location
        return []

    wind_dir = context.wind_direction if context else 0.0
    candidates: List[CandidateSource] = []

    for src in sources:
        if not src.active_flag:
            continue
        dist = haversine_km(
            event.latitude, event.longitude, src.latitude, src.longitude
        )
        if dist > max_distance_km:
            continue

        source_bearing = bearing_degrees(
            event.latitude, event.longitude, src.latitude, src.longitude
        )
        upwind = wind_alignment_score(
            wind_dir, source_bearing, tolerance_deg=upwind_tolerance_deg
        )

        # Simple candidate score: distance proximity × (0.4 + 0.6 * upwind)
        proximity = max(0.0, 1.0 - (dist / max_distance_km))
        score = proximity * (0.4 + 0.6 * upwind)

        candidates.append(
            CandidateSource(
                event_id=event.event_id,
                source_id=src.source_id,
                source_type=src.source_type,
                distance_km=round(dist, 3),
                upwind_score=round(upwind, 3),
                candidate_score=round(score, 4),
                latitude=src.latitude,
                longitude=src.longitude,
            )
        )

    candidates.sort(key=lambda c: c.candidate_score, reverse=True)
    return candidates