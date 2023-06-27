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
        
        self.sub = self.create_subscription(JointTrajectoryControllerState,
                                             '/joint_trajectory_controller/state',
                                             self.state_callback,
                                             10)
        #  self.subscription  # prevent unused variable warning ?
        self.br = CvBridge()
    
        self.rotate_client = ActionClient(self,FollowJointTrajectory,
                                  '/joint_trajectory_controller/follow_joint_trajectory')
        self.list = []
        # self.ok = 0
    def state_callback(self, msg):
        
        #self.get_logger().info('%s'%msg.actual)
        #self.get_logger().info('%s'%msg.desired.positions)
        #self.get_logger().info('%s'%msg.joint_names)
        # for i in range(4):
        if msg.desired.positions == array.array('d',[-0.359, -0.0458, -0.051544, 0.0]):
            self.sub = self.create_subscription(Image,
                    '/Cam2/image_raw',
                    self.detection_callback,
                    10)
                #time.sleep(0.5)  
            self.rotate_action()

        # for i in range(4):
        if msg.desired.positions == array.array('d',[-0.359, -0.0458, -0.051544, 6.4]):
            #time.sleep(0.5)
            
            self.fit_ellipse()
                
            #exit(0)

    def detection_callback(self,data):
        #图像处理完了还要在回到原位置，除此以外需要从任意位置开始运动到指定点吗
        im = self.br.imgmsg_to_cv2(data)
        
        # im = cv2.imread("/home/pmlab/Desktop/Greifer_Unterseitenkamera.bmp")    
        # gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)    
        gray2 = cv2.GaussianBlur(im, (5, 5),1)
        # gray2 = cv2.medianBlur(im, 5)
        canny = cv2.Canny(im, 40, 500,apertureSize=3) # , apertureSize = 3) #(55, 230)
        _, thresh = cv2.threshold(canny, 140, 220, cv2.THRESH_BINARY)  
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  
            #最小二乘法拟合椭圆  椭圆检测能检测圆吗 摄像机侧边拍真的是椭圆吗（不倾斜，相互平行）
            # 检测椭圆内圈？
        # print(11111111111,np.size(contours))
        a = []
        b = 0
        c = 0
        m1 = 0
        m2 = 0

        for i in range(len(contours)):  #sobel? kaolv geng fuza yidian
            # if len(contours[i]) >= 300 and len(contours[i]) < 330:
            if len(contours[i]) >= 100 and len(contours[i]) <= 200:
                
                print(hierarchy)
                retval = cv2.fitEllipse(contours[i])  
                
                cv2.ellipse(im, retval, (0, 0, 255), thickness=1) 
                cv2.circle(im, (int(retval[0][0]),int(retval[0][1])),1, (0, 0, 255), -2)
                
                col = cv2.cvtColor(canny, cv2.COLOR_GRAY2BGR)
                cv2.drawContours(col, contours, -1, (0, 0, 255), 1)
             
                # print(retval)
                
                  # 就用这个半径， 具体数值看下pixel。 看看哪个是a哪个是b。 
                if retval[1][0] < 240.0 and retval[1][1] > 100 and (retval[1][1]-retval[1][0]) <= 10:
                      #  noch durchschnittswert            
                   # print('sdadasdasdasd',contours[i])
                    a.append(retval)
                    b += retval[0][0]
                    c += retval[0][1]
                    
            #         if retval[0] not in self.list:
            #         #if cv2.fitEllipse(contours[i])[0] not in self.list:
            #             # if (m1, m2) not in self.list:
            #                 self.list.append(retval[0])
                #print(i)
               # print(retval)
        if len(a) != 0:
            m1 += b/len(a)
            m2 += c/len(a)
        
        print(m1,m2)
        print('length:',len(a))
        print('its b',b)
        if [m1, m2] not in self.list:
            self.list.append([m1,m2])
        
        # print(self.list)     # T_Axis: 5.64 --> leer
        # self.ok = 1         
                        #print(cv2.fitEllipse(contours[i])[0])
        for point in self.list:
    
            cv2.circle(im, (int(point[0]),int(point[1])),1, (0, 0, 255), -2)
        print('-------------------------------------')
        #self.get_logger().info('%s'%(self.list))
       # cv2.getRectSubPix(im,)
            # 还有别的方法画椭圆中心吗
        cv2.namedWindow('ellip',0)
        cv2.resizeWindow('ellip',1000,1000)
        cv2.imshow("ellip", im)

        # cv2.namedWindow('ellips',0)
        # cv2.resizeWindow('ellips',1000,1000)
        # cv2.imshow("ellips", canny)
        
        cv2.waitKey(1)
        
        # im = self.br.imgmsg_to_cv2(data)
        # cv2.namedWindow('ellip',0)
        # cv2.resizeWindow('ellip',1000,1000)
        # cv2.imshow("ellip", im)
        # cv2.waitKey(1)

    def fit_ellipse(self): # codition in image_processing.py
       
        #if len(self.list) >= 5:
        try:
            points = (np.array(self.list,dtype=np.float32))#.astype(float)
            #print(1232131231, type(self.list[1][1]))
            print(points)
            print(type(points))
            data = cv2.fitEllipse(points)
            print(data)
            self.x, self.y = data[0][0], data[0][1] # /1000
            error = (self.x - self.list[0][0], self.y - self.list[0][1])
            # self.get_logger().info('%s'%points)
            self.get_logger().info('%s'%self.list[0])
            self.get_logger().info('The center point of Gripper_Rot_Plate is: [{0},{1}]'.format(self.x,self.y))
            self.get_logger().info('The error is: {0}'.format(error))  #error in x, y
        except cv2.error: 
            self.get_logger().error('Error: not enough points collected!')

        except:
            self.get_logger().error('Unknown error!')

        else:
            self.adjust_yaml()
        # print(data)
               # !!! degree !!!
        
            #return
            
    def adjust_yaml(self):
        # joint_calibration['PM_Robot_Tool_TCP_Joint']['x_offset'] = self.x
    # AttributeError: 'ImageSubscriber' object has no attribute 'x'
        
        yaml = YAML()
    
        with open ("/home/pmlab/ros2_ws/src/match_pm_robot/pm_robot_description/calibration_config/pm_robot_joint_calibration.yaml"
            , "r") as file:
            joint_calibration = yaml.load(file)
                                                                
            joint_calibration['PM_Robot_Tool_TCP_Joint']['x_offset'] = self.x
            joint_calibration['PM_Robot_Tool_TCP_Joint']['y_offset'] = self.y

        with open('/home/pmlab/asd.yaml','w') as new_file:
            yaml.dump(joint_calibration, new_file)
        
        self.get_logger().info('Calibration successful!')
        # except AttributeError:
        #     self.get_logger().error('Error: ')


        
    def rotate_action(self):  

            target_rotation = JointTrajectoryPoint()
            target_rotation.positions = [6.4]  # because of the offset in x,y, can less than 2pi   !maybe!  if fitellipse() except big point then not necessary
            target_rotation.time_from_start = Duration(sec=8)   # langer for more points detection
            #target_rotation.velocities = [0.0]
            #target_rotation.accelerations = [0.0] # if added, offset in x or y
            
            goal_msg = FollowJointTrajectory.Goal()

            goal_msg.trajectory.joint_names = ['T_Axis_Joint']
            goal_msg.trajectory.points = [target_rotation]
            self.get_logger().info('asdadasdasdasdasdasd')
            # self.rotate_client.wait_for_server() ?
            
            self.send_goal_future = self.rotate_client.send_goal_async(goal_msg
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
