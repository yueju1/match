import numpy as np
import cv2
import rclpy  # Python library for ROS 2
from rclpy.node import Node  # Handles the creation of nodes
from sensor_msgs.msg import Image  # Image is the message type
from cv_bridge import CvBridge
2142 3110 44
[[[-1 -1  1 -1]
  [-1 -1  2  0]
  [-1 -1 -1  1]]]
1999 1999
2145 3112
2146 3113

class ImageSubscriber(Node):

    def __init__(self):

        super().__init__('image_subscriber')

        self.subscription = self.create_subscription(
            Image,
            '/Cam2/image_raw',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

        self.br = CvBridge()

    def listener_callback(self, data):
        image_color = self.br.imgmsg_to_cv2(data)

     **  circles = cv2.HoughCircles(
       klein     asd, cv2.HOUGH_GRADIENT, 1.5, 50, param1=30, param2=50, minRadius=5, maxRadius=100) **
                        gross            1                                                      0

def main(args=None):

    rclpy.init(args=args)

    image_subscriber = ImageSubscriber()

    rclpy.spin(image_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    image_subscriber.destroy_node()

    # Shutdown the ROS client library for Python
    rclpy.shutdown()


if __name__ == '__main__':
    main()
