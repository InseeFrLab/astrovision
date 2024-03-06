"""
Tests for astrovision/filter/corruption.py
"""

import numpy as np
from astrovision.data.satellite_image import (
    SatelliteImage,
)
from astrovision.filter.corruption import (
    is_corrupted,
    filter_corrupted,
)
import pytest


@pytest.fixture
def corrupted_satellite_image():
    path = "tests/test_data/ORT_2020052526656219_0499_8600_U38S_8Bits.jp2"
    satellite_image = SatelliteImage.from_raster(path)
    return satellite_image


@pytest.fixture
def satellite_image():
    path = "tests/test_data/ORT_2020052526656219_0509_8593_U38S_8Bits.jp2"
    satellite_image = SatelliteImage.from_raster(path)
    return satellite_image


def test_is_not_corrupted(satellite_image):
    assert not is_corrupted(satellite_image)


def test_is_corrupted(satellite_image):
    satellite_image.array[:, 0:1001, :] = 0
    assert is_corrupted(satellite_image)


def test_is_corrupted_2(corrupted_satellite_image):
    assert is_corrupted(corrupted_satellite_image)


def test_filter_corrupted(satellite_image):
    corrupted_image = satellite_image.copy()
    corrupted_image.array[:, 0:1001, :] = 0
    satellite_images = [satellite_image, corrupted_image]
    filtered_images = filter_corrupted(satellite_images)
    assert len(filtered_images) == 1
    assert np.array_equal(filtered_images[0].array, satellite_image.array)
