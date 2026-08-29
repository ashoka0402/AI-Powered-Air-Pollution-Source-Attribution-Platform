# AI-Powered Air Pollution Source-Attribution Platform
## Complete Technology and Domain Concepts Handbook
### What each topic is, why it is used, how it is used, and how it fits into the project

---

# 1. Purpose of this document

This document is a **conceptual and technical handbook** for the complete air-pollution source-attribution project.

It explains:

- What each technology/concept is
- Why the project needs it
- How it is used
- What data goes into it
- What comes out of it
- Which team member owns it
- How it connects to the rest of the system
- What should be built first
- What is optional or advanced

The three team members should use this document alongside the **3-Person Master Context + Code Generation Contract**.

---

# 2. Project in one sentence

The project is a system that combines air-quality measurements, weather, wind, traffic, GIS, satellite observations, fires, construction, industrial information and citizen reports to estimate:

> **where pollution is increasing, which sources are probably responsible, who is exposed, and what targeted action should be taken.**

---

# 3. Core system idea

A normal air-quality application does this:

```text
Sensor
   |
   v
PM2.5 = 140
   |
   v
AQI = High
   |
   v
Show on dashboard
```

Our system does this:

```text
Sensor + Weather + Wind + Traffic + GIS + Satellite
+ Construction + Industry + Fires + Citizen Reports
                         |
                         v
                 Detect pollution event
                         |
                         v
              Find candidate sources
                         |
                         v
            Compare physical direction
                         +
              pollutant signatures
                         +
              source activity
                         +
              satellite evidence
                         +
              traffic evidence
                         |
                         v
                Evidence fusion
                         |
                         v
              Source probabilities
                         |
                         v
          Contribution + confidence
                         |
                         v
            Exposure estimation
                         |
                         v
             Targeted recommendation
```

---

# 4. Domain Concepts

## 4.1 Air pollution

Air pollution is the presence of harmful substances in air at concentrations that can adversely affect people, ecosystems, or infrastructure.

For this project, the most relevant pollutants are:

```text
PM2.5
PM10
NO2
SO2
CO
O3
```

### Why these pollutants?

They provide different kinds of evidence.

```text
PM2.5
    -> fine particles
    -> combustion and secondary aerosol evidence

PM10
    -> coarse particles
    -> construction / road dust evidence

NO2
    -> combustion
    -> strong traffic-related evidence

SO2
    -> fuel/industrial combustion
    -> useful industrial evidence

CO
    -> incomplete combustion
    -> useful for traffic and burning

O3
    -> atmospheric chemistry
    -> useful mainly for secondary pollution
```

A source should never be identified using a single pollutant alone.

---

# 5. PM2.5

## What it is

PM2.5 means particulate matter with aerodynamic diameter of approximately 2.5 micrometres or smaller.

## Why it matters

It can penetrate deeply into the respiratory system and is an important exposure indicator.

## How the project uses it

```text
PM2.5 readings
   |
   +-- baseline comparison
   +-- pollution-event detection
   +-- source signature
   +-- exposure estimation
   +-- forecast
```

## Important source clues

PM2.5 can be associated with:

- combustion
- traffic
- waste burning
- biomass burning
- industrial activity
- regional transport
- secondary atmospheric formation

It is therefore powerful but not source-specific by itself.

---

# 6. PM10

## What it is

PM10 means particulate matter with aerodynamic diameter of approximately 10 micrometres or smaller.

## Why it matters

PM10 responds strongly to coarse dust sources.

## How it is used

```text
High PM10
+
relatively weaker combustion-gas increase
+
dry conditions
+
construction/road activity
=
strong dust evidence
```

Likely sources include:

- construction
- demolition
- road dust
- soil
- uncovered material
- dusty trucks

---

# 7. NO2

## What it is

Nitrogen dioxide is an atmospheric pollutant associated strongly with combustion.

## Why it is useful

It can provide stronger evidence for traffic and combustion than PM alone.

Example:

```text
Traffic index ↑
NO2 ↑
CO ↑
PM2.5 ↑
Sensor close to road
Wind from road toward sensor
```

Together these form stronger traffic evidence.

---

# 8. SO2

## What it is

Sulphur dioxide is produced mainly by combustion of sulphur-containing fuels and certain industrial processes.

## Why it is useful

An SO2 increase combined with:

- an upwind industrial facility
- matching operating time
- compatible industrial category

can provide useful industrial-source evidence.

---

# 9. CO

## What it is

Carbon monoxide is a combustion product.

## Why it is useful

CO can support evidence for:

- traffic
- waste burning
- biomass burning
- generators
- incomplete combustion

Again, it should be combined with other evidence.

---

# 10. O3

## What it is

Ground-level ozone is a secondary pollutant formed through atmospheric chemical reactions involving precursor pollutants and sunlight.

## Why it is different

Unlike a direct stack or road source, ozone may be formed away from the original precursor emissions.

Therefore:

```text
O3 high
```

does not necessarily mean:

```text
O3 source nearby
```

This makes O3 particularly important when the system is trying to distinguish local primary emissions from secondary/regional pollution.

---

# 11. AQI

## What it is

The Air Quality Index converts pollutant measurements into an interpretable air-quality category.

India's official AQI framework is associated with CPCB.

## Why the project uses it

AQI is useful for:

- public communication
- dashboard display
- health-oriented warning categories
- comparing neighbourhood conditions

## What AQI does NOT do

AQI does not tell us:

```text
why pollution is high
```

That is the purpose of the source-attribution layer.

The project therefore has:

```text
AQI
+
Source Attribution
+
Exposure
+
Action Recommendation
```

---

# 12. CPCB air-quality data

## What it is

CPCB operates India's central environmental monitoring and air-quality reporting infrastructure.

## Why it is used

CPCB observations provide an important reference source for:

- official measurements
- model validation
- sensor calibration
- historical analysis
- city-level context

## How to use it

Person 1 should create:

```text
src/ingestion/cpcb_client.py
```

with:

```python
fetch_cpcb_air_quality()
normalize_air_quality_record()
```

## Important rule

Never assume that every CPCB station reports every pollutant continuously.

The system must handle:

```text
missing values
different station coverage
different sampling intervals
station downtime
```

---

# 13. OpenAQ

## What it is

OpenAQ is an open air-quality data platform and API.

## Why it is useful

It can provide:

- historical observations
- station information
- additional data coverage
- a reproducible API for research/development

## How it is used

```text
OpenAQ
   |
   v
Python API client
   |
   v
normalize_air_quality_record()
   |
   v
common schema
```

Official documentation:
https://docs.openaq.org/

---

# 14. Low-cost air-quality sensors

## What they are

Low-cost sensor nodes are inexpensive devices for measuring pollutants and environmental conditions.

Typical measurements:

```text
PM2.5
PM10
temperature
humidity
NO2/CO/SO2 depending on hardware
```

## Why the project uses them

