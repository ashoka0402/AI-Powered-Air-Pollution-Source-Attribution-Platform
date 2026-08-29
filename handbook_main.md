# AI-Powered Air Pollution Source-Attribution Platform
## Complete Concepts, Algorithms, AI/ML Keywords, Alternatives, and Implementation Handbook
### Master learning + engineering reference for the 3-person team

---

# 0. How to use this handbook

This handbook is deliberately broader than the implementation plan.

Its purpose is to make sure the team understands not only:

- **what to build**
- but also **what concepts are behind it**
- **which algorithms are available**
- **what alternatives exist**
- **why one approach may be selected over another**
- **what data each method needs**
- **what the output means**
- **what its limitations are**

For every major topic, this handbook tries to answer:

1. **What is it?**
2. **Why does this project need it?**
3. **How does it work?**
4. **How will we implement it?**
5. **What goes in?**
6. **What comes out?**
7. **How does it connect to other modules?**
8. **Who owns it?**
9. **Which alternatives exist?**
10. **Which option is recommended for the MVP?**
11. **What is an advanced/research option?**
12. **What are the important AI/ML keywords?**

---

# 1. Project goal

## 1.1 Problem

Urban air pollution changes continuously because different sources operate at different times and locations.

Examples:

- traffic during rush hour
- construction during working hours
- industrial activity
- road dust
- waste burning
- biomass burning
- landfill fires
- regional smoke
- regional dust
- weather-driven accumulation

A traditional air-quality system might produce:

```text
PM2.5 = 142 µg/m³
AQI = High
```

Our system should go further:

```text
PM2.5 is increasing rapidly
        |
        v
This is an abnormal event
        |
        v
Affected area = Grid G42
        |
        v
Likely source candidates:
    Traffic
    Construction
    Road dust
    Burning
        |
        v
Wind + spatial + pollutant + activity evidence
        |
        v
Source probabilities:
    Traffic       18%
    Construction  61%
    Road dust     14%
    Burning        3%
    Unknown        4%
        |
        v
Confidence = 0.84
        |
        v
Exposure = 12,400 people
        |
        v
Recommended action = inspect active construction site
```

---

# 2. Core architecture

```text
REAL WORLD
│
├── Pollution sources
├── Atmosphere
├── Traffic
├── Construction
├── Industry
└── Citizens
        |
        v
DATA SOURCES
│
├── CPCB/OpenAQ
├── Low-cost sensors
├── Weather
├── Traffic
├── GIS
├── Satellite
├── Fire products
├── Construction records
├── Industrial records
└── Citizen reports
        |
        v
PERSON 1
DATA ENGINEERING + GIS
│
├── ingestion
├── cleaning
├── calibration
├── quality control
├── spatial processing
└── database
        |
        v
COMMON DATA LAYER
        |
        v
PERSON 2
AI/ML + SOURCE ATTRIBUTION
│
├── baseline
├── anomaly detection
├── event detection
├── candidate-source generation
├── wind analysis
├── source signatures
├── ML
├── evidence fusion
├── attribution
├── contribution
└── confidence
        |
        v
PERSON 3
APPLICATION + EXPOSURE + ACTION
│
├── API
├── exposure
├── alerts
├── recommendation
└── dashboard
        |
        v
USERS
├── Pollution-control authorities
├── Municipal teams
├── Traffic teams
└── Citizens
```

---

# 3. Key AI/ML vocabulary for the project

Before studying individual algorithms, the team should understand these terms.

## 3.1 Feature

A measurable input used by a model.

Example:

```text
pm25
pm10
no2
traffic_index
wind_speed
wind_direction
distance_to_source
construction_active
```

---

## 3.2 Target / label

The value the model is trying to predict.

For source classification:

```text
traffic
construction
industrial
road_dust
burning
regional_transport
unknown
```

---

## 3.3 Training data

Examples used to learn the relationship between features and targets.

```text
features ---> model ---> source class
```

---

## 3.4 Inference

Using a trained model on new observations.

```text
new sensor event
      |
      v
trained model
      |
      v
prediction
```

---

## 3.5 Supervised learning

Training with known labels.

Example:

```text
Historical event
features = [PM10, NO2, wind, traffic, construction...]
label = construction
```

Algorithms:

- Logistic Regression
- Random Forest
- XGBoost
- SVM
- Neural networks

---

## 3.6 Unsupervised learning

Learning patterns without labeled targets.

Useful for:

- anomaly detection
- clustering
- discovering pollution regimes

Algorithms:

- K-Means
- DBSCAN
- Isolation Forest
- PCA
- Autoencoders

---

## 3.7 Semi-supervised learning

Uses a small labeled dataset plus a larger unlabeled dataset.

This is potentially useful because source labels are difficult to obtain.

---

## 3.8 Self-supervised learning

The model creates learning signals from the data itself.

More advanced and not necessary for the MVP.

---

## 3.9 Classification

Predicting a category.

Example:

```text
Input event
      |
      v
Traffic = 0.71
Construction = 0.18
Burning = 0.04
Industry = 0.07
```

---

## 3.10 Regression

Predicting a continuous number.

Examples:

```text
PM2.5 = 146
source contribution = 0.42
future PM2.5 = 158
```

---

## 3.11 Probability

A prediction describing relative likelihood.

Example:

```text
P(construction) = 0.64
```

It is not automatically proof that construction caused the event.

---

## 3.12 Confidence

A broader assessment of result reliability.

It may consider:

- model calibration
- sensor quality
- number of sensors
- wind availability
- independent evidence
- missing data

A source probability and an overall confidence should be stored separately.

---

## 3.13 Uncertainty

The range of plausible values around an estimate.

Example:

```text
PM2.5 forecast:
150 ± 25
```

or:

```text
Construction contribution:
45–62%
```

---

## 3.14 Calibration

Calibration can mean two different things in this project.

### Sensor calibration

Correcting sensor measurements against reference measurements.

### Probability calibration

Making predicted probabilities better match actual frequencies.

Example:

```text
Events predicted at 80% confidence
should occur roughly 80% of the time
```

---

## 3.15 Overfitting

The model memorizes training data and performs poorly on new situations.

Typical causes:

- too many features
- too-complex model
- data leakage
- too little training data

---

## 3.16 Underfitting

The model is too simple to capture the actual relationships.

---

## 3.17 Data leakage

Information that would not be available at prediction time accidentally enters training.

This is especially dangerous in time-series problems.

Example:

Using future pollution measurements to predict an event that occurred in the past.

---

## 3.18 Feature engineering

Converting raw observations into useful model variables.

Example:

```text
wind direction
+
source bearing
=
wind alignment score
```

---

## 3.19 Embedding

A learned numerical representation of a complex object.

Potential advanced uses:

- satellite image embeddings
- citizen-image embeddings
- road-context embeddings

Not required for the MVP.

---

## 3.20 Hyperparameter

A model configuration selected before/during training.

Examples:

```text
tree depth
learning rate
number of estimators
minimum samples
```

---

# 4. Time-series data

## What is it?

Data indexed by time.

Examples:

```text
10:00 -> PM2.5 = 80
10:05 -> PM2.5 = 85
10:10 -> PM2.5 = 91
```

## Why do we need it?

Pollution is dynamic.

The system must know:

- what is happening now
- what happened recently
- what is normal at this time
- whether a spike is unusual
- whether the situation is improving or worsening

## How is it used?

```text
Historical time series
      |
      v
baseline
      |
      v
current observation
      |
      v
anomaly/event
```

## Data in

```text
timestamp
pollutants
weather
traffic
source activity
```

## Data out

```text
trend
baseline
event
forecast features
```

## Algorithms/keywords

- rolling mean
- rolling median
- EWMA
- seasonal decomposition
- ARIMA
- SARIMA
- exponential smoothing
- LSTM
- GRU
- temporal transformer
- temporal cross-validation

## MVP

Use:

```text
rolling statistics
+
time-of-day/day-of-week baseline
```

---

# 5. Data ingestion

## What is it?

The process of collecting external data and moving it into our system.

## Why use it?

The system cannot perform AI unless data continuously arrives.

## Architecture

```text
External API / sensor
        |
        v
connector
        |
        v
validation
        |
        v
normalization
        |
        v
database
```

## Examples

```text
CPCB        -> HTTP/API adapter
OpenAQ      -> HTTP/API adapter
Open-Meteo  -> HTTP/API adapter
FIRMS       -> HTTP/file adapter
Sentinel    -> geospatial data adapter
Sensor      -> MQTT
```

## Data in

Raw external data.

## Data out

Canonical internal records.

## Alternatives

