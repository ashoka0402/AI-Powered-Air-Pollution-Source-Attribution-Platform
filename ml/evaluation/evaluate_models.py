#!/usr/bin/env python3
"""
Evaluate a trained attribution model on a held-out feature set.

Usage:
    python -m ml.evaluation.evaluate_models --model ml/artifacts/attribution_model.joblib
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from sklearn.metrics import classification_report, log_loss, accuracy_score

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.source_attribution.attribution_model import AttributionModel
from src.source_attribution.feature_builder import features_to_matrix


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="ml/artifacts/attribution_model.joblib")
    parser.add_argument("--data", default="data/sample/training_features.json")
    args = parser.parse_args()

    model_path = ROOT / args.model
    data_path = ROOT / args.data

    if not model_path.exists():
        print(f"Model not found: {model_path}")
        print("Train first: python -m ml.training.train_attribution_model")
        return

    model = AttributionModel.load(model_path)
    print(f"Loaded model version={model.model_version} classes={model.classes_}")

    if not data_path.exists():
        print(f"Eval data not found: {data_path}")
        return

    with open(data_path) as f:
        data = json.load(f)
    X = features_to_matrix(data["features"])
    y = np.array(data["labels"])

    y_pred = model.model.predict(X)
    y_proba = model.model.predict_proba(X)

    print("Accuracy:", round(accuracy_score(y, y_pred), 3))
    try:
        print("Log-loss:", round(log_loss(y, y_proba, labels=model.classes_), 3))
    except Exception as e:
        print("Log-loss: n/a", e)
    print(classification_report(y, y_pred, zero_division=0))


if __name__ == "__main__":
    main()