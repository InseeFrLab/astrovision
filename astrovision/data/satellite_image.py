"""
Satellite image class.
"""
from __future__ import annotations

import os
from datetime import date
from typing import List, Literal, Optional, Tuple

from affine import Affine
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import rasterio
import rasterio.plot as rp
import torch
from osgeo import gdal

from .constants import DEPARTMENTS_LIST
from .utils import (
    generate_tiles_borders,
    get_bounds_for_tile,
    get_transform_for_tile,
)


class SatelliteImage:
    """
    Wrapper class for a satellite image.
    """

    def __init__(
        self,
        array: np.array,
        crs: str,
        bounds: Tuple,
        transform: Affine,
        dep: Optional[Literal[DEPARTMENTS_LIST]] = None,
        date: Optional[date] = None,
    ):
        """
        Constructor.

        Args:
            array (np.array): Image array. Assumes (C, H, W) format.
            crs (str): Coordinate Reference System.
            bounds (Tuple): Bounds for the satellite image.
            transform (Affine): Transform for the satellite image.
            dep (Optional[Literal[DEPARTMENTS_LIST]]): French département
                of the image. Defaults to None.
            date (Optional[date]): Date of the satellite image. Defaults
                to None.
        """
        self.array = array
        self.crs = crs
        self.bounds = bounds
        self.transform = transform
        self.dep = dep
        self.date = date

    def split(self, tile_length: int) -> List[SatelliteImage]:
        """
        Split the SatelliteImage into square tiles of side `tile_length`.

        Args:
            tile_length (int): Side of of tiles.

        Returns:
            List[SatelliteImage]: List of tiles.
        """
        height = self.array.shape[1]
        width = self.array.shape[2]

        indices = generate_tiles_borders(height, width, tile_length)

        tiles = [
            SatelliteImage(
                array=self.array[:, rows[0] : rows[1], cols[0] : cols[1]],  # noqa
                crs=self.crs,
                bounds=get_bounds_for_tile(self.transform, rows, cols),
                transform=get_transform_for_tile(self.transform, rows[0], cols[0]),
                dep=self.dep,
                date=self.date,
            )
            for rows, cols in indices
        ]

        return tiles

    def to_tensor(self, bands_indices: Optional[List[int]] = None) -> torch.Tensor:
        """
        Return SatelliteImage array as a torch.Tensor.

        Args:
            bands_indices (List): List of indices of bands to plot.
                The indices should be integers between 0 and the
                number of bands - 1.

        Returns:
            torch.Tensor: Image tensor.
        """
        if bands_indices is None:
            return torch.from_numpy(self.array)
        else:
            return torch.from_numpy(self.array[bands_indices, :, :])

    def normalize(self, quantile: float = 0.97) -> SatelliteImage:
        """
        Normalize array values with min-max normalization after
        clipping at quantiles.

        Args:
            quantile (float): Normalize an array.

        Returns:
            SatelliteImage: Normalized image.
        """
        if quantile < 0.5 or quantile > 1:
            raise ValueError(
                "Value of the `quantile` parameter must be between 0.5 and 1."
            )

        normalized_bands = [
            rp.adjust_band(
                np.clip(
                    self.array[i, :, :],
                    0,
                    np.quantile(self.array[i, :, :], quantile),
                )
            )
            for i in range(len(self.array))
        ]
        array = np.stack(normalized_bands)
        return SatelliteImage(
            array=array,
            crs=self.crs,
            bounds=self.bounds,
            transform=self.transform,
            dep=self.dep,
            date=self.date,
        )

    def copy(self) -> SatelliteImage:
        """
        Deep copy a satellite image.

        Returns:
            SatelliteImage: Copied image.
        """
        return SatelliteImage(
            array=self.array.copy(),
            crs=self.crs,
            bounds=self.bounds,
            transform=self.transform,
            dep=self.dep,
            date=self.date,
        )

    def plot(self, bands_indices: List[int]):
        """
        Plot a subset of bands from a 3D array as an image.

        Args:
            bands_indices (List[int]): List of indices of bands to plot.
                The indices should be integers between 0 and the
                number of bands - 1.
        """
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.imshow(np.transpose(self.array, (1, 2, 0))[:, :, bands_indices])
        plt.xticks([])
        plt.yticks([])
        plt.show()

        return plt.gcf()

    @staticmethod
    def from_raster(
        file_path: str,
        dep: Optional[Literal[DEPARTMENTS_LIST]] = None,
        date: Optional[date] = None,
        n_bands: int = 3,
        channels_first: bool = True,
        cast_to_float: bool = False,
    ) -> SatelliteImage:
        """
        Factory method to create a Satellite image from a raster file.

        Args:
            file_path (str): File path.
            dep (Optional[Literal[DEPARTMENTS_LIST]]): Département.
            date (Optional[date]): Date. Defaults to None.
            n_bands (int): Number of bands.
            channels_first (bool): True if channels should be moved
                to first axis.
            cast_to_float (bool): True to cast array to float.

        Returns:
            SatelliteImage: Satellite image.
        """
        ds = gdal.Open(file_path)
        array = ds.ReadAsArray()

        if not channels_first:
            array = np.transpose(array, [1, 2, 0])

        if cast_to_float:
            if np.issubdtype(array.dtype, np.integer):
                array = np.uint8(array)
                array = array.astype(float) / 255.0

        crs = ds.GetProjection()
        transform = ds.GetGeoTransform()
        bounds = (
            transform[0],  # left
            transform[3] + transform[5] * ds.RasterYSize,  # bottom
            transform[0] + transform[1] * ds.RasterXSize,  # right
            transform[3],  # top
        )
        transform = Affine.from_gdal(*transform)

        return SatelliteImage(
            array,
            crs,
            bounds,
            transform,
            dep,
            date,
        )

    def to_raster(
        self,
        file_path: str,
    ) -> None:
        """
        Save a SatelliteImage to a raster file
        according to the raster type desired (.tif or .jp2).

        Args:
            file_path (str): File path.
        """
        file_format = Path(file_path).suffix
        if file_format == ".jp2":
            self.to_raster_jp2(file_path)
        elif file_format == ".tif":
            self.to_raster_tif(file_path)
        else:
            raise ValueError(
                f"File format is {file_format} must " f'be either ".jp2" or ".tif".'
            )

    def to_raster_jp2(self, file_path: str):
        """
        Save a SatelliteImage to a .jp2 raster file.

        Args:
            file_path (str): File path.
        """
        data = self.array
        crs = self.crs
        transform = self.transform
        n_bands = len(data)

        # TODO: fix potential issue with the data type there.
        # For now this will only work properly if the numpy
        # array is uint16 ?
        metadata = {
            "dtype": "uint16",
            "count": n_bands,
            "width": data.shape[2],
            "height": data.shape[1],
            "crs": crs,
            "transform": transform,
            "driver": "JP2OpenJPEG",
            "compress": "jp2k",
            "interleave": "pixel",
        }

        dirname = os.path.dirname(file_path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        # Use Gdal here to remove rasterio dependency
        with rasterio.open(file_path, "w", **metadata) as dst:
            dst.write(data, indexes=np.arange(n_bands) + 1)

    def to_raster_tif(self, file_path: str) -> None:
        """
        Save a SatelliteImage to a .tif raster file.

        Args:
            file_path (str): File path.
        """
        transform = self.transform
        array = self.array
        crs = self.crs

        driver = gdal.GetDriverByName("GTiff")
        out_ds = driver.Create(
            file_path,
            array.shape[2],
            array.shape[1],
            array.shape[0],
            gdal.GDT_Float64,
        )
        out_ds.SetGeoTransform(
            [
                transform[2],
                transform[0],
                transform[1],
                transform[5],
                transform[3],
                transform[4],
            ]
        )
        out_ds.SetProjection(crs.to_wkt())

        for j in range(array.shape[0]):
            out_ds.GetRasterBand(j + 1).WriteArray(array[j, :, :])

        out_ds = None
        return
