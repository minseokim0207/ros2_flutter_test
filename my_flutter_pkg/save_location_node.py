import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json
import os

class LocationSaver(Node):
    def __init__(self):
        super().__init__('location_saver')
        # 플러터에서 보낼 토픽 이름('/save_location')을 구독합니다.
        self.subscription = self.create_subscription(
            String,
            '/save_location',
            self.listener_callback,
            10)
        
        # 저장할 기본 디렉토리 설정
        self.save_dir = "/home/msk/map_img"
        
        # 폴더가 없으면 생성 (안전 장치)
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
            
        self.get_logger().info(f"좌표 저장 대기 중... (저장 경로: {self.save_dir})")

    def listener_callback(self, msg):
        try:
            # 1. 플러터에서 온 JSON 문자열 데이터를 딕셔너리로 변환
            data = json.loads(msg.data)
            place_name = data['name']
            
            # 2. 지정된 경로에 파일 이름 설정 (예: /home/msk/map_img/화장실.json)
            save_path = os.path.join(self.save_dir, f"{place_name}.json")
            
            # 3. 파일로 저장하기 (한글 깨짐 방지를 위해 utf-8 설정)
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                
            self.get_logger().info(f"✨ 성공! 장소가 저장되었습니다: {save_path}")
            
        except Exception as e:
            self.get_logger().error(f"저장 실패: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = LocationSaver()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
