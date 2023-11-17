"""
Tests for astrovision/data/utils.py
"""
from astrovision.data.utils import generate_tiles_borders
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
