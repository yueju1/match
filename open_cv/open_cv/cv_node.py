
import rclpy  # Python library for ROS 2
from rclpy.node import Node  # Handles the creation of nodes
from sensor_msgs.msg import Image  # Image is the message type
from cv_bridge import CvBridge  # Package to convert
import cv2
import numpy


"CV2.TM_CCOEFF_NORMED"


class ImageSubscriber(Node):
    """
    Create an ImageSubscriber class, which is a subclass of the Node class.
    """

    def __init__(self):
        """
        Class constructor to set up the node
        """
        # Initiate the Node class's constructor and give it a name
        super().__init__('image_subscriber')

        # Create the subscriber. This subscriber will receive an Image
        # from the video_frames topic. The queue size is 10 messages.
        self.subscription = self.create_subscription(
            Image,
            '/Cam2/image_raw',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

        # Used to convert between ROS and OpenCV images
        self.br = CvBridge()

    def listener_callback(self, data):
        """
        Callback function.
        """
        # Display the message on the console

        # Convert ROS Image message to OpenCV image

        current_frame = self.br.imgmsg_to_cv2(data)
        # print(current_frame.ndim)

        # print(current_frame)
        self.get_logger().info('Receiving video frame')
        # bild=cv2.color
        # gray = cv2.cvtColor(current_frame, cv2.COLOR_GRAY2BGR)
        # rint(gray)
        # gray2=cv2.GaussianBlur(current_frame, (19, 19),1)
        # canny=cv2.Canny(gray2,75,200)
        # casd = cv2.medianBlur(current_frame, 7)

        edges = cv2.Canny(current_frame, threshold1=15, threshold2=30)
        #   filter?
        circles = cv2.HoughCircles(
            current_frame, cv2.HOUGH_GRADIENT, 1, 50, param1=100, param2=30, minRadius=5, maxRadius=100)
        print(circles)
        for circle in circles[0, :]:

            print(circle[2])

            x = int(circle[0])
            y = int(circle[1])

            r = int(circle[2])

            cv2.circle(current_frame, (x, y), r, (0, 0, 255), 3)

            cv2.circle(current_frame, (x, y), 5, (0, 0, 255), -1)

        cv2.namedWindow('camera', 0)
        cv2.resizeWindow("camera", 1100, 1000)
        # Display image
        cv2.imshow("camera", current_frame)

        cv2.waitKey(1)


def main(args=None):

    # Initialize the rclpy library
    rclpy.init(args=args)

    # Create the node
    image_subscriber = ImageSubscriber()

    # Spin the node so the callback function is called.
    rclpy.spin(image_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    image_subscriber.destroy_node()

    # Shutdown the ROS client library for Python
    rclpy.shutdown()


if __name__ == '__main__':
    main()
