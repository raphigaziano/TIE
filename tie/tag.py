#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Tag classes and utilities.

Basic usage should only require the use of the register function.
Simple customization can be achieved by explicit instanciation or subclassing 
of the Tag class.
"""
import re
import logging

from tie import processors
from tie import utils

LOGGER = logging.getLogger(__name__)

class TagError(utils.TIEError): 
    """ Tag related Errors """
    pass
class InvalidTagError(TagError): 
    """ Invalid value to register a Tag object """
    pass

class TagManager(object):
    """
    Tag Container.
    Iterating over it will yield each contained tag in order of their 
    insertion.

    Tags are stored in a simple list. Eventual subclasses will need to
    redefine their access and __next__ method if they decide to use another
    data structure.
    """
    def __init__(self):
        self.tag_list = []

    def add(self, tag):
        """
        Register a new tag. 
        Override to accomodate a different internal data strucutre.
        """
        self.tag_list.append(self._check_tag(tag))
        LOGGER.debug("Added %s to %s" % (tag, self))

    def clear(self):
        """
        Clear the internal tag list.
        Override to accomodate a different internal data strucutre.
        """
        self.tag_list = []
        LOGGER.debug("%s has been cleared" % self)

    def __iter__(self):
        """
        Yield contained tags.
        Override to accomodate a different internal data strucutre.
        """
        for tag in self.tag_list:
            yield tag
    
    @staticmethod
    def _check_tag(tag):
        """
        Validate tha passed tag.
        Will convert a unicode string into a Tag Instance, and raise an
        InvalidTagError for any invalid type.
        """
        if isinstance(tag, utils.unicode):
            return Tag(tag)
        elif isinstance(tag, Tag):
            return tag
        else:
            raise InvalidTagError(
                    "Invalid tag %s of type %s" % (tag, type(tag))
            )


# TODO: Test me!
class PriorityTagManager(TagManager):
    """
    TagManager that keeps a priority value along its tags and yields them
    in that order.
    """
    def __init__(self):
        super(PriorityTagManager, self).__init__()
        self.tag_list = {}

    def add(self, tag):
        """
        Register a new tag. 
        tag should be a tupple (tag, priority). If not, priority will
        default to 0.
        """
        try:
            tag_obj, priority = tag
        except ValueError:
            tag_obj, priority = tag, 0
        tag_obj = self._check_tag(tag_obj)
        self.tag_list.setdefault(priority, []).append(tag_obj)
        LOGGER.debug("Added %s to %s" % (tag, self))

    def clear(self):
        """ Clear the internal tag list. """
        self.tag_list = {}
        LOGGER.debug("%s has been cleared" % self)

    def __iter__(self):
        """ Yield contained tags. """
        for i in sorted(self.tag_list.keys()):
            for tag in self.tag_list[i]:
                yield tag

# "Global" manager instance.
_manager = TagManager()

class Tag(object):
    """
    Custom, user defined template tag.
    Will detect matching placeholders in a given template and replace
    them with provided values.
    The user should not have to handle this process himself, but can
    provide callback functions to fine-tune a particular tag's processing and
    rendering.
    Altering the tag mathcing logic will require redefining the match method.
    """

    def __init__(self, pattern, flags=0, processor=processors.sub): 
        """
        Class initializer.
        :param pattern: Regular expression used for tag matching.
          Can be either a string or an already compiled regex object.
          See the python docs for more information on python's regular 
          expressions.
        :param flags: re module's flags for pattern compilation.
          Pass them just as you would when using the re.compile function.
        :param processor: Tag processing callback. Defaults to processors.sub.
        """
        self.regexp = re.compile(pattern, flags=flags)
        self.processor = processor

    def __repr__(self):
        """ Instance representation """
        return "<Tag %s>" % self.regexp.pattern

    def match(self, template):
        """
        Basic pattern matching.
        :param template: String template to match
        :returns: Iterator yielding found MatchObjects
        """
        return self.regexp.finditer(template)

    def process(self, template, **context):
        """
        Basic processing logic.
        Scans the template string for all occurences of the Tag and process
        those using the instance's own processor function.
        :param template: String template to process.
        :param **context: Keyword args will be passed to the Tag's processor
          function.
        :returns: Processed template.
        """
        out = template
        num_matches = 0
        for m in self.match(template):
            num_matches += 1
            src_tag = m.group(0)
            LOGGER.debug("%s matched %s" % (self, src_tag))
            val = self.processor(m, **context)
            LOGGER.debug("Substituting %s for %s" % (val, src_tag))
            # out = out.replace(src_tag, val)
            out = re.sub(src_tag, val, out)
        LOGGER.debug("Found %i matches for %s" % (num_matches, self))
        return out

### Module Level Utils ###
##########################

def get_manager():
    """ Return the global TagManager """
    return _manager

def set_manager(manager):
    """
    Set the global TagManager to manager. Only useful to setup a custom manager.
    """
    global _manager
    LOGGER.info("New Tag manager: %s" % manager)
    _manager = manager

def register(*tag_list):
    """
    Register a sequence of tags.
    :param *tag_list: List of tags to be registered, as positional arguments.
    """
    manager = get_manager()
    for tag in tag_list:
        manager.add(tag)
        LOGGER.info("Registered: %s" % tag)

