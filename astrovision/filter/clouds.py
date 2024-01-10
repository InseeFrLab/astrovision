"""
Cloud filtering.
"""
from typing import List
import numpy as np
from ..data import SatelliteImage


def filter_cloudy(
    satellite_images: List[SatelliteImage],
    cloud_masks: List[np.array],
    cloud_threshold: float = 0.5,
):
    """
    Filter out cloudy images.
    """
    if len(satellite_images) != len(cloud_masks):
        raise ValueError("Length of satellite_images and cloud_masks must be the same.")
    cloudless_images = []
    for satellite_image, cloud_mask in zip(satellite_images, cloud_masks):
        cloud_coverage = np.sum(cloud_mask) / np.prod(cloud_mask.shape)
        if cloud_coverage < cloud_threshold:
            cloudless_images.append(satellite_image)
    return cloudless_images
