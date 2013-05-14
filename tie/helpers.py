#!/usr/bin/env python
#-*- coding:utf-8 -*-
""" Helper functions for the TIE library """

### REGEX Helpers ###
#####################

def get_single_group(match, key=1):
    """
    Return one and only one group from the passed match object.
    If no group was defined in the matched regexp, return the whole match.
    :param match: A re.match object to extract the group from.
    :param key: Optionnal key arg to get a specific group.
      Can be either a list index or a string to get a named group.
      Defaults to 1, to return the first group.
    """
    return match.group(key) if match.groups() else match.group(0)
