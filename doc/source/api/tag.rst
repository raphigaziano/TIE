Tag module
==========

The tie.tag module exposes the functions needed to manage your tag patterns,
as well as the base classes needed to customize their behaviour or the way
they will be managed in your application.

Module's Top level Classes & Utilities
--------------------------------------

.. autofunction:: tie.tag.register

   Call this function and pass it an arbitrary number of tags to register them
   with TIE.

   Since your Tag list is needed by various internal parts of the TIE library,
   you **must** use this function in order for them to have any effect. TIE
   stores them in a default :class:`TagManager<tie.tag.TagManager>` instance,
   which you can replace if you need it to behave differently (See below).

   Each `tag` parameter should be either a string of the tag's regular
   expression (or an already compiled regex object), or an instance
   of :class:`Tag<tie.tag.Tag>` (or of any class inheriting from it).
   Instanciating your Tag objects manually allows you to adjust their behaviour,
   either by tweaking their default parameters or by using a custom subclass:

   ::

      tie.tag.register(
          "sometagpattern",
          tie.Tag("anothertag", processor=FOO),
          MyCustomTagSubclass("taggytagtag"),
          ...
      )

   Internally, this function simply hands each of its parameters to the current
   :class:`TagManager<tie.tag.TagManager>`
   and lets it handle the registration process.
   Actual error checking is done in the :class:`Tag<tie.tag.Tag>`
   's constructor.

   .. note::

      The actual arguments expected by `register` might vary if you decide to
      use a different :class:`TagManager<tie.tag.TagManager>`.
      For instance, a :class:`PriorityTagManager<tie.tag.PriorityTagManager>`
      will expect tuples of (tag, priority).
      `register` will simply pass each item it receives to the current manager;
      see their documentation, as well as the one for any custom Tag class you 
      might use, to know for certain how you should register your tag patterns.

.. class:: tie.tag.Tag(pattern, flags=0, processor=tie.processors.sub)

   The Tag class is TIE's central component.

   It's a somewhat boosted regular expression object, which knows how to match
   itself against a given template, and modify each occurence of its pattern 
   within the template's text using its internal `processor` function.

   TIE takes care of managing and handling its registered Tag object, but 
   instanciating them manually allows one to change their default behaviour
   by providing a custom callback as the `processor` argument. (Default 
   processors callbacks are defined in the :mod:`tie.processors` module.)

   If further customisation is needed, feel free to override its public methods
   in a subclass.

   Parameters:

   - `pattern`:   Regular expression used for tag matching.
                  This can be either a normal string or an already compiled
                  regular expression.
   - `flags`:     :mod:`re` module's flags for pattern compilation.
                  Pass them just as you would when using the 
                  :func:`re.compile` function.
   - `processor`: Tag processing callback.
                  Processor function should accept a :class:`match` object as
                  their first parameter, and a dictionnary of keyword arguments
                  containing the context variables available for processing.
                  
                  For more information about tag processors, see this
                  HOWTO on tags customization (once its there, that is...)

   .. todo:: Link to custom tags guide

   .. automethod:: match

   .. automethod:: process

.. note::

   For convenience, the Tag class is imported into TIE's global namespace,
   so you can just ``import tie.Tag``.

Managers
--------

TIE uses an internal manager object to keep track of every registered tag.
It will use a basic :class:`TagManager<tie.tag.TagManager>` instance by default,
which should be able to handle the simplest use cases, so that you don't have
to worry about those if you don't need to.

It also provides a few specialized managers with commonly needed special
behaviour. If you need tighter control on how your tags should be stored and
handled, you can also define and use your own 
:class:`TagManager<tie.tag.TagManager>` subclass.

The :mod:`tie.tag` module exposes the two following functions to set or 
access the current manager:

.. autofunction:: tie.tag.set_manager

.. autofunction:: tie.tag.get_manager

.. note::

   Since the :func:`register<tie.tag.register>` function appends the tags it
   receives to the current manager, it should only be called after setting any
   custom one.

.. warning::

   Unlike Template Managers, which are completely optionnal, most of TIE's
   internal objects *require* a global TagManager instance to be set in order 
   to be able to perform their tasks. While it is possible to bypass
   calling the :func:`get_manager<tie.tag.get_manager>` function when using a 
   non-default manager if you also tweak these objects, doing so will probably 
   bypass most of TIE's convenience as well.

TIE comes with the following managers:

.. class:: tie.tag.TagManager

   A basic :class:`Tag<tie.tag.Tag>` container to keep track of registered 
   tags. TIE will use this manager by default.
   You can iterate over it to retrieve individual tags -- Those will be yielded
   in the order of their insertion:

   .. testsetup:: manager-iteration

      from __future__ import print_function
      import tie
      tie.tag.get_manager().clear()

   .. doctest:: manager-iteration

      >>> tie.tag.register('pattern2',
      ...                  'pattern1',
      ...                  'pattern3'
      ... )
      >>> manager = tie.tag.get_manager()
      >>> for tag in manager:
      ...     print(tag)
      ... 
      <Tag 'pattern2'>
      <Tag 'pattern1'>
      <Tag 'pattern3'>

   Tags are stored in a simple list, in a "private" ``_tag_list`` attribute. 
   Subclasses will probably need to override this attribute in order to use
   other data structures.

   .. automethod:: tie.tag.TagManager.add

      This method is called by the :func:`register<tie.tag.register>` function.

   .. automethod:: tie.tag.TagManager.clear

   .. automethod:: tie.tag.TagManager.__iter__

   .. method:: tie.tag.TagManager._check_tag(tag, cls=tie.tag.Tag)

      Internal checking method, called before inserting any tag to the
      manager's tag list.
      It simply passes its ``tag`` parameter to the ``cls`` constructor if
      ``tag`` is not already an instance (or subclass) of it -- 
      This is what allows you to pass either regular strings or
      :class:`Tag<tie.tag.Tag>` instances to the 
      :func:`register<tie.tag.register>` function.
      
      Actual error handling is left to the called constructor.

      You might need to override this method if you're using fancier Tag 
      objects. If not, you should probably still remember to call it before
      inserting your tags when redefining the
      :func:`add<tie.tag.TagManager.add>` method.

Moar specialized managers provided by TIE are listed below:

.. autoclass:: tie.tag.PriorityTagManager
   :show-inheritance:

   Tags with the lowest priority value will be yielded first:

   .. testsetup:: priority-ordering

      from __future__ import print_function
      import tie
      tie.tag.get_manager().clear()

   .. doctest:: priority-ordering

      >>> tie.tag.set_manager(tie.tag.PriorityTagManager())
      >>> tie.tag.register(
      ...     ('sometag', 2),
      ...     ('othertag', 0),
      ...     ('taggytag', 1),
      ... )
      >>> manager = tie.tag.get_manager()
      >>> for tag in manager:
      ...     print(tag)
      ...
      <Tag 'othertag'>
      <Tag 'taggytag'>
      <Tag 'sometag'>

   .. testcleanup:: priority-ordering
      
      tie.tag.set_manager(tie.tag.TagManager())

   .. automethod:: tie.tag.PriorityTagManager.add
   .. automethod:: tie.tag.PriorityTagManager.clear

