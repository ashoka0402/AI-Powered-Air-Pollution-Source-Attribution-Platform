"""
Short-term pollution forecasting.

Canonical function:
    forecast_pollution()

Class:
    PollutionForecaster
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional, Sequence

import numpy as np

try:
    from sklearn.ensemble import GradientBoostingRegressor
    _SKLEARN_AVAILABLE = True
except ImportError:
    GradientBoostingRegressor = None  # type: ignore
    _SKLEARN_AVAILABLE = False

from src.common.constants import FORECASTER_VERSION
from src.common.schemas import ForecastResult, PollutionRecord
from src.common.utils import rolling_mean


@dataclass
class PollutionForecaster:
    """
    Simple multi-horizon forecaster.

    MVP approach:
    - Persistence baseline
    - Gradient boosting on lagged features + time-of-day
    - Simple residual-based uncertainty bands
    """

    model: Optional[GradientBoostingRegressor] = None
    pollutant: str = "pm25"
    model_version: str = FORECASTER_VERSION
    residual_std: float = 15.0  # default uncertainty

    def fit(self, records: Sequence[PollutionRecord], lag: int = 6) -> None:
        """Fit on historical records (expects chronological order)."""
        values = [
            getattr(r, self.pollutant)
            for r in records
            if getattr(r, self.pollutant) is not None
        ]
        if len(values) < lag + 20 or not _SKLEARN_AVAILABLE:
            # Not enough data or no sklearn – stay with persistence
            self.model = None
            self.residual_std = float(np.std(values)) if values else 15.0
            return

        X, y = [], []
        for i in range(lag, len(values)):
            window = values[i - lag : i]
            hour = records[i].timestamp.hour
            dow = records[i].timestamp.weekday()
            X.append(window + [hour, dow])
            y.append(values[i])

        X = np.asarray(X)
        y = np.asarray(y)
        self.model = GradientBoostingRegressor(
            n_estimators=80, max_depth=3, learning_rate=0.1, random_state=42
        )
        self.model.fit(X, y)
        preds = self.model.predict(X)
        self.residual_std = float(np.std(y - preds)) or 10.0

    def predict(
        self,
        recent: Sequence[PollutionRecord],
        horizon_hours: int = 24,
        lag: int = 6,
    ) -> List[ForecastResult]:
        return forecast_pollution(
            recent,
            horizon_hours=horizon_hours,
            pollutant=self.pollutant,
            model=self.model,
            residual_std=self.residual_std,
            model_version=self.model_version,
            lag=lag,
        )


def forecast_pollution(
    recent: Sequence[PollutionRecord],
    horizon_hours: int = 24,
    pollutant: str = "pm25",
    model: Optional[GradientBoostingRegressor] = None,
    residual_std: float = 15.0,
    model_version: str = FORECASTER_VERSION,
    lag: int = 6,
) -> List[ForecastResult]:
    """
    Produce horizon-hour forecasts for a grid.

    Uses the trained model if available; otherwise falls back to persistence
    (last observed value) with expanding uncertainty.
    """
    if not recent:
        return []

    ordered = sorted(recent, key=lambda r: r.timestamp)
    values = [
        float(getattr(r, pollutant))
        for r in ordered
        if getattr(r, pollutant) is not None
    ]
    if not values:
        return []

    last_ts = ordered[-1].timestamp
    grid_id = ordered[-1].grid_id
    last_val = values[-1]

    results: List[ForecastResult] = []
    history = list(values[-lag:]) if len(values) >= lag else list(values)

    for h in range(1, horizon_hours + 1):
        if model is not None and len(history) >= lag:
            hour = (last_ts + timedelta(hours=h)).hour
            dow = (last_ts + timedelta(hours=h)).weekday()
            feat = np.array(history[-lag:] + [hour, dow]).reshape(1, -1)
            pred = float(model.predict(feat)[0])
        else:
            # Persistence + mild mean-reversion toward rolling mean
            roll = float(np.mean(history[-min(12, len(history)) :]))
            pred = 0.7 * last_val + 0.3 * roll

        # Uncertainty grows with horizon
        band = residual_std * (1.0 + 0.08 * h)
        results.append(
            ForecastResult(
                grid_id=grid_id,
                pollutant=pollutant,
                forecast_horizon_hours=h,
                predicted_value=round(max(0.0, pred), 2),
                lower_bound=round(max(0.0, pred - 1.28 * band), 2),  # ~80% band
                upper_bound=round(pred + 1.28 * band, 2),
                model_version=model_version,
                timestamp=last_ts + timedelta(hours=h),
            )
        )
        history.append(pred)
        last_val = pred

    return results