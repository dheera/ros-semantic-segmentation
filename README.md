# ros-road-segmentation

ROS package to segment the driveable area of a road. Agnostic to model and deep learning framework.

One TensorFlow (1.13) based sample model is provided. You can follow the example to add models using other architectures or frameworks.

* **mnv2_bdd100k_driveable_513** -- Deeplab V3+ on a MobileNet v2 backbone, trained on BDD100K driveable area, 513x513 input size.

![screenshot](/screenshot.gif?raw=true "screenshot")

## Parameters:

* **model** (string) -- name of the model to use. Defaults to "mnv2_bdd100k_driveable_321".
* **rate** (float) -- the maximum frame rate to run inferences. Default to 30.0. Note that if your system is too slow, it will run at the maximum speed possible while dropping frames.
* **topic_image** (string) -- topic to listen for images. Defaults to "image_raw".
* **topic_semantic** (string) -- topic to output semantic predictions. Defaults to "semantic". Outputs a mono8 image indicating semantic classes at each pixel.
* **topic_semantic_color** (string) -- topic to output a colored RGB version of the semantic predictions for visualization purposes. Defaults to "semantic_color". Outputs a rgb8 image.

When the node is initialized, it will set an additional ROS parameter **semantic_categories** as is defined in the chose model. This parameter can be read by other nodes to know which IDs correspond to which classes.

## Subscribers:

* **image_raw** (sensor_msgs/Image)

## Publishers:

* **semantic** (sensor_msgs/Image)
* **semantic_color** (sensor_msgs/Image)

## Disclaimer

This is not intended to be used for production autonomous vehicles. This is provided "as-is" for educational purposes. I am not liable for any damage or injury that may result from the use of this software.
