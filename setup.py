#!/usr/bin/env python

import os
from setuptools import setup, find_packages

install_requires = [line.rstrip() for line in open(os.path.join(os.path.dirname(__file__), "requirements.txt"))]

setup(
    name="dss",
    version='6.5.1',
    url='https://github.com/DataBiosphere/data-store-cli',
    license='Apache Software License',
    author='Data Store Contributors',
    author_email='akislyuk@chanzuckerberg.com',
    description='Data Storage System Command Line Interface',
    long_description=open('README.rst').read(),
    install_requires=install_requires,
    extras_require={
        ':python_version < "3.5"': [
            'typing >= 3.6.2, < 4',
            'scandir >= 1.9.0, < 2'
        ],
    },
    packages=find_packages(exclude=['test']),
    entry_points={
        'console_scripts': [
            'dss=dss.cli:main'
        ],
    },
    platforms=['MacOS X', 'Posix'],
    package_data={'dsscli': ['*.json']},
    zip_safe=False,
    include_package_data=True,
    test_suite='test',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
