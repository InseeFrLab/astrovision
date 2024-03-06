"""
Test the plot_utils module.
"""

from astrovision.data.satellite_image import (
    SatelliteImage,
)
from astrovision.plot import make_mosaic
import pytest
import numpy as np


@pytest.fixture
def satellite_image():
    path = "tests/test_data/ORT_2020052526656219_0499_8600_U38S_8Bits.jp2"
    satellite_image = SatelliteImage.from_raster(path)
    return satellite_image


def test_mosaic(satellite_image):
    tiles = satellite_image.split(500)
    mosaic = make_mosaic(tiles, bands_indices=[0, 1, 2])
    # Check arrays are the same
    assert np.allclose(satellite_image.array, mosaic.array)
    assert satellite_image.crs == mosaic.crs
    assert satellite_image.bounds[0] == mosaic.bounds[0]
    assert satellite_image.bounds[1] == mosaic.bounds[1]
    assert satellite_image.bounds[2] == mosaic.bounds[2]
    assert satellite_image.bounds[3] == mosaic.bounds[3]
    assert satellite_image.transform == mosaic.transform


def test_plot_images():
    # TODO: Implement test
    # Just a placeholder for now
    pass


def test_plot_images_with_segmentation_label():
    # TODO: Implement test
    # Just a placeholder for now
    pass


def test_plot_images_with_classification_label():
    # TODO: Implement test
    # Just a placeholder for now
    pass


def test_plot_images_with_detection_label():
    # TODO: Implement test
    # Just a placeholder for now
    pass
