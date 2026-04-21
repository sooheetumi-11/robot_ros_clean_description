"""
display.launch.py
Hien thi robot trong RViz2 voi joint_state_publisher_gui
Dung de kiem tra URDF/Xacro: hinh dang, cac khop, cam bien
"""

import os
from launch_ros.parameter_descriptions import ParameterValue
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command, FindExecutable, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    pkg_share = FindPackageShare('robot_ros_clean_description')

    # Path den file xacro
    default_model_path = PathJoinSubstitution([
        pkg_share, 'urdf', 'robot_ros_clean.xacro'
    ])

    # Path den file rviz config
    default_rviz_config = PathJoinSubstitution([
        pkg_share, 'launch', 'urdf.rviz'
    ])

    # Arguments
    declare_model_arg = DeclareLaunchArgument(
        name='model',
        default_value=default_model_path,
        description='Duong dan den file URDF/Xacro'
    )

    declare_rviz_arg = DeclareLaunchArgument(
        name='rvizconfig',
        default_value=default_rviz_config,
        description='Duong dan den file rviz config'
    )

    declare_gui_arg = DeclareLaunchArgument(
        name='gui',
        default_value='true',
        description='Bat/tat joint_state_publisher_gui'
    )

    # Doc noi dung URDF tu xacro
    robot_description = Command([
        FindExecutable(name='xacro'),
        ' ',
        LaunchConfiguration('model')
    ])

    # Robot State Publisher: publish /tf va /robot_description
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': ParameterValue(robot_description, value_type=str),
            'use_sim_time': False # (hoặc False trong file display)
        }]
    )

    # Joint State Publisher GUI: tao slider dieu khien khop
    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen'
    )

    # RViz2
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', LaunchConfiguration('rvizconfig')],
    )

    return LaunchDescription([
        declare_model_arg,
        declare_rviz_arg,
        declare_gui_arg,
        robot_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz_node,
    ])