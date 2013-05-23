Tutorial
========

.. todo:: Tuts overview

.. contents::
   :local:
   :backlinks: top

Part I   - Simple substitution tags
-----------------------------------

The naive way's shortcomings
++++++++++++++++++++++++++++

The :ref:`exemple <intro-overview>` shown in the overview might demonstrate
how simple using TIE can be, but defining tags in this way is a pretty bad
idea.

Indeed, consider what would happen if you used another template string:

.. testsetup:: naive-several-tag-occurences

   from __future__ import print_function
   from __future__ import unicode literals
   import tie
   tie.tag.register("name")

.. doctest:: naive-several-tag-occurences

   >>> my_template = tie.Template("Hello, my name is name!")
   >>> my_template(name="raphi")
   'Hello, my raphi is raphi!'

.. testcleanup:: naive-several-tag-occurences

   tie.tag.get_manager().clear()

Your `name` tag matched *all* occurences of the word "name" in your template,
which is probably *not* what you wanted!

And, let's face it, this was to be expected. `name` is an awfull tag pattern -
In order for TIE to detect your placeholders more intelligently, they need to
contain some specific tokens that will help differentiate them from regular
words.
In order to be more flexible, TIE requires you to include those tokens in your
patterns yourself - But this also means that you should think carefully about
them to avoid that kind of confusion.

Let's decide that our tags should be surrounded by '%' characters to be detected.

.. testsetup:: naive-tokens

   from __future__ import print_function
   from __future__ import unicode literals
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

This means that in our case, our ``name`` argument and our `%name%` tag don't
match, which explains why the above code didn't work.

But... `%name%` is not a valid python identifier, is it ?

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

One of the neat things about regular expressions is that they allow you to
capture specific parts, or "groups", of the matching string.
If you define one such group in your pattern, TIE will try to match your context 
variables against it, instead of using the whole tag.

The simplest way to define a group is simply to surround in with parenthesis.
(You can also use another syntax to assign names to your groups. While this can
come in handy, there's no real need to do so in our situation, so we'll settle
for an anonymous group for the sake of readability.)

Let's try this:

.. testsetup:: simple-regex

   from __future__ import print_function
   from __future__ import unicode literals
   import tie
   tie.tag.get_manager().clear()

.. doctest:: simple-regex

   >>> tie.tag.register("%(name)%")
   >>> my_template = tie.Template("Hello, my name is %name%!")
   >>> my_template(name="raphi")
   'Hello, my name is raphi!'

Hurrah! This lib might not be so useless after all!

While you can get more fancy, this is really all you have to understand to
start using TIE. 
As long as you include appropriate tokens [#f1]_ in your patterns, 
and remember to define a group that can match the variables names you'll be
using in your code, 
you're ready to start defining a simple template language using arbitrary tags.

But, as far as regular expressions go, `%(name)%` is about as simple as it gets.
If you've ever used regexes, then you know that they can be far more powerful
(and far less readable ;)) than this.

Let's see if we can tweak our tag further...

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

.. [#f1] What's an appropriate token? Well, it all depends on the context in
         which you plan to use your template tags. If generating html documents,
         surrounding your tags with angle brackets (`<>`) might not be the best 
         idea...

         Just take some time to think about it and use some common sense.
         Typical patterns could look like the ones we're defining in this
         tutorial (`%my_tag%`), or like the ones used by the django and Jinja2
         template engines (`{{ my_tag }}`).

More generic tags
+++++++++++++++++

So, now that we know how to define better template tags, let's register 
another one:

.. doctest:: simple-regex

   >>> tie.tag.register(    # Notice that you can pass an arbitrary number
   ...     "%(name)%",      # of patterns to register them all at once
   ...     "%(age)%"
   ... )
   >>> my_template = tie.Template("Hello, my name is %name% and I'm %age% years old!")
   >>> my_template(name="raphi", age=26)
   "Hello, my name is raphi and I'm 26 years old!"
   
Yup, still works. And as a bonus, you might have noticed that we passed the
``age`` argument as an integer value, and not as a string.
TIE is just smart enough to call the ``__str__`` method of the objects it's 
asked to process in order to display them. 
Keep that in mind if you plan on sending custom objects to your templates.

We still have to register a new pattern for every tag we want to support.
This is perfectly fine if you want to allow only a limited set of template
tags - sometimes you need tight control over what can or can't go in your 
templates, and explicitely defining each tag in this way will help you manage
what's going on.

But still, wouldn't it be nice if we could let TIE match any arbitrary argument
we might send it ? Get rid of the `%name%` and `%age%` tags and instead, have
some kind of generic `%<var>%` tag that would match whatever context argument 
happened to be referenced between those two percent signs ?

Remember. While the ones we've used so far didn't look like much, our tag
patterns are still regular expressions. Knowing this, and assuming you've
read up a bit on those, the solution becomes trivial:

.. testsetup:: generic-regex

   from __future__ import print_function
   from __future__ import unicode literals
   import tie
   tie.tag.get_manager().clear()

.. doctest:: generic-regex

   >>> tie.tag.register("%(\w+)%")
   >>> my_template = tie.Template("Hello, my name is %name% and I'm %age% years old!")
   >>> my_template(name="raphi", age=26)
   "Hello, my name is raphi and I'm 26 years old!"
   
.. todo:: explain regex a bit + short conclusion

Part II  - Managing your templates
----------------------------------

While it's allright to define your template strings directly in your code for
very simple use cases such as the ones we've covered so far,
real world applications should enforce a better 
`separation of concerns <http://en.wikipedia.org/wiki/Separation_of_concerns>`_
and store their templates in external files.
Think `MVC <http://en.wikipedia.org/wiki/Model-view-controller>`_:
Your presentation layer (which most templating systems will be be a part of)
should always be kept cleanly separated from the rest of your code.

While you can certainly manage these external files yourself, TIE provides some
handy shortcuts to help you keep your presentation layer 

Let's have a look at those and start using some best-practices before diving in 
any further.

Using external template files
+++++++++++++++++++++++++++++

Fire up your favourite editor and start designing a simple template.
I'll use a pretty minimal one, and save it as `test_template.txt`:

::

   Hello, world!
   My name is %name%,
   and I'm %age% years old!
   Yay!

Now, back to your python code.

You could use the python builtin :func:`open` function to read your new
template file and pass its contents to the 
:class:`Template <tie.template.Template>`'s constructor,
but the class provides a handy factory method to handle this for you:

.. testsetup:: external-template

   import os
   os.chdir('exemples')

   import tie
   tie.tag.get_manager().clear()
   tie.tag.register("%(\w+)%")

.. doctest:: external-template

   >>> my_template = tie.Template.from_file("test_template.txt")
   >>> res = my_template(name="Eddie", age=21)
   >>> print(res)
   Hello, world!
   My name is Eddie,
   and I'm 21 years old!
   Yay!
   <BLANKLINE>
   
Just provide a valid path to your template and it will take care of 
instanciating itself from its contents,
allowing you to avoid some clutter and focus on more important stuff.

Register your templates to a manager
++++++++++++++++++++++++++++++++++++

Since template managers are a nice, but rather optional feature, they haven't
been implemented yet.

I do plan to add them soon, so check back in a while for them!

Part III - Custom Tag behaviour
-------------------------------

Coming soon!
