#!/usr/bin/env python
#-*- coding:utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setuptools

config = {
    'name': 'TIE',
    'version': '0.1dev',
    'author': 'Raphi',
    'author_email': 'r.gaziano@gmail.com',
    'packages': ['tie', 'tie.tests'],
    'scripts': [], # any script in the bin directory
    'url': None,
    'download_url': None,
    'license': 'LICENSE.txt',
    'description': 'TODO',
    'long_description': open('README.txt').read(),
    'install_requires': [
    ]
}

setup(**config)
