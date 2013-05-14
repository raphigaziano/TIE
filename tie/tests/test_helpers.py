#!/usr/bin/env python
#-*- coding:utf-8 -*-
""" Helper functions tests """
import unittest
import re

from tie import helpers

class TestRegexHelpers(unittest.TestCase):
    """ Tests for regex helpers """
    def setUp(self): pass
    def tearDown(self): pass

    def test_get_sinle_group(self):
        """ Basic usage of get_single_group """
        m = re.search("% (\w+) %", "dumdummy % test % mudmud")
        self.assertEqual("test", helpers.get_single_group(m))

    def test_get_single_group_no_groups(self):
        """ get_single_group should return the whole match if no group is defined """
        m = re.search("% test %", "dumdummy % test % mudmud")
        self.assertEqual("% test %", helpers.get_single_group(m))
        # invalid key should be ignored
        self.assertEqual("% test %", helpers.get_single_group(m, 32))

    def test_get_single_group_several(self):
        """ get_single_group with several groups defined """
        m = re.search("% (\w+) (\w+) %", "dumdummy % test foo % mudmud")
        self.assertEqual("test", helpers.get_single_group(m, 1))
        self.assertEqual("foo",  helpers.get_single_group(m, 2))

    def test_get_single_group_several_groups_no_key(self):
        """ get_single_group should default to the first group if several are defined """
        m = re.search("% (\w+) (\w+) %", "dumdummy % test foo % mudmud")
        self.assertEqual("test", helpers.get_single_group(m))

    def test_get_single_group_named_groups(self):
        """ get_single_group should work the same with named groups """
        m = re.search("% (?P<tag>\w+) (?P<val>\w+) %",
                      "dumdummy % test val % mudmud")
        self.assertEqual("test", helpers.get_single_group(m, "tag"))
        self.assertEqual("test", helpers.get_single_group(m))
        self.assertEqual("val",  helpers.get_single_group(m, "val"))
        self.assertEqual("val",  helpers.get_single_group(m, 2))

