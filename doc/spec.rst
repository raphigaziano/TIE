===
TIE
===

Template Illiterate Engine

Working documents. Goals, design notes, doc, etc...

.. contents::

Main Goal:
----------

This library is intended to be a simple templating **engine**.

Note the emphasis on engine: This will *not* provide any syntactical features 
(tags, functions, you name it...), but rather, a basic mechanism for users to 
define their own small templating language.

The goal here is definitely not to rival any existing TE, but rather to provide 
a way to simply and quickly define custom templating features.
For the simplest use case, this can be seen as nothing more than a convenience 
wrapper around python Template class or built-in string formatting capacities.
We hope to be abble to provide ways to define more powerful tags as well, but 
we'll focus at first on simple substitution features.
When THIS works, it might be nice to find a way to allow users to define a few 
"logical" tags, but this will not be a priority for a while.

TYPICAL USE CASES
~~~~~~~~~~~~~~~~~

Small templating needs. (TODO: fluff & exemples)

Focus (AKA What does that I stand for?)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TIE's T & E stand for Templating Engine, and that I in the middle is mostly 
there because I thought it'd make an awesome name.
I came up with the following terms to try and summarize what the library's
main goals should be.

- **ILLITERATE.** As stated above, it should be up to the user to define
  the syntax of his mini language. While TIE will provide a few helpers to
  manipulate the regular expressions which will define the language's tags,
  it won't try to impose any style on those.

- **INFLATABLE.** User defined templating mini languages should be easy
  to extend. It's up to the user to provide some kind of API to access
  his custom language or to hide it, but this should prove relatively
  easy to do.

- **INTUITIVE.** As long as you're not trying to do anything too fancy,
  defining a small syntax for your templating needs should take no more than
  calling a single function, yelling a bit at regular expressions and managing
  a few Template objects. 

  Developpement will focus on providing a convenient, easy to use api rather 
  than anything else.

- **INEFFICIENT?** Well, probably. This engine is intended for rather small 
  scale use cases, for which a regular template engine would be overkill.
  Trying to build a modern template language with it will surely prove very
  cumbersome and exhibit disastrous performances.
  
Implementation details, Ideas:
------------------------------

callbacks callbacks callbacks

- IDEA: optional definition of tags - mapping in a "config" declarative 
  file
- IDEA: optional TemplateManager to register templs by name (nice for
  inclusions, could serve as a cache) ?
  
  IF SO => Document a way to use with simple objects (simple strings, 
  stdlib Templates...), by wrapping with a callable object

- IDEA: Allow use of simple string patterns ?

API
~~~

- Template & Tag Classes
- register func (access to _TagManager???)
- regex helpers

Document user available api...

To document:
~~~~~~~~~~~~

- Python Regexes allow the re.compile() method flags to be replaced by
  special chars at the begining of the regex.
  If viable, advertize this as the way to register verbose regexes or 
  crap.
  
Doc:
----

- pyratemp
  Nice, small tmpl lang:
  http://www.simple-is-better.org/template/pyratemp.html#pyratemp-tool
  code:
  
  - pyratemp:
    http://www.simple-is-better.org/template/pyratemp-latest/pyratemp.py
  - pyratool:
    http://www.simple-is-better.org/template/pyratemp-latest/pyratemp_tool.py
  - thoughts:
    http://www.simple-is-better.org/template/index.html
