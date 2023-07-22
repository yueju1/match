import rclpy
from rclpy.node import Node
from control_msgs.msg import JointTrajectoryControllerState
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import array
from rclpy.action import ActionClient
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint
from builtin_interfaces.msg import Duration
import time
from ruamel.yaml import YAML
import math
from circle_fit import taubinSVD
import numpy as np                #  folge 
import inspect
import traceback

class Imag(Node):

    # if asd.ImageSubscriber().ok == 1:

    #     print(s.AutoCalibration().m)
    def __init__(self):
        #这里面的不报位置吗     
        super().__init__('image_detecn')
        self.declare_parameter('asd',1)
        self.br = CvBridge()
        self.sub = self.create_subscription(Image,
                    '/Cam2/image_raw',
                    self.detection_callback,
                    10)
    def detection_callback(self,data):
        im = self.br.imgmsg_to_cv2(data)
        cv2.namedWindow('ellip',0)
        cv2.resizeWindow('ellip',1000,1000)
        cv2.imshow("ellip", im)
        cv2.waitKey(1)
def main():
    rclpy.init()
    image_subscriber = Imag()

    rclpy.spin(image_subscriber)
    image_subscriber.destroy_node()
    rclpy.shutdown()
 
if __name__ == "__main__":
    main()