#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Tag managers tests
"""
from __future__ import unicode_literals

import sys
import unittest

from tie import tag 

Tag = tag.Tag

def assertListEqual(self, l_1, l_2):
    """ Replacement of unittest.TestCase.assertListEqual() for 2.6 """
    self.assertTrue(all([item == l_2[i] for i, item in enumerate(l_1)]))

if sys.version < '2.7':
    setattr(unittest.TestCase, 'assertListEqual', assertListEqual)

class TestTagManager(unittest.TestCase):

    def setUp(self): pass
    def tearDown(self): 
        tag.get_manager().clear()

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

    def test_global_cache_clear(self):
        """ Clearing all registered tags' cache """
        tag.register(
            tag.Tag("dummy",  cached=True),
            tag.Tag("dumdum", cached=True),
            tag.Tag("mudmud", cached=True),
        )
        m = tag.get_manager()
        for t in m:
            t.process("dummydumdummudmud", **{'dummy':'dummy',
                                              'dumdum':'dumdum',
                                              'mudmud':'mudmud'}
            )
        m.clear_cache()
        for t in m:
            self.assertEqual({}, t.cache)

class TestPriorityTagManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        tag.set_manager(tag.PriorityTagManager())
    @classmethod
    def tearDownClass(cls):
        tag.set_manager(tag.TagManager())

    def setUp(self): pass
    def tearDown(self):
        tag.get_manager().clear()

    def test_register_with_priority(self):
        """ Registering tag with a PriorityTagManager """
        try:
            tag.register(
                ("dummy", 0),
                ("dumdum", 7),
                ("mudmud", 4)
            )
        except Exception:
            self.fail("Couldnt register Priority Tags")

    def test_register_without_priority(self):
        """ Registering a tag without specifying a priority: default to 0 """
        tag_objs = [Tag("dummy"), Tag("dumdum"), Tag("mudmud")]
        tag.register(*tag_objs)
        tags = tag.get_manager()._tag_list
        self.assertTrue(0 in tags.keys())
        self.assertEqual(len(tags[0]), 3)
        self.assertListEqual(tags[0], tag_objs)

    def test_check_tags_priority(self):
        """ Checking Tags priority """
        tag.register(
            ("dummy", 4),
            ("dumdum", 7),
            ("mudmud", 0)
        )
        tag_patterns = [t.regexp.pattern for t in tag.get_manager()]
        self.assertListEqual(tag_patterns, ["mudmud", "dummy", "dumdum"])
        
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
        self.assertEqual(len(tag._manager._tag_list), 3)
        self.assertListEqual(self.tags, tag._manager._tag_list)

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

    def test_register_Tag_sublass(self):
        """ Registering a Tag subclass """
        class DummyTag(Tag): pass
        t = DummyTag("dummy")
        tag.register(t)
        self.assertTrue(isinstance(tag.get_manager()._tag_list[0], DummyTag))
