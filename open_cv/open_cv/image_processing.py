import rclpy
from rclpy.node import Node
from control_msgs.msg import JointTrajectoryControllerState
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class ImageSubscriber(Node):

    def __init__(self):

        super().__init__('image_detection')
        
        
        self.sub2 = self.create_subscription(JointTrajectoryControllerState,
                                             '/joint_trajectory_controller/state',
                                             self.state_callback,
                                             10)
        
        self.br = CvBridge()

    def state_callback(self, msg):
        #self.get_logger().info('%s'%msg.actual)
        self.get_logger().info('%s'%msg.error)
        self.get_logger().info('%s'%msg.joint_names)
        for i in range(4):
            if msg.error.positions[i] < 0.005:
                self.sub = self.create_subscription(Image,
                    '/Cam2/image_raw',
                    self.listener_callback,
                    10)

    def listener_callback(self,data):
        im = self.br.imgmsg_to_cv2(data)
        cv2.namedWindow('ellip',0)
        cv2.resizeWindow('ellip',1000,1000)
        cv2.imshow("ellip", im)
        cv2.waitKey(1)








def main():
    rclpy.init()
    image_subscriber = ImageSubscriber()
    
    rclpy.spin(image_subscriber)
    
    rclpy.shutdown()
 
if __name__ == "__main__":
    main()