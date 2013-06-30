Template module
===============

The tie.template module stores all the classes needed to represent your
template objects.

.. note::

   Only the base Template class is defined in here for now.
   
   TemplateManager basic classes will be defined here as well in a future
   release.

.. class:: tie.template.Template(tmpl, renderer=renderers.default_renderer)

   Template objects represent your template strings and provide ways to handle
   them easily.

   It uses a callback function (defaulting to
   :func:`renderers.default_renderer<tie.renderers.default_renderer>`)
   to handle the actual rendering, most of its public methods being convenience
   wrappers around it.
   Passing it another function on instantiation will allow you to alter this
   default processing, but the default function should be fine for most cases.

   .. todo:: LINK TO GUIDE ON CUSTOM TEMPLATES

   Parameters:

   - `tmpl`:     Template string, containing your defined tags.

   - `renderer`: Rendering callback.

   .. automethod:: tie.template.Template.render

   Override this method if you need some custom behiavour that can't be handled
   by a simple callback.

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

   .. method:: Template.from_file(tmpl_path, *args, **kwargs)
    
      Class method.

      This alternative constructor allows you to instanciate a template object
      directly from an external file.

      Simply pass it a valid file path instead of a template string, as well as
      any other argument required by the ``Template`` constructor, and a 
      ``Template`` instance initialized with the specified file's contents will
      be returned.

.. note::

   For convenience, the Template class is imported into TIE's global namespace,
   so you can just ``import tie.Template``.
