#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Template classes and utilities.

"""
import os
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
    def __init__(self, tmpl, name='', renderer=renderers.default_renderer):
        """ 
        Parameters:
        tmpl:     Template string.
        renderer: Rendering callback. 
                  Defaults to renderers.default_renderer.
        """
        self.template = tmpl
        self.name     = name
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
    def from_file(cls, tmpl_path, name='', *args, **kwargs):
        """ Alternative constructor -> Creates a template from a file. """
        with open(tmpl_path, 'r') as tmpl_f:
            template_string = tmpl_f.read()
        if not name:
            name = os.path.splitext(os.path.basename(tmpl_path))[0]
        return cls(template_string, name=name, *args, **kwargs)
        
### Managers ###
################

class TemplateManager(object):
    """
    Template Container.
    Iterating over it will yield each contained template in order of their 
    insertion.

    Templates are stored in a simple list. Eventual subclasses will need to
    redefine their access and __iter__ method if they decide to use another
    data structure.
    """
    def __init__(self):
        self._template_list = []

    def add(self, template):
        """
        Register a new template.
        Override this method to accomodate a different internal data strucutre.
        """
        self._template_list.append(self._check_template(template))

    def clear(self):
        """
        Clear the internal template list.
        Override to accomodate a different internal data strucutre.
        """
        self._template_list = []

    def __iter__(self):
        """
        Yield contained templates.
        Override to accomodate a different internal data strucutre.
        """
        for template in self._template_list:
            yield template
    
    def __getattr__(self, key):
        """ 
        Try and return a contained template whose name matches the key arg.
        Raises an AttributeError if none is found.
        """
        for t in self._template_list:
            if t.name == key:
                return t
        raise AttributeError("Invalid attribute or template name: %s" % key)

    @staticmethod
    def _check_template(template, cls=Template):
        """
        Instances of cls (or a subclass of it) will be returned unchanged.
        Any other type will be sent to cls' constructor, which is responsible
        for type checking.
        cls defaults to Template.
        """
        if not isinstance(template, cls):
            return cls(template)
        return template

class DirectoryWatcher(TemplateManager):
    """ """
    def __init__(self, *dirs):
        super(DirectoryWatcher, self).__init__()

        self.dirs = []
        for d in dirs:
            self.add_directory(d)

        self.recursive = True

    def add_directory(self, dir_, index=None):
        """ """
        if not os.path.isdir(dir_):
            raise IOError('%s is not a valid directory' % dir_)
        if index is None:
            self.dirs.append(os.path.abspath(dir_))
        else:
            self.dirs.insert(index, os.path.abspath(dir_))

    def list_templates(self):
        """ """
        for d in self.dirs:
            if self.recursive:
                for root, dirs, files in os.walk(d):
                    for f in files:
                        yield os.path.abspath(os.path.join(root, f))
            else:
                for f in os.listdir(d):
                    path = os.path.abspath(os.path.join(d, f))
                    if os.path.isfile(path):
                        yield path

    def _load_template(self, tmpl_name):
        """ """
        for t_f in self.list_templates():
            t_n = os.path.splitext(os.path.basename(t_f))[0]
            if t_n == tmpl_name:
                t = Template.from_file(t_f, t_n)
                self.add(t)
                return t
        raise TemplateError('No template named %s' % tmpl_name)

    def __getattr__(self, tmpl_name):
        """ """
        try:
            return super(DirectoryWatcher, self).__getattr__(tmpl_name)
        except AttributeError:
            return self._load_template(tmpl_name)

    def __iter__(self):
        """ """
        for t_path in self.list_templates():
            t_name = os.path.splitext(os.path.basename(t_path))[0]
            yield getattr(self, t_name)
