"""Canonical enumerations for the air-pollution source-attribution platform."""

from enum import Enum


class SourceType(str, Enum):
    TRAFFIC = "traffic"
    ROAD_DUST = "road_dust"
    CONSTRUCTION = "construction"
    INDUSTRIAL = "industrial"
    WASTE_BURNING = "waste_burning"
    BIOMASS_BURNING = "biomass_burning"
    REGIONAL_TRANSPORT = "regional_transport"
    BACKGROUND = "background"
    UNKNOWN = "unknown"


class Pollutant(str, Enum):
    PM25 = "pm25"
    PM10 = "pm10"
    NO2 = "no2"
    SO2 = "so2"
    CO = "co"
    O3 = "o3"


class EventSeverity(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class EventStatus(str, Enum):
    ACTIVE = "active"
    RESOLVED = "resolved"
    MONITORING = "monitoring"


class QualityFlag(str, Enum):
    VALID = "valid"
    SUSPECT = "suspect"
    INVALID = "invalid"
    CALIBRATED = "calibrated"