Reference stations are sparse.

Low-cost sensors can create a much denser network:

```text
Reference station       ●
Low-cost sensor         •
Low-cost sensor         •
Low-cost sensor         •
Low-cost sensor         •
```

This helps estimate neighbourhood-level variation.

## Problem

Low-cost sensors may be affected by:

- humidity
- temperature
- sensor ageing
- cross-sensitivity
- drift
- contamination
- electronics noise

Therefore raw values should not automatically be treated as reference-grade data.

---

# 15. Sensor calibration

## What it is

Calibration is the process of relating a low-cost sensor's raw output to a more trusted reference measurement.

## Why it is required

Example:

```text
Reference PM2.5 = 100
Sensor raw       = 127
```

The sensor has systematic error.

## Basic model

```text
corrected_pm25 =
    f(raw_pm25, humidity, temperature, sensor_id, season)
```

Possible models:

- Linear regression
- Polynomial regression
- Random Forest
- XGBoost
- Neural network

For a student project, start with:

```text
Linear / polynomial model
```

and compare it with:

```text
Random Forest / XGBoost
```

## Required output

```text
corrected_value
quality_flag
calibration_model_version
uncertainty
```

---

# 16. Sensor drift

## What it is

Sensor behaviour can change over time.

Example:

```text
Month 1:
Sensor error = +3

Month 6:
Sensor error = +19
```

## Why it matters

Without drift monitoring, the AI could mistake sensor degradation for a pollution event.

## How to detect it

Compare:

```text
sensor
vs
reference station
vs
nearby sensors
vs
historical sensor behaviour
```

## Sensor state

```text
healthy
suspected_drift
calibration_required
temporarily_unreliable
disabled
```

---

# 17. IoT

## What it is

IoT means connected physical devices that measure or interact with the environment.

In this project:

```text
Air sensor
    |
    v
Network
    |
    v
Backend
```

## Why it is used

It allows continuous data collection rather than manual uploads.

---

# 18. MQTT

## What it is

MQTT is a lightweight publish/subscribe messaging protocol commonly used for IoT.

## Why use it

Sensors may have:

- limited bandwidth
- limited computing resources
- intermittent connectivity

MQTT is designed for that type of environment.

## Example

Sensor publishes:

```text
topic:
air/sensors/S001
```

Payload:

```json
{
  "sensor_id": "S001",
  "pm25": 145.2,
  "pm10": 210.4
}
```

The backend subscribes to:

```text
air/sensors/#
```

## Architecture

```text
Sensor
   |
 MQTT
   |
   v
MQTT Broker
   |
   v
Python Consumer
   |
   v
Database
```

---

# 19. Weather data

## Why weather is critical

Air pollution is not determined only by emissions.

Weather controls:

- transport
- dilution
- accumulation
- plume direction
- rainfall removal
- atmospheric mixing

The most important variables are:

```text
wind_speed
wind_direction
temperature
humidity
pressure
precipitation
atmospheric stability
mixing height
```

---

# 20. Wind direction

## What it means

Wind direction tells us where the air is coming from or, depending on convention, where it is going.

Meteorological wind direction is normally expressed as the direction **from which** wind originates.

Example:

```text
Wind direction = 270°
```

means wind is coming from the west and moving approximately eastward.

## Why it matters

Suppose:

```text
Factory
   |
   |  wind
   v
Sensor
```

If the wind direction is consistent with the factory-to-sensor path, the factory becomes a stronger candidate.

---

# 21. Wind backtracking

## What it is

Wind backtracking estimates where the air reaching a polluted sensor likely came from.

## Basic concept

```text
Sensor
  ●
  |
  | reverse wind direction
  |
  v
possible source area
```

## Why it is used

A source located downwind is less plausible as the cause of the current measurement.

A source located upwind is more plausible.

## Important limitation

Wind alone does not prove source causation.

It is only one evidence component.

---

# 22. Wind geometry

## What it does

The system should calculate whether a candidate source lies within an upwind angular sector.

Example:

```text
                 Sensor
                   ●
                  / \
                 /   \
                /     \
        upwind search area
              /         \
             /           \
        Source A       Source B
```

Useful function:

```python
calculate_upwind_score()
```

Typical inputs:

```text
sensor_latitude
sensor_longitude
source_latitude
source_longitude
wind_direction
```

Possible output:

```text
0.0 = poor alignment
1.0 = strong alignment
```

---

# 23. Open-Meteo

## What it is

Open-Meteo provides weather forecast and historical weather APIs.

## Why use it

It is convenient for:

- development
- historical analysis
- weather forecasts
- wind data

Documentation:
https://open-meteo.com/en/docs

## How Person 1 uses it

```text
fetch_weather_data()
      |
      v
normalize_weather_record()
      |
      v
weather_observations
```

---

# 24. ERA5

## What it is

ERA5 is a global atmospheric reanalysis dataset.

## Why it matters

It provides a consistent historical atmospheric dataset useful for:

- research
- model training
- historical weather reconstruction
- long-term studies

## Why not use it for everything?

ERA5 is often more appropriate for historical/research analysis than low-latency street-level nowcasting.

---

# 25. GIS

## What GIS means

GIS = Geographic Information System.

It is the system used to represent:

```text
where things are
```

and analyze spatial relationships.

## Why this project needs GIS

Almost every important question is spatial:

```text
Which source is near the sensor?
Which source is upwind?
Which roads are near the hotspot?
Which schools are inside the affected area?
Which neighbourhood is downwind?
```

---

# 26. Latitude and longitude

Every important object should have a geographic location.

Examples:

```text
sensor
road
construction site
factory
fire
school
hospital
neighbourhood
```

Example:

```text
latitude  = 28.6139
longitude = 77.2090
```

---

# 27. Spatial grid

## What it is

The city is divided into small geographic cells.

Example:

```text
+----+----+----+
| G1 | G2 | G3 |
+----+----+----+
| G4 | G5 | G6 |
+----+----+----+
| G7 | G8 | G9 |
+----+----+----+
```

## Why use a grid?

The system can maintain one standardized state per neighbourhood unit:

```text
G5
PM2.5 = 140
PM10  = 210
Traffic = 0.83
Exposure = High
```

## Recommended approach

Use a consistent grid system such as H3 or another geospatial indexing approach.

---

# 28. PostGIS

## What it is

PostGIS is the spatial extension for PostgreSQL.

It allows database operations on geographic objects.

## Why it is important

You can query things like:

```text
Find all construction sites within 2 km of sensor S10.
```

or:

```text
Find industrial facilities inside the upwind area.
```

or:

```text
Find schools inside the predicted plume.
```

## Example architecture

```text
PostgreSQL
    |
    +-- normal database features
    |
    +-- PostGIS
            |
            +-- POINT
            +-- LINESTRING
            +-- POLYGON
            +-- distance
            +-- intersection
            +-- containment
```

