#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Tag processors tests
"""
import unittest
import warnings
import re

from tie import utils
from tie import processors

class TestProcessorSub(unittest.TestCase):

    def setUp(self): pass
    def tearDown(self): pass

    def test_basic_sub(self):
        """ Basic string substitution """
        match = re.search("%dummy%", "I am %dummy%, yay")
        res = processors.sub(match, **{"%dummy%": "raphi"})
        self.assertEqual("raphi", res)

    def test_single_group_match(self):
        """ Substitution for a single captured group """
        match = re.search("% (\w+) %", "I am % dummy %, yay")
        res = processors.sub(match, dummy="bob")
        self.assertEqual("bob", res)

    def test_named_group_match(self):
        """ Substitution for a single, named group """
        match = re.search("% (?P<tag>\w+) %", "I am % dummy %, yay")
        res = processors.sub(match, dummy="muddy waters")
        self.assertEqual("muddy waters", res)

    def test_convert_to_string(self):
        """ Substituted values should be converted to unicode strings """
        match = re.search("% (\w+) %", "I am % dummy %, yay")
        res = processors.sub(match, dummy=78)
        self.assertTrue(isinstance(res, utils.unicode))
        # TODO: moar type conversions

    def test_missing_arg(self):
        """ Missing context variable should be replaced by a blank string """
        # Will prolly need to be refactored
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            match = re.search("% (?P<tag>\w+) %", "I am % dummy %, yay")
            res = processors.sub(match)
            self.assertEqual("", res)

    def test_missing_arg_warning(self):
        """ Missing context variables should raise a ContextWarning """
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            match = re.search("% (?P<tag>\w+) %", "I am % dummy %, yay")
            res = processors.sub(match)
            self.assertEqual(1, len(w))
            self.assertEqual(w[-1].category, processors.ContextWarning)



