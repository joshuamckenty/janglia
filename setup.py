#!/usr/bin/env python

import setuptools

setuptools.setup(
    name='janglia',
    version='0.1',
    description='Packaging of Ganglia for Moxie',
    url='http://www.pistoncloud.com',
    packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    package_data={'janglia': ['templates/*']},
    install_requires=[
        'savage'
    ],
    entry_points={
        'console_scripts': [
            'janglia = janglia:main',
        ],
        'piston.moxie.v1.configuration': [
            'GangliaTask = janglia:GangliaTask',
        ]
    }
)