Documentation:
https://postgis.net/documentation/

---

# 29. GeoPandas

## What it is

GeoPandas extends pandas with geographic objects.

## Why use it

Person 1 and Person 2 can use GeoPandas for:

- source mapping
- spatial joins
- geospatial preprocessing
- shape files
- GeoJSON
- distance calculations
- data preparation

Example:

```text
construction.csv
       +
city_grid.geojson
       |
       v
GeoPandas spatial join
       |
       v
construction_to_grid.csv
```

---

# 30. OpenStreetMap

## What it is

OpenStreetMap is an open geographic database.

## Why use it

It can provide:

- roads
- intersections
- highways
- buildings
- land-use features
- traffic signals
- points of interest

## How it helps

Traffic attribution needs road geography:

```text
Sensor
  |
  +-- nearest road
  |
  +-- road distance
  |
  +-- intersection density
  |
  +-- road type
```

---

# 31. Overpass API

## What it is

Overpass API is a query interface for extracting selected OpenStreetMap elements.

## Why use it

Instead of downloading the entire world map, you can ask for specific objects.

Example conceptual query:

```text
Give me all major roads
inside this city boundary.
```

Documentation:
https://wiki.openstreetmap.org/wiki/Overpass_API

---

# 32. Traffic data

## Why traffic is important

Traffic is both:

```text
an emission source
```

and:

```text
a time-varying activity signal
```

Useful features:

```text
traffic_index
vehicle_count
average_speed
queue_length
heavy_vehicle_percentage
road_type
```

## Example

```text
09:00
speed = 35 km/h
traffic = 0.35

09:30
speed = 8 km/h
traffic = 0.91
```

If NO2 simultaneously rises, traffic becomes stronger source evidence.

---

# 33. Traffic index

A simple normalized index:

```text
0.0 → free flowing
0.5 → moderate congestion
0.8 → heavy
1.0 → severe
```

The exact formula depends on available data.

Example:

```text
traffic_index =
1 - current_speed / free_flow_speed
```

This is only a possible proxy, not a universal definition.

---

# 34. Satellite data

## Why satellites are used

Ground sensors provide local measurements.

Satellites provide broader spatial context.

```text
Ground sensors:
high local detail

Satellite:
broader regional coverage
```

Together:

```text
ground truth/context
        +
regional observation
```

improves interpretation.

---

# 35. Sentinel-5P / TROPOMI

## What it is

Sentinel-5P carries the TROPOMI instrument for atmospheric composition observations.

## Useful products

Depending on the selected product:

- NO2
- SO2
- CO
- aerosol-related atmospheric information

## Why use it

Suppose a city has a local NO2 spike.

Satellite observations can help determine whether:

```text
the city is experiencing a broader regional pollution event
```

rather than only:

```text
one local road is responsible
```

## Important limitation

Satellite values are not equivalent to one ground-level sensor measurement.

Therefore:

```text
Satellite
=
context/evidence

Ground sensor
=
near-surface local observation
```

Copernicus Data Space documentation:
https://documentation.dataspace.copernicus.eu/

---

# 36. NASA FIRMS

## What it is

FIRMS = Fire Information for Resource Management System.

It uses satellite observations from systems such as MODIS and VIIRS to detect active fires and thermal anomalies.

## Why it is used

It can provide evidence for:

- open burning
- agricultural burning
- landfill fires
- biomass burning
- regional smoke events

## Example

```text
Fire hotspot
      |
      v
Distance to pollution event
      +
wind alignment
      +
PM2.5/CO increase
      |
      v
Burning evidence
```

FIRMS provides APIs, maps and downloadable geospatial fire products.

Official sources:
https://firms.modaps.eosdis.nasa.gov/
https://firms.modaps.eosdis.nasa.gov/api/

---

# 37. Satellite temporal mismatch

A satellite may observe an area only at certain times.

Therefore:

```text
ground sensor:
continuous

satellite:
periodic observation
```

The system must handle missing satellite observations without declaring the entire analysis invalid.

---

# 38. Construction data

## What it is

Information about active construction/demolition projects.

## Why it is important

Construction is often a local and intermittent source of PM10/dust.

Required fields:

```text
site_id
permit_id
location
status
construction_type
start_date
end_date
active_flag
```

## How it is used

```text
Pollution event
      |
      v
upwind area
      |
      v
construction sites
      |
      v
active at event time?
      |
      v
yes
      |
      v
candidate source
```

---

# 39. Industrial source inventory

## What it is

A list of industrial facilities and their relevant attributes.

Example:

```text
source_id
location
industry_type
operating_status
permit_status
stack_height
expected_pollutants
```

## Why it is used

The attribution model needs to know:

```text
what sources exist
```

before it can determine:

```text
which source could explain the event
```

---

# 40. Citizen reports

## What they are

People can report:

- smoke
- dust
- waste burning
- industrial odour
- uncovered trucks
- visible construction dust

## Why they are valuable

Sensors may miss a very small local event.

A citizen report can provide:

```text
human observation
+
location
+
time
+
photograph/video
```

## Important limitation

Citizen reports can be:

- inaccurate
- duplicated
- delayed
- biased
- malicious

Therefore they should be an **evidence input**, not automatic truth.

---

# 41. Citizen report credibility

A credibility score can use:

```text
GPS validity
+
timestamp validity
+
duplicate detection
+
image evidence
+
nearby sensor agreement
+
other citizen reports
```

Example:

```text
credibility_score = 0.86
```

This score becomes an evidence feature.

---

# 42. Computer vision for citizen images

## What it is

Using an ML model to interpret uploaded images.

## Possible tasks

```text
smoke / no smoke
fire / no fire
dust cloud / no dust cloud
construction / non-construction
uncovered truck / normal truck
```

## Why optional?

It adds complexity.

For the first version:

```text
manual category
+
sensor agreement
```

may be enough.

Add computer vision after the core attribution pipeline works.

---

# 43. Data ingestion

## What it is

Data ingestion means bringing external observations into your system.

Example:

```text
CPCB API
     |
Weather API
     |
FIRMS API
     |
Traffic API
     |
Sensor MQTT
     |
     v
INGESTION LAYER
```

## Why it is separate

The rest of the project should not care how a source delivers data.

For example:

```text
AI model
```

should only receive:

```text
PollutionRecord
ContextRecord
```

and not care whether the data came from CPCB, OpenAQ, MQTT, or a CSV file.

---

# 44. Data normalization

## What it is

Different sources use different:

- field names
- units
- timestamp formats
- coordinate systems
- update intervals

Normalization creates one common format.

Example:

```text
Provider A:
PM2_5

Provider B:
pm25

Provider C:
PM25

Internal:
pm25
```

---

# 45. Timestamp alignment

## Why it is necessary

Suppose:

```text
Sensor:
10:05

Traffic:
10:04

Weather:
10:00

Satellite:
09:58
```

The system needs a consistent event window.

