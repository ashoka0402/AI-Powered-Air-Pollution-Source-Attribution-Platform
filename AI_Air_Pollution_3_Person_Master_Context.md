# AI-Powered Air Pollution Source Attribution Platform
## 3-Person Master Context + Code Generation Contract

**Version:** 1.0

> This document is the single source of truth for the team. Every member should give this file to ChatGPT before requesting code and state their role: `PERSON 1`, `PERSON 2`, or `PERSON 3`.

---

# 1. Problem Statement

Indian-city air pollution can change rapidly because of traffic congestion, construction, industrial emissions, waste/biomass burning, road dust, regional transport, and weather.

Existing systems primarily answer:

> How polluted is this location?

This project should additionally answer:

> What are the probable sources of the current pollution event?

The platform continuously combines:

- Low-cost sensor readings
- CPCB/OpenAQ air-quality observations
- Weather and wind
- Traffic movement
- OpenStreetMap/GIS
- Construction activity
- Industrial source information
- Sentinel-5P satellite observations
- NASA FIRMS fire hotspots
- Citizen reports
- Population and sensitive-location data

The platform should:

1. Detect pollution events.
2. Identify probable pollution sources.
3. Estimate source contributions.
4. Calculate attribution confidence.
5. Generate neighbourhood-level exposure warnings.
6. Recommend targeted traffic-management/enforcement actions.
7. Display results through a dashboard.

The system reports **probable attribution**, not absolute causation.

---

# 2. Architecture

```text
                         EXTERNAL DATA SOURCES
                                  |
        +-------------------------+-------------------------+
        |                         |                         |
        v                         v                         v
   AIR QUALITY              CONTEXT DATA              CITIZEN DATA
   CPCB/OpenAQ              Weather/Wind              Reports
   Low-cost sensors         Traffic
                            GIS
                            Satellite
                            Fires
                            Construction
                            Industry
                                  |
                                  v
                         PERSON 1 DATA LAYER
                                  |
                    +-------------+-------------+
                    |                           |
                    v                           v
              Data Cleaning               Geospatial
              Calibration                 Processing
                    |                           |
                    +-------------+-------------+
                                  |
                                  v
                         PostgreSQL + PostGIS
                                  |
                                  v
                         COMMON DATA RECORDS
                                  |
                                  v
                         PERSON 2 AI LAYER
                                  |
                +-----------------+-----------------+
                |                 |                 |
                v                 v                 v
             Baseline        Event Detection    Candidate
             Detection                          Sources
                |                 |                 |
                +-----------------+-----------------+
                                  |
                                  v
                           Evidence Fusion
                                  |
                                  v
                       Source Attribution Result
                                  |
                                  v
                         PERSON 3 APP LAYER
                                  |
                +-----------------+-----------------+
                |                 |                 |
                v                 v                 v
             Exposure       Recommendations     Dashboard
             Warnings           / Actions          Maps
                                  |
                                  v
                              END USERS
```

---

# 3. Non-Negotiable Team Rules

## Rule 1 — Fixed names

If this document defines:

```python
get_current_pollution()
```

nobody creates:

```python
fetch_pollution()
get_pollution_data()
retrieve_pollution()
```

Use the canonical name.

## Rule 2 — No duplicate functionality

Do not independently implement the same shared function in multiple modules.

## Rule 3 — Shared schemas are contracts

If the field is:

```text
pm25
```

do not rename it to `pm_25` or `pm25_value`.

## Rule 4 — API routes are contracts

Use:

```text
GET /api/v1/pollution/current
```

not a newly invented alternative.

## Rule 5 — Do not silently change another person's module

A change crossing ownership boundaries must be discussed first.

## Rule 6 — ChatGPT must follow this document

When generating code, ChatGPT must use this document as the source of truth.

If a required component does not exist, it should clearly state the proposed new name before introducing it.

---

# 4. Team Division

## PERSON 1 — Data Engineering + GIS + Database

Owns:

```text
External Data
    ↓
Ingestion
    ↓
Validation
    ↓
Cleaning
    ↓
Sensor Calibration
    ↓
Spatial Processing
    ↓
PostgreSQL/PostGIS
```

Owns these folders:

```text
src/ingestion/
src/preprocessing/
src/calibration/
src/spatial/
src/database/
```

Does not own:

- ML attribution
- ML training
- React dashboard
- Recommendation logic

---

## PERSON 2 — AI/ML + Event Detection + Source Attribution