```text
REST API
WebSocket
MQTT
batch CSV
SFTP
database replication
```

## MVP

Python API clients + MQTT for sensors.

## Owner

**Person 1**

---

# 6. ETL and ELT

## What is ETL?

```text
Extract
Transform
Load
```

Transform before storing.

## What is ELT?

```text
Extract
Load
Transform
```

Store raw data first, then transform.

## Why this matters

For research, preserving raw data is valuable.

Recommended:

```text
External source
    |
    v
RAW STORAGE
    |
    v
Transform
    |
    v
PROCESSED STORAGE
```

This is closer to an ELT approach.

## MVP

Use raw + processed folders/tables.

---

# 7. Data validation

## What is it?

Checking whether input data is plausible.

## Examples

```text
PM2.5 < 0       -> invalid
humidity > 100  -> invalid
wind direction > 360 -> invalid
missing timestamp -> invalid
```

## Why needed?

Bad data becomes bad AI.

## Algorithms

Mostly rule-based, not ML.

Possible checks:

- range validation
- type validation
- uniqueness
- completeness
- freshness
- cross-field rules
- temporal consistency

## Data in

Raw observation.

## Data out

```text
valid
suspect
invalid
```

---

# 8. Missing-value handling

## What is it?

Handling observations that are absent.

## Why needed?

Sensors and APIs can fail.

## Alternatives

### Option A — Drop

Best when very few values are missing.

### Option B — Forward fill

Useful for slowly changing variables, but dangerous for rapidly changing pollution.

### Option C — Interpolation

Useful for short time gaps.

### Option D — Model-based imputation

Use regression/ML to estimate missing values.

### Option E — Leave missing

Often better than inventing data when uncertainty is high.

## MVP

Use short-gap interpolation plus explicit missingness flags.

## Advanced

Multiple imputation or probabilistic imputation.

---

# 9. Outlier detection

## What is it?

Finding observations that are unusually different.

Important distinction:

```text
outlier != error
```

A real pollution plume can be a genuine outlier.

## Algorithms

### Statistical

- z-score
- modified z-score
- IQR
- Hampel filter

### ML

- Isolation Forest
- Local Outlier Factor
- One-Class SVM
- Autoencoder

## Best approach

Use:

```text
data-quality rules
+
statistical detection
+
ML anomaly detection
```

rather than deleting every outlier.

---

# 10. Sensor calibration

## What is it?

Correcting low-cost sensor readings using reference observations.

## Why use it?

Low-cost sensors can have:

- bias
- humidity effects
- temperature effects
- drift
- cross-sensitivity

## Basic example

```text
Raw PM2.5 = 130
Reference = 100
```

Model learns correction.

## Mathematical view

```text
PM_corrected
=
f(
    PM_raw,
    humidity,
    temperature,
    sensor_id,
    season
)
```

## Alternatives

### Linear regression

Simple and interpretable.

### Polynomial regression

Captures simple nonlinear effects.

### Random Forest

Captures nonlinear interactions.

### XGBoost

Strong tabular performance.

### Neural network

Flexible but requires more data and complexity.

## MVP

Linear/polynomial model + quality checks.

## Advanced

Device-specific gradient boosting or domain adaptation.

## Owner

**Person 1**

---

# 11. Sensor drift detection

## What is it?

Detecting when sensor behaviour changes over time.

## Why needed?

A sensor may gradually stop matching its reference.

## Methods

- residual monitoring
- CUSUM
- EWMA control chart
- change-point detection
- rolling calibration error

## Data in

```text
sensor reading
reference reading
time
```

## Data out

```text
drift score
sensor state
```

---

# 12. Spatial data

## What is it?

Data with geographic location.

Examples:

```text
POINT   -> sensor
LINE    -> road
POLYGON -> construction site
```

## Why use it?

The project is fundamentally spatial.

Questions:

```text
Which source is near the sensor?
Which source is upwind?
Which people are downwind?
```

---

# 13. Coordinate systems

## Latitude/longitude

Global geographic coordinates.

## Projected coordinate systems

Convert locations into units suitable for accurate local distance calculations.

## Why it matters

Do not casually calculate local distances using raw latitude/longitude as if they were planar x/y coordinates.

GIS libraries can handle this conversion.

---

# 14. Geospatial indexing

## What is it?

Converting a geographic location to a compact cell identifier.

Possible technologies:

- H3
- Geohash
- S2

## Why use it?

Fast neighbourhood aggregation.

```text
Sensor
   |
   v
H3 cell
   |
   v
aggregate pollution
```

## Alternatives

### H3

Very useful for hierarchical hexagonal grids.

### Geohash

Simple and widely understood.

### S2

Strong spherical spatial indexing.

## MVP

H3 or a simple fixed grid.

---

# 15. Spatial join

## What is it?

Combining datasets based on location.

Example:

```text
sensor
+
construction polygons
```

Question:

> Which construction site is nearest to each sensor?

## Tools

- PostGIS
- GeoPandas

## Algorithms/operations

- point-in-polygon
- nearest neighbor
- intersection
- buffer
- distance
- containment

---

# 16. Distance calculation

## What is it?

Distance between two geographic objects.

## Why use it?

A candidate-source score needs distance.

```text
sensor -> road
sensor -> construction
sensor -> industry
sensor -> fire
```

## Alternatives

- geodesic distance
- Haversine distance
- projected Euclidean distance
- network distance

## MVP

Use geodesic/Haversine for point-to-point candidate filtering.

---

# 17. Wind direction

## What is it?

The direction from which wind originates in meteorological convention.

Example:

```text
270°
```

usually indicates wind coming from west.

## Why use it?

It constrains source candidates.

If pollution is measured at point B, sources located in the plausible upwind sector are more relevant.

---

# 18. Wind vector representation

Angles are awkward for ML if used directly.

Better representation:

```text
wind_u = speed * cos(direction)
wind_v = speed * sin(direction)
```

## Why?

Angles are circular:

```text
359° and 1°
```

are very close, although numerically they appear far apart.

Alternative:

```text
sin(direction)
cos(direction)
```

This is a key **feature-engineering concept**.

---

# 19. Wind backtracking

## What is it?

Estimating the region from which air reaching the sensor originated.

## Simple method

1. Get sensor location.
2. Get wind direction.
3. Reverse the direction.
4. Draw an upwind search cone.
5. Search for sources inside it.

## Data in

```text
sensor coordinates
wind direction
wind speed
time window
```

## Data out

```text
upwind polygon/cone
candidate source list
```

## Advanced alternatives

- trajectory model
- HYSPLIT
- FLEXPART
- numerical weather transport
- inverse dispersion

## MVP

Geometric backtracking.

## Advanced

Trajectory/dispersion model.

---

# 20. Wind alignment score

## What is it?

A score describing how well a candidate source direction aligns with the wind.

Conceptually:

```text
source bearing
vs
upwind bearing
```

Example:

```text
0.95 -> excellent alignment
0.50 -> moderate
0.05 -> poor
```

## Why use it?

A source may be nearby but physically poorly aligned.

---

# 21. Atmospheric dispersion

## What is it?

The movement and dilution of pollutants in the atmosphere.

## Why use it?

Source attribution needs more than straight-line direction.

A pollutant plume:

- spreads
- dilutes
- moves
- can be delayed
- can be affected by atmospheric stability

---

# 22. Gaussian plume model

## What is it?

A simplified analytical model of pollutant concentration from a continuous source.

Typical conceptual inputs:

```text
source strength
wind speed
wind direction
stack height
distance
stability
```

## Why useful?

Fast and understandable.

## Weaknesses

Real urban flow can be much more complicated because of:

- buildings
- street canyons
- changing winds
- terrain
- intermittent emissions

## MVP

Optional supporting model.

---

# 23. Gaussian puff model

Unlike a steady plume, a puff represents a temporary release.

Useful for:

```text
short-duration burning event
truck plume
temporary construction dust
industrial upset
```

---

# 24. HYSPLIT

## What is it?

A meteorological transport and dispersion modeling system.

## Why it may be useful

For more advanced source-transport analysis.

## How it fits

```text
candidate source
+
meteorological data
+
event time
    |
    v
dispersion/trajectory model
    |
    v
predicted impact at sensors
```

## MVP?

No.

## Advanced research?

Yes.

---

# 25. Pollution baseline

## What is it?

The expected pollution under similar conditions.

Example:

```text
Expected PM10 = 90
Observed PM10 = 170
```

## Why use it?

A high value may be normal during certain conditions.

The system should detect:

```text
unexpected pollution
```

rather than merely:

```text
high pollution
```

---

