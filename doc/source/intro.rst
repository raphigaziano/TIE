Introduction
============

.. contents::
   :local:
   :backlinks: top

What is TIE ?
-------------

The TIE library provides a set of classes and utilities to facilitate the 
definition of very simple, personal template languages.

The library provides a basic substitution engine based on regular expressions, 
which doesn't recognize any particular syntax by itself; it's up to the user to 
provide it with his own tag patterns as well as their optional, custom 
behaviour.

TIE also provides simple tools to ease the definition of those custom tags,
and aims to allow for easy customisation or extension (either by providing
callbacks or by subclassing the provided types).

Do I need it ?
--------------

Maybe. Maybe not.

If you need a full-fledged template engine,
with lots of features and good performances,
then TIE is probably not for you.
You'll be far better off using an already established template language -
`Quite a lot of them <http://wiki.python.org/moin/Templating>`_ are already 
part of the python ecosystem and have more than proven themselves.
Trying to emulate one of those with TIE *might* be possible,
but will surely prove very cumbersome and inneficient.

.. note::

  If you're looking for a lightweight, but more featured template engine, I'd
  like to recommend
  `pyratemp <http://www.simple-is-better.org/template/pyratemp.html>`_.
  I like the author's "simple is better" philosophy, and his
  `thoughts on template engines <http://www.simple-is-better.org/template/>`_ 
  have been a nice source of inspiration for TIE.
    
On the other hand, TIE might still be overkill if your requirements are very
simple.
Python's batteries include a very nice and quite powerful string formatting syntax,
and also provides a Template class for slightly more complex operations. 
Those built-in features might be more than sufficient for what you have in mind. 
(See http://docs.python.org/2/library/string.html for more info on python's 
string operations.)

TIE aims to step in when python's built-in tools might be enough for the job, 
but become too unwieldy to handle the task in a straight-forward way.

Installation
------------

.. todo::
   - pip install command
   - cloning instructions

.. _intro-overview:

Getting Started
---------------

For most basic uses, rendering a template with TIE involves 3 simple steps:

  - Register your tag patterns
  - Wrap your template(s) text in (a) Template object(s)
  - Pass your templates the data they need to render them

A naive exemple could look like this:

.. testsetup::

   from __future__ import print_function

>>> import tie
>>> # Register a tag pattern
>>> tie.tag.register("name")
>>> # Instanciate a Template object
>>> my_template = tie.Template("Hello, name!")
>>> # Render it!
>>> res = my_template(name="raphi")
>>> print(res)
Hello, raphi!
>>> res = my_template(name="Darth Vader, lord of the sith")
>>> print(res)
Hello, Darth Vader, lord of the sith!

.. note::

   For testing purposes, I'm using the python 3 print function here,
   but this should work just as well with the python 2.x syntax. 
   Adjust the code accordingly, or add a
   ``from __future__ import print_function`` statement before running this code.

While this exemple is way too simple to be useful, 
the basic process it illustrates should be able to handle a lot of common 
situations.

Head on to the :doc:`TIE tutorial <tutorial>` to start using TIE the right way !
