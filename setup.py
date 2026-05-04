from setuptools import find_packages, setup

package_name = 'my_flutter_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='msk',
    maintainer_email='msk@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
		'data_saver = my_flutter_pkg.data_saver:main',
		'save_location_node = my_flutter_pkg.save_location_node:main',
        	'send_goal_node = my_flutter_pkg.send_goal_node:main', 
        ],
    },
)


 
