"""
Source contribution estimation.

Canonical function:
    estimate_source_contributions()

Class:
    ContributionEstimator
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from src.common.schemas import SourceContribution
from src.common.utils import clamp


@dataclass
class ContributionEstimator:
    """
    Convert source probabilities into approximate mass contributions.

    For the MVP we use a simple scaling: contribution ≈ probability × excess
    fraction of the observed pollutant above baseline.  More advanced
    approaches (CMB, PMF) can be swapped in later.
    """

    def estimate(
        self,
        probabilities: Dict[str, float],
        observed: float,
        baseline: float,
    ) -> List[SourceContribution]:
        return estimate_source_contributions(probabilities, observed, baseline)


def estimate_source_contributions(
    probabilities: Dict[str, float],
    observed: float,
    baseline: float,
) -> List[SourceContribution]:
    """
    Produce a list of SourceContribution objects.

    contribution is the estimated fraction of the *excess* pollution
    attributable to each source (sums ≈ 1 for excess; background kept separate).
    """
    excess = max(0.0, observed - baseline)
    excess_fraction = excess / observed if observed > 1e-6 else 0.0

    contributions: List[SourceContribution] = []
    for source_type, prob in sorted(
        probabilities.items(), key=lambda x: x[1], reverse=True
    ):
        # Background absorbs the non-excess portion
        if source_type == "background":
            contrib = clamp(1.0 - excess_fraction, 0.0, 1.0) * prob
        else:
            contrib = excess_fraction * prob
        contributions.append(
            SourceContribution(
                source_type=source_type,
                probability=round(prob, 4),
                contribution=round(contrib, 4),
            )
        )
    return contributions