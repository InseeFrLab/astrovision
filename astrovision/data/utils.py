"""
Util functions for the data module.
"""
from typing import List, Tuple
import numpy as np


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
    transform: Tuple, row_indices: Tuple, col_indices: Tuple
) -> Tuple:
    """
    Given an transformation of a satellite image, and indices for a
    tile's row and column, returns the bounding coordinates (left, bottom,
    right, top) of the tile.

    Args:
        transform (Tuple): An affine transformation
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

    left, bottom = tuple(transform[5] * np.array([col_min, row_max]) + np.array([transform[0], transform[3]]))
    right, top = tuple(transform[1] * np.array([col_max, row_min]) + np.array([transform[0], transform[3]]))
    return (left, bottom, right, top)


def get_transform_for_tile(transform: Tuple, row_off: int, col_off: int) -> Tuple:
    """
    Compute the transform matrix of a tile.

    Args:
        transform (Affine): An affine transform matrix.
        row_off (int): Minimum row index of the tile.
        col_off (int): Minimum column index of the tile.

    Returns:
        Tuple: The transform matrix for the given tile.
    """

    transform = list(transform)
    transform[3] = transform[3] + transform[5] * row_off
    transform[0] = transform[0] + transform[1] * col_off
    return tuple(transform)
