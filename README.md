# AI-Powered Air Pollution Source-Attribution Platform
## Full Project Work Report, Data Sources, Architecture, Team Division and Execution Plan

**Team size:** 3 members  
**Recommended project type:** Final-year / capstone / research prototype  
**Primary objective:** Build a platform that continuously combines air-quality sensors, weather/wind, traffic, satellite observations, construction/industrial information and citizen reports to identify probable pollution sources in near real time, estimate neighbourhood exposure, and recommend targeted actions.

---

# 1. Executive Summary

Indian-city air pollution is influenced by multiple simultaneous sources such as:

- Vehicular traffic
- Road dust
- Construction and demolition
- Industrial emissions
- Waste/biomass burning
- Regional pollution transported by wind
- Weather and atmospheric conditions

A conventional AQI dashboard tells users **how polluted** an area is, but not reliably **why it is polluted right now**.

The proposed system adds a source-attribution layer:

```text
Multiple Data Sources
        |
        v
Data Ingestion
        |
        v
Cleaning + Quality Control
        |
        v
Sensor Calibration + Spatial/Temporal Alignment
        |
        v
Pollution Event Detection
        |
        v
Candidate Source Generation
        |
        +------------------------------+
        |                              |
        v                              v
Physics / Wind Evidence          AI / ML Evidence
        |                              |
        +---------------+--------------+
                        |
                        v
                 Evidence Fusion
                        |
                        v
              Source Attribution
                        |
                        v
           Contribution + Confidence
                        |
              +---------+---------+
              |                   |
              v                   v
       Exposure Analysis     Forecasting
              |                   |
              +---------+---------+
                        |
                        v
              Decision / Action Engine
                        |
             +----------+----------+
             |                     |
             v                     v
       Government Dashboard   Citizen Alerts
```

The system should report results probabilistically. It should say **"construction is the most likely source with 64% attribution probability and 87% confidence"**, not claim absolute causality from sensor data alone.

---

# 2. Project Scope

## 2.1 Minimum viable system

The MVP should support:

1. Air-quality data ingestion
2. Weather/wind ingestion
3. Traffic indicators
4. Geographic road/source data
5. Pollution spike detection
6. Wind-based source candidate generation
7. Source classification
8. Source contribution estimation
9. Neighbourhood pollution map
10. Exposure warning
11. Targeted action recommendation
12. Web dashboard

## 2.2 Advanced features

Add these only after the MVP works:

- Sentinel-5P satellite NO2 analysis
- NASA FIRMS fire/hotspot detection
- Citizen image classification
- Construction activity detection from imagery
- Pollution forecasting
- Dispersion/plume simulation
- Counterfactual action simulation
- Automated enforcement prioritization
- Model explainability

---

# 3. Data Sources: Where to Fetch the Data

The most important rule is to distinguish **authoritative data**, **open supporting data**, and **synthetic/demo data**.

## 3.1 Air-quality observations

### Primary source: CPCB

Use the Central Pollution Control Board (CPCB) air-quality ecosystem for reference/official monitoring data.

Useful variables:

- PM2.5
- PM10
- NO2
- SO2
- CO
- O3
- NH3
- Station latitude/longitude
- Timestamp
- AQI where available
- Station metadata

CPCB documentation describes CAAQMS data being transmitted to CPCB servers and processed before dissemination. CPCB also maintains real-time air-quality and AQI resources.

Official sources:

- CPCB: https://cpcb.nic.in/
- CPCB air-quality publications/data: https://cpcb.nic.in/publications-3/
- CPCB AQI reporting: https://cpcb.nic.in/aqi_report.php

### Secondary source: OpenAQ

OpenAQ provides an API for air-quality measurements and station/sensor metadata.

Useful for:

- Historical data
- Cross-checking
- Additional stations
- Reproducible research
- Development when direct CPCB integration is inconvenient

API documentation:

https://api.openaq.org/docs

### Recommended implementation

Do not make the whole project dependent on one external API.

Build:

```text
CPCB Adapter
      |
OpenAQ Adapter
      |
Low-cost Sensor Adapter
      |
      v
Common AirQualityRecord
```

This allows the project to replace a source without changing the AI layer.

---

# 4. Low-Cost Sensor Data

For the actual research prototype, deploy a small network of low-cost sensors if possible.