Owns:

```text
Clean Data
    ↓
Baseline
    ↓
Anomaly Detection
    ↓
Pollution Event
    ↓
Candidate Sources
    ↓
Wind/Spatial Evidence
    ↓
ML Model
    ↓
Evidence Fusion
    ↓
Attribution + Confidence
```

Owns:

```text
src/event_detection/
src/source_attribution/
src/forecasting/
ml/
```

Does not own:

- external data ingestion
- database infrastructure
- React UI
- dashboard implementation

---

## PERSON 3 — Backend API + Exposure + Recommendations + Frontend

Owns:

```text
Database + AI Results
       ↓
FastAPI
       ↓
Exposure
       ↓
Recommendations
       ↓
React Dashboard
```

Owns:

```text
src/api/
src/exposure/
src/recommendations/
dashboard/
```

Does not own:

- sensor calibration
- external ingestion internals
- ML training
- source-attribution internals

---

# 5. Canonical Project Structure

```text
air-pollution-source-attribution/
│
├── README.md
├── requirements.txt
├── pyproject.toml
├── .env.example
├── .gitignore
├── docker-compose.yml
│
├── configs/
│   ├── app_config.yaml
│   ├── sensor_config.yaml
│   ├── model_config.yaml
│   ├── pollutant_config.yaml
│   └── threshold_config.yaml
│
├── data/
│   ├── raw/
│   │   ├── air_quality/
│   │   ├── sensors/
│   │   ├── weather/
│   │   ├── traffic/
│   │   ├── satellite/
│   │   ├── fires/
│   │   ├── construction/
│   │   ├── industrial/
│   │   └── citizen_reports/
│   ├── processed/
│   ├── features/
│   └── sample/
│
├── src/
│   ├── common/
│   │   ├── constants.py
│   │   ├── schemas.py
│   │   ├── enums.py
│   │   ├── exceptions.py
│   │   └── utils.py
│   │
│   ├── ingestion/
│   │   ├── cpcb_client.py
│   │   ├── openaq_client.py
│   │   ├── weather_client.py
│   │   ├── traffic_client.py
│   │   ├── satellite_client.py
│   │   ├── firms_client.py
│   │   ├── construction_loader.py
│   │   ├── industrial_loader.py
│   │   └── sensor_receiver.py
│   │
│   ├── preprocessing/
│   │   ├── air_quality_cleaner.py
│   │   ├── weather_cleaner.py
│   │   ├── traffic_cleaner.py
│   │   └── quality_control.py
│   │
│   ├── calibration/
│   │   ├── sensor_calibrator.py
│   │   └── calibration_model.py
│   │
│   ├── spatial/
│   │   ├── grid_manager.py
│   │   ├── source_locator.py
│   │   ├── wind_geometry.py
│   │   └── spatial_features.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   ├── models.py
│   │   ├── repositories.py
│   │   └── migrations/
│   │
│   ├── event_detection/
│   │   ├── baseline.py
│   │   ├── anomaly_detector.py
│   │   └── event_detector.py
│   │
│   ├── source_attribution/
│   │   ├── candidate_sources.py
│   │   ├── pollutant_signatures.py
│   │   ├── feature_builder.py
│   │   ├── attribution_model.py
│   │   ├── evidence_fusion.py
│   │   ├── contribution_estimator.py
│   │   └── confidence.py
│   │
│   ├── forecasting/
│   │   └── pollution_forecaster.py
│   │
│   ├── exposure/
│   │   ├── exposure_calculator.py
│   │   └── population_loader.py
│   │
│   ├── recommendations/
│   │   ├── recommendation_engine.py
│   │   └── action_rules.py
│   │
│   └── api/
│       ├── main.py
│       ├── dependencies.py
│       └── routes/
│           ├── pollution.py
│           ├── events.py
│           ├── attribution.py
│           ├── exposure.py
│           ├── recommendations.py
│           └── citizen_reports.py
│
├── ml/
│   ├── training/
│   │   ├── train_event_detector.py
│   │   └── train_attribution_model.py
│   ├── evaluation/
│   │   └── evaluate_models.py
│   └── artifacts/
│
├── dashboard/
│   ├── package.json
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── types/
│   │   └── utils/
│   └── public/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
│
└── docs/
    ├── architecture.md
    ├── api.md
    ├── data_dictionary.md
    ├── model.md
    └── deployment.md
```

---

# 6. File Ownership

