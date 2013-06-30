#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Helper functions for the TIE library.

These functions will be exposed to the user and documented. For strictly
internal helpers, see utils.py.

Regex helpers will provide shortcuts for some common regular expression 
handling.
"""

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
