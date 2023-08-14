import rclpy
from rclpy.node import Node
from control_msgs.msg import JointTrajectoryControllerState
from trajectory_msgs.msg import JointTrajectoryPoint
from builtin_interfaces.msg import Duration
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from rclpy.action import ActionClient
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint
from builtin_interfaces.msg import Duration
from ruamel.yaml import YAML
import math
from circle_fit import hyperSVD
import numpy as np               



class AutoCalibration(Node):

    def __init__(self):
    
        super().__init__('image_detection', allow_undeclared_parameters = True)

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
        self.r = 0 
        self.R = 0
        self.reached_joint_number = 0    

        self.sub = self.create_subscription(JointTrajectoryControllerState,
                                            self.Parameter[0],
                                            self.state_callback,
                                            10)
        
        self.br = CvBridge()
        
        self.get_logger().info('Waiting for controller state...')

        self.timer = self.create_timer(1,self.check_callback)
        
        self.action_client = ActionClient(self,FollowJointTrajectory,
                                self.Parameter[1])

        self.align_action() 
        
    def check_callback(self):

        check = self.get_parameter('ok').value

        if check == 1:
            self.sub = self.create_subscription(Image,
                    self.Parameter[2],
                    self.detection_callback,
                    10)
        
            self.rotate_action()
            
            self.timer.cancel()
                
    def state_callback(self, msg):
        
        self.get_logger().info('state_callback')
       
        for i in range(len(msg.actual.positions)):     
            if msg.desired.positions.tolist() == self.Parameter[3] and msg.actual.positions[i] > self.Parameter[3][i]-0.000001 and msg.actual.positions[i] < self.Parameter[3][i]+0.000001:       
                if self.reached_joint_number < i:

                    self.reached_joint_number += 1
              
                self.get_logger().info('Reached joint number:%s'%self.reached_joint_number)
        
        if self.reached_joint_number == 3:
            
            self.set_parameters([rclpy.Parameter('ok',value=1)])

        if msg.desired.positions.tolist()[3] == self.Parameter[5][0] and msg.actual.positions[3] > self.Parameter[5][0]-0.000001 and msg.actual.positions[3] < self.Parameter[5][0]+0.000001:
            
            self.reached_joint_number += 1

        if self.reached_joint_number == 4:

            self.reached_joint_number = 0 
            
            self.fit_ellipse()

            if self.k == ord('s'):
                exit(1)
 
    def detection_callback(self,data):

        self.get_logger().info('Detection starts!') 

        img = self.br.imgmsg_to_cv2(data)
        
        median = cv2.medianBlur(img,9)

        canny = cv2.Canny(median, 50, 150, apertureSize=3, L2gradient=True)

        contours, _ = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)  

        ellipse = []
        x = 0
        y = 0
        m1 = 0
        m2 = 0
        r = 0
          
        self.col = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        for i in range(len(contours)): 

            if len(contours[i]) >= 100 and len(contours[i]) <= 500:
  
                retval = cv2.fitEllipseDirect(contours[i])          
                
                if retval[1][0] > 105.0 and retval[1][1] < 120.0 and (retval[1][1]-retval[1][0]) <= 5:

                    cv2.ellipse(self.col, retval, (0, 0, 255), 1) 
                    cv2.circle(self.col, (int(retval[0][0]),int(retval[0][1])),1, (0, 0, 255), -1)

                    ellipse.append(retval)
                    x += retval[0][0]
                    y += retval[0][1]

                    r += (retval[1][0]/2 + retval[1][1]/2)/2
                  
        if len(ellipse) != 0: 
            m1 += x/len(ellipse)
            m2 += y/len(ellipse)
            self.r += r/len(ellipse)
           
        self.list.append([m1,m2])
        self.R = self.r/len(self.list)
            
        for point in self.list:
        
            cv2.circle(self.col, (int(point[0]), int(point[1])), 1, (0, 0, 255), -1)
        
        cv2.namedWindow('Circle',0)
        cv2.resizeWindow('Circle',1000,1000)
        cv2.imshow('Circle', self.col)
        cv2.waitKey(1)
        
    def fit_ellipse(self): 

        self.real_pixel_size = 2.2
        self.sim_pixel_size = 250/self.R
        
        if self.mode == '1':
            
            self.pixel_size = self.real_pixel_size

        elif self.mode == '2':
            
            self.pixel_size = self.sim_pixel_size
        
        self.x,self.y,e,_ = hyperSVD(self.list)
    
        cv2.circle(self.col, (int(self.x),int(self.y)),1, (0, 0, 255), -1)
        cv2.circle(self.col, (int(self.x),int(self.y)),int(e), (0, 0, 255), 1)
        
        cv2.namedWindow('Circle',0)
        cv2.resizeWindow('Circle',1000,1000)
        cv2.imshow('Circle', self.col)

        self.k =cv2.waitKey(0)
        
        self.error = (self.list[0][0]-float(self.x), self.list[0][1]-float(self.y))
        square = self.error[0]*self.error[0]+self.error[1]*self.error[1]
        deviation = math.sqrt(square)*self.pixel_size

        self.get_logger().info('Predicted center of the red plate in the image coordinate : ({0},{1})'.format(self.x,self.y))
        self.get_logger().info('Position of the vacuum gripper relative to the red plate: ({0},{1}) (µm)'.format
                                (self.error[0]*self.pixel_size, -self.error[1]*self.pixel_size))             
        self.get_logger().info('The error is: {0} µm'.format(deviation))
          
        self.adjust_yaml()
             
    def adjust_yaml(self):
        
        yaml = YAML()
   
        with open ("/home/pmlab/pm_ros2_ws/src/match_pm_robot/pm_robot_description/calibration_config/pm_robot_joint_calibration.yaml"
            , "r") as file:
            joint_calibration = yaml.load(file)
                                                                
            joint_calibration['PM_Robot_Tool_TCP_Joint']['x_offset'] = self.error[0]*self.pixel_size  
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
                                        'Z_Axis_Joint','T_Axis_Joint' ]
        goal_msg.trajectory.points = [target_point]
        
        self.action_client.wait_for_server()
        
        self.send_goal_future = self.action_client.send_goal_async(goal_msg
                                                                  ,feedback_callback=self.align_callback)
        self.send_goal_future.add_done_callback(self.align_response_callback)

    def align_response_callback(self, future):
     
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected.') 
            print(future.exception())
            return                      
        
        self.get_logger().info('Goal accepted.')
        
        self.get_result_future = goal_handle.get_result_async()
        self.get_result_future.add_done_callback(self.align_result_callback)

    def align_result_callback(self, future):
        
        self.get_logger().info('Goal reached!')
   
    def align_callback(self, feedback_msg):

        self.get_logger().info('Approaching...')
                                                    
    def rotate_action(self):  
        
            self.get_logger().info('Starting ratation...')
            
            target_rotation = JointTrajectoryPoint()
            
            target_rotation.positions = self.Parameter[5] 
            
            if self.mode == '2':
                target_rotation.time_from_start = Duration(sec=6)   
           
            
            rotate_msg = FollowJointTrajectory.Goal()

            rotate_msg.trajectory.joint_names = ['T_Axis_Joint']
            rotate_msg.trajectory.points = [target_rotation]
           
            self.action_client.wait_for_server()
            
            self.send_goal_future = self.action_client.send_goal_async(rotate_msg
                                                                  ,feedback_callback=self.feedback_callback)
            self.send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Rotation rejected.') 
            print(future.exception())
            return                      
        
        self.get_logger().info('Rotation starts.')
        
        self.get_result_future = goal_handle.get_result_async()
        self.get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):

        self.get_logger().info('Rotation finished!')
      
    def feedback_callback(self,feedback_msg):
        
        feedback = feedback_msg.feedback
        
        self.get_logger().info('Rotating...')
        
        position =  np.array(feedback.actual.positions).tolist()
        
        self.get_logger().info('The present position is: %s'%(position))

    

def main():
    
    rclpy.init()
    rclpy.spin(AutoCalibration())
    rclpy.shutdown()
    
if __name__ == "__main__":
    
    main()
