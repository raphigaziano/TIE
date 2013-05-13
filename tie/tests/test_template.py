#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Template objects tests
"""
from __future__ import unicode_literals

import unittest
import os
from tie import template 
from tie import renderers

Template = template.Template

class TestTemplate(unittest.TestCase):

    def setUp(self): pass
    def tearDown(self): pass
    
    def test_template_instanciation(self):
        """ Template.__init__ expects at least one argument """
        self.assertRaises(TypeError, Template)

    def test_templates_are_callables(self):
        """ Template objects shoud be directly callable """
        t = Template("dummy")
        try: t()
        except TypeError: self.fail("templates objects should be callable")

    def test_default_renderer(self):
        """ Defaulting to the right renderer callback """
        t = Template("dumdum")
        self.assertEqual(t.renderer, renderers.default_renderer)

    def test_renderer_callback(self):
        """ Template instanciation with a custom renderer """
        dummy_renderer = lambda x: x
        t = Template("mudmud", renderer=dummy_renderer)
        self.assertEqual(dummy_renderer, t.renderer)

class TestFileTemplate(unittest.TestCase):

    tmplpath = os.path.join(os.path.dirname(__file__), "testtemplate.txt")

    tmpl = "{{ include testinclude.txt }}\n{{ title }}\n" \
           "Hello, my name is {{ name }}\n" \
           "I'm {{ age }} years old and my name is {{ name }} !"

    def setUp(self): pass
    def tearDown(self): pass

    def test_filetemplate_instanciation(self):
        """ FileTemplate instanciation from file path """
        t = Template.from_file(self.tmplpath)
        self.assertEqual(t.template, self.tmpl)

    def test_filetemplate_instanciation_invalid_path(self):
        """ FileTemplate instanciation should fail if given an non-existent path """
        self.assertRaises(IOError, Template.from_file, "dummy")
