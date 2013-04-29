#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Main test file.
Dynamically build a test suite out of all the other test files and run 
them all.

This should be run from the project's top directory, so that any of the
imported test modules can import their needed project files.

I'm hoping this is generic enough not to trip up any test running 
framework. For now I can only assert that nose doesn't mind.

Tested with:
-win7:
    py2.7, py3.2
-linux 2.6 (mint):
    py2.6, py2.7, py3.2
    
Author:     raphi <r.gaziano@gmail.com>
Date:       20.01.2013
Version:    1.0
"""
import unittest
import sys
import os

# Is this ugly ?
path = os.getcwd()
sys.path.append(path)

suite = unittest.TestSuite()

# Dynamic building of the whole test suite
dir_ = os.path.dirname(os.path.realpath(__file__))
for f in os.listdir(dir_):
    if f == os.path.basename(__file__): continue
    if f == '__init__.py':              continue
    name, ext = os.path.splitext(f)
    if ext == '.py' and f.startswith('test'):
        test_module = __import__(name, globals())
        suite.addTest(test_module.suite())

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite)