Possible measurements:

- PM2.5
- PM10
- Temperature
- Relative humidity
- CO
- NO2, if the selected sensor supports it

Example record:

```json
{
  "sensor_id": "S001",
  "timestamp": "2026-08-29T10:30:00+05:30",
  "latitude": 28.6139,
  "longitude": 77.2090,
  "pm25_raw": 145.2,
  "pm10_raw": 210.4,
  "temperature": 31.4,
  "humidity": 48.2
}
```

The sensor pipeline should perform:

```text
Raw sensor reading
      |
      v
Range validation
      |
      v
Humidity/temperature correction
      |
      v
Reference-station calibration
      |
      v
Drift detection
      |
      v
Calibrated measurement
```

Do not present raw low-cost sensor readings as equivalent to regulatory reference instruments.

---

# 5. Weather and Wind Data

Wind direction is one of the most important inputs to source attribution.

Required variables:

- Wind speed
- Wind direction
- Temperature
- Relative humidity
- Pressure
- Precipitation
- Boundary-layer / atmospheric stability indicators where available

## Recommended source: Open-Meteo

Open-Meteo provides historical weather and forecast APIs, including wind speed and wind direction.

Official documentation:

https://open-meteo.com/en/docs/historical-weather-api

Historical weather can also be obtained from ERA5/ERA5-Land based datasets through Open-Meteo.

Recommended usage:

```text
Real-time / forecast:
Open-Meteo forecast API

Historical:
Open-Meteo Historical Weather API
or
ERA5 / ERA5-Land
```

For a research-grade implementation, retain the exact source, model, timestamp and retrieval time for every weather record.

---

# 6. Traffic Data

Traffic is one of the hardest data sources because high-quality live traffic APIs are often commercial or restricted.

## Recommended approach

Use three levels.

### Level 1 — OpenStreetMap

Use OpenStreetMap for:

- Roads
- Road classification
- Intersections
- Highways
- Major corridors
- Road geometry
- Nearby land-use/context

OpenStreetMap's Overpass API can query selected map features.

Official documentation:

https://wiki.openstreetmap.org/wiki/Overpass_API

Example:

```text
Overpass API
    |
    +-- primary roads
    +-- secondary roads
    +-- highways
    +-- intersections
    +-- traffic signals
    +-- construction-related map features
```

### Level 2 — Open / government traffic datasets

Search the selected city's/state's open-data portal and data.gov.in for:

- Traffic counts
- Road statistics
- Transport data
- Vehicle registrations
- Road network information

India's Open Government Data platform:

https://data.gov.in/

### Level 3 — Live traffic provider

If the project has access to a permitted traffic API, use it only according to that provider's terms.

The application should convert traffic information into a common feature:

```text
traffic_index = 0.0 ... 1.0
```

Example:

```text
0.0 = free-flow
0.5 = moderate
0.8 = heavy
1.0 = severe congestion
```

For the student MVP, a traffic index derived from available traffic observations is sufficient.

---

# 7. Satellite Data

Satellite data should be treated as **regional supporting evidence**, not as a replacement for ground sensors.

## 7.1 Sentinel-5P / TROPOMI

Useful for:

- NO2
- SO2
- CO
- Aerosol-related products depending on the selected product

Copernicus provides Sentinel-5P Level-2 data through the Copernicus Data Space Ecosystem.

Official sources:

https://sentinels.copernicus.eu/
https://documentation.dataspace.copernicus.eu/APIs/SentinelHub/Data/S5PL2.html

For NO2, the Level-2 product includes tropospheric column information and quality indicators.

Important limitation:

```text
Satellite observation
        !=
Ground-level concentration at one sensor
```

Satellite observations have different spatial/temporal characteristics and should therefore be fused as contextual evidence.

## 7.2 NASA FIRMS

Use NASA FIRMS for:

- Active fire hotspots
- Biomass/waste-burning evidence
- Thermal anomalies

Official API:

https://firms.modaps.eosdis.nasa.gov/api/

FIRMS provides MODIS and VIIRS active-fire data. Global near-real-time data are generally available within hours of observation.

Recommended features:

```text
fire_distance_km
fire_count_5km
fire_count_10km
nearest_fire_time
fire_confidence
fire_radiative_power
```

These can become evidence for a burning source.

---

# 8. Construction Data