## Person 1

```text
src/ingestion/
src/preprocessing/
src/calibration/
src/spatial/
src/database/
```

## Person 2

```text
src/event_detection/
src/source_attribution/
src/forecasting/
ml/
```

## Person 3

```text
src/api/
src/exposure/
src/recommendations/
dashboard/
```

## Shared

```text
src/common/
configs/
tests/
docs/
```

Shared changes require coordination.

---

# 7. Canonical Function Names

## Person 1

### Air quality

```python
fetch_cpcb_air_quality()
fetch_openaq_air_quality()
normalize_air_quality_record()
```

### Weather

```python
fetch_weather_data()
normalize_weather_record()
```

### Traffic

```python
fetch_traffic_data()
normalize_traffic_record()
```

### Satellite

```python
fetch_satellite_observations()
normalize_satellite_record()
```

### Fire

```python
fetch_fire_hotspots()
normalize_fire_record()
```

### Construction / industry

```python
load_construction_sites()
load_industrial_sources()
```

### Sensors

```python
receive_sensor_reading()
normalize_sensor_reading()
```

### Cleaning

```python
clean_air_quality_data()
clean_weather_data()
clean_traffic_data()
run_quality_checks()
```

### Calibration

```python
calibrate_sensor_reading()
fit_sensor_calibration_model()
```

### Spatial

```python
assign_grid_id()
calculate_distance_km()
calculate_upwind_score()
find_candidate_sources()
build_spatial_features()
```

### Database

```python
get_db_session()
save_air_quality_record()
save_weather_record()
save_source_record()
save_pollution_event()
save_attribution_result()
```

---

## Person 2

### Baseline

```python
build_pollution_baseline()
get_expected_concentration()
```

### Detection

```python
detect_pollution_anomaly()
detect_pollution_event()
```

### Candidate sources

```python
generate_candidate_sources()
build_source_features()
```

### ML

```python
train_attribution_model()
predict_source_probabilities()
```

### Evidence

```python
calculate_wind_evidence()
calculate_distance_evidence()
calculate_pollutant_signature_evidence()
fuse_source_evidence()
```

### Attribution

```python
estimate_source_contributions()
calculate_attribution_confidence()
generate_attribution_result()
```

### Forecasting

```python
forecast_pollution()
```

---

## Person 3

### Backend services

```python
get_current_pollution()
get_pollution_history()
get_pollution_events()
get_event_details()
get_event_attribution()
get_neighbourhood_exposure()
get_event_recommendations()
submit_citizen_report()
```

### Exposure

```python
calculate_neighbourhood_exposure()
estimate_exposed_population()
identify_sensitive_locations()
```

### Recommendations

```python
generate_recommendations()
rank_recommended_actions()
```

### Frontend service names

```typescript
fetchCurrentPollution()
fetchPollutionHistory()
fetchPollutionEvents()
fetchEventAttribution()
fetchExposureData()
fetchRecommendations()
submitCitizenReport()
```

---

# 8. Canonical Class Names

## Person 1

```text
CPCBClient
OpenAQClient
WeatherClient
TrafficClient
SatelliteClient
FIRMSClient
SensorReceiver
SensorCalibrator
GridManager
SourceLocator
DatabaseRepository
```

## Person 2

```text
PollutionBaseline
PollutionEventDetector
CandidateSourceEngine
AttributionModel
EvidenceFusionEngine
ContributionEstimator
ConfidenceEstimator
PollutionForecaster
```

## Person 3

```text
ExposureCalculator
RecommendationEngine
PollutionService
EventService
AttributionService
ExposureService
RecommendationService
CitizenReportService
```

---

# 9. Canonical Database Tables

Never rename these without team agreement.

```text
air_quality_readings
sensor_readings
weather_observations
traffic_observations
satellite_observations
fire_hotspots
construction_sites
industrial_sources
citizen_reports
pollution_events
candidate_sources
attribution_results
source_contributions
neighbourhood_exposure
recommendations
```

---

# 10. Canonical Database Fields

## air_quality_readings

```text
id
timestamp
station_id
source
latitude
longitude
pm25
pm10
no2
so2
co
o3
aqi
quality_flag
created_at
```

## sensor_readings

```text
id
timestamp
sensor_id
latitude
longitude
pm25_raw
pm10_raw
pm25_calibrated
pm10_calibrated
temperature
humidity
quality_flag
created_at
```

## weather_observations

