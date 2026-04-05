"""
Oppstartsfil for hele Qube-Servo 2-systemet.

Starter følgende komponenter:
- robot_state_publisher: publiserer TF-transformasjoner
- ros2_control_node: håndterer maskinvare og kontrollere
- joint_state_broadcaster: publiserer leddetilstander til /joint_states
- velocity_controller: mottar hastighetskommandoer fra PID-kontrolleren
- rviz2: visualiserer roboten

Argumenter:
    simulation (standard: true): Bruk simulert eller ekte maskinvare
    device (standard: /dev/ttyACM0): USB-enhet for ekte maskinvare
    baud_rate (standard: 115200): Seriell baudrate for Arduino

Bruk (simulering):
    ros2 launch qube_bringup bringup.launch.py simulation:=true

Bruk (ekte maskinvare):
    ros2 launch qube_bringup bringup.launch.py simulation:=false device:=/dev/ttyACM0
"""
import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_bringup = get_package_share_directory('qube_bringup')
    pkg_driver  = get_package_share_directory('qube_driver')

    # Deklarer oppstartsargumenter for maskinvarekonfigurasjon
    baud_arg   = DeclareLaunchArgument('baud_rate',  default_value='115200',
                    description='Baudrate for Arduino seriekommunikasjon')
    device_arg = DeclareLaunchArgument('device',     default_value='/dev/ttyACM0',
                    description='USB-enhetsnavn for Quben')
    sim_arg    = DeclareLaunchArgument('simulation', default_value='true',
                    description='Bruk simulering (true) eller ekte maskinvare (false)')

    def create_description(context):
        # Behandle xacro med kjøretidsverdier fra oppstartsargumenter
        xacro_file = os.path.join(pkg_bringup, 'urdf', 'controlled_qube.urdf.xacro')
        robot_description = xacro.process_file(xacro_file, mappings={
            'baud_rate':  context.launch_configurations['baud_rate'],
            'device':     context.launch_configurations['device'],
            'simulation': context.launch_configurations['simulation'],
        }).toxml()

        # Inkluder qube_driver launch som starter controller_manager og spawners
        driver_launch = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_driver, 'launch', 'qube_driver.launch.py')
            )
        )

        return [
            # Publiserer robotbeskrivelse og TF-transformasjoner
            Node(
                package='robot_state_publisher',
                executable='robot_state_publisher',
                parameters=[{'robot_description': robot_description}]
            ),
            # Starter kontrollbehandler, leddetilstandskringkaster og hastighetskontroller
            driver_launch,
            # RViz-visualisering
            Node(
                package='rviz2',
                executable='rviz2',
            ),
        ]

    return LaunchDescription([
        baud_arg, device_arg, sim_arg,
        OpaqueFunction(function=create_description)
    ])
