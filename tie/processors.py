#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Default Tag processing callbacks.

Callbacks should be callable objects (simple functions or objects with a 
__call__ method) and must accept the following arguments:

    match:      A MatchObject instance, returned by regular expression string
                matching.
    **context:  A dictionnary of context variables, provided as keyword 
                arguments.

After any processing is done, they should return the value to be injected as
a unicode string.
"""
import warnings

from tie import utils

class ContextWarning(RuntimeWarning):
    """ Context variables Warning """
    pass

def sub(match, **context):
    """
    Default Ttag processor.
    Returns the appropriate value from **context for a matched tag.
    """
    tag = match.group(1) if match.groups() else match.group(0)
    val = utils.unicode(context.get(tag, "")) # TODO: Error check
    if not val and tag not in context.keys():
        warnings.warn(
            "No context variable matched the tag %s" % tag,
            ContextWarning
        )
    return val
