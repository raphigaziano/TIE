#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Tag managers tests
"""
from __future__ import unicode_literals

import os
import sys
import unittest

from tie import tag 
from tie import template

Tag      = tag.Tag
Template = template.Template

def assertListEqual(self, l_1, l_2):
    """ Replacement of unittest.TestCase.assertListEqual() for 2.6 """
    self.assertTrue(all([item == l_2[i] for i, item in enumerate(l_1)]))

def assertIsNotNone(self, val):
    """ Replacement of unittest.TestCase.assertIsNotNone) for 2.6 """
    self.assertTrue(val is not None)

if sys.version < '2.7':
    setattr(unittest.TestCase, 'assertListEqual', assertListEqual)
    setattr(unittest.TestCase, 'assertIsNotNone', assertIsNotNone)

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

class TemplateTagManager(unittest.TestCase):

    templates = [
        Template('foo', name='foo'),
        Template('bar', name='bar'),
        Template('baz', name='baz')
    ]

    manager = template.TemplateManager()

    def setUp(self):
        for t in self.templates:
            self.manager.add(t)

    def tearDown(self):
        self.manager.clear()

    def test_manager_iterator(self): 
        """ Iterating directly over a TemplateManager """
        for i, t in enumerate(self.manager):
            self.assertEqual(t, self.templates[i])

    def test_access_named_templates(self):
        """ Accessing a template from the manager via attribute lookup """
        self.assertEqual(self.templates[0], self.manager.foo)
        self.assertEqual(self.templates[1], self.manager.bar)
        self.assertEqual(self.templates[2], self.manager.baz)

    def test_invalid_attr_access(self):
        """ Accessing a non registered name should raise an AttributeError like any non existing attribute """
        self.assertRaises(AttributeError, getattr, self.manager, 'dummy')

class DirectoryWatcher(unittest.TestCase):

    root_dir    = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    watched_dir = 'tie/tests/watched-templates'

    def setUp(self): pass
    def tearDown(self): pass

    def test_add_directory(self):
        """ Adding a directory to the watched dirs list """
        m = template.DirectoryWatcher()
        # Note: assumes tests are run from the project's root directory
        m.add_directory('tie/tests')
        self.assertEqual(os.path.dirname(__file__), m.dirs[0])

    def test_add_dirs_on_instanciation(self):
        """ Adding several watched directories on manager's instanciation """
        pathes = [
            'tie/tests/watched-templates',
            'doc',
            '.'
        ]
        m = template.DirectoryWatcher(*pathes)
        for i, d in enumerate(pathes):
            self.assertEqual(os.path.abspath(os.path.join(self.root_dir, d)), 
                             m.dirs[i])

    def test_valid_dirs(self):
        """ Only existing directory can be added to a DirectoryWatcher """
        m = template.DirectoryWatcher()
        self.assertRaises(IOError, m.add_directory, 'dummy/directory')

    def test_directory_insert_index(self):
        """ Inserting a directory with a custom index """
        pathes = [
            '.',
            'tie/tests'
        ]
        m = template.DirectoryWatcher()
        m.add_directory(pathes[0])
        m.add_directory(pathes[1], 0)
        for i, p in enumerate(reversed(pathes)):
            self.assertEqual(os.path.abspath(os.path.join(self.root_dir, p)),
                             m.dirs[i])

    def test_list_watched_templates(self):
        """ Listing templates from a watched directory (with recursion) """
        m = template.DirectoryWatcher(self.watched_dir)
        expected = sorted([
            os.path.abspath(os.path.join(self.root_dir, self.watched_dir, f)) 
                for f in ['foo.txt',
                          'subdir/dummy.txt',
                          'bar.txt', 
                          'baz.txt', 
                ]
        ])
        actual = sorted(list(m.list_watched_templates()))
        self.assertListEqual(expected, actual)

    def test_list_watched_templates_basenames(self):
        """ Get only templates' basenames when listing them """
        m = template.DirectoryWatcher(self.watched_dir)
        expected = sorted([
            'foo',
            'dummy',
            'bar', 
            'baz', 
        ])
        actual = sorted(list(m.list_watched_templates(basenames=True)))
        self.assertListEqual(expected, actual)

    def test_list_watched_templates_non_recursive(self):
        """ No recursion when listing templates if flag is false """
        m = template.DirectoryWatcher(self.watched_dir)
        m.recursive = False
        expected = sorted([
            os.path.abspath(os.path.join(self.root_dir, self.watched_dir, f))
                for f in ['foo.txt',
                          'bar.txt', 
                          'baz.txt', 
                    ]
        ])
        actual = sorted(list(m.list_watched_templates()))
        self.assertListEqual(expected, actual)

    def test_load_template(self):
        """ Load a templatefrom a watched directory """
        m = template.DirectoryWatcher(self.watched_dir)
        t = m._load_template('foo')
        self.assertEqual(t.name, 'foo')
        self.assertEqual(1, len(m._template_list))
        self.assertEqual(m._template_list[0].name, 'foo')

    def test_load_invalid_template(self):
        """ Raise TemplateError if trying to load an invalid template """
        m = template.DirectoryWatcher(self.watched_dir)
        self.assertRaises(template.TemplateError, m._load_template, 'oof')
        
    def test_get_loaded_template(self):
        """ Getting an already loaded template from a DirectoryWatcher """
        m = template.DirectoryWatcher(self.watched_dir)
        m.add(template.Template.from_file('tie/tests/watched-templates/foo.txt'))
        t = m.foo
        self.assertIsNotNone(t)
        self.assertEqual('foo', t.name)

    def test_get_non_loaded_template(self):
        """ Getting an unloaded template from a DirectoryWatcher """
        m = template.DirectoryWatcher(self.watched_dir)
        t = m.foo
        self.assertIsNotNone(t)
        self.assertEqual('foo', t.name)

    def test_get_template_error(self):
        """ Trying to get a non-existing template should raise a TemplateError """
        m = template.DirectoryWatcher(self.watched_dir)
        self.assertRaises(template.TemplateError, getattr, m, 'oof')

    def test_iteration(self):
        """ Load all templates on iteration """
        m = template.DirectoryWatcher(self.watched_dir)
        expected = sorted([
            'foo', 'dummy', 'bar', 'baz'
        ])
        actual = sorted([t.name for t in m])
        self.assertListEqual(actual, expected)
