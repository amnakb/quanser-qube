"""
Launch-fil for visualisering av Qube-Servo 2 i RViz.

Starter følgende noder:
- robot_state_publisher: publiserer robotbeskrivelse og TF-transformasjoner
- joint_state_publisher_gui: gir en glidebryter for å manuelt styre ledd
- rviz2: visualiserer robotmodellen

Bruk:
    ros2 launch qube_description view_qube.launch.py
"""
import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # Finn pakkedelen for å finne URDF-filer
    pkg = get_package_share_directory('qube_description')

    # Behandle xacro-filen til en URDF-streng
    xacro_file = os.path.join(pkg, 'urdf', 'qube.urdf.xacro')
    robot_description = xacro.process_file(xacro_file).toxml()

    return LaunchDescription([
        # Publiserer robotbeskrivelse og TF-transformasjoner
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_description}]
        ),
        # GUI-glidebryter for manuell styring av ledd i RViz
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
        ),
        # RViz-visualisering
        Node(
            package='rviz2',
            executable='rviz2',
        ),
    ])
