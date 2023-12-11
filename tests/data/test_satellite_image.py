"""
Tests for astrovision/data/satellite_image.py
"""
from astrovision.data.satellite_image import (
    SatelliteImage,
)
from osgeo import ogr
from shapely.wkt import loads
import shapely
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


@pytest.fixture
def satellite_image_2():
    path = "tests/test_data/ORT_2020052526656219_0506_8573_U38S_8Bits.jp2"
    satellite_image = SatelliteImage.from_raster(path)
    return satellite_image


def test_from_raster(satellite_image):
    assert satellite_image.array.shape == (3, 2000, 2000)


def test_channels_last(satellite_image):
    path = "tests/test_data/ORT_2020052526656219_0499_8600_U38S_8Bits.jp2"
    satellite_image = SatelliteImage.from_raster(path, channels_first=False)
    assert satellite_image.array.shape == (2000, 2000, 3)


def test_cast_to_float(satellite_image):
    path = "tests/test_data/ORT_2020052526656219_0499_8600_U38S_8Bits.jp2"
    satellite_image = SatelliteImage.from_raster(path, cast_to_float=True)
    assert np.issubdtype(satellite_image.array.dtype, np.floating)
    assert np.all((satellite_image.array >= 0) & (satellite_image.array <= 1))


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


def test_intersects_box_1(
    satellite_image,
):
    box_bounds = satellite_image.bounds
    crs = satellite_image.crs
    assert satellite_image.intersects_box(box_bounds=box_bounds, crs=crs)


def test_intersects_box_2(
    satellite_image,
    satellite_image_2,
):
    box_bounds = satellite_image_2.bounds
    crs = satellite_image_2.crs
    assert not satellite_image.intersects_box(box_bounds=box_bounds, crs=crs)


shapefile = "states.shp"
driver = ogr.GetDriverByName("ESRI Shapefile")
dataSource = driver.Open(shapefile, 0)
layer = dataSource.GetLayer()


def test_intersects_polygon_1(
    satellite_image,
):
    geometries = []
    shapefile_path = "tests/test_data/adminexpress/971/REGION.shp"
    ds = ogr.Open(shapefile_path)
    layer = ds.GetLayer()
    feature = layer.GetNextFeature()
    for feature in layer:
        geometry_wkt = feature.GetGeometryRef().ExportToWkt()
        geometries.append(loads(geometry_wkt))

    multipolygon = shapely.geometry.MultiPolygon(geometries)
    crs_epsg = layer.GetSpatialRef().GetAuthorityCode(None)

    assert not satellite_image.intersects_polygon(
        polygon_geometry=multipolygon, crs=crs_epsg
    )


def test_intersects_polygon_2(
    satellite_image,
):
    shapefile_path = "tests/test_data/adminexpress/976/REGION.shp"
    ds = ogr.Open(shapefile_path)
    layer = ds.GetLayer()
    feature = layer.GetNextFeature()
    geometry_wkt = feature.GetGeometryRef().ExportToWkt()
    polygon_geometry = loads(geometry_wkt)

    crs = layer.GetSpatialRef().ExportToWkt()
    assert satellite_image.intersects_polygon(
        polygon_geometry=polygon_geometry, crs=crs
    )
