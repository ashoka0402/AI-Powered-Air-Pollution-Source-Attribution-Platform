"""Utility helpers used by event detection and attribution modules."""

from __future__ import annotations

import math
from datetime import datetime, timedelta
from typing import Iterable, List, Optional, Sequence, Tuple

import numpy as np


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in kilometres."""
    r = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    )
    return 2 * r * math.asin(math.sqrt(a))


def bearing_degrees(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Initial bearing from point 1 to point 2 (0–360, degrees)."""
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dlambda = math.radians(lon2 - lon1)
    x = math.sin(dlambda) * math.cos(phi2)
    y = math.cos(phi1) * math.sin(phi2) - math.sin(phi1) * math.cos(phi2) * math.cos(
        dlambda
    )
    bearing = math.degrees(math.atan2(x, y))
    return (bearing + 360) % 360


def angular_difference(a: float, b: float) -> float:
    """Smallest absolute angular difference in degrees (0–180)."""
    diff = abs(a - b) % 360
    return min(diff, 360 - diff)


def wind_alignment_score(
    wind_direction: float,
    source_bearing: float,
    tolerance_deg: float = 45.0,
) -> float:
    """
    Score how well the source lies upwind of the receptor.

    Wind direction is meteorological (direction FROM which the wind blows).
    A source is upwind when its bearing is opposite to the wind direction.
    Returns 1.0 (perfectly upwind) → 0.0 (outside tolerance).
    """
    # Direction toward which the wind is blowing
    downwind = (wind_direction + 180) % 360
    # Source is upwind if its bearing from receptor is close to the opposite of downwind
    # i.e. bearing from receptor to source ≈ wind_direction (source is where wind comes from)
    diff = angular_difference(wind_direction, source_bearing)
    if diff >= tolerance_deg:
        return 0.0
    return max(0.0, 1.0 - (diff / tolerance_deg))


def zscore(value: float, mean: float, std: float) -> float:
    if std is None or std <= 1e-9:
        return 0.0
    return (value - mean) / std


def clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def safe_divide(a: float, b: float, default: float = 0.0) -> float:
    if b is None or abs(b) < 1e-12:
        return default
    return a / b


def rolling_mean(values: Sequence[float], window: int) -> List[float]:
    if not values or window <= 0:
        return []
    arr = np.asarray(values, dtype=float)
    if len(arr) < window:
        return [float(np.nanmean(arr[: i + 1])) for i in range(len(arr))]
    out = []
    for i in range(len(arr)):
        start = max(0, i - window + 1)
        out.append(float(np.nanmean(arr[start : i + 1])))
    return out


def generate_event_id(grid_id: str, timestamp: datetime) -> str:
    ts = timestamp.strftime("%Y%m%d%H%M")
    return f"EVT-{grid_id}-{ts}"


def parse_iso(ts: str) -> datetime:
    """Parse ISO-8601 timestamps, tolerating trailing Z."""
    if ts.endswith("Z"):
        ts = ts[:-1] + "+00:00"
    return datetime.fromisoformat(ts)