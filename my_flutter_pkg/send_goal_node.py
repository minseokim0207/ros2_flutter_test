import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
import json
import os
import time

class SendGoalNode(Node):
    def __init__(self):
        super().__init__('send_goal_node')
        self.publisher = self.create_publisher(PoseStamped, '/goal_pose', 10)
        time.sleep(1.0) 

    def send_goal(self, place_name):
        file_path = f"/home/msk/map_img/{place_name}.json"

        if not os.path.exists(file_path):
            self.get_logger().error(f"❌ 파일을 찾을 수 없습니다: {file_path}")
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            ros_x = float(data['x'])
            ros_y = float(data['y'])

            goal_msg = PoseStamped()
            goal_msg.header.frame_id = 'map' 
            goal_msg.header.stamp = self.get_clock().now().to_msg()

            # 플러터가 계산해준 미터 좌표 입력
            goal_msg.pose.position.x = ros_x
            goal_msg.pose.position.y = ros_y
            goal_msg.pose.position.z = 0.0

            # 로봇 방향 기본값 설정 (정면)
            goal_msg.pose.orientation.x = 0.0
            goal_msg.pose.orientation.y = 0.0
            goal_msg.pose.orientation.z = 0.0
            goal_msg.pose.orientation.w = 1.0

            self.publisher.publish(goal_msg)
            self.get_logger().info(f"🚀 출발! 목적지: {place_name}")
            self.get_logger().info(f"   - 플러터에서 받은 목적지: (x:{ros_x:.2f}m, y:{ros_y:.2f}m)")

        except Exception as e:
            self.get_logger().error(f"오류 발생: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = SendGoalNode()

    print("\n====================================")
    print("🗺️ 로봇 자율주행 목적지 전송 테스트 (Flutter 연산 버전)")
    print("====================================")

    while rclpy.ok():
        place_name = input("이동할 장소 입력 (종료는 'q'): ")
        if place_name.lower() == 'q':
            break
        node.send_goal(place_name)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()