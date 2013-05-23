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
   which you can customize you need it to behave differently.

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

   Internally, this function simply hands each of its parameters to the current
   :class:`TagManager<tie.tag.TagManager>`
   and lets it handle the registration process.
   Actual error checking is done in the :class:`Tag<tie.tag.Tag>`
   's constructor.

.. class:: tie.tag.Tag(pattern, flags=0, processor=tie.processors.sub)

   blaaa

   .. automethod:: match

   .. automethod:: process

.. note::

   For convenience, the Tag class is imported into TIE's global namespace,
   so you can just `import tie.Tag`.


TEST

.. autoclass:: tie.tag.PriorityTagManager
   :show-inheritance:
