import time
from pathlib import Path
import open3d as o3d
import numpy as np
import cv2


class DataCollector:
    def __init__(self, num, root_dir='./data'):
        self.root = Path(root_dir)
        self.time = time.strftime('%y%m%d%H%M%S', time.localtime())
        self.counter = 0
        self.num = num
        self.sub_dirs = []
        for i in range(num):
            self.sub_dirs.append(self.root.joinpath(self.time, f"camera_{i}"))
            self.sub_dirs[-1].mkdir(parents=True, exist_ok=True)

    def __call__(self, images=None, pointclouds=None, colorMerged=None):
        if images is not None:
            for i, img in enumerate(images):
                self.save_images(img, self.sub_dirs[i])
        if pointclouds is not None:
            for i, pointcloud in enumerate(pointclouds):
                pc = o3d.geometry.PointCloud()
                pc.points = o3d.utility.Vector3dVector(pointcloud)
                if colorMerged is not None:
                    pc.colors = o3d.utility.Vector3dVector(
                        colorMerged(images[i][:, :, ::-1])/255.0)
                self.save_pointcloud(pc, self.sub_dirs[i])
        self.counter += 1

    def save_images(self, img, sub_dir):
        cv2.imwrite(str(sub_dir.joinpath(f"{self.counter}.png")), img)

    def save_pointcloud(self, pc, sub_dir):
        o3d.io.write_point_cloud(
            str(sub_dir.joinpath(f"{self.counter}.ply")), pc)

    def finish(self):
        if self.counter < self.num:
            pass
