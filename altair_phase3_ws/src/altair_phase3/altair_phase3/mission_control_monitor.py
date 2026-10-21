import json

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MissionControlMonitor(Node):
    def __init__(self):
        super().__init__('mission_control_monitor')

        self.subscription = self.create_subscription(
            String,
            '/mars_telemetry',
            self.telemetry_callback,
            10
        )

    def telemetry_callback(self, msg):
        try:
            data = json.loads(msg.data)

            battery = data['battery_pct']
            temperature = data['temperature_c']
            wheel_speed = data['wheel_speed_mps']
            elapsed = data['elapsed_s']

            self.get_logger().info(
                f'Mission time: {elapsed} s | '
                f'Battery: {battery:.1f}% | '
                f'Internal temperature: {temperature:.1f} °C | '
                f'Wheel speed: {wheel_speed:.2f} m/s'
            )

            if battery < 25.0:
                self.get_logger().warning(
                    f'LOW BATTERY WARNING: {battery:.1f}% remaining!'
                )

        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
            self.get_logger().error(f'Invalid telemetry message: {error}')


def main(args=None):
    rclpy.init(args=args)
    node = MissionControlMonitor()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
