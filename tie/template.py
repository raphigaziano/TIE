#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Template classes and utilities.

"""
import logging

from tie.utils import TIEError
from tie import renderers

LOGGER = logging.getLogger(__name__)

class TemplateError(TIEError):
    """ Template related Errors """
    pass

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
        Class initializer.
        :param tmpl: Template string.
        :param renderer: Rendering callback. 
          Defaults to renderers.default_renderer.
        """
        self.template = tmpl
        self.renderer = renderer
    
    def __call__(self, **kwargs):
        """ Convenience alias for Template.render. """
        return self.render(**kwargs)

    def render(self, **context):
        """
        Process the template & return the result.
        :param **context: Keyword dict of context variable inject into the
          processed template.
          Passed to every Tag processor.
        """
        LOGGER.info("Rendering template %s" % self)
        LOGGER.debug("Context vars: %s" % context)
        return self.renderer(self, **context)

class FileTemplate(Template):
    """ File based Template object """
    def __init__(self, tmpl_path, *args, **kwargs):
        """ 
        Class initializer.
        :param tmpl_path: Path to the template file.
        :param renderer: Rendering callback. 
          Defaults to renderers.default_renderer.
        """
        with open(tmpl_path, 'r') as tmpl_f:
            template_string = tmpl_f.read()
        super(FileTemplate, self).__init__(
            template_string,
            *args,
            **kwargs
        )

