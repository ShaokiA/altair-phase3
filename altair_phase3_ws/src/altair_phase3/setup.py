
from setuptools import find_packages, setup

package_name = 'altair_phase3'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name],
        ),
        (
            'share/' + package_name,
            ['package.xml'],
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='hp',
    maintainer_email='shaokirf@gmail.com',
    description='Project Altair Phase 3 Mars telemetry monitoring',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'mars_telemetry_publisher = altair_phase3.mars_telemetry_publisher:main',
            'mission_control_monitor = altair_phase3.mission_control_monitor:main',
        ],
    },
)

