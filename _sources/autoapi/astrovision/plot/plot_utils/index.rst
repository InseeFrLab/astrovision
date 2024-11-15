astrovision.plot.plot_utils
===========================

.. py:module:: astrovision.plot.plot_utils

.. autoapi-nested-parse::

   Utility functions for plotting.



Functions
---------

.. autoapisummary::

   astrovision.plot.plot_utils.make_mosaic
   astrovision.plot.plot_utils.make_mosaic_si
   astrovision.plot.plot_utils.make_mosaic_lsi
   astrovision.plot.plot_utils.plot_images
   astrovision.plot.plot_utils.plot_images_with_segmentation_label
   astrovision.plot.plot_utils.plot_images_with_classification_label
   astrovision.plot.plot_utils.plot_images_with_detection_label


Module Contents
---------------

.. py:function:: make_mosaic(images: List[Union[astrovision.data.SatelliteImage, astrovision.data.SegmentationLabeledSatelliteImage]], bands_indices: List[int])

   Creates a mosaic image from a list of satellite images.

   Args:
       images (List[Union[SatelliteImage, SegmentationLabeledSatelliteImage]]):
           A list of satellite images to be used for creating the mosaic.
       bands_indices (List[int]):
           A list of band indices to be used for creating the mosaic.

   Returns:
       The mosaic image created from the input images.

   Raises:
       ValueError: If the image type is not supported.



.. py:function:: make_mosaic_si(satellite_images: List[astrovision.data.SatelliteImage], bands_indices: List[int]) -> astrovision.data.SatelliteImage

   Create a mosaic from satellite images.

   Args:
       satellite_images (List[SatelliteImage]): Images.
       bands_indices (List[int]): Indices of bands to include in the mosaic.

   Returns:
       SatelliteImage: Mosaic of satellite images.


.. py:function:: make_mosaic_lsi(labelled_satellite_images: List[astrovision.data.SegmentationLabeledSatelliteImage], bands_indices: List[int]) -> astrovision.data.SegmentationLabeledSatelliteImage

   Create a mosaic from labeled satellite images.

   Args:
       labelled_satellite_images (List[SegmentationLabeledSatelliteImage]): Labeled images.
       bands_indices (List[int]): Indices of bands to include in the mosaic.

   Returns:
       SegmentationLabeledSatelliteImage: Mosaic of satellite images and labels.


.. py:function:: plot_images(satellite_images: List[astrovision.data.SatelliteImage], bands_indices: List[int])

   Plot satellite images.

   Args:
       satellite_images (List[SatelliteImage]): Images.
       bands_indices (List[int]): Indices of bands to plot.


.. py:function:: plot_images_with_segmentation_label(labeled_satellite_images: List[astrovision.data.SegmentationLabeledSatelliteImage], bands_indices: List[int], overlay: bool = True)

   Plot satellite images with segmentation labels.

   Args:
       labeled_satellite_images (List[ClassificationLabeledSatelliteImage]):
           Images with segmentation label.
       bands_indices (List[int]): Indices of bands to plot.
       overlay (bool): Whether to overlay segmentation label on top
           of satellite image.


.. py:function:: plot_images_with_classification_label(labeled_satellite_images: List[astrovision.data.ClassificationLabeledSatelliteImage], bands_indices: List[int], overlay: bool = True)

   Plot satellite images with classification labels.

   Args:
       labeled_satellite_images (List[ClassificationLabeledSatelliteImage]):
           Images with classification labels.
       bands_indices (List[int]): Indices of bands to plot.
       overlay (bool): Whether to overlay segmentation label on top
           of satellite image.


.. py:function:: plot_images_with_detection_label(labeled_satellite_images: List[astrovision.data.DetectionLabeledSatelliteImage], bands_indices: List[int], overlay: bool = True)

   Plot satellite images with detection labels.

   Args:
       labeled_satellite_images (List[DetectionLabeledSatelliteImage]): Images with
           detection labels.
       bands_indices (List[int]): Indices of bands to plot.
       overlay (bool, optional): Whether to overlay segmentation label on top.
           Defaults to True.


