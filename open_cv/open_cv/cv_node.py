
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

        # print(current_frame)
        # print(current_frame.shape)
        self.get_logger().info('Receiving')
        # bild=cv2.color
        # gray = cv2.cvtColor(current_frame, cv2.COLOR_GRAY2BGR)
        # rint(gray)
        gray2 = cv2.GaussianBlur(dst, (19, 19), 1)
        canny = cv2.Canny(gray2, 75, 200)

        part = current_frame[700:1100, 1100:1500]
        asd = cv2.resize(part, (0, 0), fx=10, fy=10)
        edges = cv2.Canny(gray2, threshold1=30, threshold2=60)
        dst2 = cv2.pyrDown(current_frame)
        casd = cv2.medianBlur(dst2, 7)

        ret, thresh = cv2.threshold(asd, 140, 220, cv2.THRESH_BINARY)

        contours, hierarchy = cv2.findContours(
            thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        # cv2.drawContours(asd, contours, -1, (0, 0, 255), 1)

        #   filter?
        circles = cv2.HoughCircles(  # kleiner keris in 1.py
            asd, cv2.HOUGH_GRADIENT, 1.5, 50, param1=30, param2=50, minRadius=5, maxRadius=100)
        # print(circles)
        # hough param und cany param
        # try: ? if there is no circle, output typeerror
        for circle in circles[0]:

            # print(circle[2])

            x = int(circle[0])
            y = int(circle[1])

            r = int(circle[2])

            # cv2.circle(asd, (x, y), r, (0, 0, 255), 3)

            # cv2.circle(asd, (x, y), 5, (0, 0, 255), -1)
        print(x, y, r)
        center_points = []
        print(hierarchy)
        for contour in contours:
            moments = cv2.moments(contour)
            cX = int(moments["m10"] / moments["m00"])
            cY = int(moments["m01"] / moments["m00"])
            center_points.append((cX, cY))
            print(cX, cY)
        print(len(contours))
    # try: durchschnitt ,  minus < 10

    three points, but drawed two ？
    then first - -> track the Trajectory

    # cv2.drawContours(asd, contours, -1, (0, 255, 0), 2)
    cv2.circle(asd, (cX, cY), 10, (0, 0, 255), -1)
    # cv2.circle(asd, (1999, 1999), 5, (0, 0, 255), -1)
    cv2.namedWindow('camera', 0)
    cv2.resizeWindow("camera", 1000, 1000)
    # cv2.namedWindow('asd', 0)
    # cv2.resizeWindow("asd", 1000, 1000)
    # Display image
    cv2.imshow("camera", asd)
    # cv2.imshow('asd', part)
    # cv2.imshow('asd', casd)
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
