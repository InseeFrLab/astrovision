"""
Tests for astrovision/sample/sample.py
"""

from astrovision.data.satellite_image import (
    SatelliteImage,
)
from astrovision.sample import (
    compute_distance_to_point,
    is_within_distance,
    sample_around_coordinates,
)
import pytest


@pytest.fixture
def satellite_image():
    path = "tests/test_data/ORT_2020052526656219_0499_8600_U38S_8Bits.jp2"
    satellite_image = SatelliteImage.from_raster(path)
    return satellite_image


@pytest.fixture
def satellite_image_land():
    path = "tests/test_data/ORT_2020052526656219_0509_8593_U38S_8Bits.jp2"
    satellite_image = SatelliteImage.from_raster(path)
    return satellite_image


def test_compute_distance_to_point(satellite_image_land):
    distance = compute_distance_to_point(
        satellite_image=satellite_image_land,
        coordinates=[-12.820789105073207, 45.144534566336205],
    )
    assert distance < 50


def test_is_within_distance(satellite_image_land):
    distance = 50
    assert is_within_distance(
        satellite_image=satellite_image_land,
        distance=distance,
        coordinates=[-12.820789105073207, 45.144534566336205],
    )


def test_is_within_distance_false(satellite_image_land):
    distance = 0.01
    assert not is_within_distance(
        satellite_image=satellite_image_land,
        distance=distance,
        coordinates=[-12.820789105073207, 45.144534566336205],
    )


def test_sample_around_coordinates(satellite_image, satellite_image_land):
    satellite_images = [satellite_image, satellite_image_land]
    distance = 15
    inside, outside = sample_around_coordinates(
        satellite_images=satellite_images,
        distance=distance,
        coordinates=[-12.820789105073207, 45.144534566336205],
    )
    assert len(inside) == 1
    assert len(outside) == 1
