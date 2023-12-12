"""
Functions to sample from a list of satellite images.
"""
from geopy.distance import geodesic
from pyproj import Transformer
from typing import List, Tuple
from ..data import SatelliteImage


def compute_distance_to_point(
    satellite_image: SatelliteImage, coordinates: List[float], crs: str = "EPSG:4326"
) -> float:
    """
    Return distance between the centroid of a satellite image
    and a point with coordinates `coordinates`.

    Args:
        satellite_image (SatelliteImage): Satellite image.
        coordinates (List[float]): Coordinates of the point.
        crs (str): EPSG of coordinates. Defaults to "EPSG:4326".

    Returns:
        float: Distance in kilometers.
    """
    # Reproject coordinates to lat and long if needed
    if crs != "EPSG:4326":
        lat, lon = project(coordinates, crs, "EPSG:4326")
    else:
        lat, lon = coordinates

    # Get centroid coordinates
    x0, y0, x1, y1 = satellite_image.bounds
    centroid_x = (x0 + x1) / 2
    centroid_y = (y0 + y1) / 2

    # Reproject centroid coordinates if needed
    if satellite_image.crs != "EPSG:4326":
        centroid_lat, centroid_lon = project(
            (centroid_x, centroid_y), satellite_image.crs, "EPSG:4326"
        )
    else:
        centroid_lat, centroid_lon = centroid_x, centroid_y

    # Return the geodesic distance between the two points
    return geodesic((lat, lon), (centroid_lat, centroid_lon)).meters / 1000


def is_within_distance(
    satellite_image: SatelliteImage,
    distance: float,
    coordinates: List[float],
    crs: str = "EPSG:4326",
) -> bool:
    """
    Return True if the centroid of a satellite image is within distance
    `distance` of a point with coordinates `coordinates`.

    Args:
        satellite_image (SatelliteImage): Satellite image.
        distance (float): Distance in kilometers.
        coordinates (List[float]): Coordinates of the point.
        crs (str): EPSG. Defaults to "EPSG:4326".

    Returns:
        bool: True if image is within distance.
    """
    if (
        compute_distance_to_point(
            satellite_image=satellite_image, coordinates=coordinates, crs=crs
        )
        < distance
    ):
        return True
    return False


def sample_around_coordinates(
    satellite_images: List[SatelliteImage],
    distance: float,
    coordinates: List[float],
    crs: str = "EPSG:4326",
) -> Tuple[List[SatelliteImage]]:
    """
    Sample satellite images which are within a distance
    `distance` from a point with coordinates `coordinates`.

    Args:
        satellite_image (SatelliteImage): Satellite image.
        distance (float): Distance in kilometers.
        coordinates (List[float]): Coordinates of the point.
        crs (str): EPSG. Defaults to "EPSG:4326".

    Returns:
        Tuple[List[SatelliteImage]]: Tuple containing two lists,
            the first containing the images which are within the
            given distance of the specified point and the second
            containing the others.
    """
    inside_images = []
    outside_images = []

    for satellite_image in satellite_images:
        if is_within_distance(
            satellite_image=satellite_image,
            distance=distance,
            coordinates=coordinates,
            crs=crs,
        ):
            inside_images.append(satellite_image)
        else:
            outside_images.append(satellite_image)
    return inside_images, outside_images


def project(coordinates: List[float], input_crs: str, output_crs: str) -> List[float]:
    """
    Reproject coordinates.

    Args:
        coordinates (List[float]): Coordinates.
        input_crs (str): EPSG.
        output_crs (str): EPSG.

    Returns:
        List[float]: Reprojected coordinates.
    """
    transformer = Transformer.from_crs(input_crs, output_crs)
    input_lat, input_lon = coordinates
    return transformer.transform(*coordinates)
