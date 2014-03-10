#!/usr/bin/env python

import setuptools
import os
from setuptools.command.install import install as setuptools_install

GANGLIA_FILES = [
    ('/usr/local/sbin', ['files/gmond']),
    ('/usr/local/bin', ['files/ganglia-config', 'files/gmetric', 'files/gstat']),
    ('/usr/local/lib', ['files/libconfuse.a', 'files/libconfuse.la', 'files/libconfuse.so.0.0.0']),
    ('/usr/local/lib/pkgconfig', ['files/libconfuse.pc']),
    ('/usr/local/lib64', ['files/libganglia.a', 'files/libganglia.la', 
        'files/libganglia-3.6.0.so.0.0.0']),
    ('/usr/local/lib64/ganglia', ['files/modcpu.so', 'files/moddisk.so', 
        'files/modload.so', 'files/modmem.so',
        'files/modmulticpu.so', 'files/modnet.so', 'files/modproc.so', 
        'files/modpython.so', 'files/modsys.so']),
    ('/usr/local/etc/conf.d', ['files/modpython.conf'])
] 

GANGLIA_SYMLINKS = [
    ('/usr/local/lib/libconfuse.so.0.0.0', '/usr/local/lib/libconfuse.so'),
    ('/usr/local/lib/libconfuse.so.0.0.0', '/usr/local/lib/libconfuse.so.0'),
    ('/usr/local/lib64/libganglia-3.6.0.so.0.0.0', 'libganglia-3.6.0.so.0'),
    ('/usr/local/lib64/libganglia-3.6.0.so.0.0.0', 'libganglia.so'),
]

class install(setuptools_install):
    def run(self):
        super(install, self).run()
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
