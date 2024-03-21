:py:mod:`astrovision.data.labeled_satellite_image`
==================================================

.. py:module:: astrovision.data.labeled_satellite_image

.. autoapi-nested-parse::

   Classes representing satellite images labeled according
   to a segmentation, a classification or an object detection
   task.



Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   astrovision.data.labeled_satellite_image.SegmentationLabeledSatelliteImage
   astrovision.data.labeled_satellite_image.DetectionLabeledSatelliteImage
   astrovision.data.labeled_satellite_image.ClassificationLabeledSatelliteImage




.. py:class:: SegmentationLabeledSatelliteImage(satellite_image: astrovision.data.satellite_image.SatelliteImage, label: numpy.array, source: Optional[Literal[RIL, BDTOPO]] = None, labeling_date: Optional[datetime.datetime] = None)


   Class for satellite images with a semantic segmentation label.
   The segmentation label is a 0-1 mask marking the presence of
   a building on each pixel.
   TODO: generalize to n classes ?

   .. py:method:: split(tile_length: int) -> List[SegmentationLabeledSatelliteImage]

      Split the SegmentationLabeledSatelliteImage into labeled
      tiles of dimension (`tile_length` x `tile_length`).

      Args:
          tile_length (int): Dimension of tiles

      Returns:
          List[SegmentationLabeledSatelliteImage]: Labeled tiles.


   .. py:method:: plot(bands_indices: List[int], alpha: float = 0.3)

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


   .. py:method:: plot_label_next_to_image(bands_indices: List[int])

      Plot a subset of bands from a satellite image and its
      corresponding label on the side.

      Args:
          bands_indices (List[int]): List of indices of bands to plot.
              The indices should be integers between 0 and the
              number of bands - 1.


   .. py:method:: to_classification_labeled_image() -> ClassificationLabeledSatelliteImage

      Return a ClassificationLabeledSatelliteImage.



.. py:class:: DetectionLabeledSatelliteImage(satellite_image: astrovision.data.satellite_image.SatelliteImage, label: List[Tuple[int]], source: Optional[Literal[RIL, BDTOPO]] = None, labeling_date: Optional[datetime.datetime] = None)


   Class for satellite images with an object detection label.
   The segmentation label is a List of box coordinates indicating
   the coordinates of buildings on the image.
   TODO: generalize to n classes ?

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



.. py:class:: ClassificationLabeledSatelliteImage(satellite_image: astrovision.data.satellite_image.SatelliteImage, label: int, source: Optional[Literal[RIL, BDTOPO]] = None, labeling_date: Optional[datetime.datetime] = None)


   Class for satellite images with 0-1 classification label.

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



