# Copyright 2019 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from ament_index_python.packages import get_package_share_path

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration

from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.actions import Node

import xacro

def generate_launch_description():
    urdf_tutorial_path = get_package_share_path('ignition_ros2_control_test')
    default_model_path = urdf_tutorial_path / 'urdf/my-simple-robot.urdf.xacro'

    model_arg = DeclareLaunchArgument(name='model', default_value=str(default_model_path),
                                      description='Absolute path to robot urdf file')

    robot_description_config = xacro.process_file(
        default_model_path
    )

    # Robot state publisher
    params = {'use_sim_time': True, 'robot_description': robot_description_config.toxml()}
    robot_state_publisher = Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[params],
            arguments=[])


    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
    )

    # Gazebo Sim
    pkg_ros_gz_sim = get_package_share_path('ros_gz_sim')
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': '-r empty.sdf'}.items(),
    )

    # RViz
    pkg_ros_gz_sim_demos = get_package_share_path('ros_gz_sim_demos')
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=[
            '-d',
            os.path.join(pkg_ros_gz_sim_demos, 'rviz', 'robot_description_publisher.rviz')
        ]
    )

    # Spawn
    spawn = Node(package='ros_gz_sim', executable='create',
                 arguments=[
                    '-name', 'simple_robot',
                    '-x', '0.0',
                    '-z', '6.0',
                    '-y', '0.0',
                    '-topic', '/robot_description'],
                 output='screen')

    return LaunchDescription([
        model_arg,
        gazebo,
        robot_state_publisher,
        # joint_state_publisher_node,
        # rviz,
        spawn
    ])