Construction is highly city-specific.

Possible sources:

1. Municipal construction permits
2. City open-data portals
3. Building-permit databases
4. Government GIS portals
5. Construction-site geospatial datasets
6. Satellite imagery
7. Citizen reports
8. Manually curated project dataset for the prototype

Required fields:

```text
site_id
latitude
longitude
permit_id
permit_status
start_date
expected_end_date
construction_type
area
height
demolition_flag
active_flag
```

For a student prototype, create a verified construction-site table from public municipal information and manually validate a limited number of sites.

Do not assume that every mapped construction location is active.

---

# 9. Industrial Source Data

Required:

```text
industry_id
name
latitude
longitude
industry_type
emission_category
operating_status
stack_height_if_available
permit_information
```

Possible sources:

- CPCB/SPCB datasets
- State pollution control board portals
- Government environmental clearances
- Industry consent/permit information
- Public GIS/open-data portals

If exact emission rates are unavailable, use **source-category evidence** rather than inventing emission quantities.

---

# 10. Citizen Reports

Citizen reports can provide high-value local evidence, especially for:

- Smoke
- Waste burning
- Dust
- Construction activity
- Strong odours
- Visible pollution events

Example:

```json
{
  "report_id": "CR102",
  "timestamp": "2026-08-29T10:25:00+05:30",
  "latitude": 28.615,
  "longitude": 77.208,
  "category": "dust",
  "description": "Heavy dust from construction site",
  "image_url": "...",
  "credibility_score": 0.82
}
```

The system should not treat every citizen report as ground truth.

Use:

```text
Citizen report
      |
      v
Location/time validation
      |
      v
Duplicate detection
      |
      v
Optional image classification
      |
      v
Credibility score
      |
      v
Evidence fusion
```

---

# 11. Population and Vulnerability Data

Required for exposure warnings:

- Population density
- Schools
- Hospitals
- Elder-care facilities where available
- Residential areas
- Sensitive locations

Possible sources:

- Census/open government datasets
- Government GIS portals
- OpenStreetMap for POIs
- City administrative GIS
- Public demographic datasets

Exposure output:

```text
grid_id
population
schools
hospitals
estimated_exposed_population
exposure_severity
```

---

# 12. Data Storage Architecture

Recommended stack:

```text
                    DATA SOURCES
                         |
                         v
                Ingestion Workers
                         |
                         v
                    Message Queue
                         |
                         v
              Raw Data / Object Storage
                         |
                         v
                 Processing Pipeline
                         |
                         v
                 PostgreSQL + PostGIS
                         |
             +-----------+-----------+
             |                       |
             v                       v
        AI/ML Pipeline          REST API
                                     |
                                     v
                                 Dashboard
```

Recommended technologies:

```text
Python
FastAPI
PostgreSQL
PostGIS
Pandas
NumPy
GeoPandas
Scikit-learn
XGBoost
PyTorch (optional)
Docker
GitHub
```

For a student project, Kafka is optional. Start with scheduled Python workers or MQTT; introduce Kafka only if the data volume actually requires it.

---

# 13. Common Data Model

The three team members must agree on schemas before coding.

## AirQualityRecord

```json
{
  "timestamp": "ISO-8601",
  "source": "cpcb|openaq|sensor",
  "station_id": "S001",
  "latitude": 28.6139,
  "longitude": 77.2090,
  "pm25": 145.2,
  "pm10": 210.4,
  "no2": 72.5,
  "so2": 15.2,
  "co": 1.8,
  "o3": 44.2,
  "temperature": 31.4,
  "humidity": 48.2,
  "quality_flag": "valid"
}
```

## ContextRecord

```json
{
  "timestamp": "ISO-8601",
  "grid_id": "G42",
  "wind_speed": 3.2,
  "wind_direction": 245,
  "traffic_index": 0.82,
  "construction_activity": 1,
  "industrial_activity": 0,
  "fire_count_5km": 0
}
```

## AttributionResult

```json
{
  "event_id": "EVT1042",
  "grid_id": "G42",
  "timestamp": "ISO-8601",
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
  "confidence": 0.87,
  "evidence": [
    "upwind construction site",
    "PM10 spike",
    "dry conditions"
  ]
}
```

---

# 14. AI / Source Attribution Pipeline

This is the core research component.

## Step 1: Establish baseline

