"""
Util functions for the data module.
"""
from affine import Affine
from typing import List, Tuple
import rasterio


def generate_tiles_borders(height: int, width: int, tile_length: int) -> List:
    """
    Given the dimensions of an original image and a desired tile side length,
    this function returns a list of tuples, where each tuple contains the
    border indices of a tile that can be extracted from the original image.
    The function raises a ValueError if the size of the tile is larger than
    the size of the original image.

    Args:
        height (int): Height of the original image.
        width (int): Width of the original image.
        tile_length (int): Dimension of tiles.

    Returns:
        List: A list of tuples, where each tuple contains the border indices
            of a tile that can be extracted from the original image.
    """

    if (tile_length > height) | (tile_length > width):
        raise ValueError(
            "The size of the tile should be smaller"
            "than the size of the original image."
        )

    indices = [
        ((height - tile_length, height), (width - tile_length, width))
        if (x + tile_length > height) & (y + tile_length > width)
        else ((x, x + tile_length), (y, y + tile_length))
        if (x + tile_length <= height) & (y + tile_length <= width)
        else ((height - tile_length, height), (y, y + tile_length))
        if (x + tile_length > height) & (y + tile_length <= width)
        else ((x, x + tile_length), (width - tile_length, width))
        for x in range(0, height, tile_length)
        for y in range(0, width, tile_length)
    ]
    return indices


def get_bounds_for_tile(
    transform: Affine, row_indices: Tuple, col_indices: Tuple
) -> Tuple:
    """
    Given a transformation of a satellite image, and indices for a
    tile's row and column, returns the bounding coordinates (left, bottom,
    right, top) of the tile.

    Args:
        transform (Affine): An affine transformation
        row_indices (Tuple): A tuple containing the minimum and maximum
            indices for the tile's row.
        col_indices (Tuple): A tuple containing the minimum and maximum
            indices for the tile's column

    Returns:
        Tuple: A tuple containing the bounding coordinates
            (left, bottom, right, top) of the tile.
    """

    row_min = row_indices[0]
    row_max = row_indices[1]
    col_min = col_indices[0]
    col_max = col_indices[1]

    left, bottom = transform * (col_min, row_max)
    right, top = transform * (col_max, row_min)
    return rasterio.coords.BoundingBox(left, bottom, right, top)


def get_transform_for_tile(transform: Affine, row_off: int, col_off: int) -> Affine:
    """
    Compute the transform matrix of a tile.

    Args:
        transform (Affine): An affine transform matrix.
        row_off (int): Minimum row index of the tile.
        col_off (int): Minimum column index of the tile.

    Returns:
        Affine: The transform matrix for the given tile.
    """
    x, y = transform * (col_off, row_off)
    return Affine.translation(x - transform.c, y - transform.f) * transform