```text
id
timestamp
latitude
longitude
temperature
humidity
pressure
wind_speed
wind_direction
precipitation
created_at
```

## traffic_observations

```text
id
timestamp
road_id
latitude
longitude
traffic_index
speed_kmh
congestion_level
created_at
```

## construction_sites

```text
id
site_id
latitude
longitude
permit_id
permit_status
construction_type
active_flag
start_date
expected_end_date
```

## industrial_sources

```text
id
source_id
latitude
longitude
industry_type
operating_status
permit_status
```

## fire_hotspots

```text
id
timestamp
latitude
longitude
confidence
frp
source
```

## citizen_reports

```text
id
timestamp
latitude
longitude
category
description
image_url
credibility_score
status
```

## pollution_events

```text
id
event_id
grid_id
start_time
end_time
pollutant
observed_value
baseline_value
severity
status
```

## candidate_sources

```text
id
event_id
source_id
source_type
distance_km
upwind_score
candidate_score
```

## attribution_results

```text
id
event_id
primary_source_type
confidence
model_version
created_at
```

## source_contributions

```text
id
attribution_result_id
source_type
probability
contribution
```

## neighbourhood_exposure

```text
id
grid_id
timestamp
pm25
pm10
population
sensitive_location_count
exposure_score
exposure_level
```

## recommendations

```text
id
event_id
action_type
priority
reason
expected_impact
responsible_authority
status
created_at
```

---

# 11. Canonical Enum Values

## Source types

```text
traffic
road_dust
construction
industrial
waste_burning
biomass_burning
regional_transport
background
unknown
```

## Pollutants

```text
pm25
pm10
no2
so2
co
o3
```

## Event severity

```text
low
moderate
high
critical
```

## Exposure levels

```text
low
moderate
high
very_high
```

## Recommendation types

```text
traffic_management
construction_inspection
dust_suppression
industrial_inspection
burning_investigation
public_alert
```

---

# 12. Common Data Schemas

## PollutionRecord

```python
{
    "timestamp": "2026-08-29T10:30:00+05:30",
    "grid_id": "G042",
    "latitude": 28.6139,
    "longitude": 77.2090,
    "pm25": 145.2,
    "pm10": 210.4,
    "no2": 72.5,
    "so2": 15.2,
    "co": 1.8,
    "o3": 44.2,
    "aqi": 285,
    "quality_flag": "valid"
}
```

## ContextRecord

```python
{
    "timestamp": "2026-08-29T10:30:00+05:30",
    "grid_id": "G042",
    "wind_speed": 3.2,
    "wind_direction": 245,
    "temperature": 31.4,
    "humidity": 48.2,
    "traffic_index": 0.82,
    "construction_activity": 1.0,
    "industrial_activity": 0.0,
    "fire_count_5km": 0
}
```

## AttributionResult

```python
{
    "event_id": "EVT1042",
    "grid_id": "G042",
    "timestamp": "2026-08-29T10:30:00+05:30",
    "primary_source_type": "construction",
    "confidence": 0.87,
    "model_version": "attribution_v1",
    "sources": [
        {
            "source_type": "construction",
            "probability": 0.64,
            "contribution": 0.48
        },
        {
            "source_type": "road_dust",
            "probability": 0.21,
            "contribution": 0.14
        },
        {
            "source_type": "traffic",
            "probability": 0.09,
            "contribution": 0.07
        }
    ],
    "evidence": [
        "upwind construction site",
        "PM10 spike",
        "dry conditions"
    ]
}
```

---

# 13. API Contract

## Pollution

```http
GET /api/v1/pollution/current
GET /api/v1/pollution/history
GET /api/v1/pollution/grid/{grid_id}
```

## Events

```http
GET /api/v1/events
GET /api/v1/events/{event_id}
```

## Attribution

```http
GET /api/v1/attribution/{event_id}
```

## Exposure

```http
GET /api/v1/exposure/{grid_id}
```

## Recommendations

```http
GET /api/v1/recommendations/{event_id}
```

## Citizen reports

```http
POST /api/v1/reports
GET /api/v1/reports
```

---

# 14. External Data Sources

Recommended sources:

```text
Air quality:
    CPCB
    OpenAQ

Weather:
    Open-Meteo
    ERA5 where appropriate

Road/GIS:
    OpenStreetMap
    Overpass API

Satellite:
    Copernicus Sentinel-5P / TROPOMI

Fire:
    NASA FIRMS

Traffic:
    Approved traffic API
    Government/open traffic datasets

Construction:
    Municipal permit/open-data sources
    Validated project dataset if needed

Industrial:
    CPCB/SPCB/government environmental datasets

Citizen reports:
    This project's own API
```