For every grid and pollutant:

```text
Historical observations
        |
        v
Hourly/day-of-week/seasonal baseline
        |
        v
Expected concentration
```

Example:

```text
Expected PM10 = 95 µg/m³
Observed PM10 = 185 µg/m³
Spike = +94.7%
```

## Step 2: Detect pollution events

Possible methods:

- Rolling z-score
- Isolation Forest
- Local Outlier Factor
- Change-point detection
- XGBoost classification
- LSTM/Temporal Transformer as an advanced option

Start with a transparent statistical baseline plus one ML model.

## Step 3: Generate candidate sources

For each event:

```text
Pollution hotspot
       |
       v
Use current wind direction
       |
       v
Trace upwind area
       |
       +-- roads
       +-- construction
       +-- industries
       +-- fire hotspots
       +-- other candidate sources
```

## Step 4: Calculate source evidence

### Traffic evidence

Features:

```text
traffic_index
road_distance
road_class
intersection_density
time_of_day
NO2 level
CO level
```

### Construction evidence

Features:

```text
construction_distance
upwind_score
active_permit
PM10 spike
dryness
citizen_dust_reports
```

### Industrial evidence

Features:

```text
industry_distance
upwind_score
industry_type
pollutant_signature
operating_status
```

### Burning evidence

Features:

```text
fire_distance
fire_count
fire_confidence
FRP
wind alignment
PM2.5 spike
CO spike
citizen_smoke_reports
```

## Step 5: Evidence fusion

A practical first model:

```text
Source Score =
    ML probability
  + wind alignment evidence
  + distance evidence
  + pollutant signature evidence
  + temporal evidence
  + satellite/fire evidence
  + citizen evidence
```

Normalize the resulting scores into probabilities.

A more formal version can use:

- Bayesian evidence fusion
- Logistic regression
- XGBoost
- Random Forest
- Neural network
- Graph neural network as an advanced research extension

## Step 6: Confidence

Confidence should depend on evidence quality.

Example:

```text
High confidence:
    multiple sensors agree
    strong wind alignment
    active source confirmed
    pollutant signature matches

Medium confidence:
    some evidence agrees
    limited sensors

Low confidence:
    weak source evidence
    missing weather/traffic data
    conflicting measurements
```

---

# 15. Source Attribution Logic

The system should distinguish **probability** from **contribution**.

Example:

```text
Source probability:
    Construction = 0.72
    Traffic      = 0.14
    Burning      = 0.08
    Industry     = 0.06

Estimated contribution:
    Construction = 52%
    Traffic      = 22%
    Burning      = 16%
    Industry     = 10%
```

These numbers are model outputs and should be presented with uncertainty.

Never claim that a source caused a pollution event with certainty unless there is independent validation.

---

# 16. Neighbourhood Exposure Engine

Divide the city into spatial cells.

Example:

```text
City
|
+-- G01
+-- G02
+-- G03
+-- ...
+-- G99
```

For each grid:

```text
pollution concentration
        +
population
        +
duration
        +
sensitive locations
        |
        v
exposure score
```

Example:

```text
Grid G42

PM2.5: 145
PM10: 210
Population: 12,400
Schools: 2
Hospitals: 1

Risk:
HIGH

Alert:
Avoid unnecessary outdoor activity.
Schools should reduce outdoor exposure.
```

The exact health messaging should be based on appropriate public-health guidance and not be presented as individualized medical advice.

---

# 17. Recommendation Engine

The recommendation engine converts source attribution into targeted operational actions.

## Traffic

If traffic is dominant:

```text
High congestion
      |
      +-- optimize signal timing
      +-- route/divert traffic
      +-- restrict selected heavy vehicles
      +-- inspect idling hotspots
```

## Construction

If construction/road dust dominates:

```text
High PM10
      |
      +-- inspect construction site
      +-- verify dust-control compliance
      +-- water/suppress dust
      +-- cover material
      +-- control truck movement
```

## Industrial

```text
Industrial attribution high
      |
      +-- prioritize inspection
      +-- verify operating permit
      +-- inspect emission-control equipment
      +-- check continuous monitoring data
```

## Burning

```text
Fire/burning evidence
      |
      +-- verify hotspot
      +-- dispatch local response
      +-- investigate waste burning
      +-- issue local alert
```

