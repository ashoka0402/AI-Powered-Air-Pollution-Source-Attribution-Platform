"""Custom exceptions for the AI layer."""


class AILayerError(Exception):
    """Base exception for Person 2 modules."""


class InsufficientDataError(AILayerError):
    """Raised when there is not enough data to compute baseline / attribution."""


class ModelNotLoadedError(AILayerError):
    """Raised when a required ML model artifact is missing."""


class InvalidEventError(AILayerError):
    """Raised when an event object is incomplete or inconsistent."""