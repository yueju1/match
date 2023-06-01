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





class ImageSubscriber(Node):

    def __init__(self):

        super().__init__('image_detection')
        
        
        self.sub2 = self.create_subscription(JointTrajectoryControllerState,
                                             '/joint_trajectory_controller/state',
                                             self.state_callback,
                                             10)
        
        self.br = CvBridge()
    
        self.rotate_client = ActionClient(self,FollowJointTrajectory,
                                  '/joint_trajectory_controller/follow_joint_trajectory')
        self.ok = 0
    def state_callback(self, msg):
        
        #self.get_logger().info('%s'%msg.actual)
        self.get_logger().info('%s'%msg.desired.positions)
        #self.get_logger().info('%s'%msg.joint_names)
        for i in range(4):
            if msg.desired.positions == array.array('d',[-0.359, -0.0458, -0.026791, 1.08]):
                self.sub = self.create_subscription(Image,
                    '/Cam2/image_raw',
                    self.listener_callback,
                    10)
                self.rotate_action()
        # time.sleep(2.0)   加了这个降频了？  卡

    def listener_callback(self,data):
        
        im = self.br.imgmsg_to_cv2(data)
        cv2.namedWindow('ellip',0)
        cv2.resizeWindow('ellip',1000,1000)
        cv2.imshow("ellip", im)
        cv2.waitKey(1)
        self.ok = 1
    

    def rotate_action(self):
        if self.ok == 1:

            time.sleep(2.0)
            self.get_logger().info('asdadasdasdasdasdasd')

            jt2 = JointTrajectoryPoint()
            jt2.positions = [-0.359, -0.0458, -0.026791, 12.0]
            jt2.time_from_start = Duration(sec=4)   # langer for more points detection
            
            goal_msg = FollowJointTrajectory.Goal()

            goal_msg.trajectory.joint_names = ['X_Axis_Joint','Y_Axis_Joint',  
                                                'Z_Axis_Joint', 'T_Axis_Joint']
            goal_msg.trajectory.points = [jt2]
            
            self.rotate_client.wait_for_server()
            return self.rotate_client.send_goal_async(goal_msg)







def main():
    rclpy.init()

    image_subscriber = ImageSubscriber()
    # rclpy.spin(image_subscriber)

    #future = image_subscriber.rotate_action([-0.7, -0.0458, -0.026791, 1.08]) 
    rclpy.spin(image_subscriber)

    rclpy.shutdown()
    
if __name__ == "__main__":
    main()