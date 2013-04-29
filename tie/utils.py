#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Various internal utilities for the tie library.
"""
import sys

unicode = str if sys.version > '3' else unicode

class TIEError(Exception):
    """ TIE lib's main Exception class. """
    pass

