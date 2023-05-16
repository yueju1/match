import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from control_msgs.msg import JointTrajectoryControllerState

from std_msgs.msg._header import Header


class Centering(Node):

    def __init__(self):

        super().__init__('auto_centering')

        self.pub = self.create_publisher(JointTrajectory, '/joint_trajectory_controller/joint_trajectory', 10
                                         )
        jt = JointTrajectory()
        jt.header.frame_id = ''
        jt.header.stamp = self.get_clock().now().to_msg()
        action
        jt.joint_names = ['X_Axis_Joint', 'Y_Axis_Joint',
                          'Z_Axis_Joint', 'Gripper_Rot_Plate_Joint']
        # jt.desired.positions = [0.068, -0.04, -0.01, 0.0]
        # jt.desired.velocities = [100.0, 100.0, 0.05, 2.0]
        # jt.desired.accelerations = [5.0, 5.0, 5.0, 5.0]
        # jt.actual.positions = [0.068, -0.04, -0.01, 0.0]
        # jt.actual.velocities = [100.0, 100.0, 0.5, 2.0]
        # jt.actual.accelerations = [5.0, 5.0, 5.0, 5.0]
        jt2 = JointTrajectoryPoint()
        # 0 0 0 https://answers.ros.org/question/362943/joint-trajectory-published-but-not-executed/
        jt2.positions = [0.068, -0.04, -0.01, 0.0]
        jt2.velocities = [100.0, 100.0, 0.05, 2.0]
        # jt2.accelerations = [100.0, 100.0, 0.05, 2.0]

        jt.points = [jt2]

        # jt.points.append(jt2)
        # jt.points[0].positions = [-0.568, -0.111, -0.04, 10.6317]
        # jt.points[0].velocities = [0.02, 0.02, 0.02, 1.0]
        # jt.points[0].accelerations = [2.0, 2.0, 2.0, 5.0]
        # jt.points[0].time_from_start =

        self.pub.publish(jt)


def main():

    rclpy.init()
    rclpy.spin(Centering())
    rclpy.shutdown()


if __name__ == '__main__':
    main()