A common approach:

```text
1-minute or 5-minute time windows
```

All observations are aligned to the appropriate interval.

---

# 46. Data quality

Every measurement should have a quality state.

Example:

```text
valid
suspect
missing
calibration_required
stale
```

This is critical to model confidence.

---

# 47. Time-series database

## What it is

A time-series database is optimized for timestamped measurements.

Examples:

- TimescaleDB
- InfluxDB

## Should you use one?

For a 3-person project, PostgreSQL + TimescaleDB or PostgreSQL alone can be sufficient.

The important point is that the schema should handle large timestamped sensor records efficiently.

---

# 48. PostgreSQL

## What it is

A relational database management system.

## Why use it

It can manage:

- structured records
- relationships
- constraints
- transactions
- indexes
- application data

It becomes especially powerful when combined with PostGIS.

---

# 49. Redis

## What it is

An in-memory key-value store.

## Why optional

It can be used for:

- caching
- short-lived dashboard values
- rate limiting
- session data
- temporary computation results

You do not need Redis for the first MVP.

---

# 50. Data lake / object storage

## What it is

Storage for large raw files.

Examples:

```text
satellite files
images
videos
historical CSV files
model artifacts
```

Possible technologies:

- S3
- MinIO
- cloud blob storage

For a student deployment, local object storage or MinIO can be enough.

---

# 51. Feature engineering

## What it is

Turning raw measurements into features useful for ML.

Raw:

```text
PM10 = 210
wind_dir = 245
traffic = 0.82
```

Features:

```text
PM10_spike_ratio = 2.1
wind_alignment = 0.91
distance_to_road = 0.3 km
construction_active = 1
traffic_index = 0.82
```

ML models usually benefit from these derived variables.

---

# 52. Baseline

## What it is

The normal expected pollution value under similar conditions.

Example:

```text
Expected PM10 at 10 AM on weekday:
95

Observed:
180
```

Excess:

```text
85
```

## Why it matters

A raw value is not enough.

```text
PM10 = 180
```

may be normal during a severe city-wide episode.

The system therefore compares:

```text
observed
vs
expected
```

---

# 53. Pollution anomaly detection

## What it is

Finding pollution values that are unusually different from the expected baseline.

## Why it is used

It identifies events worthy of investigation.

Possible techniques:

- z-score
- rolling residual
- Isolation Forest
- change-point detection
- autoencoder
- temporal ML

## Recommended first implementation

```text
historical baseline
+
robust threshold
+
Isolation Forest
```

This gives you both interpretability and an ML component.

---

# 54. Pollution event

## What it is

A temporally and spatially defined pollution anomaly.

Example:

```text
Event ID: EVT1042

Start: 10:10
End: 10:55
Grid: G042
Pollutant: PM10
Peak: 215
Baseline: 98
Severity: High
```

This event then becomes the input to source attribution.

---

# 55. Candidate source generation

## What it is

Instead of asking the ML model to consider thousands of sources, first create a shortlist.

Example:

```text
Pollution event
      |
      v
Affected grid
      |
      v
Upwind search area
      |
      +-- roads
      +-- construction
      +-- industry
      +-- fires
      +-- waste sites
```

This reduces computation and makes reasoning more transparent.

---

# 56. Source signatures

## What they are

A source signature is a pattern of pollutant/environmental evidence associated with a source class.

Example:

```text
Traffic:
NO2 + CO + PM2.5 + congestion

Construction:
PM10 + dry conditions + active site

Burning:
PM2.5 + CO + fire evidence

Industrial:
SO2/NO2 + facility + operating time
```

## Important

A signature is not a deterministic rule.

It is evidence.

---

# 57. Source attribution

## What it means

Source attribution estimates which source or source category most likely contributed to the observed pollution event.

Example:

```text
Traffic         0.12
Construction    0.64
Road dust       0.21
Industrial      0.03
```

These are probabilities, not legal proof.

---

# 58. Source category vs exact source

This distinction is important.

## Category

```text
construction
```

means:

> the event likely belongs to the construction source class.

## Exact source

```text
construction site CONST-7841
```

means:

> among known construction sites, this particular site is the strongest candidate.

The exact-source confidence should often be lower than the source-category confidence.

Example:

```text
Construction category: 82%
Exact site CONST-7841: 61%
```

---

# 59. Wind evidence

A candidate source should get higher score when:

- it is upwind
- its direction aligns with the sensor
- wind speed is sufficient to move emissions
- travel time matches the event delay

Example:

```text
Source
  |
  | wind transport
  v
Sensor
```

Useful function:

```python
calculate_wind_evidence()
```

---

# 60. Distance evidence

Distance matters because a source farther away may have a weaker immediate influence, although this depends on dispersion and meteorology.

Example:

```text
Source A = 0.4 km
Source B = 8 km
```

Source A may receive higher local-distance evidence, but Source B could still matter when wind and plume transport strongly support it.

Never use distance alone.

---

# 61. Temporal evidence

This checks whether the source activity and pollution event occurred at compatible times.

Example:

```text
Construction active:
10:00–16:00

Pollution event:
10:25
```

Good temporal match.

But:

```text
Construction active:
18:00–20:00

Pollution event:
11:00
```

Poor temporal match.

---

# 62. Activity evidence

The model should ask:

```text
Was the source actually active?
```

Examples:

```text
traffic = high
construction_active = 1
industry_operating = 1
fire_detected = 1
```

This is often stronger than simply knowing that the source exists.

---

# 63. Dispersion model

## What it is

A dispersion model estimates how pollutants emitted from a source could travel through the atmosphere.

## Why it is used

The project wants to answer:

```text
If source X were emitting at this time,
would the observed sensors see a plume like this?
```

## Possible approaches

### Simple

Gaussian plume/puff approximation.

### Intermediate

Trajectory-based backtracking.

### Advanced

HYSPLIT or another atmospheric dispersion framework.

---

# 64. Gaussian plume concept

A Gaussian plume approximates concentration downwind from a continuous source.

Conceptually:

```text
Source
  ●
   \\\\\
    \\\\\
     \\\\\
      \\\\\
       sensor zone
```

The model depends on:

- source strength
- wind
- distance
- stack height
- atmospheric stability
- dispersion parameters

For the capstone, use this as a supporting physical model rather than building a complete computational-fluid-dynamics system.

---

# 65. HYSPLIT

## What it is

HYSPLIT is a modeling system for atmospheric transport and dispersion.

## Why it is useful

It can support:

- trajectory analysis
- dispersion studies
- source/transport investigation

For your system:

```text
Candidate source
      +
meteorology
      +
sensor observations
      |
      v
dispersion simulation
      |
      v
compatibility score
```

It is an advanced feature and does not need to be in the first MVP.

---

# 66. Evidence fusion

## What it is

Combining different evidence types into a final source score.

Example:

