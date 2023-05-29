
import rclpy  # Python library for ROS 2
from rclpy.node import Node  # Handles the creation of nodes
from sensor_msgs.msg import Image  # Image is the message type
from cv_bridge import CvBridge  # Package to convert
import cv2
import numpy as np

class ImageSubscriber(Node):

    def __init__(self):

        super().__init__('image_detection')
        
        # self.subscription = self.create_subscription(
        #     Image,
        #     '/Cam2/image_raw',
        #     self.listener_callback,
        #     10)
        # self.subscription  # prevent unused variable warning

        # self.br = CvBridge()
    # is the callbackfunction a must?

        current_frame = cv2.imread(
        '/home/yueju/下载/Greifer_Unterseitenkamera.bmp')
        
        #先看看canny,threshold值,对检测到的个数的影响.   再  搞一下转动之后圆有偏差的问题
    # def listener_callback(self, data):

        # current_frame = self.br.imgmsg_to_cv2(data)
        
        
    # print(current_frame.ndim)
        a, b = current_frame.shape[0:2]
    # print(current_frame.shape)
    # dst = cv2.resize(current_frame, (4*x, 4*y))
        
        dst = cv2.pyrUp(current_frame)
        (current_frame.max())
    # print(current_frame)
    # print(current_frame.shape)
    # self.get_logger().info('Receiving')
    # bild=cv2.color
        gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    # rint(gray)
        casd = cv2.medianBlur(gray, 7)
        gray2 = cv2.GaussianBlur(gray, (5, 5), 1)
        

        kernel = np.ones((5,5),np.uint8)
        # cv2.findell
        kernel2 = np.ones((10,10),np.uint8)
        pengzhang = cv2.dilate(gray,kernel2)
        fushi =cv2.erode(pengzhang,kernel)
        kai = cv2.morphologyEx(gray,cv2.MORPH_CLOSE,kernel2,iterations=1)
       # cv2.sobel  Gradient
        part = current_frame[680:1550, 750:1750]  # to be modified
        asd = cv2.resize(part, (0, 0), fx=10, fy=10)
        edges = cv2.Canny(gray2, threshold1=30, threshold2=60)
        dst2 = cv2.pyrDown(current_frame)  #轮廓加粗!!!
        canny = cv2.Canny(gray2, 10, 800)
        p2 = cv2.dilate(canny,kernel)
        
        ret, thresh = cv2.threshold(canny, 140, 220, cv2.THRESH_BINARY)
        #na ge fangfa geng zhunque
        contours, hierarchy = cv2.findContours(
            thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # muss a binary bild
    # cv2.drawContours(asd, contours, -1, (0, 0, 255), 1)

    #   filter?
    # double houghcircles to detect two times
        #找轮廓的点，拟合圆
        circles = cv2.HoughCircles(  # kleiner keris in 1.py
        gray, cv2.HOUGH_GRADIENT, 1.5, 50, param1=50, param2=175, minRadius=5, maxRadius=100)
        print(circles)
    # hough param und cany param
    # try: ? if there is no circle, output typeerror
        for circle in circles[0]:

            print(circle[2])

            x = int(circle[0])
            y = int(circle[1])

            r = int(circle[2])

            
            col = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            cv2.circle(col, (x, y), r, (0, 0, 255), 1)
            cv2.circle(col, (x, y), 5, (0, 0, 255), -1)
            print(x, y, r)

    # ru guo bianyuan jiance li you zhixian  then  loesch
    # ru guo yuan de shuliang > 2 then ...
    # center_points = []
    # # print(hierarchy[0])

        # for contour in contours:
        #     moments = cv2.moments(contour)
        #     # if moments['m00'] != 0:    # or try:...?
        # # ZeroDivisionError: float division by zero
        #     cX = int(moments["m10"] / moments["m00"])
        #     cY = int(moments["m01"] / moments["m00"])  # ausschneiden
        # # center_points.append((cX, cY))
        #     cv2.circle(current_frame, (cX, cY), 2, (0, 0, 255), -1)
        #     print(cX, cY)     
        #     col = cv2.cvtColor(canny, cv2.COLOR_GRAY2BGR)
        #     cv2.drawContours(col, contours, -1, (0, 0, 255), 1)
            #c v2.circle(col, (cX, cY), 2, (0, 0, 255), -1)
        
        # cv2.circle(current_frame, (1999, 1999), 4, (0, 0, 255), -1)

    # print(len(contours))
    # print(contours[0])
    # try: durchschnitt ,  minus < 10

    # three points, but drawed two ？
    # then first - -> track the Trajectory:
                                    # alle miitelpunkte sammeln und den mittelpunkt berechnen

        cv2.namedWindow('camera', 0)
        cv2.resizeWindow("camera", 1000, 1000)
    # cv2.namedWindow('asd', 0)
    # cv2.resizeWindow("asd", 1000, 1000)
    # Display image

        cv2.imshow("camera", col)
        # cv2.namedWindow('asd', 0)
        # cv2.resizeWindow("asd", 1000, 1000)
        # cv2.imshow('asd', current_frame)
    # cv2.imshow('asd', casd)
        cv2.waitKey()


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