Do not hard-code external API logic into the AI or frontend.

All external providers should be behind Person 1's ingestion adapters.

---

# 15. Mock Data Contract

To guarantee parallel development, keep these files:

```text
data/sample/
├── sample_air_quality.json
├── sample_weather.json
├── sample_traffic.json
├── sample_sources.json
├── sample_pollution_event.json
├── sample_attribution_result.json
├── sample_exposure.json
└── sample_recommendations.json
```

Person 2 can train/test against sample data while Person 1 builds ingestion.

Person 3 can build the application against sample AI results while Person 2 builds the model.

---

# 16. Parallel Development

```text
                         COMMON CONTRACT
                               |
            +------------------+------------------+
            |                  |                  |
            v                  v                  v
        PERSON 1           PERSON 2           PERSON 3
          DATA               AI                 APP
            |                  |                  |
       Real ingestion      Mock inputs       Mock outputs
            |                  |                  |
            v                  v                  v
        Data API           AI API          Dashboard
            |                  |                  |
            +------------------+------------------+
                               |
                               v
                         INTEGRATION
```

Nobody needs to wait for another person.

---

# 17. Integration Interfaces

Person 1 publishes:

```text
PollutionRecord
ContextRecord
Source records
```

Person 2 consumes those and publishes:

```text
PollutionEvent
AttributionResult
```

Person 3 consumes those and publishes:

```text
ExposureResult
RecommendationResult
API responses
```

The integration chain is:

```text
PERSON 1
   |
   | PollutionRecord + ContextRecord
   v
DATABASE
   |
   v
PERSON 2
   |
   | PollutionEvent + AttributionResult
   v
DATABASE
   |
   v
PERSON 3
   |
   +-- Exposure
   +-- Recommendations
   +-- Dashboard
```

---

# 18. Source Attribution Pipeline

```text
Pollution observations
        |
        v
Baseline calculation
        |
        v
Anomaly detection
        |
        v
Pollution event
        |
        v
Candidate source generation
        |
        +-------------------+
        |                   |
        v                   v
Wind evidence          Spatial evidence
        |                   |
        v                   v
Pollutant signature    Distance/source type
        |                   |
        +---------+---------+
                  |
                  v
             Feature Builder
                  |
                  v
          XGBoost / ML Model
                  |
                  v
         Source probabilities
                  |
                  v
            Evidence Fusion
                  |
                  v
       Source Contributions
                  |
                  v
               Confidence
```

Recommended starting models:

```text
Anomaly detection:
    statistical baseline + Isolation Forest

Source attribution:
    XGBoost

Explainability:
    SHAP
```

---

# 19. Exposure Pipeline

```text
Pollution grid
     +
Population
     +
Sensitive locations
     +
Duration
     |
     v
ExposureCalculator
     |
     +-- estimated population
     +-- sensitive locations
     +-- exposure score
     |
     v
Exposure level
```

---

# 20. Recommendation Pipeline

```text
AttributionResult
       |
       v
RecommendationEngine
       |
       +-----------------------+
       |           |           |
       v           v           v
    Traffic   Construction  Industrial
       |           |           |
       v           v           v
    Traffic    Inspection   Inspection
   management  / dust       / emission
               control      verification
       |
       v
Public/local alert where appropriate
```

Recommendations are decision support. Authorized authorities make final enforcement decisions.

---

# 21. Git Strategy

```text
main
  |
  └── develop
       |
       ├── feature/person1-data
       ├── feature/person2-ai
       └── feature/person3-app
```

Optional sub-branches:

```text
feature/person1-cpcb
feature/person1-sensors
feature/person2-event-detection
feature/person2-attribution
feature/person3-dashboard
feature/person3-exposure
```

Use pull requests into `develop`.

Do not directly push experimental work to `main`.

---

# 22. Change Control

If someone needs a new shared function, field, class, API route, or folder:

```text
Need new component
       |
       v
Search this document
       |
       v
Already exists?
   /          \
 YES          NO
  |            |
Use it      Propose name
               |
               v
          Team agreement
               |
               v
        Update master file
               |
               v
             Code
```

Never silently introduce a new public/shared name.

---

# 23. ChatGPT Code Generation Protocol