The system should recommend actions; authorized officials remain responsible for enforcement decisions.

---

# 18. Dashboard Requirements

## Main screen

```text
+-----------------------------------------------------------+
| AIR POLLUTION COMMAND CENTER                              |
+-----------------------------------------------------------+
| AQI | PM2.5 | PM10 | NO2 | Active Events                |
+-----------------------------------------------------------+
|                                                           |
|                     CITY MAP                              |
|                                                           |
|  Hotspots     Sources      Roads      Construction        |
|                                                           |
+----------------------------+------------------------------+
| ACTIVE EVENT               | SOURCE ATTRIBUTION           |
| Grid G42                   | Construction   62%          |
| PM10 210                   | Road Dust      21%          |
| Severity: High             | Traffic         9%          |
|                            | Industry        3%          |
+----------------------------+------------------------------+
| EXPOSURE                   | RECOMMENDED ACTION          |
| Population: 12,400        | Inspect construction       |
| Schools: 2                | Deploy dust-control team   |
| Hospitals: 1              | Issue local alert          |
+----------------------------+------------------------------+
```

---

# 19. Project Directory Structure

```text
air-pollution-source-attribution/
|
+-- README.md
+-- requirements.txt
+-- pyproject.toml
+-- docker-compose.yml
|
+-- configs/
|   +-- sensors.yaml
|   +-- pollutants.yaml
|   +-- model_config.yaml
|   +-- thresholds.yaml
|   +-- city_config.yaml
|
+-- data/
|   +-- raw/
|   |   +-- sensors/
|   |   +-- cpcb/
|   |   +-- weather/
|   |   +-- traffic/
|   |   +-- satellite/
|   |   +-- construction/
|   |   +-- industrial/
|   |   +-- citizen_reports/
|   |
|   +-- processed/
|   +-- features/
|   +-- models/
|
+-- src/
|   +-- ingestion/
|   +-- preprocessing/
|   +-- calibration/
|   +-- spatial/
|   +-- event_detection/
|   +-- source_attribution/
|   +-- forecasting/
|   +-- exposure/
|   +-- recommendations/
|   +-- citizen_ai/
|   +-- streaming/
|   +-- database/
|   +-- api/
|   +-- common/
|
+-- ml/
|   +-- training/
|   +-- evaluation/
|   +-- experiments/
|
+-- dashboard/
|   +-- frontend/
|   +-- admin/
|
+-- simulation/
|
+-- tests/
|   +-- unit/
|   +-- integration/
|   +-- fixtures/
|
+-- scripts/
|
+-- deployment/
|
+-- docs/
```

---

# 20. Three-Person Work Division

The three members can work in parallel.

## PERSON 1 — Data Engineering, Sensors and Geospatial Infrastructure

### Ownership

```text
PERSON 1
|
+-- Data ingestion
+-- CPCB/OpenAQ adapter
+-- Low-cost sensor ingestion
+-- Weather ingestion
+-- Traffic data ingestion
+-- Satellite data ingestion pipeline
+-- Data cleaning
+-- Sensor calibration
+-- Data quality checks
+-- PostgreSQL/PostGIS
+-- Spatial grid
+-- Data APIs
```

### Main files

```text
src/ingestion/
src/preprocessing/
src/calibration/
src/spatial/
src/database/
```

### Deliverables

1. Unified data schema
2. Data ingestion scripts
3. Cleaned datasets
4. Calibrated sensor data
5. Spatial grid
6. Database
7. Data-quality pipeline
8. Internal data API

---

## PERSON 2 — AI, Event Detection and Source Attribution

### Ownership

```text
PERSON 2
|
+-- Pollution baseline
+-- Anomaly detection
+-- Event detection
+-- Wind backtracking
+-- Candidate source generation
+-- Pollutant signatures
+-- Source classification
+-- Evidence fusion
+-- Contribution estimation
+-- Confidence score
+-- Forecasting
+-- Model evaluation
```

### Main files

```text
src/event_detection/
src/source_attribution/
src/forecasting/
ml/training/
ml/evaluation/
```

### Deliverables

1. Pollution event detector
2. Candidate source engine
3. Source-attribution model
4. Contribution estimator
5. Confidence estimator
6. Model evaluation report
7. Explainability/evidence output
8. Attribution API

---

## PERSON 3 — Dashboard, Exposure and Decision Support

### Ownership

```text
PERSON 3
|
+-- FastAPI integration
+-- Dashboard
+-- City map
+-- Pollution visualization
+-- Source visualization
+-- Exposure analysis
+-- Neighbourhood alerts
+-- Citizen reporting
+-- Recommendation engine
+-- Government action panel
+-- Frontend testing
```

### Main files

```text
src/api/
src/exposure/
src/recommendations/
dashboard/
```

### Deliverables

1. Government dashboard
2. Citizen-facing view
3. Pollution map
4. Source-attribution map
5. Exposure map
6. Alerts
7. Action recommendations
8. API integration
9. Demo workflow

---

# 21. Parallel Development Strategy

The members must NOT wait for one another.

Use mock data and fixed API contracts.

```text
                 COMMON SCHEMA
                      |
       +--------------+--------------+
       |              |              |
       v              v              v
   PERSON 1       PERSON 2       PERSON 3
   REAL DATA      MOCK DATA      MOCK DATA
       |              |              |
       v              v              v
   Data API       AI API        Dashboard
       |              |              |
       +--------------+--------------+
                      |
                      v
                 INTEGRATION
                      |
                      v
                FINAL SYSTEM
```

## Example

Person 2 does not need Person 1's final data.

Person 2 can train using:

```text
sample_pollution_events.csv
```

Person 3 does not need Person 2's final AI model.

Person 3 can build the dashboard using:

```text
sample_attribution.json
```

At integration time:

```text
sample data
    |
    v
replace with real data
```

---

# 22. Common API Contracts

## Pollution API

```text
GET /api/v1/pollution/current
GET /api/v1/pollution/history
GET /api/v1/pollution/grid/{grid_id}
```

## Event API

```text
GET /api/v1/events
GET /api/v1/events/{event_id}
```

## Attribution API

```text
GET /api/v1/attribution/{event_id}
```

## Exposure API

```text
GET /api/v1/exposure/{grid_id}
```

## Recommendation API

```text
GET /api/v1/recommendations/{event_id}
```

## Citizen report API

```text
POST /api/v1/reports
GET /api/v1/reports
```

---

# 23. Suggested 8-Week Schedule

## Week 1 — Planning and Interfaces

### Everyone

- Select one pilot city
- Define pollutants
- Define source categories
- Define grid size
- Finalize database schema
- Finalize API contracts
- Create GitHub repository

### Person 1

- Data-source research
- Ingestion schema
- Synthetic data generator

### Person 2

- Attribution methodology
- Source signatures
- Event-detection baseline

### Person 3

- Dashboard wireframe
- API requirements
- Map design

---

# Week 2 — Basic Pipeline

### Person 1

- Air-quality ingestion
- Weather ingestion
- Database

### Person 2

- Baseline calculation
- Pollution anomaly detection
- Synthetic events

### Person 3

- Dashboard skeleton
- Map
- AQI/pollution charts

---

# Week 3 — Spatial and AI Layer

### Person 1

- PostGIS
- Grid generation
- Road/source spatial features
- Sensor-to-grid mapping

### Person 2

- Wind backtracking
- Candidate sources
- First attribution model

### Person 3

- Source layer on map
- Event panel
- Historical charts

---

# Week 4 — Multimodal Attribution

### Person 1

- Traffic integration
- Construction dataset
- Fire/satellite ingestion

### Person 2

- Evidence fusion
- Source probabilities
- Confidence score

### Person 3

- Attribution visualization
- Exposure map
- Alert interface

---

# Week 5 — Exposure and Recommendations

### Person 1

- Population/POI datasets
- Data quality improvements

### Person 2

- Model evaluation
- Feature importance
- Attribution error analysis

### Person 3

- Exposure engine
- Recommendation engine
- Government action panel

---

# Week 6 — Advanced Features

### Person 1

- Pipeline automation
- Data refresh jobs
- Monitoring

### Person 2

- Forecasting
- Optional dispersion simulation
- Uncertainty estimation

### Person 3

- Citizen reports
- Optional image classification
- Notification system

---

# Week 7 — Integration

All members:

```text
Real Data
   |
   v
Real AI
   |
   v
Real Dashboard
```

Tasks:

- End-to-end testing
- API integration
- Performance testing
- Data validation
- Fix bugs
- Improve UI
- Verify model outputs

