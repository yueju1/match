import time
import rclpy
from rclpy.node import Node

class fdg():
    def abc():
        print(123)

class ImageSubscriber(Node):

     def __init__(self):
        #这里面的不报位置吗     
        super().__init__('image_detecn')
        # time.sleep(6.0)

        self.ok = 1

        # ins= input('asd')
        # if ins == '2':
        #     self.ok = 2

        print(self.ok)




def main():
    rclpy.init()
    image_subscriber = ImageSubscriber()

    rclpy.spin(image_subscriber)
    image_subscriber.destroy_node()
    rclpy.shutdown()
 
if __name__ == "__main__":
    main()