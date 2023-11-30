"""
Tests for astrovision/data/labeled_satellite_image.py
"""
from astrovision.data.satellite_image import SatelliteImage
from astrovision.data.labeled_satellite_image import (
    SegmentationLabeledSatelliteImage,
    DetectionLabeledSatelliteImage,
)
import pytest
import numpy as np


@pytest.fixture
def segmentation_labeled_image():
    path = "tests/test_data/ORT_2020052526656219_0499_8600_U38S_8Bits.jp2"
    # Shape is (3, 2000, 2000)
    satellite_image = SatelliteImage.from_raster(path)
    label = np.zeros(satellite_image.array.shape[1:])
    label[0, 0] = 1
    segmentation_labeled_image = SegmentationLabeledSatelliteImage(
        satellite_image=satellite_image, label=label
    )
    return segmentation_labeled_image


@pytest.fixture
def segmentation_identity_labeled_image():
    path = "tests/test_data/ORT_2020052526656219_0499_8600_U38S_8Bits.jp2"
    # Shape is (3, 2000, 2000)
    satellite_image = SatelliteImage.from_raster(path)
    label = np.identity(2000)
    segmentation_labeled_image = SegmentationLabeledSatelliteImage(
        satellite_image=satellite_image, label=label
    )
    return segmentation_labeled_image


@pytest.fixture
def empty_segmentation_labeled_image():
    path = "tests/test_data/ORT_2020052526656219_0499_8600_U38S_8Bits.jp2"
    # Shape is (3, 2000, 2000)
    satellite_image = SatelliteImage.from_raster(path)
    label = np.zeros((2000, 2000))
    segmentation_labeled_image = SegmentationLabeledSatelliteImage(
        satellite_image=satellite_image, label=label
    )
    return segmentation_labeled_image


def test_split(segmentation_labeled_image, segmentation_identity_labeled_image):
    # 1st split
    tiles = segmentation_labeled_image.split(1000)
    assert len(tiles) == 4

    n_empty_tiles = 0
    n_single_one_tiles = 0
    n_other_tiles = 0
    for tile in tiles:
        label = tile.label
        assert label.shape == (1000, 1000)
        if not np.any(label):
            n_empty_tiles += 1
        elif label.sum() == 1:
            n_single_one_tiles += 1
        else:
            n_other_tiles += 1
    assert n_empty_tiles == 3
    assert n_single_one_tiles == 1
    assert n_other_tiles == 0

    # 2nd split
    tiles = segmentation_identity_labeled_image.split(1000)
    assert len(tiles) == 4
    for tile in tiles:
        label = tile.label
        assert label.shape == (1000, 1000)
        assert np.array_equal(label, np.identity(1000)) | np.array_equal(
            label, np.zeros_like(label)
        )


def test_segmentation_to_classification(
    segmentation_labeled_image, empty_segmentation_labeled_image
):
    classification_label = (
        segmentation_labeled_image.to_classification_labeled_image().label
    )
    assert classification_label == 1

    classification_label = (
        empty_segmentation_labeled_image.to_classification_labeled_image().label
    )
    assert classification_label == 0


@pytest.fixture
def detection_labeled_image():
    path = "tests/test_data/ORT_2020052526656219_0499_8600_U38S_8Bits.jp2"
    # Shape is (3, 2000, 2000)
    satellite_image = SatelliteImage.from_raster(path)
    label = [(10, 10, 20, 20)]
    labeled_image = DetectionLabeledSatelliteImage(
        satellite_image=satellite_image, label=label
    )
    return labeled_image


@pytest.fixture
def empty_detection_labeled_image():
    path = "tests/test_data/ORT_2020052526656219_0499_8600_U38S_8Bits.jp2"
    # Shape is (3, 2000, 2000)
    satellite_image = SatelliteImage.from_raster(path)
    label = []
    labeled_image = DetectionLabeledSatelliteImage(
        satellite_image=satellite_image, label=label
    )
    return labeled_image


def test_wrong_detection_label():
    path = "tests/test_data/ORT_2020052526656219_0499_8600_U38S_8Bits.jp2"
    # Shape is (3, 2000, 2000)
    satellite_image = SatelliteImage.from_raster(path)
    label = [(5, 7, 2000, 9)]
    with pytest.raises(Exception):
        labeled_image = DetectionLabeledSatelliteImage(
            satellite_image=satellite_image, label=label
        )


def test_detection_to_classification(
    detection_labeled_image, empty_detection_labeled_image
):
    classification_label = (
        detection_labeled_image.to_classification_labeled_image().label
    )
    assert classification_label == 1

    classification_label = (
        empty_detection_labeled_image.to_classification_labeled_image().label
    )
    assert classification_label == 0