# 26. Baseline algorithms

## Option 1 — Historical median

Use median for:

```text
same hour
same weekday
same season
```

Robust and simple.

## Option 2 — Moving average

Good for trends but can be distorted by spikes.

## Option 3 — EWMA

Weights recent observations more strongly.

## Option 4 — STL decomposition

Separates:

```text
trend
seasonality
residual
```

## Option 5 — SARIMA

Handles temporal structure.

## Option 6 — Gradient boosting baseline

Uses weather/traffic/context to predict expected pollution.

## Recommendation

MVP:

```text
historical median
+
rolling statistics
```

Advanced:

```text
weather-aware XGBoost baseline
```

---

# 27. Anomaly detection

## What is it?

Detecting unusual observations or events.

## Why use it?

This creates the trigger for the source-attribution pipeline.

## Algorithms

### Z-score

Simple:

```text
z = (x - mean) / standard_deviation
```

Good for approximately stable distributions.

### Modified z-score

Uses median and MAD.

More robust to outliers.

### IQR

Useful for simple statistical screening.

### Isolation Forest

Randomly partitions observations and isolates unusual samples.

### Local Outlier Factor

Looks for observations that are sparse relative to neighbours.

### One-Class SVM

Learns the boundary around normal data.

### Autoencoder

Neural network trained to reconstruct normal observations.

### Change-point detection

Finds where the statistical properties of a time series change.

## Recommendation

```text
baseline residual
+
robust threshold
+
Isolation Forest
```

---

# 28. Change-point detection

## What is it?

Finding the moment when a process changes.

Example:

```text
Normal:
70 72 74 71 73

Change:
115 132 148 140
```

## Algorithms

- CUSUM
- Bayesian online change-point detection
- PELT
- binary segmentation
- rolling-statistic threshold

## Why use it?

Pollution events are often better represented as a **change in regime** rather than one isolated outlier.

## MVP

CUSUM or rolling residual threshold.

---

# 29. Pollution-event detection

## What is it?

Combining anomaly evidence over space and time to create an actual event.

## Why not just detect one anomaly?

One bad sensor should not create a city emergency.

## Event logic

```text
Sensor anomaly
   +
Neighbour sensor agreement
   +
Temporal persistence
   +
Spatial coherence
        |
        v
Pollution Event
```

## Event fields

```text
event_id
start_time
end_time
grid_id
pollutant
peak_value
baseline_value
severity
```

---

# 30. Spatial coherence

## What is it?

Nearby sensors showing related behaviour.

Example:

```text
Sensor A ↑
Sensor B ↑
Sensor C ↑
Sensor D normal
```

This may indicate a localized plume.

By contrast:

```text
Only Sensor A ↑
others normal
```

may indicate a sensor fault.

## Algorithms

- spatial correlation
- Moran's I
- local spatial autocorrelation
- neighbour agreement score
- graph-based smoothing

## Advanced

Graph neural networks.

---

# 31. Graphs and graph neural networks

## What is a graph?

Nodes:

```text
sensor
grid
road
source
```

Edges:

```text
nearby
connected by road
upwind/downwind
potential plume influence
```

## Why use graphs?

Cities are naturally networked.

Example:

```text
Sensor A ---- Sensor B
   |              |
 Road R1       Road R2
```

## Graph Neural Network (GNN)

A GNN learns from node features plus graph relationships.

Possible applications:

- pollution field estimation
- spatiotemporal forecasting
- sensor relationships

## Algorithms

- GCN
- GraphSAGE
- GAT
- temporal GNN

## MVP?

No.

## Research extension?

Yes.

---

# 32. Candidate source generation

## What is it?

Creating a shortlist of plausible sources for an event.

## Why?

Suppose the city has 10,000 mapped source entities.

It is inefficient to evaluate all 10,000 equally.

## Process

```text
Event
 |
 +-- spatial filter
 +-- wind filter
 +-- time filter
 +-- source-type filter
 +-- activity filter
 |
 v
candidate sources
```

## Data in

- event location
- event time
- wind
- source inventory

## Data out

```text
candidate_sources
```

---

# 33. Source inventory

## What is it?

A structured registry of known emission sources.

Examples:

```text
roads
construction sites
industries
waste facilities
landfills
burning locations
```

## Why use it?

Attribution cannot identify sources that the system does not know about.

---

# 34. Source taxonomy

The system should start with:

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

Why have `unknown`?

Because forcing every event into a known class creates false certainty.

---

# 35. Pollutant signatures

## What are they?

Characteristic combinations of pollutant changes and contextual variables.

Example:

```text
Traffic:
NO2 ↑
CO ↑
PM2.5 ↑
traffic_index ↑
```

Construction:

```text
PM10 ↑↑
dryness ↑
construction_active = 1
```

Burning:

```text
PM2.5 ↑↑
CO ↑
fire evidence
```

Industrial:

```text
SO2/NO2/CO pattern
+
industrial activity
```

## Important

A signature is probabilistic evidence, not a fixed rule.

---

# 36. Feature engineering for source attribution

## Raw features

```text
pm25
pm10
no2
co
traffic_index
wind_direction
wind_speed
```

## Derived features

```text
pm10_spike_ratio
pm25_spike_ratio
no2_to_pm25_ratio
source_distance
wind_alignment
construction_active
industry_active
fire_distance
fire_confidence
citizen_report_count
```

## Why this matters

The derived features expose relationships that raw values alone do not express.

---

# 37. Ratios and pollutant relationships

Ratios can sometimes provide useful source-pattern information.

Examples:

```text
NO2 / PM2.5
CO / PM2.5
PM10 / PM2.5
```

## Caution

Ratios can become unstable near zero and can amplify sensor noise.

Use them carefully and include quality checks.

---

# 38. Classification models for source attribution

## Option 1 — Logistic Regression

### What it is

A linear probabilistic classifier.

### Benefits

- simple
- interpretable
- fast
- good baseline

### Weakness

Limited nonlinear behavior.

---

## Option 2 — Decision Tree

### Benefits

Easy to explain.

### Weakness

Can overfit.

---

## Option 3 — Random Forest

### Benefits

- nonlinear
- robust
- strong baseline
- feature importance

### Weakness

Large ensembles may be less compact.

---

## Option 4 — XGBoost

### Benefits

- excellent for tabular data
- handles nonlinear interactions
- often strong performance
- supports probability prediction
- works well with structured environmental features

### Weakness

Needs tuning.

---

## Option 5 — SVM

Good for some medium-sized datasets.

Less convenient with very large streaming data and probability outputs.

---

## Option 6 — Neural network / MLP

Useful if you have enough labeled data.

Harder to explain.

---

## Option 7 — Graph neural network

Useful when spatial relationships are central.

More complex.

## Recommendation

MVP:

```text
Logistic Regression baseline
+
XGBoost final model
```

---

# 39. Multi-class vs multi-label source attribution

This is a crucial design decision.

## Multi-class

Exactly one class:

```text
traffic
OR
construction
OR
burning
```

Problem:

Real events can have multiple sources.

## Multi-label

Multiple source classes can be active simultaneously:

```text
traffic = yes
road_dust = yes
construction = yes
```

This better reflects reality.

## Alternative: mixture/contribution model

Output:

```text
Traffic = 40%
Construction = 30%
Road dust = 20%
Other = 10%
```

## Recommendation

Use:

```text
probabilities over source categories
+
contribution estimates
```

rather than forcing exactly one source.

---

# 40. Evidence fusion

## What is it?

Combining evidence from multiple independent or partially independent sources.

Possible evidence:

```text
sensor
weather
wind
traffic
construction
industry
satellite
fire
citizen report
historical pattern
```

## Simple weighted fusion

```text
Score =
w1 * wind
+
w2 * signature
+
w3 * activity
+
w4 * distance
+
w5 * traffic
+
w6 * satellite
+
w7 * citizen
```

## Alternative algorithms

### Bayesian inference

```text
P(source | evidence)
```

### Logistic regression

Learn source probability from features.

### XGBoost

Learn nonlinear interactions.

### Dempster-Shafer

Useful for combining uncertain evidence, but more complex.

### Ensemble averaging

Combine multiple models.

## MVP

XGBoost + explicit physical evidence.

---

# 41. Bayesian inference

## What is it?

Bayesian reasoning updates belief about a hypothesis given evidence.

Concept:

```text
P(Source | Evidence)
```

can be thought of as:

```text
prior belief
×
evidence compatibility
```

## Why useful?

It naturally represents uncertainty.

## Example

Prior:

```text
traffic = 30%
construction = 25%
```

Evidence:

