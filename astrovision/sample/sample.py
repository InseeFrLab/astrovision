"""
Functions to sample from a list of satellite images.
"""
from geopy.distance import geodesic
from pyproj import Transformer
from typing import List
from ..data import SatelliteImage


def sample_around_coordinates(
    satellite_images: List[SatelliteImage],
    coordinates: List[float],
    distance: float,
    crs: str = "EPSG:4326",
):
    """ """
    inside_images = []
    outside_images = []

    if crs != "EPSG:4326":
        lat, lon = project(coordinates, crs, "EPSG:4326")
    else:
        lat, lon = coordinates

    for satellite_image in satellite_images:
        x0, y0, x1, y1 = satellite_image.bounds
        centroid_x = (x0 + x1) / 2
        centroid_y = (y0 + y1) / 2

        # Convert pixel coordinates to real-world coordinates using the transform
        centroid_x, centroid_y = satellite_image.transform * (centroid_x, centroid_y)

        if satellite_image.crs != "EPSG:4326":
            centroid_lat, centroid_lon = project(
                (centroid_x, centroid_y), satellite_image.crs, "EPSG:4326"
            )
        else:
            centroid_lat, centroid_lon = centroid_x, centroid_y

        # Calculate the geodesic distance between the two points
        if geodesic((lat, lon), (centroid_lat, centroid_lon)).meters / 1000 < distance:
            inside_images.append(satellite_image)
        else:
            outside_images.append(satellite_image)

    return inside_images, outside_images


def project(coordinates, input_crs, output_crs):
    """ """
    transformer = Transformer.from_crs(input_crs, output_crs)
    input_lat, input_lon = coordinates
    return transformer(*coordinates)
