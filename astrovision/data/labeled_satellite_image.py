"""
Classes representing satellite images labeled according
to a segmentation, a classification or an object detection
task.
"""
from __future__ import annotations

from datetime import datetime
from typing import List, Literal, Optional

import matplotlib.pyplot as plt
import numpy as np

from .satellite_image import SatelliteImage
from .utils import generate_tiles_borders


class SegmentationLabeledSatelliteImage:
    """
    Class for satellite images with a semantic segmentation label.
    The segmentation label is a 0-1 mask marking the presence of
    a building on each pixel.
    TODO: generalize to n classes ?
    """

    def __init__(
        self,
        satellite_image: SatelliteImage,
        label: np.array,
        source: Optional[Literal["RIL", "BDTOPO"]] = None,
        labeling_date: Optional[datetime] = None,
    ):
        """
        Constructor.

        Args:
            satellite_image (SatelliteImage): Satellite Image.
            label (np.array): Segmentation mask.
            source (Optional[Literal["RIL", "BDTOPO"]]): Labeling source.
            labeling_date (Optional[datetime]): Date of labeling data.
        """
        if not np.all(np.isin(label, [0, 1])):
            raise ValueError("Label has values outside of 0 and 1.")

        self.satellite_image = satellite_image
        self.label = label
        self.source = source
        self.labeling_date = labeling_date

    def split(self, tile_length: int) -> List[SegmentationLabeledSatelliteImage]:
        """
        Split the SegmentationLabeledSatelliteImage into labeled
        tiles of dimension (`tile_length` x `tile_length`).

        Args:
            tile_length (int): Dimension of tiles

        Returns:
            List[SegmentationLabeledSatelliteImage]: Labeled tiles.
        """
        # Split satellite image
        tiles = self.satellite_image.split(tile_length=tile_length)

        # Split label
        height = self.satellite_image.array.shape[1]
        width = self.satellite_image.array.shape[2]

        indices = generate_tiles_borders(height, width, tile_length)
        label_tiles = [
            self.label[rows[0] : rows[1], cols[0] : cols[1]]  # noqa: E203
            for rows, cols in indices
        ]

        labeled_tiles = [
            SegmentationLabeledSatelliteImage(
                image, label, self.source, self.labeling_date
            )
            for image, label in zip(tiles, label_tiles)
        ]

        return labeled_tiles

    def plot(self, bands_indices: List[int], alpha: float = 0.3):
        """
        Plot a subset of bands of the satellite image and its
        corresponding labels on the same plot.

        Args:
            bands_indices (List): List of indices of bands to plot.
                The indices should be integers between 0 and the
                number of bands - 1.
            alpha (float, optional): The transparency of the label
                image when overlaid on the satellite image. A value of
                0 means fully transparent and a value of 1 means fully
                opaque. The default value is 0.3.
        """
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.imshow(
            np.transpose(self.satellite_image.array, (1, 2, 0))[:, :, bands_indices]
        )
        ax.imshow(self.label, alpha=alpha)
        plt.xticks([])
        plt.yticks([])

        return plt.gcf()

    def plot_label_next_to_image(self, bands_indices: List[int]):
        """
        Plot a subset of bands from a satellite image and its
        corresponding label on the side.

        Args:
            bands_indices (List[int]): List of indices of bands to plot.
                The indices should be integers between 0 and the
                number of bands - 1.
        """
        label = np.zeros((*self.label.shape, 3))
        label[self.label == 1, :] = [255, 255, 255]
        label = label.astype(np.uint8)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 10))
        ax1.imshow(
            np.transpose(self.satellite_image.array, (1, 2, 0))[:, :, bands_indices]
        )
        ax1.axis("off")
        ax2.imshow(label)
        plt.xticks([])
        plt.yticks([])

        return plt.gcf()
