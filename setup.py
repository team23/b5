#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='b5',
    version='0.1.0',
    description='b5 - sane task runner',
    author='David Danier',
    author_email='danier@team23.de',
    url='http://www.team23.de/b5',
    packages=find_packages(exclude=['tests.*', 'tests']),
    install_requires=[
        # 'TODO'
    ],
    entry_points={
        'console_scripts': [
            'b5 = b5.main:main',
        ]
    },
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        #'Programming Language :: Python :: 3.7',
        'Topic :: Software Development',
        'Topic :: Software Development :: Build Tools',
        'Topic :: System :: Systems Administration',
    ],
)