```text
PM10 spike
+
active construction
+
strong upwind alignment
```

Posterior:

```text
construction = 64%
```

## MVP?

A full Bayesian network is optional.

Use Bayesian concepts when designing probability and evidence fusion.

---

# 42. Ensemble learning

## What is it?

Combining multiple models.

Example:

```text
XGBoost
+
Logistic Regression
+
physics score
        |
        v
final attribution
```

## Why?

Different models capture different structures.

## Advanced option

Stacking or weighted ensemble.

---

# 43. Probability calibration

## What is it?

Turning model scores into more trustworthy probabilities.

## Why important?

If model says:

```text
construction = 0.90
```

that value should mean something meaningful.

## Algorithms

- Platt scaling
- isotonic regression
- temperature scaling for neural networks

## Evaluation

- reliability diagrams
- Brier score
- expected calibration error

---

# 44. Source contribution estimation

## What is it?

Estimating how much of the observed pollution excess is associated with each source.

Example:

```text
Observed excess PM2.5 = 100

traffic      42
construction 28
burning      15
background   15
```

## Important distinction

```text
probability:
How likely is the source involved?

contribution:
How much does the model estimate it explains?
```

These should not be conflated.

## Algorithms/approaches

- nonnegative regression
- constrained optimization
- Bayesian source apportionment
- PMF
- CMB
- inverse dispersion
- neural mixture models

---

# 45. Positive Matrix Factorization (PMF)

## What is it?

A receptor-modeling technique that decomposes observed pollutant mixtures into latent source factors.

Conceptually:

```text
Observed pollutant matrix
        |
        v
PMF
        |
        +-- Factor 1
        +-- Factor 2
        +-- Factor 3
```

The factors can be interpreted as source profiles when enough chemical/speciation data exists.

## Why useful?

It is a classic source-apportionment methodology.

## Limitation

Needs appropriate chemical measurements and source-profile interpretation.

## MVP?

No, unless the team has suitable speciation data.

## Research extension?

Very valuable as a validation/comparison method.

---

# 46. Chemical Mass Balance (CMB)

## What is it?

A receptor-model approach using known source profiles to estimate contributions.

Conceptually:

```text
ambient composition
+
known source profiles
        |
        v
CMB
        |
        v
source contributions
```

## Difference from PMF

PMF can derive latent factors from ambient observations.

CMB relies more directly on known source profiles.

## MVP?

Usually no.

## Advanced research?

Yes, especially where chemical-speciation data is available.

---

# 47. Receptor model vs dispersion model

## Receptor model

Starts from measurements at the receptor and asks:

```text
what combination of sources explains the measured composition?
```

Examples:

- PMF
- CMB

## Dispersion model

Starts from sources and asks:

```text
where would emissions travel?
```

Examples:

- Gaussian plume
- HYSPLIT
- FLEXPART

## Why combine them?

They answer complementary questions.

```text
Dispersion:
Can source X physically affect this sensor?

Receptor model:
Does the observed chemical mixture look like a mixture of sources?
```

---

# 48. Source attribution confidence

## What is it?

An estimate of how reliable the source-attribution conclusion is.

## Possible components

```text
sensor quality
+
number of agreeing sensors
+
wind quality
+
source activity evidence
+
pollutant-signature match
+
satellite evidence
+
citizen evidence
+
model certainty
```

## Example

```text
Source category:
construction = 0.72 probability

Confidence:
0.86
```

---

# 49. Unresolved/unknown source

## Why this is essential

A robust system must be allowed to say:

```text
unknown
```

or:

```text
unresolved
```

If evidence is weak, uncertainty should increase rather than the model inventing certainty.

---

# 50. Forecasting

## What is it?

Predicting future pollution or exposure.

## Why use it?

A warning is more useful if it can say:

```text
pollution expected to remain elevated for the next 60 minutes
```

## Inputs

```text
current pollution
weather
wind
traffic
source activity
historical patterns
```

---

# 51. Forecasting alternatives

## Statistical

- ARIMA
- SARIMA
- exponential smoothing
- Prophet-style decomposition

Good for strong time patterns.

## ML

- Random Forest
- XGBoost
- LightGBM

Good for feature-rich data.

## Deep learning

- LSTM
- GRU
- Temporal CNN
- Transformer
- Temporal Fusion Transformer

Good for complex sequential relationships but needs more data and engineering.

## Spatial-temporal

- ConvLSTM
- spatiotemporal GNN
- graph transformers

Research-level complexity.

## Recommendation

MVP:

```text
XGBoost forecasting
or
simple time-series baseline
```

Advanced:

```text
LSTM/Transformer/GNN
```

---

# 52. Exposure modeling

## What is it?

Estimating how many people may experience elevated pollution in a location for a period of time.

## Conceptual formula

```text
Exposure indicator
≈
concentration
×
duration
×
population
```

A more advanced model can include:

```text
activity patterns
vulnerability
building characteristics
outdoor time
```

## Data in

```text
pollution grid
population
duration
sensitive locations
```

## Data out

```text
exposure score
population exposed
risk category
```

---

# 53. Population weighting

Why?

Two neighbourhoods with identical pollution may have very different impacts.

```text
Grid A:
PM2.5 = 150
Population = 2,000

Grid B:
PM2.5 = 150
Population = 20,000
```

Grid B has much greater population exposure.

---

# 54. Sensitive-location analysis

Relevant locations:

- schools
- hospitals
- care facilities
- dense residential areas
- transit areas
- outdoor markets

## GIS process

```text
pollution plume polygon
      +
school points
      |
      v
spatial intersection
      |
      v
affected schools
```

---

# 55. Alert generation

## What is it?

Converting pollution/exposure states into human-readable warnings.

## Levels

Example:

```text
Normal
Watch
Warning
High
Critical
```

These categories should be defined consistently with the project's chosen communication policy and relevant official guidance.

## Alert inputs

```text
pollution level
trend
exposure
forecast
source confidence
duration
```

---

# 56. Recommendation system

## What is it?

A decision-support module that proposes actions.

## Why use it?

The objective is not merely prediction.

The system should support response.

## Example rules

```text
IF traffic probability > threshold
AND congestion > threshold
THEN traffic management
```

```text
IF construction probability > threshold
AND PM10 high
THEN construction inspection
```

## Approaches

### Rule-based

Best MVP.

### Optimization

Select the action maximizing estimated benefit.

### Reinforcement learning

Potential future research but not recommended for the first project.

---

# 57. Optimization

## What is it?

Finding the best action according to an objective.

Possible objective:

```text
maximize exposure reduction
while minimizing:
traffic disruption
cost
operational effort
```

Conceptually:

```text
Utility(action)
=
expected pollution reduction
-
cost
-
traffic disruption
-
uncertainty penalty
```

## MVP

Rule-based ranking.

## Advanced

Constrained optimization / mixed-integer optimization.

---

# 58. Counterfactual reasoning

## What is it?

Asking:

> What might happen if a different action were taken?

Example:

```text
Current:
road congestion = high

Action A:
signal optimization

Action B:
vehicle diversion

Action C:
heavy-vehicle restriction
```

Model estimates effect for each.

## Why useful?

Turns the project from:

```text
diagnosis
```

into:

```text
decision support
```

## MVP?

Optional.

---

# 59. Reinforcement learning

## What is it?

An agent learns actions through reward and feedback.

Potential application:

```text
Traffic management
```

where the system chooses signal or routing policies.

## Why not MVP?

Needs:

- reliable environment
- action simulator
- reward design
- safety controls
- large training experience

Use only as a future extension.

---

# 60. Computer vision

## What is it?

Using image/video data to classify visual conditions.

Potential classes:

```text
smoke
fire
dust
construction
uncovered truck
```

## Why use it?

Citizen reports can include images.

## Algorithms

### Classical

- HOG
- SVM
- color/texture features

### CNN

- ResNet
- EfficientNet

### Object detection

- YOLO
- Faster R-CNN

### Vision transformers

- ViT
- DETR

## MVP

Manual category + metadata.

## Advanced

YOLO or another object detector.

---

# 61. Natural language processing

## Why potentially useful?

Citizen reports may be text:

```text
"heavy smoke coming from the garbage area"
```

NLP can classify:

```text
burning
dust
industry
odour
```

## Techniques

### Simple

Keyword/rule-based.

### Classical ML

TF-IDF + logistic regression.

### Transformer

BERT-style classifier.

## Recommendation

Use simple text classification first.

---

# 62. Multimodal learning

## What is it?

Learning from multiple types of data simultaneously.

This project is inherently multimodal:

