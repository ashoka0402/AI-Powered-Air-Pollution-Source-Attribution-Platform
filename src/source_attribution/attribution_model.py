"""
ML attribution model (Random Forest / Gradient Boosting).

Canonical functions:
    train_attribution_model()
    predict_source_probabilities()

Class:
    AttributionModel
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

try:
    import joblib
    from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
    from sklearn.calibration import CalibratedClassifierCV
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report, log_loss
    _SKLEARN_AVAILABLE = True
except ImportError:  # allows demo/pipeline to run without sklearn installed
    joblib = None  # type: ignore
    _SKLEARN_AVAILABLE = False

from src.common.constants import ATTRIBUTION_SOURCE_TYPES, MODEL_VERSION
from src.common.exceptions import ModelNotLoadedError
from src.source_attribution.feature_builder import (
    FEATURE_COLUMNS,
    features_to_matrix,
    features_to_vector,
)


@dataclass
class AttributionModel:
    model: Any = None
    classes_: List[str] = field(default_factory=list)
    feature_columns: List[str] = field(default_factory=lambda: list(FEATURE_COLUMNS))
    model_version: str = MODEL_VERSION
    trained: bool = False

    def predict_proba(self, features: Dict[str, float]) -> Dict[str, float]:
        if not self.trained or self.model is None:
            raise ModelNotLoadedError("Attribution model has not been trained or loaded")
        vec = features_to_vector(features).reshape(1, -1)
        proba = self.model.predict_proba(vec)[0]
        return {cls: float(p) for cls, p in zip(self.classes_, proba)}

    def save(self, path: str | Path) -> None:
        if not _SKLEARN_AVAILABLE or joblib is None:
            raise ModelNotLoadedError("joblib/sklearn not installed — cannot save model")
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(
            {
                "model": self.model,
                "classes_": self.classes_,
                "feature_columns": self.feature_columns,
                "model_version": self.model_version,
            },
            path,
        )

    @classmethod
    def load(cls, path: str | Path) -> "AttributionModel":
        if not _SKLEARN_AVAILABLE or joblib is None:
            raise ModelNotLoadedError("joblib/sklearn not installed — cannot load model")
        path = Path(path)
        if not path.exists():
            raise ModelNotLoadedError(f"Model artifact not found: {path}")
        data = joblib.load(path)
        obj = cls(
            model=data["model"],
            classes_=data["classes_"],
            feature_columns=data.get("feature_columns", list(FEATURE_COLUMNS)),
            model_version=data.get("model_version", MODEL_VERSION),
            trained=True,
        )
        return obj


def train_attribution_model(
    feature_dicts: Sequence[Dict[str, float]],
    labels: Sequence[str],
    model_type: str = "gbm",
    test_size: float = 0.2,
    random_state: int = 42,
    calibrate: bool = True,
) -> Tuple[AttributionModel, Dict[str, Any]]:
    """
    Train a multi-class source attribution model.

    Parameters
    ----------
    feature_dicts : list of feature dictionaries (from build_source_features)
    labels : corresponding source_type labels
    model_type : "rf" | "gbm"
    """
    if not _SKLEARN_AVAILABLE:
        raise ModelNotLoadedError(
            "scikit-learn is required to train the attribution model. "
            "Install with: pip install scikit-learn joblib"
        )
    if len(feature_dicts) != len(labels):
        raise ValueError("feature_dicts and labels must have the same length")
    if len(feature_dicts) < 10:
        raise ValueError("Need at least 10 labelled examples to train")

    X = features_to_matrix(list(feature_dicts))
    y = np.array(labels)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    if model_type == "rf":
        base = RandomForestClassifier(
            n_estimators=200,
            max_depth=12,
            min_samples_leaf=3,
            class_weight="balanced",
            random_state=random_state,
            n_jobs=-1,
        )
    else:
        base = GradientBoostingClassifier(
            n_estimators=150,
            max_depth=5,
            learning_rate=0.08,
            random_state=random_state,
        )

    if calibrate and len(np.unique(y_train)) > 1:
        clf = CalibratedClassifierCV(base, method="isotonic", cv=3)
    else:
        clf = base

    clf.fit(X_train, y_train)

    # Metrics
    y_pred = clf.predict(X_test)
    y_proba = clf.predict_proba(X_test)
    report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
    try:
        ll = float(log_loss(y_test, y_proba, labels=clf.classes_))
    except Exception:
        ll = None

    metrics = {
        "classification_report": report,
        "log_loss": ll,
        "n_train": len(X_train),
        "n_test": len(X_test),
        "classes": list(clf.classes_),
    }

    model = AttributionModel(
        model=clf,
        classes_=list(clf.classes_),
        trained=True,
        model_version=MODEL_VERSION,
    )
    return model, metrics


def predict_source_probabilities(
    model: AttributionModel,
    features: Dict[str, float],
) -> Dict[str, float]:
    """Canonical inference helper."""
    return model.predict_proba(features)