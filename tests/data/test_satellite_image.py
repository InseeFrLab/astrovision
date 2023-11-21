"""
Tests for astrovision/data/satellite_image.py
"""
from astrovision.data.satellite_image import (
    SatelliteImage,
)
import tempfile
import pytest
from pathlib import Path
import torch
import numpy as np


@pytest.fixture
def satellite_image():
    path = "tests/test_data/ORT_2020052526656219_0499_8600_U38S_8Bits.jp2"
    satellite_image = SatelliteImage.from_raster(path)
    return satellite_image


def test_from_raster(satellite_image):
    assert satellite_image.array.shape == (3, 2000, 2000)


def test_split(satellite_image):
    # 1st split
    tiles = satellite_image.split(1000)
    assert len(tiles) == 4
    for tile in tiles:
        assert tile.array.shape == (3, 1000, 1000)

    # 2nd split with overlap
    tiles = satellite_image.split(1500)
    assert len(tiles) == 4
    for tile in tiles:
        assert tile.array.shape == (3, 1500, 1500)


def test_to_tensor(satellite_image):
    # 1st tensor conversion
    tensor = satellite_image.to_tensor(bands_indices=None)
    assert isinstance(tensor, torch.Tensor)
    assert tensor.size() == torch.Size([3, 2000, 2000])

    # 2nd tensor conversion
    tensor = satellite_image.to_tensor(bands_indices=[0, 2])
    assert isinstance(tensor, torch.Tensor)
    assert tensor.size() == torch.Size([2, 2000, 2000])


def test_normalize(satellite_image):
    normalized_image = satellite_image.normalize()
    assert isinstance(normalized_image, SatelliteImage)
    normalized_array = normalized_image.array
    assert np.all((normalized_array >= 0) & (normalized_array <= 1))


def test_copy(satellite_image):
    copy = satellite_image.copy()
    assert np.all(satellite_image.array == copy.array)


def test_to_raster(satellite_image):
    with tempfile.TemporaryDirectory() as tmpdirname:
        # .jp2 file
        file_name = Path(tmpdirname) / "tmp.jp2"
        file_name = file_name.absolute().as_posix()
        satellite_image.to_raster(file_name)

        read_image = SatelliteImage.from_raster(file_name)
        assert isinstance(read_image, SatelliteImage)
        assert read_image.array.shape == (3, 2000, 2000)

        # .tif file
        # TODO: run this test but this requires fixing install
        # issues
        # file_name = Path(tmpdirname) / "tmp.tif"
        # file_name = file_name.absolute().as_posix()
        # satellite_image.to_raster(file_name)

        # read_image = SatelliteImage.from_raster(file_name)
        # assert isinstance(read_image, SatelliteImage)
        # assert read_image.array.shape == (3, 2000, 2000)