```text
numerical sensor data
+
weather
+
spatial
+
traffic
+
satellite imagery
+
citizen text/image
```

## Possible architectures

### Early fusion

Combine all features before the model.

```text
all features
   |
   v
single model
```

### Late fusion

Each modality gets its own model.

```text
sensor model
weather model
image model
traffic model
   |
   v
fusion
```

### Hybrid fusion

Some modalities are fused early and others later.

## Recommendation

Start with structured feature fusion.

Advanced:

late/hybrid multimodal fusion.

---

# 63. Attention

## What is it?

A mechanism that allows a model to focus more on important inputs.

Possible advanced use:

```text
which sensors matter most?
which time steps matter most?
```

Useful in:

- transformers
- attention-based GNNs
- multimodal models

Not essential for MVP.

---

# 64. Transformers

## What are they?

Neural architectures using attention to model relationships across sequences.

## Potential uses

- pollution forecasting
- long temporal dependencies
- multimodal fusion
- satellite/time-series analysis

## Why not start here?

They need:

- more data
- more compute
- careful validation

Use as an advanced extension.

---

# 65. LSTM

## What is it?

A recurrent neural network designed for sequential data.

## Why useful?

Pollution has temporal dependence.

```text
previous hours
      |
      v
LSTM
      |
      v
future pollution
```

## Alternative

GRU is simpler and often similar.

---

# 66. XGBoost

## What is it?

A gradient-boosted tree ensemble.

## Why it is a good choice here

Your features are mostly structured:

```text
PM values
weather
traffic
distance
wind alignment
activity flags
fire metrics
```

XGBoost can model nonlinear interactions without requiring enormous datasets.

## Main uses

- source classification
- pollution forecasting
- baseline estimation
- source scoring

---

# 67. Random Forest

## Why keep it as an alternative?

It is:

- robust
- easy to train
- easy to compare against
- relatively easy to explain

A useful benchmark for XGBoost.

---

# 68. Logistic Regression

## Why use it?

It is an excellent simple baseline.

Suppose:

```text
features -> linear boundary -> source probability
```

If XGBoost only slightly improves over logistic regression, the simpler model may be preferable.

---

# 69. Model comparison

Do not select a model only because it has the highest training accuracy.

Compare:

```text
Logistic Regression
Random Forest
XGBoost
```

using:

- validation accuracy
- macro F1
- per-class precision/recall
- probability calibration
- inference speed
- interpretability

---

# 70. Cross-validation for time-series

Randomly shuffling time-series data can cause leakage.

Use:

- walk-forward validation
- expanding-window validation
- blocked time-series split

Example:

```text
Train: Jan-Mar
Test:  Apr

Train: Jan-Apr
Test:  May

Train: Jan-May
Test:  Jun
```

---

# 71. Class imbalance

Suppose your dataset has:

```text
traffic events = 1000
construction = 100
industrial = 40
burning = 20
```

A naive model may mostly learn traffic.

## Solutions

- class weights
- oversampling
- undersampling
- SMOTE
- focal loss for neural models

## Recommendation

Start with class weights and careful evaluation.

---

# 72. SMOTE

## What is it?

Synthetic Minority Over-sampling Technique.

It creates synthetic examples for underrepresented classes.

## Why potentially useful?

Rare source categories may have few labels.

## Caution

Do not blindly apply SMOTE to time-series or spatial data because it can create unrealistic observations.

---

# 73. Data augmentation

Possible for images:

- flips
- crops
- brightness changes
- noise

For sensor time-series, augmentation must be physically plausible.

Examples:

- small measurement noise
- time shifts
- simulated source events

Do not create impossible environmental conditions.

---

# 74. Synthetic data generation

## Why needed?

Exact source labels are expensive.

You can generate scenarios:

```text
traffic event
construction event
fire event
industrial event
regional event
```

## Approaches

### Rule-based simulation

Simple and transparent.

### Physics-based simulation

Use plume/trajectory models.

### Generative models

GANs/diffusion models.

## Recommendation

Rule + physics-based synthetic events.

---

# 75. Ground truth

## What is it?

Trusted information about the true source/event.

Examples:

- field inspection
- verified burning event
- confirmed construction violation
- traffic closure
- industrial shutdown
- mobile sensor investigation

## Why important?

AI accuracy cannot be meaningfully measured without labels.

---

# 76. Weak supervision

## What is it?

Using imperfect rules or noisy sources to create training labels.

Example:

```text
active construction
+
strong PM10 spike
+
upwind alignment
```

might create a weak construction label.

Useful when expert labels are scarce.

---

# 77. Active learning

## What is it?

The model identifies uncertain cases for human labeling.

Example:

```text
Prediction:
construction 51%
traffic 43%

Confidence low
      |
      v
Request field verification
```

This can make data collection much more efficient.

---

# 78. Human-in-the-loop

The final system should include human review.

```text
AI
 |
 v
Probable source
 |
 v
Human officer
 |
 +-- confirm
 +-- reject
 +-- alternative source
 |
 v
verified record
 |
 v
future training data
```

This is valuable for both safety and continual improvement.

---

# 79. Explainable AI

## Why?

Government users need to understand why the system made a recommendation.

The dashboard should show:

```text
Construction = 64%

Supporting evidence:
+ strong PM10 increase
+ active permit
+ upwind location
+ dry conditions
+ sensor agreement
```

---

# 80. SHAP

## What is it?

SHAP estimates how individual features contributed to a model prediction.

## Example

```text
Prediction: construction

PM10 spike            ++++++
Upwind construction   +++++
Dryness               ++++
Distance              +++
Traffic                --
NO2                    --
```

## Why useful?

It provides model-level explanation for structured ML models.

## MVP?

Yes, if XGBoost is used.

---

# 81. Feature importance

Simpler model explanation.

Methods:

- gain
- split importance
- permutation importance

Permutation importance is often more informative than raw tree frequency but can be affected by correlated features.

---

# 82. Calibration curve

A calibration curve compares:

```text
predicted probability
vs
observed frequency
```

Useful for source probabilities.

---

# 83. Brier score

Measures quality of probabilistic predictions.

Lower is better.

Useful when probability quality matters, which it does for attribution.

---

# 84. Precision

```text
precision
=
correct positive predictions
/
all positive predictions
```

For this project:

> When the model says "industrial", how often is that reasonable/correct in validated data?

---

# 85. Recall

```text
recall
=
correct positive predictions
/
all actual positives
```

Important for ensuring real events are not missed.

---

# 86. F1 score

Harmonic mean of precision and recall.

Useful when classes are imbalanced.

---

# 87. ROC-AUC

Useful for binary/multiclass ranking performance, but should not replace per-class precision/recall in an imbalanced source-attribution problem.

---

# 88. PR-AUC

Precision-recall area under curve.

Often more informative than ROC-AUC for rare classes.

---

# 89. Confusion matrix

Shows which source types the model confuses.

Example:

```text
                 Predicted
             traffic construction burning

Actual traffic       90      8        2
Actual construction   9     84        7
Actual burning        2      5       93
```

---

# 90. Spatial interpolation

## What is it?

Estimating pollution between sensors.

## Why needed?

Sensors are not everywhere.

## Algorithms

### Nearest neighbor

Simple but discontinuous.

### Inverse Distance Weighting (IDW)

Nearby sensors contribute more.

### Kriging

Uses spatial covariance.

### Gaussian Process

Probabilistic spatial modeling.

### ML interpolation

Uses environmental features.

### Graph neural network

Advanced spatiotemporal estimation.

## Recommendation

MVP:

```text
IDW or ordinary kriging
```

Advanced:

spatiotemporal ML/GNN.

---

# 91. Kriging

## What is it?

A geostatistical interpolation method.

## Why useful?

It models spatial correlation and can provide uncertainty.

## Key concept

Nearby observations influence the estimated value, but influence depends on spatial covariance.

## Outputs

```text
estimated concentration
+
estimation variance
```

That uncertainty is useful.

---

# 92. IDW

## What is it?

Inverse Distance Weighting.

Concept:

```text
closer sensor = larger weight
```

Simple formula concept:

```text
weight_i ∝ 1 / distance_i^p
```

## Advantages

- easy
- fast
- intuitive

## Weakness

Does not model directional spatial structure as well as kriging.

---

# 93. Pollution heatmap

## What is it?

A spatial representation of predicted pollution.

```text
low  -> high
```

## Inputs

```text
sensor measurements
weather
road context
land use
```

## Output

```text
pollution estimate per grid
```

---

# 94. Spatial-temporal forecasting

This combines:

```text
space + time
```

Example:

```text
G1 at 10:00
G2 at 10:00
G3 at 10:00
...
```

