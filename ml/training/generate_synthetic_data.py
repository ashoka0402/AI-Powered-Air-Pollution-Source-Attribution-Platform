#!/usr/bin/env python3
"""Generate reproducible synthetic training data for source attribution.

Run from project root:
    python -m ml.training.generate_synthetic_data --samples 10000
"""

import argparse
import json
import random
from pathlib import Path

from src.source_attribution.feature_builder import FEATURE_COLUMNS
from src.common.constants import ATTRIBUTION_SOURCE_TYPES

ROOT = Path(__file__).resolve().parents[2]

# Illustrative pollutant signatures, not real-world measured distributions.
SIGNATURES = {
    "traffic": {"pm25": 0.35, "pm10": 0.25, "no2": 0.55, "so2": 0.10, "co": 0.40},
    "road_dust": {"pm25": 0.40, "pm10": 0.70, "no2": 0.10, "so2": 0.05, "co": 0.05},
    "construction": {"pm25": 0.45, "pm10": 0.75, "no2": 0.15, "so2": 0.10, "co": 0.10},
    "industrial": {"pm25": 0.30, "pm10": 0.35, "no2": 0.30, "so2": 0.60, "co": 0.20},
    "waste_burning": {"pm25": 0.65, "pm10": 0.50, "no2": 0.20, "so2": 0.25, "co": 0.45},
    "biomass_burning": {"pm25": 0.70, "pm10": 0.55, "no2": 0.15, "so2": 0.15, "co": 0.50},
    "regional_transport": {"pm25": 0.50, "pm10": 0.40, "no2": 0.25, "so2": 0.20, "co": 0.20},
    "background": {"pm25": 0.20, "pm10": 0.20, "no2": 0.15, "so2": 0.10, "co": 0.10},
    "unknown": {"pm25": 0.25, "pm10": 0.25, "no2": 0.20, "so2": 0.15, "co": 0.15},
}


def clamp(value, low, high):
    return max(low, min(high, value))


def noisy(value, rng, noise=0.12):
    return max(0.0, value + rng.gauss(0, noise))


def generate_one(label, rng):
    """Generate one feature row with class-dependent correlations."""
    feat = {name: 0.0 for name in FEATURE_COLUMNS}
    signature = SIGNATURES[label]
    strength = rng.uniform(0.65, 1.35)
    feat["wind_speed"] = rng.uniform(0.2, 8.0)

    # Illustrative scales only; calibrate against measured data before deployment.
    scales = {"pm25": 100, "pm10": 160, "no2": 100, "so2": 80, "co": 8}
    for pollutant, weight in signature.items():
        feat[pollutant] = noisy(
            scales[pollutant] * weight * strength,
            rng,
            scales[pollutant] * 0.08,
        )

    feat["pm25_excess"] = noisy(feat["pm25"] * rng.uniform(0.45, 0.95), rng, 5)
    feat["pm10_excess"] = noisy(feat["pm10"] * rng.uniform(0.45, 0.95), rng, 8)

    activity = rng.uniform(0.55, 1.0)
    if label == "traffic":
        feat["traffic_index"] = activity
        feat["sig_traffic"] = rng.uniform(0.55, 1.0)
    elif label == "road_dust":
        feat["traffic_index"] = rng.uniform(0.3, 0.8)
        feat["sig_road_dust"] = rng.uniform(0.55, 1.0)
    elif label == "construction":
        feat["construction_activity"] = activity
        feat["sig_construction"] = rng.uniform(0.55, 1.0)
    elif label == "industrial":
        feat["industrial_activity"] = activity
        feat["sig_industrial"] = rng.uniform(0.55, 1.0)
    elif label == "waste_burning":
        feat["fire_count_5km"] = rng.randint(1, 8)
        feat["sig_waste_burning"] = rng.uniform(0.55, 1.0)
    elif label == "biomass_burning":
        feat["fire_count_5km"] = rng.randint(1, 10)
        feat["sig_biomass_burning"] = rng.uniform(0.55, 1.0)
    elif label == "regional_transport":
        feat["nearest_candidate_score"] = rng.uniform(0.1, 0.55)
        feat["nearest_upwind_score"] = rng.uniform(0.1, 0.6)
    elif label == "background":
        feat["nearest_candidate_score"] = rng.uniform(0.0, 0.2)
        feat["nearest_upwind_score"] = rng.uniform(0.0, 0.2)
    else:  # unknown: weak or conflicting evidence
        feat["nearest_candidate_score"] = rng.uniform(0.0, 0.45)
        feat["nearest_upwind_score"] = rng.uniform(0.0, 0.45)

    # Add noise to context values so each class is not perfectly separable.
    for name in ("traffic_index", "construction_activity", "industrial_activity"):
        feat[name] = clamp(noisy(feat[name], rng, 0.12), 0, 1)

    feat["fire_count_5km"] = max(0, int(round(noisy(feat["fire_count_5km"], rng, 1.0))))
    for name in ("nearest_candidate_score", "nearest_upwind_score"):
        feat[name] = clamp(noisy(feat[name], rng, 0.12), 0, 1)
    feat["nearest_distance_km"] = rng.uniform(0.2, 15.0)

    signal_names = (
        "sig_traffic", "sig_road_dust", "sig_construction",
        "sig_industrial", "sig_waste_burning", "sig_biomass_burning",
    )
    for name in signal_names:
        feat[name] = clamp(noisy(feat[name], rng, 0.08), 0, 1)

    return feat


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic attribution training data")
    parser.add_argument("--samples", type=int, default=10000, help="Total rows to generate")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    parser.add_argument("--out", default="data/sample/training_features.json", help="Output JSON path")
    args = parser.parse_args()

    if args.samples < len(ATTRIBUTION_SOURCE_TYPES) * 10:
        parser.error(f"--samples must be at least {len(ATTRIBUTION_SOURCE_TYPES) * 10}")

    missing = set(ATTRIBUTION_SOURCE_TYPES) - set(SIGNATURES)
    if missing:
        parser.error(f"Missing synthetic signatures for: {sorted(missing)}")

    rng = random.Random(args.seed)
    features, labels = [], []
    per_class, remainder = divmod(args.samples, len(ATTRIBUTION_SOURCE_TYPES))

    for i, label in enumerate(ATTRIBUTION_SOURCE_TYPES):
        count = per_class + (1 if i < remainder else 0)
        for _ in range(count):
            features.append(generate_one(label, rng))
            labels.append(label)

    combined = list(zip(features, labels))
    rng.shuffle(combined)
    features, labels = map(list, zip(*combined))

    output_path = ROOT / args.out
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "metadata": {
            "dataset_type": "synthetic",
            "warning": "Illustrative synthetic data, not real measurements or evidence of real-world accuracy.",
            "seed": args.seed,
            "samples": len(features),
            "classes": ATTRIBUTION_SOURCE_TYPES,
            "features": FEATURE_COLUMNS,
        },
        "features": features,
        "labels": labels,
    }
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"Generated {len(features):,} synthetic rows")
    print(f"Classes: {len(ATTRIBUTION_SOURCE_TYPES)} | Features per row: {len(FEATURE_COLUMNS)}")
    print(f"Output: {output_path}")
    print("Class counts:")
    for label in ATTRIBUTION_SOURCE_TYPES:
        print(f"  {label}: {labels.count(label)}")


if __name__ == "__main__":
    main()
