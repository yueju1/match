import rclpy
from rclpy.node import Node
from interface.srv import SetLed


class Battery_node(Node):
    def __init__(self):
        super().__init__("node_battery")
        

    def call_service(self,a):
        self.client=self.create_client(SetLed,"set_led")
        while not self.client.wait_for_service(1.0):
            self.get_logger().warn("waiting...")
        request=SetLed. 
        request.onoroff=a
        future=self.client.call_async(request)
        future.add_done_callback(partial(self.callit,))









def main():
    rclpy. init()
    rclpy.spin()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
