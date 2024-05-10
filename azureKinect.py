import pykinect_azure as pykinect
import numpy as np


class azureKinect:
    # Initialize the library, if the library is not found, add the library path as argument
    def __init__(self, idx=0):
        pykinect.initialize_libraries()

        # Modify camera configuration
        device_config = pykinect.default_configuration
        device_config.camera_fps = pykinect.K4A_FRAMES_PER_SECOND_15
        device_config.color_format = pykinect.K4A_IMAGE_FORMAT_COLOR_BGRA32
        device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_1080P
        device_config.depth_mode = pykinect.K4A_DEPTH_MODE_NFOV_UNBINNED

        self.config = device_config
        self.ID = idx
        self.device = pykinect.start_device(
            device_index=idx, config=device_config)
        self.capture = None

    def update(self):
        self.capture = self.device.update()

    def point_cloud(self):
        ret, point_cloud = self.capture.get_pointcloud()
        if ret:
            return ret, point_cloud*[0.001, -0.001, -0.001]
        else:
            return ret, None

    def color(self, rgb=True):
        ret, color_image = self.capture.get_color_image()
        if ret:
            if rgb:
                color_image = color_image[:, :, 2::-1]
            else:
                color_image = color_image[:, :, 0:3]
            return ret, color_image
        else:
            return ret, None

    def depth(self):
        ret, depth_image = self.capture.get_depth_image()
        if ret:
            return ret, depth_image/1000.0
        else:
            return ret, None

    def ir(self):
        ret, ir_image = self.capture.get_ir_image()
        return ret, ir_image

    def tf_point_cloud(self):
        ret, transformed_point_cloud = self.capture.get_transformed_pointcloud()
        if ret:
            return ret, transformed_point_cloud*[0.001, -0.001, -0.001]
        else:
            return ret, None

    def tf_color(self, rgb=True):
        ret, transformed_color_image = self.capture.get_transformed_color_image()
        if ret:
            if rgb:
                color_image = color_image[:, :, 2::-1]
            else:
                color_image = color_image[:, :, 0:3]
            return ret, color_image
        else:
            return ret, None

    def tf_depth(self):
        ret, transformed_depth_image = self.capture.get_transformed_depth_image()
        if ret:
            return ret, transformed_depth_image/1000.0
        else:
            return ret, None

    def close(self):
        self.device.close()

    def start(self):
        self.device.start()

    def is_opened(self):
        return self.device.is_valid() is not None

    @staticmethod
    def ordered_color(img):
        return img.reshape(-1, 3)
