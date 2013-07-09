#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Exceptions and warnings for the tie library.
"""

### Exceptions ###
##################

class TIEError(Exception):
    """TIE lib's main Exception class."""
    pass

### Tag Errors ###

class TagError(TIEError): 
    """Tag related Errors"""
    pass

class InvalidTagError(TagError): 
    """Invalid value to register a Tag object"""
    pass

### Template Errors ###

class TemplateError(TIEError):
    """Template related Errors"""
    pass

### Warnings ###
################

class ContextWarning(RuntimeWarning):
    """Context variables Warning"""
    pass
