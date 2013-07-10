#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Helper functions for the TIE library.

These functions will be exposed to the user and documented. For strictly
internal helpers, see utils.py.

Regex helpers will provide shortcuts for some common regular expression 
handling.
"""

import os

### REGEX Helpers ###
#####################

def get_single_group(match, key=1):
    """
    Return one and only one group from the passed match object.
    If no group was defined in the matched regexp, return the whole match.
    params:
    match: A re.match object to extract the group from.
    key:   Optionnal key arg to get a specific group.
      Can be either a list index or a string to get a named group.
      Defaults to 1, to return the first group.
    """
    return match.group(key) if match.groups() else match.group(0)

### Files & Pathes Helpers ###
##############################

def path_to_basename(path, stripext=False):
    """
    Return the basename of the passed path, without the extension if
    `stripext` is True.
    """
    basename = os.path.basename(path)
    if stripext:
        return os.path.splitext(basename)[0]
    return basename

def list_files(startdir, recursive=False, abspathes=True):
    """
    Yield files contained in `startdir`.
    Optionnal parameters:
    `recursive`: Look for files recursively. Defaults to False.
    `abspathes`: Return absolute pathes. Defaults to True.
    """
    for f in os.listdir(startdir):
        path = os.path.join(startdir, f)
        if os.path.isfile(path):
            if abspathes:
                path = os.path.abspath(path)
            yield path
        elif recursive and os.path.isdir(path):
            for sub in list_files(path, recursive, abspathes):
                yield sub
