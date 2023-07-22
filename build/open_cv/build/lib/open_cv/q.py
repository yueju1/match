import rclpy
import rclpy.node

class MinimalParam(rclpy.node.Node):
    def __init__(self):
        super().__init__('minimal_param_node')
        
        self.declare_parameter('my_parameter', 'world')

        self.timer = self.create_timer(1, self.timer_callback)
        self.get_logger().info('asdasd')
    def timer_callback(self):
        self._allow_undeclared_parameters
        par = self.get_parameter('my_parameter').value
        print(234)
        # if par == 'world':
        #     self.timer.cancel()
        if par == 1:
            print(123)
        
def main():
    rclpy.init()
    node = MinimalParam()
    rclpy.spin(node)

if __name__ == '__main__':
    main()