```text
Wind evidence          0.90
Pollutant signature    0.85
Activity evidence      1.00
Traffic evidence       0.20
Satellite evidence    0.60
Citizen evidence      0.80
```

These become inputs to the final attribution process.

---

# 67. Bayesian thinking

A useful conceptual formulation is:

```text
P(Source | Evidence)
```

Meaning:

> Probability of a source given the observed evidence.

The evidence may include:

```text
pollutants
wind
distance
activity
traffic
satellite
citizen report
```

You do not need a full Bayesian network to implement the idea. A calibrated ML classifier plus explicit physical evidence can achieve a practical first version.

---

# 68. XGBoost

## What it is

XGBoost is a gradient-boosted decision-tree algorithm.

## Why it is suitable

It works well for structured/tabular features such as:

```text
PM2.5
PM10
NO2
wind_alignment
distance
traffic_index
construction_active
fire_count
industry_active
```

It is easier to train and explain than many deep neural networks.

## Use in project

```text
features
   |
   v
XGBoost
   |
   v
source probabilities
```

Documentation:
https://xgboost.readthedocs.io/

---

# 69. Scikit-learn

## What it is

A Python machine-learning library.

## Why use it

Useful for:

- preprocessing
- baseline models
- anomaly detection
- validation
- metrics
- train/test splitting

Documentation:
https://scikit-learn.org/

---

# 70. Isolation Forest

## What it is

An anomaly-detection algorithm.

## Why use it

It can identify unusual observations without requiring labels for every event.

Example:

```text
Normal PM2.5:
60, 65, 70, 62, 68

Anomaly:
190
```

## Caveat

An unusual reading might be:

```text
real pollution
```

or:

```text
sensor fault
```

Therefore anomaly detection must be followed by sensor-quality validation.

---

# 71. SHAP

## What it is

SHAP is a model-explanation method.

## Why it is useful

It can show which features influenced a source prediction.

Example:

```text
Prediction: Construction

Positive:
PM10 spike
Active construction
Upwind alignment
Dry weather

Negative:
Low construction proximity
Strong traffic signature
```

Documentation:
https://shap.readthedocs.io/

---

# 72. Confidence

## What it means

Confidence estimates how trustworthy the attribution result is.

Confidence should increase when:

```text
multiple sensors agree
+
good-quality sensors
+
clear wind
+
strong source signature
+
source activity confirmed
+
independent evidence agrees
```

Confidence should decrease when:

```text
sensor failure
+
missing wind
+
conflicting evidence
+
satellite unavailable
+
only one sensor
```

---

# 73. Contribution estimation

## What it means

Contribution estimates how much of the pollution excess may be associated with each source.

Example:

```text
Observed excess PM2.5 = 100 units

Traffic       40
Construction  25
Burning       20
Background    15
```

This is different from probability.

A source can have:

```text
high probability
```

but:

```text
small estimated contribution
```

---

# 74. Forecasting

## What it means

Predicting future pollution.

Possible horizons:

```text
15 min
30 min
1 hour
3 hours
```

## Inputs

```text
current pollution
wind
weather forecast
traffic forecast/current state
source activity
historical patterns
```

## Outputs

```text
future pollution
affected grids
estimated duration
uncertainty
```

---

# 75. Exposure

## What it means

Exposure describes how much pollution people in a location may encounter.

The project does not need individual medical records.

Use aggregate information:

```text
grid pollution
+
population
+
duration
+
sensitive locations
```

---

# 76. Population exposure

Example:

```text
Grid G42

PM2.5 = 145
Population = 12,400
Duration = 90 minutes
Schools = 2
Hospital = 1
```

The system calculates an exposure indicator.

A simple conceptual metric:

```text
Exposure
≈
Concentration × Duration × Population
```

More sophisticated versions can add vulnerability weights.

---

# 77. Vulnerable locations

Potential sensitive locations:

- schools
- hospitals
- elderly-care facilities
- dense residential areas
- outdoor markets
- transit terminals

Why?

Because a pollution event may need a faster warning even if the city-wide AQI has not changed dramatically.

---

# 78. Neighbourhood alert

A neighbourhood alert should contain:

```text
Location
Pollutant
Current level
Trend
Expected duration
Probable source category
Confidence
Basic precaution
Expiry time
```

Example:

```text
Ward 21
PM10 rapidly increasing

Probable source:
Construction

Confidence:
High

Expected duration:
60–90 minutes

Action:
Avoid unnecessary outdoor exposure near the hotspot.
```

---

# 79. Recommendation engine

## What it is

A system that converts analytical results into suggested operational actions.

## Why use it

The project should not stop at:

```text
Construction = 64%
```

It should answer:

```text
What should the authority do?
```

---

# 80. Rule engine

The first recommendation engine should be rule-based.

Example:

```text
IF construction_probability > 0.60
AND PM10 is rapidly increasing
THEN:
    recommend construction inspection
```

Another:

```text
IF traffic_probability > 0.60
AND traffic_index > 0.80
THEN:
    recommend traffic-management response
```

Rules are easy to explain in a viva.

---

# 81. Action-impact simulation

## What it is

Estimating what might happen if an action is taken.

Example:

```text
Current:
Traffic contribution = 45%

Proposed:
temporary diversion

Predicted:
PM2.5 reduction = 8–14%
Traffic delay = +5 minutes
```

This is an advanced feature.

---

# 82. FastAPI

## What it is

A Python framework for building APIs.

## Why use it

Person 3 needs to connect:

```text
Database
+
AI
+
Exposure
+
Recommendations
```

to:

```text
React frontend
```

FastAPI is well suited to that.

Documentation:
https://fastapi.tiangolo.com/

---

# 83. REST API

## What it is

A standard way for applications to request resources over HTTP.

Example:

```http
GET /api/v1/pollution/current
```

Response:

```json
{
  "grid_id": "G042",
  "pm25": 145,
  "pm10": 210
}
```

---

# 84. API versioning

Use:

```text
/api/v1/
```

Why?

Later, you can add:

```text
/api/v2/
```

without immediately breaking old clients.

---

# 85. Pydantic

## What it is

A Python library for data validation and structured models.

## Why use it

It enforces API contracts.

Example conceptually:

```python
class PollutionRecord:
    timestamp
    grid_id
    pm25
    pm10
```

If Person 1 sends:

```text
pm_25
```

instead of:

```text
pm25
```

the contract can catch the mismatch.

---

# 86. WebSockets

## What they are

A persistent connection allowing real-time data updates.

## Why use them

Instead of the dashboard asking every few seconds:

```text
Any new pollution?
```

the server can push updates:

```text
NEW EVENT
PM10 SPIKE IN G042
```

Useful for the live dashboard.

---

# 87. React

## What it is

A frontend library for building interactive web interfaces.

## Why use it

The project needs:

- live maps
- charts
- alerts
- event details
- source-attribution visualization

React is well suited to this.

---

# 88. TypeScript

## What it is

