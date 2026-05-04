import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import datetime

class DataSaverNode(Node):
    def __init__(self):
        super().__init__('data_saver_node')
        # /flutter_data 토픽을 구독합니다.
        self.subscription = self.create_subscription(
            String,
            '/flutter_data',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.get_logger().info("데이터 저장 노드가 시작되었습니다. 데이터를 기다리는 중...")

    def listener_callback(self, msg):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{current_time}] 수신된 데이터: {msg.data}\n"
        
        self.get_logger().info(f'저장 중: "{msg.data}"')
        
        # 파일에 저장 (appends to dataFromFlutter.txt)
        with open("/home/msk/ros2_ws/src/my_flutter_pkg/my_flutter_pkg/dataFromFlutter.txt", "a") as f:
            f.write(log_message)

def main(args=None):
    rclpy.init(args=args)
    node = DataSaverNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
