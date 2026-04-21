"""
controller.launch.py
Spawn cac controller sau khi Gazebo va robot da chay san
Dung khi can khoi dong lai controller ma khong restart Gazebo
"""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    # JointStateBroadcaster: publish /joint_states
    # - Encoder: doc position cua wheel_fl/bl/fr/br_joint (don vi rad)
    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        name='joint_state_broadcaster_spawner',
        output='screen',
        arguments=[
            'joint_state_broadcaster',
            '--controller-manager', '/controller_manager'
        ],
    )

    # ArmController: nhan goal qua /arm_controller/follow_joint_trajectory
    arm_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        name='arm_controller_spawner',
        output='screen',
        arguments=[
            'arm_controller',
            '--controller-manager', '/controller_manager'
        ],
    )

    return LaunchDescription([
        joint_state_broadcaster_spawner,
        arm_controller_spawner,
        
    ])