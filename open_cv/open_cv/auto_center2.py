import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration

class CenteringClient(Node):

    def __init__(self):

        super().__init__('auto_centering')

        self.client = ActionClient(self,FollowJointTrajectory,
                                   '/joint_trajectory_controller/follow_joint_trajectory')
    
    def send_goal(self,points): # kann ohne points sein, und jt2.positions = []
        
        jt2 = JointTrajectoryPoint()
        jt2.positions = points
        jt2.velocities = [100.0, 100.0, 0.05, 2.0]
        jt2.accelerations = [100.0, 100.0, 0.05, 2.0]
        # more smothly: x_joint by 0.08 und y,z,t......
        goal_msg = FollowJointTrajectory.Goal()
        jt2.time_from_start = Duration(sec= 4)
        goal_msg.trajectory.joint_names = ['X_Axis_Joint','Y_Axis_Joint',
                          'Z_Axis_Joint', 'T_Axis_Joint']
        goal_msg.trajectory.points = [jt2]
        
        self.client.wait_for_server()
        return self.client.send_goal_async(goal_msg)









def main(args=None):

    rclpy.init(args=args)
    client = CenteringClient()
    future = client.send_goal([-0.05, -0.12, -0.01, 0.0]) 
    rclpy.spin_until_future_complete(client,future)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
