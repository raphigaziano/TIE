Tutorial
========

.. todo:: Tuts overview

.. contents::
   :local:
   :backlinks: top

Part I  - Simple substitution tags
----------------------------------

The naive way's shortcomings
++++++++++++++++++++++++++++

The :ref:`exemple <intro-overview>` shown in the overview might demonstrate
how simple using TIE can be, but defining tags in this way is a pretty bad
idea.

Indeed, consider what would happen if you used another template string:

.. testsetup:: naive-several-tag-occurences

   from __future__ import print_function
   import tie
   tie.tag.register("name")

.. doctest:: naive-several-tag-occurences

   >>> my_template = tie.Template("Hello, my name is name!")
   >>> my_template(name="raphi")
   'Hello, my raphi is raphi!'

.. testcleanup:: naive-several-tag-occurences

   tie.tag.get_manager().clear()

Your ``name`` tag matched *all* occurences of the word "name" in your template,
which is probably *not* what you wanted!

And, let's face it, this was to be expected. ``name`` is an awfull tag pattern -
In order for TIE to detect your placeholders more intelligently, they need to
contain some specific tokens that will help differentiate them from regular
words.
In order to be more flexible, TIE requires you to include those tokens in your
patterns yourself - But this also means that you should think carefully about
them to avoid that kind of confusion.

Let's decide that our tags should be surrounded by '%' characters to be detected.

.. testsetup:: naive-tokens

   from __future__ import print_function
   import tie
   tie.tag.get_manager().clear() # Doesn't seem to be executed in previous test cleanup ???

.. doctest:: naive-tokens

    >>> tie.tag.register("%name%")                              # Register our new tag pattern
    >>> my_template = tie.Template("Hello, my name is %name%!") # Use it in our template
    >>> my_template(name="raphi")                               # Does it work ???
    'Hello, my name is !'

Well shoot. Our tag apparently matched but it got replaced with a blank string 
instead of our custom data!

This is because when you call your :class:`Template <tie.template.Template>` 
object to render it, it receives your arguments as a dictionnary 
(this is the normal python behaviour for keyword arguments).
TIE's default behaviour is then to replace each detected tag with a matching
value from this dictionnary.
If it can't find it, it raises a warning and returns a blank string.

.. warning::

   The behaviour described above might change in future versions.

This means that in our case, our ``name`` argument and our ``%name%`` tag don't
match, which explains why the above code didn't work.

But... ``%name%`` is not a valid python identifier, is it ?

.. doctest:: naive-tokens

   >>> my_template(%name%="raphi")
   Traceback (most recent call last):
       ...
       my_template(%name%="raphi")
                    ^
   SyntaxError: invalid syntax

Nope, it isn't.

So, we need to define special tokens to identify our template tags,
but we can't use non-alphanumerical characters besides the underscore ?
Well, this sucks. And I thought this library claimed to be "flexible" ?

Don't worry. We just need to improve our tag just a little more.

.. note::

   Experienced Python users might be thinking of building the arguments 
   dictionary themselves and sending it with the splat operator, like this:

   ::

      my_template(**{"%name%": "raphi"}) # **Don't do this!**

   This will work, but is ugly as hell.
   Experienced or not, Python users shouldn't have to write such ugly code.

Regular expressions to the rescue !
+++++++++++++++++++++++++++++++++++

If you've never heard of regular expressions, then things might start to get
a bit hairy.
I'll try to explain how the first few ones we'll use in this tutorial work,
but you'll need to learn more about them to use TIE efficiently.
I suggest reading this `howto <http://docs.python.org/2/howto/regex.html>`_
from the python's documentation to get started.
Also, while you shouldn't need to use it directly, reading the standard library's
:mod:`re` module's reference might help you as well.



.. note::

   It's possible to use the :mod:`re` module's flags in your tags' regexes.
   To do so, you'll have to instanciate your
   :class:`Tag <tie.tag.Tag>` 
   objects explicitely and pass them to the 
   :func:`register <tie.tag.register>` 
   function, instead of simply passing the regex string, like so:

   ::

      import re
      import tie

      tie.tag.register(
         tie.Tag("^my_awesome_regex$", flags=re.FOO | re.BAR)
      )

More generic tags
+++++++++++++++++

Part II - Using external template files
---------------------------------------
