#!/usr/bin/env python3
"""Duvardan kacan kaplumbaga dugumu.

/turtle1/pose konusunu dinler, /turtle1/cmd_vel ile kaplumbagayi ileri surer.
x veya y degeri alt/ust sinirin disina ciktiginda kaplumbaga donerek
(sahanin merkezine dogru) yon degistirir. Konum saniyede bir loglanir.
"""

import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose


class DuvarKacan(Node):
    def __init__(self):
        super().__init__('duvar_kacan')

        # --- Bonus: parametreler ---
        self.declare_parameter('linear_speed', 1.5)    # ileri hiz (m/s)
        self.declare_parameter('angular_speed', 2.0)   # donus hizi (rad/s)
        self.declare_parameter('min_limit', 1.0)       # alt sinir (x ve y)
        self.declare_parameter('max_limit', 10.0)      # ust sinir (x ve y)
        self.declare_parameter('log_period', 1.0)      # log periyodu (sn)

        self.pose = None
        self.turning = False

        # Abone: konum bilgisi
        self.pose_sub = self.create_subscription(
            Pose, '/turtle1/pose', self.pose_callback, 10)

        # Yayinci: hiz komutu
        self.cmd_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        # Kontrol dongusu (10 Hz)
        self.control_timer = self.create_timer(0.1, self.control_loop)

        # Log zamanlayicisi (varsayilan: saniyede bir)
        log_period = self.get_parameter('log_period').value
        self.log_timer = self.create_timer(log_period, self.log_position)

        self.get_logger().info('duvar_kacan dugumu basladi.')

    # ---------------------------------------------------------------- abone
    def pose_callback(self, msg: Pose):
        self.pose = msg

    # -------------------------------------------------------------- yardimci
    def outside_limits(self) -> bool:
        lo = self.get_parameter('min_limit').value
        hi = self.get_parameter('max_limit').value
        x, y = self.pose.x, self.pose.y
        return x < lo or x > hi or y < lo or y > hi

    @staticmethod
    def normalize(angle: float) -> float:
        return math.atan2(math.sin(angle), math.cos(angle))

    # ------------------------------------------------------- kontrol dongusu
    def control_loop(self):
        if self.pose is None:
            return  # henuz konum gelmedi

        linear = self.get_parameter('linear_speed').value
        angular = self.get_parameter('angular_speed').value
        lo = self.get_parameter('min_limit').value
        hi = self.get_parameter('max_limit').value

        cmd = Twist()

        if self.outside_limits():
            # Sinir disinda: sahanin merkezine dogru bak (don)
            centre = (lo + hi) / 2.0
            target = math.atan2(centre - self.pose.y, centre - self.pose.x)
            error = self.normalize(target - self.pose.theta)

            if abs(error) > 0.2:
                self.turning = True
                cmd.linear.x = 0.0
                cmd.angular.z = angular if error > 0 else -angular
            else:
                # Merkeze donuldu: ileri giderek sinirin icine don
                self.turning = False
                cmd.linear.x = linear
                cmd.angular.z = 0.0
        else:
            self.turning = False
            cmd.linear.x = linear
            cmd.angular.z = 0.0

        self.cmd_pub.publish(cmd)

    # ------------------------------------------------------------------ log
    def log_position(self):
        if self.pose is None:
            self.get_logger().info('Konum bekleniyor (/turtle1/pose)...')
            return
        durum = 'DONUYOR' if self.turning else 'ILERI'
        self.get_logger().info(
            f'Konum: x={self.pose.x:.2f}, y={self.pose.y:.2f}, '
            f'theta={self.pose.theta:.2f} | durum: {durum}')


def main(args=None):
    rclpy.init(args=args)
    node = DuvarKacan()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
