Processors Module
=================

This module stores all the callback functions provided by TIE and used to
process matching tags in a template.

.. note:: Only one function, the default ``sub`` processor, is defined for now.

.. autofunction:: tie.processors.sub

   This processor performs a simpe substitution on the processed tag.
   It will check for a value matching the current tag within the ``context``
   dictionnary and return it, or an empty string if no match was found.

   .. warning:: 
      The "no match found" behaviour is still undefined.
      For now it simply raises a warning and return an empty value, so that the 
      tag will simply be suppressed.

Custom processors:
------------------

.. todo:: Renderer "protocol" summary
