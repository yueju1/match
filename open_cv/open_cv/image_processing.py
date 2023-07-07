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
from circle_fit import taubinSVD
import numpy as np                #  folge 
 #试一下加不加中值滤波的区别 椒盐噪声    先搞destroy_node 然后看下yaml
# 程序考虑一下顺时针逆时针，想下之前想到的关于顺逆时针的东西。会转出去吗，如果图缩放比例的话
 #也许不需要很复杂， 可能可以通过: 知道图片中 现实点和未来点之前的关系，来求出实际中未来点的位置(也许要用坐标转换)。
   #搞像素坐标转真实的
#     add conditions
class ImageSubscriber(Node):

    def __init__(self):
        #这里面的不报位置吗     
        super().__init__('image_detection')
        # try self.sub
            # if except ...
            #        ...shutdown
            
            # ...
            
            
            
        self.sub = self.create_subscription(JointTrajectoryControllerState,
                                             '/pm_robot_xyz_axis_controller/state',
                                             self.state_callback,
                                             10)
        #  self.subscription  # prevent unused variable warning ?
        self.br = CvBridge()
    
        # self.action_client = ActionClient(self,FollowJointTrajectory,
        #                           '/joint_trajectory_controller/follow_joint_trajectory')
        self.action_client = ActionClient(self,FollowJointTrajectory,
                                  '/pm_robot_xyz_axis_controller/follow_joint_trajectory')
        self.list = []
        self.first_point = []
        self.r_r = 0
        self.m = 0
        self.s = 0
        self. RR = 0
        self.mm = 0
        self.align_action()   # 不写这个行吗
        # self.ok = 0
    def state_callback(self, msg):
        
        # for i in range(4):

                # desired position is meaningful?
        if msg.desired.positions == array.array('d',[-0.359, -0.0458, 0.03, 0.00004]):
            #time.sleep(0.5)
            self.sub = self.create_subscription(Image,
                    '/Camera_Bottom_View/pylon_ros2_camera_node/image_raw',
                    self.detection_callback,
                    10)
                #time.sleep(0.5) 
            self.get_logger().info('Detection callback started') 
            self.rotate_action()
            这边有问题，如何靠程序解决呢
            
        # for i in range(4):
        if msg.desired.positions == array.array('d',[-0.359, -0.0458, 0.03, -0.00008]):
                ZeroDivisionError by -0.00008 am Anfang
            self.fit_ellipse()
            

            # self.return_action()  
            
            #exit(0)
    def return_action(self):
            target_point = JointTrajectoryPoint()
            target_point.positions = [0.0, 0.0, 0.0, 0.0]         # ros::Time::now()  ros2 li shisha
            target_point.time_from_start = Duration(sec= 6) # longer for more point detection 
            # target_point.velocities = [0.0, 0.0, 0.0, 0.0]
            # target_point.accelerations = [0.0, 0.0, 0.0, 0.0]
            # more smoothly: x_joint by 0.08 und y,z,t......
            goal_msg = FollowJointTrajectory.Goal()
            # goal_msg.trajectory.header.stamp = Clock().clock     use_sim_time in launch
        
            goal_msg.trajectory.joint_names = ['X_Axis_Joint','Y_Axis_Joint',
                                            'Z_Axis_Joint','T_Axis_Joint'
                                                ]
            goal_msg.trajectory.points = [target_point]
            # + velocity accelerate  速度和duration2选1吗 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            self.action_client.send_goal_async(goal_msg)

           # exit()


    def detection_callback(self,data):
        self.get_logger().info(f'detection callback')
        #图像处理完了还要在回到原位置，除此以外需要从任意位置开始运动到指定点吗
        im = self.br.imgmsg_to_cv2(data)
        self.get_logger().info(f'detection callback')
        # im = cv2.imread("/home/pmlab/Desktop/Greifer_Unterseitenkamera.bmp")    
        # gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)    
        gray2 = cv2.GaussianBlur(im, (5, 5),1)
        # gray2 = cv2.medianBlur(im, 5)  # 40, 500
        canny = cv2.Canny(gray2, 50, 150,apertureSize=3) # , apertureSize = 3) #(55, 230)
        
        _, thresh = cv2.threshold(canny, 140, 220, cv2.THRESH_BINARY)  
        contours, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  
          
        
        a = []
        b = 0
        c = 0
        m1 = 0
        m2 = 0
        r = 0
        diff = 0
        area = 0
        col = cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)
        for i in range(len(contours)):  #sobel? kaolv geng fuza yidian
            # if len(contours[i]) >= 300 and len(contours[i]) < 330:
            if len(contours[i]) >= 100 and len(contours[i]) <= 500:
                # and len(contours[i]) <= 500
                retval = cv2.fitEllipse(contours[i])  
                
                # 不要launch了，下面的改yaml的改了，再看下畸变比例能不能算，下面fit_ellipse里的
                # if error写一下，不行就运动回去，镜子折射的tf转换搞掉。tf 直接看gazebo运动
             
                #self.get_logger().info('{0}'.format(retval))
                
                  # 就用这个半径， 具体数值看下pixel。 看看哪个是a哪个是b。 
                if retval[1][0] > 105.0 and retval[1][1] < 120.0 and (retval[1][1]-retval[1][0]) <= 5:
                     #if retval[1][0] < 240.0 and retval[1][1] > 100 
                     
                      #  noch durchschnittswert            
                   # print('sdadasdasdasd',contours[i])
                # cv2.ellipse(im, retval, (0, 0, 255), thickness=1) 
                # cv2.circle(im, (int(retval[0][0]),int(retval[0][1])),1, (0, 0, 255), -2)
                    
                    # col = cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)
                    # cv2.drawContours(col, contours, -1, (0, 0, 255), 1)
                    cv2.ellipse(col, retval, (0, 0, 255), thickness=1) 
                    cv2.circle(col, (int(retval[0][0]),int(retval[0][1])),1, (0, 0, 255), -2)

                    a.append(retval)
                    b += retval[0][0]
                    c += retval[0][1]
                    while len(self.first_point) < 1:
                        self.first_point.append(retval)
                    #  成像大小再想想
                    #                  确保第一个ellipse的b
                    r += (retval[1][0]/2 + retval[1][1]/2)/2
                    diff += (retval[1][0]/2 / r)  # or (a-b)/2
                    area += math.pi * retval[1][0]/2 * retval[1][1]/2 

            #         if retval[0] not in self.list:
            #         #if cv2.fitEllipse(contours[i])[0] not in self.list:
            #             # if (m1, m2) not in self.list:
            #                 self.list.append(retval[0])
                    # print(i)
                    # print(retval)
        if len(a) != 0: 
            m1 += b/len(a)
            m2 += c/len(a)
            self.r_r += r/len(a)
            self.m += diff/len(a)
            self.s += area/len(a)
        # print(m1,m2)
        print('length:',len(a))
        print('its b',b)
        # if [m1, m2] not in self.list:
        self.list.append([m1,m2])
        #self.RR = self.r_r/len(self.list)
        self.mm = self.m/len(self.list) 
        
        self.get_logger().info('last mittelpunkt:%s'%self.list[-1])
        #print(self.list)     # T_Axis: 5.64 --> leer
        # self.ok = 1         
                        #print(cv2.fitEllipse(contours[i])[0])
        
        for point in self.list:
    
            cv2.circle(col, (int(point[0]),int(point[1])),1, (0, 0, 255), -2)
        print('-------------------------------------')
        
       # cv2.getRectSubPix(im,)
            # 还有别的方法画椭圆中心吗
        cv2.namedWindow('ellip',0)
        cv2.resizeWindow('ellip',1000,1000)
        cv2.imshow("ellip", col)

        # cv2.namedWindow('ellips',0)
        # cv2.resizeWindow('ellips',1000,1000)
        # cv2.imshow("ellips", canny)
        
        cv2.waitKey(1)
        
    
    def fit_ellipse(self): 
        #self.sim_pixel = 250/self.RR  # reality also define

        sr = math.sqrt(self.s/len(self.list)/math.pi)
        self.sim2 = 250/sr
        self.real_pixel = 2.2
        self.x,self.y,e,r = taubinSVD(self.list)
        # cv2.circle(self.im, (int(self.x),int(self.y)), int(e), (0, 0, 255), 1)
        # cv2.circle(self.im, (int(self.x), int(self.y)), 5, (0, 0, 255), -1)
        
        #if len(self.list) >= 5:
        try:
            points = (np.array(self.list, dtype=np.float32))#.astype(float)
            
            
            data = cv2.fitEllipse(points)
            
            #self.x, self.y = data[0][0], data[0][1] # /1000
            self.error = (self.list[0][0]-self.x, self.list[0][1]-self.y)
            x = self.error[0]*self.error[0]+self.error[1]*self.error[1]
            errer2 = math.sqrt(x)*self.real_pixel


        # cali_x = 1296 + (self.x - 1296)/self.m
        # cali_y = 972 + (self.y - 972)/self.m
        # k = (self.first_point[0][1][0]/2)/((self.first_point[0][1][0]/2+self.first_point[0][1][1]/2)/2)
        # cali_x0 = 1296 + (self.list[0][0] - 1296)/k
        # cali_y0 = 972 + (self.list[0][1] - 972)/k
        # error3 = (cali_x0-cali_x,cali_y0-cali_y)
        # s = error3[0]*error3[0]+error3[1]*error3[1]
        # e4 = math.sqrt(s)*real_pixel
        
            self.get_logger().info('erster mittelpunkt: %s'%self.list[0])
            self.get_logger().info('The center point of Gripper_Rot_Plate is: [{0},{1}]'.format
                                   (self.error[0]*self.real_pixel, self.error[1]*self.real_pixel))
                    #offset: wer relative zu wem: tf , weite zum spiegel
                    
            self.get_logger().info('The error is: {0}'.format(errer2))  #error in x, y
            
        except cv2.error: 
            self.get_logger().error('Error: not enough points collected!')

        except:  # besser machen
            self.get_logger().error('Unknown error!')

        else:
                
            self.adjust_yaml()

        #     return
        # print(data)
               # !!! degree !!!
        
            #return
            
    def adjust_yaml(self):
        # joint_calibration['PM_Robot_Tool_TCP_Joint']['x_offset'] = self.x
    # AttributeError: 'ImageSubscriber' object has no attribute 'x'
        
        yaml = YAML()
    
        with open ("/home/pmlab/pm_ros2_ws/src/match_pm_robot/pm_robot_description/calibration_config/pm_robot_joint_calibration.yaml"
            , "r") as file:
            joint_calibration = yaml.load(file)
                                                                
            joint_calibration['PM_Robot_Tool_TCP_Joint']['x_offset'] = self.error[1]*self.real_pixel  # error(0)-self.x
            joint_calibration['PM_Robot_Tool_TCP_Joint']['y_offset'] = -self.error[0]*self.real_pixel

        with open('/home/pmlab/asd.yaml','w') as new_file:
            yaml.dump(joint_calibration, new_file)
        
        self.get_logger().info('Calibration successful!')
        # except AttributeError:
        #     self.get_logger().error('Error: ')
        值过大：超过100
        asdasdad的东西都清理一遍
        删除不需要的文件
    def align_action(self):
        self.get_logger().info('Align action started!')
        target_point = JointTrajectoryPoint()
        target_point.positions = [-0.359, -0.0458, 0.03, 0.00004]      
        target_point.time_from_start = Duration(sec= 6) # longer for more point detection 
        
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
        error_code = future.result().result.error_code
        if error_code != 0:
            self.get_logger().info(f'Error code: "{error_code}"')
        self.get_logger().info(f'Goal reached!')
        
        # rclpy.shutdown()
        
         # add some conditions ?
      
    def align_callback(self,feedcak_msg):

        self.get_logger().info('Approaching...')


                                                    
    def rotate_action(self):  

            target_rotation = JointTrajectoryPoint()
            target_rotation.positions = [-0.00008]  # because of the offset in x,y, can less than 2pi   !maybe!  if fitellipse() except big point then not necessary
            target_rotation.time_from_start = Duration(sec=8)   # langer for more points detection
            #target_rotation.velocities = [0.0]
            #target_rotation.accelerations = [0.0] # if added, offset in x or y
            
            rotate_msg = FollowJointTrajectory.Goal()

            rotate_msg.trajectory.joint_names = ['T_Axis_Joint']
            rotate_msg.trajectory.points = [target_rotation]
            self.get_logger().info('asdadasdasdasdasdasd')
            # self.action_client.wait_for_server() ?
            
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
   
     

    image_subscriber = ImageSubscriber()
    # rclpy.spin(image_subscriber)

    #future = image_subscriber.rotate_action([-0.7, -0.0458, -0.026791, 1.08]) 
    rclpy.spin(image_subscriber)

    rclpy.shutdown()
    
if __name__ == "__main__":
    main()