and predicts:

```text
G1 at 10:30
G2 at 10:30
...
```

Advanced algorithms:

- ConvLSTM
- Temporal GNN
- graph transformers
- spatiotemporal Gaussian processes

---

# 95. Data normalization/scaling

## What is it?

Making numerical features comparable.

Methods:

### Standardization

```text
(x - mean) / std
```

### Min-max scaling

Map to 0–1.

### Robust scaling

Uses median and IQR.

## Do tree models require scaling?

Usually not.

## Do linear/SVM/neural models benefit?

Often yes.

---

# 96. One-hot encoding

Converts categories into binary variables.

Example:

```text
industry_type:
cement

becomes:
industry_cement = 1
```

Useful for classical ML.

---

# 97. Target encoding

Converts categories to statistics.

Can be powerful but risks leakage.

Not necessary for MVP.

---

# 98. Feature selection

## Why?

Too many irrelevant features can hurt models.

Methods:

- correlation filtering
- mutual information
- recursive feature elimination
- L1 regularization
- tree-based importance

For the project, domain-driven feature engineering plus model-based importance is a good balance.

---

# 99. Multicollinearity

Two features may contain nearly the same information.

Example:

```text
traffic_index
vehicle_density
average_speed
```

may be highly correlated.

This can affect linear models more strongly.

---

# 100. Database concepts

## Relational database

Stores structured records in tables.

## PostgreSQL

Recommended primary database.

## PostGIS

Adds geospatial support.

---

# 101. Time-series database

Useful for large sensor histories.

Examples:

- TimescaleDB
- InfluxDB

For a student project, PostgreSQL + TimescaleDB or PostgreSQL with suitable indexes is sufficient.

---

# 102. Indexes

## What are they?

Structures that speed queries.

Important indexes:

```text
timestamp
sensor_id
grid_id
source_type
geospatial geometry
event_id
```

PostGIS spatial indexes are particularly important.

---

# 103. Geospatial queries

Examples:

```text
sources within 2 km
```

```text
schools inside plume
```

```text
sensors within grid
```

```text
roads intersecting affected area
```

PostGIS is ideal for these.

---

# 104. REST API

## What is it?

HTTP-based service interface.

Example:

```http
GET /api/v1/pollution/current
```

## Why use it?

Frontend and ML services should not directly depend on database internals.

---

# 105. WebSocket

## What is it?

Persistent two-way connection.

## Why use it?

Push real-time events to dashboard.

Example:

```text
server
  |
  | NEW_EVENT
  v
React dashboard
```

---

# 106. FastAPI

## What is it?

Python framework for APIs.

## Why recommended?

- integrates easily with Python ML
- type validation
- automatic API documentation
- good performance
- easy development

---

# 107. React

## What is it?

Frontend library for interactive UI.

## Why use it?

Useful for:

- dashboards
- map views
- alerts
- source-analysis screens

---

# 108. TypeScript

## What is it?

Typed JavaScript.

## Why useful?

It reduces frontend integration errors.

For example:

```typescript
interface AttributionResult {
    event_id: string;
    confidence: number;
    primary_source_type: string;
}
```

---

# 109. Leaflet

Useful for interactive 2D maps.

Use it for:

```text
sensor points
hotspots
sources
roads
construction
fire points
```

---

# 110. MapLibre

Alternative to Leaflet.

Better suited to advanced vector-map styling.

Choose one for the project rather than implementing both.

---

# 111. Recharts

Charting library for React.

Use for:

```text
PM2.5 trend
PM10 trend
source contribution
forecast
exposure
```

---

# 112. MQTT

## What is it?

Lightweight publish/subscribe messaging.

## Why use it?

Good for low-bandwidth IoT sensor communication.

Example:

```text
air/sensors/S001
```

---

# 113. Kafka

## What is it?

Distributed event-streaming platform.

## Why consider it?

Large-scale event pipelines.

## Why not MVP?

Operational complexity is unnecessary for a small team unless the project has very high event volume.

---

# 114. Redis

Useful for:

- caching
- temporary results
- rate limits
- sessions
- real-time state

Optional.

---

# 115. Docker

## What is it?

Containerization technology.

## Why use it?

Same environment on all three team members' systems.

Example:

```text
Docker
 |
 +-- PostgreSQL
 +-- backend
 +-- frontend
 +-- MQTT
```

This is especially helpful for your integration problem.

---

# 116. Git

## What is it?

Version control.

## Why use it?

Three developers need controlled collaboration.

---

# 117. GitHub

Use for:

- repository
- branches
- pull requests
- issues
- reviews
- CI

---

# 118. Branch strategy

```text
main
  |
  └── develop
       |
       +-- feature/person1-data
       +-- feature/person2-ai
       +-- feature/person3-app
```

---

# 119. CI/CD

## What is it?

Automated building/testing/deployment.

## MVP

GitHub Actions:

```text
push
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

---

# 120. Testing levels

## Unit test

One function.

```text
calculate_distance_km()
```

## Integration test

Several modules.

```text
database -> attribution service
```

## End-to-end

Whole system.

```text
sensor -> AI -> API -> dashboard
```

---

# 121. Reproducibility

A research project should be reproducible.

Record:

```text
data version
model version
feature version
code commit
configuration
training parameters
```

---

# 122. MLOps

## What is it?

Operational lifecycle for ML.

```text
data
 -> training
 -> evaluation
 -> registry
 -> deployment
 -> monitoring
 -> retraining
```

## Why needed?

A model can degrade after deployment.

---

# 123. Model registry

Store:

```text
model name
version
training dataset
features
metrics
date
status
```

Example:

```text
attribution_v1
attribution_v2
```

---

# 124. Data drift

Input data distribution changes.

Example:

```text
training traffic:
mostly 0.2–0.7

production traffic:
mostly 0.7–1.0
```

Monitor this.

---

# 125. Model drift

Performance changes over time.

Could happen because:

- source patterns change
- sensor characteristics change
- seasons change
- road patterns change

---

# 126. Model monitoring

Monitor:

```text
prediction distribution
confidence distribution
missing features
latency
accuracy when labels arrive
```

---

# 127. Data lineage

## What is it?

Knowing where every value came from.

Example:

```text
AttributionResult
   |
   +-- model version
   +-- feature version
   +-- sensor observations
   +-- weather observation
   +-- source inventory
```

Important for debugging and auditability.

---

# 128. Schema versioning

Data schemas should have versions.

Example:

```text
schema_version = 1
```

If fields change:

```text
schema_version = 2
```

---

# 129. API versioning

Use:

```text
/api/v1/
```

This gives room for future versions.

---

# 130. Security basics

## Authentication

Who are you?

## Authorization

What are you allowed to access?

## Encryption

Protect data in transit and at rest.

## Secrets

Store API keys in environment variables/secret managers.

Never commit them to Git.

---

# 131. Privacy

Traffic should preferably use:

```text
aggregate road-level data
```

rather than individual person trajectories.

Citizen images should be protected.

Sensitive personal information should not be necessary for the core project.

---

# 132. Responsible AI

The model should not produce:

```text
Company X is guilty.
```

Instead:

```text
Facility X is a high-probability candidate
with medium confidence.
Human verification recommended.
```

This distinction is important.

---

# 133. Safety architecture

The system should be allowed to output:

```text
do not act yet
```

when evidence is weak.

This is safer than forced predictions.

---

# 134. Source attribution as a ranking problem

Another way to formulate the problem is:

```text
Given event E,
rank candidate sources S1...Sn.
```

Example:

```text
1. construction_site_7841
2. road_R118
3. factory_F04
4. waste_site_W10
```

Each gets a score.

This can be useful even before final source classification.

---

# 135. Learning-to-rank

Advanced ML approach for candidate-source ranking.

Input:

```text
candidate source
+
event features
```

Output:

```text
candidate relevance score
```

Algorithms:

- LambdaMART
- XGBoost ranking
- pairwise ranking

Not necessary for MVP.

---

# 136. Source localization

## What is it?

Finding the likely geographic location of an unknown source.

Possible approaches:

- wind backtracking
- inverse dispersion
- Bayesian optimization
- grid search
- differentiable physics
- neural inverse models

## MVP

Use known source inventory + upwind geometry.

---

# 137. Inverse problem

This is a major scientific concept behind the project.

## Forward problem

```text
source
+
weather
=
pollution at sensors
```

## Inverse problem

```text
pollution at sensors
+
weather
=
infer source
```

Our source-attribution problem is therefore an **inverse environmental modeling problem**.

---

# 138. Bayesian inverse modeling

Advanced formulation:

```text
observed sensor data
        |
        v
