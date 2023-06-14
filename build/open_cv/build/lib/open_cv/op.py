#!/usr/bin/env/python3
import cv2
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np


class ImageSubscriber(Node):

    def __init__(self):

        super().__init__('image_detection')
        
#         self.subscription = self.create_subscription(
#             Image,
#             '/Cam2/image_raw',
#             self.listener_callback,
#             10)
#         self.subscription  # prevent unused variable warning

#         self.br = CvBridge()
    # is the callbackfunction a must?
        self.list=[]
        print("asdasdasd")
    # def listener_callback(self, data):
        # im = self.br.imgmsg_to_cv2(data)
        
        im = cv2.imread("/home/pmlab/Desktop/Greifer_Unterseitenkamera.bmp")    
        # gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)    
        gray2 = cv2.GaussianBlur(im, (5, 5), 1)
        #gray2 = cv2.medianBlur(gray, 7)
        canny = cv2.Canny(im, 40, 500) # (460,500)  有些值检测不到
        _, thresh = cv2.threshold(canny, 140, 220, cv2.THRESH_BINARY)  
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  
            #最小二乘法拟合椭圆  椭圆检测能检测圆吗 摄像机侧边拍真的是椭圆吗（不倾斜，相互平行）
            # 检测椭圆内圈？
        for i in range(len(contours)):  #sobel? kaolv geng fuza yidian
            if len(contours[i]) >= 5 :
                retval = cv2.fitEllipseAMS(contours[i])  
                # print('-------')
                # print(contours[i])
                # print('-------')
                cv2.ellipse(im, retval, (0, 0, 255), thickness=1) 
                cv2.circle(im, (int(retval[0][0]),int(retval[0][1])),3, (0, 0, 255), -2)
                col = cv2.cvtColor(canny, cv2.COLOR_GRAY2BGR)
                cv2.drawContours(col, contours, -1, (0, 0, 255), 1)
                print(retval)
                # if retval[1][0] < 240.0 and retval[1][1] > 220:
                #     #  noch durchschnittswert
                #     if cv2.fitEllipse(contours[i])[0] not in self.list:
                #         self.list.append(cv2.fitEllipse(contours[i])[0])
                #         #print(i)
                #         print(self.list)     # T_Axis: 5.64 --> leer
                        #print(cv2.fitEllipse(contours[i])[0])
            # 还有别的方法画椭圆中心吗

        


        cv2.namedWindow('ellip',0)
        cv2.resizeWindow('ellip',1000,1000)
        cv2.imshow("ellip", im)

        cv2.namedWindow('ellips',0)
        cv2.resizeWindow('ellips',1000,1000)
        cv2.imshow("ellips", canny)
        1300.6314697265625, 967.3241577148438
        cv2.waitKey()
        
def main():
    rclpy.init()
    image_subscriber = ImageSubscriber()

    rclpy.spin(image_subscriber)
    image_subscriber.destroy_node()
    rclpy.shutdown()
 
if __name__ == "__main__":
    main()
                  #对比 圆 椭圆
#     im = cv2.imread("/home/pmlab/yueju3/robot/Greifer_Unterseitenkamera.bmp")    
#     gray = cv2.cv2tColor(im, cv2.COLOR_BGR2GRAY)    
#     gray2 = cv2.GaussianBlur(gray, (5, 5), 1)
#     #gray2 = cv2.medianBlur(gray, 7)
#     canny = cv2.Canny(gray2, 460, 800) # (460,500)  有些值检测不到
#     _, thresh = cv2.threshold(canny, 140, 220, cv2.THRESH_BINARY)  
#     contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  
#          #最小二乘法拟合椭圆  椭圆检测能检测圆吗 摄像机侧边拍真的是椭圆吗（不倾斜，相互平行）
#          # 检测椭圆内圈？
#     for i in contours:  #sobel? kaolv geng fuza yidian
#         if len(i) >= 5 :
#             retval = cv2.fitEllipse(i)  
#             cv2.ellipse(im, retval, (0, 0, 255), thickness=1) 
#             cv2.circle(im, (int(retval[0][0]),int(retval[0][1])),3, (0, 0, 255), -2)
#             col = cv2.cv2tColor(canny, cv2.COLOR_GRAY2BGR)
#             cv2.drawContours(col, contours, -1, (0, 0, 255), 1)
#             print(retval) 
#         # 还有别的方法画椭圆中心吗
# cv2.namedWindow('ellip',0)
# cv2.resizeWindow('ellip',1000,1000)
# cv2.imshow("ellip", im)

# cv2.namedWindow('ellips',0)
# cv2.resizeWindow('ellips',1000,1000)
# cv2.imshow("ellips", canny)
# 1300.6314697265625, 967.3241577148438
# cv2.waitKey()


# main:  if 走到了特定位置:

#           执行此图像检测程序
