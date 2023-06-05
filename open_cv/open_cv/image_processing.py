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


程序考虑一下顺时针逆时针，想下之前想到的关于顺逆时针的东西。会转出去吗，如果图缩放比例的话
也许不需要很复杂， 可能可以通过: 知道图片中 现实点和未来点之前的关系，来求出实际中未来点的位置(也许要用坐标转换)。

    add conditions
class ImageSubscriber(Node):

    def __init__(self):

        super().__init__('image_detection')
        
        
        self.sub2 = self.create_subscription(JointTrajectoryControllerState,
                                             '/joint_trajectory_controller/state',
                                             self.state_callback,
                                             10)
        #  self.subscription  # prevent unused variable warning ?
        self.br = CvBridge()
    
        self.rotate_client = ActionClient(self,FollowJointTrajectory,
                                  '/joint_trajectory_controller/follow_joint_trajectory')
        self.ok = 0
    def state_callback(self, msg):
        
        #self.get_logger().info('%s'%msg.actual)
        self.get_logger().info('%s'%msg.desired.positions)
        #self.get_logger().info('%s'%msg.joint_names)
        for i in range(4):
            if msg.desired.positions == array.array('d',[-0.359, -0.0458, -0.051544, 1.08]):
                self.sub = self.create_subscription(Image,
                    '/Cam2/image_raw',
                    self.detection_callback,
                    10)
                self.rotate_action()
        # time.sleep(2.0)   加了这个降频了？  卡

    def detection_callback(self,data):
        
        im = self.br.imgmsg_to_cv2(data)
        cv2.namedWindow('ellip',0)
        cv2.resizeWindow('ellip',1000,1000)
        cv2.imshow("ellip", im)
        cv2.waitKey(1)
        self.get_logger().info('Detecting...')
        self.ok = 1
    

    def rotate_action(self):
        if self.ok == 1:
            # else:...
            time.sleep(0.5)
            self.get_logger().info('asdadasdasdasdasdasd')

            target_rotation = JointTrajectoryPoint()
            target_rotation.positions = [-0.359, -0.0458, -0.051544, 12.0+3.2]
            target_rotation.time_from_start = Duration(sec=4)   # langer for more points detection
            target_rotation.velocities = [0.0, 0.0, 0.0, 0.0]
            target_rotation.accelerations = [0.0, 0.0, 0.0, 0.0]
            
            goal_msg = FollowJointTrajectory.Goal()

            goal_msg.trajectory.joint_names = ['X_Axis_Joint','Y_Axis_Joint',  
                                                'Z_Axis_Joint', 'T_Axis_Joint']
            goal_msg.trajectory.points = [target_rotation]
            
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
        self.get_logger().info('Rotation finished!\nThe present position is %future.actual' )
        
        rclpy.shutdown()
        
         # add some conditions ?
      
    def feedback_callback(self,feedcak_msg):
        self.get_logger().info('Rotating...')






def main():
    rclpy.init()

    image_subscriber = ImageSubscriber()
    # rclpy.spin(image_subscriber)

    #future = image_subscriber.rotate_action([-0.7, -0.0458, -0.026791, 1.08]) 
    rclpy.spin(image_subscriber)

    rclpy.shutdown()
    
if __name__ == "__main__":
    main()
