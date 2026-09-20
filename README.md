# Person 2 – AI / ML Layer

**AI-Powered Air Pollution Source-Attribution Platform**

This package contains everything owned by **Person 2**:

| Folder | Responsibility |
|--------|----------------|
| `src/event_detection/` | Baseline, anomaly & pollution-event detection |
| `src/source_attribution/` | Candidate sources, ML model, evidence fusion, contribution & confidence |
| `src/forecasting/` | Short-term PM forecasts |
| `ml/` | Training & evaluation scripts + model artifacts |
| `configs/` | Model & threshold YAML configs |
| `data/sample/` | Mock data so development can proceed without Person 1 |

## Canonical functions (must not be renamed)

```python
build_pollution_baseline()
get_expected_concentration()
detect_pollution_anomaly()
detect_pollution_event()
generate_candidate_sources()
build_source_features()
train_attribution_model()
predict_source_probabilities()
calculate_wind_evidence()
calculate_distance_evidence()
calculate_pollutant_signature_evidence()
fuse_source_evidence()
estimate_source_contributions()
calculate_attribution_confidence()
generate_attribution_result()
forecast_pollution()
```

## Quick start

```bash
# install deps
pip install -r requirements.txt

# run end-to-end demo (uses sample data, no trained model required)
python demo_person2_pipeline.py

# train attribution model on synthetic / sample features
python -m ml.training.train_attribution_model

# evaluate
python -m ml.evaluation.evaluate_models

# unit tests
pytest tests/unit -q
```

## Integration contract

**Inputs** (from Person 1 / DB):

- `PollutionRecord`
- `ContextRecord`
- `SourceRecord`

**Outputs** (written to DB / consumed by Person 3):

- `PollutionEvent`
- `AttributionResult`
- `ForecastResult`

See `src/common/schemas.py` for exact field names.

## Pipeline overview

```
PollutionRecords
      │
      ▼
build_pollution_baseline()
      │
      ▼
detect_pollution_event()  →  PollutionEvent
      │
      ▼
generate_candidate_sources()  (+ wind geometry)
      │
      ▼
build_source_features()
      │
      ▼
predict_source_probabilities()  (ML)
      │
      ▼
fuse_source_evidence()  (ML + wind + distance + signature + activity)
      │
      ▼
estimate_source_contributions()
calculate_attribution_confidence()
      │
      ▼
AttributionResult
```

## Notes for the team

- All external data ingestion stays with **Person 1**.
- All FastAPI routes and React UI stay with **Person 3**.
- Shared schemas live in `src/common/` – coordinate any field changes.
- Model artifacts go under `ml/artifacts/` (git-ignored in a full repo).
