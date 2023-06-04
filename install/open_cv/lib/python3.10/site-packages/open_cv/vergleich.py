import rclpy  # Python library for ROS 2
from rclpy.node import Node  # Handles the creation of nodes
from sensor_msgs.msg import Image  # Image is the message type
from cv_bridge import CvBridge  # Package to convert
import cv2
import numpy as np

class ImageSubscriber(Node):

    def __init__(self):

        super().__init__('image_detection')
        
        self.subscription = self.create_subscription(
            Image,
            '/Cam2/image_raw',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

        self.br = CvBridge()
       
    def listener_callback(self, data):

        # current_frame = self.br.imgmsg_to_cv2(data)
        current_frame = cv2.imread("/home/pmlab/Desktop/Greifer_Unterseitenkamera.bmp")
        
    # print(current_frame.ndim)
        a, b = current_frame.shape[0:2]
    # print(current_frame.shape)
    # dst = cv2.resize(current_frame, (4*x, 4*y))
        
        dst = cv2.pyrUp(current_frame)

        gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    
        # casd = cv2.medianBlur(gray, 7)
        
        
        kernel = np.ones((5,5),np.uint8)
        
        kernel2 = np.ones((10,10),np.uint8)
        # pengzhang = cv2.dilate(gray,kernel2)
        # fushi =cv2.erode(pengzhang,kernel)
        # kai = cv2.morphologyEx(gray,cv2.MORPH_CLOSE,kernel2,iterations=1)
       # cv2.sobel  Gradient
        part = current_frame[360:2200, 70:1850]  # to be modified
        # gray2 = cv2.GaussianBlur(part, (5, 5), 1)
        # gray2 = cv2.medianBlur(current_frame, 5)
        gray2 = cv2.GaussianBlur(gray, (5, 5),1)
        #asd = cv2.resize(part, (0, 0), fx=10, fy=10)
        edges = cv2.Canny(gray2, threshold1=30, threshold2=60)
        dst2 = cv2.pyrDown(current_frame)  #轮廓加粗!!!
        canny = cv2.Canny(gray2, 150, 200)
        p2 = cv2.dilate(canny,kernel)

        #找轮廓的点，拟合圆

        circles = cv2.HoughCircles(  # kleiner keris in 1.py
        gray2, cv2.HOUGH_GRADIENT, 1, 5, param1=160, param2=30, minRadius=15, maxRadius=0)
        print(circles)
        print('---------------------------')
    # try: ? if there is no circle, output typeerror
        for circle in circles[0]:

            # print(circle[2])

            x = int(circle[0])
            y = int(circle[1])

            r = int(circle[2])
               
            
            col = cv2.cvtColor(gray2, cv2.COLOR_GRAY2BGR)
            cv2.circle(col, (x, y), r, (0, 0, 255), 1)
            cv2.circle(col, (x, y), 5, (0, 0, 255), -1)
            # print(x, y, r)

        # ret, thresh = cv2.threshold(canny, 140, 220, cv2.THRESH_BINARY)
        # #na ge fangfa geng zhunque
        # contours, hierarchy = cv2.findContours(
        #     thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # muss a binary bild
        # for contour in contours:
        #     moments = cv2.moments(contour)
        #     if moments['m00'] != 0:    # or try:...?
        # # ZeroDivisionError: float division by zero
        #         cX = moments["m10"] / moments["m00"]
        #         cY = moments["m01"] / moments["m00"] # ausschneiden
        #         col = cv2.cvtColor(canny, cv2.COLOR_GRAY2BGR)
        #         #cv2.drawContours(col, contours, -1, (0, 0, 255), 1)
        #         #cv2.circle(col, (cX, cY), 3, (0, 0, 255), -1)
        #     # center_points.append((cX, cY))
        #         #cv2.circle(current_frame, (cX, cY), 2, (0, 0, 255), -1)
        #         print(cX, cY)     
                

        cv2.namedWindow('camera', 0)
        cv2.resizeWindow("camera", 1000, 1000)
 

        cv2.imshow("camera", canny)
        cv2.namedWindow('asd', 0)
        cv2.resizeWindow("asd", 1000, 1000)
        cv2.imshow('asd', col)
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
