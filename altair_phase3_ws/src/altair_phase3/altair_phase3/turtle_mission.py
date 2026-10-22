import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from std_msgs.msg import Bool
from std_srvs.srv import Trigger


class TurtleMission(Node):
    def __init__(self):
        super().__init__('turtle_mission')

        self.pose = None
        self.blocked = False
        self.paused = False
        self.finished = False
        self.target_index = 0

        self.targets = [
            ('Bottle', 8.0, 5.5),
            ('Mallet', 8.0, 8.0),
            ('Base', 5.5, 5.5),
        ]

        self.pose_sub = self.create_subscription(
            Pose, '/turtle1/pose', self.pose_callback, 10
        )
        self.blocked_sub = self.create_subscription(
            Bool, '/field_blocked', self.blocked_callback, 10
        )

        self.cmd_pub = self.create_publisher(
            Twist, '/turtle1/cmd_vel', 10
        )

        self.resume_service = self.create_service(
            Trigger, '/resume_mission', self.resume_callback
        )

        self.timer = self.create_timer(0.1, self.control_loop)

        self.get_logger().info('Mission ready. Waiting for turtle pose.')

    def pose_callback(self, msg):
        self.pose = msg

    def blocked_callback(self, msg):
        self.blocked = msg.data

        if self.blocked and not self.finished:
            if not self.paused:
                self.get_logger().warn('FIELD BLOCKED: mission paused.')
            self.paused = True

        elif not self.blocked:
            self.get_logger().info(
                'Field clear. Call /resume_mission to continue.'
            )

    def resume_callback(self, request, response):
        if self.finished:
            response.success = False
            response.message = 'Mission already finished.'
        elif self.blocked:
            response.success = False
            response.message = 'Cannot resume: field is still blocked.'
        elif not self.paused:
            response.success = False
            response.message = 'Mission is not paused.'
        elif self.pose is None:
            response.success = False
            response.message = 'Cannot resume: waiting for turtle pose.'
        else:
            self.paused = False
            response.success = True
            response.message = 'Mission resumed.'
            self.get_logger().info(response.message)

        return response

    def publish_stop(self):
        self.cmd_pub.publish(Twist())

    def control_loop(self):
        if self.finished:
            self.publish_stop()
            return

        if self.pose is None:
            self.publish_stop()
            return

        if self.blocked or self.paused:
            self.publish_stop()
            return

        name, target_x, target_y = self.targets[self.target_index]

        dx = target_x - self.pose.x
        dy = target_y - self.pose.y
        distance = math.sqrt(dx * dx + dy * dy)

        cmd = Twist()

        if distance < 0.15:
            self.publish_stop()
            self.get_logger().info(f'ARRIVED: {name}')

            if self.target_index == len(self.targets) - 1:
                self.finished = True
                self.get_logger().info('DONE: all targets reached.')
            else:
                self.target_index += 1

            return

        desired_angle = math.atan2(dy, dx)
        angle_error = math.atan2(
            math.sin(desired_angle - self.pose.theta),
            math.cos(desired_angle - self.pose.theta)
        )

        if abs(angle_error) > 0.15:
            cmd.angular.z = 2.0 * angle_error
        else:
            cmd.linear.x = min(1.5, 1.0 * distance)

        self.cmd_pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = TurtleMission()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.publish_stop()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
