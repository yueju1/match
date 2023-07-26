import cv2
from rcl_interfaces.msg import SetParametersResult
import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from control_msgs.msg import JointControllerState
import numpy as np
import time
import os
from rcl_interfaces.msg import ParameterEvent


class ImageSubscriber(Node):
 
    def __init__(self):

        super().__init__('image_detection')
        print(123)
        self.subscription = self.create_subscription(
            Image,
            '/Cam1/image_raw',
            self.listener_callback,
            10)
        print(234)
        #self.subscription  # prevent unused variable warning

        self.br = CvBridge()
    # is the callbackfunction a must?
        self.list = []
                                                                 #     1483 943     1365 943
    def listener_callback(self, data):
        print(345)
        a = []
        b = 0
        c = 0
        m1 = 0
        m2 = 0

        #self.im = self.br.imgmsg_to_cv2(data)
        
        self.im = cv2.imread("/home/yueju/下载/_cgi-bin_mmwebwx-bin_webwxgetmsgimg &MsgID=8469812677115518599&skey=@crypt_8a8c9738_b2b65b258a21ea87ec9e30ab9adc417b&mmweb_appid=wx_webfilehelper.jpeg")    
        # gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)    
        #gray2 = cv2.GaussianBlur(self.im, (5, 5),1)
        gray2 = cv2.medianBlur(self.im, 7)
        #gray2 = cv2.bilateralFilter(im, d=5, sigmaColor=50, sigmaSpace=50)
        canny = cv2.Canny(self.im, 40, 500,apertureSize=3) # , apertureSize = 3) #(55, 230)   # 5,15
        
        print(123)
        
        _, thresh = cv2.threshold(canny, 140, 120, cv2.THRESH_BINARY)  # ret
        
        contours, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  
            #最小二乘法拟合椭圆  椭圆检测能检测圆吗 摄像机侧边拍真的是椭圆吗（不倾斜，相互平行）
            # 检测椭圆内圈？
        #print(11111111111,np.size(contours))
        
        print(contours)
        col = cv2.cvtColor(canny, cv2.COLOR_GRAY2BGR)
        for i in range(len(contours)) :  
            print(123)#sobel? kaolv geng fuza yidian
            # if len(contours[i]) >= 300 and len(contours[i]) < 330:
            if len(contours[i]) >= 5:# and len(contours[i]) <= 120:
                #print(222222222222,np.size(contours))
                #print(hierarchy)
                print('asdasdadasd')


                retval = cv2.fitEllipse(contours[i])  
                
                cv2.ellipse(col, retval, (0, 0, 255), thickness=1) 
                cv2.circle(col, (int(retval[0][0]),int(retval[0][1])),1, (0, 0, 255), -2)
                
                
                
                cv2.drawContours(col, contours, -1, (0, 0, 255), 1)
                # cv2.namedWindow('ellip',0)
                # cv2.resizeWindow('ellip',1200,1100)
                # cv2.imshow("ellip", self.im)
                # cv2.waitKey(0)


                print(retval)
                
                  # 就用这个半径， 具体数值看下pixel。 看看哪个是a哪个是b。 
                if retval[1][0] < 240.0 and retval[1][1] > 100 and (retval[1][1]- retval[1][0]) <= 10:
                      #  noch durchschnittswert            
                   # print('sdadasdasdasd',contours[i])
                    a.append(retval)
                    b += retval[0][0]
                    c += retval[0][1]
                    
            #         if retval[0] not in self.list:
            #         #if cv2.fitEllipse(contours[i])[0] not in self.list:
            #             # if (m1, m2) not in self.list:
            #                 self.list.append(retval[0])
            # print(i)
        
        if len(a) != 0:
            m1 += b/len(a)
            m2 += c/len(a)
        
        #print(m1,m2)
        print('length:',len(a))
        print('its b',b)
        if [m1, m2] not in self.list:
            self.list.append([m1,m2])
        
        print(self.list)     # T_Axis: 5.64 --> leer
                    
                        #print(cv2.fitEllipse(contours[i])[0])
        for point in self.list:
    
            cv2.circle(self.im, (int(point[0]),int(point[1])),1, (0, 0, 255), -2)
            
            #轨迹
        print('-------------------------------------')

        
        
       # cv2.getRectSubPix(im,)
            # 还有别的方法画椭圆中心吗
        
        # cv2.namedWindow('ellips',0)
        # cv2.resizeWindow('ellips',1200,1100)
        # cv2.imshow("ellips", canny)

        cv2.namedWindow('ellip',0)
        cv2.resizeWindow('ellip',1200,1100)
        cv2.imshow("ellip", col)
        
        
        
        cv2.waitKey(0)
    
     # first detection finished then fitellipse
    def fit_ellipse(self): # codition in image_processing.py
        
        
        self.get_logger().info('qweweqweqweqweqweqweqwe')
        points = (np.array(self.list)*1000).astype(int)
        data = cv2.fitEllipse(points)
        x,y = data[0][0]/1000, data[0][1]/1000
        
        self.get_logger().info('%s'%points)
        

def main():
    rclpy.init()
    image_subscriber = ImageSubscriber()

    rclpy.spin(image_subscriber)
    #image_subscriber.destroy_node()
    rclpy.shutdown()
    
if __name__ == "__main__":
    
    main()
    
    
