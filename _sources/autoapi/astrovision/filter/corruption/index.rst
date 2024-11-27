astrovision.filter.corruption
=============================

.. py:module:: astrovision.filter.corruption

.. autoapi-nested-parse::

   Filtering functions.



Functions
---------

.. autoapisummary::

   astrovision.filter.corruption.is_corrupted
   astrovision.filter.corruption.filter_corrupted


Module Contents
---------------

.. py:function:: is_corrupted(image: astrovision.data.SatelliteImage, black_value_threshold: int = 25, black_area_threshold: float = 0.5) -> bool

   Check if image is corrupted.

   Args:
       image (SatelliteImage): Satellite image.
       black_value_threshold (int): The intensity threshold to consider
           a pixel as black. Pixels with intensity values less than
           this threshold are considered black. Default is 100.
       black_area_threshold (float): The threshold for the proportion
           of black pixels in the image. If the ratio of black pixels
           exceeds this threshold, the function returns True. Default is 0.5.

   Returns:
       bool: True if image is corrupted, False otherwise.


.. py:function:: filter_corrupted(satellite_images: List[astrovision.data.SatelliteImage], black_value_threshold: int = 25, black_area_threshold: float = 0.5) -> List[astrovision.data.SatelliteImage]

   Filter out corrupted images.

   Args:
       satellite_images (List[SatelliteImage]): List of satellite images.
   Returns:
       List[SatelliteImage]: List of satellite images without corrupted images.


