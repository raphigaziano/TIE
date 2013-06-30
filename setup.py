#!/usr/bin/env python
#-*- coding:utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setuptools

config = {
    'name': 'TIE',
    'version': '0.1.0',
    'author': 'Raphi',
    'author_email': 'r.gaziano@gmail.com',
    'packages': ['tie', 'tie.tests'],
    'scripts': [], # any script in the bin directory
    'url': 'https://pypi.python.org/pypi/TIE',
    'download_url': None,
    'license': 'LICENCE.txt',
    'description': 'A minimalist template ENGINE allowing users to define '
                   'their own simple templating languages.',
    'long_description': open('README.rst').read(),
    'install_requires': [
    ]
    'keywords': [
        'templating'
    ],
    'classifiers': [
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ]
}

setup(**config)
