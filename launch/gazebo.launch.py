"""
gazebo.launch.py
Khoi dong Gazebo, spawn robot, khoi dong controllers
Bao gom: LiDAR, Camera, Encoder (qua joint_state_broadcaster)
"""

import os
from launch_ros.parameter_descriptions import ParameterValue
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    TimerAction,
    ExecuteProcess
)
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import (
    LaunchConfiguration,
    Command,
    FindExecutable,
    PathJoinSubstitution
)
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    pkg_share = FindPackageShare('robot_ros_clean_description')
    gazebo_ros_share = FindPackageShare('gazebo_ros')

    # Arguments
    declare_world_arg = DeclareLaunchArgument(
        name='world',
        default_value='',
        description='Path den file world Gazebo (de trong = empty world)'
    )

    declare_gui_arg = DeclareLaunchArgument(
        name='gui',
        default_value='true',
        description='Hien thi Gazebo GUI'
    )

    declare_verbose_arg = DeclareLaunchArgument(
        name='verbose',
        default_value='false',
        description='Verbose output cua Gazebo'
    )

    # Doc noi dung URDF tu xacro
    robot_description = Command([
        FindExecutable(name='xacro'),
        ' ',
        PathJoinSubstitution([pkg_share, 'urdf', 'robot_ros_clean.xacro'])
    ])

    # ============================================================
    # GAZEBO SERVER + CLIENT
    # ============================================================
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([gazebo_ros_share, 'launch', 'gazebo.launch.py'])
        ]),
        launch_arguments={
            'verbose': LaunchConfiguration('verbose'),
            'gui': LaunchConfiguration('gui'),
        }.items()
    )

    # ============================================================
    # ROBOT STATE PUBLISHER
    # ============================================================
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': ParameterValue(robot_description, value_type=str),
            'use_sim_time': True # (hoặc False trong file display)
        }]
    )

    # ============================================================
    # SPAWN ROBOT VAO GAZEBO
    # ============================================================
    spawn_entity_node = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_robot',
        output='screen',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'robot_ros_clean',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.15',
            '-Y', '0.0',
        ]
    )

    # ============================================================
    # CONTROLLERS - dung TimerAction de cho robot spawn xong
    # ============================================================

    # JointStateBroadcaster: publish /joint_states (bao gom encoder 4 banh)
    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        name='joint_state_broadcaster_spawner',
        output='screen',
        arguments=['joint_state_broadcaster', '--controller-manager', '/controller_manager'],
    )

    # ArmController: dieu khien tay may P-R
    arm_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        name='arm_controller_spawner',
        output='screen',
        arguments=['arm_controller', '--controller-manager', '/controller_manager'],
    )

   

    # Delay 3 giay cho Gazebo va robot spawn xong truoc khi khoi dong controllers
    delayed_controllers = TimerAction(
        period=3.0,
        actions=[
            joint_state_broadcaster_spawner,
            arm_controller_spawner,
           
        ]
    )

    return LaunchDescription([
        declare_world_arg,
        declare_gui_arg,
        declare_verbose_arg,
        gazebo_launch,
        robot_state_publisher_node,
        spawn_entity_node,
        delayed_controllers,
    ])