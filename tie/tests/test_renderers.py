#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Template rendererd tests
"""
from __future__ import unicode_literals

import unittest
from tie import renderers
from tie import template
from tie import tag

class TestDefaultRenderer(unittest.TestCase):

    render = staticmethod(renderers.default_renderer)

    def setUp(self): pass
    def tearDown(self):
        tag.get_manager().clear()

    def test_no_tag_matched(self):
        """ Template default renderer should return the template string unchanged if no tag matched """
        tag.register('foo')
        tmpl = template.Template("dummydumdum")
        self.assertEqual(tmpl.template, self.render(tmpl))

    def test_no_tag_registered(self):
        """
        Templates fall back to default python string formatting if no 
        tags are registered
        """
        tmpl = template.Template('Hello, my name is {name} and i\'m {age} years old')
        self.assertEqual(
            'Hello, my name is raphi and i\'m 26 years old',
            self.render(tmpl, **{'name': 'raphi', 'age': 26}))

    def test_single_tag(self):
        """ Rendering a single tag template """
        tag.register("%dummytag%")
        tmpl = template.Template("dum dummy %dummytag% dumdum")
        self.assertEqual("dum dummy dummyval dumdum",
                         self.render(tmpl, **{"%dummytag%": "dummyval"}))

    def test_several_tags(self):
        """ Rendering a template containing several different tags """
        tag.register("%dummytag%", "{muddytag}", "--dumdum--")
        tmpl = template.Template("%dummytag%, {muddytag} & --dumdum--")
        args = {
            "%dummytag%" : "dummyval",
            "{muddytag}" : "foo",
            "--dumdum--" : "bar"
        }
        self.assertEqual("dummyval, foo & bar", self.render(tmpl, **args))

    def test_repeated_tags(self):
        """ Rendering a template containing repeated tags """
        tag.register("--dumdum--")
        tmpl = template.Template("--dumdum--, --dumdum-- & --dumdum--")
        self.assertEqual("foo, foo & foo",
                         self.render(tmpl, **{"--dumdum--": "foo"}))

