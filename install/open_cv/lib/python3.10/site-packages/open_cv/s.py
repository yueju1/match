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

import numpy as np                #  folge 
import inspect
import sys
import asd
 #试一下加不加中值滤波的区别 椒盐噪声    先搞destroy_node 然后看下yaml
# 程序考虑一下顺时针逆时针，想下之前想到的关于顺逆时针的东西。会转出去吗，如果图缩放比例的话
 #也许不需要很复杂， 可能可以通过: 知道图片中 现实点和未来点之前的关系，来求出实际中未来点的位置(也许要用坐标转换)。
   
#     add conditions
class AutoCalibration(Node):
    
    def __init__(self):
        #这里面的不报位置吗     
        super().__init__('image_detection')
        # # try self.sub
        #     # if except ...
        #     #        ...shutdown
        #     # ...
        # self.m = 0
        # self.mode =input('Please select the operating self.self.mode: \n1: Calibration of the realistic equipment\n2: Calibration in simulation\n')
    
        # Para_real = ('/pm_robot_xyz_axis_controller/state',
        #             '/pm_robot_xyz_axis_controller/follow_joint_trajectory',
        #             '/Camera_Bottom_View/pylon_ros2_camera_node/image_raw',
        #             [-0.359, -0.0458, 0.03, 0.0],
        #             [-0.359, -0.0458, 0.03, -0.00008],
        #             [-0.00008])
        
        # Para_sim = ('/joint_trajectory_controller/state',
        #             '/joint_trajectory_controller/follow_joint_trajectory',
        #             '/Cam2/image_raw',
        #             [-0.359, -0.0458, -0.051544, 0.0],
        #             [-0.359, -0.0458, -0.051544, 6.4],
        #             [6.4])

        # if self.mode == '1':
        #     Parameter = Para_real
            
        # if self.mode == '2':
        #     Parameter = Para_sim
        
        # print(Parameter)
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
        #self.asd()
        if msg.desired.positions == array.array('d',[-0.359, -0.0458, -0.051544, 0.0]):
            print(123)
            image = AutoCalibration()
            print(222)
            image.destroy_node()
            print(111)
            rclpy.shutdown()
            print(456)
            rclpy.init()
            print(234)
            rclpy.spin_once(asdf())
            # self.sub = self.create_subscription(Image,
            #         '/Camera_Bottom_View/pylon_ros2_camera_node/image_raw',
            #         self.detection_callback,
            #         10)
            # self.sub = self.create_subscription(Image,
            #         '/Cam2/image_raw',
            #         self.detection_callback,
            #         10)
            # print(msg.desired.positions.tolist()[3])
        # for i in range(len(msg.actual.positions)):
            
        #     if msg.actual.positions[i] > self.posit[i]-0.001 and msg.actual.positions[i] < self.posit[i]+0.001:
            
        #         if self.n < i:
        #             self.n += 1
                #print(123)
                #continue
                #print(self.n)
        
        if self.n == 3:
            print('gogogo')
        
        
    # def asd(self):
    #     pixel = 0
        
    #     self.c = 34
    #     self.b =2022222222222222222222
    #     if self.mode == "1":
    #         self.d = self.b

    #     self.zxc()
    
    # def zxc(self):
    #     print()
    #     print(self.d)
class asdf(Node):
    
    def __init__(self):
        self.m = 0
        self.mode =input('Please select the operating self.self.mode: \n1: Calibration of the realistic equipment\n2: Calibration in simulation\n')
    
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

        if self.mode == '1':
            Parameter = Para_real
            
        if self.mode == '2':
            Parameter = Para_sim
        
        print(Parameter)
        #这里面的不报位置吗     
        super().__init__('image_detecn')
        self.reached_joint_number = 0
        self.action_client = ActionClient(self,FollowJointTrajectory,
                                  Parameter[1])
        print(000000000000000000000000000)
        self.sub2 = self.create_subscription(JointTrajectoryControllerState,Parameter[0],self.call_b2,10)
    def call_b2(self,mc):
        for i in range(len(mc.actual.positions)):
            
            if mc.desired.positions.tolist() == Parameter[3] and mc.actual.positions[i] > Parameter[3][i]-0.000001 and mc.actual.positions[i] < Parameter[3][i]+0.000001:
            
                if self.reached_joint_number < i:
                    self.reached_joint_number += 1
                    print(123)
                #continue
                #print(self.reached_joint_number)
        
        if self.reached_joint_number == 3:
            self.rotate_action()
    def rotate_action(self):  
            self.get_logger().info('Starting ratation...')
            target_rotation = JointTrajectoryPoint()
            target_rotation.positions = Parameter[5]  # because of the offset in x,y, can less than 2pi   !maybe!  if fitellipse() except big point then not necessary
            target_rotation.time_from_start = Duration(sec=8)   # langer for more points detection
            #target_rotation.velocities = [0.0]
            #target_rotation.accelerations = [0.0] # if added, offset in x or y
            
            rotate_msg = FollowJointTrajectory.Goal()

            rotate_msg.trajectory.joint_names = ['T_Axis_Joint']
            rotate_msg.trajectory.points = [target_rotation]
           
            # self.action_client.wait_for_server() ?
            
            self.send_goal_future = self.action_client.send_goal_async(rotate_msg
                                                                  ,feedback_callback=self.feedback_callback)
            self.send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        #goal_handle = future.re
        
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Rotation rejected.') # add error type
            print(future.exception())
            return                      # 校准多个bauteil看下这里的 if not 循环
        
        self.get_logger().info('Rotation starts.')
        self.get_result_future = goal_handle.get_result_async()
        self.get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self,future):
        result = future.result().result
        self.get_logger().info('Rotation finished!')
        
        # rclpy.shutdown()
        
         # add some conditions ?
      
    def feedback_callback(self,feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info('Rotating...')
        position =  np.array(feedback.actual.positions).tolist()
        self.get_logger().info('The present position is: %s'%(position) )


def main():
    rclpy.init()
    # global Parameter
    
    # Parameter = []
    # global oad, asd
    # asd = [5,5,5]
    # oad = [1,2,3]
    
        
        
        # image_subscriber = AutoCalibration()
        # rclpy.spin(image_subscriber)
        #future = image_subscriber.rotate_action([-0.7, -0.0458, -0.026791, 1.08]) 
        
    rclpy.spin(AutoCalibration())

    
    
if __name__ == "__main__":
    
    # self.self.mode =input('Please select the operating self.self.mode: \n1: Calibration of the realistic equipment\n2: Calibration in simulation\n')
    
    # if self.self.mode == 1:
    
    
    main()
