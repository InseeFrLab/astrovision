"""
Classes representing satellite images labeled according
to a segmentation, a classification or an object detection
task.
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Literal, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw

from .satellite_image import SatelliteImage
from .utils import generate_tiles_borders

import matplotlib as mpl
from matplotlib.patches import Patch


class SegmentationLabeledSatelliteImage:
    """
    Class for satellite images with a semantic segmentation label.
    The segmentation label supports n classes.
    """

    def __init__(
        self,
        satellite_image: SatelliteImage,
        label: np.array,
        source: Optional[Literal["RIL", "BDTOPO"]] = None,
        labeling_date: Optional[datetime] = None,
        logits: Optional[bool] = False,
    ):
        """
        Constructor.

        Args:
            satellite_image (SatelliteImage): Satellite Image.
            label (np.array): Segmentation mask with class IDs (0 to n-1).
            source (Optional[Literal["RIL", "BDTOPO"]]): Labeling source.
            labeling_date (Optional[datetime]): Date of labeling data.
            logits (Optional[bool]): Whether label array is logits or class IDs
        """
        if not issubclass(label.dtype.type, np.integer) and not logits:
            raise ValueError("Label array must contain integer values for class IDs.")

        if not issubclass(label.dtype.type, np.float) and logits:
            raise ValueError("Label array must contain float values for logits.")

        self.satellite_image = satellite_image
        self.label = label
        self.source = source
        self.labeling_date = labeling_date
        self.logits = logits

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

    def plot(
        self,
        bands_indices: List[int],
        alpha: float = 0.3,
        color_palette: List[str] = None,
        class_labels: Optional[List[str]] = None,
    ):
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
            color_palette (list, optional): Color palette.
            class_labels (Optional[List[str]], optional): List of class labels for the legend.
                If not provided, it assumes a binary classification.
        """
        # Initialize the plot
        fig, ax = plt.subplots(figsize=(6, 6))

        # Plot the satellite image (adjusted for selected bands)
        ax.imshow(
            np.transpose(self.satellite_image.array, (1, 2, 0))[:, :, bands_indices]
        )

        # If class_labels is not provided, assume binary classification (two classes)
        if class_labels is None:
            ax.imshow(self.label, alpha=alpha)
        else:
            # Handle label overlay for multi-class case
            cmap = mpl.colors.ListedColormap(color_palette)
            # Handle multi-class case with legend
            # Create the color-mapped label for multi-class
            color_mapped_label = cmap(
                self.label
            )  # Converts class indices to RGBA values
            ax.imshow(color_mapped_label, alpha=alpha)  # Overlay the color-mapped mask

            # Create a legend for the classes
            legend_elements = [
                Patch(
                    facecolor=color_palette[i],
                    edgecolor="black",
                    label=f"{class_labels[i]}",
                )
                for i in range(len(class_labels))
            ]
            ax.legend(
                handles=legend_elements, loc="upper right", bbox_to_anchor=(1.41, 1)
            )

        # Turn off axis and show the plot
        ax.axis("off")

        return plt.gcf()

    def plot_label_next_to_image(
        self,
        bands_indices: List[int],
        color_palette: List[str] = None,
        class_labels: Optional[List[str]] = None,
    ):
        """
        Plot a subset of bands from a satellite image and its
        corresponding label on the side.

        Args:
            bands_indices (List[int]): List of indices of bands to plot.
                The indices should be integers between 0 and the
                number of bands - 1.
            color_palette (list, optional): Color palette.
            class_labels (Optional[List[str]], optional): List of class labels for the legend.
                If not provided, it assumes a binary classification.
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 10))
        ax1.imshow(
            np.transpose(self.satellite_image.array, (1, 2, 0))[:, :, bands_indices]
        )
        ax1.axis("off")

        # If class_labels is not provided, assume binary classification (two classes)
        if class_labels is None:
            label = np.zeros((*self.label.shape, 3))
            label[self.label == 1, :] = [255, 255, 255]
            label = label.astype(np.uint8)
            ax2.imshow(label)
        else:
            # Handle label overlay for multi-class case
            cmap = mpl.colors.ListedColormap(color_palette)
            # Handle multi-class case with legend
            # Create the color-mapped label for multi-class
            color_mapped_label = cmap(
                self.label
            )  # Converts class indices to RGBA values

            ax2.imshow(color_mapped_label)  # Overlay the color-mapped mask

            # Create a legend for the classes
            legend_elements = [
                Patch(
                    facecolor=color_palette[i],
                    edgecolor="black",
                    label=f"{class_labels[i]}",
                )
                for i in range(len(class_labels))
            ]
            ax2.legend(
                handles=legend_elements, loc="upper right", bbox_to_anchor=(1.54, 1)
            )

        ax2.axis("off")

        return plt.gcf()

    def to_classification_labeled_image(
        self, aggregation_method: str = "any"
    ) -> ClassificationLabeledSatelliteImage:
        """
        Return a ClassificationLabeledSatelliteImage.

        Args:
            aggregation_method (str): Method to aggregate pixel labels to a single class.
                Options: 'any' (default), 'majority', 'weighted'.

        Returns:
            ClassificationLabeledSatelliteImage: Image with a single class label.
        """
        if aggregation_method == "any":
            classification_label = int(np.any(self.label > 0))
        elif aggregation_method == "majority":
            unique, counts = np.unique(self.label, return_counts=True)
            classification_label = unique[np.argmax(counts)]
        elif aggregation_method == "weighted":
            unique, counts = np.unique(self.label, return_counts=True)
            total_pixels = self.label.size
            weights = counts / total_pixels
            classification_label = unique[np.argmax(weights)]
        else:
            raise ValueError("Invalid aggregation method.")

        return ClassificationLabeledSatelliteImage(
            satellite_image=self.satellite_image,
            label=classification_label,
            source=self.source,
            labeling_date=self.labeling_date,
        )


class DetectionLabeledSatelliteImage:
    """
    Class for satellite images with an object detection label.
    The segmentation label is a List of box coordinates indicating
    the coordinates of buildings on the image.
    TODO: generalize to n classes ?
    """

    def __init__(
        self,
        satellite_image: SatelliteImage,
        label: List[Tuple[int]],
        source: Optional[Literal["RIL", "BDTOPO"]] = None,
        labeling_date: Optional[datetime] = None,
    ):
        """
        Constructor.

        Args:
            satellite_image (SatelliteImage): Satellite image.
            label (List[Tuple[int]]): Object detection label
                with format (x0, y0, x1, y1).
            source (Optional[Literal["RIL", "BDTOPO"]]): Labeling source.
            labeling_date (Optional[datetime]): Date of labeling data.
        """
        _, width, height = satellite_image.array.shape
        for bounding_box in label:
            x0, y0, x1, y1 = bounding_box
            if (max(x0, x1) >= width) | (max(y0, y1) >= height):
                raise ValueError(
                    f"Bounding box {bounding_box} is not" f"contained in image."
                )

        self.satellite_image = satellite_image
        self.label = label
        self.source = source
        self.labeling_date = labeling_date

    def split(self, nfolds: int) -> List[DetectionLabeledSatelliteImage]:
        """
        Split the DetectionLabeledSatelliteImage into labeled
        tiles of dimension (`tile_length` x `tile_length`).

        Args:
            tile_length (int): Dimension of tiles

        Returns:
            List[DetectionLabeledSatelliteImage]: Labeled tiles.
        """
        raise NotImplementedError()

    def plot(self, bands_indices: List[int]):
        """
        Plot a subset of bands from the satellite image with its
        corresponding label.

        Args:
            bands_indices (List[int]): List of indices of bands to plot.
                The indices should be integers between 0 and the
                number of bands - 1.
        """
        # Array is supposed to be float [0, 1]
        image = Image.fromarray(
            np.transpose(np.uint8(self.satellite_image.array * 255), (1, 2, 0))[
                :, :, bands_indices
            ],
            mode="RGB",
        )
        # Drawing bounding boxes
        for x, y, xx, yy in self.label:
            c1 = (int(x), int(y))
            c2 = (int(xx), int(yy))
            draw = ImageDraw.Draw(image)
            draw.rectangle((c1, c2), width=2, outline="red")

        fig, ax = plt.subplots(figsize=(5, 5))
        ax.imshow(image)

        return plt.gcf()

    def to_classification_labeled_image(self) -> ClassificationLabeledSatelliteImage:
        """
        Return a ClassificationLabeledSatelliteImage.
        """
        if self.label:
            classification_label = 1
        else:
            classification_label = 0
        return ClassificationLabeledSatelliteImage(
            satellite_image=self.satellite_image,
            label=classification_label,
            source=self.source,
            labeling_date=self.labeling_date,
        )


class ClassificationLabeledSatelliteImage:
    """
    Class for satellite images with 0-1 classification label.
    """

    def __init__(
        self,
        satellite_image: SatelliteImage,
        label: int,
        source: Optional[Literal["RIL", "BDTOPO"]] = None,
        labeling_date: Optional[datetime] = None,
    ):
        """
        Constructor.

        Args:
            satellite_image (SatelliteImage): Satellite Image.
            label (int): Classification label.
            source (Optional[Literal["RIL", "BDTOPO"]]): Labeling source.
            labeling_date (Optional[datetime]): Date of labeling data.
        """
        if label not in [0, 1]:
            raise ValueError(f"Label must be 0 and 1, not {label}.")

        self.satellite_image = satellite_image
        self.label = label
        self.source = source
        self.labeling_date = labeling_date

    def plot(self, bands_indices: List[int], alpha: float = 0.2):
        """
        Plot a subset of bands of the satellite image with a green
        or red overlay depending on whether it is labeled 1 or 0.

        Args:
            bands_indices (List): List of indices of bands to plot.
                The indices should be integers between 0 and the
                number of bands - 1.
            alpha (float, optional): The transparency of the label
                color when overlaid on the satellite image. A value of
                0 means fully transparent and a value of 1 means fully
                opaque. The default value is 0.2.
        """
        if self.label == 1:
            color = "23c552"
        else:
            color = "f84f31"

        image_array = np.transpose(self.satellite_image.array, (1, 2, 0))[
            :, :, bands_indices
        ]

        # Green or red array
        rgb_list = [int(color[i : i + 2], 16) for i in (0, 2, 4)]  # noqa: E203
        color_array = np.ones_like(image_array)
        color_array = color_array * rgb_list

        fig, ax = plt.subplots(figsize=(5, 5))
        ax.imshow(image_array)
        ax.imshow(color_array, alpha=alpha)
        plt.xticks([])
        plt.yticks([])

        return plt.gcf()
