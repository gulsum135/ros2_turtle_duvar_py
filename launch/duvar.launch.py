from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('linear_speed', default_value='1.5'),
        DeclareLaunchArgument('angular_speed', default_value='2.0'),
        DeclareLaunchArgument('min_limit', default_value='1.0'),
        DeclareLaunchArgument('max_limit', default_value='10.0'),

        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='sim',
        ),
        Node(
            package='turtle_duvar_py',
            executable='duvar_kacan',
            name='duvar_kacan',
            output='screen',
            parameters=[{
                'linear_speed': LaunchConfiguration('linear_speed'),
                'angular_speed': LaunchConfiguration('angular_speed'),
                'min_limit': LaunchConfiguration('min_limit'),
                'max_limit': LaunchConfiguration('max_limit'),
            }],
        ),
    ])
