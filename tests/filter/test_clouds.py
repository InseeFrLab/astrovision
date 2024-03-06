"""
Tests for the clouds filter.
"""

from astrovision.data.satellite_image import (
    SatelliteImage,
)
from astrovision.filter.clouds import (
    filter_cloudy,
)
import pytest
import numpy as np


@pytest.fixture
def satellite_image():
    path = "tests/test_data/ORT_2020052526656219_0509_8593_U38S_8Bits.jp2"
    satellite_image = SatelliteImage.from_raster(path)
    return satellite_image


def test_filter_cloudy(satellite_image):
    cloud_mask = np.zeros((2000, 2000))
    filtered_images = filter_cloudy([satellite_image], [cloud_mask])
    assert len(filtered_images) == 1


def test_filter_cloudy_2(satellite_image):
    cloud_mask = np.ones((2000, 2000))
    filtered_images = filter_cloudy([satellite_image], [cloud_mask])
    assert len(filtered_images) == 0


def test_filter_cloudy_3(satellite_image):
    cloud_mask = np.ones((2000, 2000))
    cloud_mask[0:1001, :] = 0
    filtered_images = filter_cloudy([satellite_image], [cloud_mask])
    assert len(filtered_images) == 1
