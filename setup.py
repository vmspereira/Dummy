#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


requirements = ['xmlschema']

test_requirements = [
    'pytest'
]

setup(
    name='dummy',
    version='0.0.2',
    description="Dummy package",
    author="BiSBII CEB University of Minho",
    author_email='vpereira@ceb.uminho.pt',
    url='',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    install_requires=requirements,
    license="MIT License",
    zip_safe=False,
    keywords='Dummy',
    classifiers=[
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
