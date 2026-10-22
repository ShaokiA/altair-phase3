#!/usr/bin/env python3

import math
import threading
import time

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class TurtleDrivingMenu(Node):
    def __init__(self):
        super().__init__('turtle_driving_menu')
        self.publisher = self.create_publisher(
            Twist, '/turtle1/cmd_vel', 10
        )
        self.lock = threading.Lock()
        self.busy = False

    def send_velocity(self, linear=0.0, angular=0.0):
        msg = Twist()
        msg.linear.x = float(linear)
        msg.angular.z = float(angular)
        self.publisher.publish(msg)

    def stop(self):
        self.send_velocity(0.0, 0.0)
        time.sleep(0.2)
        self.send_velocity(0.0, 0.0)

    def drive(self, linear, angular, duration):
        end_time = time.monotonic() + duration
        while time.monotonic() < end_time:
            self.send_velocity(linear, angular)
            time.sleep(0.05)
        self.stop()

    def patrol(self):
        self.get_logger().info('Patrol: moving forward.')
        self.drive(1.0, 0.0, 3.0)

        self.get_logger().info('Turning approximately 180 degrees.')
        self.drive(0.0, math.pi / 3.0, 3.0)

        self.get_logger().info('Returning toward the starting area.')
        self.drive(1.0, 0.0, 3.0)
        self.stop()

    def rectangle(self):
        self.get_logger().info('Rectangle: tracing four sides.')
        for _ in range(2):
            self.drive(1.0, 0.0, 2.0)
            self.drive(0.0, math.pi / 4.0, 2.0)
            self.drive(1.0, 0.0, 1.0)
            self.drive(0.0, math.pi / 4.0, 2.0)
        self.stop()

    def zigzag(self):
        self.get_logger().info('Zigzag: three forward segments.')
        self.drive(1.0, 0.0, 2.0)
        self.drive(0.0, math.pi / 4.0, 1.5)

        self.drive(1.0, 0.0, 2.0)
        self.drive(0.0, -math.pi / 2.0, 1.5)

        self.drive(1.0, 0.0, 2.0)
        self.stop()

    def run_menu(self):
        print('\nTurtle Driving Menu')
        print('P - Patrol')
        print('R - Rectangle')
        print('Z - Zigzag')
        print('Q - Quit')

        while rclpy.ok():
            try:
                choice = input('\nChoose P, R, Z, or Q: ').strip().upper()
            except (EOFError, KeyboardInterrupt):
                break

            if choice == 'Q':
                print('Stopping turtle and quitting.')
                break
            elif choice not in ('P', 'R', 'Z'):
                print('Invalid choice. Enter P, R, Z, or Q.')
                continue

            with self.lock:
                if self.busy:
                    print('A pattern is already running.')
                    continue
                self.busy = True

            try:
                if choice == 'P':
                    self.patrol()
                elif choice == 'R':
                    self.rectangle()
                elif choice == 'Z':
                    self.zigzag()
            finally:
                self.stop()
                with self.lock:
                    self.busy = False

        self.stop()


def main(args=None):
    rclpy.init(args=args)
    node = TurtleDrivingMenu()
    try:
        node.run_menu()
    finally:
        node.stop()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
