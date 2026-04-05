import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray

class QubeController(Node):

    def __init__(self):
        super().__init__('qube_controller')

        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.callback,
            10)

        self.publisher = self.create_publisher(
            Float64MultiArray,
            '/velocity_controller/commands',
            10)

        self.kp = 2.0
        self.ki = 0.0
        self.kd = 0.1

        self.ref = 1.0
        self.prev_error = 0.0
        self.integral = 0.0

    def callback(self, msg):
        pos = msg.position[0]

        error = self.ref - pos
        self.integral += error
        derivative = error - self.prev_error

        u = self.kp*error + self.ki*self.integral + self.kd*derivative

        cmd = Float64MultiArray()
        cmd.data = [u]

        self.publisher.publish(cmd)

        self.prev_error = error


def main():
    rclpy.init()
    node = QubeController()
    rclpy.spin(node)
    rclpy.shutdown()