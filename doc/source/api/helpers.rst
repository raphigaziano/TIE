Helpers Module
==============

This module regroups various helper functions which you can use when defining
your custom processors or renderers.

Regular Expresssions Helpers:
-----------------------------

The following helpers are convenience shortcuts for manipulating regex matches
when handling custom tags.

.. function:: tie.helpers.get_single_group(match, key=1)

   Return one and only one group from the passed match object.
   If no group was defined in the matched regexp, return the whole match.

   Parameters:

   - ``match``:
      A re.match object to extract the group from.
   - ``key``:
      Optionnal key argument to get a specific group.
      This can be either a list index or a string to get a named group.
      (See the :meth:`re.MatchObject.group` method's documentation if you don't know
      how to get a specific group from a match object).
      Defaults to 1, to return the first defined group in the matching regex.
     
   
