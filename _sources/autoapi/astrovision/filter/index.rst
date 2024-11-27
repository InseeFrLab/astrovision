astrovision.filter
==================

.. py:module:: astrovision.filter

.. autoapi-nested-parse::

   Filter module



Submodules
----------

.. toctree::
   :maxdepth: 1

   /autoapi/astrovision/filter/bounds/index
   /autoapi/astrovision/filter/clouds/index
   /autoapi/astrovision/filter/corruption/index


Functions
---------

.. autoapisummary::

   astrovision.filter.filter_corrupted
   astrovision.filter.filter_oob
   astrovision.filter.filter_cloudy


Package Contents
----------------

.. py:function:: filter_corrupted(satellite_images: List[astrovision.data.SatelliteImage], black_value_threshold: int = 25, black_area_threshold: float = 0.5) -> List[astrovision.data.SatelliteImage]

   Filter out corrupted images.

   Args:
       satellite_images (List[SatelliteImage]): List of satellite images.
   Returns:
       List[SatelliteImage]: List of satellite images without corrupted images.


.. py:function:: filter_oob(satellite_images: List[astrovision.data.SatelliteImage], polygon_geometry: shapely.geometry.Polygon, crs: str) -> List[astrovision.data.SatelliteImage]

   Filter out images that are not within the bounds of a box.

   Args:
       satellite_images (List[SatelliteImage]): List of satellite images.
       polygon_geometry (Polygon): Polygon.
       crs (str): EPSG of the bounds.

   Returns:
       List[SatelliteImage]: List of satellite images within the bounds of the box.


.. py:function:: filter_cloudy(satellite_images: List[astrovision.data.SatelliteImage], cloud_masks: List[numpy.array], cloud_threshold: float = 0.5)

   Filter out cloudy images.


