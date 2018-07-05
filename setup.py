#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of djangodbmodel.
# https://github.com/belonesox/djangodbmodel

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2018, Stas Fomin <stas-fomin@yandex.ru>

from setuptools import setup, find_packages
from djangodbmodel import __version__

# tests_require = [
#     'mock',
#     'nose',
#     'coverage',
#     'yanc',
#     'preggy',
#     'tox',
#     'ipdb',
#     'coveralls',
#     'sphinx',
# ]

setup(
    name='djangodbmodel',
    version=__version__,
    description='Generate D3.js visualization from django-model',
    long_description='''
Generate D3.js visualization from django-model
''',
    keywords='',
    author='Stas Fomin',
    author_email='stas-fomin@yandex.ru',
    url='https://github.com/belonesox/djangodbmodel',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # add your dependencies here
        # remember to use 'package-name>=x.y.z,<x.y+1.0' notation (this way you get bugfixes)
    ],
    extras_require={
        # 'tests': tests_require,
    },
    entry_points={
        'console_scripts': [
            # add cli scripts here in this form:
            # 'djangodbmodel=djangodbmodel.cli:main',
        ],
    },
    zip_safe=False
)
