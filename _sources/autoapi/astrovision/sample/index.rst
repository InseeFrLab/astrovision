astrovision.sample
==================

.. py:module:: astrovision.sample

.. autoapi-nested-parse::

   Sample module.



Submodules
----------

.. toctree::
   :maxdepth: 1

   /autoapi/astrovision/sample/sample/index


Functions
---------

.. autoapisummary::

   astrovision.sample.compute_distance_to_point
   astrovision.sample.is_within_distance
   astrovision.sample.sample_around_coordinates


Package Contents
----------------

.. py:function:: compute_distance_to_point(satellite_image: astrovision.data.SatelliteImage, coordinates: List[float], crs: str = 'EPSG:4326') -> float

   Return distance between the centroid of a satellite image
   and a point with coordinates `coordinates`.

   Args:
       satellite_image (SatelliteImage): Satellite image.
       coordinates (List[float]): Coordinates of the point.
       crs (str): EPSG of coordinates. Defaults to "EPSG:4326".

   Returns:
       float: Distance in kilometers.


.. py:function:: is_within_distance(satellite_image: astrovision.data.SatelliteImage, distance: float, coordinates: List[float], crs: str = 'EPSG:4326') -> bool

   Return True if the centroid of a satellite image is within distance
   `distance` of a point with coordinates `coordinates`.

   Args:
       satellite_image (SatelliteImage): Satellite image.
       distance (float): Distance in kilometers.
       coordinates (List[float]): Coordinates of the point.
       crs (str): EPSG. Defaults to "EPSG:4326".

   Returns:
       bool: True if image is within distance.


.. py:function:: sample_around_coordinates(satellite_images: List[astrovision.data.SatelliteImage], distance: float, coordinates: List[float], crs: str = 'EPSG:4326') -> Tuple[List[astrovision.data.SatelliteImage]]

   Sample satellite images which are within a distance
   `distance` from a point with coordinates `coordinates`.

   Args:
       satellite_image (SatelliteImage): Satellite image.
       distance (float): Distance in kilometers.
       coordinates (List[float]): Coordinates of the point.
       crs (str): EPSG. Defaults to "EPSG:4326".

   Returns:
       Tuple[List[SatelliteImage]]: Tuple containing two lists,
           the first containing the images which are within the
           given distance of the specified point and the second
           containing the others.


