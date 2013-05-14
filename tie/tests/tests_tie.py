#!/usr/bin/env python
#-*- coding:utf-8 -*-
""" TIE lib's functionnal tests. """
import os
import unittest

from tie import tag, template

class TestTIE(unittest.TestCase):
    """ Global functionnal tests """

    tmplpath = os.path.join(os.path.dirname(__file__), "testtemplate.txt")

    def setUp(self): pass
    def tearDown(self):
        tag.get_manager().clear()

    def test_basic_rendering_filetemplate(self):
        """ Basic rendering of a file template """
        tag.register(r"{{ (\w+) }}")
        t = template.Template.from_file(self.tmplpath)
        rt = t(title="TIE Is Evil", name="Raphi", age=26)
        self.assertEqual("{{ include testinclude.txt }}\n"
                         "TIE Is Evil\n"
                         "Hello, my name is Raphi\n"
                         "I'm 26 years old and my name is Raphi !",
                         rt)

    def test_rendering_filetemplate_with_customtag(self):
        """ Rendering a file template with a custom tag defined """
        def include_tag(match, **context):
            fname = match.group(1)
            return "Contents of file %s" % fname
        tag.register(r"{{ (\w+) }}")
        tag.register(tag.Tag(r"{{ include (\w.+) }}", processor=include_tag))
        t = template.Template.from_file(self.tmplpath)
        rt = t(title="TIE Is Evil", name="Bobby", age=32)
        self.assertEqual("Contents of file testinclude.txt\n"
                         "TIE Is Evil\n"
                         "Hello, my name is Bobby\n"
                         "I'm 32 years old and my name is Bobby !",
                         rt)

