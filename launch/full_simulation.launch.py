import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue  # <-- Thư viện mới để sửa lỗi

def generate_launch_description():
    pkg_name = 'robot_ros_clean_description'
    pkg_share = get_package_share_directory(pkg_name)

    # 1. Đọc file Xacro và bật Robot State Publisher (Đã bọc ParameterValue để chống lỗi YAML)
    xacro_file = os.path.join(pkg_share, 'urdf', 'robot_ros_clean.xacro')
    robot_description_content = ParameterValue(Command(['xacro ', xacro_file]), value_type=str)
    
    robot_description_params = {'robot_description': robot_description_content, 'use_sim_time': True}

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description_params]
    )

    # 2. Khởi động thế giới Gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
    )

    # 3. Thả Robot vào Gazebo
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description', '-entity', 'my_robot', '-z', '0.15'],
                        output='screen')

    # 4. Mở RViz với file config đã lưu
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', os.path.join(pkg_share, 'rviz', 'urdf.rviz')],
        parameters=[{'use_sim_time': True}]
    )

    # 5. Khởi động các Controllers (Đợi vài giây để Gazebo load xong)
    joint_state_broadcaster = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
    )

    arm_controller = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["arm_controller"],
    )

    return LaunchDescription([
        robot_state_publisher,
        gazebo,
        spawn_entity,
        rviz,
        TimerAction(period=3.0, actions=[joint_state_broadcaster]),
        TimerAction(period=4.0, actions=[arm_controller]),
    ])