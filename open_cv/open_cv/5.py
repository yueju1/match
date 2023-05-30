import rclpy
from rclpy.node import Node
from control_msgs.msg import JointControllerState


class ImageSubscriber(Node):

    def __init__(self):

        super().__init__('image_detection')
        
        
        self.sub2 = self.create_subscription(JointControllerState,
                                             '/joint_trajectory_controller/state',
                                             self.state_callback,
                                             10)
        

    def state_callback(self, msg):
        print(msg.desired.positions)



def main():
    rclpy.init()
    image_subscriber = ImageSubscriber()

    rclpy.spin(image_subscriber)
    image_subscriber.destroy_node()
    rclpy.shutdown()
 
if __name__ == "__main__":
    main()