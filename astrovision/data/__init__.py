"""
Data module.
"""
from .satellite_image import SatelliteImage
from .labeled_satellite_image import SegmentationLabeledSatelliteImage

__all__ = ["SatelliteImage", "SegmentationLabeledSatelliteImage"]
