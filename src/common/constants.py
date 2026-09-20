"""Project-wide constants for Person 2 AI layer."""

MODEL_VERSION = "attribution_v1"
FORECASTER_VERSION = "forecaster_v1"

# Baseline windows (hours)
BASELINE_LOOKBACK_HOURS = 168  # 7 days
BASELINE_TIME_OF_DAY_WINDOW_HOURS = 2

# Anomaly / event thresholds
ANOMALY_ZSCORE_THRESHOLD = 2.0
EVENT_MIN_DURATION_MINUTES = 30
EVENT_MERGE_WINDOW_MINUTES = 60

# Spatial
MAX_CANDIDATE_DISTANCE_KM = 15.0
UPWIND_ANGLE_TOLERANCE_DEG = 45.0

# Confidence
MIN_CONFIDENCE = 0.15
MAX_CONFIDENCE = 0.98

# Source types used by attribution model (order matters for encoding)
ATTRIBUTION_SOURCE_TYPES = [
    "traffic",
    "road_dust",
    "construction",
    "industrial",
    "waste_burning",
    "biomass_burning",
    "regional_transport",
    "background",
    "unknown",
]

# Default pollutant signatures (relative weights, illustrative for MVP)
POLLUTANT_SIGNATURES = {
    "traffic": {"pm25": 0.35, "pm10": 0.25, "no2": 0.55, "co": 0.40, "so2": 0.10},
    "road_dust": {"pm25": 0.40, "pm10": 0.70, "no2": 0.10, "co": 0.05, "so2": 0.05},
    "construction": {"pm25": 0.45, "pm10": 0.75, "no2": 0.15, "co": 0.10, "so2": 0.10},
    "industrial": {"pm25": 0.30, "pm10": 0.35, "no2": 0.30, "so2": 0.60, "co": 0.20},
    "waste_burning": {"pm25": 0.65, "pm10": 0.50, "no2": 0.20, "co": 0.45, "so2": 0.25},
    "biomass_burning": {"pm25": 0.70, "pm10": 0.55, "no2": 0.15, "co": 0.50, "so2": 0.15},
    "regional_transport": {"pm25": 0.50, "pm10": 0.40, "no2": 0.25, "co": 0.20, "so2": 0.20},
    "background": {"pm25": 0.20, "pm10": 0.20, "no2": 0.15, "co": 0.10, "so2": 0.10},
    "unknown": {"pm25": 0.25, "pm10": 0.25, "no2": 0.20, "co": 0.15, "so2": 0.15},
}