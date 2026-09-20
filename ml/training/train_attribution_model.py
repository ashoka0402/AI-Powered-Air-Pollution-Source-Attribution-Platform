#!/usr/bin/env python3
"""
Train the source-attribution model and save the artifact.

Usage (from project root):
    python -m ml.training.train_attribution_model
    python ml/training/train_attribution_model.py --data data/sample/training_features.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Allow running as script
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.source_attribution.attribution_model import train_attribution_model, AttributionModel


def load_training_data(path: Path):
    with open(path) as f:
        data = json.load(f)
    features = data["features"]
    labels = data["labels"]
    return features, labels


def main():
    parser = argparse.ArgumentParser(description="Train attribution model")
    parser.add_argument(
        "--data",
        type=str,
        default="data/sample/training_features.json",
        help="Path to JSON with 'features' and 'labels' keys",
    )
    parser.add_argument(
        "--model-type",
        choices=["rf", "gbm"],
        default="gbm",
        help="Base estimator type",
    )
    parser.add_argument(
        "--out",
        type=str,
        default="ml/artifacts/attribution_model.joblib",
        help="Output path for the trained model",
    )
    args = parser.parse_args()

    data_path = ROOT / args.data
    if not data_path.exists():
        print(f"[WARN] Training data not found at {data_path}")
        print("Generating synthetic training set for demo…")
        features, labels = _synthetic_data()
    else:
        features, labels = load_training_data(data_path)

    print(f"Training on {len(features)} examples…")
    model, metrics = train_attribution_model(
        features, labels, model_type=args.model_type
    )

    out_path = ROOT / args.out
    model.save(out_path)
    print(f"Model saved → {out_path}")
    print(f"Classes: {metrics['classes']}")
    print(f"Log-loss: {metrics.get('log_loss')}")
    report = metrics["classification_report"]
    if "weighted avg" in report:
        print(f"Weighted F1: {report['weighted avg']['f1-score']:.3f}")


def _synthetic_data(n: int = 400):
    """Create a small synthetic labelled set so the script always runs."""
    import random
    from src.source_attribution.feature_builder import FEATURE_COLUMNS
    from src.common.constants import ATTRIBUTION_SOURCE_TYPES

    random.seed(42)
    features, labels = [], []
    for _ in range(n):
        label = random.choice(ATTRIBUTION_SOURCE_TYPES[:6])  # skip unknown/background rarely
        feat = {c: random.random() for c in FEATURE_COLUMNS}
        # Inject weak signal
        if label == "construction":
            feat["construction_activity"] = random.uniform(0.6, 1.0)
            feat["sig_construction"] = random.uniform(0.5, 0.95)
            feat["pm10_excess"] = random.uniform(40, 120)
        elif label == "traffic":
            feat["traffic_index"] = random.uniform(0.5, 1.0)
            feat["sig_traffic"] = random.uniform(0.4, 0.9)
            feat["no2"] = random.uniform(40, 100)
        elif label == "industrial":
            feat["industrial_activity"] = random.uniform(0.5, 1.0)
            feat["sig_industrial"] = random.uniform(0.4, 0.9)
            feat["so2"] = random.uniform(20, 80)
        features.append(feat)
        labels.append(label)
    return features, labels


if __name__ == "__main__":
    main()