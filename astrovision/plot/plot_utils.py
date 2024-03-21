"""
Utility functions for plotting.
"""

import numpy as np
from typing import List, Union
from ..data import (
    SatelliteImage,
    SegmentationLabeledSatelliteImage,
    DetectionLabeledSatelliteImage,
    ClassificationLabeledSatelliteImage,
)
import rasterio
from rasterio.merge import merge
from matplotlib import pyplot as plt


def make_mosaic(
    images: List[Union[SatelliteImage, SegmentationLabeledSatelliteImage]],
    bands_indices: List[int],
):
    """
    Creates a mosaic image from a list of satellite images.

    Args:
        images (List[Union[SatelliteImage, SegmentationLabeledSatelliteImage]]):
            A list of satellite images to be used for creating the mosaic.
        bands_indices (List[int]):
            A list of band indices to be used for creating the mosaic.

    Returns:
        The mosaic image created from the input images.

    Raises:
        ValueError: If the image type is not supported.

    """
    if isinstance(images[0], SatelliteImage):
        return make_mosaic_si(images, bands_indices)
    elif isinstance(images[0], SegmentationLabeledSatelliteImage):
        return make_mosaic_lsi(images, bands_indices)
    else:
        raise ValueError("Unsupported image type")


def make_mosaic_si(
    satellite_images: List[SatelliteImage],
    bands_indices: List[int],
) -> SatelliteImage:
    """
    Create a mosaic from satellite images.

    Args:
        satellite_images (List[SatelliteImage]): Images.
        bands_indices (List[int]): Indices of bands to include in the mosaic.

    Returns:
        SatelliteImage: Mosaic of satellite images.
    """
    # Check all images have same CRS
    if len(satellite_images) == 1:
        pass
    else:
        reference_crs = satellite_images[0].crs
        for idx in range(1, len(satellite_images)):
            if satellite_images[idx].crs != reference_crs:
                return ValueError("Images must have the same CRS.")

    # Create mosaic array from satellite images
    memory_files = []
    raster_list = []
    for i, image in enumerate(satellite_images):
        array = image.array
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

    mosaic, out_transform = merge(raster_list)

    # Compute bounds
    left = min([satellite_image.bounds[0] for satellite_image in satellite_images])
    bottom = min([satellite_image.bounds[1] for satellite_image in satellite_images])
    right = max([satellite_image.bounds[2] for satellite_image in satellite_images])
    top = max([satellite_image.bounds[3] for satellite_image in satellite_images])
    bounds = (left, bottom, right, top)

    # Create SatelliteImage
    # TODO: dep and date if all images have same dep and date
    mosaic_image = SatelliteImage(
        array=mosaic.astype("uint8"),
        crs=satellite_images[0].crs,
        bounds=bounds,
        transform=out_transform,
    )

    return mosaic_image


def make_mosaic_lsi(
    labelled_satellite_images: List[SegmentationLabeledSatelliteImage],
    bands_indices: List[int],
) -> SegmentationLabeledSatelliteImage:
    """
    Create a mosaic from labeled satellite images.

    Args:
        labelled_satellite_images (List[SegmentationLabeledSatelliteImage]): Labeled images.
        bands_indices (List[int]): Indices of bands to include in the mosaic.

    Returns:
        SegmentationLabeledSatelliteImage: Mosaic of satellite images and labels.
    """
    # Check all images have same CRS
    if len(labelled_satellite_images) == 1:
        pass
    else:
        reference_crs = labelled_satellite_images[0].satellite_image.crs
        for idx in range(1, len(labelled_satellite_images)):
            if labelled_satellite_images[idx].satellite_image.crs != reference_crs:
                return ValueError("Images must have the same CRS.")

    # Create mosaic array from satellite images
    memory_files = []
    raster_list = []
    for i, image in enumerate(labelled_satellite_images):
        array = image.satellite_image.array
        memfile = rasterio.io.MemoryFile()
        with memfile.open(
            driver="GTiff",
            height=array.shape[1],
            width=array.shape[2],
            count=len(bands_indices),
            dtype=rasterio.float64,
            crs=image.satellite_image.crs,
            transform=image.satellite_image.transform,
        ) as dataset:
            dataset.write(array, [idx + 1 for idx in bands_indices])
        memory_files.append(memfile)

    for memfile in memory_files:
        raster_list.append(rasterio.open(memfile))

    mosaic, out_transform = merge(raster_list)

    # Compute bounds
    left = min([lsi.satellite_image.bounds[0] for lsi in labelled_satellite_images])
    bottom = min([lsi.satellite_image.bounds[1] for lsi in labelled_satellite_images])
    right = max([lsi.satellite_image.bounds[2] for lsi in labelled_satellite_images])
    top = max([lsi.satellite_image.bounds[3] for lsi in labelled_satellite_images])
    bounds = (left, bottom, right, top)

    # Create SatelliteImage
    # TODO: dep and date if all images have same dep and date
    mosaic_image = SatelliteImage(
        array=mosaic.astype("uint8"),
        crs=labelled_satellite_images[0].satellite_image.crs,
        bounds=bounds,
        transform=out_transform,
    )

    # Create mosaic array from labels
    memory_files = []
    raster_list = []
    for i, image in enumerate(labelled_satellite_images):
        label = np.expand_dims(image.label, axis=0)
        memfile = rasterio.io.MemoryFile()
        with memfile.open(
            driver="GTiff",
            height=label.shape[1],
            width=label.shape[2],
            count=1,
            dtype=rasterio.float64,
            crs=image.satellite_image.crs,
            transform=image.satellite_image.transform,
        ) as dataset:
            dataset.write(label)
        memory_files.append(memfile)

    for memfile in memory_files:
        raster_list.append(rasterio.open(memfile))

    mosaic_mask, out_transform = merge(raster_list)

    mosaic_labelled = SegmentationLabeledSatelliteImage(
        mosaic_image, np.squeeze(mosaic_mask)
    )

    return mosaic_labelled


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
    # TODO: here and in the following functions:
    # TODO: plot mosaic from `make_mosaic` function
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
