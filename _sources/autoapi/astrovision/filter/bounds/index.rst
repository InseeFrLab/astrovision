astrovision.filter.bounds
=========================

.. py:module:: astrovision.filter.bounds

.. autoapi-nested-parse::

   Filter out of bounds images.



Functions
---------

.. autoapisummary::

   astrovision.filter.bounds.filter_oob


Module Contents
---------------

.. py:function:: filter_oob(satellite_images: List[astrovision.data.SatelliteImage], polygon_geometry: shapely.geometry.Polygon, crs: str) -> List[astrovision.data.SatelliteImage]

   Filter out images that are not within the bounds of a box.

   Args:
       satellite_images (List[SatelliteImage]): List of satellite images.
       polygon_geometry (Polygon): Polygon.
       crs (str): EPSG of the bounds.

   Returns:
       List[SatelliteImage]: List of satellite images within the bounds of the box.


