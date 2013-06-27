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

from tie import utils, helpers
from tie.exceptions import ContextWarning

def sub(match, **context):
    """
    Default tag processor.
    Returns the appropriate value from **context for a matched tag.
    """
    tag = helpers.get_single_group(match)
    val = utils.unicode(context.get(tag, "")) # TODO: Error check
    if not val and tag not in context.keys():
        warnings.warn(
            "No context variable matched the tag %s" % tag,
            ContextWarning
        )
    return val
