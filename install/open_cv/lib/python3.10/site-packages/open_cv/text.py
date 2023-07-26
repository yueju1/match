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
import traceback
import threading
 #试一下加不加中值滤波的区别 椒盐噪声    先搞destroy_node 然后看下yaml
# 程序考虑一下顺时针逆时针，想下之前想到的关于顺逆时针的东西。会转出去吗，如果图缩放比例的话
 #也许不需要很复杂， 可能可以通过: 知道图片中 现实点和未来点之前的关系，来求出实际中未来点的位置(也许要用坐标转换)。

class AutoCa(Node):

    def __init__(self):
        #这里面的不报位置吗     
        super().__init__('image',allow_undeclared_parameters = True)
        # try self.sub
            # if except ...
            #        ...shutdown
           
            # ...
        self.declare_parameter('ok',0)
        self.declare_parameter('bad',1)
        self.declare_parameter('1','asd')
        self.declare_parameter('2','sdf')
        self.declare_parameter('3','qwe')
        self.declare_parameter('4',[-0.359, -0.0458, -0.051544, 5.0])
        self.declare_parameter('5',2)
        self.declare_parameter('6',[3.0])

        
        global Parameter, mode
        mode = '2'
        Parameter = ('/joint_trajectory_controller/state',
                '/joint_trajectory_controller/follow_joint_trajectory',
                '/Cam2/image_raw',
                [-0.359, -0.0458, -0.051544, 0.0],
                [-0.359, -0.0458, -0.051544, 6.2],
                [6.2])
        

        self.get_logger().info('Calibration starting...')   
        self.ok = 0
        self.list = []
        self.first_point = []
        self.r_r = 0
        self.m = 0
        self.s = 0
        self. RR = 0
        self.mm = 0
        print(Parameter) 
        
        self.timer = self.create_timer(1,self.da_ba)

        self.reached_joint_number = 0    
        # self.sub = self.create_subscription(JointTrajectoryControllerState,
        #                                      '/pm_robot_xyz_axis_controller/state',
        #                                      self.state_callback,
        #                                      10)
        self.sub = self.create_subscription(JointTrajectoryControllerState,
                                             self.get_parameter('1').value,
                                             self.state_callback,
                                             10)
        self.br = CvBridge()
        self.get_logger().info('Waiting for controller state...')
        #  self.subscription  # prevent unused variable warning ?
        
        self.action_client = ActionClient(self,FollowJointTrajectory,
                                  self.get_parameter('2').value)
        # self.action_client = ActionClient(self,FollowJointTrajectory,
        #                           '/pm_robot_xyz_axis_controller/follow_joint_trajectory')
        self. ok = 0
        self.align_action()  
    
        
    def da_ba(self):
        ad = self.get_parameter('ok').value
        if ad == 1:
            self.rotate_action()
            self.timer.cancel()
        if ad == 2:
            rclpy.shutdown()
            exit(1)
      
    def state_callback(self, msg):
        
        self.get_logger().info('state_callback')
        # if msg.desired.positions == array.array('d',[-0.359, -0.0458, 0.03, 0.0]):
        for i in range(len(msg.actual.positions)):
            
            if msg.desired.positions.tolist() == self.get_parameter('4').value and msg.actual.positions[i] > self.get_parameter('4').value[i]-0.000001 and msg.actual.positions[i] < self.get_parameter('4').value[i]+0.000001:
            
                if self.reached_joint_number < i:
                    self.reached_joint_number += 1
                    print(123)
                #continue
                #print(self.reached_joint_number)
        
        if self.reached_joint_number == 3:
            print('gogogo') 

            self.set_parameters([rclpy.Parameter('ok',value=1)])
 
                
        #for i in range(len(msg.actual.positions)):
        if  msg.desired.positions.tolist()[3] == self.get_parameter('6').value[0] and msg.actual.positions[3] > self.get_parameter('6').value[0]-0.3 and msg.actual.positions[3] < self.get_parameter('6').value[0]+0.3:
              # msg.desired.positions.tolist()[3] == self.get_parameter('6').value[0] and 
      
                # ZeroDivisionError by -0.00008 am Anfang (maybe together with multiple detection)
            #if self.reached_joint_number < i+3:
                self.reached_joint_number += 1
        if self.reached_joint_number == 4:
            print('backbackbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb') 
            self.reached_joint_number = 0 
            #self.fit_ellipse()
            # self.return_action()  
            self.set_parameters([rclpy.Parameter('ok',value=2)])
            # rclpy.shutdown()!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
              

    def align_action(self):
        self.get_logger().info('Starting align...')
        target_point = JointTrajectoryPoint()
        target_point.positions = self.get_parameter('4').value     
        target_point.time_from_start = Duration(sec= 6) # longer for more point detection 
        
        goal_msg = FollowJointTrajectory.Goal()
        
    
        goal_msg.trajectory.joint_names = ['X_Axis_Joint','Y_Axis_Joint',
                                        'Z_Axis_Joint','T_Axis_Joint'
                                            ]
        goal_msg.trajectory.points = [target_point]
        
        self.action_client.wait_for_server()
        self.send_goal_future = self.action_client.send_goal_async(goal_msg
                                                                  ,feedback_callback=self.align_callback)
        self.send_goal_future.add_done_callback(self.align_response_callback)


    def align_response_callback(self, future):
        #goal_handle = future.re
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected.') # add error type
            print(future.exception())
            return                      
        
        self.get_logger().info('Goal accepted.')
        self.get_result_future = goal_handle.get_result_async()
        self.get_result_future.add_done_callback(self.align_result_callback)

    
    def align_result_callback(self,future):
        # error_code = future.result().result.error_code
        # if error_code != 0:
        #     self.get_logger().info(f'Error code: "{error_code}"')
        self.get_logger().info('Goal reached!')
        
        # rclpy.shutdown()

      
    def align_callback(self,feedcak_msg):

        self.get_logger().info('Approaching...')
                                                    
    def rotate_action(self):  
            self.get_logger().info('Starting ratation...')
            target_rotation = JointTrajectoryPoint()
            target_rotation.positions = self.get_parameter('6').value  # because of the offset in x,y, can less than 2pi   !maybe!  if fitellipse() except big point then not necessary
            target_rotation.time_from_start = Duration(sec=8)   # langer for more points detection

            
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
        # value of velocity is not 0
    
    def return_action(self):
            target_point = JointTrajectoryPoint()
            target_point.positions = [0.0, 0.0, 0.0, 0.0]         # ros::Time::now()  ros2 li shisha
            target_point.time_from_start = Duration(sec= 6) # longer for more point detection 

            goal_msg = FollowJointTrajectory.Goal()

        
            goal_msg.trajectory.joint_names = ['X_Axis_Joint','Y_Axis_Joint',
                                            'Z_Axis_Joint','T_Axis_Joint'
                                                ]
            goal_msg.trajectory.points = [target_point]
            
            
            self.action_client.send_goal_async(goal_msg)

def main():
    rclpy.init()
    # th1 = threading.Thread(target=asdf(),name='asd')
    # th1.start()
    # print(123123123123)
    # th2 = threading.Thread(target=AutoCa(),name='yx')
    # th2.start()
    # rclpy.spin_once(asdf())
    node = AutoCa()
    #node.pare()
    rclpy.spin(node) 
    #rclpy.shutdown()
    
if __name__ == "__main__":


    main()
