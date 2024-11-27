astrovision.data.utils
======================

.. py:module:: astrovision.data.utils

.. autoapi-nested-parse::

   Util functions for the data module.



Functions
---------

.. autoapisummary::

   astrovision.data.utils.generate_tiles_borders
   astrovision.data.utils.get_bounds_for_tile
   astrovision.data.utils.get_transform_for_tile


Module Contents
---------------

.. py:function:: generate_tiles_borders(height: int, width: int, tile_length: int) -> List

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


.. py:function:: get_bounds_for_tile(transform: affine.Affine, row_indices: Tuple, col_indices: Tuple) -> Tuple

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


.. py:function:: get_transform_for_tile(transform: affine.Affine, row_off: int, col_off: int) -> affine.Affine

   Compute the transform matrix of a tile.

   Args:
       transform (Affine): An affine transform matrix.
       row_off (int): Minimum row index of the tile.
       col_off (int): Minimum column index of the tile.

   Returns:
       Affine: The transform matrix for the given tile.


