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
                            [-0.359, -0.0458, -0.051544, 6.2],
                            [6.2])
            
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

        self.align_action() 
        
    def da_ba(self):

        ad = self.get_parameter('ok').value

        if ad == 1:
            self.sub = self.create_subscription(Image,
                    self.Parameter[2],
                    self.detection_callback,
                    10)
        
            self.rotate_action()
            
            self.timer.cancel()
                
    def state_callback(self, msg):
        
        #self.get_logger().info('state_callback')
       
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

        if self.reached_joint_number == 4:

            print('backbackbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb') 

            self.reached_joint_number = 0 
            self.fit_ellipse()

            if self.k == ord('s'):
                exit(1)
 
    def detection_callback(self,data):



        im = self.br.imgmsg_to_cv2(data)
        
        gray2 = cv2.GaussianBlur(im, (5, 5),1)

        canny = cv2.Canny(gray2, 50, 150, apertureSize=3)

        contours, _ = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)  

        a = []
        b = 0
        c = 0
        m1 = 0
        m2 = 0
        r = 0
        diff = 0
        
        self.col = cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)
        print('length of contours',len(contours))
        #cv2.drawContours(self.col,contours,-1, (0, 0, 255), 1)
        for i in range(len(contours)): 

            if len(contours[i]) >= 100 and len(contours[i]) <= 500:
  
                retval = cv2.fitEllipseDirect(contours[i])          
                
                if retval[1][0] > 104.0 and retval[1][1] < 118.0 and (retval[1][1]-retval[1][0]) <= 2.0:

                    cv2.ellipse(self.col, retval, (0, 0, 255), 1) 
                    cv2.circle(self.col, (int(retval[0][0]),int(retval[0][1])),1, (0, 0, 255), -1)

                    a.append(retval)
                    b += retval[0][0]
                    c += retval[0][1]

                    r += (retval[1][0]/2 + retval[1][1]/2)/2
                    diff += (retval[1][0]/2 / r)  
                  

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
        cv2.imshow("ellip", self.col)

        cv2.waitKey(1)
        
    
    def fit_ellipse(self): 

        self.real_pixel_size = 2.2
        self.sim_pixel_size = 250/self.RR
        
        if self.mode == '1':
            
            self.pixel_size = self.real_pixel_size

        elif self.mode == '2':
            
            self.pixel_size = self.sim_pixel_size
        
        #self.x,self.y,e,r = taubinSVD(self.list)
        self.x,self.y,e,r = taubinSVD(self.list)
        # cv2.circle(self.im, (int(self.x),int(self.y)), int(e), (0, 0, 255), 1)
        # cv2.circle(self.im, (int(self.x), int(self.y)), 5, (0, 0, 255), -1)

        # points = np.array(self.list)*1000
        # points = np.array(points).astype(int)

        points = np.array(self.list, dtype=np.float32)#.astype(int)
                    
        data = cv2.fitEllipse(points)
        self.get_logger().info('{0}'.format(data))

        # cv2.ellipse(self.col, data, (0, 0, 255), thickness=1) 
        cv2.circle(self.col, (int(data[0][0]),int(data[0][1])),1, (0, 0, 255), -1)
        cv2.circle(self.col, (int(data[0][0]),int(data[0][1])),int((data[1][0]/2+data[1][1]/2)/2), (0, 0, 255), -1)
        # cv2.circle(self.col, (int(self.x),int(self.y)),1, (0, 0, 255), -2)
        # cv2.circle(self.col, (int(self.x),int(self.y)),int(e), (0, 0, 255), 2)
        cv2.namedWindow('ellip',0)
        cv2.resizeWindow('ellip',1000,1000)
        cv2.imshow("ellip", self.col)

        self.k =cv2.waitKey(0)
        
        
        #self.x, self.y = data[0][0], data[0][1] # /1000
        self.error = (self.list[0][0]-float(self.x), self.list[0][1]-float(self.y))
        square = self.error[0]*self.error[0]+self.error[1]*self.error[1]
        deviation = math.sqrt(square)*self.pixel_size

    # cali_x = 1296 + (self.x - 1296)/self.m
    # cali_y = 972 + (self.y - 972)/self.m
    # k = (self.first_point[0][1][0]/2)/((self.first_point[0][1][0]/2+self.first_point[0][1][1]/2)/2)
    # cali_x0 = 1296 + (self.list[0][0] - 1296)/k
    # cali_y0 = 972 + (self.list[0][1] - 972)/k
    # error3 = (cali_x0-cali_x,cali_y0-cali_y)
    # s = error3[0]*error3[0]+error3[1]*error3[1]
    # e4 = math.sqrt(s)*real_pixel
        self.get_logger().info('real mitte[{0},{1}]'.format(self.x,self.y))
        self.get_logger().info('erster mittelpunkt: %s'%self.list[0])
        self.get_logger().info('The center point of Gripper_Rot_Plate is: [{0},{1}]'.format
                                (self.error[0]*self.pixel_size, self.error[1]*self.pixel_size))             
        self.get_logger().info('The error is: {0}'.format(deviation))  #error in x, y
          
        self.adjust_yaml()
            
    def adjust_yaml(self):
        
        yaml = YAML()
   
        with open ("/home/pmlab/pm_ros2_ws/src/match_pm_robot/pm_robot_description/calibration_config/pm_robot_joint_calibration.yaml"
            , "r") as file:
            joint_calibration = yaml.load(file)
                                                                
            joint_calibration['PM_Robot_Tool_TCP_Joint']['x_offset'] = self.error[0]*self.pixel_size  # error(0)-self.x
            joint_calibration['PM_Robot_Tool_TCP_Joint']['y_offset'] = -self.error[1]*self.pixel_size

        with open('/home/pmlab/asd.yaml','w') as new_file:
            yaml.dump(joint_calibration, new_file)
        
        self.get_logger().info('Calibration successful!')

    def align_action(self):
        self.get_logger().info('Starting align...')
        target_point = JointTrajectoryPoint()
        target_point.positions = self.Parameter[3]     
        if self.mode == '2':
            target_point.time_from_start = Duration(sec= 6)

        goal_msg = FollowJointTrajectory.Goal()
        
        goal_msg.trajectory.joint_names = ['X_Axis_Joint','Y_Axis_Joint',
                                        'Z_Axis_Joint','T_Axis_Joint'
                                            ]
        goal_msg.trajectory.points = [target_point]
        
        self.action_client.wait_for_server()
        self.send_goal_future = self.action_client.send_goal_async(goal_msg
                                                                  ,feedback_callback=self.align_callback)
        self.send_goal_future.add_done_callback(self.align_response_callback)


    def align_response_callback(self, future):
        #goal_handle = future.re
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected.') # add error type
            print(future.exception())
            return                      # 校准多个bauteil看下这里的 if not 循环
        
        self.get_logger().info('Goal accepted.')
        self.get_result_future = goal_handle.get_result_async()
        self.get_result_future.add_done_callback(self.align_result_callback)

    
    def align_result_callback(self,future):
        # error_code = future.result().result.error_code
        # if error_code != 0:
        #     self.get_logger().info(f'Error code: "{error_code}"')
        self.get_logger().info('Goal reached!')
        
        # rclpy.shutdown()
        
         # add some conditions ?
      
    def align_callback(self,feedcak_msg):

        self.get_logger().info('Approaching...')
                                                    
    def rotate_action(self):  
            self.get_logger().info('Starting ratation...')
            target_rotation = JointTrajectoryPoint()
            target_rotation.positions = self.Parameter[5]  # because of the offset in x,y, can less than 2pi   !maybe!  if fitellipse() except big point then not necessary
            if self.mode == '2':
                target_rotation.time_from_start = Duration(sec=8)   # langer for more points detection
            #target_rotation.velocities = [0.0]
            #target_rotation.accelerations = [0.0] # if added, offset in x or y
            
            rotate_msg = FollowJointTrajectory.Goal()

            rotate_msg.trajectory.joint_names = ['T_Axis_Joint']
            rotate_msg.trajectory.points = [target_rotation]
           
            self.action_client.wait_for_server()
            
            self.send_goal_future = self.action_client.send_goal_async(rotate_msg
                                                                  ,feedback_callback=self.feedback_callback)
            self.send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        #goal_handle = future.re
        
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Rotation rejected.') # add error type
            print(future.exception())
            return                      # 校准多个bauteil看下这里的 if not 循环
        
        self.get_logger().info('Rotation starts.')
        self.get_result_future = goal_handle.get_result_async()
        self.get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self,future):
        result = future.result().result
        self.get_logger().info('Rotation finished!')
        
        # rclpy.shutdown()
        
         # add some conditions ?
      
    def feedback_callback(self,feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info('Rotating...')
        position =  np.array(feedback.actual.positions).tolist()
        self.get_logger().info('The present position is: %s'%(position) )
        # value of velocity is not 0
    


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
