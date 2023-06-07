import cv2
import sys
import cv2
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import time
from rclpy.action import ActionClient
from rclpy.node import Node
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration


class ImageSubscriber(Node):

    def __init__(self):

        super().__init__('image_detection')
        
       
        self.rotate_client = ActionClient(self,FollowJointTrajectory,
                                  '/joint_trajectory_controller/follow_joint_trajectory')
# opencv特定点的追踪
#         https://github.com/makelove/OpenCV-Python-Tutorial/blob/master/my02-%E8%A7%86%E9%A2%91-%E5%AF%B9%E8%B1%A1%E8%B7%9F%E8%B8%AA/tracker.py
#         https://www.cnblogs.com/annie22wang/p/9366610.html
#         https://www.cvmart.net/community/detail/5856
#         https://zhuanlan.zhihu.com/p/479341525
#         https://www.google.com/search?channel=fs&client=ubuntu-sn&q=ros+opencv+%E7%89%B9%E5%AE%9A%E7%82%B9%E8%BF%BD%E8%B8%AA
#         https://www.guyuehome.com/23381/notice.html
#         https://www.guyuehome.com/34967
#         opencv point tracking
#         https://stackoverflow.com/questions/62079484/opencv-tracking-points-in-an-image
#         https://stackoverflow.com/questions/14689090/tracking-user-defined-points-with-opencv



    def listener_callback(self,points):
            
        
    
            # self.get_logger().info('mllllllllllllllllll')
            # else:...
            
            

            target_rotation = JointTrajectoryPoint()
            target_rotation.positions = points
            target_rotation.time_from_start = Duration(sec=6)   # langer for more points detection
            target_rotation.velocities = [0.0]
            target_rotation.accelerations = [0.0]
            
            goal_msg = FollowJointTrajectory.Goal()

            goal_msg.trajectory.joint_names = ['T_Axis_Joint']
            goal_msg.trajectory.points = [target_rotation]
            self.get_logger().info('asdadasdasdasdasdasd')
            # self.rotate_client.wait_for_server() ?


            self.rotate_client.wait_for_server()
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
    time.sleep(3.0)
    rclpy.init()
    image_subscriber = ImageSubscriber()
    image_subscriber.listener_callback([7.3])
    rclpy.spin(image_subscriber)
    #image_subscriber.destroy_node()
    rclpy.shutdown()
 
if __name__ == "__main__":
    main()

 

 
