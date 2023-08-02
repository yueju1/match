import rclpy
from rclpy.node import Node
from control_msgs.msg import JointTrajectoryControllerState
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import array
from rclpy.action import ActionClient
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint
from builtin_interfaces.msg import Duration
import time
from ruamel.yaml import YAML
import math
from circle_fit import taubinSVD,standardLSQ,hyperLSQ,riemannSWFLa,lm,hyperSVD,kmh,prattSVD
import numpy as np                #  folge 
import inspect
import traceback
 #试一下加不加中值滤波的区别 椒盐噪声    先搞destroy_node 然后看下yaml
# 程序考虑一下顺时针逆时针，想下之前想到的关于顺逆时针的东西。会转出去吗，如果图缩放比例的话
 #也许不需要很复杂， 可能可以通过: 知道图片中 现实点和未来点之前的关系，来求出实际中未来点的位置(也许要用坐标转换)。
   
#     add conditions

class AutoCalibration(Node):

    def __init__(self):
    
        super().__init__('image_detection',allow_undeclared_parameters = True)

        while True:
            
            self.mode =input('Please select the operating mode: \n1: Calibration of the realistic equipment\n2: Calibration in simulation\n')
            
            if self.mode == '1' or self.mode == '2':
                
                Para_real = ('/pm_robot_xyz_axis_controller/state',
                            '/pm_robot_xyz_axis_controller/follow_joint_trajectory',
                            '/Camera_Bottom_View/pylon_ros2_camera_node/image_raw',
                            [-0.359, -0.0458, 0.03, 0.0],
                            [-0.359, -0.0458, 0.03, -1300000.0],
                            [-1300000.0])
                
                Para_sim = ('/joint_trajectory_controller/state',
                            '/joint_trajectory_controller/follow_joint_trajectory',
                            '/Cam2/image_raw',
                            [-0.359, -0.0458, -0.051544, 0.0],
                            [-0.359, -0.0458, -0.051544, 2.27],
                            [2.27])
            
                break

            else: 
                continue
        
        if self.mode == '1':
            self.Parameter = Para_real
        
        if self.mode == '2':
            self.Parameter = Para_sim

        self.get_logger().info('Calibration starting...') 

        self.list = []
        self.r_r = 0
        self.m = 0
        self.s = 0
        self. RR = 0
        self.mm = 0
        print(self.Parameter) 
        self.reached_joint_number = 0    

        self.sub = self.create_subscription(JointTrajectoryControllerState,
                                            self.Parameter[0],
                                            self.state_callback,
                                            10)
        self.br = CvBridge()
        self.get_logger().info('Waiting for controller state...')

        self.timer = self.create_timer(1,self.da_ba)
        self.action_client = ActionClient(self,FollowJointTrajectory,
                                self.Parameter[1])

        #self.align_action() 
        
    def da_ba(self):

        ad = self.get_parameter('ok').value

        if ad == 1:
            self.sub = self.create_subscription(Image,
                    self.Parameter[2],
                    self.detection_callback,
                    10)
        
            #self.rotate_action()
            
            self.timer.cancel()
                
    def state_callback(self, msg):
        
        self.get_logger().info('state_callback')
       
        for i in range(len(msg.actual.positions)):     
            if msg.desired.positions.tolist() == self.Parameter[3] and msg.actual.positions[i] > self.Parameter[3][i]-0.000001 and msg.actual.positions[i] < self.Parameter[3][i]+0.000001:       
                if self.reached_joint_number < i:

                    self.reached_joint_number += 1
                    print(123)
              
                self.get_logger().info('Reached joint number:%s'%self.reached_joint_number)
        
        if self.reached_joint_number == 3:

            print('gogogo') 
            
            self.set_parameters([rclpy.Parameter('ok',value=1)])

        if msg.desired.positions.tolist()[3] == self.Parameter[5][0] and msg.actual.positions[3] > self.Parameter[5][0]-0.000001 and msg.actual.positions[3] < self.Parameter[5][0]+0.000001:
            
            self.reached_joint_number += 1

        # if self.reached_joint_number == 4:

        #     print('backbackbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb') 

        #     self.reached_joint_number = 0 
        #     self.fit_ellipse()

        #     if self.k == ord('s'):
        #         exit(1)
 
    def detection_callback(self,data):

        self.get_logger().info('Detection starts!') 
        print(self.reached_joint_number)
        im = self.br.imgmsg_to_cv2(data)
        gray =cv2.medianBlur(im,9)
        gray2 = cv2.GaussianBlur(im, (3, 3),1.1)
        
        canny = cv2.Canny(gray, 50, 150, apertureSize=3)

        contours, _ = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)  

        a = []
        b = 0
        c = 0
        m1 = 0
        m2 = 0
        r = 0
        diff = 0
        print('lengtg:%s'%len(contours)) 
        self.col = cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)
        cv2.drawContours(self.col,contours,-1, (0, 0, 255), 1)
        for i in range(len(contours)): 

            if len(contours[i]) >= 100 and len(contours[i]) <= 500:
  
                retval = cv2.fitEllipseAMS(contours[i])          
                
                if retval[1][0] > 105.0 and retval[1][1] < 120.0 and (retval[1][1]-retval[1][0]) <= 5:

                    cv2.ellipse(self.col, retval, (0, 0, 255), 1) 
                    cv2.circle(self.col, (int(retval[0][0]),int(retval[0][1])),1, (0, 0, 255), -1)

                    a.append(retval)
                    b += retval[0][0]
                    c += retval[0][1]

                    r += (retval[1][0]/2 + retval[1][1]/2)/2
                    diff += (retval[1][0]/2 / r)  
                    print(retval)

        if len(a) != 0: 
            m1 += b/len(a)
            m2 += c/len(a)
            self.r_r += r/len(a)
            self.m += diff/len(a)
           
        
      
        self.list.append([m1,m2])
        self.RR = self.r_r/len(self.list)
        self.mm = self.m/len(self.list) 
            
        for point in self.list:
    
            cv2.circle(self.col, (int(point[0]),int(point[1])),1, (0, 0, 255), -1)
        print('-------------------------------------')
        
        cv2.namedWindow('ellip',0)
        cv2.resizeWindow('ellip',1000,1000)
        cv2.imshow("ellip", im)

        cv2.waitKey(1)


def main():
    # time.sleep(5.0)
    
    rclpy.init()
   
    # image_subscriber = AutoCalibration()
    # rclpy.spin(image_subscriber)
    #future = image_subscriber.rotate_action([-0.7, -0.0458, -0.026791, 1.08]) 
    #rclpy.spin_once(aasd())
    
    #try:
    rclpy.spin(AutoCalibration())
    

    rclpy.shutdown()
    
if __name__ == "__main__":
    
    # self.mode =input('Please select the operating self.mode: \n1: Calibration of the realistic equipment\n2: Calibration in simulation\n')

    # Para_real = ('/pm_robot_xyz_axis_controller/state',
    #              '/pm_robot_xyz_axis_controller/follow_joint_trajectory',
    #              '/Camera_Bottom_View/pylon_ros2_camera_node/image_raw',
    #              [-0.359, -0.0458, 0.03, -1200000.0],
    #              [-0.359, -0.0458, 0.03, 600000.0],
    #              [600000.0])
    
    # Para_sim = ('/joint_trajectory_controller/state',
    #             '/joint_trajectory_controller/follow_joint_trajectory',
    #             '/Cam2/image_raw',
    #             [-0.359, -0.0458, -0.051544, 0.0],
    #             [-0.359, -0.0458, -0.051544, 6.2],
    #             [6.2])
  
    # if self.mode == '1':
    #     self.Parameter = Para_real
    
    # if self.mode == '2':
    #     self.Parameter = Para_sim
    main()
    # try:
    #     main()
    # except Exception as e: 
    #         Aut().get_logger().info('%s'%e)
