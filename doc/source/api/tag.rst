Tag module
==========

.. todo:: Module intro (Tag)

Module's Top level Classes & Utilities
--------------------------------------

.. autofunction:: tie.tag.register

   Call this function and pass it an arbitrary number of tags to register them
   with TIE.

   Since your Tag list is needed by various internal parts of the TIE library,
   you **must** use this function in order for them to have any effect. TIE
   stores them in a default :class:`TagManager<tie.tag.TagManager>` instance,
   which you can customize if you need it to behave differently (See below).

   Each `tag` parameter should be either a string of the tag's regular
   expression (or an already compiled regex object), or an instance
   of :class:`Tag<tie.tag.Tag>` (or of any class inheriting from it).

   ::

      tie.tag.register(
          "sometagpattern",
          tie.Tag("anothertag", processor=FOO),
          MyCustomTagSubclass("taggytagtag"),
          ...
      )

   .. note::

      The actual arguments expected by `register` might vary if you decide to
      use a different :class:`TagManager<tie.tag.TagManager>`.
      For instance, a :class:`PriorityTagManager<tie.tag.PriorityTagManager>`
      will expect tuples of (tag, priority).
      `register` will simply pass each item it receives to the current manager;
      see their documentation, as well as the one for any custom Tag class you 
      might use, to know for certain how you should register your tag patterns.

   Internally, this function simply hands each of its parameters to the current
   :class:`TagManager<tie.tag.TagManager>`
   and lets it handle the registration process.
   Actual error checking is done in the :class:`Tag<tie.tag.Tag>`
   's constructor.

.. class:: tie.tag.Tag(pattern, flags=0, processor=tie.processors.sub)

   The Tag class is TIE's central component.

   It's a somewhat boosted regular expression object, which knows how to look
   for itself against a given template, and calls its `processor` function with
   each match.

   TIE takes care of managing and handling its registered Tag object, but 
   instanciating them manually allows one to change their default behaviour
   by providing a customm callback as the `processor` argument.

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
   so you can just `import tie.Tag`.

Managers
--------

blaaaaa

.. autofunction:: tie.tag.set_manager

.. autofunction:: tie.tag.get_manager

.. autoclass:: tie.tag.TagManager
   :members:

   .. automethod:: classmethod _check_tag(tag, :class:`Tag<tie.tag.Tag`

.. autoclass:: tie.tag.PriorityTagManager
   :show-inheritance:
   :members:

