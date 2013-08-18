===
TIE
===

Template Illiterate Engine

.. image:: https://www.travis-ci.org/raphigaziano/TIE.png?branch=master,develop
    :target: https://www.travis-ci.org/raphigaziano/TIE

.. image:: https://pypip.in/v/TIE/badge.png
    :target: https://crate.io/packages/$REPO/
    :alt: Latest PyPI version

.. image:: https://pypip.in/d/TIE/badge.png
    :target: https://crate.io/packages/$REPO/
    :alt: Number of PyPI downloads

.. image:: https://raw.github.com/raphigaziano/TIE/master/TIE.jpg
   :alt: Twin Ion Engine of Awesomeness
   :align: center
   :scale: 50 %

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

You can install TIE by simply using pip (this is the recomanded way):

::

   pip install tie

If you must, you can also use easy_install:

::

   easy_install tie

Alternativeley, you could also clone the project's repository and run the 
setup script:

::

   git clone https://github.com/raphigaziano/TIE
   cd TIE/
   python setup.py install

Getting Started
---------------

For most basic uses, rendering a template with TIE involves 3 simple steps:

  - Register your tag patterns
  - Wrap your template(s) text in (a) Template object(s)
  - Pass your templates the data they need to render them

A naive exemple could look like this:

.. code-block:: python

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

Read the (still incomplete)
`Full documentation <https://tie.readthedocs.org/en/latest/index.html>`_
hosted on readthedocs.

