from setuptools import setup

package_name = 'open_cv'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='yueju',
    maintainer_email='juyue0835@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ['auto_centering = open_cv.auto_centering:main',
                            'image_procesing = open_cv.image_processing:main'
        ],
    },
)
