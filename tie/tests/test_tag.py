#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Tag objects tests
"""
from __future__ import unicode_literals

import unittest
import sys
import re

from tie import tag 
from tie import processors

Tag = tag.Tag

class TestTag(unittest.TestCase):

    def setUp(self): pass
    def tearDown(self): pass
    
    def test_tag_instanciation(self):
        """ Tag.__init__ expects at least one argument """
        self.assertRaises(TypeError, Tag)

    def test_tag_regex_autocompile(self):
        """ Tag.pattern should be compiled to a regex object on instanciation """
        t = Tag("pattern")
        self.assertEqual(t.regexp, re.compile("pattern"))

    # Failing with 3.2:
    # compiled rgxp.flags is 32 more than equivalent re.<flags> combination.
    def test_tag_regex_flags(self):
        """ Tag.__init__ should pass optional flags to re.compile """
        # No flags
        t = Tag("pattern")
        self.assertEqual(t.regexp.flags, 0)
        # Verbose flag
        t = Tag("""
            pattern     # comment
            moar pattern
            dummy
        """, flags=re.VERBOSE)
        self.assertEqual(t.regexp.flags, re.VERBOSE)
        # Several flags
        t = Tag("pattern", flags=re.I | re.S | re.L)
        self.assertEqual(t.regexp.flags, re.I | re.S | re.L)

    def test_default_processor(self):
        """ Defaulting to the right processor callback """
        t = Tag("dumdum")
        self.assertEqual(t.processor, processors.sub)

    def test_processor_callback(self):
        """ Tag instanciation with a custom processor """
        dummy_processor = lambda x: x
        t = Tag("mudmud", processor=dummy_processor)
        self.assertEqual(t.processor, dummy_processor)

class TestTagManager(unittest.TestCase):

    def setUp(self): pass
    def tearDown(self): pass

    def test_manager_iterator(self): 
        """ Iterating directly over a TagManager """
        tags = TestRegistration.tags
        tag.register(*tags)
        for i, t in enumerate(tag._manager):
            self.assertEqual(t, tags[i])

    def test_set_manager(self):
        """ Setting up a custom TagManager """
        tm = tag.TagManager()
        self.assertNotEqual(tm, tag._manager)
        tag.set_manager(tm)
        self.assertEqual(tm, tag._manager)

    def test_get_manager(self):
        """ Getting the current TagManager """
        tm = tag.get_manager()
        self.assertEqual(tm, tag._manager)

class TestRegistration(unittest.TestCase):

    tags = [
        Tag("dummy"),
        Tag("dumdum"),
        Tag("mudmud"),
    ]

    def setUp(self): pass
    def tearDown(self): tag._manager = tag.TagManager()

    def test_basic_registration(self):
        """ Basic tag registration and retrieval """
        tag.register(*self.tags)
        self.assertEqual(len(tag._manager.tag_list), 3)
        self.assertListEqual(self.tags, tag._manager.tag_list)

    def test_custom_manager_registration(self):
        """ Registration with a custom tag manager """
        class dummy_manager(object):
            patterns = []
            def add(self, t): self.patterns.append(t)

        dm = dummy_manager()
        tag.set_manager(dm)
        tag.register(*self.tags)
        self.assertListEqual(self.tags, dm.patterns)

    def test_register_string(self):
        """ Registering string instead of Tag instances """
        tag.register(
            "dummy",
            "dumdum",
            "mudmud",
        )
        self.assertTrue(all(map(lambda t: isinstance(t, tag.Tag),
                            tag._manager)))
    
    def test_register_invalid_tag(self):
        """ Trying to register a invalid tag should raise an error """
        self.assertRaises(tag.InvalidTagError, tag.register, 666)
        # TODO: add moar bad input

class TestMatches(unittest.TestCase):

    tag = Tag("%\w+")

    def matches_list(self, template):
        """ Helper """
        return [m for m in self.tag.match(template)]

    def test_tag_matches(self):
        """ Basic tag matching """
        # No match
        matches = self.matches_list("dummytemplate")
        self.assertEqual(len(matches), 0)
        # One match
        matches = self.matches_list("dummy %dummy dummy")
        self.assertEqual(len(matches), 1)
        # Three matches
        matches = self.matches_list("%dummy %dummy %dummy")
        self.assertEqual(len(matches), 3)

    def test_valid_matches(self):
        """ Valid matches returned by Tag.match """
        tags = ["%dummy", "%dumdum", "%mudmud"]
        for i, m in enumerate(self.matches_list("%dummy, %dumdum & %mudmud")):
            self.assertEqual(m.group(0), tags[i])

class TestProcessing(unittest.TestCase):

    def test_naive_substituion(self):
        """ Very naive text substitution """
        t = Tag("name")
        self.assertEqual("i am raphi", t.process("i am name", name="raphi"))

    def test_several_matches_sub(self):
        """ Substitution with several matches of a tag """
        t = Tag("name")
        self.assertEqual("raphi, raphi & raphi", t.process("name, name & name",
                                                            name="raphi"))

    def test_basic_regex_sub(self):
        """ Regex based basic substitution """
        t = Tag("%\w*%")
        self.assertEqual("i am raphi", t.process("i am %name%",
                                                 **{'%name%':"raphi"}))

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestTag))
    return suite
