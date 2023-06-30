#!/usr/bin/env/python3
import cv2
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np
from circle_fit import taubinSVD

class ImageSubscriber(Node):

    def __init__(self):

        super().__init__('image_detection')
        
        current_frame = cv2.imread(
        '/home/pmlab/Desktop/Greifer_Unterseitenkamera.bmp')
        f = open('/home/pmlab/Desktop/Greifer_Unterseitenkamera.bmp', 'rb')
        image_bytes = f.read()  # b'\xff\xd8\xff\xe0\x00\x10...'

        decoded = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), -1)
        
    # print(current_frame.ndim)
        a, b = current_frame.shape[0:2]
    # print(current_frame.shape)
    # dst = cv2.resize(current_frame, (4*x, 4*y))
        
        dst = cv2.pyrUp(current_frame)
        # (current_frame.max())
    # print(current_frame)
    # print(current_frame.shape)
    # self.get_logger().info('Receiving')
    # bild=cv2.color
        self.list=[]
    # rint(gray)
        # gray2 = cv2.medianBlur(gray, 7)
        gray = cv2.GaussianBlur(current_frame, (5, 5), 1.5)
        gray2 = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
        
        # kernel = np.ones((5,5),np.uint8)
        # # cv2.findell
        # kernel2 = np.ones((10,10),np.uint8)
        # pengzhang = cv2.dilate(gray,kernel2)
        # fushi =cv2.erode(pengzhang,kernel)
        # kai = cv2.morphologyEx(gray,cv2.MORPH_CLOSE,kernel2,iterations=1)
       # cv2.sobel  Gradient
        part = current_frame[680:1550, 750:1750]  # to be modified
        # asd = cv2.resize(part, (0, 0), fx=10, fy=10)
        # edges = cv2.Canny(gray2, threshold1=30, threshold2=60)
        # dst2 = cv2.pyrDown(current_frame)  #轮廓加粗!!!
        canny = cv2.Canny(gray2, 40, 500)
        # p2 = cv2.dilate(canny,kernel)
        
        ret, thresh = cv2.threshold(canny, 140, 220, cv2.THRESH_BINARY)
        #na ge fangfa geng zhunque
        contours, hierarchy = cv2.findContours(
            canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # muss a binary bild
        
        # for x in range(2591):
        #     for y in range(1493):
        #         if canny[y, x] != 0:
        #             self.list.append([float(x),float(y)])
        #             #cv2.circle(current_frame, (x, y), 1, (0, 0, 255), -1)
        # col = cv2.cvtColor(canny,cv2.COLOR_GRAY2BGR)
        # q,w,e,r = taubinSVD(self.list)
        # cv2.circle(col, (int(q),int(w)), int(e), (0, 0, 255), 1)
        # cv2.circle(col, (int(q), int(w)), 5, (0, 0, 255), -1)
        # for contour in contours:
        #     for i in contour:
                
        #         self.list.append(i)
        # x = np.array(self.list)
        # print(x.shape)
        for i in range(len(contours)):  #sobel? kaolv geng fuza yidian
            # if len(contours[i]) >= 300 and len(contours[i]) < 330:
            if len(contours[i]) >= 100 and len(contours[i]) <= 200:
                cv2.drawContours(current_frame, contours, -1, (0, 0, 255), 1)
                cen,rad = cv2.minEnclosingCircle(contours[i])
        cv2.circle(current_frame, (int(cen[0]),int(cen[1])), int(rad), (0, 0, 255), 1)
        cv2.circle(current_frame, (int(cen[0]), int(cen[1])), 5, (0, 0, 255), -1)



        

        circles = cv2.HoughCircles(  # kleiner keris in 1.py
        gray2, cv2.HOUGH_GRADIENT, 1, 50, param1=500, param2=50, minRadius=15, maxRadius=100)
        # print(circles)
        
    # hough param und cany param
    # try: ? if there is no circle, output typeerror
        # for circle in circles[0]:

        #     print(circle[2])

        #     x = int(circle[0])
        #     y = int(circle[1])

        #     r = int(circle[2])

            
        #     col = cv2.cvtColor(gray2, cv2.COLOR_GRAY2BGR)
        #     cv2.circle(current_frame, (x, y), r, (0, 0, 255), 1)
        #     cv2.circle(current_frame, (x, y), 5, (0, 0, 255), -1)
        #     print(x, y, r)

        


        cv2.namedWindow('ellip',0)
        cv2.resizeWindow('ellip',1000,1000)
        cv2.imshow("ellip", current_frame)

        cv2.namedWindow('ellips',0)
        cv2.resizeWindow('ellips',1000,1000)
        cv2.imshow("ellips", canny)
        
        cv2.waitKey(0)
        
def main():
    rclpy.init()
    image_subscriber = ImageSubscriber()

    rclpy.spin(image_subscriber)
    image_subscriber.destroy_node()
    rclpy.shutdown()
 
if __name__ == "__main__":
    main()
                  