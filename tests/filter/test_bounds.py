"""
Tests for astrovision/filter/bounds.py
"""

from osgeo import ogr
from shapely.wkt import loads
from astrovision.data.satellite_image import (
    SatelliteImage,
)
from astrovision.filter.bounds import (
    filter_oob,
)
import pytest


@pytest.fixture
def oob_satellite_image():
    path = "tests/test_data/ORT_2020052526656219_0499_8600_U38S_8Bits.jp2"
    satellite_image = SatelliteImage.from_raster(path)
    return satellite_image


@pytest.fixture
def satellite_image():
    path = "tests/test_data/ORT_2020052526656219_0509_8593_U38S_8Bits.jp2"
    satellite_image = SatelliteImage.from_raster(path)
    return satellite_image


def test_filter_oob(oob_satellite_image, satellite_image):
    # Data source
    driver_name = "ESRI Shapefile"
    driver = ogr.GetDriverByName(driver_name)
    shapefile_path = "tests/test_data/adminexpress/976/REGION.shp"
    ds = driver.Open(shapefile_path, 0)
    layer = ds.GetLayer()
    feature = layer.GetNextFeature()
    ogr_geometry = feature.GetGeometryRef()

    # Geometry to shapely
    geometry_wkt = ogr_geometry.ExportToWkt()
    geometry = loads(geometry_wkt)

    # Projection
    crs = "EPSG:4471"  # For Mayotte

    filtered_images = filter_oob([oob_satellite_image, satellite_image], geometry, crs)
    assert len(filtered_images) == 1
