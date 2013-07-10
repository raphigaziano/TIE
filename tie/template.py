#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Template classes and utilities.

"""
import os
import logging

from tie import renderers
from tie.exceptions import TemplateError
from tie.helpers import list_files, path_to_basename

LOGGER = logging.getLogger(__name__)

def _path_2_tmpl_name(tmpl_path):
    """
    Quick helper.
    Get a file's basename (without extension) from its path and return it.
    """
    return path_to_basename(tmpl_path, stripext=True)


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
        """
        Alternative constructor -> Creates a template from a file.
        If `name` is not proveded, the template's name attribute will default
        to the file's basename, without extension.
        """
        with open(tmpl_path, 'r') as tmpl_f:
            template_string = tmpl_f.read()
        if not name:
            name = _path_2_tmpl_name(tmpl_path)
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
        for template in self._template_list:
            if template.name == key:
                return template
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
    """ 
    Template Manager that dynamically loads templates from one or several
    watched directories.
    """
    def __init__(self, *dirs):
        """
        Parameters:
        *dirs: list of directories to watch.
               Pathes can be either relative or absolute.
        """
        super(DirectoryWatcher, self).__init__()

        self.dirs = []
        for d in dirs:
            self.add_directory(d)

        self.recursive = True

    def add_directory(self, dir_, index=None):
        """ 
        Add a single directory (`dir_`) to the list of watched directories.
        `dir_` can be either a relative or absolute path (it will be stored as
        an absolute path either way).
        Optional argument `index` can be used to insert `dir_` at a specific
        index (behave like the regular :func:`list.insert` method).
        """
        if not os.path.isdir(dir_):
            raise IOError('%s is not a valid directory' % dir_)
        if index is None:
            self.dirs.append(os.path.abspath(dir_))
        else:
            self.dirs.insert(index, os.path.abspath(dir_))

    def list_watched_templates(self, basenames=False):
        """
        Yield the pathes of all files contained in all watched directories,
        recursively if the managers's instance's `recursive` attribute is set
        to True (which it is by default).
        Pathes will be absolute, unless the `basenames` argument is set to
        True, in which case only the files' base names will be returned.
        """
        for d in self.dirs:
            for t_path in  list_files(d, recursive=self.recursive):
                if basenames:
                    yield _path_2_tmpl_name(t_path)
                else:
                    yield t_path

    def _load_template(self, tmpl_name):
        """
        Load the `tmpl_name` template from disk, add it to the internal managed
        list and return it.
        Will raise a TemplateError if no template matched.
        """
        for t_f in self.list_watched_templates():
            t_n = _path_2_tmpl_name(t_f)
            if t_n == tmpl_name:
                template = Template.from_file(t_f, t_n)
                self.add(template)
                return template
        raise TemplateError('No template named %s' % tmpl_name)

    def __getattr__(self, tmpl_name):
        """
        Try and return a contained template whose name matches the key arg.
        Raises an AttributeError if none is found.
        The template will be loaded from disk if not already present in the
        internal list of managed templates.
        """
        try:
            return super(DirectoryWatcher, self).__getattr__(tmpl_name)
        except AttributeError:
            return self._load_template(tmpl_name)

    def __iter__(self):
        """
        Yield contained templates.
        This will cause all available templates to be loaded from disk and
        instanciated.
        """
        for t_name in self.list_watched_templates(basenames=True):
            yield getattr(self, t_name)
