import time
import rclpy
from rclpy.node import Node

class fdg():
    def abc():
        print(123)

class ImageSubscriber(Node):

    def __init__(self):
        #这里面的不报位置吗     
        super().__init__('image_detecn',allow_undeclared_parameters=True)
        # time.sleep(6.0)
        a= self.create_timer(1,self.call_b)
    def call_b(self):
        ak = self.get_parameter('ok').value
        if ak == 2:
            print(123)
      

        # ins= input('asd')
        # if ins == '2':
        #     self.ok = 2

 




def main():
    rclpy.init()
    image_subscriber = ImageSubscriber()

    rclpy.spin(image_subscriber)
    image_subscriber.destroy_node()
    rclpy.shutdown()
 
if __name__ == "__main__":
    main()