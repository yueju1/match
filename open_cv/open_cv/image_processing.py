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
import numpy as np

# 程序考虑一下顺时针逆时针，想下之前想到的关于顺逆时针的东西。会转出去吗，如果图缩放比例的话
# 也许不需要很复杂， 可能可以通过: 知道图片中 现实点和未来点之前的关系，来求出实际中未来点的位置(也许要用坐标转换)。

#     add conditions
class ImageSubscriber(Node):

    def __init__(self):
        这里面的不报位置吗     在这之前先看下 RETR_EXTERNAL mode
        super().__init__('image_detection')
        
        self.sub2 = self.create_subscription(JointTrajectoryControllerState,
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
        for i in range(4):
            if msg.desired.positions == array.array('d',[-0.359, -0.0458, -0.051544, 0.0]):
                self.sub = self.create_subscription(Image,
                    '/Cam2/image_raw',
                    self.detection_callback,
                    10)
                time.sleep(0.5)  
                self.rotate_action()
        

        # for i in range(4):
        #     if msg.desired.positions == array.array('d',[-0.359, -0.0458, -0.051544, 6.4]):
        #         time.sleep(0.5)
        #         self.fit_ellipse()

    def detection_callback(self,data):
        
        im = self.br.imgmsg_to_cv2(data)
        
        #im = cv2.imread("/home/pmlab/Desktop/Greifer_Unterseitenkamera.bmp")    
        # gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)    
        gray2 = cv2.GaussianBlur(im, (5, 5),1)
        # gray2 = cv2.medianBlur(im, 5)
        canny = cv2.Canny(im, 40, 500) # , apertureSize = 3) #(55, 230)
        _, thresh = cv2.threshold(canny, 140, 220, cv2.THRESH_BINARY)  
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  
            #最小二乘法拟合椭圆  椭圆检测能检测圆吗 摄像机侧边拍真的是椭圆吗（不倾斜，相互平行）
            # 检测椭圆内圈？
        # print(11111111111,np.size(contours))
        a = []
        b = 0
        c = 0
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
            print(i)
            print(retval)
        m1, m2 = b/len(a), c/len(a)
        
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
            
            #轨迹
        print('-------------------------------------')
        self.get_logger().info('%s'%(self.list))
       # cv2.getRectSubPix(im,)
            # 还有别的方法画椭圆中心吗
        cv2.namedWindow('ellip',0)
        cv2.resizeWindow('ellip',1000,1000)
        cv2.imshow("ellip", im)

        # cv2.namedWindow('ellips',0)
        # cv2.resizeWindow('ellips',1000,1000)
        # cv2.imshow("ellips", col)
        
        cv2.waitKey(1)
        
        # im = self.br.imgmsg_to_cv2(data)
        # cv2.namedWindow('ellip',0)
        # cv2.resizeWindow('ellip',1000,1000)
        # cv2.imshow("ellip", im)
        # cv2.waitKey(1)
        # self.get_logger().info('Detecting...')
        # self.ok = 1
        # self.get_logger().info('mokokokokokokokokokokokokok')

    def rotate_action(self): 
        
        #if self.ok == 1:
            
            # self.get_logger().info('mllllllllllllllllll')
            # else:...
            
            

            target_rotation = JointTrajectoryPoint()
            target_rotation.positions = [6.5]
            target_rotation.time_from_start = Duration(sec=6)   # langer for more points detection
            #target_rotation.velocities = [0.0]
            #target_rotation.accelerations = [0.0]
            
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
        # result = future.result().result.points
        self.get_logger().info('Rotation finished!\tThe present position is' )
        
        # rclpy.shutdown()
        
         # add some conditions ?
      
    def feedback_callback(self,feedcak_msg):
        self.get_logger().info('Rotating...')






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
