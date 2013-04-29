#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Default Template renderers.

Renderers should be callable objects (simple functions or objects with a 
__call__ method) and must accept the following arguments:

    template:   A Template instance to be processed.
    **context:  A dictionnary of context variables, provided as keyword 
                arguments.

After any processing is done, they should return the rendered template as a 
unicode string.
"""
from tie import tag

def default_renderer(template, **context):
    """
    Default template renderer. 
    Process each registered Tag and returns the whole processed string.
    """
    out = template.template
    for t in tag.get_manager():
        out = t.process(out, **context)
    return out
