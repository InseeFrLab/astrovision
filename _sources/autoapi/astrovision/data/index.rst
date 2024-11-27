astrovision.data
================

.. py:module:: astrovision.data

.. autoapi-nested-parse::

   Data module.



Submodules
----------

.. toctree::
   :maxdepth: 1

   /autoapi/astrovision/data/constants/index
   /autoapi/astrovision/data/labeled_satellite_image/index
   /autoapi/astrovision/data/satellite_image/index
   /autoapi/astrovision/data/utils/index


Classes
-------

.. autoapisummary::

   astrovision.data.SatelliteImage
   astrovision.data.SegmentationLabeledSatelliteImage
   astrovision.data.DetectionLabeledSatelliteImage
   astrovision.data.ClassificationLabeledSatelliteImage


Package Contents
----------------

.. py:class:: SatelliteImage(array: numpy.array, crs: str, bounds: Tuple, transform: affine.Affine, dep: Optional[Literal[astrovision.data.constants.DEPARTMENTS_LIST]] = None, date: Optional[SatelliteImage.__init__.date] = None)

   Wrapper class for a satellite image.


   .. py:attribute:: array


   .. py:attribute:: crs


   .. py:attribute:: bounds


   .. py:attribute:: transform


   .. py:attribute:: dep


   .. py:attribute:: date


   .. py:method:: split(tile_length: int) -> List[SatelliteImage]

      Split the SatelliteImage into square tiles of side `tile_length`.

      Args:
          tile_length (int): Side of of tiles.

      Returns:
          List[SatelliteImage]: List of tiles.



   .. py:method:: to_tensor(bands_indices: Optional[List[int]] = None) -> torch.Tensor

      Return SatelliteImage array as a torch.Tensor.

      Args:
          bands_indices (List): List of indices of bands to plot.
              The indices should be integers between 0 and the
              number of bands - 1.

      Returns:
          torch.Tensor: Image tensor.



   .. py:method:: normalize(quantile: float = 0.97) -> SatelliteImage

      Normalize array values with min-max normalization after
      clipping at quantiles.

      Args:
          quantile (float): Normalize an array.

      Returns:
          SatelliteImage: Normalized image.



   .. py:method:: copy() -> SatelliteImage

      Deep copy a satellite image.

      Returns:
          SatelliteImage: Copied image.



   .. py:method:: plot(bands_indices: List[int])

      Plot a subset of bands from a 3D array as an image.

      Args:
          bands_indices (List[int]): List of indices of bands to plot.
              The indices should be integers between 0 and the
              number of bands - 1.



   .. py:method:: from_raster(file_path: str, dep: Optional[Literal[astrovision.data.constants.DEPARTMENTS_LIST]] = None, date: Optional[SatelliteImage.from_raster.date] = None, n_bands: int = 3, channels_first: bool = True, cast_to_float: bool = False) -> SatelliteImage
      :staticmethod:


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



   .. py:method:: to_raster(file_path: str) -> None

      Save a SatelliteImage to a raster file
      according to the raster type desired (.tif or .jp2).

      Args:
          file_path (str): File path.



   .. py:method:: to_raster_jp2(file_path: str)

      Save a SatelliteImage to a .jp2 raster file.

      Args:
          file_path (str): File path.



   .. py:method:: to_raster_tif(file_path: str) -> None

      Save a SatelliteImage to a .tif raster file.

      Args:
          file_path (str): File path.



   .. py:method:: intersects_box(box_bounds: Tuple, crs: str) -> bool

      Return True if image intersects a bounding box specified by
      `box_bounds` and a `crs`.

      Args:
          box_bounds (Tuple): Box bounds.
          crs (str): Projection system.

      Returns:
          bool: Boolean.



   .. py:method:: intersects_polygon(polygon_geometry: shapely.geometry.Polygon, crs: str) -> bool

      Return True if image intersects a polygon.

      Args:
          polygon_geometry (Polygon): Polygon geometry.
          crs (str): Projection system.

      Returns:
          bool: Boolean.



   .. py:method:: contains(coordinates: Tuple, crs: str) -> bool

      Return True if image contains a point specified by `coordinates`

      Args:
          coordinates (Tuple): Coordinates.
          crs (str): Projection system.

      Returns:
          bool: Boolean.



