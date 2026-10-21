import json

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MarsTelemetryPublisher(Node):
    def __init__(self):
        super().__init__('mars_telemetry_publisher')

        self.publisher_ = self.create_publisher(
            String,
            '/mars_telemetry',
            10
        )

        self.battery_pct = 100.0
        self.temperature_c = 22.0
        self.mission_elapsed_s = 0
        self.timer = self.create_timer(1.0, self.publish_telemetry)

    def publish_telemetry(self):
        self.mission_elapsed_s += 1
        self.battery_pct = max(0.0, self.battery_pct - 8.0)
        self.temperature_c += 0.5

        telemetry = {
            'battery_pct': round(self.battery_pct, 1),
            'temperature_c': round(self.temperature_c, 1),
            'wheel_speed_mps': 0.25,
            'elapsed_s': self.mission_elapsed_s
        }

        msg = String()
        msg.data = json.dumps(telemetry)
        self.publisher_.publish(msg)

        self.get_logger().info(f'Telemetry: {msg.data}')


def main(args=None):
    rclpy.init(args=args)
    node = MarsTelemetryPublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
