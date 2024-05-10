from azureKinect import azureKinect
import cv2
import numpy as np
import open3d as o3d
from dataCollector import DataCollector
import argparse

arg = argparse.ArgumentParser("An Azure Kinect Demo")
arg.add_argument("-d", "--deviceID", type=int, nargs='+',
                 help="Device ID of Azure Kinect", default=[0])
arg.add_argument("-s", "--save", type=str,
                 help="Save data to directory", default="./metadata/")
args = vars(arg.parse_args())

deviceID = args['deviceID']

kinects = []
pointcloud = [None]*len(deviceID)
image = [None]*len(deviceID)
save = DataCollector(len(deviceID), root_dir=args['save'])

for id in deviceID:
    kinects.append(azureKinect(id))
print(f"Device {kinects} is connected.")


kinect_open = True
while kinect_open:
    for i, kinect in enumerate(kinects):
        kinect.update()
        ret_pc, pointcloud[i] = kinect.tf_point_cloud()
        ret_rgb, image[i] = kinect.color(rgb=False)
        if ret_pc and ret_rgb:
            img = image[i].copy()
            cv2.putText(img, f"{save.counter} data(s) saved", (50, 50),
                        cv2.FONT_HERSHEY_COMPLEX, 1.0, (255, 70, 70), 2)
            cv2.imshow(f"Color Image {kinect.ID}", img)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('s') or key == ord('S') or key == 32 or key == 13:
                save(images=image, pointclouds=pointcloud,
                     colorMerged=azureKinect.ordered_color)
            if key == 27 or key == ord('Q') or key == ord('q'):
                kinect_open = False

cv2.destroyAllWindows()
for kinect in kinects:
    kinect.close()
