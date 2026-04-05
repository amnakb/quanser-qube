import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray

class PIDController(Node):
    def __init__(self):
        super().__init__('pid_controller')

        # Declare parameters so they can be set externally
        self.declare_parameter('target_angle', 0.0)
        self.declare_parameter('kp', 10.0)
        self.declare_parameter('ki', 0.1)
        self.declare_parameter('kd', 0.5)

        self.prev_error = 0.0
        self.integral = 0.0
        self.prev_time = None

        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10)

        self.publisher = self.create_publisher(
            Float64MultiArray,
            '/velocity_controller/commands',
            10)

        self.get_logger().info('PID Controller started. Target: 0.0 rad')

    def joint_state_callback(self, msg):
        if 'motor_joint' not in msg.name:
            return

        # Read parameters live so they can be changed anytime
        target = self.get_parameter('target_angle').value
        kp = self.get_parameter('kp').value
        ki = self.get_parameter('ki').value
        kd = self.get_parameter('kd').value

        now = self.get_clock().now().nanoseconds / 1e9
        idx = msg.name.index('motor_joint')
        position = msg.position[idx]

        error = target - position
        dt = (now - self.prev_time) if self.prev_time else 0.01
        self.prev_time = now

        self.integral += error * dt
        derivative = (error - self.prev_error) / dt
        self.prev_error = error

        output = kp * error + ki * self.integral + kd * derivative

        cmd = Float64MultiArray()
        cmd.data = [output]
        self.publisher.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = PIDController()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
