import os
from glob import glob

from setuptools import find_packages, setup

package_name = 'turtle_duvar_py'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='gulsum',
    maintainer_email='glsmbyrkdrr@gmail.com',
    description='Duvardan kacan kaplumbaga (turtlesim, rclpy)',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'duvar_kacan = turtle_duvar_py.duvar_kacan:main',
        ],
    },
)
