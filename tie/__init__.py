#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
The tie library provides a set of classes and utilities to facilitate the 
definition of very simple, personal template languages.

The library provides a basic, regex-based substitution engine, which doesn't 
recognize any particular syntax by itself; it's up to the user to provide it
with his own tag patterns as well as their optional, custom behaviour.

tie also provides simple tools to ease the definition of those custom tags, and 
aims to allow for easy customisation or extension (either by proviing callbacks 
or by subclassing the provided types).

Author:  raphi <r.gaziano@gmail.com>
Created: 18/04/2013
"""
from __future__ import unicode_literals

import logging

### Submodules Imports ###

from tie import tag, template
from tie.tag import Tag, register
from tie.template import Template
from tie.exceptions import *

### Logging Setup ###

# For py26 compat, create a NullHandler
if hasattr(logging, 'NullHandler'):
    NullHandler = logging.NullHandler
else:
    class NullHandler(logging.Handler):
        def handle(self, record):
            pass

        def emit(self, record):
            pass

        def createLock(self):
            self.lock = None

logging.getLogger('tie').addHandler(NullHandler())
# TEMPO
# stream_handler = logging.StreamHandler()
# fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
# stream_handler.setFormatter(logging.Formatter(fmt))
# logging.getLogger('tie').addHandler(stream_handler)
# logging.getLogger('tie').setLevel(logging.DEBUG)
