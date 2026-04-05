"""
PID-kontroller node for Quanser Qube-Servo 2.

Denne noden abonnerer på /joint_states for å få gjeldende vinkel på
motorleddet, kjører en PID-kontrollsløyfe, og publiserer hastighetskommandoer
til /velocity_controller/commands for å drive disken til en målvinkel.
"""
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray

class PIDController(Node):
    """PID-kontroller for Qube-motorleddet."""

    def __init__(self):
        super().__init__('pid_controller')

        # Deklarer parametere slik at de kan endres under kjøring
        self.declare_parameter('target_angle', 0.0)  # Målvinkel i radianer
        self.declare_parameter('kp', 10.0)           # Proporsjonal forsterkning
        self.declare_parameter('ki', 0.1)            # Integral forsterkning
        self.declare_parameter('kd', 0.5)            # Derivert forsterkning

        # Intern PID-tilstand
        self.prev_error = 0.0
        self.integral = 0.0
        self.prev_time = None

        # Abonner på leddetilstander for å få gjeldende posisjon
        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10)

        # Publiser hastighetskommandoer til hastighetskontrolleren
        self.publisher = self.create_publisher(
            Float64MultiArray,
            '/velocity_controller/commands',
            10)

        self.get_logger().info('PID-kontroller startet. Målvinkel: 0.0 rad')

    def joint_state_callback(self, msg):
        """Beregn PID-utgang og publiser hastighetskommando."""
        if 'motor_joint' not in msg.name:
            return

        # Les parametere under kjøring slik at de kan endres når som helst
        target = self.get_parameter('target_angle').value
        kp = self.get_parameter('kp').value
        ki = self.get_parameter('ki').value
        kd = self.get_parameter('kd').value

        # Hent gjeldende tid i sekunder
        now = self.get_clock().now().nanoseconds / 1e9

        # Hent gjeldende posisjon til motorleddet
        idx = msg.name.index('motor_joint')
        position = msg.position[idx]

        # Beregn feil mellom mål og gjeldende posisjon
        error = target - position

        # Beregn tidssteget
        dt = (now - self.prev_time) if self.prev_time else 0.01
        self.prev_time = now

        # Oppdater integral og derivert ledd
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt
        self.prev_error = error

        # Beregn PID-utgang (hastighetskommando)
        output = kp * error + ki * self.integral + kd * derivative

        # Publiser hastighetskommando
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
