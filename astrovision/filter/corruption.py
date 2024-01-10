"""
Filtering functions.
"""
import numpy as np
from typing import List
from ..data import SatelliteImage


def is_corrupted(
    image: SatelliteImage,
    black_value_threshold: int = 25,
    black_area_threshold: float = 0.5,
) -> bool:
    """
    Check if image is corrupted.

    Args:
        image (SatelliteImage): Satellite image.
        black_value_threshold (int): The intensity threshold to consider
            a pixel as black. Pixels with intensity values less than
            this threshold are considered black. Default is 100.
        black_area_threshold (float): The threshold for the proportion
            of black pixels in the image. If the ratio of black pixels
            exceeds this threshold, the function returns True. Default is 0.5.

    Returns:
        bool: True if image is corrupted, False otherwise.
    """
    # Convert the RGB image to grayscale
    gray_image = (
        0.2989 * image.array[0] + 0.5870 * image.array[1] + 0.1140 * image.array[2]
    )

    # Count the number of black pixels
    nb_black_pixels = np.sum(gray_image < black_value_threshold)

    # Calculate the proportion of black pixels
    black_pixel_ratio = nb_black_pixels / np.prod(gray_image.shape)

    # Check if the proportion exceeds the threshold
    return black_pixel_ratio >= black_area_threshold


def filter_corrupted(
    satellite_images: List[SatelliteImage],
    black_value_threshold: int = 25,
    black_area_threshold: float = 0.5,
) -> List[SatelliteImage]:
    """
    Filter out corrupted images.

    Args:
        satellite_images (List[SatelliteImage]): List of satellite images.
    Returns:
        List[SatelliteImage]: List of satellite images without corrupted images.
    """
    corrupted_images = []
    for satellite_image in satellite_images:
        if not is_corrupted(
            satellite_image, black_value_threshold, black_area_threshold
        ):
            corrupted_images.append(satellite_image)
    return corrupted_images