A typed version/superset of JavaScript.

## Why use it

It helps catch mistakes in shared frontend data structures.

Example:

```typescript
interface AttributionResult {
    event_id: string;
    primary_source_type: string;
    confidence: number;
}
```

This is useful because API responses must remain consistent.

---

# 89. Leaflet

## What it is

A JavaScript mapping library.

## Why use it

It can display:

```text
sensor points
roads
hotspots
source locations
construction
industrial facilities
fire detections
pollution cells
```

---

# 90. MapLibre

MapLibre is an open-source map-rendering ecosystem.

Use it instead of Leaflet if you want:

- more advanced styling
- vector-tile based maps
- greater control over map rendering

For a student project:

```text
Leaflet = simplest
MapLibre = more advanced
```

Choose one, not both.

---

# 91. Recharts

## What it is

A React charting library.

## Why use it

For:

```text
PM2.5 timeline
PM10 timeline
source contributions
forecast
exposure
```

---

# 92. Dashboard architecture

```text
                  FASTAPI
                     |
        +------------+------------+
        |            |            |
        v            v            v
   Pollution     Attribution   Exposure
        |            |            |
        +------------+------------+
                     |
                     v
                  React
                     |
         +-----------+-----------+
         |           |           |
         v           v           v
        Map        Charts      Alerts
```

---

# 93. Government dashboard

The government version should answer:

```text
Where?
Why?
How confident?
Who is affected?
What should we do?
```

Main components:

```text
Live map
Active events
Source probabilities
Evidence
Exposure
Recommendations
Case tracking
```

---

# 94. Citizen dashboard

The citizen version should be simpler:

```text
Current AQI
Local pollution
Current warning
Expected duration
Basic precautions
Report pollution
```

Do not expose internal enforcement details unnecessarily.

---

# 95. Database relationships

Conceptual relationship:

```text
Sensor
  |
  +---- readings ----> AirQualityRecord
  |
  +---- located in ---> Grid

Grid
  |
  +---- contains ---> PollutionEvent
  |
  +---- contains ---> Exposure

PollutionEvent
  |
  +---- has ---> CandidateSource
  |
  +---- has ---> AttributionResult
  |
  +---- has ---> Recommendation
```

---

# 96. Feature store

## What it is

A place to store ML-ready features in a consistent form.

## Why it is useful

Training and real-time inference should use compatible feature definitions.

Example:

```text
training:
traffic_index = 0.83

production:
traffic_index = 0.83
```

not two different formulas.

For a student project, a versioned feature table in PostgreSQL is enough. A dedicated feature-store product is optional.

---

# 97. Data versioning

Data used for experiments should be versioned.

Example:

```text
dataset_v1
dataset_v2
dataset_v3
```

Track:

```text
source
download date
processing version
filtering logic
features
target labels
```

This makes your results reproducible.

---

# 98. Model versioning

Every deployed model should have a version:

```text
attribution_v1
attribution_v2
```

Store:

```text
model version
training dataset version
feature version
metrics
training date
```

---

# 99. ML training pipeline

```text
Historical data
       |
       v
Cleaning
       |
       v
Feature engineering
       |
       v
Train / validation split
       |
       v
Model training
       |
       v
Evaluation
       |
       v
Model artifact
       |
       v
Model registry
       |
       v
Deployment
```

---

# 100. Training data problem

The biggest research challenge is that exact pollution-source labels are limited.

Examples of high-quality labels:

```text
verified waste-burning incident
verified construction violation
traffic closure event
industrial shutdown/restart
field inspection
mobile sensor validation
```

---

# 101. Synthetic data

## Why use it

You can simulate known source events.

Example:

```text
Scenario:
Construction source

Expected:
PM10 ↑
Dryness ↑
Construction_active = 1
Wind alignment strong
```

This creates training/testing situations where the true source is known.

---

# 102. Active learning

## What it is

The model asks for human verification where uncertainty is high.

Example:

```text
AI confidence = 0.52

System:
Request field verification
```

After the officer confirms the actual source:

```text
new verified label
      |
      v
training data
```

This can progressively improve the model.

---

# 103. Model evaluation

## Classification

Use:

```text
precision
recall
F1-score
confusion matrix
```

## Probabilities

Use:

```text
Brier score
calibration curve
expected calibration error
```

## Contribution

Use:

```text
MAE
RMSE
```

## Event detection

Use:

```text
false positives
false negatives
detection lead time
```

---

# 104. Precision

## Meaning

Of all predictions that the model called a source:

> how many were actually correct?

Important when false accusations are costly.

---

# 105. Recall

## Meaning

Of all truly occurring source events:

> how many did the system successfully detect?

Important for not missing severe pollution events.

---

# 106. F1-score

## Meaning

A balance between precision and recall.

Useful for comparing source-classification models.

---

# 107. Confusion matrix

Shows which source categories the model confuses.

Example:

```text
                 Predicted
             T    C    I    B

Actual T     8    2    0    0
       C     1    9    0    0
       I     0    1    8    1
       B     0    1    1    8
```

This may reveal that:

```text
construction
```

and:

```text
road dust
```

are hard to distinguish.

---

# 108. Explainability

The system should not simply display:

```text
Construction: 64%
```

It should also display:

```text
Why?

+ PM10 spike
+ upwind construction
+ active permit
+ dry conditions
+ nearby citizen report
```

This is particularly important for government decision support.

---

# 109. MLOps

## What it means

The discipline of managing ML models after they are developed.

It covers:

```text
training
evaluation
deployment
monitoring
versioning
retraining
rollback
```

For your project, basic MLOps is enough.

---

# 110. Model drift

A model may become worse because the environment changes.

Examples:

```text
new traffic patterns
new construction zones
new industrial activity
sensor changes
seasonal changes
```

Monitor performance over time.

---

# 111. Data drift

Input distributions can change.

Example:

```text
Training:
traffic_index mostly 0.2–0.7

Production:
traffic_index mostly 0.7–1.0
```

This could reduce model reliability.

---

# 112. Logging

Log important events:

```text
data ingestion failure
sensor offline
model prediction
API error
alert generated
recommendation generated
officer action
```

Do not log unnecessary personal information.

---

# 113. Monitoring

Monitor:

```text
CPU
memory
API latency
database health
sensor availability
ingestion lag
model inference latency
data freshness
```

---

# 114. Docker

## What it is

Docker packages applications and dependencies into containers.

## Why use it

It solves:

```text
"It works on my laptop."
```

problems.

Example:

```text
docker-compose
   |
   +-- backend
   +-- frontend
   +-- postgres
   +-- mqtt
   +-- redis (optional)
```

---

# 115. Git

## What it is

Version-control software.

## Why use it

Three people need to:

- work in parallel
- track changes
- merge code
- revert mistakes
- review each other's work

---

# 116. GitHub

Use GitHub for:

```text
repository
branches
issues
pull requests
reviews
GitHub Actions
```

