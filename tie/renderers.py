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
import re
from tie import tag

def default_renderer(template, **context):
    """
    Default template renderer. 
    Process each registered Tag and returns the whole processed string.
    """
    out = template.template
    vals = {}
    for t in tag.get_manager():
        vals.update(t.process(out, **context))
    if vals:
        rgx = re.compile('|'.join(vals.keys()))
        return rgx.sub(lambda m: vals[m.group(0)], out)
    else: 
        return out

