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
import sys
 #试一下加不加中值滤波的区别 椒盐噪声    先搞destroy_node 然后看下yaml
# 程序考虑一下顺时针逆时针，想下之前想到的关于顺逆时针的东西。会转出去吗，如果图缩放比例的话
 #也许不需要很复杂， 可能可以通过: 知道图片中 现实点和未来点之前的关系，来求出实际中未来点的位置(也许要用坐标转换)。
   
#     add conditions
class AutoCalibration(Node):
    
    def __init__(self):
        #这里面的不报位置吗     
        super().__init__('image_detection')
        # try self.sub
            # if except ...
            #        ...shutdown
            # ...
        
        
        print(Parameter)
        self.n = 0
            
        # self.sub = self.create_subscription(JointTrajectoryControllerState,
        #                                      '/pm_robot_xyz_axis_controller/state',
        #                                      self.state_callback,
        #                                      10)
        self.sub = self.create_subscription(JointTrajectoryControllerState,
                                             '/joint_trajectory_controller/state',
                                             self.state_callback,
                                             10)
        
        #  self.subscription  # prevent unused variable warning ?
        
        # self.action_client = ActionClient(self,FollowJointTrajectory,
        #                           '/joint_trajectory_controller/follow_joint_trajectory')
        # self.action_client = ActionClient(self,FollowJointTrajectory,
        #                           '/pm_robot_xyz_axis_controller/follow_joint_trajectory')
        
        self.posit = [-0.359, -0.0458, -0.051544, 6.4]
        #print(self.Parameter[1])
    def state_callback(self, msg):
        #print(self.Parameter[1])
         
        # if msg.desired.positions == array.array('d',[-0.359, -0.0458, 0.03, 0.0]):
           
            # self.sub = self.create_subscription(Image,
            #         '/Camera_Bottom_View/pylon_ros2_camera_node/image_raw',
            #         self.detection_callback,
            #         10)
            # self.sub = self.create_subscription(Image,
            #         '/Cam2/image_raw',
            #         self.detection_callback,
            #         10)
        print(msg.desired.positions.tolist()[3])
        for i in range(len(msg.actual.positions)):
            
            if msg.actual.positions[i] > self.posit[i]-0.001 and msg.actual.positions[i] < self.posit[i]+0.001:
            
                if self.n < i:
                    self.n += 1
                #print(123)
                #continue
                #print(self.n)
        
        if self.n == 3:
            print('gogogo')
        
        
        
        # if self.n == 1:
        #     print(123)





def main():
    # global Parameter
    
    # Parameter = []
    # global oad, asd
    # asd = [5,5,5]
    # oad = [1,2,3]
    rclpy.init()
    
    # image_subscriber = AutoCalibration()
    # rclpy.spin(image_subscriber)
    #future = image_subscriber.rotate_action([-0.7, -0.0458, -0.026791, 1.08]) 
    
    rclpy.spin(AutoCalibration())

    rclpy.shutdown()
    
if __name__ == "__main__":
    
    # mode =input('Please select the operating mode: \n1: Calibration of the realistic equipment\n2: Calibration in simulation\n')
    
    # if mode == 1:
    mode =input('Please select the operating mode: \n1: Calibration of the realistic equipment\n2: Calibration in simulation\n')

    Para_real = ('/pm_robot_xyz_axis_controller/state',
                 '/pm_robot_xyz_axis_controller/follow_joint_trajectory',
                 '/Camera_Bottom_View/pylon_ros2_camera_node/image_raw',
                 [-0.359, -0.0458, 0.03, 0.0],
                 [-0.359, -0.0458, 0.03, -0.00008],
                 [-0.00008])
    
    Para_sim = ('/joint_trajectory_controller/state',
                '/joint_trajectory_controller/follow_joint_trajectory',
                '/Cam2/image_raw',
                [-0.359, -0.0458, -0.051544, 0.0],
                [-0.359, -0.0458, -0.051544, 6.4],
                [6.4])
  
    if mode == '1':
        Parameter = Para_real
        
    if mode == '2':
        Parameter = Para_sim
    
    main()