---

# Week 8 — Evaluation and Presentation

### Research

- Accuracy
- Precision
- Recall
- F1
- Attribution accuracy
- Calibration error
- False attribution rate
- Alert precision
- API latency

### Documentation

- Architecture
- Methodology
- Dataset documentation
- Model card
- Limitations
- Results
- Future work

### Demo

Prepare a scenario:

```text
10:00
Normal pollution

       ↓

10:15
PM10 suddenly rises

       ↓

10:16
System detects event

       ↓

10:17
Wind analysis identifies upwind area

       ↓

10:18
Construction site found in candidate area

       ↓

10:19
Traffic + satellite + citizen evidence added

       ↓

10:20
Attribution:

Construction 64%
Road dust    21%
Traffic       9%
Other         6%

       ↓

10:21
Exposure estimated

       ↓

10:22
Recommended action:

Inspect construction site
+ dust-control enforcement
+ neighbourhood alert
```

---

# 24. Testing Strategy

## Unit testing

Test:

- Sensor validation
- Calibration
- Wind calculations
- Distance calculations
- Source scoring
- Exposure calculation
- Recommendation rules

## Integration testing

Test:

```text
Data source
    ↓
Database
    ↓
AI
    ↓
API
    ↓
Dashboard
```

## Model testing

Use historical or simulated events with known source labels.

Metrics:

```text
Classification:
Precision
Recall
F1

Attribution:
Top-1 source accuracy
Top-2 source accuracy
Contribution MAE

Event detection:
Precision
Recall
False alarm rate

Forecasting:
MAE
RMSE
MAPE where appropriate
```

---

# 25. Synthetic Data and Simulation

Because real source labels are difficult to obtain, simulation is essential.

Create synthetic scenarios:

## Scenario A — Traffic

```text
High traffic
+
high NO2
+
high CO
+
road proximity
+
wind alignment
```

Expected:

```text
Traffic attribution high
```

## Scenario B — Construction

```text
Active construction
+
high PM10
+
dry conditions
+
upwind construction site
```

Expected:

```text
Construction attribution high
```

## Scenario C — Burning

```text
Fire hotspot
+
PM2.5 spike
+
CO increase
+
wind from fire toward sensor
```

Expected:

```text
Burning attribution high
```

## Scenario D — Industrial

```text
Industrial facility
+
appropriate pollutant signature
+
wind alignment
+
elevated concentration
```

Expected:

```text
Industrial attribution high
```

## Scenario E — Regional pollution

```text
No nearby strong source
+
multiple sensors elevated
+
regional wind pattern
+
satellite evidence
```

Expected:

```text
Regional/background attribution high
```

---

# 26. Important Research Challenges

## Challenge 1 — Correlation is not causation

A nearby road does not automatically mean traffic caused the pollution.

Solution:

```text
distance
+
wind
+
time
+
pollutant signature
+
traffic intensity
+
multiple sensors
```

## Challenge 2 — Low-cost sensors are noisy

Solution:

- Calibration
- Reference-station comparison
- Drift monitoring
- Quality flags
- Sensor redundancy

## Challenge 3 — Satellite data is not ground truth

Solution:

Use it as regional evidence rather than direct substitution for ground measurements.

## Challenge 4 — Missing data

Solution:

```text
Missing data
    |
    +-- short gap -> interpolation where scientifically appropriate
    +-- long gap  -> model-based imputation with flag
    +-- critical variable missing -> lower confidence
```

## Challenge 5 — Source overlap

Traffic and road dust can happen simultaneously.

Therefore the model should allow:

```text
Traffic       35%
Road dust     30%
Construction  20%
Other         15%
```

rather than forcing exactly one source.

---

# 27. Recommended MVP Technology Stack

```text
Frontend
    React
    Leaflet / MapLibre

Backend
    FastAPI

Data
    Python
    Pandas
    NumPy
    GeoPandas

Database
    PostgreSQL
    PostGIS

ML
    Scikit-learn
    XGBoost

Optional deep learning
    PyTorch

Weather
    Open-Meteo

Air quality
    CPCB
    OpenAQ

Satellite
    Copernicus Sentinel-5P
    NASA FIRMS

Road/GIS
    OpenStreetMap
    Overpass API

Deployment
    Docker
    GitHub

Testing
    Pytest
```

