"""
Data module.
"""
from .satellite_image import SatelliteImage
from .labeled_satellite_image import (
    SegmentationLabeledSatelliteImage,
    DetectionLabeledSatelliteImage,
    ClassificationLabeledSatelliteImage,
)

__all__ = [
    "SatelliteImage",
    "SegmentationLabeledSatelliteImage",
    "DetectionLabeledSatelliteImage",
    "ClassificationLabeledSatelliteImage",
]
