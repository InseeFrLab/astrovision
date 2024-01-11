"""
Utility functions for plotting.
"""
import numpy as np
from typing import List
from ..data import SatelliteImage
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
