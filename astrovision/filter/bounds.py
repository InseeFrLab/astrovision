"""
Filter out of bounds images.
"""
from typing import List
from shapely.geometry import Polygon
from ..data import SatelliteImage


def filter_oob(
    satellite_images: List[SatelliteImage],
    polygon_geometry: Polygon,
    crs: str,
) -> List[SatelliteImage]:
    """
    Filter out images that are not within the bounds of a box.

    Args:
        satellite_images (List[SatelliteImage]): List of satellite images.
        polygon_geometry (Polygon): Polygon.
        crs (str): EPSG of the bounds.

    Returns:
        List[SatelliteImage]: List of satellite images within the bounds of the box.
    """
    inbound_images = []
    for satellite_image in satellite_images:
        if satellite_image.intersects_polygon(
            polygon_geometry,
            crs,
        ):
            inbound_images.append(satellite_image)
    return inbound_images