.. py:class:: SegmentationLabeledSatelliteImage(satellite_image: astrovision.data.satellite_image.SatelliteImage, label: numpy.array, source: Optional[Literal['RIL', 'BDTOPO']] = None, labeling_date: Optional[datetime.datetime] = None, logits: Optional[bool] = False)

   Class for satellite images with a semantic segmentation label.
   The segmentation label supports n classes.


   .. py:attribute:: satellite_image


   .. py:attribute:: label


   .. py:attribute:: source


   .. py:attribute:: labeling_date


   .. py:attribute:: logits


   .. py:method:: split(tile_length: int) -> List[SegmentationLabeledSatelliteImage]

      Split the SegmentationLabeledSatelliteImage into labeled
      tiles of dimension (`tile_length` x `tile_length`).

      Args:
          tile_length (int): Dimension of tiles

      Returns:
          List[SegmentationLabeledSatelliteImage]: Labeled tiles.



   .. py:method:: plot(bands_indices: List[int], alpha: float = 0.3, color_palette: List[str] = None, class_labels: Optional[List[str]] = None)

      Plot a subset of bands of the satellite image and its
      corresponding labels on the same plot.

      Args:
          bands_indices (List): List of indices of bands to plot.
              The indices should be integers between 0 and the
              number of bands - 1.
          alpha (float, optional): The transparency of the label
              image when overlaid on the satellite image. A value of
              0 means fully transparent and a value of 1 means fully
              opaque. The default value is 0.3.
          color_palette (list, optional): Color palette.
          class_labels (Optional[List[str]], optional): List of class labels for the legend.
              If not provided, it assumes a binary classification.



   .. py:method:: plot_label_next_to_image(bands_indices: List[int], color_palette: List[str] = None, class_labels: Optional[List[str]] = None)

      Plot a subset of bands from a satellite image and its
      corresponding label on the side.

      Args:
          bands_indices (List[int]): List of indices of bands to plot.
              The indices should be integers between 0 and the
              number of bands - 1.
          color_palette (list, optional): Color palette.
          class_labels (Optional[List[str]], optional): List of class labels for the legend.
              If not provided, it assumes a binary classification.



   .. py:method:: to_classification_labeled_image(aggregation_method: str = 'any') -> ClassificationLabeledSatelliteImage

      Return a ClassificationLabeledSatelliteImage.

      Args:
          aggregation_method (str): Method to aggregate pixel labels to a single class.
              Options: 'any' (default), 'majority', 'weighted'.

      Returns:
          ClassificationLabeledSatelliteImage: Image with a single class label.



.. py:class:: DetectionLabeledSatelliteImage(satellite_image: astrovision.data.satellite_image.SatelliteImage, label: List[Tuple[int]], source: Optional[Literal['RIL', 'BDTOPO']] = None, labeling_date: Optional[datetime.datetime] = None)

   Class for satellite images with an object detection label.
   The segmentation label is a List of box coordinates indicating
   the coordinates of buildings on the image.
   TODO: generalize to n classes ?


   .. py:attribute:: satellite_image


   .. py:attribute:: label


   .. py:attribute:: source


   .. py:attribute:: labeling_date


   .. py:method:: split(nfolds: int) -> List[DetectionLabeledSatelliteImage]
      :abstractmethod:


      Split the DetectionLabeledSatelliteImage into labeled
      tiles of dimension (`tile_length` x `tile_length`).

      Args:
          tile_length (int): Dimension of tiles

      Returns:
          List[DetectionLabeledSatelliteImage]: Labeled tiles.



   .. py:method:: plot(bands_indices: List[int])

      Plot a subset of bands from the satellite image with its
      corresponding label.

      Args:
          bands_indices (List[int]): List of indices of bands to plot.
              The indices should be integers between 0 and the
              number of bands - 1.



   .. py:method:: to_classification_labeled_image() -> ClassificationLabeledSatelliteImage

      Return a ClassificationLabeledSatelliteImage.



.. py:class:: ClassificationLabeledSatelliteImage(satellite_image: astrovision.data.satellite_image.SatelliteImage, label: int, source: Optional[Literal['RIL', 'BDTOPO']] = None, labeling_date: Optional[datetime.datetime] = None)

   Class for satellite images with 0-1 classification label.


   .. py:attribute:: satellite_image


   .. py:attribute:: label


   .. py:attribute:: source


   .. py:attribute:: labeling_date


   .. py:method:: plot(bands_indices: List[int], alpha: float = 0.2)

      Plot a subset of bands of the satellite image with a green
      or red overlay depending on whether it is labeled 1 or 0.

      Args:
          bands_indices (List): List of indices of bands to plot.
              The indices should be integers between 0 and the
              number of bands - 1.
          alpha (float, optional): The transparency of the label
              color when overlaid on the satellite image. A value of
              0 means fully transparent and a value of 1 means fully
              opaque. The default value is 0.2.



