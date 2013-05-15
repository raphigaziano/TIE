Introdution
===========

.. note::
   The tie library is still a work in progress, and as such the api described 
   here is still subject to change. I'll do my best to keep changes to a 
   minimum after its first release, and more importantly to reflect those 
   changes in the documentation if and as they happen.

   Should you happen to notice any missing, outdated or plain wrong information,
   feel free to contact me through `github <https://github.com/raphigaziano>`_
   or via `email <r.gaziano@gmail.com>`_.

What is TIE ?
-------------

The tie library provides a set of classes and utilities to facilitate the
definition of very simple, personal template languages.

The library provides a basic, regex-based substitution engine, which doesn't
recognize any particular syntax by itself; it's up to the user to provide it
with his own tag patterns as well as their optional, custom behaviour.

tie also provides simple tools to ease the definition of those custom tags,
and aims to allow for easy customisation or extension (either by proviing
callbacks or by subclassing the provided types).

.. todo::
   Quick spec summary

Getting Started
---------------

.. todo::
   - pip install command
   - cloning instructions
   - link to tuts
