"""
Utility functions for plotting.
"""
import numpy as np
from typing import List
from ..data import (
    SatelliteImage,
    SegmentationLabeledSatelliteImage,
    DetectionLabeledSatelliteImage,
    ClassificationLabeledSatelliteImage,
)
import rasterio
from rasterio.merge import merge
from matplotlib import pyplot as plt


def plot_images(
    satellite_images: List[SatelliteImage],
    bands_indices: List[int],
):
    """
    Plot satellite images.

    Args:
        satellite_images (List[SatelliteImage]): Images.
        bands_indices (List[int]): Indices of bands to plot.
    """
    # Create mosaic from satellite images
    memory_files = []
    raster_list = []
    for i, image in enumerate(satellite_images):
        array = image.normalize().array
        memfile = rasterio.io.MemoryFile()
        with memfile.open(
            driver="GTiff",
            height=array.shape[1],
            width=array.shape[2],
            count=len(bands_indices),
            dtype=rasterio.float64,
            crs=image.crs,
            transform=image.transform,
        ) as dataset:
            dataset.write(array, [idx + 1 for idx in bands_indices])
        memory_files.append(memfile)

    for memfile in memory_files:
        raster_list.append(rasterio.open(memfile))

    mosaic, _ = merge(raster_list)

    # Plot mosaic
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.imshow(np.transpose(mosaic, (1, 2, 0)))
    plt.xticks([])
    plt.yticks([])
    plt.show()

    return plt.gcf()


def plot_images_with_segmentation_label(
    labeled_satellite_images: List[SegmentationLabeledSatelliteImage],
    bands_indices: List[int],
    overlay: bool = True,
):
    """
    Plot satellite images with segmentation labels.

    Args:
        labeled_satellite_images (List[ClassificationLabeledSatelliteImage]):
            Images with segmentation label.
        bands_indices (List[int]): Indices of bands to plot.
        overlay (bool): Whether to overlay segmentation label on top
            of satellite image.
    """
    # Create mosaic from satellite images including segmentation label
    memory_files = []
    raster_list = []
    for i, labeled_image in enumerate(labeled_satellite_images):
        image = labeled_image.satellite_image
        array = image.normalize().array
        memfile = rasterio.io.MemoryFile()
        with memfile.open(
            driver="GTiff",
            height=array.shape[1],
            width=array.shape[2],
            count=len(bands_indices) + 1,
            dtype=rasterio.float64,
            crs=image.crs,
            transform=image.transform,
        ) as dataset:
            dataset.write(array, [idx + 1 for idx in bands_indices])
            dataset.write(
                labeled_image.label,
                len(bands_indices) + 1,
            )
        memory_files.append(memfile)

    for memfile in memory_files:
        raster_list.append(rasterio.open(memfile))

    mosaic, _ = merge(raster_list)

    # Plot mosaic
    image_mosaic = np.transpose(mosaic[: len(bands_indices), :, :], (1, 2, 0))
    label_mosaic = mosaic[-1, :, :]
    if overlay:
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.imshow(
            image_mosaic,
        )
        ax.imshow(
            label_mosaic,
            alpha=0.2,
        )
        plt.xticks([])
        plt.yticks([])
        plt.show()
    else:
        fig, ax = plt.subplots(1, 2, figsize=(15, 15))
        ax[0].imshow(image_mosaic)  # with normalization for display
        ax[0].set_axis_off()
        ax[1].imshow(label_mosaic)
        ax[1].set_axis_off()
        plt.show()

    # Return plot
    return plt.gcf()


def plot_images_with_classification_label(
    labeled_satellite_images: List[ClassificationLabeledSatelliteImage],
    bands_indices: List[int],
    overlay: bool = True,
):
    """
    Plot satellite images with classification labels.

    Args:
        labeled_satellite_images (List[ClassificationLabeledSatelliteImage]):
            Images with classification labels.
        bands_indices (List[int]): Indices of bands to plot.
        overlay (bool): Whether to overlay segmentation label on top
            of satellite image.
    """
    segmented_images = []
    for labeled_image in labeled_satellite_images:
        segmentation_label = (
            np.ones(
                (
                    labeled_image.satellite_image.array.shape[1],
                    labeled_image.satellite_image.array.shape[2],
                )
            )
            * labeled_image.label
        )
        segmented_images.append(
            SegmentationLabeledSatelliteImage(
                labeled_image.satellite_image,
                segmentation_label,
            )
        )

    return plot_images_with_segmentation_label(segmented_images, bands_indices, overlay)


def plot_images_with_detection_label(
    labeled_satellite_images: List[DetectionLabeledSatelliteImage],
    bands_indices: List[int],
    overlay: bool = True,
):
    """
    Plot satellite images with detection labels.

    Args:
        labeled_satellite_images (List[DetectionLabeledSatelliteImage]): Images with
            detection labels.
        bands_indices (List[int]): Indices of bands to plot.
        overlay (bool, optional): Whether to overlay segmentation label on top.
            Defaults to True.
    """
    segmented_images = []
    for labeled_image in labeled_satellite_images:
        segmentation_label = np.zeros(
            (
                labeled_image.satellite_image.array.shape[1],
                labeled_image.satellite_image.array.shape[2],
            )
        )
        for bounding_box in labeled_image.label:
            x0, y0, x1, y1 = bounding_box
            segmentation_label[x0:x1, y0:y1] = 1
        segmented_images.append(
            SegmentationLabeledSatelliteImage(
                labeled_image.satellite_image,
                segmentation_label,
            )
        )

    return plot_images_with_segmentation_label(segmented_images, bands_indices, overlay)
