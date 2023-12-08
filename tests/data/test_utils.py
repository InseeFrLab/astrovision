"""
Tests for astrovision/data/utils.py
"""
from astrovision.data.utils import (
    generate_tiles_borders,
    get_bounds_for_tile,
    get_transform_for_tile,
)
from collections import Counter


def test_generate_tiles_borders():
    height = 2
    width = 2
    tile_length = 1
    tiles = generate_tiles_borders(height, width, tile_length)

    awaited_tiles = [
        ((1, 2), (1, 2)),
        ((0, 1), (0, 1)),
        ((0, 1), (1, 2)),
        ((1, 2), (0, 1)),
    ]
    assert Counter(tiles) == Counter(awaited_tiles)


def test_generate_tiles_borders_overlap():
    height = 4
    width = 3
    tile_length = 2
    tiles = generate_tiles_borders(height, width, tile_length)

    awaited_tiles = [
        ((0, 2), (0, 2)),
        ((2, 4), (0, 2)),
        ((0, 2), (1, 3)),
        ((2, 4), (1, 3)),
    ]
    assert Counter(tiles) == Counter(awaited_tiles)


def test_generate_tiles_borders_large_image():
    height = 6
    width = 4
    tile_length = 2
    tiles = generate_tiles_borders(height, width, tile_length)

    awaited_tiles = [
        ((0, 2), (0, 2)),
        ((2, 4), (0, 2)),
        ((4, 6), (0, 2)),
        ((0, 2), (2, 4)),
        ((2, 4), (2, 4)),
        ((4, 6), (2, 4)),
    ]
    assert Counter(tiles) == Counter(awaited_tiles)


def test_get_bounds_for_tile():
    transform = (1, 1, 0, 5, 1, 0)
    row_indices = (1, 2)
    col_indices = (0, 1)
    bounds = get_bounds_for_tile(transform, row_indices, col_indices)

    awaited_bounds = (1, 7, 2, 6)
    assert bounds == awaited_bounds


def test_get_transform_for_tile():
    transform = (1, 1, 0, 1, 1, 0)
    col = 2
    row = 2

    tile_transform = get_transform_for_tile(transform, row, col)
    awaited_tile_transform = (3, 1, 0, 3, 1, 0)
    assert tile_transform == awaited_tile_transform
