#!/usr/bin/env python

import setuptools
import os
from setuptools.command.install import install as setuptools_install

GANGLIA_FILES = [
    ('/usr/lib', ['files/libart_lgpl_2.so.2.3.21', 'files/libfreetype.so.6.9.0',
        'files/libpng12.so.0.18.0', 'files/libpng.so.3.18.0',
        'files/librrd.so.2.0.15', 'files/librrd_th.so.2.0.13']),
    ('/usr/local/sbin', ['files/gmond']),
    ('/usr/local/bin', ['files/ganglia-config', 'files/gmetric', 'files/gstat']),
    ('/usr/local/lib', ['files/libconfuse.so.0.0.0']),
    ('/usr/local/lib64', ['files/libganglia-3.6.0.so.0.0.0']),
    ('/usr/local/lib64/ganglia', ['files/modcpu.so', 'files/moddisk.so', 
        'files/modload.so', 'files/modmem.so',
        'files/modmulticpu.so', 'files/modnet.so', 'files/modproc.so', 
        'files/modpython.so', 'files/modsys.so']),
    ('/usr/local/etc/conf.d', ['files/modpython.conf'])
] 

GANGLIA_SYMLINKS = [
    ('/usr/local/lib/libconfuse.so.0.0.0', '/usr/local/lib/libconfuse.so'),
    ('/usr/local/lib/libconfuse.so.0.0.0', '/usr/local/lib/libconfuse.so.0'),
    ('/usr/local/lib64/libganglia-3.6.0.so.0.0.0', '/usr/local/lib64/libganglia-3.6.0.so.0'),
    ('/usr/local/lib64/libganglia-3.6.0.so.0.0.0', '/usr/local/lib64/libganglia.so'),
    ('/usr/lib/libart_lgpl_2.so.2.3.21', '/usr/lib/libart_lgpl_2.so.2'),
    ('/usr/lib/libart_lgpl_2.so.2.3.21', '/usr/lib/libart_lgpl_2.so'),
    ('/usr/lib/libfreetype.so.6.9.0', '/usr/lib/libfreetype.so.6'),
    ('/usr/lib/libfreetype.so.6.9.0', '/usr/lib/libfreetype.so'),
    ('/usr/lib/libpng12.so.0.18.0', '/usr/lib/libpng12.so.0'),
    ('/usr/lib/libpng12.so.0.18.0', '/usr/lib/libpng12.so'),
    ('/usr/lib/libpng.so.3.18.0', '/usr/lib/libpng.so.3'),
    ('/usr/lib/libpng.so.3.18.0', '/usr/lib/libpng.so'),
    ('/usr/lib/librrd.so.2.0.15', '/usr/lib/librrd.so.2'),
    ('/usr/lib/librrd.so.2.0.15', '/usr/lib/librrd.so'),
    ('/usr/lib/librrd_th.so.2.0.13', '/usr/lib/librrd_th.so.2'),
    ('/usr/lib/librrd_th.so.2.0.13', '/usr/lib/librrd_th.so'),
]

class install(setuptools_install):
    def run(self):
        setuptools_install.run(self)
        # Data files don't get their execute bit set, so fix that.
        for dirname, files in GANGLIA_FILES:
            if dirname in ['/usr/local/sbin', '/usr/local/bin']:
                for filename in files:
                    os.chmod(os.path.join(dirname, os.path.basename(filename)), 0755)
        for src, target in GANGLIA_SYMLINKS:
            os.symlink(src, target)


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
    },
    data_files=GANGLIA_FILES,
    cmdclass={'install': install}
)
