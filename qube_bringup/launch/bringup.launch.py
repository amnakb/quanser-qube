import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_bringup = get_package_share_directory('qube_bringup')
    pkg_driver  = get_package_share_directory('qube_driver')

    baud_arg   = DeclareLaunchArgument('baud_rate',  default_value='115200')
    device_arg = DeclareLaunchArgument('device',     default_value='/dev/ttyACM0')
    sim_arg    = DeclareLaunchArgument('simulation', default_value='true')

    xacro_file = os.path.join(pkg_bringup, 'urdf', 'controlled_qube.urdf.xacro')
    robot_description = xacro.process_file(xacro_file, mappings={
        'baud_rate':  '115200',
        'device':     '/dev/ttyACM0',
        'simulation': 'true'
    }).toxml()

    driver_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_driver, 'launch', 'qube_driver.launch.py')
        )
    )

    return LaunchDescription([
        baud_arg, device_arg, sim_arg,

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_description}]
        ),

        driver_launch,

        Node(
            package='rviz2',
            executable='rviz2',
        ),
    ])