---

# 28. What NOT to Build Initially

To keep the project achievable, do not start with:

- A huge deep-learning model
- Full CFD atmospheric simulation
- City-wide IoT deployment
- A custom satellite-processing infrastructure
- A complicated Kafka cluster
- Mobile apps for both Android and iOS
- Automated legal enforcement
- Fully autonomous government decisions

Start with:

```text
Data
  ↓
Detection
  ↓
Wind + source candidates
  ↓
ML attribution
  ↓
Exposure
  ↓
Dashboard
```

Then add advanced features.

---

# 29. Final System Tree

```text
AI AIR POLLUTION SOURCE ATTRIBUTION PLATFORM
|
+-- DATA SOURCES
|   |
|   +-- CPCB / OpenAQ
|   +-- Low-cost sensors
|   +-- Open-Meteo / ERA5
|   +-- Traffic
|   +-- OpenStreetMap
|   +-- Construction
|   +-- Industrial
|   +-- Sentinel-5P
|   +-- NASA FIRMS
|   +-- Citizen reports
|   +-- Population / GIS
|
+-- PERSON 1
|   |
|   +-- Ingestion
|   +-- Cleaning
|   +-- Calibration
|   +-- Spatial processing
|   +-- Database
|   +-- Data API
|
+-- PERSON 2
|   |
|   +-- Event detection
|   +-- Wind backtracking
|   +-- Candidate sources
|   +-- Source signatures
|   +-- AI attribution
|   +-- Evidence fusion
|   +-- Contribution
|   +-- Confidence
|   +-- Forecasting
|
+-- PERSON 3
|   |
|   +-- Backend integration
|   +-- Dashboard
|   +-- Pollution map
|   +-- Attribution map
|   +-- Exposure
|   +-- Alerts
|   +-- Recommendations
|   +-- Citizen reports
|
+-- OUTPUT
    |
    +-- Real-time pollution map
    +-- Pollution event detection
    +-- Probable source
    +-- Source contribution
    +-- Confidence
    +-- Neighbourhood exposure
    +-- Alerts
    +-- Targeted recommendations
```

---

# 30. Final Deliverables

By project completion, the team should have:

### Software

- Working data-ingestion pipeline
- Database
- Pollution-event detector
- Source-attribution model
- Exposure engine
- Recommendation engine
- REST API
- Web dashboard

### Data

- Cleaned air-quality dataset
- Weather dataset
- Traffic/context dataset
- GIS source dataset
- Satellite/fire dataset
- Synthetic validation dataset

### AI

- Baseline model
- Final attribution model
- Model evaluation
- Explainability/evidence output
- Confidence estimation

### Documentation

- Architecture document
- Dataset documentation
- API documentation
- Model methodology
- Model evaluation
- Limitations
- Reproducibility instructions

### Demonstration

A complete end-to-end event:

```text
Pollution spike
      ↓
Detection
      ↓
Location
      ↓
Wind direction
      ↓
Candidate sources
      ↓
AI evidence fusion
      ↓
Source probability
      ↓
Contribution
      ↓
Confidence
      ↓
Population exposure
      ↓
Neighbourhood warning
      ↓
Targeted action recommendation
```

---

# 31. Most Important Team Rule

The three members should own different modules but share one contract:

```text
PERSON 1
"Here is clean, spatially aligned data."
          |
          v
PERSON 2
"Here is the probable source and confidence."
          |
          v
PERSON 3
"Here is who is exposed and what action is recommended."
```

All three modules should be independently testable and connected through documented APIs.

This makes parallel development possible and prevents the project from becoming dependent on one team member finishing before the others can start.

---

# 32. Recommended First-Day Checklist

Before writing major code, complete these items together:

- [ ] Choose one pilot city
- [ ] Choose 4–6 pollutant/source categories
- [ ] Choose spatial grid resolution
- [ ] Decide time resolution
- [ ] Create common database schema
- [ ] Create sample JSON records
- [ ] Create GitHub repository
- [ ] Create three feature branches
- [ ] Assign module ownership
- [ ] Create API contracts
- [ ] Download a small historical dataset
- [ ] Generate synthetic events
- [ ] Agree on evaluation metrics
- [ ] Agree on the Week-4 MVP

Once these are completed, all three members can work independently and integrate progressively.
