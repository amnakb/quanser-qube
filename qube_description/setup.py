from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'qube_description'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
    ('share/ament_index/resource_index/packages',
        ['resource/qube_description']),
    ('share/qube_description', ['package.xml']),
    ('share/qube_description/urdf', ['urdf/qube.urdf.xacro',
                                    'urdf/qube.macro.xacro']),
    ('share/qube_description/launch', ['launch/view_qube.launch.py']),
],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='student',
    maintainer_email='student@todo.todo',
    description='URDF description for Quanser Qube',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [],
    },
)