prior source assumptions
        +
dispersion model
        |
        v
posterior source distribution
```

This can provide uncertainty but is computationally heavier.

---

# 139. Sensor network design

## What is it?

Choosing where sensors should be placed.

## Why important?

Poor sensor placement weakens attribution.

## Possible objectives

Maximize:

- spatial coverage
- source distinguishability
- population coverage
- plume observability

## Advanced methods

- coverage optimization
- entropy reduction
- Bayesian experimental design
- facility-location optimization

## MVP

Manually place sensors around:

```text
traffic
construction
industry
residential background
```

---

# 140. Background pollution

## What is it?

Pollution not attributed to the local candidate sources.

It may include:

- regional transport
- secondary formation
- distant sources
- persistent background

Always keep:

```text
background
unknown
```

as valid model categories.

---

# 141. Regional transport

## What is it?

Pollution transported from outside the local area.

## Why important?

A city can be polluted even when local sources are not unusually active.

## Evidence

```text
many sensors elevated
+
strong regional wind
+
satellite aerosol pattern
+
no strong local candidate
```

---

# 142. Secondary pollution

## What is it?

Pollution formed in the atmosphere from precursor chemicals.

Examples include ozone and secondary particulate matter.

## Why difficult?

The source may be geographically far from the final observed pollutant.

This is one reason the system must support:

```text
regional_transport
```

and:

```text
unknown/background
```

rather than only local primary sources.

---

# 143. Satellite-ground data fusion

Satellite provides broad spatial context.

Ground sensors provide local surface observations.

Possible fusion:

```text
ground PM
+
satellite aerosol
+
weather
+
land use
```

into a pollution field model.

## Algorithms

- regression
- random forest
- XGBoost
- Gaussian process
- deep spatiotemporal model

---

# 144. Satellite quality flags

Satellite observations have quality metadata.

Do not use every pixel equally.

Check:

```text
cloud screening
retrieval quality
validity flags
coverage
```

Low-quality observations should reduce evidence rather than being treated as ground truth.

---

# 145. Construction activity inference

Construction status can come from:

```text
permit
+
schedule
+
manual verification
+
citizen report
+
satellite imagery
```

Advanced computer vision could detect:

- exposed soil
- demolition
- heavy equipment
- construction expansion

---

# 146. Industrial operating state

A factory existing near a sensor does not prove it emitted during an event.

Useful features:

```text
operating schedule
shutdown
maintenance
production status
stack status
```

This is an example of **temporal source activity**.

---

# 147. Fire hotspot evidence

Fire datasets provide:

```text
location
time
confidence
thermal intensity
```

## Why useful?

A local PM2.5/CO event with an upwind fire hotspot becomes a much stronger burning candidate.

---

# 148. Citizen evidence integration

Citizen reports should become:

```text
evidence_score
```

not:

```text
ground truth
```

Possible pipeline:

```text
report
 |
 +-- location validation
 +-- time validation
 +-- duplicate detection
 +-- optional image/text analysis
 +-- sensor agreement
 |
 v
credibility score
```

---

# 149. Knowledge graph

## What is it?

A graph storing entities and their relationships.

Example:

```text
Construction Site
     |
     +-- has permit
     +-- located in grid G42
     +-- active at 10:15
     +-- upwind of Sensor S04
```

## Why useful?

It can connect otherwise separate data sources.

## MVP?

PostGIS tables are enough.

## Advanced?

Neo4j or graph-based representations.

---

# 150. Rules engine vs ML

A strong design uses both.

## ML

Best for:

```text
complex pattern recognition
probability estimation
forecasting
```

## Rules

Best for:

```text
hard constraints
safety
legal/operational policy
```

Example:

```text
ML:
construction probability = 0.72

Rule:
if confidence < 0.6, do not create enforcement recommendation

Result:
monitor only
```

---

# 151. Hybrid AI

The project is best thought of as:

```text
Machine Learning
+
Physics
+
GIS
+
Rules
+
Human verification
```

This is more defensible than a pure black-box neural network.

---

# 152. Recommended algorithm stack

## MVP

```text
Sensor calibration:
Linear regression / polynomial regression

Baseline:
Historical median + rolling statistics

Anomaly:
Robust z-score / CUSUM + Isolation Forest

Spatial interpolation:
IDW or Kriging

Candidate source:
GIS + wind backtracking

Source attribution:
Logistic Regression baseline + XGBoost

Evidence fusion:
Weighted evidence + ML probability

Contribution:
Nonnegative constrained estimation

Confidence:
Calibrated probability + data quality

Forecast:
XGBoost or time-series baseline

Exposure:
Spatial aggregation

Recommendations:
Rule-based ranking
```

---

# 153. Advanced algorithm stack

```text
Sensor calibration:
XGBoost / domain adaptation

Event detection:
Bayesian change-point + temporal neural model

Pollution field:
Spatiotemporal GNN

Candidate-source localization:
Inverse dispersion

Attribution:
XGBoost ensemble + Bayesian fusion

Source apportionment:
PMF / CMB

Transport:
HYSPLIT / FLEXPART

Forecast:
Temporal Transformer / GNN

Citizen images:
YOLO / vision transformer

Citizen text:
BERT-style classifier

Action:
Optimization / simulation

Continuous learning:
Active learning + human-in-the-loop
```

---

# 154. What each person should learn

## Person 1 — Data/GIS

### Core

```text
Python
Pandas
NumPy
REST APIs
JSON
PostgreSQL
SQL
PostGIS
GeoPandas
Shapely
MQTT
Docker
```

### Concepts

```text
ETL
ELT
data validation
time-series storage
coordinate systems
spatial joins
geospatial indexing
sensor calibration
sensor drift
```

---

## Person 2 — AI/ML

### Core

```text
Python
NumPy
Pandas
Scikit-learn
XGBoost
SciPy
SHAP
Matplotlib
```

### Concepts

```text
supervised learning
unsupervised learning
classification
regression
anomaly detection
feature engineering
time-series
probability
calibration
uncertainty
cross-validation
class imbalance
explainability
source apportionment
inverse problems
```

### Advanced

```text
PyTorch
GNN
Transformers
Bayesian modeling
PMF
dispersion modeling
```

---

## Person 3 — Application

### Core

```text
FastAPI
Pydantic
React
TypeScript
Leaflet / MapLibre
Recharts
WebSockets
Docker
```

### Concepts

```text
REST
API versioning
authentication
authorization
state management
component architecture
real-time updates
GIS visualization
```

### Advanced

```text
WebSockets
role-based access
notification infrastructure
offline-first mobile reporting
```

---

# 155. Complete AI pipeline

```text
RAW DATA
    |
    v
Preprocessing
    |
    v
Feature Engineering
    |
    v
Baseline
    |
    v
Anomaly Detection
    |
    v
Pollution Event
    |
    v
Candidate Source Generation
    |
    v
Physics / Wind Evidence
    |
    v
ML Prediction
    |
    v
Evidence Fusion
    |
    v
Probability Calibration
    |
    v
Source Attribution
    |
    v
Contribution Estimation
    |
    v
Confidence / Uncertainty
    |
    v
Forecast
    |
    v
Exposure
    |
    v
Recommendation
```

---

# 156. Complete data-to-decision example

```text
SENSOR
PM10 = 210
PM2.5 = 130
NO2 = 50
      |
      v
PERSON 1
Quality check
      |
      v
Calibration
      |
      v
Grid G42
      |
      v
PERSON 2
Baseline:
PM10 expected = 95
      |
      v
Anomaly:
PM10 residual = +115
      |
      v
Event detected
      |
      v
Wind:
245 degrees
      |
      v
Candidate sources:
- construction site
- road
- factory
      |
      v
Feature engineering
      |
      v
XGBoost
      |
      v
Probabilities:
Construction = 0.64
Road dust = 0.21
Traffic = 0.09
Industry = 0.03
Unknown = 0.03
      |
      v
Evidence fusion
      |
      v
Confidence = 0.87
      |
      v
PERSON 3
Exposure:
12,400 people
      |
      v
Recommendation:
construction inspection
      |
      v
Dashboard
```

---

# 157. Where each algorithm sits

```text
Sensor data
   |
   +-- validation
   +-- calibration model
   |
   v
Clean data
   |
   +-- spatial interpolation
   |
   v
Pollution field
   |
   +-- baseline model
   |
   v
Expected pollution
   |
   +-- anomaly detection
   +-- change-point detection
   |
   v
Pollution event
   |
   +-- GIS filtering
   +-- wind backtracking
   +-- candidate ranking
   |
   v