Every team member should begin a coding request with:

```text
I am PERSON X.

Use the TEAM MASTER CONTEXT + CODE GENERATION CONTRACT as the single source of truth.

Generate code only for my assigned module.

Follow the exact:
- folder names
- filenames
- function names
- class names
- database tables
- database fields
- enum values
- API routes
- input schemas
- output schemas

Do not rename existing components.
Do not create duplicate functionality.
Do not modify another person's module unless explicitly required by an interface.

If a new shared component is genuinely required, clearly propose its name before implementing it.
```

---

# 24. Person 1 Prompt

Copy/paste:

```text
I am PERSON 1.

Use the TEAM MASTER CONTEXT + CODE GENERATION CONTRACT as the single source of truth.

My responsibility is DATA ENGINEERING + GEO DATA + DATABASE.

Generate the code for:

[TASK]

Use the exact canonical filenames, functions, classes, database tables and schemas.

Do not invent alternative names.

Do not implement Person 2's ML logic.
Do not implement Person 3's frontend.

Tell me:
1. Files to create/change.
2. Complete code.
3. Dependencies.
4. Expected input/output.
5. How it connects to the shared contract.
6. Tests.
```

---

# 25. Person 2 Prompt

Copy/paste:

```text
I am PERSON 2.

Use the TEAM MASTER CONTEXT + CODE GENERATION CONTRACT as the single source of truth.

My responsibility is AI/ML + POLLUTION EVENT DETECTION + SOURCE ATTRIBUTION.

Generate the code for:

[TASK]

Use the exact canonical filenames, functions, classes, source types and AttributionResult schema.

Do not duplicate Person 1's ingestion logic.
Do not modify Person 3's frontend.

Use sample data if the real data pipeline is not ready.

Tell me:
1. Files to create/change.
2. Complete code.
3. Dependencies.
4. Expected input schema.
5. Expected output schema.
6. How Person 3 consumes the result.
7. Tests.
```

---

# 26. Person 3 Prompt

Copy/paste:

```text
I am PERSON 3.

Use the TEAM MASTER CONTEXT + CODE GENERATION CONTRACT as the single source of truth.

My responsibility is BACKEND API + EXPOSURE + RECOMMENDATIONS + FRONTEND.

Generate the code for:

[TASK]

Use the exact canonical API routes, functions, classes, AttributionResult, exposure and recommendation schemas.

Do not create alternative API routes.
Do not implement Person 1's ingestion.
Do not implement Person 2's ML model.

Use sample JSON if upstream modules are not ready.

Tell me:
1. Files to create/change.
2. Complete code.
3. API request/response examples.
4. Frontend integration.
5. Dependencies.
6. Tests.
```

---

# 27. Example

## Person 1 asks

```text
I am PERSON 1.
Create the weather ingestion module.
```

ChatGPT must use:

```text
src/ingestion/weather_client.py
```

and:

```python
fetch_weather_data()
normalize_weather_record()
```

It must not invent:

```text
src/weather/weather_api.py
get_weather()
WeatherFetcher
```

---

## Person 2 asks

```text
I am PERSON 2.
Implement XGBoost source attribution.
```

ChatGPT must use:

```text
src/source_attribution/attribution_model.py
```

and:

```python
train_attribution_model()
predict_source_probabilities()
```

The output must fit `AttributionResult`.

---

## Person 3 asks

```text
I am PERSON 3.
Create the event-attribution API.
```

ChatGPT must use:

```http
GET /api/v1/attribution/{event_id}
```

and return the agreed attribution schema.

---

# 28. 8-Week Work Plan

## Week 1

### Person 1

- Data source research
- Common schemas
- Synthetic data
- Database design

### Person 2

- Attribution methodology
- Source signatures
- Baseline
- Synthetic pollution events

### Person 3

- API contract
- React setup
- Dashboard wireframe

## Week 2

### Person 1

- Air-quality/weather ingestion
- Database
- Cleaning

### Person 2

- Anomaly detection
- Event detection

### Person 3

- Dashboard
- Map
- Pollution charts

## Week 3

### Person 1

- PostGIS
- Grid generation
- Spatial features

### Person 2

- Wind backtracking
- Candidate sources

### Person 3

- Event UI
- Source map

## Week 4

### Person 1

- Traffic
- Construction
- Fire/satellite data

### Person 2

- XGBoost
- Evidence fusion
- Attribution output

### Person 3

