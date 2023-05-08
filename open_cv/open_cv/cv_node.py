
import rclpy  # Python library for ROS 2
from rclpy.node import Node  # Handles the creation of nodes
from sensor_msgs.msg import Image  # Image is the message type
from cv_bridge import CvBridge  # Package to convert
import cv2
import numpy


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

        current_frame = self.br.imgmsg_to_cv2(data)
        # print(current_frame.ndim)
        a, b = current_frame.shape[0:2]
        # print(current_frame.shape)
        # dst = cv2.resize(current_frame, (4*x, 4*y))

        dst = cv2.pyrUp(current_frame)

        print(current_frame)
        print(current_frame.shape)
        self.get_logger().info('Receiving')
        # bild=cv2.color
        # gray = cv2.cvtColor(current_frame, cv2.COLOR_GRAY2BGR)
        # rint(gray)
        gray2 = cv2.GaussianBlur(dst, (19, 19), 1)
        # canny = cv2.Canny(gray2, 75, 200)
        # casd = cv2.medianBlur(current_frame, 7)
        part = current_frame[960:1080, 1100:1200]
        asd = cv2.resize(part, (0, 0), fx=10, fy=10)
        edges = cv2.Canny(gray2, threshold1=15, threshold2=30)
        dst2 = cv2.pyrDown(asd)
        #   filter?
        circles = cv2.HoughCircles(
            current_frame, cv2.HOUGH_GRADIENT, 1, 50, param1=100, param2=30, minRadius=1, maxRadius=100)
        # print(circles)

        # try: ? if there is no circle, output typeerror
        for circle in circles[0]:

            # print(circle[2])

            x = int(circle[0])
            y = int(circle[1])

            r = int(circle[2])

            cv2.circle(current_frame, (x, y), r, (0, 0, 255), 3)

            # cv2.circle(current_frame, (x, y), 5, (0, 0, 255), -1)
        print(x, y, r)

        cv2.namedWindow('camera', 0)
        cv2.resizeWindow("camera", 1000, 1000)
        cv2.namedWindow('asd', 0)
        cv2.resizeWindow("asd", 1000, 1000)
        # Display image
        cv2.imshow("camera", current_frame)
        # cv2.imshow('asd', part)
        cv2.imshow('asd', dst2)
        cv2.waitKey(1)


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
