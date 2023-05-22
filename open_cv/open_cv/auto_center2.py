import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration
from rosgraph_msgs.msg import Clock
from decimal import Decimal
from rclpy.action.client import ClientGoalHandle



class CenteringClient(Node):

    def __init__(self):

        super().__init__('auto_centering')

        self.action_client = ActionClient(self,FollowJointTrajectory,
                                   '/joint_trajectory_controller/follow_joint_trajectory')


    def send_goal(self,points): # kann ohne points sein, und jt2.positions = []
        
        jt2 = JointTrajectoryPoint()
        jt2.positions = points
        jt2.time_from_start = Duration(sec= 4)
        # jt2.velocities = [100.0, 100.0, 0.05, 2.0]
        # jt2.accelerations = [100.0, 100.0, 0.05, 2.0]
        # more smothly: x_joint by 0.08 und y,z,t......
        goal_msg = FollowJointTrajectory.Goal()
        # goal_msg.trajectory.header.stamp = Clock().clock     use_sim_time in launch
       
        goal_msg.trajectory.joint_names = ['X_Axis_Joint','Y_Axis_Joint',
                          'Z_Axis_Joint', 'T_Axis_Joint']
        goal_msg.trajectory.points = [jt2]
        
        self.action_client.wait_for_server()
        self.send_goal_future = self.action_client.send_goal_async(goal_msg)
                                                                  # ,feedback_callback=self.feedback_callback)
        self.send_goal_future.add_done_callback(self.goal_response_callback)


    def goal_response_callback(self, future):
        #goal_handle = future.re
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected.') # add error type
            print(future.exception())
            return
        
        self.get_logger().info('Goal accepted.')
        self.get_result_future = goal_handle.get_result_async()
        self.get_result_future.add_done_callback(self.get_result_callback)


    def get_result_callback(self,future):
        self.get_logger().info('Goal reached!')

        # self.get_logger().info('Result: {0}'.format(result))  
        

       

      # besser + diese👇?
    # def feedback_callback(self,feedcak_msg):
    #     self.get_logger().info('Approaching...')
        
    
    # add conditions



def main(args=None):

    rclpy.init(args=args)
    client = CenteringClient()       #  decimal  kanxia jonit_state  position
    future = client.send_goal([-0.7, -0.04, -0.01, 12.0]) 
    # future = client.send_goal([Decimal(-0.7), Decimal(-0.04), Decimal(-0.01), Decimal(12.0)]) 
    rclpy.spin(client)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
