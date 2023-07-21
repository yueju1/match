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


class asdf(Node):
    
    def __init__(self):
        #这里面的不报位置吗     
        super().__init__('image_detecn')
        self.mode =input('Please select the operating self.mode: \n1: Calibration of the realistic equipment\n2: Calibration in simulation\n')

        Para_real = ('/pm_robot_xyz_axis_controller/state',
                    '/pm_robot_xyz_axis_controller/follow_joint_trajectory',
                    '/Camera_Bottom_View/pylon_ros2_camera_node/image_raw',
                    [-0.359, -0.0458, 0.03, -1200000.0],
                    [-0.359, -0.0458, 0.03, 600000.0],
                    [600000.0])
        
        Para_sim = ('/joint_trajectory_controller/state',
                    '/joint_trajectory_controller/follow_joint_trajectory',
                    '/Cam2/image_raw',
                    [-0.359, -0.0458, -0.051544, 0.0],
                    [-0.359, -0.0458, -0.051544, 6.2],
                    [6.2])
    
        if self.mode == '1':
            self.Parameter = Para_real
            
        if self.mode == '2':
            self.Parameter = Para_sim
        time.sleep(6.0)
        self.reached_joint_number = 0
        self.action_client = ActionClient(self,FollowJointTrajectory,
                                  self.Parameter[1])
        print(000000000000000000000000000)
        self.sub2 = self.create_subscription(JointTrajectoryControllerState,self.Parameter[0],self.call_b2,10)
    def call_b2(self,mc):
        for i in range(len(mc.actual.positions)):
            
            if mc.desired.positions.tolist() == self.Parameter[3] and mc.actual.positions[i] > self.Parameter[3][i]-0.000001 and mc.actual.positions[i] < self.Parameter[3][i]+0.000001:
            
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
            target_rotation.positions = self.Parameter[5]  # because of the offset in x,y, can less than 2pi   !maybe!  if fitellipse() except big point then not necessary
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
   
    # image_subscriber = AutoCalibration()
    # rclpy.spin(image_subscriber)
    #future = image_subscriber.rotate_action([-0.7, -0.0458, -0.026791, 1.08]) 
    #rclpy.spin_once(aasd())
    rclpy.spin(asdf())
    

    rclpy.shutdown()
    
if __name__ == "__main__":

    

    main()
