import rclpy
from rclpy.node import Node
from interface.srv import SetLed
from interface.msg import Led

class Led_panel_node(Node):
    def __init__(self):
        super().__init__("Led_panel")
        self.server_=self.create_service(SetLed,"set_led",self.callback_setled)
        self.pub1_=self.create_publisher(Led,"led_state",10)
        
        self.get_logger().info("Service has been started")
    
    def callback_setled(self,request,response):
         if request.empty:
            response.led_3_state= 1
            response.success=1
            return response
            self.timer_=self.create_timer(6,self.callback_on)
    def callback_on(self):   
        msg=Led()
        msg.led_3=True
        self.pub1_.publish(msg) 
        self.get_logger().info("the set succeeds!")

   
       










def main():
    rclpy.init()
    rclpy.spin(Led_panel_node())
    rclpy.shutdown()


if __name__ == '__main__':
    main()
