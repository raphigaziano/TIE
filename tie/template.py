#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Template classes and utilities.

"""
import logging

from tie import renderers
from tie.exceptions import TemplateError

LOGGER = logging.getLogger(__name__)

class Template(object):
    """
    Template object.
    Holds a template string and provides a render method to process it.
    Callable for convenience.
    Basic customization can be achieved by providing a custom rendering
    callback.
    """
    def __init__(self, tmpl, renderer=renderers.default_renderer):
        """ 
        Parameters:
        tmpl:     Template string.
        renderer: Rendering callback. 
                  Defaults to renderers.default_renderer.
        """
        self.template = tmpl
        self.renderer = renderer
    
    def __call__(self, **context):
        """
        Convenience alias for
        :func:`Template.render()<tie.template.Template.render>`.
        """
        return self.render(**context)

    def render(self, **context):
        """
        Process the template & return the result.
        context is the keyword dictionary of context variables to be injected 
        into the processed template.
        """
        LOGGER.info("Rendering template %s", self)
        LOGGER.debug("Context vars: %s", context)
        return self.renderer(self, **context)

    @classmethod
    def from_file(cls, tmpl_path, *args, **kwargs):
        """ Alternative constructor -> Creates a template from a file. """
        with open(tmpl_path, 'r') as tmpl_f:
            template_string = tmpl_f.read()
        return cls(template_string, *args, **kwargs)
        
