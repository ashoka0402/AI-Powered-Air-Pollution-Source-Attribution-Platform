"""
Pollutant chemical-signature evidence.

Canonical function:
    calculate_pollutant_signature_evidence()
"""

from __future__ import annotations

from typing import Dict, Optional

import numpy as np

from src.common.constants import POLLUTANT_SIGNATURES
from src.common.schemas import PollutionRecord


def _normalise_vector(vec: Dict[str, float]) -> Dict[str, float]:
    total = sum(max(0.0, v) for v in vec.values())
    if total < 1e-9:
        return {k: 0.0 for k in vec}
    return {k: max(0.0, v) / total for k, v in vec.items()}


def _cosine_similarity(a: Dict[str, float], b: Dict[str, float]) -> float:
    keys = set(a) | set(b)
    va = np.array([a.get(k, 0.0) for k in keys], dtype=float)
    vb = np.array([b.get(k, 0.0) for k in keys], dtype=float)
    na = np.linalg.norm(va)
    nb = np.linalg.norm(vb)
    if na < 1e-12 or nb < 1e-12:
        return 0.0
    return float(np.dot(va, vb) / (na * nb))


def calculate_pollutant_signature_evidence(
    record: PollutionRecord,
    source_type: str,
    signatures: Optional[Dict[str, Dict[str, float]]] = None,
) -> float:
    """
    Compare the observed pollutant mix against a known source signature.

    Returns a similarity score in [0, 1].
    """
    signatures = signatures or POLLUTANT_SIGNATURES
    sig = signatures.get(source_type)
    if not sig:
        return 0.0

    observed = {
        "pm25": record.pm25 or 0.0,
        "pm10": record.pm10 or 0.0,
        "no2": record.no2 or 0.0,
        "so2": record.so2 or 0.0,
        "co": record.co or 0.0,
    }
    # Drop species that are completely missing (all zero) to avoid bias
    observed = {k: v for k, v in observed.items() if v > 0}
    if not observed:
        return 0.0

    obs_norm = _normalise_vector(observed)
    sig_norm = _normalise_vector({k: sig.get(k, 0.0) for k in observed})
    sim = _cosine_similarity(obs_norm, sig_norm)
    return float(max(0.0, min(1.0, sim)))