- Attribution visualization
- Exposure UI

## Week 5

### Person 1

- Population
- Sensitive locations
- Pipeline improvements

### Person 2

- Contribution estimation
- Confidence
- Evaluation

### Person 3

- Exposure engine
- Recommendation engine

## Week 6

### Person 1

- Automation
- Data refresh
- Monitoring

### Person 2

- Forecasting
- SHAP
- Uncertainty

### Person 3

- Citizen reports
- Alerts
- Government dashboard

## Week 7

All:

```text
End-to-end integration
Testing
Bug fixing
Performance
```

## Week 8

All:

```text
Final testing
Documentation
Demo
Presentation
Research report
```

---

# 29. Integration Checklist

Before merging:

```text
[ ] Correct folder
[ ] Correct filename
[ ] Correct function name
[ ] Correct class name
[ ] Correct schema
[ ] Correct database fields
[ ] Correct API route
[ ] No duplicate functionality
[ ] No hard-coded secrets
[ ] Tests included
[ ] Existing tests pass
[ ] Sample data still works
```

---

# 30. Final End-to-End Test

```text
Low-cost sensor reading
        |
        v
Person 1 ingestion
        |
        v
Cleaning + calibration
        |
        v
PostGIS
        |
        v
Pollution event
        |
        v
Person 2 detection
        |
        v
Candidate sources
        |
        v
Wind + GIS + ML
        |
        v
AttributionResult
        |
        v
Person 3 API
        |
        +----> Exposure
        |
        +----> Recommendations
        |
        v
React Dashboard
```

---

# 31. Final Responsibility Matrix

| Component | Person 1 | Person 2 | Person 3 |
|---|---:|---:|---:|
| CPCB/OpenAQ | OWNER | Consumer | Consumer |
| Sensors | OWNER | Consumer | Consumer |
| Weather | OWNER | Consumer | Consumer |
| Traffic ingestion | OWNER | Consumer | Consumer |
| Satellite ingestion | OWNER | Consumer | Consumer |
| Fire ingestion | OWNER | Consumer | Consumer |
| Construction data | OWNER | Consumer | Consumer |
| Industrial data | OWNER | Consumer | Consumer |
| Database | OWNER | Consumer | Consumer |
| GIS | OWNER | Consumer | Consumer |
| Data cleaning | OWNER | Consumer | - |
| Calibration | OWNER | - | - |
| Event detection | - | OWNER | Consumer |
| Source attribution | - | OWNER | Consumer |
| ML training | - | OWNER | - |
| Evidence fusion | - | OWNER | Consumer |
| Confidence | - | OWNER | Consumer |
| Forecasting | - | OWNER | Consumer |
| FastAPI | - | Consumer | OWNER |
| Exposure | - | Consumer | OWNER |
| Recommendations | - | Consumer | OWNER |
| React dashboard | - | - | OWNER |
| Maps UI | - | - | OWNER |
| Citizen reporting | - | - | OWNER |
| Integration testing | Shared | Shared | Shared |
| Final deployment | Shared | Shared | Shared |

---

# 32. Golden Rule

```text
                  ONE MASTER CONTRACT
                          |
        +-----------------+-----------------+
        |                 |                 |
        v                 v                 v
     PERSON 1          PERSON 2          PERSON 3
       DATA              AI                APP
        |                 |                 |
    Fixed names       Fixed names       Fixed names
    Fixed schemas     Fixed schemas     Fixed APIs
        |                 |                 |
        +-----------------+-----------------+
                          |
                          v
                     INTEGRATION
                          |
                          v
                    FINAL PROJECT
```

The objective is not for all three members to write the same kind of code.

The objective is for all three members to write **different code that fits exactly into the same system**.

---

# 33. Mandatory ChatGPT Behavior

When a team member asks ChatGPT for code:

1. Identify whether they are Person 1, 2, or 3.
2. Restrict implementation to that person's ownership.
3. Use this document's canonical names.
4. Reuse existing interfaces.
5. Never silently rename shared components.
6. Never duplicate another person's functionality.
7. Generate code that can be merged into the canonical directory.
8. Include tests.
9. State files created/modified.
10. If a contract change is necessary, flag it explicitly before introducing it.

If no person is specified, ask:

```text
Which team member are you?

1. Person 1 — Data Engineering + GIS + Database
2. Person 2 — AI/ML + Source Attribution
3. Person 3 — Backend + Exposure + Recommendations + Dashboard
```
