#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Various *internal* utilities for the tie library.
Utilities meant to be exposed to the user should be defined in the helpers.py
module, not here.
"""
import sys

# Handle unicode between Python 2 and 3
# http://stackoverflow.com/a/6633040/305414
if sys.version < '3':
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
