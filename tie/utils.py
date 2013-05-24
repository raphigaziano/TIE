#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Various internal utilities for the tie library.
"""
import sys

PY2 = sys.version_info[0] == 2

### Compatibility String Utils ###

# Handle unicode between Python 2 and 3
# http://stackoverflow.com/a/6633040/305414
if PY2:
    unicode = unicode
    import codecs
    def u(string):
        """ Convert string to unicode """
        return codecs.unicode_escape_decode(string)[0]
else:
    unicode = str
    def u(string):
        """ No-op - Py 3 strings are unicode by default """
        return string

# from http://lucumr.pocoo.org/2013/5/21/porting-to-python-3-redux/
if PY2:
    def implements_to_string(cls):
        """ Class decorator to turn any __str__ method into a __unicode__ """
        cls.__unicode__ = cls.__str__
        cls.__str__ = lambda x: x.__unicode__().encode('utf-8')
        return cls
else:
    implements_to_string = lambda x: x
