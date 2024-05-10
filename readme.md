# Simple Azure Kinect Demo

***This project is based on the [`pyKinectAzure`](https://github.com/ibaiGorordo/pyKinectAzure)***, which I found is still a little bit difficult to handle for beginners, since users have to interact with other class like `k4a.device` and `k4a.capture`. I wrap the code into a simple and easy-to-use interface, and provide a simple demo to show how to use the Azure Kinect device.

In this project, I create a `AzureKinect` class to handle the Azure Kinect device. Image Prosessing methods like getting the depth and color image is provided, while leaving imu and other functions omitted, cause they have low priority for my daily work.

## Installation

1. Install the Azure Kinect SDK from [here](https://github.com/microsoft/Azure-Kinect-Sensor-SDK).
2. Install `pyAzureKinect` python package by running `pip install pyAzureKinect`.

***Note***: It's recommended to update the Azure Kinect SDK Firmware to the latest version. More details are shown in [azure-kinect-dk.pdf, 更新 Azure Kinect DK 固件](azure-kinect-dk.pdf)

## Usage

You can run `demo.py` to see a simple demo of how to use the `AzureKinect` class. Notice that you need to install all the required packages and it would be better to run the `Azure Kinect SDK` to check if the device is connected and working properly.

Open the `cmd` or `terminal`, navigate to the project directory, and run `python demo.py -d 0 1 -s "./data"`, which will start the demo with device id 0 and 1, and save the data to the folder `./data`. It's OK to leave input arguements empty to open the *0th* device and save data to the `./metadata/`.

You can press `s` to save RGB image and PointCloud, and `q`  or `esc` to exit the demo.

### Create an Instance of the AzureKinect Object
You can use the `AzureKinect` class easily by importing it and creating an instance:

```python
from azureKinect import azureKinect

# id stands for the device id, which can be 0, 1, 2, or 3. If there is only one device, you can leave it omitted.
kinect=azureKinect(id)
```

Next, all you need to do is to interact with object `kinect`, and it will handle everything.

### Get Images

Class `AzureKinect` provides several methods to get images from the Azure Kinect device. Open `azureKinect.py` to see all the methods. Here are some examples: 
> Note: method `update()` should always be call every time before you want to get a new status of the device.

```python
# Update the device status
kinect.update()
# Get the PointCloud data stored in NX3 ndarray in meters
ret_pc, pointcloud = kinect.tf_point_cloud()
# Get color image in BGR format
ret_rgb, image = kinect.color(rgb=False)
```

There are other methods like `depth()`, `ir()`, etc. to get different types of images.

### Create colored PointCloud

A RGB image is a MXNX3 ndarray, where M is the height, N is the width, and 3 represents the RGB channels, while PointCloud is a (MXN)X3 ndarray, where (MXN) is the number of points and 3 represents the XYZ coordinates. To create a colored PointCloud, You need to align the color image with the point cloud. You can use the `ordered_color` method to align the color image with the point cloud.

```python
# Align the color image with the point cloud
aligned_image = azureKinect.ordered_color(image)
# Then you can merge the aligned image and point cloud to get a 3D PointCloud
pc = o3d.geometry.PointCloud()
pc.points = o3d.utility.Vector3dVector(pointcloud)
pc.colors = o3d.utility.Vector3dVector(aligned_image)
```

> Notice: an original PointCloud is corresponding to the transformed RGB image, which means if you want to merge PointCloud and RGB image, you need to transform the PointCloud back to the original RGB image space, vise versa. You can get a transformed Image by using `tf_XX` methods provided by `AzureKinect` class.