---

# 117. Branching model

Recommended:

```text
main
  |
  v
develop
  |
  +-- feature/person1-data
  +-- feature/person2-ai
  +-- feature/person3-app
```

---

# 118. Continuous integration

## What it means

Whenever code is pushed:

```text
GitHub
   |
   v
tests
   |
   v
lint
   |
   v
build
```

This catches integration problems early.

---

# 119. Unit testing

Test small pieces.

Examples:

```text
calculate_distance_km()
calculate_upwind_score()
detect_pollution_anomaly()
predict_source_probabilities()
calculate_neighbourhood_exposure()
```

---

# 120. Integration testing

Test the connection between modules:

```text
Person 1 data
      |
      v
Person 2 AI
      |
      v
Person 3 API
      |
      v
Dashboard
```

---

# 121. End-to-end testing

Test one complete pollution event:

```text
sensor reading
    ->
event detected
    ->
source identified
    ->
exposure calculated
    ->
recommendation generated
    ->
dashboard updated
```

---

# 122. Postman

Use Postman to test APIs before frontend integration.

Example:

```http
GET /api/v1/events/EVT1042
```

Verify:

```text
HTTP 200
valid JSON
correct schema
correct fields
```

---

# 123. Security

The system should protect:

```text
API credentials
sensor credentials
database
citizen data
industrial records
government accounts
```

Use:

```text
environment variables
secret management
HTTPS
authentication
authorization
```

Never commit:

```text
API keys
passwords
tokens
private certificates
```

to GitHub.

---

# 124. Authentication

Different users need different access.

Example:

```text
Citizen
  -> public data + own reports

Officer
  -> cases + evidence + recommendations

Admin
  -> system configuration + user management
```

This is called role-based access control.

---

# 125. Privacy

The system should avoid unnecessary personal data.

For traffic:

```text
Prefer:
road-level aggregate traffic

Avoid:
individual vehicle tracking
```

For citizen images:

```text
store only what is necessary
remove unnecessary metadata
limit access
```

---

# 126. Responsible AI

The system must not say:

```text
Factory X is guilty.
```

based solely on an ML probability.

It should say:

```text
Factory X is a high-probability candidate
based on available evidence.

Human verification recommended.
```

This is especially important for enforcement applications.

---

# 127. Unknown source

A robust source-attribution model must allow:

```text
unknown
```

or:

```text
unresolved
```

Why?

Because forcing every event into a known category creates false certainty.

---

# 128. False positives

A false positive occurs when the system reports a source that was not actually responsible.

Example:

```text
Model:
Construction

Reality:
Road dust
```

This is why confidence and human verification are important.

---

# 129. False negatives

A false negative occurs when the system misses a real source.

Example:

```text
Waste burning occurred
but
model did not detect it.
```

Recall is important here.

---

# 130. Exposure warning vs source accusation

These should be separated.

The public may need:

```text
High PM2.5 in Ward 21
```

without needing:

```text
Company X caused it.
```

Source attribution can remain an internal operational layer until verified.

---

# 131. Recommended MVP

Build these first:

```text
1. CPCB/OpenAQ data
2. Weather/wind
3. OpenStreetMap
4. Construction dataset
5. Traffic proxy
6. PostgreSQL/PostGIS
7. Pollution baseline
8. Anomaly detection
9. Wind-based candidate generation
10. XGBoost source attribution
11. Confidence
12. Exposure estimate
13. FastAPI
14. React + map dashboard
```

---

# 132. Advanced extensions

After MVP:

```text
Sentinel-5P
NASA FIRMS
Citizen image AI
HYSPLIT
Forecasting
Counterfactual action simulation
Mobile sensors
Graph neural networks
Real-time MQTT network
Advanced MLOps
```

---

# 133. Complete technical stack

```text
LANGUAGES
|
+-- Python
+-- TypeScript
+-- SQL

DATA INGESTION
|
+-- HTTPX / Requests
+-- MQTT
+-- Scheduled jobs

DATA PROCESSING
|
+-- Pandas
+-- NumPy
+-- SciPy
+-- GeoPandas

GIS
|
+-- PostGIS
+-- Shapely
+-- OpenStreetMap
+-- Overpass

DATABASE
|
+-- PostgreSQL
+-- PostGIS
+-- optional TimescaleDB
+-- optional Redis

AI / ML
|
+-- Scikit-learn
+-- XGBoost
+-- SHAP
+-- optional PyTorch

PHYSICS / ATMOSPHERIC
|
+-- wind geometry
+-- Gaussian plume/puff concepts
+-- optional HYSPLIT

SATELLITE
|
+-- Sentinel-5P
+-- NASA FIRMS

BACKEND
|
+-- FastAPI
+-- Pydantic
+-- Uvicorn

FRONTEND
|
+-- React
+-- TypeScript
+-- Leaflet OR MapLibre
+-- Recharts
+-- Tailwind CSS

DEVOPS
|
+-- Git
+-- GitHub
+-- Docker
+-- GitHub Actions

TESTING
|
+-- Pytest
+-- Postman
+-- Playwright
```

---

# 134. Three-person ownership

## PERSON 1 — Data/GIS

```text
CPCB
OpenAQ
Weather
Traffic ingestion
Satellite ingestion
FIRMS ingestion
Construction data
Industrial data
Sensors
Cleaning
Calibration
PostGIS
Spatial grid
```

## PERSON 2 — AI/ML

```text
Baseline
Anomaly detection
Pollution events
Candidate sources
Wind evidence
Signatures
XGBoost
Evidence fusion
Contribution
Confidence
Forecasting
Evaluation
SHAP
```

## PERSON 3 — Application

```text
FastAPI
Exposure
Recommendations
Alerts
React
Maps
Charts
Citizen UI
Government UI
Integration
```

---

# 135. Data ownership boundary

Person 1 delivers:

```text
PollutionRecord
ContextRecord
Source records
```

Person 2 consumes those and delivers:

```text
PollutionEvent
AttributionResult
```

Person 3 consumes those and delivers:

```text
ExposureResult
RecommendationResult
API responses
```

This boundary is what allows parallel development.

---

# 136. Recommended end-to-end data flow

```text
CPCB/OpenAQ ------------------+
Sensors ----------------------+
Weather ----------------------+
Traffic ----------------------+ 
OSM/GIS ----------------------+
Construction -----------------+
Industrial -------------------+
Sentinel-5P ------------------+
FIRMS ------------------------+
Citizen reports --------------+
                               |
                               v
                       PERSON 1
                 INGEST + CLEAN + CALIBRATE
                               |
                               v
                      PostgreSQL/PostGIS
                               |
                               v
                       PERSON 2
                EVENT + ATTRIBUTION + AI
                               |
                               v
                        AttributionResult
                               |
                               v
                       PERSON 3
                  API + EXPOSURE + ACTION
                               |
                  +------------+------------+
                  |                         |
                  v                         v
              Government                Citizens
              Dashboard                 Dashboard
```