Candidate sources
   |
   +-- XGBoost
   +-- pollutant signatures
   +-- dispersion evidence
   +-- satellite evidence
   +-- traffic evidence
   |
   v
Evidence fusion
   |
   +-- probability calibration
   |
   v
Attribution
   |
   +-- contribution estimation
   +-- confidence
   |
   v
Exposure
   |
   +-- recommendation rules
   |
   v
Dashboard
```

---

# 158. What to implement first

## Stage 1

```text
CPCB/OpenAQ
Weather
OpenStreetMap
Synthetic construction/traffic
PostgreSQL/PostGIS
```

## Stage 2

```text
Cleaning
Calibration
Grid
Baseline
Anomaly detection
```

## Stage 3

```text
Wind backtracking
Candidate sources
XGBoost
Attribution
```

## Stage 4

```text
Exposure
Recommendations
Dashboard
```

## Stage 5

```text
Satellite
FIRMS
Citizen reports
Forecasting
```

## Stage 6

```text
Advanced physics
GNN
Transformers
PMF/CMB
Optimization
```

---

# 159. What is essential vs optional

| Component | MVP | Advanced |
|---|---:|---:|
| CPCB/OpenAQ | Yes | - |
| Low-cost sensors | Yes, simulated if needed | More dense network |
| Weather | Yes | Higher-resolution weather |
| Traffic | Yes | Real-time feeds |
| GIS | Yes | 3D/advanced GIS |
| PostGIS | Yes | - |
| Sensor calibration | Yes | Adaptive calibration |
| Baseline | Yes | ML baseline |
| Anomaly detection | Yes | Deep temporal models |
| Wind backtracking | Yes | Full trajectory models |
| XGBoost | Yes | Ensembles |
| SHAP | Yes | Advanced explainability |
| Source contribution | Yes | PMF/CMB/inverse modeling |
| Sentinel-5P | Useful | Advanced fusion |
| FIRMS | Useful | Automated fire analysis |
| Citizen reports | Useful | CV/NLP analysis |
| Forecasting | Basic | Transformer/GNN |
| Exposure | Yes | Dynamic activity modeling |
| Recommendations | Rule-based | Optimization/RL |
| Web dashboard | Yes | Advanced control center |
| Kafka | No | Large-scale deployment |
| Kubernetes | No | Production scale |

---

# 160. Recommended project stack summary

```text
LANGUAGES
Python
TypeScript
SQL

DATA
CPCB
OpenAQ
Open-Meteo
ERA5
OpenStreetMap
Sentinel-5P
NASA FIRMS
Municipal datasets
Traffic data
Citizen reports

DATA ENGINEERING
Pandas
NumPy
GeoPandas
SciPy
MQTT

DATABASE
PostgreSQL
PostGIS
optional TimescaleDB
optional Redis

AI/ML
Scikit-learn
XGBoost
SHAP
optional PyTorch

SPATIAL
H3
Shapely
PostGIS
Leaflet/MapLibre

BACKEND
FastAPI
Pydantic
Uvicorn

FRONTEND
React
TypeScript
Tailwind CSS
Leaflet/MapLibre
Recharts

DEVOPS
Git
GitHub
Docker
GitHub Actions

TESTING
Pytest
Postman
Playwright
```

---

# 161. Recommended three-person concept ownership

## Person 1

Primary concepts:

```text
data engineering
ETL/ELT
IoT
MQTT
sensor calibration
sensor drift
time-series databases
GIS
PostGIS
GeoPandas
spatial indexing
spatial joins
```

## Person 2

Primary concepts:

```text
statistics
time-series
anomaly detection
change-point detection
supervised learning
classification
regression
feature engineering
XGBoost
probability
calibration
uncertainty
source attribution
dispersion
inverse problems
source apportionment
explainability
forecasting
```

## Person 3

Primary concepts:

```text
REST APIs
FastAPI
React
TypeScript
WebSockets
GIS visualization
exposure
decision support
rule engines
optimization
alerts
human-in-the-loop
```

---

# 162. Questions each team member should be able to answer

## Person 1

```text
Where does the data come from?
How often does it update?
How do you validate it?
How do you calibrate sensors?
How do you detect drift?
How do you store geospatial data?
How do you handle missing data?
```

## Person 2

```text
How do you know a pollution event is abnormal?
How do you determine the likely source?
Why is wind direction important?
Why is XGBoost suitable?
How do you calculate confidence?
What is source probability vs source contribution?
How do you evaluate the model?
How do you prevent false attribution?
```

## Person 3

```text
How does the dashboard obtain AI results?
How is neighbourhood exposure calculated?
How are alerts generated?
How are recommendations selected?
How does real-time updating work?
How does the system support government users?
```

---

# 163. Viva-ready explanation of the project

A concise technical answer:

> The platform is a multimodal, physics-informed decision-support system for urban air-pollution source attribution. It first collects and calibrates heterogeneous air-quality observations, aligns them spatially and temporally with weather, traffic, satellite and source-activity data, then detects abnormal pollution events. For each event, it generates candidate sources using GIS and wind backtracking. A machine-learning model such as XGBoost combines pollutant, spatial, temporal, traffic and activity features to estimate source probabilities. Physical dispersion evidence and independent observations are then fused with the ML output. The system reports source contribution estimates, calibrated confidence and uncertainty, predicts neighbourhood exposure, and recommends targeted operational responses. Human verification is retained for enforcement actions.

---

# 164. Important design philosophy

The platform should follow these principles:

```text
1. Measure before inferring.
2. Clean before modeling.
3. Detect events before attributing sources.
4. Filter candidates before running expensive models.
5. Combine physics and ML.
6. Keep probability separate from contribution.
7. Keep confidence separate from probability.
8. Allow unknown/unresolved outcomes.
9. Preserve uncertainty.
10. Keep human verification for enforcement.
11. Preserve raw data and lineage.
12. Evaluate using time-aware validation.
13. Prefer simple models before complex models.
14. Add complexity only when it improves measurable performance.
```

---

# 165. Final recommended learning roadmap

```text
PHASE 1
Python
SQL
Git
JSON
REST APIs

        ↓

PHASE 2
Pandas
NumPy
Statistics
Time-series basics

        ↓

PHASE 3
PostgreSQL
PostGIS
GeoPandas
GIS concepts

        ↓

PHASE 4
Scikit-learn
Classification
Regression
Anomaly detection
Feature engineering

        ↓

PHASE 5
XGBoost
SHAP
Probability calibration
Model evaluation

        ↓

PHASE 6
Wind backtracking
Dispersion concepts
Source attribution
Inverse problems

        ↓

PHASE 7
FastAPI
React
Maps
WebSockets

        ↓

PHASE 8
Advanced:
GNN
Transformers
PMF/CMB
HYSPLIT
Optimization
Active learning
```

---

# 166. Final architecture concept

The entire project can be understood as five nested levels:

```text
LEVEL 1 — OBSERVE
What is happening?

Sensors
CPCB
Satellite
Weather
Traffic
Citizen reports

        ↓

LEVEL 2 — DETECT
Is something unusual happening?

Baseline
Anomaly detection
Change-point detection
Spatial coherence

        ↓

LEVEL 3 — EXPLAIN
Why might it be happening?

GIS
Wind
Source signatures
ML
Dispersion
Satellite
Activity evidence
Evidence fusion

        ↓

LEVEL 4 — PREDICT
What happens next?

Forecast
Plume movement
Exposure

        ↓

LEVEL 5 — ACT
What should the authority do?

Exposure warning
Recommendation
Prioritization
Human verification
Feedback
```

---

# 167. Final mental model for the team

```text
                 REAL WORLD
                     |
                     v
                  DATA
                     |
                     v
              DATA ENGINEERING
                     |
                     v
                CLEAN DATA
                     |
                     v
            STATISTICS + GIS
                     |
                     v
              POLLUTION EVENT
                     |
                     v
             AI + PHYSICS
                     |
                     v
           SOURCE ATTRIBUTION
                     |
                     v
          PROBABILITY + UNCERTAINTY
                     |
                     v
                FORECAST
                     |
                     v
                EXPOSURE
                     |
                     v
             RECOMMENDATION
                     |
                     v
              HUMAN DECISION
                     |
                     v
                 FEEDBACK
                     |
                     v
             BETTER FUTURE MODELS
```

The central idea is therefore not simply:

> **"Train an AI model to predict pollution."**

It is:

> **"Build an evidence-driven system that detects abnormal pollution, reasons about possible causes using both physics and machine learning, quantifies uncertainty, estimates exposure, and supports targeted action."**
