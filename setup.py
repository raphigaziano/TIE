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
}

setup(**config)
