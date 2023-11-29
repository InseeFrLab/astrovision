"""
Data module.
"""

from .satellite_image import SatelliteImage
from .satellite_image import SegmentationLabeledSatelliteImage

__all__ = [
    "SatelliteImage",
    "SegmentationLabeledSatelliteImage"
]
