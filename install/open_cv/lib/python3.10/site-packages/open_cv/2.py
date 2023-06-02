import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration
import time
class CenteringClient(Node):

    def __init__(self):

        super().__init__('auto_centering')

        self.client = ActionClient(self,FollowJointTrajectory,
                                   '/joint_trajectory_controller/follow_joint_trajectory')
        period = 3.0
        
        print('asdasd')
        
        time.sleep(5.0)

    def send_g(self,points): # kann ohne points sein, und jt2.positions = []
        self.get_logger().info('213')
        jt2 = JointTrajectoryPoint()
        jt2.positions = points
        jt2.time_from_start = Duration(sec=4)
        # more smothly: x_joint by 0.08 und y,z,t......
        goal_msg = FollowJointTrajectory.Goal()

        goal_msg.trajectory.joint_names = ['X_Axis_Joint','Y_Axis_Joint',  
                                            'Z_Axis_Joint', 'T_Axis_Joint']
        goal_msg.trajectory.points = [jt2]
        
        self.client.wait_for_server()
        return self.client.send_goal_async(goal_msg)
        

# ,'Y_Axis_Joint',    'Z_Axis_Joint', 'T_Axis_Joint'
# , -0.0458, -0.026791, 1.08]

def main(args=None):

    rclpy.init(args=args)
    client = CenteringClient()
    future = client.send_g([-0.7, -0.0458, -0.026791, 1.08]) 
    rclpy.spin_until_future_complete(client,future)
    rclpy.shutdown()


if __name__ == '__main__':
    main()