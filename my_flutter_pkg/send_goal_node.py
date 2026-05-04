import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped # Nav2가 사용하는 목적지 메시지 타입
import json
import os
import time

class SendGoalNode(Node):
    def __init__(self):
        super().__init__('send_goal_node')
        # '/goal_pose' 토픽으로 데이터를 쏘는 퍼블리셔 생성
        self.publisher = self.create_publisher(PoseStamped, '/goal_pose', 10)

        # (꿀팁) 퍼블리셔가 생성되자마자 쏘면 메시지가 유실될 수 있어 1초 대기합니다.
        time.sleep(1.0) 

    def send_goal(self, place_name):
        file_path = f"/home/msk/map_img/{place_name}.json"

        # 1. 파일 존재 여부 확인
        if not os.path.exists(file_path):
            self.get_logger().error(f"❌ 파일을 찾을 수 없습니다: {file_path}")
            return

        try:
            # 2. JSON 파일 읽어오기
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 3. Nav2 전용 메시지 포장하기
            goal_msg = PoseStamped()
            goal_msg.header.frame_id = 'map'  # 지도를 기준으로 이동하겠다는 뜻
            goal_msg.header.stamp = self.get_clock().now().to_msg()

            # JSON에서 뽑아낸 X, Y 좌표 입력
            goal_msg.pose.position.x = float(data['x'])
            goal_msg.pose.position.y = float(data['y'])
            goal_msg.pose.position.z = 0.0

            # 로봇이 목적지에서 바라볼 방향 (w=1.0 이면 회전 없이 정면을 봄)
            goal_msg.pose.orientation.x = 0.0
            goal_msg.pose.orientation.y = 0.0
            goal_msg.pose.orientation.z = 0.0
            goal_msg.pose.orientation.w = 1.0

            # 4. 토픽 발사!
            self.publisher.publish(goal_msg)
            self.get_logger().info(f"🚀 출발! 목적지: {place_name} (x:{data['x']:.2f}, y:{data['y']:.2f})")

        except Exception as e:
            self.get_logger().error(f"오류 발생: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = SendGoalNode()

    print("\n====================================")
    print("🗺️ 로봇 자율주행 목적지 전송 테스트")
    print("====================================")

    # 터미널에서 계속 입력받으며 테스트할 수 있게 만듭니다.
    while rclpy.ok():
        place_name = input("이동할 장소 입력 (종료는 'q'): ")
        if place_name.lower() == 'q':
            break
        node.send_goal(place_name)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()