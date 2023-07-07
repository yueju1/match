#!/usr/bin/env/python3
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration
from rosgraph_msgs.msg import Clock
from decimal import Decimal
from rclpy.action.client import ClientGoalHandle
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

# float: 每次运动到相同的坐标，看下actual的值一样吗，运行了看看  以及后面 for i in range(4)的条件
#         add conditions
class CenteringClient(Node):

    def __init__(self):

        super().__init__('auto_centering')

        self.action_client = ActionClient(self,FollowJointTrajectory,
                                   '/pm_robot_xyz_axis_controller/follow_joint_trajectory')

        
    def send_goal(self,points): # kann ohne points sein, und target_point.positions = []
        
        target_point = JointTrajectoryPoint()
        target_point.positions = points          # ros::Time::now()  ros2 li shisha
        target_point.time_from_start = Duration(sec= 6) # longer for more point detection 
        # target_point.velocities = [0.0, 0.0, 0.0, 0.0]
        # target_point.accelerations = [0.0, 0.0, 0.0, 0.0]
        # more smoothly: x_joint by 0.08 und y,z,t......
        goal_msg = FollowJointTrajectory.Goal()
        # goal_msg.trajectory.header.stamp = Clock().clock     use_sim_time in launch
       
        goal_msg.trajectory.joint_names = ['X_Axis_Joint','Y_Axis_Joint',
                                           'Z_Axis_Joint','T_Axis_Joint'
                                            ]
        goal_msg.trajectory.points = [target_point]
        # + velocity accelerate  速度和duration2选1吗 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.action_client.wait_for_server()
        self.send_goal_future = self.action_client.send_goal_async(goal_msg
                                                                  ,feedback_callback=self.feedback_callback)
        self.send_goal_future.add_done_callback(self.goal_response_callback)


    def goal_response_callback(self, future):
        #goal_handle = future.re
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected.') # add error type
            print(future.exception())
            return                      # 校准多个bauteil看下这里的 if not 循环
        
        self.get_logger().info('Goal accepted.')
        self.get_result_future = goal_handle.get_result_async()
        self.get_result_future.add_done_callback(self.get_result_callback)


    def get_result_callback(self,future):
        self.get_logger().info('Goal reached!')
        
        rclpy.shutdown()
        
         # add some conditions ?
      
    def feedback_callback(self,feedcak_msg):

        self.get_logger().info('Approaching...')


def main(args=None):
    #os.system('/home/pmlab/yueju/change/open_cv/open_cv/op.py')
    
    rclpy.init(args=args)
    
    client = CenteringClient()       #  decimal  kanxia jonit_state  position
    client.send_goal([-0.359, -0.0458, 0.02, -0.00008]) 
    # future = client.send_goal([Decimal(-0.7), Decimal(-0.04), Decimal(-0.01), Decimal(12.0)]) 
    rclpy.spin(client)
    #client.destroy_node()
    
    

if __name__ == '__main__':
    main()
