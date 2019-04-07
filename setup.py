#!/usr/bin/env python

from setuptools import setup, find_packages
from os import path
import re


_ABSOLUTE_DOC_LINK = re.compile('\[(?P<text>[^\]]+)\]\((?P<link>docs/[^\)]+)\)')
def _absolute_docs_link_replacement(text):
    def _replacement(m):
        return '[{text}](https://github.com/team23/b5/blob/master/{link})'.format(
            text=m.group('text'),
            link=m.group('link')
        )
    return _ABSOLUTE_DOC_LINK.sub(_replacement, text)


# read the contents of your README file
package_path = path.abspath(path.dirname(__file__))
with open(path.join(package_path, 'README.md'), encoding='utf-8') as f:
    long_description = _absolute_docs_link_replacement(f.read())


setup(
    name='b5',
    version='1.1.2',
    description='b5 - simple and sane task runner',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='David Danier',
    author_email='danier@team23.de',
    url='https://github.com/team23/b5',
    packages=find_packages(exclude=['tests.*', 'tests']),
    package_data = {
        'b5': [
            'bash/*',
            'legacy/*',
            'legacy/modules/*',
        ],
    },
    install_requires=[
        'pyyaml ~=5.1',
        'termcolor ~=1.1.0',
        'Jinja2 ~=2.10',
        'MarkupSafe ~=1.1',
        'packaging >=16.0',
    ],
    entry_points={
        'console_scripts': [
            'b5 = b5.main:main',
            'b5-init = b5.init:main',
            'b5-execute = b5.execute:main',
        ]
    },
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        #'Programming Language :: Python :: 3.8',
        'Topic :: Software Development',
        'Topic :: Software Development :: Build Tools',
        'Topic :: System :: Systems Administration',
    ],
)