---

# 137. Example complete event

```text
09:55
Traffic begins increasing

10:00
Traffic index = 0.87

10:05
NO2 and PM2.5 begin rising

10:08
Three sensors agree

10:09
Pollution-event detector triggers

10:10
Wind analysis points toward road corridor

10:11
Construction site also appears as candidate

10:12
AI evidence fusion:

Traffic       0.68
Construction  0.19
Road dust     0.08
Other         0.05

10:13
Confidence = 0.89

10:14
Exposure engine finds:
Population = 10,800
Schools = 2

10:15
Recommendation:
Traffic management + anti-idling enforcement

10:20
Dashboard updated

10:45
Traffic action begins

11:10
Pollution falls faster than no-action forecast

11:15
Action outcome recorded
```

---

# 138. Why the architecture is hybrid

The project should combine:

```text
PHYSICS
+
STATISTICS
+
MACHINE LEARNING
+
GIS
+
DOMAIN RULES
```

instead of relying entirely on deep learning.

### Physics tells us:

```text
Can the source physically influence the sensor?
```

### Statistics tells us:

```text
Is this event unusual?
```

### ML tells us:

```text
How does the evidence pattern resemble historical examples?
```

### GIS tells us:

```text
Where are the sources and affected locations?
```

### Domain rules tell us:

```text
What action is operationally reasonable?
```

Together, these make a stronger decision-support system.

---

# 139. What not to claim

Do not claim:

```text
100% accurate source identification
```

Do not claim:

```text
AI proves legal responsibility
```

Do not treat:

```text
satellite observation = ground concentration
```

Do not treat:

```text
low-cost sensor = reference monitor
```

Do not assume:

```text
nearest source = cause
```

The platform is a probabilistic decision-support system.

---

# 140. Suggested research questions

The project can be framed around these questions:

### RQ1

Can multimodal data improve real-time pollution-event detection compared with pollutant thresholding alone?

### RQ2

Can wind, spatial relationships and source activity improve source attribution accuracy?

### RQ3

Can combining ML with physical evidence reduce false source attribution?

### RQ4

Can neighbourhood-level exposure warnings be generated at higher spatial resolution than sparse official monitoring alone?

### RQ5

Can recommended interventions reduce pollution exposure in simulated or observed events?

---

# 141. Suggested final-year-project contribution

Your strongest contribution should be stated as:

> A multimodal, physics-informed AI framework for near-real-time urban air-pollution source attribution that combines heterogeneous environmental, mobility, geospatial, satellite and citizen-generated evidence to generate probabilistic source attribution, neighbourhood exposure warnings and targeted operational recommendations.

This is much stronger than:

> "We made an AQI prediction app."

---

# 142. Official/reference resources

Use official documentation when implementing the corresponding component.

### CPCB

https://cpcb.nic.in/

### OpenAQ

https://docs.openaq.org/

### Open-Meteo

https://open-meteo.com/en/docs

### Copernicus Data Space

https://documentation.dataspace.copernicus.eu/

### NASA FIRMS

https://firms.modaps.eosdis.nasa.gov/

### OpenStreetMap Overpass

https://wiki.openstreetmap.org/wiki/Overpass_API

### PostGIS

https://postgis.net/documentation/

### FastAPI

https://fastapi.tiangolo.com/

### Scikit-learn

https://scikit-learn.org/

### XGBoost

https://xgboost.readthedocs.io/

### SHAP

https://shap.readthedocs.io/

### India Open Government Data

https://data.gov.in/

---

# 143. Official FIRMS implementation notes

NASA FIRMS provides active-fire products from instruments including MODIS and VIIRS and makes active-fire information available through web services and downloadable formats.

For the project:

```text
FIRMS
  |
  v
fire location
  +
time
  +
confidence
  +
FRP where available
  |
  v
spatial join with pollution events
  |
  v
wind alignment
  |
  v
burning evidence
```

FIRMS documentation also distinguishes near-real-time and standard/science-quality products. For final research analysis, preserve the product version and processing status used.

Reference:
https://firms.modaps.eosdis.nasa.gov/
https://firms.modaps.eosdis.nasa.gov/web-services/

---

# 144. Final learning order for the team

## Person 1 should learn in this order

```text
Python
  ->
Pandas
  ->
REST APIs
  ->
JSON
  ->
PostgreSQL
  ->
PostGIS
  ->
GeoPandas
  ->
MQTT
  ->
Data pipelines
```

## Person 2 should learn in this order

```text
Python
  ->
NumPy/Pandas
  ->
Statistics
  ->
Scikit-learn
  ->
Anomaly detection
  ->
XGBoost
  ->
Feature engineering
  ->
GIS/wind calculations
  ->
Evidence fusion
  ->
SHAP
  ->
Forecasting
```

## Person 3 should learn in this order

```text
HTTP/REST
  ->
FastAPI
  ->
Pydantic
  ->
React
  ->
TypeScript
  ->
Leaflet/MapLibre
  ->
Charts
  ->
WebSockets
  ->
Dashboard architecture
```

---

# 145. Final mental model

Every team member should understand this complete chain:

```text
                         REAL WORLD
                             |
          +------------------+------------------+
          |                  |                  |
        SOURCES            WEATHER           PEOPLE
          |                  |                  |
          v                  v                  v
    Pollution emitted    Wind transports     Reports
          |                  |                  |
          +------------------+------------------+
                             |
                             v
                        SENSOR DATA
                             |
                             v
                   PERSON 1 DATA PIPELINE
                             |
                   clean + calibrate + GIS
                             |
                             v
                         DATA STORE
                             |
                             v
                     PERSON 2 AI PIPELINE
                             |
                  detect + attribute + forecast
                             |
                             v
                    ATTRIBUTION RESULT
                             |
                             v
                    PERSON 3 APP PIPELINE
                             |
                exposure + recommendations
                             |
              +--------------+--------------+
              |                             |
              v                             v
         GOVERNMENT                     CITIZENS
```

---

# 146. The single most important design principle

The system should never jump directly from:

```text
PM2.5 increased
```

to:

```text
Construction caused it.
```

The correct reasoning chain is:

```text
PM2.5 increased
      |
      v
Is the increase real?
      |
      v
Which area is affected?
      |
      v
What was the normal baseline?
      |
      v
Where is the air coming from?
      |
      v
Which sources are upwind?
      |
      v
Were those sources active?
      |
      v
Does the pollutant signature match?
      |
      v
Do satellite/fire/traffic/citizen data agree?
      |
      v
Does the dispersion pattern fit?
      |
      v
Calculate probabilities
      |
      v
Calculate confidence
      |
      v
Estimate contributions
      |
      v
Assess exposure
      |
      v
Recommend action
      |
      v
Human verification
```

That reasoning chain is the core of the entire project.
