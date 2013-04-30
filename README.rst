===
TIE
===

Template Illiterate Engine

.. image:: https://raw.github.com/raphigaziano/TIE/master/TIE.jpg
   :alt: Twin Ion Engine of Awesomeness
   :align: center
   :scale: 50 %

.. contents::

The tie library provides a set of classes and utilities to facilitate the 
definition of very simple, personal template languages.

The library provides a basic, regex-based substitution engine, which doesn't 
recognize any particular syntax by itself; it's up to the user to provide it
with his own tag patterns as well as their optional, custom behaviour.

tie also provides simple tools to ease the definition of those custom tags, and 
aims to allow for easy customisation or extension (either by proviing callbacks 
or by subclassing the provided types).

Basic Usage
-----------

Register your tags:

.. code:: python

  from tie import tag

  tag.register(
      "%(title)%",
      "{{ (\w+) }}"
  )

Instanciate a template:

.. code:: python

  from tie import template

  my_template = template.Template("""
    %title%
    Hi! my name is {{ name }}
    and i'm {{ age }} years old!
    yay!
    """)

Render it!

.. code:: python

  my_rendered_template = my_template(title="TIE IS EVIL", name="Raphi", age=26)
  # Now my_rendered_template is:
  """
  TIE IS EVIL
  Hi! my name is Raphi
  and i'm 26 years old!
  yay!
  """

TODO
----

- **DOC** (including this readme)
- Cleanup spec & code
- Regex helpers
- Moar tests (integration)
- Release v0.1

for more info on the lib's goals, see doc/spec.rst.
