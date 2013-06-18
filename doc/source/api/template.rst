Template module
===============

The tie.template module stores all the classes needed to represent your
template objects.

.. note::

   Only the base Template class is defined in here for now.
   
   TemplateManager basic classes will be defined here as well in a future
   release.

.. class:: tie.template.Template(tmpl, renderer=renderers.default_renderer)

   .. todo:: Class doc & __init__

   .. automethod:: tie.template.Template.render

   .. automethod:: tie.template.Template.__call__

    This is what allows you to simply call your template objects directly:

    ::

        >>> t = Template("Hello, %name%!")
        >>> res = t(name="Santa")
        >>> print(res)
        'Hello, Santa!'

    is equivalent to:

    ::

        >>> t = Template("Hello, %name%!")
        >>> res = t.render(name="Santa")
        >>> print(res)
        'Hello, Santa!'

   .. automethod:: tie.template.Template.from_file

.. note::

   For convenience, the Template class is imported into TIE's global namespace,
   so you can just ``import tie.Template``.
